---
layout: default
title: "기술 태그"
description: "아진네트웍스 기술 블로그의 자동화·로봇·비전·PLC·스마트팩토리 관련 태그별 게시물을 찾습니다."
permalink: /tag/
---

<style>
.tag-hub{max-width:900px;margin:56px auto;padding:0 24px}.tag-search{display:flex;gap:8px;margin:20px 0}.tag-search input{flex:1;padding:12px 14px;border:1px solid #d9e0e7;border-radius:8px}.tag-grid{display:grid;gap:12px}.tag-card{padding:16px;border:1px solid #e2e7ee;border-radius:10px;background:#fff}.tag-card a{font-weight:700;text-decoration:none}.tag-meta{font-size:.85rem;color:#68707a;margin-top:5px}.tag-chip{display:inline-block;background:#f1f4f8;border-radius:999px;padding:4px 9px;margin:3px;font-size:.76rem}
</style>

<div class="tag-hub">
  <h1>기술 태그 검색</h1>
  <p>기존 태그 링크도 이 페이지로 자동 복구됩니다. 검색어를 입력하면 해당 태그가 포함된 게시물만 표시됩니다.</p>
  <div class="tag-search"><input id="tagQuery" type="search" placeholder="예: AGV, 머신비전, PLC, 스마트팩토리"></div>
  <div id="tagStatus"></div>
  <div id="tagResults" class="tag-grid"></div>
</div>

<script>
(function(){
 const posts=[{% for post in site.posts %}{title:{{ post.title | jsonify }},url:{{ post.url | relative_url | jsonify }},date:{{ post.date | date: "%Y-%m-%d" | jsonify }},tags:{{ post.tags | jsonify }}},{% endfor %}];
 const params=new URLSearchParams(location.search); const input=document.getElementById('tagQuery');
 input.value=params.get('q')||'';
 function norm(s){return (s||'').toLowerCase().replace(/[^0-9a-z가-힣]+/g,' ').trim()}
 function render(){const q=norm(input.value); const rows=posts.filter(p=>!q||norm((p.tags||[]).join(' ')+' '+p.title).includes(q));
 document.getElementById('tagStatus').textContent=q?'검색 결과 '+rows.length+'개':'전체 게시물 '+rows.length+'개';
 document.getElementById('tagResults').innerHTML=rows.slice(0,120).map(p=>'<div class="tag-card"><a href="'+p.url+'">'+p.title+'</a><div class="tag-meta">'+p.date+'</div><div>'+((p.tags||[]).slice(0,8).map(t=>'<span class="tag-chip">#'+t+'</span>').join(''))+'</div></div>').join('')||'<p>일치하는 게시물이 없습니다.</p>';}
 input.addEventListener('input',render); render();
})();
</script>
