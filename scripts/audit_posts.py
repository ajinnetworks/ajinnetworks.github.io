"""Report SEO/content debt across Jekyll posts without blocking legacy content."""
from pathlib import Path
import re

POSTS = Path('_posts')
required = ('title',)
critical = []
warnings = []
rows = []

for path in sorted(POSTS.glob('*.md')):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if not text.startswith('---\n') or text.count('\n---\n') < 1:
        critical.append((path.name, 'missing front matter'))
        continue
    fm = text.split('\n---\n', 1)[0][4:]
    def get(key):
        m = re.search(rf'(?m)^{re.escape(key)}:\s*(.+)$', fm)
        return m.group(1).strip() if m else ''
    title = get('title').strip('"\'')
    meta = get('meta_description') or get('description')
    category = get('category') or get('categories')
    tags = get('tags')
    image = get('image') or get('og_image')
    if not title:
        critical.append((path.name, 'missing title'))
    if not meta:
        warnings.append((path.name, 'missing meta description'))
    if not category:
        warnings.append((path.name, 'missing category'))
    if not tags:
        warnings.append((path.name, 'missing tags'))
    if not image:
        warnings.append((path.name, 'missing image'))
    if len(title) > 60:
        warnings.append((path.name, f'long title {len(title)} chars'))
    if any(x in title.lower() for x in ('티켓링크','아정당','카드결제','핀테크','프로야구')):
        warnings.append((path.name, 'off-domain title candidate'))
    rows.append(path.name)

print(f'POST QUALITY AUDIT: posts={len(rows)} critical={len(critical)} warnings={len(warnings)}')
for name, issue in critical[:50]: print(f'CRITICAL: {name} -> {issue}')
for name, issue in warnings[:80]: print(f'WARNING: {name} -> {issue}')
if critical:
    raise SystemExit(1)
