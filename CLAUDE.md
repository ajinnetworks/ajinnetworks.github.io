# CLAUDE.md — 아진네트웍스 블로그 + 음악 플레이어 컨텍스트
> 레포: ajinnetworks/ajinnetworks.github.io
> 최종 업데이트: 2026-04-11

---

## WHAT — 이 레포는 무엇인가

Jekyll 기반 기술 블로그 + Ajin Soft Rock Ballad 음악 플레이어 통합 운영

```
blog.ajinnetworks.co.kr          ← 블로그 메인
blog.ajinnetworks.co.kr/music/   ← 음악 플레이어 (임베드)
blog.ajinnetworks.co.kr/Ajin-Soft-Rock-Ballad/  ← PWA 앱
```

---

## WHY — 목적

- 아진네트웍스(주) 공장자동화·딥러닝 비전·스마트팩토리 기술 블로그 자동 발행
- AI 에이전트(Anthropic Claude API)로 화/목/토 주 3회 자동 포스팅
- Ajin Soft Rock Ballad 음악 채널 홍보 및 플레이어 제공

---

## HOW — 구조 및 빌드

### 디렉토리 구조
```
ajinnetworks.github.io/
├── _layouts/
│   ├── default.html   ← 전체 레이아웃 (리다이렉트 코드 없음 — CNAME이 처리)
│   ├── home.html      ← 블로그 홈
│   └── post.html      ← 포스트 (하단 Music 배너 자동 삽입)
├── _includes/
│   ├── head.html      ← 메타/GA4/SEO (946줄)
│   ├── header.html    ← 네비게이션 (Music 메뉴 포함)
│   └── seo-schema.html
├── _posts/            ← 자동 발행 포스트
├── agents/            ← blog_agent 코드
├── scripts/
│   └── run_agent.py   ← 진입점
├── assets/
├── _config.yml        ← Jekyll 설정
├── auto_post.yml      ← GitHub Actions 워크플로우
├── home_current.html  ← 현재 블로그 메인 레이아웃
├── music.md           ← 음악 플레이어 페이지 (/music/)
├── index.html         ← layout: home (3줄만 — 절대 수정 금지)
└── CNAME              ← blog.ajinnetworks.co.kr
```

### 빌드 명령
```bash
bundle exec jekyll build
bundle exec jekyll serve --livereload
```

### 배포
- GitHub Actions `deploy.yml` → push 시 자동 빌드/배포
- `auto_post.yml` → 화/목/토 00:00 UTC (09:00 KST) 자동 포스팅

---

## 절대 수정 금지 파일

```
index.html                      ← layout: home 3줄만 유지
CNAME                           ← blog.ajinnetworks.co.kr
_layouts/default.html 4번 줄    ← 리다이렉트 주석 유지
```

---

## GitHub Actions Secrets 목록

| Secret | 용도 |
|---|---|
| `BLOG_GITHUB_TOKEN` | GitHub 커밋/푸시 (repo + workflow 권한) |
| `ANTHROPIC_API_KEY` | Claude API 포스트 생성 |
| `BLOG_REPO` | `ajinnetworks/ajinnetworks.github.io` |
| `GMAIL_USER` | 이메일 알림 (선택) |
| `GMAIL_APP_PASSWORD` | 이메일 앱 비밀번호 (선택) |

---

## 음악 플레이어 시스템

### 레포 구조
```
Ajin-Soft-Rock-Ballad/          ← 음악 파일 전용 레포
├── *.mp3                       ← 트랙 파일 (영문-하이픈 파일명 규칙)
├── cover-ajin.jpg              ← 공통 앨범 커버 (모든 트랙 공유)
├── titles.json                 ← 트랙 제목 메타데이터
├── index.html                  ← PWA 플레이어
├── manifest.json               ← PWA 설정
└── sw.js                       ← 서비스 워커
```

### GitHub API 자동 로딩 구조
```
플레이어 로드
    ↓
GitHub API 호출 (파일 목록)
    ↓
titles.json 병렬 로드 (제목 매핑)
    ↓
MP3 파일 자동 감지 + 제목 매핑
    ↓
플레이리스트 자동 생성
```

**제외 파일 패턴:** `cover`, `index`, `manifest`, `sw` 로 시작하는 파일

### 현재 트랙 목록

| 파일명 | 표시 제목 |
|---|---|
| `Carpenters-Yesterday-Once-More.mp3` | Yesterday Once More / 어제처럼 또다시 |
| `Jim-Croces-Time-In-A-Bottle.mp3` | Time in a Bottle / 시간을 병에 담아 |
| `The-Light-Left-at-Dawn25.mp3` | The Light Left at Dawn / 새벽빛이 머물던 곳 |
| `Where-Silence-Holds-Your-Name.mp3` | Where Silence Holds Your Name / 침묵이 네 이름을 품는 곳 |
| `good-day.mp3` | Good Day / 좋은 날 |

### titles.json 규칙

```json
{
  "파일명.mp3": {
    "title": "영문만 / 한글만 / English / 한글 혼용 모두 가능",
    "artist": "아티스트명",
    "year": "2025 · 장르",
    "cover": "트랙별 커버 URL (생략 시 cover-ajin.jpg 사용)"
  }
}
```

**제목 표기 방식:**
- 영문만: `"title": "Good Day"`
- 한글만: `"title": "좋은 날"`
- 혼용: `"title": "Good Day / 좋은 날"`

### 새 트랙 추가 방법

```
Step 1. Suno MP3 다운로드
        파일명: 영문-소문자-하이픈.mp3
        예: bit-sok-ui-gieok.mp3

Step 2. Ajin-Soft-Rock-Ballad 레포 업로드
        → 파일 추가하기 → 업로드 → Commit

Step 3. titles.json에 항목 추가
        {
          "bit-sok-ui-gieok.mp3": {
            "title": "Memories in the Rain / 빗속의 기억",
            "artist": "Ajin Soft Rock Ballad",
            "year": "2025 · Korean Ballad"
          }
        }

Step 4. titles.json Commit
        → 플레이어 새로고침 → 자동 반영 ✅
```

### ADD TRACK 탭 사용법

```
플레이어 → ADD TRACK 탭
→ 트랙 선택 (자동으로 로드된 트랙 목록 표시)
→ GitHub Raw MP3 URL 입력 → SET (URL 교체)
→ 앨범 커버 이미지 URL 입력 → SET (커버 교체)
```

### YouTube
```
채널: https://www.youtube.com/@AjinSoftRock
Shorts: https://www.youtube.com/@AjinSoftRock/shorts
```

---

## 알려진 이슈 및 해결책

### 1. 블로그 캐시 지연
- 원인: GitHub Pages CDN (Fastly) 10분 캐시 고정
- 해결: `home_current.html` 캐시 버스팅 스크립트 적용
- 임시: Ctrl+Shift+R 강제 새로고침

### 2. 리다이렉트 오류 (해결됨 2026-04-11)
- 원인: `_layouts/default.html` 4번 줄 JS 리다이렉트 코드
- 증상: `ajinnetworks.github.io` → `www.ajinnetworks.co.kr` 으로 이동
- 해결: JS 코드 제거, CNAME이 처리하도록 변경

### 3. MP3 파일명 규칙
- 파일명: 영문 소문자 + 하이픈만 사용 (공백·따옴표 금지)
- 이유: URL 인코딩 문제 방지
- 올바른 예: `good-day.mp3`, `carpenters-yesterday-once-more.mp3`

### 4. 앨범 커버 이미지
- Google Drive 공유 링크 → CORS 차단으로 표시 불가
- 해결: GitHub Raw URL 사용
  ```
  https://raw.githubusercontent.com/ajinnetworks/Ajin-Soft-Rock-Ballad/main/cover-ajin.jpg
  ```

### 5. GitHub API Rate Limit
- 비인증 요청: 시간당 60회 제한
- 현재: 공개 레포이므로 일반 사용에 문제 없음
- titles.json: `?t=Date.now()` 캐시 버스팅 적용

---

## 작업 이력

### 2026-04-11 (오전)
- Claude Code 플러그인 설정 (frontend-for-opus-4-5, frontend-design)
- 음악 플레이어 개발 (레트로 카세트 + VU미터 디자인)
- GitHub Pages 배포 + PWA 설정
- Auto Blog Post 워크플로우 복구 (Secrets 등록)
- 블로그 Music 메뉴 추가 (header.html + music.md)
- 포스트 하단 Music 배너 자동 삽입 (post.html)
- 리다이렉트 오류 수정 (default.html JS 제거)
- 캐시 버스팅 스크립트 적용 (home_current.html)

### 2026-04-11 (오후)
- GitHub API 자동 트랙 로딩 구현
  - 레포에 MP3 업로드 → 플레이어 자동 반영
  - `f.download_url` 사용 (인코딩 문제 해결)
  - 제외 패턴: cover, index, manifest, sw
- titles.json 시스템 구축
  - 영문 / 한글 / 혼용 제목 자유 설정
  - titles.json 없어도 파일명 자동 변환 폴백
  - 트랙별 커버 이미지 URL 설정 가능
- ADD TRACK 탭 복원
  - 트랙 선택 드롭다운 자동 생성 (buildTrackSelect)
  - MP3 URL 수동 등록 (addAudio)
  - 커버 이미지 URL 수동 등록 (addCover)
- music.md + index.html(PWA) 동일 적용
- 앨범 커버 이미지 GitHub Raw URL 하드코딩

---

## 다음 작업

- [ ] Suno 오리지널 트랙 추가 (빗속의 기억, 새벽 두 시)
- [ ] `post (1).html` 삭제
- [ ] github MCP 인증 처리
- [ ] Node.js 20→24 Actions 업그레이드 (기한: 2026-09-16)
