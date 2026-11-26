"""
github_publisher.py — GitHub Pages 자동 커밋 발행 에이전트
Goal: 검수 완료 포스트를 Jekyll 마크다운으로 변환 후
      GitHub API를 통해 레포지토리에 자동 커밋 → GitHub Actions 빌드 트리거

의존성: PyGithub, python-frontmatter
설치: pip install PyGithub python-frontmatter
"""

import io
import json
import logging
import os
import re
import sys
import zlib

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding='utf-8', errors='replace'
    )

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import frontmatter                  # python-frontmatter
from github import Auth, Github, GithubException, InputGitTreeElement   # PyGithub

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

logger = logging.getLogger(__name__)

KST = ZoneInfo("Asia/Seoul")


# ─── 설정 로드 ────────────────────────────────────────────────────────────────

from dotenv import load_dotenv
load_dotenv(override=False)

def get_github_config() -> dict:
    """환경변수에서 GitHub 설정 읽기."""
    token = (os.getenv("BLOG_GITHUB_TOKEN") or "").strip()
    token = token or (os.getenv("GITHUB_TOKEN") or "").strip()
    if not token:
        raise EnvironmentError("GitHub 토큰 없음: BLOG_GITHUB_TOKEN 또는 GITHUB_TOKEN 필요")
    repo_name = os.environ.get("BLOG_REPO") or os.environ.get("GITHUB_REPO")
    branch = os.environ.get("GITHUB_BRANCH", "main")
    posts_path = os.environ.get("GITHUB_POSTS_PATH", "_posts")

    if not repo_name:
        raise EnvironmentError(
            "필수 환경변수 미설정: BLOG_REPO\n"
            "config/.env.sample 참고 후 .env에 추가하세요."
        )

    return {
        "token": token,
        "repo_name": repo_name,
        "branch": branch,
        "posts_path": posts_path,
    }


# ─── 마크다운 변환 ────────────────────────────────────────────────────────────

# ── 대표 이미지 ──────────────────────────────────────────────
# 작성 모델이 본문에 넣던 Unsplash 사진은 프롬프트에 고정된 5장이 반복돼 277편에 같은 사진이 쓰였다.
# 본문 외부 이미지는 제거하고, 대표 이미지는 저장소의 공정별 일러스트(assets/img/hero-v2)로 지정한다.
HERO_DIR = "/assets/img/hero-v2"
HERO_KEYWORDS = [  # (제목·키워드에 포함되면, 일러스트) — 위에서부터 우선
    (("택트", "사이클타임", "라인 밸런싱", "병목"), "smart-oee"),
    (("팔레타이징", "적재"), "palletizing"),
    (("포장", "라벨", "케이스 패커", "테이핑"), "packaging-line"),
    (("소터", "분류기"), "sorter"),
    (("자동창고", "AS/RS", "ASRS", "스태커"), "logistics-asrs"),
    (("반도체", "웨이퍼", "HBM", "OHT", "MLCC"), "semiconductor-fab"),
    (("배터리", "이차전지", "2차전지", "수소전지"), "battery-cell"),
    (("AMR", "AGV", "자율이동", "무인운반"), "logistics-amr"),
    (("용접",), "robot-welding"),
    (("CNC", "가공"), "cnc-machining"),
    (("협동로봇", "코봇", "픽앤플레이스", "PICK"), "cobot-assembly"),
    (("디지털 트윈", "디지털트윈"), "digital-twin"),
    (("FEMS", "에너지", "전력", "탄소"), "energy-fems"),
    (("중대재해", "안전", "웨어러블", "사고"), "safety-monitoring"),
    (("5G", "IOT", "통신", "네트워크"), "iiot-network"),
    (("딥러닝", "CNN", "불량"), "deep-learning-defect"),
    (("그리퍼", "EOAT", "엔드이펙터", "로봇"), "robot-eoat"),
    (("PLC", "HMI", "SCADA", "EtherCAT", "PROFINET", "제어"), "plc-control"),
    (("비전", "AOI", "검사"), "vision-inspection"),
    (("OEE", "MES", "예지보전", "예측 보전", "예측보전", "모니터링"), "smart-oee"),
    (("보조금", "지원 사업", "정부 지원", "세액", "ROI", "주가", "투자", "정책", "원가"), "investment-roi"),
]
CATEGORY_HEROES = {
    "딥러닝비전": ["vision-inspection", "deep-learning-defect"],
    "물류자동화": ["logistics-amr", "logistics-asrs", "sorter"],
    "공장자동화": ["robot-eoat", "palletizing", "packaging-line", "cobot-assembly"],
    "제어SW": ["plc-control", "iiot-network"],
    "스마트팩토리": ["smart-oee", "digital-twin", "iiot-network", "investment-roi", "robot-eoat"],
}
_EXTERNAL_IMAGE = re.compile(r"!\[[^\]]*\]\(https?://[^)\s]+[^)]*\)")


def strip_external_images(content: str) -> str:
    """본문의 외부 URL 마크다운 이미지를 제거하고, 남는 빈 줄을 정리한다."""
    cleaned = _EXTERNAL_IMAGE.sub("", content)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip() + "\n"


def pick_hero_image(title: str, category: str, keywords=None) -> str:
    """제목·키워드에 맞는 공정 일러스트, 없으면 카테고리 일러스트 (같은 제목은 항상 같은 결과)."""
    text = " ".join([title or ""] + [str(k) for k in (keywords or [])]).upper()
    for terms, name in HERO_KEYWORDS:
        if any(t.upper() in text for t in terms):
            return f"{HERO_DIR}/{name}.svg"
    options = CATEGORY_HEROES.get(category) or CATEGORY_HEROES["스마트팩토리"]
    name = options[zlib.crc32((title or "").encode("utf-8")) % len(options)]
    return f"{HERO_DIR}/{name}.svg"


def make_slug(title: str) -> str:
    """
    포스트 제목을 Jekyll URL-safe 슬러그로 변환.
    한글은 romanize 없이 그대로 사용 (GitHub Pages 한글 URL 지원).
    특수문자만 제거.
    """
    # 특수문자 제거, 공백을 하이픈으로
    slug = re.sub(r"[^\w\s가-힣-]", "", title)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = slug[:60]  # 최대 60자
    return slug


def post_to_jekyll_markdown(post: dict) -> tuple[str, str]:
    """
    에이전트 포스트 dict → Jekyll Front Matter + 본문 마크다운 변환.

    Returns:
        (file_name, markdown_content)
        file_name: "YYYY-MM-DD-slug.md"
    """
    now = datetime.now(KST)
    date_str = now.strftime("%Y-%m-%d")
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S +0900")

    title = post.get("title", "제목 없음")
    slug = make_slug(title)
    file_name = f"{date_str}-{slug}.md"

    # content 안전 변환
    raw_content = post.get("content", "")
    if isinstance(raw_content, list):
        safe_content = "\n\n".join(str(c) for c in raw_content)
    elif isinstance(raw_content, dict):
        safe_content = str(raw_content)
    else:
        safe_content = str(raw_content) if raw_content else ""
    safe_content = safe_content.encode("utf-8", errors="ignore").decode("utf-8")
    safe_content = strip_external_images(safe_content)
    categories = _parse_category(post.get("category", "기술"))

    # Front Matter 구성
    meta = frontmatter.Post(
        content=safe_content,
        layout="post",
        title=title,
        date=datetime_str,
        categories=categories,
        tags=post.get("tags", [])[:10],
        description=post.get("meta_description", "")[:160],
        keywords=post.get("seo_keywords", []),
        author="AI Agent",
        # 검수 점수 메타로 기록 (독자에게 비표시)
        review_score=post.get("review_result", {}).get("total_score", 0),
        generated_at=post.get("generated_at", now.isoformat()),
        image=pick_hero_image(title, categories[0] if categories else "", post.get("seo_keywords")),
        image_alt=f"{title} — {categories[0] if categories else '자동화'} 공정 일러스트",
        image_strategy="process-hero-v3",
    )

    # python-frontmatter 로 직렬화
    md_content = frontmatter.dumps(meta)

    # <!--more--> 태그 자동 삽입 (첫 단락 뒤)
    # 본문에 이미 있으면 생략
    if "<!--more-->" not in md_content:
        lines = md_content.split("\n")
        # Front Matter 끝(---) 이후 첫 빈 줄 찾기
        in_front = True
        dash_count = 0
        insert_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "---":
                dash_count += 1
                if dash_count == 2:
                    in_front = False
                continue
            if not in_front and line.strip() == "" and insert_idx is None:
                insert_idx = i + 1  # 빈 줄 다음에 삽입

        if insert_idx and insert_idx < len(lines):
            lines.insert(insert_idx, "\n<!--more-->\n")
            md_content = "\n".join(lines)

    return file_name, md_content


def _parse_category(category_str: str) -> list[str]:
    """'기술/자동화' → ['기술', '자동화'] 변환."""
    if not category_str:
        return ["기술"]
    parts = re.split(r"[/,·]", category_str)
    return [p.strip() for p in parts if p.strip()][:3]


# ─── Human-in-the-loop Gate ──────────────────────────────────────────────────

def human_approval_gate(post: dict) -> bool:
    """HUMAN_GATE=true 시 발행 전 터미널 승인 요구."""
    if os.environ.get("HUMAN_GATE", "true").lower() != "true":
        return True

    print("\n" + "=" * 60)
    print("📋 GitHub Pages 발행 전 승인 요청")
    print("=" * 60)
    print(f"제목   : {post.get('title', 'N/A')}")
    print(f"카테고리: {post.get('category', 'N/A')}")
    print(f"태그   : {post.get('tags', [])}")
    score = post.get("review_result", {}).get("total_score", "N/A")
    print(f"검수점수: {score}/100")
    print(f"초안   : {post.get('draft_path', 'N/A')}")
    print("=" * 60)

    answer = input("GitHub Pages에 발행하시겠습니까? (y/n/skip): ").strip().lower()
    if answer == "y":
        logger.info(f"✅ 승인: '{post.get('title')}'")
        return True
    elif answer == "skip":
        logger.info(f"⏭️  스킵: '{post.get('title')}'")
        return False
    else:
        logger.info(f"❌ 거절: '{post.get('title')}'")
        return False


# ─── 발행 기록 저장 ───────────────────────────────────────────────────────────

def save_publish_record(post: dict, github_result: dict) -> str:
    """발행 완료 기록을 output/published/ 에 JSON으로 저장."""
    published_dir = ROOT / "output" / "published"
    published_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(KST).strftime("%Y%m%d_%H%M%S")
    safe_title = re.sub(r"[^\w가-힣]", "_", post.get("title", "post"))[:30]

    record = {
        "published_at": datetime.now(KST).isoformat(),
        "platform": "github_pages",
        "title": post.get("title"),
        "file_name": github_result.get("file_name"),
        "file_path": github_result.get("file_path"),
        "commit_sha": github_result.get("commit_sha"),
        "commit_url": github_result.get("commit_url"),
        "blog_url": github_result.get("blog_url"),
        "review_score": post.get("review_result", {}).get("total_score"),
        "tags": post.get("tags", []),
        "word_count": post.get("word_count", 0),
    }

    record_path = published_dir / f"{timestamp}_{safe_title}.json"
    record_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info(f"발행 기록 저장: {record_path}")
    return str(record_path)


# ─── 레포지토리 초기화 유틸 ──────────────────────────────────────────────────

def init_github_repo(config: dict, dry_run: bool = False) -> bool:
    """
    GitHub 레포지토리에 Jekyll 기본 파일이 없으면 자동으로 업로드.
    github_pages/ 폴더의 파일들을 레포지토리에 커밋.
    """
    if dry_run:
        print("[dry-run] GitHub 연결 생략 — init_github_repo 스킵")
        return None

    g = Github(auth=Auth.Token(config["token"]))
    repo = g.get_repo(config["repo_name"])
    branch = config["branch"]

    jekyll_dir = ROOT / "github_pages"
    if not jekyll_dir.exists():
        logger.warning("github_pages/ 폴더 없음 — 초기화 스킵")
        return False

    uploaded = []
    skipped = []

    for file_path in jekyll_dir.rglob("*"):
        if file_path.is_dir():
            continue
        # __pycache__ 등 제외
        if any(p in str(file_path) for p in ["__pycache__", ".pytest_cache"]):
            continue

        relative = str(file_path.relative_to(jekyll_dir))
        content = file_path.read_bytes()

        try:
            existing = repo.get_contents(relative, ref=branch)
            # 이미 존재하면 스킵 (강제 덮어쓰기 원하면 update_file 사용)
            skipped.append(relative)
        except GithubException as e:
            if e.status == 404:
                try:
                    repo.create_file(
                        path=relative,
                        message=f"init: add {relative}",
                        content=content,
                        branch=branch,
                    )
                    uploaded.append(relative)
                    logger.info(f"  업로드: {relative}")
                except Exception as upload_err:
                    logger.error(f"  업로드 실패 {relative}: {upload_err}")
            else:
                logger.error(f"  확인 실패 {relative}: {e}")

    logger.info(f"레포 초기화: {len(uploaded)}개 업로드, {len(skipped)}개 스킵")
    return True


# ─── 메인 발행 함수 ───────────────────────────────────────────────────────────

def run_github_publisher(posts: list[dict], dry_run: bool = False) -> list[dict]:
    """
    검수 완료 포스트 리스트를 GitHub Pages에 단일 커밋으로 일괄 발행.

    Args:
        posts:   reviewer_agent에서 반환된 포스트 리스트
        dry_run: True이면 마크다운 변환까지만 수행, GitHub 커밋 차단

    Returns:
        발행 결과 리스트
    """
    logger.info("=== GitHub Pages Publisher 시작 ===" + (" [DRY-RUN]" if dry_run else ""))

    if not posts:
        print("[WARN] 발행할 포스트 없음")
        return []

    # 환경변수 확인
    try:
        config = get_github_config()
    except EnvironmentError as e:
        logger.error(str(e))
        return [{"error": str(e), "platform": "github_pages"}]

    # STEP 1: 필터링 + 마크다운 변환
    ready_files = []

    for post in posts:
        if post.get("error"):
            logger.warning(f"오류 포스트 스킵: {post.get('title')}")
            continue

        if not post.get("review_result", {}).get("pass"):
            score = post.get("review_result", {}).get("total_score", 0)
            logger.warning(f"검수 미합격 스킵: '{post.get('title')}' (점수: {score})")
            continue

        if not human_approval_gate(post):
            logger.info(f"사용자 거절/스킵: '{post.get('title')}'")
            continue

        file_name, md_content = post_to_jekyll_markdown(post)
        file_path = f"{config['posts_path']}/{file_name}"
        logger.info(f"마크다운 변환 완료: {file_name} ({len(md_content)}자)")
        ready_files.append({
            "file_path": file_path,
            "file_name": file_name,
            "content": md_content,
            "post": post,
        })

    if not ready_files:
        print("[WARN] 커밋할 파일 없음")
        return [{"error": "발행 대상 없음", "platform": "github_pages"}]

    # STEP 2: dry-run 차단
    if dry_run:
        results = []
        for f in ready_files:
            logger.info(f"[dry-run] 커밋 차단: {f['file_path']}")
            print(f"[DRY-RUN] {f['post'].get('title', '')}: {f['file_path']}")
            result = {
                "file_path": f["file_path"],
                "file_name": f["file_name"],
                "commit_sha": "dry-run-no-commit",
                "commit_url": "(dry-run)",
                "blog_url": "(dry-run)",
                "action": "dry-run",
            }
            save_publish_record(f["post"], result)
            results.append(result)
        logger.info(f"GitHub Pages Publisher 완료: {len(results)}/{len(posts)}개 (dry-run)")
        return results

    # STEP 3: Git Tree API 일괄 커밋
    today = datetime.now(KST).strftime("%Y-%m-%d")

    auth = Auth.Token(config["token"])
    g = Github(auth=auth)
    repo = g.get_repo(config["repo_name"])

    ref = repo.get_git_ref(f"heads/{config['branch']}")
    parent = repo.get_git_commit(ref.object.sha)
    base_tree = repo.get_git_tree(parent.tree.sha)
    seen_paths = set()
    unique_files = []
    skipped = []
    for item in ready_files:
        path = item["file_path"]
        if path not in seen_paths:
            seen_paths.add(path)
            try:
                repo.get_contents(path, ref=parent.sha)
            except GithubException as error:
                if error.status != 404:
                    raise
                unique_files.append(item)
                continue
        logger.info("기존 또는 배치 내 중복 경로 건너뜀: %s", path)
        skipped.append({"file_path": path, "action": "duplicate_skipped"})
    ready_files = unique_files
    if not ready_files:
        return skipped

    tree_elements = []
    for f in ready_files:
        blob = repo.create_git_blob(f["content"], "utf-8")
        tree_elements.append(InputGitTreeElement(
            path=f["file_path"],
            mode="100644",
            type="blob",
            sha=blob.sha,
        ))

    if not tree_elements:
        print("[WARN] 커밋할 파일 없음")
        return [{"error": "tree_elements 비어있음", "platform": "github_pages"}]

    commit_msg = (
        f"docs: auto-post {len(ready_files)}개 포스트 발행 ({today})\n\n"
        + "\n".join(f"- {f['file_name']}" for f in ready_files)
    )

    try:
        new_tree = repo.create_git_tree(tree_elements, base_tree)
        new_commit = repo.create_git_commit(commit_msg, new_tree, [parent])
        ref.edit(new_commit.sha, force=False)
    except GithubException as e:
        logger.error(f"일괄 커밋 실패: {e.status} {e.data}")
        return [{"error": f"GitHub API {e.status}: {e.data}", "platform": "github_pages"}]
    except Exception as e:
        logger.error(f"일괄 커밋 실패: {e}")
        return [{"error": str(e), "platform": "github_pages"}]

    commit_sha = new_commit.sha
    username = config["repo_name"].split("/")[0]
    blog_url = f"https://{username}.github.io"
    commit_url = f"https://github.com/{config['repo_name']}/commit/{commit_sha}"

    print(f"[SUCCESS] {len(ready_files)}개 포스트 일괄 커밋: {commit_sha[:7]}")
    print(f"   커밋   : {commit_url}")
    print(f"   블로그 : {blog_url}")
    for f in ready_files:
        print(f"   - {f['file_name']}")
    print(f"   ※ GitHub Actions 빌드 후 1~3분 내 반영됩니다.")

    # STEP 4: 결과 구성 + 발행 기록 저장
    results = []
    for f in ready_files:
        result = {
            "file_path": f["file_path"],
            "file_name": f["file_name"],
            "commit_sha": commit_sha,
            "commit_url": commit_url,
            "blog_url": blog_url,
            "action": "일괄 커밋",
        }
        save_publish_record(f["post"], result)
        results.append(result)

    logger.info(f"GitHub Pages Publisher 완료: {len(results)}/{len(posts)}개 발행")
    return results + skipped


if __name__ == "__main__":
    import sys as _sys
    logging.basicConfig(level=logging.INFO)
    dry_run = "--dry-run" in _sys.argv

    print("GitHub Pages Publisher - 환경변수 확인")
    try:
        cfg = get_github_config()
        print(f"  repo     : {cfg['repo_name']}")
        print(f"  branch   : {cfg['branch']}")
        print(f"  dry-run  : {dry_run}")
        print("  [OK] 환경변수 확인 완료")
    except EnvironmentError as e:
        print(f"  [ERROR] {e}")
        _sys.exit(1)

    if dry_run:
        print()
        print("[dry-run] 샘플 포스트 1건으로 publish 경로 테스트")
        sample = [{
            "title": "dry-run 테스트 포스트",
            "content": "# 테스트\n\nDry-run 확인용 포스트입니다.",
            "category": "스마트팩토리",
            "tags": ["테스트"],
            "filename": "2099-01-01-dry-run-test.md",
            "review_result": {"pass": True, "total_score": 100},
        }]
        results = run_github_publisher(sample, dry_run=True)
        for r in results:
            print(f"  status : {r.get('github_status', 'unknown')}")
            print(f"  path   : {r.get('github_path', '-')}")
    else:
        print()
        print("단독 실행 시에는 --dry-run 옵션을 사용하거나 run_agent.py 를 통해 실행하세요.")
