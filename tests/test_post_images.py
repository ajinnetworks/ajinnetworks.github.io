"""대표 이미지·본문 이미지 처리 테스트 (agents/github_publisher.py).

배경: 작성 프롬프트가 Unsplash 사진 ID 5개를 고정 지정해, 341편 중 277편이 같은 사진을 반복(최다 260회).
"""
import glob
from pathlib import Path

from agents.github_publisher import (
    CATEGORY_HEROES, HERO_DIR, HERO_KEYWORDS, pick_hero_image, strip_external_images,
)
from agents.writer_agent import SITE_CATEGORIES


def test_every_referenced_illustration_exists():
    names = {n for _, n in HERO_KEYWORDS} | {n for v in CATEGORY_HEROES.values() for n in v}
    for name in names:
        assert Path(f".{HERO_DIR}/{name}.svg").is_file(), name


def test_every_site_category_has_a_hero():
    assert set(SITE_CATEGORIES) <= set(CATEGORY_HEROES)


def test_keyword_beats_category_and_is_stable():
    assert pick_hero_image("자동창고 AS/RS 도입 비용", "스마트팩토리") == f"{HERO_DIR}/logistics-asrs.svg"
    assert pick_hero_image("협동로봇 팔레타이징", "공장자동화") == f"{HERO_DIR}/palletizing.svg"
    t = "제조기업 가업승계 전략"
    assert pick_hero_image(t, "공장자동화") == pick_hero_image(t, "공장자동화")


def test_unknown_category_falls_back():
    assert pick_hero_image("무관한 제목", "없는카테고리").startswith(HERO_DIR)


def test_external_images_stripped_local_kept():
    md = "도입\n\n![a](https://images.unsplash.com/photo-1?w=800&q=80)\n\n\n본문 ![b](/assets/x.png)"
    out = strip_external_images(md)
    assert "unsplash" not in out and "/assets/x.png" in out and "\n\n\n" not in out


def test_writer_prompt_no_longer_requests_unsplash():
    assert "unsplash" not in Path("prompts/writer_prompt.md").read_text(encoding="utf-8").lower()


def test_no_post_points_at_missing_heroes_v2():
    assert not [f for f in glob.glob("_posts/*.md") if "/assets/images/heroes-v2/" in open(f, encoding="utf-8").read()]


def test_line_productivity_topics_use_oee_illustration():
    assert pick_hero_image("컨베이어 라인 택트타임 계산 방법", "물류자동화") == f"{HERO_DIR}/smart-oee.svg"


def test_post_layout_respects_explicit_image():
    """Codex 리뷰(#20): post.html 스크립트가 page.image를 카테고리 사진으로 덮어쓰던 문제."""
    layout = Path("_layouts/post.html").read_text(encoding="utf-8")
    script_at = layout.index("heroEl.style.setProperty")
    guard_at = layout.index("{%- unless explicit_hero -%}")
    assert guard_at < script_at < layout.index("{%- endunless -%}", script_at)
    assert '"/assets/img/og-default.png"' in layout  # 사이트 기본값은 고유 이미지로 보지 않음
