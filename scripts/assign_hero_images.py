"""글 대표 일러스트(hero-v2) 일괄 배정·재배정.

기본은 미리보기(dry-run)이며 --write를 줘야 파일을 고친다.
- 대상: image가 없거나 /assets/img/hero-v2/ 일러스트인 글
- 제외: og_image가 있는 글, 머리말에 `image_lock: true`가 있는 글(수동 지정 고정)
- 규칙: agents/github_publisher.pick_hero_image (새 글 발행과 동일)

사용: python scripts/assign_hero_images.py [--write] [--posts _posts]
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agents.github_publisher import HERO_DIR, pick_hero_image  # noqa: E402

LOCK_RE = re.compile(r"^image_lock:\s*(true|yes|on)\s*$", re.M | re.I)
IMAGE_RE = re.compile(r"^image:\s*(\S+)\s*$", re.M)


def _field(fm: str, name: str) -> str:
    m = re.search(rf"^{name}:\s*(.*)$", fm, re.M)
    return m.group(1).strip().strip("'\"") if m else ""


def _keywords(fm: str) -> list[str]:
    """keywords: 한 줄 값 또는 아래 '- 항목' 목록 (발행 에이전트가 넘기는 것과 같은 입력)."""
    m = re.search(r"^keywords:[ \t]*(\S.*)?\n((?:[ \t]*-[ \t]*.+\n?)*)", fm, re.M)
    if not m:
        return []
    items = [m.group(1).strip()] if m.group(1) else []
    items += [x.strip().strip("'\"") for x in re.findall(r"^[ \t]*-[ \t]*(.+)$", m.group(2), re.M)]
    return [x for x in items if x]


def _first_category(fm: str) -> str:
    m = re.search(r"^categories?:\s*\[([^\]]*)\]", fm, re.M)
    if m:
        return m.group(1).split(",")[0].strip().strip("'\"")
    m = re.search(r"^categories?:\s*\n\s*-\s*(.+)$", fm, re.M) or re.search(r"^categories?:\s*(\S.*)$", fm, re.M)
    return m.group(1).strip().strip("'\"") if m else ""


def plan(text: str) -> tuple[str | None, str | None]:
    """(현재 image, 새 image) — 대상이 아니면 (None, None)."""
    if not text.startswith("---"):
        return None, None
    fm = text.split("---", 2)[1]
    if LOCK_RE.search(fm) or re.search(r"^og_image:", fm, re.M):
        return None, None
    m = IMAGE_RE.search(fm)
    current = m.group(1) if m else ""
    if current and not current.startswith(HERO_DIR + "/"):
        return None, None
    return current, pick_hero_image(_field(fm, "title"), _first_category(fm), _keywords(fm))


def apply(text: str, new: str) -> str:
    _, fm, body = text.split("---", 2)
    if IMAGE_RE.search(fm):
        fm = IMAGE_RE.sub(f"image: {new}", fm, count=1)
    else:
        title = _field(fm, "title").replace('"', "'")
        cat = _first_category(fm) or "자동화"
        fm = fm.rstrip("\n") + f'\nimage: {new}\nimage_alt: "{title} — {cat} 공정 일러스트"\nimage_strategy: process-hero-v3-bulk\n'
    return "---" + fm + "---" + body


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--posts", default=str(ROOT / "_posts"))
    args = ap.parse_args(argv)
    after, changed, locked = collections.Counter(), 0, 0
    for f in sorted(Path(args.posts).glob("*.md")):
        text = f.read_text(encoding="utf-8")
        if LOCK_RE.search(text.split("---", 2)[1] if text.startswith("---") else ""):
            locked += 1
        current, new = plan(text)
        if new is None:
            continue
        after[new.rsplit("/", 1)[1]] += 1
        if new != current:
            changed += 1
            if args.write:
                f.write_text(apply(text, new), encoding="utf-8")
    print(f"targets={sum(after.values())} changed={changed} locked={locked} write={args.write}")
    print("distribution:", after.most_common())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
