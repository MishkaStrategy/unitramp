#!/usr/bin/env python3
import argparse
import html
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

BASE = "https://unitramp.ru"
CATALOG = f"{BASE}/katalog/"
UA = "UnitRamp redesign catalog synchronizer/1.0 (+https://github.com/MishkaStrategy/unitramp)"

LABEL_TO_KEY = {
    "игровые комплексы для помещений": "igrovye-kompleksy",
    "детские игровые лабиринты": "labirinty",
    "вертикальные лабиринты": "labirinty",
    "уличные игровые лабиринты": "labirinty",
    "веревочные лабиринты": "labirinty",
    "батутные арены": "batutnye-areny",
    "горки-косогоры": "slope",
    "тюбинговые горки": "tubing",
    "сухие аквапарки": "dry",
    "интерактивное оборудование": "interactive",
    "ниндзя-парки": "nindzya",
    "полосы препятствий ниндзя": "nindzya",
    "горки-вулканы": "volcano",
    "детские игровые комнаты": "rooms",
    "батутное оборудование": "trampoline-equipment",
    "профессиональные спортивные батуты": "trampoline-equipment",
    "сетки для батута коммерческие": "trampoline-equipment",
    "сетки для спортивных батутов": "trampoline-equipment",
    "пружины для батута": "trampoline-equipment",
    "обкладочные маты для батута": "trampoline-equipment",
    "зоны приземления и надувные подушки": "trampoline-equipment",
    "заградительные и страховочные сетки для батута": "trampoline-equipment",
    "баскетбольная зона для батутной арены slam ball": "trampoline-equipment",
    "прочее оборудование для батутного центра": "trampoline-equipment",
    "скалодромы": "climbing",
    "акробатические надувные дорожки": "airtrack",
    "акробатические надувные дорожки и ковры": "airtrack",
    "детские карусели": "carousel",
    "мягкие модули": "soft",
    "маты и покрытия для залов": "mats",
}

CONTROL_TEXT = {
    "уточнить цену", "заказать", "подробнее", "в корзину", "в корзине",
    "получить прайс", "получить прайс на", "показать больше товаров",
    "все проекты", "смотреть все", "читать далее", "купить", "рассчитать",
}

KEY_ORDER = [
    "igrovye-kompleksy", "labirinty", "batutnye-areny", "slope", "tubing",
    "dry", "interactive", "nindzya", "volcano", "rooms",
    "trampoline-equipment", "climbing", "airtrack", "carousel", "soft", "mats",
]


def clean(value):
    return re.sub(r"\s+", " ", (value or "").replace("\xa0", " ")).strip()


def label_key(value):
    t = clean(value).lower().replace('"', '').replace("«", "").replace("»", "")
    t = re.sub(r"\s+\d+\s+(товар(?:а|ов)?|товары?)$", "", t).strip()
    return LABEL_TO_KEY.get(t)


def normalize_url(href):
    if not href:
        return None
    url = urljoin(BASE, href)
    p = urlparse(url)
    if p.netloc not in {"unitramp.ru", "www.unitramp.ru"}:
        return None
    path = re.sub(r"/{2,}", "/", p.path)
    if not path.startswith("/katalog/"):
        return None
    if path != "/katalog/" and not path.endswith("/"):
        path += "/"
    return urlunparse(("https", "unitramp.ru", path, "", "", ""))


def fetch(session, url, retries=3):
    error = None
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=25, headers={"User-Agent": UA})
            r.raise_for_status()
            return r.text
        except Exception as exc:
            error = exc
            time.sleep(1.2 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {error}")


def discover_pages(session):
    root_html = fetch(session, CATALOG)
    soup = BeautifulSoup(root_html, "html.parser")
    pages = {}
    nav_urls = {CATALOG}
    for a in soup.find_all("a", href=True):
        key = label_key(a.get_text(" ", strip=True))
        url = normalize_url(a.get("href"))
        if key and url:
            pages[url] = key
            nav_urls.add(url)
    # Crawl discovered category pages once to discover subcategories that may not be exposed in root HTML.
    for url, inherited_key in list(pages.items()):
        try:
            sub = BeautifulSoup(fetch(session, url), "html.parser")
        except Exception as exc:
            print(f"WARN category discovery {url}: {exc}", file=sys.stderr)
            continue
        for a in sub.find_all("a", href=True):
            key = label_key(a.get_text(" ", strip=True))
            child = normalize_url(a.get("href"))
            if key and child:
                pages.setdefault(child, key)
                nav_urls.add(child)
    return pages, nav_urls


def meaningful_name(text):
    t = clean(text)
    low = t.lower()
    if not t or len(t) < 3 or len(t) > 180:
        return False
    if low in CONTROL_TEXT or low.startswith("получить прайс"):
        return False
    if re.fullmatch(r"\d+", t):
        return False
    if "товар" in low and len(t) < 80:
        return False
    return True


def nearest_card_data(anchor, name):
    best = ""
    best_node = None
    node = anchor
    for _ in range(7):
        node = getattr(node, "parent", None)
        if node is None:
            break
        text = clean(node.get_text(" ", strip=True))
        if name in text and len(text) <= 1200 and ("₽" in text or "Уточнить цену" in text or "Размер" in text or "Площадь" in text):
            if not best or len(text) < len(best):
                best, best_node = text, node
    price = "Уточнить цену"
    if best:
        m = re.search(r"((?:от\s*)?[\d\s]+\s*₽(?:\s*за\s*кв\.?\s*м)?)", best, re.I)
        if m:
            price = clean(m.group(1))
    size = ""
    if best:
        m = re.search(r"(?:Размер(?:ы)?|Площадь(?: комплекса)?)[\s:]*(.{2,80}?)(?=(?:от\s*)?[\d\s]+\s*₽|Уточнить цену|$)", best, re.I)
        if m:
            size = clean(m.group(1)).strip(" .,:;-")[:100]
    image = ""
    if best_node:
        img = best_node.find("img")
        if img:
            raw = img.get("data-src") or img.get("data-original") or img.get("src") or ""
            if raw and not raw.startswith("data:"):
                image = urljoin(BASE, raw)
    return price, size, image


def crawl_catalog(session):
    pages, nav_urls = discover_pages(session)
    print(f"Discovered {len(pages)} category/subcategory pages")
    products = {}
    category_failures = []
    for index, (page_url, cat_key) in enumerate(sorted(pages.items()), 1):
        try:
            page_html = fetch(session, page_url)
        except Exception as exc:
            category_failures.append({"url": page_url, "error": str(exc)})
            print(f"WARN [{index}/{len(pages)}] {page_url}: {exc}", file=sys.stderr)
            continue
        soup = BeautifulSoup(page_html, "html.parser")
        found_here = 0
        for a in soup.find_all("a", href=True):
            url = normalize_url(a.get("href"))
            if not url or url in nav_urls or url == CATALOG:
                continue
            name = clean(a.get_text(" ", strip=True))
            if not meaningful_name(name):
                continue
            # Generic cross-navigation pages should not become products.
            if label_key(name):
                continue
            parsed = urlparse(url)
            if any(token in parsed.path for token in ("/search/", "/compare/", "/manufacturer/")):
                continue
            price, size, image = nearest_card_data(a, name)
            existing = products.get(url)
            item = {
                "name": name,
                "cat": cat_key,
                "price": price,
                "size": size,
                "image": image,
                "source": url,
                "path": parsed.path,
            }
            if existing:
                # Keep the most descriptive visible product title and richest metadata.
                if len(name) > len(existing.get("name", "")) and len(name) < 150:
                    existing["name"] = name
                if existing.get("price") == "Уточнить цену" and price != "Уточнить цену":
                    existing["price"] = price
                if not existing.get("size") and size:
                    existing["size"] = size
                if not existing.get("image") and image:
                    existing["image"] = image
                if existing.get("cat") == "trampoline-equipment" and cat_key == "batutnye-areny":
                    existing["cat"] = cat_key
            else:
                products[url] = item
                found_here += 1
        print(f"[{index}/{len(pages)}] {cat_key}: +{found_here} from {page_url}")
    items = list(products.values())
    order = {key: i for i, key in enumerate(KEY_ORDER)}
    items.sort(key=lambda x: (order.get(x["cat"], 99), x["name"].lower()))
    return items, pages, category_failures


def js_dump(items, meta):
    data = json.dumps(items, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    m = json.dumps(meta, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    return f"window.UNITRAMP_GENERATED_CATALOG={data};\nwindow.UNITRAMP_CATALOG_META={m};\n"


def product_page(item):
    path = item["path"].strip("/")
    depth = len([x for x in path.split("/") if x])
    root = "../" * depth
    name = html.escape(item["name"])
    price = html.escape(item.get("price") or "Уточнить цену")
    size = html.escape(item.get("size") or "Характеристики уточняются")
    source = html.escape(item["source"], quote=True)
    image = item.get("image") or ""
    image_html = f'<img src="{html.escape(image, quote=True)}" alt="{name}" loading="eager">' if image else '<div class="product-placeholder">UNITRAMP / PRODUCT</div>'
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101114"><title>{name} — UnitRamp</title><meta name="description" content="{name}. Карточка оборудования UnitRamp: основные параметры, стоимость и заявка на расчёт."><meta name="robots" content="noindex,follow"><link rel="canonical" href="{source}"><link rel="stylesheet" href="{root}styles.css"><link rel="stylesheet" href="{root}catalog-generated.css"></head><body><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{root}"><span class="brand-mark">U</span><span class="brand-word">UNITRAMP</span></a><nav class="desktop-nav"><a class="nav-link" href="{root}katalog/">Каталог</a><a class="nav-link" href="{root}projects/">Проекты</a><a class="nav-link" href="{root}services/">Услуги</a><a class="nav-link" href="{root}contacts/">Контакты</a></nav><div class="header-actions"><a class="phone" href="tel:+78007007809">8 800 700-78-09</a><a class="btn btn-acid" href="{root}contacts/#brief">Рассчитать проект</a></div></div></header><main><section class="page-hero"><div class="wrap"><div class="breadcrumbs"><a href="{root}">Главная</a><span>/</span><a href="{root}katalog/">Каталог</a><span>/</span><span>{name}</span></div><div class="eyebrow">PRODUCT / {html.escape(item['cat'])}</div><h1>{name}</h1><p>Карточка синхронизирована из действующего каталога UnitRamp. Для юридически и коммерчески значимых характеристик используйте актуальный источник.</p></div></section><section class="section"><div class="wrap generated-product-layout"><div class="generated-product-media">{image_html}</div><div class="generated-product-info"><div class="eyebrow">SPEC / SOURCE DATA</div><h2>{name}</h2><div class="generated-spec"><span>Стоимость</span><strong>{price}</strong></div><div class="generated-spec"><span>Размер / площадь</span><strong>{size}</strong></div><div class="generated-product-actions"><a class="btn" href="{root}contacts/#brief">Получить расчёт</a><a class="btn btn-light" href="{source}" target="_blank" rel="noopener">Исходная карточка ↗</a></div></div></div></section></main><footer class="site-footer"><div class="wrap"><div class="footer-bottom"><span>© 2026 ООО «ЮНИТРАМП»</span><a href="mailto:info@unitramp.ru">info@unitramp.ru</a><a href="tel:+78007007809">8 800 700-78-09</a></div></div></footer></body></html>'''


def write_product_pages(items, nav_paths):
    made = 0
    for item in items:
        path = item["path"]
        if path in nav_paths or path == "/katalog/":
            continue
        target = Path(path.lstrip("/")) / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(product_page(item), encoding="utf-8")
        made += 1
    return made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="generated-catalog.js")
    ap.add_argument("--report", default="data/catalog-report.json")
    ap.add_argument("--min-count", type=int, default=0)
    ap.add_argument("--generate-pages", action="store_true")
    args = ap.parse_args()

    session = requests.Session()
    items, pages, failures = crawl_catalog(session)
    counts = Counter(x["cat"] for x in items)
    meta = {
        "count": len(items),
        "source": CATALOG,
        "categories": dict(sorted(counts.items())),
        "categoryPages": len(pages),
        "failures": failures,
    }
    Path(args.output).write_text(js_dump(items, meta), encoding="utf-8")
    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    generated = 0
    if args.generate_pages:
        nav_paths = {urlparse(u).path for u in pages} | {"/katalog/"}
        generated = write_product_pages(items, nav_paths)
    print(json.dumps({**meta, "generatedProductPages": generated}, ensure_ascii=False, indent=2))
    if len(items) < args.min_count:
        raise SystemExit(f"Catalog crawl returned {len(items)} products; minimum required is {args.min_count}")
    if len(items) > 850:
        raise SystemExit(f"Catalog crawl returned suspiciously high count: {len(items)}")


if __name__ == "__main__":
    main()
