"""발행 카테고리 정규화 테스트 (agents/writer_agent.py).

사이트는 카테고리 5종(category/*.md, _layouts/post.html 히어로)만 쓴다.
2026-11-26 시험 실행에서 '딥러닝비전'이 '스마트팩토리'로 잘못 보정된 문제의 회귀 테스트.
"""
from pathlib import Path

import pytest

from agents.writer_agent import (
    BLOG_CATEGORIES,
    SITE_CATEGORIES,
    TAXONOMY_TO_SITE,
    classify_category,
    validate_category,
)


def test_site_categories_match_category_pages():
    pages = {p.stem for p in Path("category").glob("*.md")}
    assert set(SITE_CATEGORIES) == pages


@pytest.mark.parametrize("cat", ["물류자동화", "공장자동화", "딥러닝비전", "스마트팩토리", "제어SW"])
def test_site_categories_kept_as_is(cat):
    assert validate_category(cat) == cat


def test_every_taxonomy_category_maps_into_site():
    for cat in BLOG_CATEGORIES:
        assert TAXONOMY_TO_SITE[cat["name"]] in SITE_CATEGORIES
        assert validate_category(cat["name"]) in SITE_CATEGORIES


@pytest.mark.parametrize("raw,expected", [
    ("비전검사", "딥러닝비전"),
    ("PLC제어", "제어SW"),
    ("포장자동화", "공장자동화"),
    ("공장자동화/스마트팩토리", "공장자동화"),
    ("제어 SW", "제어SW"),
    ("머신비전", "딥러닝비전"),
    ("물류", "물류자동화"),
])
def test_model_variants_normalized(raw, expected):
    assert validate_category(raw) == expected


def test_unknown_uses_fallback_then_default():
    assert validate_category("Factory Automation", fallback="공장자동화") == "공장자동화"
    assert validate_category("", fallback="잘못된값") == "스마트팩토리"


@pytest.mark.parametrize("keyword,expected", [
    ("딥러닝 비전검사 오검출 줄이는 방법", "딥러닝비전"),
    ("AMR 도입 전 물류 동선 분석", "물류자동화"),
    ("PLC 통신 프로토콜 선택 가이드", "제어SW"),
    ("협동로봇 팔레타이징 도입 체크리스트", "공장자동화"),
])
def test_pre_classification_returns_site_category(keyword, expected):
    assert classify_category(keyword, "") == expected
