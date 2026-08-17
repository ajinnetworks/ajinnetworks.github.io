"""Regression checks for Phase 3.2-B commercial reranking."""
from commercial_rerank import evaluate, select_balanced_priority
from pathlib import Path
import tempfile


def write_post(title, body='산업용 로봇 자동화 설비 도입 전 설계 기준과 ROI 검토', meta='자동화 설비 도입 전 기술 검토 가이드', image='/assets/img/hero/factory.jpg'):
    tmp = tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8')
    tmp.write(f'''---\ntitle: "{title}"\nmeta_description: "{meta}"\ncategory: 공장자동화\ntags: [산업용로봇, 자동화]\nimage: {image}\n---\n{body * 80}\n''')
    tmp.close()
    return Path(tmp.name)

p = write_post('산업용 로봇 EOAT 도입 전 선정 기준')
r = evaluate(p)
assert r['decision'] in ('P1_REHABILITATE','P2_REHABILITATE'), r
assert r['intent'] > 0 and r['tech_primary'] >= 12, r

for bad_title in (
    '선거 공약으로 보는 스마트팩토리 자동화 전망',
    '프로야구 기술로 보는 AI 비전검사 혁신',
    'FOMC 금리 결정과 스마트팩토리 투자 전략',
    '스마트팩토리 관련주와 핵심 수혜주 전망',
):
    rb = evaluate(write_post(bad_title))
    assert rb['decision'] == 'EXCLUDE_TREND_JACKING', (bad_title, rb)

weak = evaluate(write_post('정부 주도 스마트팩토리 정책 분석', meta='시장 전망과 정책 분석', body='스마트팩토리 산업 동향과 정책 분석'))
assert weak['decision'] in ('LOW_COMMERCIAL_RELEVANCE','P3_REVIEW'), weak

# High scoring posts from one topic family must not monopolize the first-pass priority set.
rows=[]
for i in range(8):
    rows.append({'score':100-i,'intent':30,'tech_primary':40,'file':f'l{i}.md','cluster':'logistics'})
for i in range(5):
    rows.append({'score':90-i,'intent':25,'tech_primary':35,'file':f'v{i}.md','cluster':'vision'})
for i in range(5):
    rows.append({'score':88-i,'intent':24,'tech_primary':34,'file':f'r{i}.md','cluster':'robotics'})
selected=select_balanced_priority(rows, limit=12, per_cluster=4)
from collections import Counter
counts=Counter(x['cluster'] for x in selected)
assert counts['logistics'] <= 4 and counts['vision'] <= 4 and counts['robotics'] <= 4, counts
assert len(counts) >= 3, counts

print('PHASE3.2-B COMMERCIAL RERANK TESTS: PASS')
