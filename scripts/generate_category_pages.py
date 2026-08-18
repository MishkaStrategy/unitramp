#!/usr/bin/env python3
from html import escape
from pathlib import Path

BASE = "https://unitramp.ru"
ROUTES = {
    "/katalog/akrobaticheskie-naduvnye-dorozhki-i-kovry/": ("airtrack", "Акробатические надувные дорожки и ковры"),
    "/katalog/batutnoe-oborudovanie/": ("trampoline-equipment", "Батутное оборудование"),
    "/katalog/batutnoe-oborudovanie/batutnye-areny/": ("batutnye-areny", "Батутные арены"),
    "/katalog/batutnoe-oborudovanie/obkladochnyie-matyi-dlya-batuta/": ("trampoline-equipment", "Обкладочные маты для батута"),
    "/katalog/batutnoe-oborudovanie/prochee/": ("trampoline-equipment", "Прочее оборудование для батутного центра"),
    "/katalog/batutnoe-oborudovanie/pruzhinyi-dlya-batuta/": ("trampoline-equipment", "Пружины для батута"),
    "/katalog/batutnoe-oborudovanie/setki-dlya-batuta-sport/": ("trampoline-equipment", "Сетки для спортивных батутов"),
    "/katalog/batutnoe-oborudovanie/setki-dlya-batuta/": ("trampoline-equipment", "Сетки для батута коммерческие"),
    "/katalog/batutnoe-oborudovanie/slamball/": ("trampoline-equipment", "Баскетбольная зона Slam Ball"),
    "/katalog/batutnoe-oborudovanie/sportivnye-batuty/": ("trampoline-equipment", "Профессиональные спортивные батуты"),
    "/katalog/batutnoe-oborudovanie/zagraditelnye-i-strahovochnye-setki-dlya-batuta/": ("trampoline-equipment", "Заградительные и страховочные сетки"),
    "/katalog/batutnoe-oborudovanie/zony-prizemleniya-i-naduvnye-podushki/": ("trampoline-equipment", "Зоны приземления и надувные подушки"),
    "/katalog/batutnye-kompleksy/": ("batutnye-areny", "Батутные комплексы"),
    "/katalog/detskie-igrovye-komnaty/": ("rooms", "Детские игровые комнаты"),
    "/katalog/detskie-igrovye-labirinty/": ("labirinty", "Детские игровые лабиринты"),
    "/katalog/detskie-igrovye-labirinty/ulichnye-igrovye-labirinty/": ("labirinty", "Уличные игровые лабиринты"),
    "/katalog/detskie-igrovye-labirinty/verevochnye-labirinty/": ("labirinty", "Веревочные лабиринты"),
    "/katalog/detskie-igrovye-labirinty/vertikalnye-labirinty/": ("labirinty", "Вертикальные лабиринты"),
    "/katalog/detskie-karuseli/": ("carousel", "Детские карусели"),
    "/katalog/gorki-kosogory/": ("slope", "Горки-косогоры"),
    "/katalog/gorki-vulkany/": ("volcano", "Горки-вулканы"),
    "/katalog/igrovye-kompleksy/": ("igrovye-kompleksy", "Игровые комплексы для помещений"),
    "/katalog/interaktivnoe-oborudovanie/": ("interactive", "Интерактивное оборудование"),
    "/katalog/myagkie-moduli/": ("soft", "Мягкие модули"),
    "/katalog/oborudovanie-dlya-nindzja-parka/": ("nindzya", "Оборудование для ниндзя-парка"),
    "/katalog/oborudovaniye-dlya-skalodroma/": ("climbing", "Оборудование для скалодрома"),
    "/katalog/pokrytiya-dlya-zalov/": ("mats", "Маты и покрытия для залов"),
    "/katalog/suhie-akvaparki/": ("dry", "Сухие аквапарки"),
    "/katalog/tyubingovye-gorki/": ("tubing", "Тюбинговые горки"),
}


def page(path: str, key: str, title: str) -> str:
    depth = len([part for part in path.strip("/").split("/") if part])
    root = "../" * depth
    source = BASE + path
    t = escape(title)
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101114"><title>{t} — каталог UnitRamp</title><meta name="description" content="{t} от UnitRamp. Каталог оборудования, поиск, параметры и переходы к карточкам товаров."><meta name="robots" content="index,follow"><link rel="canonical" href="{source}"><link rel="stylesheet" href="{root}styles.css"><link rel="stylesheet" href="{root}catalog-generated.css"><script defer src="{root}app.js"></script><script defer src="{root}nav-patch.js"></script><script defer src="{root}generated-catalog.js"></script><script defer src="{root}catalog-runtime.js"></script></head><body data-page="catalog" data-category="{escape(key)}"><a class="skip-link" href="#main">К содержанию</a><div id="site-header"></div><main id="main" tabindex="-1"></main><div id="site-footer"></div></body></html>'''


def main():
    made = 0
    for path, (key, title) in ROUTES.items():
        target = Path(path.lstrip("/")) / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(path, key, title), encoding="utf-8")
        made += 1
    print(f"Generated {made} preserved category/subcategory pages")


if __name__ == "__main__":
    main()
