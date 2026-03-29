from pathlib import Path

p = Path(r"E:\아진네트웍스\Claude Code\ajinnetworks.github.io\_layouts\post.html")
text = p.read_text(encoding="utf-8")
p.with_suffix(".html.bak6").write_text(text, encoding="utf-8")

changed = 0

# 1. post-hero CSS에서 배경 이미지 제거 (인라인으로 이동)
old_bg = """  background:
      linear-gradient(rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.75) 100%),
      var(--hero-image, var(--hero-bg)) center/cover no-repeat;"""
new_bg = """  background: var(--hero-bg);"""

if old_bg in text:
    text = text.replace(old_bg, new_bg, 1)
    changed += 1
    print("✅ CSS 배경 단순화")

# 2. --hero-image 변수 제거
old_var = "\n    --hero-image: url('{{ hero_image_url }}');"
if old_var in text:
    text = text.replace(old_var, "", 1)
    changed += 1
    print("✅ --hero-image 변수 제거")

# 3. header 태그에 인라인 style 추가
old_header = '<header class="post-hero">'
new_header = '<header class="post-hero" style="background: linear-gradient(rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.78) 100%), url(\'{{ hero_image_url }}\') center/cover no-repeat, {{ hero_bg }};">'

if old_header in text:
    text = text.replace(old_header, new_header, 1)
    changed += 1
    print("✅ 인라인 style 배경 이미지 적용")

# 4. 제목 텍스트 강제 흰색 인라인 추가
old_h1 = '<h1 class="hero-title">{{ page.title }}</h1>'
new_h1 = '<h1 class="hero-title" style="color:#ffffff !important; text-shadow: 0 2px 20px rgba(0,0,0,0.8);">{{ page.title }}</h1>'

if old_h1 in text:
    text = text.replace(old_h1, new_h1, 1)
    changed += 1
    print("✅ 제목 흰색 강제 적용")

# 5. 배지 텍스트 강제 표시
old_badge = '<div class="hero-badge">{{ hero_icon }} {{ cat }}</div>'
new_badge = '<div class="hero-badge" style="color: var(--hero-accent); border-color: var(--hero-accent); background: rgba(0,0,0,0.4);">{{ hero_icon }} {{ cat }}</div>'

if old_badge in text:
    text = text.replace(old_badge, new_badge, 1)
    changed += 1
    print("✅ 배지 스타일 강화")

p.write_text(text, encoding="utf-8")
print(f"\n완료: {changed}개 수정")
