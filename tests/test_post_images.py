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


def test_every_post_has_a_hero_image():
    import glob, re
    missing = [f for f in glob.glob("_posts/*.md")
               if not re.search(r"^(og_)?image:", open(f, encoding="utf-8").read().split("---", 2)[1], re.M)]
    assert missing == []


def test_hero_v2_svgs_have_png_for_social_preview():
    """SNS(카카오·페이스북 등)는 og:image로 SVG를 표시하지 않으므로 PNG 짝이 필요."""
    for svg in Path("assets/img/hero-v2").glob("*.svg"):
        assert svg.with_suffix(".png").exists(), svg


def test_social_and_jsonld_images_use_png_and_existing_paths():
    post = Path("_layouts/post.html").read_text(encoding="utf-8")
    assert "/assets/images/og-default.png" not in post and "/assets/images/logo.png" not in post
    for f in ("_layouts/post.html", "_includes/head.html", "_layouts/default.html"):
        for line in Path(f).read_text(encoding="utf-8").splitlines():
            if 'og:image"' in line or 'twitter:image"' in line or '"image":' in line:
                if "page.image" in line or "phase2_image" in line:
                    assert "replace: '.svg', '.png'" in line, (f, line)


def test_new_topic_illustrations_are_used():
    assert pick_hero_image("SK하이닉스 HBM 수율", "스마트팩토리").endswith("/semiconductor-fab.svg")
    assert pick_hero_image("에너지 관리 시스템(FEMS) 도입", "스마트팩토리").endswith("/energy-fems.svg")
    assert pick_hero_image("중대재해처벌법 대응 안전 모니터링", "스마트팩토리").endswith("/safety-monitoring.svg")
    assert pick_hero_image("초고속 소터와 AMR", "물류자동화").endswith("/sorter.svg")
    assert pick_hero_image("딥러닝 비전검사로 미세 결함", "딥러닝비전").endswith("/deep-learning-defect.svg")
    assert pick_hero_image("오타니로 본 예측 보전", "스마트팩토리").endswith("/smart-oee.svg")


def test_every_hero_illustration_file_exists_and_no_image_dominates():
    import collections, glob, re
    from agents.github_publisher import CATEGORY_HEROES, HERO_KEYWORDS
    names = {n for _, n in HERO_KEYWORDS}
    for opts in CATEGORY_HEROES.values():
        names.update(opts)
    for n in names:
        assert Path(f"assets/img/hero-v2/{n}.svg").exists() and Path(f"assets/img/hero-v2/{n}.png").exists(), n
    used = collections.Counter(
        m.group(1) for f in glob.glob("_posts/*.md")
        if (m := re.search(r"^image:\s*\S+/hero-v2/(\S+)\.svg", open(f, encoding="utf-8").read().split("---", 2)[1], re.M)))
    assert max(used.values()) <= 0.2 * sum(used.values())  # 한 그림이 20% 넘게 반복되지 않게
