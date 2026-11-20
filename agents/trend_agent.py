"""
trend_agent.py — 트렌드 크롤링 & 주제 선정 에이전트
Goal: 실시간 트렌드에서 블로그 포스팅 키워드 3개 선정
"""

import json
import logging
import os
from datetime import datetime
from typing import Optional

from google import genai as google_genai
import requests
import yaml

# 안정 버전 모델만 사용. 필요하면 Actions 변수 GEMINI_MODELS로 쉼표 구분 재정의.
GEMINI_MODELS = [
    model.strip()
    for model in os.environ.get(
        "GEMINI_MODELS",
        "gemini-3.8-flash,gemini-3.5-flash-lite",
    ).split(",")
    if model.strip()
]

import io
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding='utf-8', errors='replace'
    )


from agents.writer_agent import is_valid_topic, EXCLUDE_KEYWORDS

logger = logging.getLogger(__name__)


def _gemini_http_status(error: Exception) -> int | None:
    """google-genai 오류에서 HTTP 상태 코드를 가능한 한 구조적으로 추출."""
    import re

    for attribute in ("code", "status_code", "status"):
        value = getattr(error, attribute, None)
        try:
            status = int(value)
        except (TypeError, ValueError):
            continue
        if 100 <= status <= 599:
            return status

    match = re.search(r"\b(400|401|403|404|429)\b", str(error))
    return int(match.group(1)) if match else None


def get_gemini_response(prompt: str) -> str:
    """사용 가능한 모델을 순회하고, 429 응답만 한 번 제한 재시도."""
    import time

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY가 비어 있습니다.")

    if not GEMINI_MODELS:
        raise RuntimeError("GEMINI_MODELS에 사용할 모델이 지정되지 않았습니다.")

    client = google_genai.Client(api_key=api_key)
    unavailable_models: set[str] = set()
    rate_limited_models: set[str] = set()
    last_errors: dict[str, str] = {}

    for attempt in range(2):
        attempted_rate_limited_model = False
        for model_name in GEMINI_MODELS:
            if model_name in unavailable_models:
                continue
            if attempt == 1 and model_name not in rate_limited_models:
                continue

            try:
                response = client.models.generate_content(model=model_name, contents=prompt)
                text = (response.text or "").strip()
                if not text:
                    raise RuntimeError(f"{model_name}에서 빈 응답을 받았습니다.")
                logger.info(f"[MODEL] {model_name} 사용")
                return text
            except Exception as error:
                status = _gemini_http_status(error)
                last_errors[model_name] = f"HTTP {status or 'unknown'}: {error}"
                if status == 404:
                    unavailable_models.add(model_name)
                    logger.error(
                        "[MODEL NOT FOUND] %s: %s — 이 모델은 재시도하지 않습니다.",
                        model_name,
                        error,
                    )
                    continue
                if status == 429 or type(error).__name__ == "ResourceExhausted":
                    rate_limited_models.add(model_name)
                    attempted_rate_limited_model = True
                    logger.warning("[RATE LIMIT] %s 호출 제한: %s", model_name, error)
                    continue
                raise RuntimeError(
                    f"Gemini 요청 실패 (model={model_name}, HTTP {status or 'unknown'}): {error}"
                ) from error

        if attempt == 0 and attempted_rate_limited_model:
            logger.warning("[RATE LIMIT] 429 모델만 65초 후 1회 재시도합니다.")
            time.sleep(65)
            continue
        break

    if rate_limited_models:
        detail = "; ".join(last_errors[m] for m in rate_limited_models)
        raise RuntimeError(f"Gemini 모델 호출 한도 초과 (429, 1회 재시도 후): {detail}")
    detail = "; ".join(last_errors.values()) or "시도 가능한 모델이 없습니다."
    raise RuntimeError(f"사용 가능한 Gemini 모델을 찾지 못했습니다. 모델 ID와 API 접근 권한을 확인하세요: {detail}")


def load_config() -> dict:
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "settings.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_google_trends_rss() -> list[dict]:
    """
    Google 트렌드 RSS에서 현재 인기 검색어를 가져옵니다.
    RSS 주소는 공개 엔드포인트 사용 (확실하지 않음 — 변경될 수 있음).
    """
    url = "https://trends.google.com/trending/rss?geo=KR"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        # 간단한 XML 파싱 (추가 의존성 없이)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(resp.content)
        items = root.findall(".//item")
        trends = []
        for item in items[:20]:
            title_el = item.find("title")
            if title_el is not None and title_el.text:
                trends.append({"keyword": title_el.text, "source": "google_trends"})
        logger.info(f"Google Trends: {len(trends)}개 키워드 수집")
        return trends
    except Exception as e:
        logger.warning(f"Google Trends 수집 실패 (무시하고 계속): {e}")
        return []


def fetch_naver_datalab_trends() -> list[dict]:
    """
    네이버 데이터랩 트렌드 수집.
    주의: 공식 API가 아닌 검색 RSS 활용 — 정식 지원 여부 확실하지 않음.
    """
    url = "https://www.naver.com/rss/trending"  # 추측입니다 — 실제 URL 확인 필요
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        import xml.etree.ElementTree as ET
        root = ET.fromstring(resp.content)
        items = root.findall(".//item")
        trends = []
        for item in items[:20]:
            title_el = item.find("title")
            if title_el is not None and title_el.text:
                trends.append({"keyword": title_el.text, "source": "naver"})
        logger.info(f"Naver Trends: {len(trends)}개 키워드 수집")
        return trends
    except Exception as e:
        logger.warning(f"Naver Trends 수집 실패 (무시하고 계속): {e}")
        return []


def fetch_reddit_kr_trends() -> list[dict]:
    """Reddit r/korea 최신 인기 포스트 제목 수집."""
    url = "https://www.reddit.com/r/korea/hot.json?limit=20"
    headers = {"User-Agent": "BlogAgent/1.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        posts = data.get("data", {}).get("children", [])
        trends = []
        for post in posts:
            title = post.get("data", {}).get("title", "")
            if title:
                trends.append({"keyword": title[:50], "source": "reddit_kr"})
        logger.info(f"Reddit KR: {len(trends)}개 키워드 수집")
        return trends
    except Exception as e:
        logger.warning(f"Reddit KR 수집 실패 (무시하고 계속): {e}")
        return []


def select_topics_via_gemini(
    raw_trends: list[dict],
    blog_domain: str,
    top_n: int = 3,
) -> list[dict]:
    """
    Gemini API를 통해 수집된 트렌드 중 블로그 도메인에 적합한 주제 top_n개 선정.
    Manager AI 역할: 전략적 주제 선정.
    """
    trends_text = "\n".join(
        [f"- [{t['source']}] {t['keyword']}" for t in raw_trends[:50]]
    )

    prompt = f"""
당신은 블로그 주제 선정 전문가입니다.

블로그 도메인: {blog_domain}
현재 트렌드 목록:
{trends_text}

위 트렌드 중에서 블로그 도메인과 연관성이 높고,
검색 유입이 기대되는 주제를 {top_n}개 선정하세요.

출력은 반드시 아래 JSON 형식만 반환하세요. 설명 없이 JSON만 출력:
{{
  "selected_topics": [
    {{
      "keyword": "선정 키워드",
      "angle": "포스트 접근 각도 (한 문장)",
      "reason": "선정 이유 (한 문장)",
      "estimated_search_volume": "high|medium|low"
    }}
  ]
}}
"""

    raw = get_gemini_response(prompt)
    # JSON 펜스 제거
    if "```" in raw:
        parts = raw.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                raw = part
                break
    result = json.loads(raw.strip())
    logger.info(f"Gemini가 {len(result['selected_topics'])}개 주제 선정 완료")
    return result["selected_topics"]


def run_trend_agent(blog_domain: Optional[str] = None) -> list[dict]:
    """
    트렌드 에이전트 메인 실행 함수.
    Returns: 선정된 주제 리스트
    """
    config = load_config()
    domain = blog_domain or config["blog"]["default_category"]

    logger.info("=== Trend Agent 시작 ===")

    # 병렬 수집 (순차 실행 — 추후 asyncio로 개선 가능)
    all_trends = []
    all_trends.extend(fetch_google_trends_rss())
    all_trends.extend(fetch_naver_datalab_trends())
    all_trends.extend(fetch_reddit_kr_trends())

    if not all_trends:
        # 폴백: 빈 트렌드일 때 기본 주제 세트 사용
        logger.warning("모든 트렌드 소스 실패 — 폴백 키워드 사용")
        all_trends = [
            {"keyword": "AI 자동화 2025", "source": "fallback"},
            {"keyword": "물류 로봇 최신 트렌드", "source": "fallback"},
            {"keyword": "딥러닝 실무 적용 사례", "source": "fallback"},
        ]

    # EXCLUDE_KEYWORDS 필터링 (Gemini 전달 전 원천 차단)
    filtered_trends = [t for t in all_trends if is_valid_topic(t["keyword"])]
    excluded_count = len(all_trends) - len(filtered_trends)
    if excluded_count:
        logger.info(f"제외 키워드 필터: {excluded_count}개 키워드 제거됨")
    logger.info(f"총 {len(filtered_trends)}개 트렌드 키워드 Gemini 전달")

    selected = select_topics_via_gemini(
        raw_trends=filtered_trends,
        blog_domain=domain,
        top_n=config["trend"]["top_select"],
    )

    # Gemini 결과도 이중 필터링
    selected = [t for t in selected if is_valid_topic(t["keyword"])]

    # 로그 저장
    log_path = os.path.join(
        os.path.dirname(__file__), "..", "output", "logs",
        f"trend_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "raw_count": len(all_trends),
            "selected": selected
        }, f, ensure_ascii=False, indent=2)

    logger.info(f"트렌드 에이전트 완료 → {log_path}")
    return selected


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    topics = run_trend_agent()
    print(json.dumps(topics, ensure_ascii=False, indent=2))
