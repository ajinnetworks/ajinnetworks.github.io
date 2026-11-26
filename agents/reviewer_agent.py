"""
reviewer_agent.py — 품질 검수 & 재작성 에이전트
Goal: 작성된 포스트의 품질 점수를 산출하고, 불합격 시 원문을 바탕으로 1회 재작성
Evaluator AI 역할: 기술 정확성·근거 없는 수치·오탈자·구조 점검

2026-11-26 개정 (run #117 발행 글 검토 결과 반영):
- 검수가 본문 앞 400자만 보던 문제 → 본문 전체(최대 REVIEW_CHAR_LIMIT자) 검수
- 기술 개념 오류(예: 택트타임과 사이클타임 혼동)를 불합격 사유로 명시
- 검수 호출은 lite보다 상위 모델 우선 (gemini_client prefer="quality")
- 재작성 프롬프트에 원문이 빠져 있던 문제, 재작성 결과가 목록에 반영되지 않던 문제 수정
"""

import io
import json
import logging
import sys
from pathlib import Path

import yaml

from agents.gemini_client import get_gemini_response

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

logger = logging.getLogger(__name__)

REVIEW_CHAR_LIMIT = 8000  # 포스트 1편당 검수에 보내는 본문 최대 글자 수
QUALITY = "quality"

REVIEW_CRITERIA = """평가 기준 (100점 만점) — 산업 자동화 B2B 기술 블로그, 독자는 현장 설비 엔지니어:
1. 기술 정확성 (40): 용어·개념·공식이 업계 표준과 맞는가.
   - 개념 오류가 하나라도 있으면 이 항목 0점이고 불합격 (예: 택트타임은 고객 수요로 정해지는 값이라
     '단축'의 대상이 아니며, 공정 소요 시간은 사이클타임이다 / 슈(shoe)와 슈트(chute) 혼동 등)
2. 근거와 수치 (20): 출처 없는 비율·통계·효과 수치가 있으면 감점. "(추측입니다)"를 붙였어도 지어낸 통계는 감점.
3. 실무 유용성 (20): 설비 도입·사양 검토에 바로 쓸 수 있는 기준, 비교, 체크포인트가 있는가.
4. 문장 품질 (20): 오탈자, 띄어쓰기, 깨진 문장, 과장 표현("대참사", "완벽" 등), 제목과 본문 범위의 불일치."""


def load_config() -> dict:
    config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _content_text(post: dict) -> str:
    content = post.get("content", "")
    if isinstance(content, list):
        return " ".join(str(c) for c in content)
    return str(content)


def _extract_json(raw: str, opener: str) -> str:
    """```json 펜스나 앞뒤 설명을 걷어내고 opener('[' 또는 '{')로 시작하는 JSON만 남긴다."""
    if "```" in raw:
        for part in raw.split("```"):
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith(opener):
                return part
    raw = raw.strip()
    start = raw.find(opener)
    return raw[start:] if start > 0 else raw


def _review_from_result(r: dict, min_score: int) -> dict:
    try:
        score = int(r.get("score", 0))
    except (TypeError, ValueError):
        score = 0
    issues = [
        {"severity": str(i.get("severity", "medium")), "description": str(i.get("description", ""))}
        for i in r.get("issues", []) if isinstance(i, dict) and i.get("description")
    ]
    passed = score >= min_score and not any(i["severity"] == "critical" for i in issues)
    if not passed and not issues and r.get("reason"):
        issues = [{"severity": "medium", "description": str(r["reason"])}]
    return {
        "total_score": score,
        "breakdown": r.get("breakdown", {}) if isinstance(r.get("breakdown"), dict) else {},
        "issues": issues,
        "pass": passed,
        "min_score": min_score,
        "revision_notes": str(r.get("reason", "")),
    }


def _failed_review(min_score: int, why: str) -> dict:
    return {
        "total_score": 0, "breakdown": {}, "pass": False, "min_score": min_score,
        "issues": [{"severity": "high", "description": why}],
        "revision_notes": "검수 에이전트 오류 - 수동 확인 필요",
    }


def _post_block(index: int, post: dict) -> str:
    return (
        f"[포스트 {index}] 제목: {post.get('title', '')}\n"
        f"카테고리: {post.get('category', '')}\n"
        f"본문:\n{_content_text(post)[:REVIEW_CHAR_LIMIT]}"
    )


RESULT_SHAPE = """{{"index": {index}, "score": 점수, "breakdown": {{"accuracy": 0, "evidence": 0, "usefulness": 0, "writing": 0}},
  "issues": [{{"severity": "critical|high|medium|low", "description": "구체적 문제와 위치"}}],
  "reason": "한 줄 요약"}}"""


def batch_review_posts(posts: list[dict], min_score: int) -> list[dict]:
    """여러 포스트를 1회 호출로 일괄 검수 (본문 전체 기준). Returns: 포스트 순서대로 review_result 리스트."""
    blocks = "\n\n".join(_post_block(i + 1, p) for i, p in enumerate(posts))
    prompt = f"""아래 {len(posts)}개 블로그 포스트를 각각 엄격하게 검수하세요.

{REVIEW_CRITERIA}

합격 기준: {min_score}점 이상이며 severity "critical" 이슈가 없을 것 (기술 개념 오류는 critical).

{blocks}

반드시 아래 형식의 JSON 배열만 반환 (포스트 번호 순, 설명 문장 없이):
[
  {RESULT_SHAPE.format(index=1)},
  ...
]
"""
    raw = get_gemini_response(prompt, prefer=QUALITY)
    try:
        results = json.loads(_extract_json(raw, "["))
        if not isinstance(results, list):
            raise json.JSONDecodeError("not a list", raw, 0)
    except json.JSONDecodeError as e:
        logger.error(f"배치 검수 JSON 파싱 실패: {e}")
        return [_failed_review(min_score, f"파싱 실패: {e}") for _ in posts]

    reviews = []
    for i, post in enumerate(posts):
        r = next((x for x in results if isinstance(x, dict) and x.get("index") == i + 1), None)
        review = _review_from_result(r, min_score) if r else _failed_review(min_score, "결과 없음")
        reviews.append(review)
        status = "합격" if review["pass"] else "불합격"
        logger.info(f"[{i + 1}/{len(posts)}] '{post.get('title', '')}' {status} ({review['total_score']}/{min_score})")
        for issue in review["issues"]:
            logger.info(f"    - [{issue['severity']}] {issue['description']}")
    return reviews


def review_post(post: dict) -> dict:
    """단일 포스트 검수 (재작성 후 재검수용). 기준과 형식은 배치 검수와 같다."""
    min_score = load_config()["reviewer"]["min_score"]
    prompt = f"""아래 블로그 포스트를 엄격하게 검수하세요.

{REVIEW_CRITERIA}

합격 기준: {min_score}점 이상이며 severity "critical" 이슈가 없을 것 (기술 개념 오류는 critical).

{_post_block(1, post)}

반드시 아래 형식의 JSON 객체 하나만 반환 (설명 문장 없이):
{RESULT_SHAPE.format(index=1)}
"""
    raw = get_gemini_response(prompt, prefer=QUALITY)
    try:
        r = json.loads(_extract_json(raw, "{"))
        review = _review_from_result(r, min_score)
    except json.JSONDecodeError as e:
        logger.error(f"검수 결과 JSON 파싱 실패: {e}")
        review = _failed_review(min_score, f"파싱 실패: {e}")
    status = "합격" if review["pass"] else "불합격"
    logger.info(f"검수 결과: {status} | 점수: {review['total_score']}/{min_score}")
    return review


REVISION_KEYS = ("title", "meta_description", "tags", "content", "seo_keywords")


def revise_post(post: dict, review: dict) -> dict:
    """
    검수 불합격 시 원문과 지적 사항을 함께 주고 재작성.
    재작성 결과가 파싱되지 않거나 본문이 비면 원문을 그대로 돌려준다.
    카테고리·출처 주제 등 메타데이터는 원본을 유지한다.
    """
    issues_text = "\n".join(
        f"- [{i.get('severity', 'medium')}] {i.get('description', '')}" for i in review.get("issues", [])
    ) or "- (구체 이슈 없음)"
    original = {k: post.get(k) for k in REVISION_KEYS}
    prompt = f"""아래 블로그 포스트를 검수 지적에 따라 고쳐 쓰세요. 지적되지 않은 좋은 부분은 유지하세요.

{REVIEW_CRITERIA}

검수 점수: {review.get('total_score')}/{review.get('min_score')}
지적 사항:
{issues_text}
요약: {review.get('revision_notes', '')}

규칙:
- 기술 개념 오류는 반드시 바로잡을 것
- 출처 없는 비율·통계 수치는 삭제하고 정성적으로 서술할 것 ("(추측입니다)"를 붙여 남기지 말 것)
- 같은 JSON 키({", ".join(REVISION_KEYS)})로, 순수 JSON 객체만 반환

원문(JSON):
{json.dumps(original, ensure_ascii=False)}
"""
    raw = get_gemini_response(prompt, prefer=QUALITY)
    try:
        revised = json.loads(_extract_json(raw, "{"))
    except json.JSONDecodeError:
        logger.error("재작성 결과 파싱 실패 — 원본 유지")
        return post
    if not isinstance(revised, dict) or not str(revised.get("content", "")).strip():
        logger.error("재작성 결과에 본문 없음 — 원본 유지")
        return post

    merged = dict(post)
    for key in REVISION_KEYS:
        if revised.get(key):
            merged[key] = revised[key]
    merged["word_count"] = len(_content_text(merged).replace(" ", ""))
    merged["revised"] = True
    logger.info(f"재작성 완료: '{merged.get('title', '')}'")
    return merged


def run_reviewer_agent(posts: list[dict], max_revisions: int = 1) -> list[dict]:
    """
    포스트 리스트 전체 검수.
    - 정상 포스트: 배치 1회 호출로 일괄 검수
    - 불합격 포스트: 원문 기반 재작성 후 단일 검수 (최대 max_revisions회)
    - 끝까지 불합격이면 pass=False로 남겨 발행 단계에서 제외된다
    Returns: 검수 완료된 포스트 리스트 (review_result 포함)
    """
    logger.info(f"=== Reviewer Agent 시작: {len(posts)}개 포스트 ===")
    min_score = load_config()["reviewer"]["min_score"]

    error_posts = [p for p in posts if p.get("error")]
    valid_posts = [p for p in posts if not p.get("error")]

    if valid_posts:
        logger.info(f"배치 검수: {len(valid_posts)}개 포스트 -> 1회 API 호출 (본문 전체, 상위 모델 우선)")
        batch_reviews = batch_review_posts(valid_posts, min_score)
        if len(batch_reviews) != len(valid_posts):
            raise ValueError("검수 결과 수가 대상 포스트 수와 일치하지 않습니다.")
        for post, review in zip(valid_posts, batch_reviews):
            post["review_result"] = review

    for idx, post in enumerate(valid_posts):
        if post.get("review_result", {}).get("pass"):
            continue
        for attempt in range(1, max_revisions + 1):
            logger.info(f"재작성 시도 {attempt}/{max_revisions}: '{post.get('title')}'")
            post = revise_post(post, post["review_result"])
            post["review_result"] = review_post(post)
            valid_posts[idx] = post  # 재작성 결과를 목록에 반영 (이전에는 버려졌음)
            if post["review_result"]["pass"]:
                break
        else:
            logger.warning(f"재작성 후에도 불합격 - '{post.get('title')}' 발행 제외")

    reviewed_posts = error_posts + valid_posts
    passed = sum(1 for p in reviewed_posts if p.get("review_result", {}).get("pass"))
    logger.info(f"검수 완료: {passed}/{len(reviewed_posts)}개 합격")
    return reviewed_posts


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Reviewer Agent — 단독 실행은 run_agent.py를 통해 사용하세요.")
