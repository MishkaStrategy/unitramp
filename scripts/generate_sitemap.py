#!/usr/bin/env python3
from pathlib import Path
from xml.sax.saxutils import escape

BASE = "https://unitramp.ru"
CORE = [
    ("/", "weekly", "1.0"),
    ("/katalog/", "daily", "0.9"),
    ("/projects/", "monthly", "0.9"),
    ("/info/", "weekly", "0.7"),
    ("/contacts/", "monthly", "0.7"),
    ("/services/", "monthly", "0.7"),
    ("/franchises/", "monthly", "0.7"),
    ("/reviews/", "monthly", "0.7"),
    ("/batutnyj-centr-pod-klyuch/", "monthly", "0.9"),
    ("/nindzya-park-pod-klyuch/", "monthly", "0.9"),
    ("/aktiviti-park-pod-klyuch/", "monthly", "0.9"),
    ("/ulichnye-batutnye-areny/", "monthly", "0.8"),
    ("/touch-arena-pod-klyuch/", "monthly", "0.8"),
    ("/skalodromy-pod-klyuch/", "monthly", "0.8"),
]


def normalize(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and not path.endswith("/"):
        path += "/"
    return path


def main():
    urls = {normalize(path): (freq, priority) for path, freq, priority in CORE}
    catalog = Path("katalog")
    if catalog.exists():
        for index in catalog.rglob("index.html"):
            rel = index.parent.as_posix()
            path = normalize(rel)
            # Generated product pages are intentionally noindex on the GitHub preview,
            # but their canonical source URLs belong in the migration sitemap.
            urls.setdefault(path, ("monthly", "0.6"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in sorted(urls, key=lambda p: (p != "/", p)):
        freq, priority = urls[path]
        loc = escape(BASE + path)
        lines.append(f"  <url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{priority}</priority></url>")
    lines.append("</urlset>")
    Path("sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated sitemap.xml with {len(urls)} canonical URLs")


if __name__ == "__main__":
    main()
