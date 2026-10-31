"""Apply the common Warns header to local pages; never deploy or validate."""
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
HEADER = re.compile(r'<header\b[^>]*class=[\"\'][^\"\']*\bsite-header\b[^\"\']*[\"\'][^>]*>.*?</header>', re.S)
NAV = re.compile(r'<(?:ul|nav)\b[^>]*class=[\"\'][^\"\']*\b(?:site-nav|main-nav)\b[^\"\']*[\"\'][^>]*>(.*?)</(?:ul|nav)>', re.S)


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
        nav = NAV.search(header[0])
        if not nav:
            raise ValueError(f'Missing navigation in {path}')
        links = re.findall(r'<a\b[^>]*>.*?</a>', nav[1], re.S)
        for index, link in enumerate(links):
            if re.search(r'class=[\"\'][^\"\']*\bactive\b', link) and 'aria-current=' not in link:
                links[index] = link.replace('<a ', '<a aria-current="page" ', 1)
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
