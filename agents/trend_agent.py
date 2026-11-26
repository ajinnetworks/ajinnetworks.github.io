"""
trend_agent.py — 트렌드 크롤링 & 주제 선정 에이전트
Goal: 실시간 트렌드에서 블로그 포스팅 키워드 3개 선정
"""

import json
import logging
import os
import random
import re
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from agents.gemini_client import get_gemini_response
import requests
import yaml

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


from agents.writer_agent import is_valid_topic, EXCLUDE_KEYWORDS, CATEGORY_KEYWORDS

logger = logging.getLogger(__name__)

POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"

# 블로그 도메인(공장·물류 자동화, 로봇, 머신비전, 제어) 판별용 용어.
# 카테고리별 키워드(writer_agent.CATEGORY_KEYWORDS)에 일반 용어를 더한다.
GENERIC_DOMAIN_TERMS = [
    "자동화", "로봇", "로보틱스", "스마트팩토리", "스마트공장", "스마트 팩토리",
    "머신비전", "비전검사", "비전 검사", "딥러닝", "PLC", "HMI", "SCADA", "MES",
    "공정", "생산라인", "제조", "공장", "설비", "센서", "서보", "모션제어",
    "물류센터", "물류", "AGV", "AMR", "협동로봇", "코봇", "검사장비", "불량",
    "반도체", "배터리", "디지털트윈", "디지털 트윈", "OEE", "예지보전",
    "산업용", "FA", "자동창고", "컨베이어", "팔레타이징",
]
DOMAIN_TERMS = sorted(
    {t for t in GENERIC_DOMAIN_TERMS} | {k for kws in CATEGORY_KEYWORDS.values() for k in kws},
    key=len, reverse=True,
)


def _norm(text: str) -> str:
    return re.sub(r"\s+", "", text or "").lower()


def is_domain_relevant(keyword: str) -> bool:
    """키워드에 블로그 도메인 용어가 하나 이상 포함되면 True (공백·대소문자 무시)."""
    k = _norm(keyword)
    return any(_norm(term) in k for term in DOMAIN_TERMS)


def load_recent_titles(limit: int = 60) -> list[str]:
    """최근 발행 포스트 제목(front matter title) 목록. 실패 시 빈 목록."""
    titles = []
    try:
        for path in sorted(POSTS_DIR.glob("*.md"), reverse=True)[:limit]:
            lines = path.read_text(encoding="utf-8").splitlines()
            # front matter(--- ... ---) 안에서만 찾는다. 키가 알파벳순이라 title이 뒤쪽에 있음.
            end = lines.index("---", 1) if lines[:1] == ["---"] and "---" in lines[1:] else 0
            for line in lines[1:end]:
                if line.startswith("title:"):
                    titles.append(line[6:].strip().strip("'\""))
                    break
    except OSError as e:
        logger.warning(f"최근 포스트 제목 로드 실패 (무시): {e}")
    return titles


def _recently_used(keyword: str, recent_titles: list[str]) -> bool:
    k = _norm(keyword)
    return any(k and k in _norm(t) for t in recent_titles)


def _last_used_rank(keyword: str, recent_titles: list[str]) -> int:
    """recent_titles(최신순)에서 처음 등장한 위치. 클수록 오래전에 쓴 주제."""
    k = _norm(keyword)
    return next((i for i, t in enumerate(recent_titles) if k and k in _norm(t)), len(recent_titles))


def build_candidates(
    raw_trends: list[dict],
    evergreen: list[str],
    top_n: int,
    recent_titles: list[str],
    today: Optional[date] = None,
) -> list[dict]:
    """
    주제 후보 생성: 도메인 관련 트렌드만 남기고, 부족하면 상시 주제(evergreen)로 채운다.
    최근 발행 제목과 겹치는 후보는 제외. 상시 주제는 날짜 기준으로 순서를 섞어 매회 달라지게 한다.
    """
    seen = set()
    candidates = []
    for t in raw_trends:
        kw = t["keyword"].strip()
        if not kw or _norm(kw) in seen:
            continue
        if not is_valid_topic(kw) or not is_domain_relevant(kw):
            continue
        if _recently_used(kw, recent_titles):
            continue
        seen.add(_norm(kw))
        candidates.append({"keyword": kw, "source": t.get("source", "trend")})

    want = max(top_n * 2, top_n + 3)
    if len(candidates) < want:
        fresh = [e for e in evergreen if _norm(e) not in seen and not _recently_used(e, recent_titles)]
        random.Random((today or date.today()).toordinal()).shuffle(fresh)
        # 상시 주제가 모두 최근에 쓰였으면 가장 오래전에 쓴 것부터 재사용 (발행이 멈추지 않게)
        reused = sorted(
            (e for e in evergreen if _norm(e) not in seen and _recently_used(e, recent_titles)),
            key=lambda e: _last_used_rank(e, recent_titles), reverse=True,
        )
        for kw, source in [(k, "evergreen") for k in fresh] + [(k, "evergreen_reuse") for k in reused]:
            if len(candidates) >= want:
                break
            if _norm(kw) in seen:
                continue
            seen.add(_norm(kw))
            candidates.append({"keyword": kw, "source": source})
        if any(c["source"] == "evergreen_reuse" for c in candidates):
            logger.warning("상시 주제가 부족해 오래전에 쓴 주제를 재사용합니다: config trend.evergreen_topics 보강 권장")
    return candidates


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
당신은 산업 자동화 B2B 기술 블로그의 주제 선정 전문가입니다.

블로그 도메인: {blog_domain} — 공장자동화, 물류자동화, 로봇, 머신비전/딥러닝 검사, PLC·제어 SW, 스마트팩토리.
독자: 제조·물류 현장의 설비 엔지니어, 생산기술·구매 담당자 (설비 도입을 검토하는 사람).

후보 목록 (이 목록 밖의 주제는 선택 금지):
{trends_text}

규칙:
- 반드시 위 후보 목록의 키워드를 글자 그대로 "keyword"에 쓰세요.
- 소비재·식품·금융·연예·정치·지역 뉴스처럼 설비 도입과 무관한 주제는 고르지 마세요.
- 설비 사양, 공정 문제 해결, 도입 비용·ROI처럼 실무 검토에 쓰이는 각도를 우선하세요.

위 규칙에 맞는 주제를 {top_n}개 선정하세요.

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
    allowed = {_norm(t["keyword"]): t["keyword"] for t in raw_trends}
    selected = []
    for topic in result.get("selected_topics", []):
        key = _norm(topic.get("keyword", ""))
        if key in allowed and key not in {_norm(s["keyword"]) for s in selected}:
            topic["keyword"] = allowed[key]
            selected.append(topic)
        else:
            logger.warning(f"후보 밖 주제 제거: {topic.get('keyword')!r}")
    # 모델이 규칙을 어겨 부족하면 후보 순서대로 채운다 (도메인 보장)
    for t in raw_trends:
        if len(selected) >= top_n:
            break
        if _norm(t["keyword"]) not in {_norm(s["keyword"]) for s in selected}:
            selected.append({
                "keyword": t["keyword"],
                "angle": "현장 도입 검토 관점의 기술 해설",
                "reason": "도메인 후보 보충",
                "estimated_search_volume": "medium",
            })
    logger.info(f"주제 {len(selected[:top_n])}개 선정 완료 (후보 {len(raw_trends)}개)")
    return selected[:top_n]


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

    # 도메인 필터 + 상시 주제 보충 (Gemini 전달 전 원천 차단)
    top_n = config["trend"]["top_select"]
    candidates = build_candidates(
        raw_trends=all_trends,
        evergreen=config["trend"].get("evergreen_topics", []),
        top_n=top_n,
        recent_titles=load_recent_titles(),
    )
    from_trends = sum(1 for c in candidates if not c["source"].startswith("evergreen"))
    logger.info(
        f"트렌드 {len(all_trends)}개 중 도메인 관련 {from_trends}개 + 상시 주제 "
        f"{len(candidates) - from_trends}개 → 후보 {len(candidates)}개 Gemini 전달"
    )
    if not candidates:
        raise RuntimeError("도메인 주제 후보 없음: config trend.evergreen_topics를 확인하세요")

    selected = select_topics_via_gemini(
        raw_trends=candidates,
        blog_domain=domain,
        top_n=top_n,
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
