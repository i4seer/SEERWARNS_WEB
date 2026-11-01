"""Apply the common Warns header to local pages; never deploy or validate."""
from pathlib import Path
import hashlib
import html
import re

ROOT = Path(__file__).resolve().parents[1]
HEADER = re.compile(r'<header\b[^>]*class=[\"\'][^\"\']*\bsite-header\b[^\"\']*[\"\'][^>]*>.*?</header>', re.S)
NAV_ITEMS = (
    ('/', 'Home'),
    ('/books/', 'Books'),
    ('/people-and-places/', 'People & Places'),
    ('/the-seer/', 'The Seer'),
    ('/news/', 'News'),
    ('/about/', 'About'),
)


def navigation_for(path, root):
    route = '/' + path.relative_to(root).as_posix().removesuffix('index.html')
    if route.startswith(('/people/', '/establishments/', '/harmon/', '/map/')):
        current = '/people-and-places/'
    elif route.startswith('/the-warning/'):
        current = '/the-seer/'
    else:
        current = next((href for href, _ in NAV_ITEMS
                        if route == href or (href != '/' and route.startswith(href))), None)
    return ['<a' + (' aria-current="page" class="active"' if href == current else '') +
            f' href="{href}">{html.escape(label)}</a>' for href, label in NAV_ITEMS]


def update_header(root=ROOT):
    root = Path(root)
    versions = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()[:12]
                for name in ('style.css', 'site.js')}
    count = 0
    for path in root.rglob('*.html'):
        if any(part.startswith('.') for part in path.relative_to(root).parts):
            continue
        original = path.read_text(encoding='utf-8')
        header = HEADER.search(original)
        if not header:
            continue
        links = navigation_for(path, root)
        replacement = ('<header class="site-header">\n'
                       '<a aria-label="Seer Warns home" class="brand" href="/"><span>Seer</span><strong>Warns</strong></a>\n'
                       '<button aria-controls="main-nav" aria-expanded="false" aria-label="Open navigation" class="menu-btn" type="button">Menu</button>\n'
                       '<nav aria-label="Main navigation" class="main-nav" id="main-nav">\n' +
                       '\n'.join(links) + '\n</nav>\n</header>')
        updated = original[:header.start()] + replacement + original[header.end():]
        for name, version in versions.items():
            updated = re.sub('/' + re.escape(name) + r'(?:\?[^\"\'\s<>]*)?(?=[\"\'])',
                             f'/{name}?v={version}', updated)
        if updated != original:
            path.write_text(updated, encoding='utf-8', newline='\n')
        count += 1
    print(f'{root.name}: applied the common header and asset versions to {count} local pages.')


if __name__ == '__main__':
    update_header()
