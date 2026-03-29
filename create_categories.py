pages_dir = r"E:\아진네트웍스\Claude Code\ajinnetworks.github.io\category"
import os
os.makedirs(pages_dir, exist_ok=True)

cats = {
    "물류자동화": "Logistics Automation",
    "공장자동화": "Factory Automation", 
    "딥러닝비전": "Deep Learning Vision",
    "스마트팩토리": "Smart Factory",
    "제어SW": "Control Software",
}

for cat_ko, cat_en in cats.items():
    content = f"""---
layout: category
title: {cat_ko}
category: {cat_ko}
permalink: /category/{cat_ko}/
---
"""
    path = os.path.join(pages_dir, f"{cat_ko}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {cat_ko}.md 생성")

print("완료: 카테고리 페이지 5개")
