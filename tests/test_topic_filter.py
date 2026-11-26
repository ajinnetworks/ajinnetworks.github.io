"""주제 선정 도메인 필터 테스트 (agents/trend_agent.py)."""
import json
from datetime import date
from unittest.mock import patch

from agents.trend_agent import (
    build_candidates,
    is_domain_relevant,
    select_topics_via_gemini,
)

EVERGREEN = [
    "협동로봇 팔레타이징 도입 체크리스트",
    "딥러닝 비전검사 오검출 줄이는 방법",
    "AMR 도입 전 물류 동선 분석",
    "PLC 통신 프로토콜 선택 가이드",
    "AOI 검사 장비 선정 기준",
    "컨베이어 라인 택트타임 계산",
    "자동창고 AS/RS 도입 비용과 ROI",
]


def trends(*keywords):
    return [{"keyword": k, "source": "google_trends"} for k in keywords]


class TestDomainRelevance:
    def test_off_domain_trends_rejected(self):
        # 2026-11-26 시험 실행에서 실제로 선정됐던 주제들
        for kw in ["k-라면", "부산일보", "연금"]:
            assert not is_domain_relevant(kw)

    def test_domain_trends_accepted(self):
        for kw in ["삼성 반도체 수율", "현대차 로봇 공장", "AMR 물류", "plc 교체"]:
            assert is_domain_relevant(kw)

    def test_all_configured_evergreen_topics_are_on_domain(self):
        import yaml
        cfg = yaml.safe_load(open("config/settings.yaml", encoding="utf-8"))
        topics = cfg["trend"]["evergreen_topics"]
        assert len(topics) >= 12
        assert all(is_domain_relevant(t) for t in topics)


class TestBuildCandidates:
    def test_off_domain_trends_replaced_by_evergreen(self):
        c = build_candidates(trends("k-라면", "부산일보", "연금"), EVERGREEN, 3, [], date(2026, 11, 26))
        assert c and all(x["source"] == "evergreen" for x in c)
        assert len(c) == 6  # max(top_n*2, top_n+3)

    def test_domain_trend_kept_first(self):
        c = build_candidates(trends("k-라면", "현대차 로봇 공장"), EVERGREEN, 3, [], date(2026, 11, 26))
        assert c[0] == {"keyword": "현대차 로봇 공장", "source": "google_trends"}

    def test_excluded_keywords_blocked_even_if_domain_like(self):
        c = build_candidates(trends("결제 자동화"), EVERGREEN, 3, [], date(2026, 11, 26))
        assert "결제 자동화" not in [x["keyword"] for x in c]

    def test_recently_published_topic_skipped(self):
        recent = ["PLC 통신 프로토콜 선택 가이드"]
        c = build_candidates([], EVERGREEN, 3, recent, date(2026, 11, 26))
        assert "PLC 통신 프로토콜 선택 가이드" not in [x["keyword"] for x in c]

    def test_evergreen_order_rotates_by_date(self):
        a = [x["keyword"] for x in build_candidates([], EVERGREEN, 3, [], date(2026, 11, 26))]
        b = [x["keyword"] for x in build_candidates([], EVERGREEN, 3, [], date(2026, 11, 26))]
        c = [x["keyword"] for x in build_candidates([], EVERGREEN, 3, [], date(2026, 11, 28))]
        assert a == b  # 같은 날은 재현 가능
        assert a != c  # 다른 날은 다른 순서

    def test_duplicates_removed(self):
        c = build_candidates(trends("AMR 물류", "AMR  물류"), EVERGREEN, 3, [], date(2026, 11, 26))
        assert [x["keyword"] for x in c].count("AMR 물류") == 1


class TestSelectionGuard:
    def _run(self, model_keywords, candidates, top_n=3):
        reply = json.dumps({"selected_topics": [
            {"keyword": k, "angle": "a", "reason": "r", "estimated_search_volume": "high"}
            for k in model_keywords
        ]}, ensure_ascii=False)
        with patch("agents.trend_agent.get_gemini_response", return_value=reply):
            return select_topics_via_gemini(candidates, "스마트팩토리", top_n)

    def test_topic_outside_candidates_dropped_and_backfilled(self):
        cands = [{"keyword": k, "source": "evergreen"} for k in EVERGREEN[:4]]
        out = self._run(["k-라면", EVERGREEN[1], "연금"], cands)
        kws = [t["keyword"] for t in out]
        assert len(kws) == 3
        assert "k-라면" not in kws and "연금" not in kws
        assert set(kws) <= set(EVERGREEN[:4])

    def test_whitespace_variants_matched_to_candidate_text(self):
        cands = [{"keyword": "AMR 도입 전 물류 동선 분석", "source": "evergreen"}]
        out = self._run(["AMR도입 전 물류동선 분석"], cands, top_n=1)
        assert out[0]["keyword"] == "AMR 도입 전 물류 동선 분석"


class TestEvergreenExhaustion:
    def test_all_evergreen_recently_used_reuses_oldest_first(self):
        # 최신순 제목: 0번이 가장 최근. 모든 상시 주제가 최근에 쓰인 상태
        recent = [f"{kw} 실무 가이드" for kw in EVERGREEN]
        c = build_candidates(trends("k-라면"), EVERGREEN, 3, recent, date(2026, 11, 26))
        assert len(c) == 6  # 발행이 멈추지 않음
        assert all(x["source"] == "evergreen_reuse" for x in c)
        # 가장 오래전에 쓴 것(목록 끝)부터
        assert [x["keyword"] for x in c] == list(reversed(EVERGREEN))[:6]

    def test_fresh_topics_preferred_over_reuse(self):
        recent = [f"{kw} 가이드" for kw in EVERGREEN[:5]]
        c = build_candidates([], EVERGREEN, 3, recent, date(2026, 11, 26))
        sources = [x["source"] for x in c]
        assert sources[:2] == ["evergreen", "evergreen"]  # 남은 신규 2개 먼저
        assert sources[2:] == ["evergreen_reuse"] * 4


class TestModelSelection:
    def test_pick_models_latest_per_family_then_aliases(self):
        from agents.gemini_client import pick_models
        ids = ["gemini-2.5-pro", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite",
               "gemini-3.8-flash", "gemini-3.6-flash", "gemini-flash-latest",
               "gemini-3.8-flash-preview-09", "text-embedding-005"]
        assert pick_models(ids) == ["gemini-3.5-flash-lite", "gemini-2.5-pro",
                                    "gemini-3.8-flash", "gemini-flash-latest"]

    def test_env_models_used_without_discovery(self, monkeypatch):
        from agents import gemini_client
        monkeypatch.setenv("GEMINI_MODELS", "m-a, m-b,m-a")
        with patch.object(gemini_client, "discover_models", side_effect=AssertionError):
            assert gemini_client.configured_models("k") == ["m-a", "m-b"]

    def test_discovery_used_when_env_empty(self, monkeypatch):
        from agents import gemini_client
        monkeypatch.delenv("GEMINI_MODELS", raising=False)
        with patch.object(gemini_client, "discover_models", return_value=("x-1", "x-2")):
            assert gemini_client.configured_models("k") == ["x-1", "x-2"]
