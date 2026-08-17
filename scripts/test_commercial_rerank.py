"""Regression checks for Phase 3.2-B commercial reranking."""
from scripts.commercial_rerank import evaluate
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
assert r['intent'] > 0 and r['tech'] >= 18, r

p2 = write_post('선거 공약으로 보는 스마트팩토리 자동화 전망')
r2 = evaluate(p2)
assert r2['decision'] == 'EXCLUDE_TREND_JACKING', r2

p3 = write_post('프로야구 기술로 보는 AI 비전검사 혁신')
r3 = evaluate(p3)
assert r3['decision'] == 'EXCLUDE_TREND_JACKING', r3

print('PHASE3.2-B COMMERCIAL RERANK TESTS: PASS')
