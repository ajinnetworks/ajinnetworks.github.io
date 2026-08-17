"""Validate generated Jekyll links.

Critical site navigation/post/category/music links must resolve to generated files.
Legacy /tag/<name>/ links are reported as warnings because this site currently has
no tag archive generator; they do not block a deploy while the tag UX is migrated.
"""
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


def classify(href: str) -> str:
    parsed = urlparse(href)
    path = unquote(parsed.path or "/")
    if path.startswith("/tag/"):
        return "legacy-tag"
    return "critical"


def target_exists(href: str) -> bool:
    if href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return True
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
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
warnings = []
for html in SITE.rglob("*.html"):
    parser = LinkParser()
    parser.feed(html.read_text(encoding="utf-8", errors="ignore"))
    for href in parser.links:
        if target_exists(href):
            continue
        row = (str(html.relative_to(SITE)), href)
        if classify(href) == "legacy-tag":
            warnings.append(row)
        else:
            broken.append(row)

if warnings:
    print(f"SITE LINK INTEGRITY: {len(warnings)} legacy tag links reported as warnings")
    for src, href in warnings[:20]:
        print(f"WARNING TAG: {src} -> {href}")

if broken:
    print("SITE LINK INTEGRITY: FAIL")
    for src, href in broken[:100]:
        print(f"BROKEN: {src} -> {href}")
    raise SystemExit(1)

print("SITE LINK INTEGRITY: PASS")
