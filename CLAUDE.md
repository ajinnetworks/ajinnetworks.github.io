# CLAUDE.md — 아진네트웍스 블로그 레포 컨텍스트
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
index.html        ← layout: home 3줄만 유지
CNAME             ← blog.ajinnetworks.co.kr
_layouts/default.html 4번 줄  ← 리다이렉트 주석 유지
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

## 음악 플레이어 정보

### GitHub 레포
```
https://github.com/ajinnetworks/Ajin-Soft-Rock-Ballad
Raw URL: https://raw.githubusercontent.com/ajinnetworks/Ajin-Soft-Rock-Ballad/main/
```

### 현재 트랙 목록
| # | 제목 | 파일명 |
|---|---|---|
| 01 | Yesterday Once More | `Carpenters%20_Yesterday%20Once%20More.mp3` |
| 02 | Time in a Bottle | `Jim%20Croce%27s%20-Time%20in-%20a%20-Bottle.mp3` |
| 03 | 그대 없는 밤 | Suno 업로드 필요 |
| 04 | 빗속의 기억 | Suno 업로드 필요 |
| 05 | 새벽 두 시 | Suno 업로드 필요 |

### YouTube
```
채널: https://www.youtube.com/@AjinSoftRock
Shorts: https://www.youtube.com/@AjinSoftRock/shorts
```

---

## 알려진 이슈 및 해결책

### 1. 블로그 캐시 지연
- 원인: GitHub Pages CDN (Fastly) 10분 캐시 고정
- 해결: `home_current.html`에 Jekyll 빌드 시각 기반 캐시 버스팅 스크립트 적용
- 임시: Ctrl+Shift+R 강제 새로고침

### 2. 리다이렉트 오류 (해결됨)
- 원인: `default.html` JS 리다이렉트 코드
- 해결: 2026-04-11 제거 완료

### 3. MP3 파일명 특수문자
- 파일명에 공백·따옴표 포함 시 URL 인코딩 필요
- 권장: 영문 소문자 + 하이픈만 사용
  ```
  carpenters-yesterday-once-more.mp3
  jim-croce-time-in-a-bottle.mp3
  ```

---

## 작업 이력

### 2026-04-11
- Claude Code 플러그인 설정 (frontend-for-opus-4-5, frontend-design)
- 음악 플레이어 개발 및 GitHub Pages 배포
- Auto Blog Post 워크플로우 복구 (Secrets 등록)
- 블로그 Music 메뉴 추가 (header.html + music.md)
- 포스트 하단 Music 배너 자동 삽입 (post.html 수정)
- 리다이렉트 오류 수정 (default.html JS 코드 제거)
- 캐시 버스팅 스크립트 적용 (home_current.html)

---

## 다음 작업

- [ ] Ajin 오리지널 트랙 3~5번 MP3 Suno 다운로드 → GitHub 업로드
- [ ] 파일명 영문 변환 재업로드 (Carpenters, Jim Croce)
- [ ] `post (1).html` 삭제
- [ ] github MCP 인증 처리
- [ ] Node.js 20→24 Actions 업그레이드 (기한: 2026-09-16)
