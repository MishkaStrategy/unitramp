#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path('.').resolve()


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == 'a' and data.get('href'):
            self.refs.append(('href', data['href']))
        elif tag == 'script' and data.get('src'):
            self.refs.append(('src', data['src']))
        elif tag == 'link' and data.get('href'):
            self.refs.append(('href', data['href']))


def resolve(source: Path, ref: str):
    ref = ref.strip()
    if not ref or ref.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return None
    parsed = urlsplit(ref)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if not path:
        return source
    if path.startswith('/'):
        candidate = ROOT / path.lstrip('/')
    else:
        candidate = source.parent / path
    candidate = candidate.resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        return ('outside', candidate)
    if candidate.is_dir() or path.endswith('/'):
        candidate = candidate / 'index.html'
    return candidate


def main():
    broken = []
    html_files = list(ROOT.rglob('*.html'))
    for source in html_files:
        parser = Links()
        parser.feed(source.read_text(encoding='utf-8', errors='replace'))
        for kind, ref in parser.refs:
            target = resolve(source, ref)
            if target is None:
                continue
            if isinstance(target, tuple):
                broken.append((source, ref, 'escapes repository root'))
                continue
            if not target.exists():
                broken.append((source, ref, str(target.relative_to(ROOT))))
    if broken:
        for source, ref, target in broken[:80]:
            print(f'BROKEN {source.relative_to(ROOT)} -> {ref!r} ({target})')
        raise SystemExit(f'{len(broken)} broken internal HTML references')
    print(f'Internal-link audit passed across {len(html_files)} HTML files')


if __name__ == '__main__':
    main()
