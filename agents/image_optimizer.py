"""
image_optimizer.py — 블로그 이미지 자동 삽입 및 사이즈 최적화
Unsplash API를 통해 포스트 주제에 맞는 이미지를 자동 검색·삽입
"""

import logging
import os
import re
import requests
from typing import Optional

logger = logging.getLogger(__name__)

# 이미지 표준 사이즈 설정
IMAGE_SIZES = {
    "hero": {"width": 1200, "height": 630},      # 썸네일/대표이미지
    "content": {"width": 800, "height": 450},     # 본문 이미지
    "inline": {"width": 600, "height": 338},      # 인라인 이미지
}


def fetch_unsplash_image(keyword: str, size: str = "content") -> Optional[dict]:
    """
    Unsplash API로 키워드 관련 이미지 검색.
    UNSPLASH_ACCESS_KEY 환경변수 필요.
    """
    access_key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not access_key:
        logger.warning("UNSPLASH_ACCESS_KEY 없음 — 기본 이미지 사용")
        return None

    try:
        w = IMAGE_SIZES[size]["width"]
        h = IMAGE_SIZES[size]["height"]

        resp = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": keyword,
                "per_page": 1,
                "orientation": "landscape",
                "content_filter": "high",
            },
            headers={"Authorization": f"Client-ID {access_key}"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        if not data.get("results"):
            return None

        photo = data["results"][0]
        img_url = f"{photo['urls']['raw']}&w={w}&h={h}&fit=crop&auto=format"
        alt_text = photo.get("alt_description") or keyword
        photographer = photo["user"]["name"]

        return {
            "url": img_url,
            "alt": alt_text,
            "photographer": photographer,
            "width": w,
            "height": h,
            "credit": f"Photo by {photographer} on Unsplash",
        }

    except Exception as e:
        logger.error(f"Unsplash 이미지 검색 실패: {e}")
        return None


def get_default_image(keyword: str, size: str = "content") -> dict:
    """
    Unsplash 실패 시 사용할 기본 이미지.
    공장자동화 관련 Picsum 이미지 사용.
    """
    w = IMAGE_SIZES[size]["width"]
    h = IMAGE_SIZES[size]["height"]

    # 공장/기술 관련 기본 이미지 시드값
    seed_map = {
        "자동화": 1067,
        "로봇": 1035,
        "스마트팩토리": 1076,
        "AI": 1040,
        "물류": 1080,
        "default": 1067,
    }

    seed = seed_map.get("default", 1067)
    for key in seed_map:
        if key in keyword:
            seed = seed_map[key]
            break

    return {
        "url": f"https://picsum.photos/seed/{seed}/{w}/{h}",
        "alt": f"{keyword} 관련 이미지",
        "photographer": "Picsum Photos",
        "width": w,
        "height": h,
        "credit": "",
    }


def insert_images_into_content(
    content: str,
    keywords: list[str],
    image_count: int = 3,
) -> str:
    """
    마크다운 본문에 이미지를 자동 삽입.
    H2 섹션 헤더 아래에 관련 이미지를 삽입.
    """
    if not content:
        return content

    h2_pattern = re.compile(r"^(## .+)$", re.MULTILINE)
    h2_matches = list(h2_pattern.finditer(content))

    if not h2_matches:
        return content

    # 삽입할 이미지 수 결정
    insert_count = min(image_count, len(h2_matches), 3)
    keyword_idx = 0

    result = content
    offset = 0

    for i in range(insert_count):
        if i >= len(h2_matches):
            break

        match = h2_matches[i]
        keyword = keywords[keyword_idx % len(keywords)] if keywords else "공장자동화"
        keyword_idx += 1

        # 이미지 크기 결정
        size = "hero" if i == 0 else "content"

        # 이미지 검색
        img = fetch_unsplash_image(keyword, size)
        if not img:
            img = get_default_image(keyword, size)

        # 마크다운 이미지 태그 생성
        img_md = (
            f"\n\n![{img['alt']}]({img['url']})"
            f"{{: width=\"{img['width']}\" height=\"{img['height']}\" "
            f"loading=\"lazy\" style=\"width:100%;height:auto;border-radius:8px;\"}}\n"
        )

        if img.get("credit"):
            img_md += f"*{img['credit']}*\n"

        # H2 헤더 다음 줄에 삽입
        insert_pos = match.end() + offset
        result = result[:insert_pos] + img_md + result[insert_pos:]
        offset += len(img_md)

    return result


def optimize_existing_images(content: str) -> str:
    """
    기존 마크다운 이미지 태그에 사이즈 속성 추가.
    ![alt](url) → ![alt](url){: width="800" height="450" loading="lazy"}
    """
    # 이미 속성이 있는 이미지는 스킵
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)(?!\{)")

    def add_size_attrs(match):
        alt = match.group(1)
        url = match.group(2)
        return (
            f"![{alt}]({url})"
            f'{{: width="800" height="450" loading="lazy" '
            f'style="width:100%;height:auto;"}}'
        )

    return pattern.sub(add_size_attrs, content)
