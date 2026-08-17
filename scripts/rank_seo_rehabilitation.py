"""Phase 3.2: rank legacy Jekyll posts for SEO rehabilitation.

Produces a deterministic priority score from repository content only.
This intentionally does not pretend to know impressions/clicks without GSC data.
"""
from pathlib import Path
from datetime import date, datetime
import csv
import re

POSTS = Path('_posts')
OUT = Path('reports')
TODAY = date.today()

CORE = {
    '로봇': 12, '자동화': 12, '스마트팩토리': 12, '비전': 11, '검사': 8,
    'plc': 10, '제어': 9, '물류': 10, 'amr': 10, 'agv': 10, '포장': 10,
    '의료': 9, '카테터': 10, '자동차': 9, '반도체': 9, '조립': 8,
    '컨베이어': 8, '팔레트': 7, '공장': 7, '산업용': 7, 'eoat': 8,
    'cycle time': 7, 'takt': 7, 'oee': 7, 'mes': 7, '서보': 7,
}
COMMERCIAL = ('도입', '비용', '견적', '선정', '비교', '설계', '구축', '개조', '개선', '방법', '기준', '체크리스트', 'roi', '투자')
OFF_DOMAIN = ('티켓링크','아정당','카드결제','핀테크','프로야구','야구','주가','코인','대출','보험','트램','모바일 결제')

def fm_get(fm, key):
    m = re.search(rf'(?m)^{re.escape(key)}:\s*(.+)$', fm)
    return m.group(1).strip().strip('"\'') if m else ''

def post_date(path):
    m = re.match(r'(\d{4}-\d{2}-\d{2})-', path.name)
    if not m: return None
    try: return datetime.strptime(m.group(1), '%Y-%m-%d').date()
    except ValueError: return None

def score_post(path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if not text.startswith('---\n') or '\n---\n' not in text:
        return None
    fm, body = text.split('\n---\n', 1)
    title = fm_get(fm[4:], 'title')
    meta = fm_get(fm, 'meta_description') or fm_get(fm, 'description')
    category = fm_get(fm, 'category') or fm_get(fm, 'categories')
    tags = fm_get(fm, 'tags')
    image = fm_get(fm, 'image') or fm_get(fm, 'og_image')
    hay = (title + ' ' + category + ' ' + tags + ' ' + body[:2500]).lower()

    relevance = min(35, sum(weight for key, weight in CORE.items() if key in hay))
    intent = min(20, sum(4 for key in COMMERCIAL if key in hay))
    quality_gap = 0
    issues = []
    if not meta: quality_gap += 8; issues.append('meta')
    if not image: quality_gap += 8; issues.append('image')
    if not category: quality_gap += 5; issues.append('category')
    if not tags: quality_gap += 5; issues.append('tags')
    if len(title) > 60: quality_gap += 4; issues.append('long-title')
    if len(body.strip()) < 1800: quality_gap += 5; issues.append('thin-content')

    d = post_date(path)
    recency = 0
    if d:
        age = max(0, (TODAY - d).days)
        recency = 10 if age <= 90 else 7 if age <= 180 else 4 if age <= 365 else 1

    off = any(x in hay for x in OFF_DOMAIN)
    domain_penalty = 45 if off else 0
    score = max(0, min(100, relevance + intent + quality_gap + recency - domain_penalty))
    if off: action = 'ARCHIVE_OR_NOINDEX'
    elif score >= 60: action = 'A_REHABILITATE_NOW'
    elif score >= 40: action = 'B_REHABILITATE_NEXT'
    else: action = 'C_MAINTAIN_OR_REVIEW'
    return {
        'score': score, 'action': action, 'file': path.name, 'title': title,
        'relevance': relevance, 'intent': intent, 'quality_gap': quality_gap,
        'recency': recency, 'issues': '|'.join(issues)
    }

def main():
    rows = [r for p in POSTS.glob('*.md') if (r := score_post(p))]
    rows.sort(key=lambda r: (-r['score'], r['file']))
    OUT.mkdir(exist_ok=True)
    fields = ['rank','score','action','file','title','relevance','intent','quality_gap','recency','issues']
    with (OUT/'seo-rehabilitation-ranking.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for i, r in enumerate(rows, 1): w.writerow({'rank': i, **r})
    top = rows[:30]
    with (OUT/'seo-rehabilitation-top30.md').open('w', encoding='utf-8') as f:
        f.write('# Phase 3.2 SEO Rehabilitation — Priority 30\n\n')
        f.write('Repository-content scoring only. Search Console impressions/clicks are not included.\n\n')
        f.write('| Rank | Score | Action | Title | Gaps |\n|---:|---:|---|---|---|\n')
        for i, r in enumerate(top, 1):
            title = r['title'].replace('|','/')
            f.write(f"| {i} | {r['score']} | {r['action']} | {title} | {r['issues'] or '-'} |\n")
    counts = {}
    for r in rows: counts[r['action']] = counts.get(r['action'], 0) + 1
    print(f'PHASE3.2 RANKING: posts={len(rows)} top30={len(top)} counts={counts}')
    for i, r in enumerate(top, 1): print(f"{i:02d}. {r['score']:3d} {r['title']} [{r['issues']}]")

if __name__ == '__main__': main()
