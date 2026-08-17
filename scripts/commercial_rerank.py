"""Phase 3.2-B: re-rank legacy posts by B2B automation commercial value.

Repository-content heuristic only. It does not claim GSC or CRM performance data.
The ranking favors direct engineering/buyer-intent language in title/meta, rejects
trend-jacking, and balances the final Priority 30 across industrial topic clusters.
"""
from pathlib import Path
from datetime import datetime, date
import csv, re
from collections import defaultdict

POSTS = Path('_posts')
OUT = Path('reports')
TODAY = date.today()

HIGH_VALUE = {
    '비전검사': 18, '딥러닝 비전': 18, 'ai 비전': 16, 'agv': 16, 'amr': 16,
    '물류자동화': 15, '팔레타이징': 15, '포장자동화': 16, '산업용 로봇': 16,
    '협동로봇': 12, 'plc': 15, 'hmi': 10, 'scada': 12, 'mes': 12,
    '스마트팩토리': 10, '예지보전': 14, 'oee': 12, '카테터': 16,
    '의료기기': 15, '자동차': 10, '반도체': 14, '열처리': 14,
    '컨베이어': 13, 'eoat': 14, '그리퍼': 14, '검사 지그': 14,
    '픽앤플레이스': 14, '3d비전': 14, '3d 비전': 14,
}
BUYER_INTENT = {
    '도입 전': 12, '체크리스트': 10, '선정': 10, '비교': 8, '비용': 10,
    '견적': 12, 'roi': 10, '설계': 10, '구축': 9, '개조': 11,
    '개선': 8, '검증': 8, 'fat': 8, 'poc': 10, 'cycle time': 8, '인터록': 8,
    '불량': 5, '정밀도': 5, '수율': 5, '생산성': 5,
}
TREND_JACK = (
    '선거', '백악관', '국회', '주가', '관련주', '수혜주', 'etf', 'ipo', 'fomc', '금리',
    '코인', '야구', '오타니', 'kbo', 'fc 온라인', '게임', '폭염', '태풍', '엔저',
    '관세', '무역 전쟁', '취업박람회', '채용', '모병제', '일자리', '대선', '정치',
    '티켓링크', '아정당', '모바일 결제', '국민체력100', '와우넷', '한국경제신문',
)
WEAK_CONTEXT = (
    '정책 분석', '시장 전망', '트렌드 전망', '글로벌 공급망', '정부 주도', '지원 법안',
    '보조금 활용', '지역 제조업의 미래',
)
VERTICALS = ('반도체','자동차','의료','카테터','물류','포장','조립','검사','로봇','공장')


def fm_get(fm, key):
    m = re.search(rf'(?m)^{re.escape(key)}:\s*(.+)$', fm)
    return m.group(1).strip().strip('"\'') if m else ''


def post_date(name):
    m = re.match(r'(\d{4}-\d{2}-\d{2})-', name)
    if not m: return None
    try: return datetime.strptime(m.group(1), '%Y-%m-%d').date()
    except ValueError: return None


def weighted_hits(text, table, cap):
    return min(cap, sum(v for k, v in table.items() if k in text))


def topic_cluster(text):
    t = text.lower()
    # Vertical-specific clusters first so generic words do not swallow them.
    if any(k in t for k in ('카테터','의료기기','제약','콜드체인')): return 'medical'
    if any(k in t for k in ('반도체','hbm','웨이퍼','aoi','mlcc')): return 'semiconductor'
    if any(k in t for k in ('자동차','현대차','기아','배터리','2차전지','ev')): return 'automotive-battery'
    if any(k in t for k in ('포장자동화','파우치','실링','카토닝')): return 'packaging'
    if any(k in t for k in ('agv','amr','wms','물류자동화','자동창고','컨베이어','소터')): return 'logistics'
    if any(k in t for k in ('비전검사','딥러닝 비전','ai 비전','3d비전','3d 비전','불량검출')): return 'vision'
    if any(k in t for k in ('plc','hmi','scada','mes','opc','ethercat','profinet')): return 'control-software'
    if any(k in t for k in ('산업용 로봇','협동로봇','eoat','그리퍼','픽앤플레이스','팔레타이징')): return 'robotics'
    if any(k in t for k in ('예지보전','oee','스마트팩토리','디지털트윈')): return 'smart-factory'
    return 'other-industrial'


def evaluate(path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if not text.startswith('---\n') or '\n---\n' not in text: return None
    fm, body = text.split('\n---\n', 1)
    title = fm_get(fm[4:], 'title')
    meta = fm_get(fm, 'meta_description') or fm_get(fm, 'description')
    image = fm_get(fm, 'image') or fm_get(fm, 'og_image')
    tags = fm_get(fm, 'tags')
    category = fm_get(fm, 'category') or fm_get(fm, 'categories')

    primary = (title + ' ' + meta + ' ' + tags + ' ' + category).lower()
    body_l = body[:3500].lower()
    full = primary + ' ' + body_l

    tech_primary = weighted_hits(primary, HIGH_VALUE, 40)
    tech_body = min(8, weighted_hits(body_l, HIGH_VALUE, 40) // 5)
    tech = min(40, tech_primary + tech_body)
    intent = weighted_hits((title + ' ' + meta).lower(), BUYER_INTENT, 30)
    vertical = min(10, sum(2 for k in VERTICALS if k in primary))

    gaps = 0; issues=[]
    if not image: gaps += 5; issues.append('image')
    if not meta: gaps += 5; issues.append('meta')
    if len(body.strip()) < 1800: gaps += 5; issues.append('thin-content')
    if len(title) > 60: gaps += 2; issues.append('long-title')
    if re.search(r'\b\d{2,3}%\b', title + ' ' + body[:800]): issues.append('numeric-claim-review')

    d = post_date(path.name)
    recency = 0
    if d:
        age = max(0, (TODAY-d).days)
        recency = 6 if age <= 120 else 4 if age <= 240 else 2

    contamination = [k for k in TREND_JACK if k in full]
    weak = [k for k in WEAK_CONTEXT if k in title.lower()]
    direct_engineering = tech_primary >= 12
    score = max(0, min(100, tech + intent + vertical + gaps + recency - (60 if contamination else 0) - (18 if weak else 0)))

    if contamination:
        decision='EXCLUDE_TREND_JACKING'
    elif not direct_engineering:
        decision='LOW_COMMERCIAL_RELEVANCE'
    elif weak and intent < 12:
        decision='LOW_COMMERCIAL_RELEVANCE'
    elif score >= 58:
        decision='P1_REHABILITATE'
    elif score >= 42:
        decision='P2_REHABILITATE'
    else:
        decision='P3_REVIEW'

    return {
        'score': score, 'decision': decision, 'file': path.name, 'title': title,
        'tech': tech, 'tech_primary': tech_primary, 'intent': intent, 'vertical': vertical,
        'gaps': gaps, 'recency': recency, 'issues': '|'.join(issues),
        'excluded_terms': '|'.join(contamination), 'weak_terms': '|'.join(weak),
        'cluster': topic_cluster(primary),
    }


def select_balanced_priority(eligible, limit=30, per_cluster=4):
    ordered = sorted(eligible, key=lambda r:(-r['score'],-r['intent'],-r['tech_primary'],r['file']))
    selected=[]; counts=defaultdict(int)
    for row in ordered:
        if counts[row['cluster']] >= per_cluster:
            continue
        selected.append(row); counts[row['cluster']] += 1
        if len(selected) >= limit:
            return selected
    # If the corpus does not have enough distinct clusters, fill remaining slots by score.
    chosen={r['file'] for r in selected}
    for row in ordered:
        if row['file'] in chosen: continue
        selected.append(row)
        if len(selected) >= limit: break
    return selected


def main():
    rows=[r for p in POSTS.glob('*.md') if (r:=evaluate(p))]
    eligible=[r for r in rows if r['decision'] in ('P1_REHABILITATE','P2_REHABILITATE','P3_REVIEW')]
    priority=select_balanced_priority(eligible, limit=30, per_cluster=4)
    OUT.mkdir(exist_ok=True)
    fields=['rank','score','decision','cluster','file','title','tech','tech_primary','intent','vertical','gaps','recency','issues','excluded_terms','weak_terms']
    with (OUT/'commercial-priority30.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for i,r in enumerate(priority,1): w.writerow({'rank':i,**r})
    with (OUT/'commercial-priority30.md').open('w',encoding='utf-8') as f:
        f.write('# Phase 3.2-B — B2B Commercial Priority 30\n\n')
        f.write('Repository-content scoring only. No Google Search Console or CRM metrics are assumed.\n\n')
        f.write('| Rank | Score | Cluster | Title | Intent | Direct Tech | Gaps |\n|---:|---:|---|---|---:|---:|---|\n')
        for i,r in enumerate(priority,1):
            f.write(f"| {i} | {r['score']} | {r['cluster']} | {r['title'].replace('|','/')} | {r['intent']} | {r['tech_primary']} | {r['issues'] or '-'} |\n")
    excluded=[r for r in rows if r['decision']=='EXCLUDE_TREND_JACKING']
    low=[r for r in rows if r['decision']=='LOW_COMMERCIAL_RELEVANCE']
    distribution=defaultdict(int)
    for r in priority: distribution[r['cluster']] += 1
    print(f'PHASE3.2-B COMMERCIAL RERANK: total={len(rows)} eligible={len(eligible)} priority30={len(priority)} trend_excluded={len(excluded)} low_relevance={len(low)} clusters={dict(distribution)}')
    for i,r in enumerate(priority,1):
        print(f"{i:02d}. {r['score']:3d} [{r['cluster']}] {r['title']} [intent={r['intent']} direct_tech={r['tech_primary']} gaps={r['issues']}]")

if __name__=='__main__': main()
