---
layout: default
title: 카테고리
permalink: /category/
description: "아진네트웍스 기술 블로그 — 공장자동화, 딥러닝 비전, 스마트팩토리 카테고리별 포스트"
---

<div class="cat-index-hero">
  <h1>📁 카테고리</h1>
  <p>관심 분야를 선택해 최신 기술 인사이트를 확인하세요</p>
</div>

<div class="cat-index-grid">

  {% assign all_cats = site.posts | map: "categories" | join: "," | split: "," | uniq | sort %}
  {% for cat in all_cats %}
    {% assign cat_clean = cat | strip %}
    {% if cat_clean != "" %}
      {% assign cat_count = 0 %}
      {% for post in site.posts %}
        {% if post.categories contains cat_clean %}
          {% assign cat_count = cat_count | plus: 1 %}
        {% endif %}
      {% endfor %}

      {% if cat_clean == "스마트팩토리" %}{% assign cat_icon = "⚡" %}
      {% elsif cat_clean == "공장자동화" %}{% assign cat_icon = "🏭" %}
      {% elsif cat_clean == "물류자동화" %}{% assign cat_icon = "📦" %}
      {% elsif cat_clean == "딥러닝비전" %}{% assign cat_icon = "🤖" %}
      {% elsif cat_clean == "제어SW" %}{% assign cat_icon = "💻" %}
      {% elsif cat_clean == "AI" %}{% assign cat_icon = "🧠" %}
      {% elsif cat_clean == "자동화" %}{% assign cat_icon = "⚙️" %}
      {% else %}{% assign cat_icon = "📄" %}
      {% endif %}

      <a class="cat-index-card" href="{{ '/category/' | append: cat_clean | append: '/' | relative_url }}">
        <span class="cat-index-icon">{{ cat_icon }}</span>
        <div class="cat-index-name">{{ cat_clean }}</div>
        <div class="cat-index-count">포스트 <strong>{{ cat_count }}</strong>개</div>
      </a>
    {% endif %}
  {% endfor %}

</div>
