"""Phase 3.2-B: re-rank legacy posts by B2B automation commercial value.

This layer intentionally prioritizes topics that can plausibly lead to engineering review,
PoC, budget, retrofit, or quotation discussions. It excludes trend-jacking topics even when
they contain automation keywords. Repository content only; no fabricated GSC metrics.
"""
from pathlib import Path
from datetime import datetime, date
import csv, re

POSTS = Path('_posts')
OUT = Path('reports')
TODAY = date.today()

HIGH_VALUE = {
    '비전검사': 18, '딥러닝 비전': 18, 'ai 비전': 16, 'agv': 16, 'amr': 16,
    '물류자동화': 15, '팔레타이징': 15, '포장자동화': 16, '산업용 로봇': 16,
    '협동로봇': 12, 'plc': 15, 'hmi': 10, 'scada': 12, 'mes': 12,
    '스마트팩토리': 12, '예지보전': 14, 'oee': 12, '카테터': 16,
    '의료기기': 15, '자동차': 13, '반도체': 14, '열처리': 14,
    '컨베이어': 13, 'eoat': 14, '그리퍼': 14, '검사 지그': 14,
}
BUYER_INTENT = {
    '도입 전': 12, '체크리스트': 10, '선정': 10, '비교': 8, '비용': 10,
    '견적': 12, 'roi': 10, '투자': 8, '설계': 10, '구축': 9, '개조': 11,
    '개선': 8, '검증': 8, 'fat': 8, 'poc': 10, 'cycle time': 8, '인터록': 8,
}
TREND_JACK = (
    '선거', '백악관', '국회', '주가', 'etf', 'ipo', '코인', '야구', '오타니', 'kbo',
    'fc 온라인', '게임', '폭염', '태풍', '엔저', '관세', '무역 전쟁', '취업박람회',
    '채용', '모병제', '일자리', '대선', '정치', '티켓링크', '아정당', '모바일 결제',
)
VERTICALS = (
    '반도체', '자동차', '의료', '카테터', '물류', '포장', '조립', '검사', '로봇', '공장'
)


def fm_get(fm, key):
    m = re.search(rf'(?m)^{re.escape(key)}:\s*(.+)$', fm)
    return m.group(1).strip().strip('"\'') if m else ''


def post_date(name):
    m = re.match(r'(\d{4}-\d{2}-\d{2})-', name)
    if not m: return None
    try: return datetime.strptime(m.group(1), '%Y-%m-%d').date()
    except ValueError: return None


def evaluate(path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if not text.startswith('---\n') or '\n---\n' not in text: return None
    fm, body = text.split('\n---\n', 1)
    title = fm_get(fm[4:], 'title')
    meta = fm_get(fm, 'meta_description') or fm_get(fm, 'description')
    image = fm_get(fm, 'image') or fm_get(fm, 'og_image')
    tags = fm_get(fm, 'tags')
    category = fm_get(fm, 'category') or fm_get(fm, 'categories')
    hay = (title + ' ' + meta + ' ' + tags + ' ' + category + ' ' + body[:3500]).lower()

    tech = min(40, sum(v for k, v in HIGH_VALUE.items() if k in hay))
    intent = min(30, sum(v for k, v in BUYER_INTENT.items() if k in hay))
    vertical = min(12, sum(3 for k in VERTICALS if k in hay))
    gaps = 0; issues=[]
    if not image: gaps += 5; issues.append('image')
    if not meta: gaps += 5; issues.append('meta')
    if len(body.strip()) < 1800: gaps += 5; issues.append('thin-content')
    if len(title) > 60: gaps += 2; issues.append('long-title')

    d = post_date(path.name)
    recency = 0
    if d:
        age = max(0, (TODAY-d).days)
        recency = 8 if age <= 120 else 5 if age <= 240 else 2

    contamination = [k for k in TREND_JACK if k in hay]
    penalty = 60 if contamination else 0
    score = max(0, min(100, tech + intent + vertical + gaps + recency - penalty))

    if contamination:
        decision='EXCLUDE_TREND_JACKING'
    elif tech < 18:
        decision='LOW_COMMERCIAL_RELEVANCE'
    elif score >= 60:
        decision='P1_REHABILITATE'
    elif score >= 45:
        decision='P2_REHABILITATE'
    else:
        decision='P3_REVIEW'
    return {
        'score': score, 'decision': decision, 'file': path.name, 'title': title,
        'tech': tech, 'intent': intent, 'vertical': vertical, 'gaps': gaps,
        'recency': recency, 'issues': '|'.join(issues),
        'excluded_terms': '|'.join(contamination),
    }


def main():
    rows=[r for p in POSTS.glob('*.md') if (r:=evaluate(p))]
    eligible=[r for r in rows if r['decision'] not in ('EXCLUDE_TREND_JACKING','LOW_COMMERCIAL_RELEVANCE')]
    eligible.sort(key=lambda r:(-r['score'],-r['intent'],-r['tech'],r['file']))
    priority=eligible[:30]
    OUT.mkdir(exist_ok=True)
    fields=['rank','score','decision','file','title','tech','intent','vertical','gaps','recency','issues','excluded_terms']
    with (OUT/'commercial-priority30.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for i,r in enumerate(priority,1): w.writerow({'rank':i,**r})
    with (OUT/'commercial-priority30.md').open('w',encoding='utf-8') as f:
        f.write('# Phase 3.2-B — B2B Commercial Priority 30\n\n')
        f.write('Repository-content scoring only. No Google Search Console metrics are assumed.\n\n')
        f.write('| Rank | Score | Title | Intent | Tech | Gaps |\n|---:|---:|---|---:|---:|---|\n')
        for i,r in enumerate(priority,1):
            f.write(f"| {i} | {r['score']} | {r['title'].replace('|','/')} | {r['intent']} | {r['tech']} | {r['issues'] or '-'} |\n")
    excluded=[r for r in rows if r['decision']=='EXCLUDE_TREND_JACKING']
    print(f'PHASE3.2-B COMMERCIAL RERANK: total={len(rows)} eligible={len(eligible)} priority30={len(priority)} trend_excluded={len(excluded)}')
    for i,r in enumerate(priority,1): print(f"{i:02d}. {r['score']:3d} {r['title']} [intent={r['intent']} tech={r['tech']} gaps={r['issues']}] ")

if __name__=='__main__': main()
