"""
publisher_agent.py — 플랫폼 발행 에이전트
Goal: 검수 완료 포스트를 Tistory/WordPress에 자동 발행
Human-in-the-loop 게이트 포함
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

import requests
import yaml

logger = logging.getLogger(__name__)


def load_config() -> dict:
    config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ─── Human-in-the-loop Gate ─────────────────────────────────────────────────

def human_approval_gate(post: dict) -> bool:
    """
    HUMAN_GATE=true 환경변수 설정 시 발행 전 터미널 승인 요구.
    CI/CD 환경에서는 false로 설정하여 완전 자동화 가능.
    """
    if os.environ.get("HUMAN_GATE", "true").lower() != "true":
        return True

    print("\n" + "="*60)
    print("📋 발행 전 승인 요청")
    print("="*60)
    print(f"제목   : {post.get('title', 'N/A')}")
    print(f"카테고리: {post.get('category', 'N/A')}")
    print(f"태그   : {post.get('tags', [])}")
    print(f"초안   : {post.get('draft_path', 'N/A')}")
    score = post.get("review_result", {}).get("total_score", "N/A")
    print(f"검수점수: {score}/100")
    print("="*60)

    answer = input("발행하시겠습니까? (y/n/skip): ").strip().lower()
    if answer == "y":
        logger.info(f"✅ 승인: '{post.get('title')}'")
        return True
    elif answer == "skip":
        logger.info(f"⏭️  스킵: '{post.get('title')}'")
        return False
    else:
        logger.info(f"❌ 거절: '{post.get('title')}'")
        return False


# ─── Tistory Publisher ────────────────────────────────────────────────────────

def publish_to_tistory(post: dict) -> dict:
    """
    Tistory Open API를 통해 포스트 발행.
    API 문서: https://tistory.github.io/document-tistory-apis/
    주의: Tistory API v1 — 변경 가능성 있음 (확실하지 않음)
    """
    access_token = os.environ.get("TISTORY_ACCESS_TOKEN")
    blog_name = os.environ.get("TISTORY_BLOG_NAME")

    if not access_token or not blog_name:
        raise ValueError("TISTORY_ACCESS_TOKEN 또는 TISTORY_BLOG_NAME 미설정")

    url = "https://www.tistory.com/apis/post/write"
    params = {
        "access_token": access_token,
        "output": "json",
        "blogName": blog_name,
        "title": post.get("title", ""),
        "content": post.get("content", ""),
        "visibility": "3",      # 0:비공개, 1:보호, 3:공개
        "category": "0",        # 0=기본 카테고리 (카테고리 ID 직접 입력 가능)
        "tag": ",".join(post.get("tags", [])[:10]),  # 최대 10개
    }

    resp = requests.post(url, data=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if data.get("tistory", {}).get("status") != "200":
        raise RuntimeError(f"Tistory 발행 실패: {data}")

    post_id = data["tistory"]["postId"]
    post_url = data["tistory"]["url"]
    logger.info(f"Tistory 발행 완료: {post_url}")
    return {"platform": "tistory", "post_id": post_id, "url": post_url}


# ─── WordPress Publisher ──────────────────────────────────────────────────────

def publish_to_wordpress(post: dict) -> dict:
    """
    WordPress REST API v2를 통해 포스트 발행.
    App Password 인증 사용.
    """
    wp_url = os.environ.get("WORDPRESS_URL", "").rstrip("/")
    username = os.environ.get("WORDPRESS_USERNAME")
    app_password = os.environ.get("WORDPRESS_APP_PASSWORD")

    if not all([wp_url, username, app_password]):
        raise ValueError("WordPress 환경변수 미설정 (URL/USERNAME/APP_PASSWORD)")

    api_url = f"{wp_url}/wp-json/wp/v2/posts"
    payload = {
        "title": post.get("title", ""),
        "content": post.get("content", ""),
        "status": "publish",
        "tags": post.get("tags", []),
        "excerpt": post.get("meta_description", ""),
    }

    resp = requests.post(
        api_url,
        json=payload,
        auth=(username, app_password),
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    post_id = data.get("id")
    post_url = data.get("link")
    logger.info(f"WordPress 발행 완료: {post_url}")
    return {"platform": "wordpress", "post_id": post_id, "url": post_url}


# ─── 발행 결과 저장 ──────────────────────────────────────────────────────────

def save_published_record(post: dict, publish_result: dict) -> str:
    published_dir = Path(__file__).parent.parent / "output" / "published"
    published_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(
        c if c.isalnum() or c in "_ " else "_"
        for c in post.get("title", "published")
    )[:30]

    record = {
        "published_at": datetime.now().isoformat(),
        "title": post.get("title"),
        "platform": publish_result.get("platform"),
        "post_id": publish_result.get("post_id"),
        "url": publish_result.get("url"),
        "review_score": post.get("review_result", {}).get("total_score"),
        "tags": post.get("tags", []),
        "word_count": post.get("word_count", 0),
    }

    record_path = published_dir / f"{timestamp}_{safe_title}.json"
    record_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    logger.info(f"발행 기록 저장: {record_path}")
    return str(record_path)


# ─── 메인 ────────────────────────────────────────────────────────────────────

def run_publisher_agent(posts: list[dict]) -> list[dict]:
    """
    검수 완료 포스트 발행.
    Human-in-the-loop 게이트 통과 시만 발행.
    """
    config = load_config()
    platform = config["blog"]["platform"]
    logger.info(f"=== Publisher Agent 시작: 플랫폼={platform} ===")

    publishers = {
        "tistory": publish_to_tistory,
        "wordpress": publish_to_wordpress,
    }

    publish_func = publishers.get(platform)
    if not publish_func:
        raise ValueError(f"지원하지 않는 플랫폼: {platform} (tistory/wordpress만 지원)")

    results = []
    for post in posts:
        if post.get("error"):
            logger.warning(f"오류 포스트 스킵: {post.get('title')}")
            continue

        if not post.get("review_result", {}).get("pass"):
            logger.warning(f"검수 미합격 포스트 스킵: {post.get('title')}")
            continue

        # Human-in-the-loop 게이트
        if not human_approval_gate(post):
            logger.info(f"사용자 거절/스킵: {post.get('title')}")
            continue

        try:
            result = publish_func(post)
            record_path = save_published_record(post, result)
            result["record_path"] = record_path
            results.append(result)
            logger.info(f"발행 성공: {result.get('url')}")
        except Exception as e:
            logger.error(f"발행 실패 '{post.get('title')}': {e}")
            results.append({
                "title": post.get("title"),
                "error": str(e),
                "platform": platform,
            })

    logger.info(f"Publisher 완료: {len(results)}개 처리")
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Publisher Agent — 단독 실행은 run_agent.py를 통해 사용하세요.")
