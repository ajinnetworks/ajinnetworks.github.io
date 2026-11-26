"""검수 에이전트 테스트 (agents/reviewer_agent.py, gemini_client.order_models).

2026-11-26 run #117 발행 글 검토에서 확인된 문제의 회귀 테스트:
- 검수가 본문 앞 400자만 봄 → 택트타임 개념 오류·지어낸 수치가 85/80/75점으로 통과
- 재작성 프롬프트에 원문이 없음, 재작성 결과가 목록에 반영되지 않음
"""
import json
from unittest.mock import patch

import yaml

from agents import reviewer_agent as ra
from agents.gemini_client import order_models

LONG_TAIL = "택트타임을 30% 단축할 수 있습니다(추측입니다)."


def make_post(title="컨베이어 라인 택트타임 계산", content=None, **extra):
    body = content if content is not None else ("가" * 900) + LONG_TAIL
    post = {"title": title, "category": "공장자동화", "content": body,
            "source_topic": {"keyword": title}, "meta_description": "d", "tags": ["t"]}
    post.update(extra)
    return post


def result(index=1, score=90, issues=None, reason="ok"):
    return {"index": index, "score": score, "issues": issues or [], "reason": reason}


class TestConfig:
    def test_min_score_is_80(self):
        cfg = yaml.safe_load(open("config/settings.yaml", encoding="utf-8"))
        assert cfg["reviewer"]["min_score"] == 80


class TestModelOrder:
    def test_quality_puts_lite_last(self):
        models = ["gemini-3.5-flash-lite", "gemini-2.5-pro", "gemini-3.8-flash", "gemini-flash-latest"]
        assert order_models(models, "quality") == [
            "gemini-3.8-flash", "gemini-flash-latest", "gemini-2.5-pro", "gemini-3.5-flash-lite"]

    def test_default_keeps_order(self):
        models = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]
        assert order_models(models) == models


class TestBatchReview:
    def test_full_body_sent_and_quality_model_requested(self):
        post = make_post()
        with patch.object(ra, "get_gemini_response", return_value=json.dumps([result()])) as m:
            ra.batch_review_posts([post], 80)
        prompt, kwargs = m.call_args[0][0], m.call_args[1]
        assert LONG_TAIL in prompt  # 900자 뒤 문장까지 검수 대상 (기존: 앞 400자만)
        assert "기술 정확성" in prompt and "택트타임" in prompt
        assert kwargs.get("prefer") == "quality"

    def test_threshold_and_critical_issue(self):
        posts = [make_post("a"), make_post("b"), make_post("c")]
        reply = [
            result(1, 85),
            result(2, 79),
            result(3, 95, issues=[{"severity": "critical", "description": "택트타임/사이클타임 혼동"}]),
        ]
        with patch.object(ra, "get_gemini_response", return_value=json.dumps(reply, ensure_ascii=False)):
            reviews = ra.batch_review_posts(posts, 80)
        assert [r["pass"] for r in reviews] == [True, False, False]
        assert reviews[2]["issues"][0]["severity"] == "critical"

    def test_json_with_preamble_and_fence_parsed(self):
        raw = "검수 결과입니다.\n```json\n" + json.dumps([result(1, 88)]) + "\n```"
        with patch.object(ra, "get_gemini_response", return_value=raw):
            assert ra.batch_review_posts([make_post()], 80)[0]["pass"] is True

    def test_unparseable_fails_closed(self):
        with patch.object(ra, "get_gemini_response", return_value="not json"):
            reviews = ra.batch_review_posts([make_post(), make_post()], 80)
        assert [r["pass"] for r in reviews] == [False, False]


class TestRevise:
    def test_prompt_contains_original_and_metadata_kept(self):
        post = make_post()
        revised = {"title": "새 제목", "content": "고친 본문", "tags": ["x"]}
        with patch.object(ra, "get_gemini_response", return_value=json.dumps(revised, ensure_ascii=False)) as m:
            out = ra.revise_post(post, {"total_score": 70, "min_score": 80,
                                        "issues": [{"severity": "critical", "description": "개념 오류"}]})
        prompt = m.call_args[0][0]
        assert LONG_TAIL in prompt and "개념 오류" in prompt  # 원문 + 지적 사항 모두 전달
        assert out["content"] == "고친 본문" and out["title"] == "새 제목"
        assert out["category"] == "공장자동화" and out["source_topic"] == post["source_topic"]
        assert out["revised"] is True

    def test_empty_revision_keeps_original(self):
        post = make_post()
        with patch.object(ra, "get_gemini_response", return_value=json.dumps({"title": "x", "content": ""})):
            assert ra.revise_post(post, {"issues": []}) is post


class TestRunReviewer:
    def test_revision_written_back_and_published_only_if_passing(self):
        posts = [make_post("good"), make_post("fixable"), make_post("hopeless")]
        batch = json.dumps([result(1, 90), result(2, 60), result(3, 50)])

        def fake_revise(post, review):
            return {**post, "content": "고친 본문 " + post["title"], "revised": True}

        single = iter([
            ra._review_from_result(result(1, 88), 80),  # fixable → 재작성 후 합격
            ra._review_from_result(result(1, 70), 80),  # hopeless → 재작성 후에도 불합격
        ])
        with patch.object(ra, "get_gemini_response", return_value=batch), \
             patch.object(ra, "revise_post", side_effect=fake_revise), \
             patch.object(ra, "review_post", side_effect=lambda p: next(single)):
            out = ra.run_reviewer_agent(posts)

        by_title = {p["title"]: p for p in out}
        assert by_title["good"]["review_result"]["pass"] is True
        assert by_title["fixable"]["content"] == "고친 본문 fixable"  # 재작성본이 목록에 반영됨
        assert by_title["fixable"]["review_result"]["pass"] is True
        assert by_title["hopeless"]["review_result"]["pass"] is False  # 발행 단계에서 제외됨
        assert "forced_pass" not in by_title["hopeless"]["review_result"]
