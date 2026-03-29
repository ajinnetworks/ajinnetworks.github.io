from pathlib import Path

p = Path(r"E:\아진네트웍스\Claude Code\ajinnetworks.github.io\_layouts\post.html")
text = p.read_text(encoding="utf-8")
p.with_suffix(".html.bak5").write_text(text, encoding="utf-8")

# endcase 바로 뒤에 hero_image URL 생성 코드 삽입
old = "{% endcase %}"
new = """{% endcase %}
{% if hero_pattern == 'default' %}
  {% assign hero_image_url = "/assets/img/og-default.png" %}
{% else %}
  {% assign hero_image_url = "/assets/img/hero/" | append: hero_pattern | append: ".jpg" %}
{% endif %}"""

# :root에 --hero-image 변수 추가
old_root = "--hero-accent: {{ hero_accent }};"
new_root = """--hero-accent: {{ hero_accent }};
    --hero-image: url('{{ hero_image_url }}');"""

changed = 0

if old in text and "hero_image_url" not in text:
    text = text.replace(old, new, 1)
    changed += 1
    print("✅ hero_image_url 변수 추가")
else:
    print("⚠️  endcase 패턴 없거나 이미 존재")

if old_root in text and "hero_image_url" not in text.split(old_root)[1][:100]:
    text = text.replace(old_root, new_root, 1)
    changed += 1
    print("✅ --hero-image CSS 변수 연결")
elif "--hero-image" in text:
    # 기존 --hero-image를 hero_image_url로 업데이트
    import re
    old_img = re.search(r"--hero-image:[^;]+;", text)
    if old_img:
        text = text.replace(old_img.group(), "--hero-image: url('{{ hero_image_url }}');", 1)
        changed += 1
        print("✅ --hero-image URL 업데이트")

p.write_text(text, encoding="utf-8")
print(f"\n완료: {changed}개 수정")

# 결과 확인
lines = text.split("\n")
print("\n=== endcase 주변 확인 ===")
for i, line in enumerate(lines):
    if "endcase" in line or "hero_image" in line:
        print(f"  {i+1}: {line.strip()}")
