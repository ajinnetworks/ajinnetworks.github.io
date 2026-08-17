"""Fail CI when generated homepage/post internal links point to missing _site files."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

SITE = Path("_site")

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def target_exists(href: str) -> bool:
    if href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return True
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        # External absolute URLs are outside this build-integrity check.
        return True
    path = unquote(parsed.path or "/")
    if not path.startswith("/"):
        return True
    rel = path.lstrip("/")
    candidates = []
    if not rel:
        candidates.append(SITE / "index.html")
    elif Path(rel).suffix:
        candidates.append(SITE / rel)
    else:
        candidates.extend([SITE / rel / "index.html", SITE / f"{rel}.html"])
    return any(p.exists() for p in candidates)


broken = []
for html in SITE.rglob("*.html"):
    parser = LinkParser()
    parser.feed(html.read_text(encoding="utf-8", errors="ignore"))
    for href in parser.links:
        if not target_exists(href):
            broken.append((str(html.relative_to(SITE)), href))

if broken:
    print("SITE LINK INTEGRITY: FAIL")
    for src, href in broken[:100]:
        print(f"BROKEN: {src} -> {href}")
    raise SystemExit(1)

print("SITE LINK INTEGRITY: PASS")
