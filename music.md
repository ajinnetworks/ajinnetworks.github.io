---
layout: none
---
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Music | 아진네트웍스 (주)</title>
  
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      background-image: none !important;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: white;
      color: #333;
      line-height: 1.6;
    }
    
    .container {
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem 1rem;
    }
    
    .header {
      text-align: center;
      padding: 2rem;
      background: linear-gradient(135deg, #667eea, #764ba2);
      border-radius: 12px;
      margin-bottom: 2rem;
    }
    
    .header h1 {
      color: white;
      font-size: 2rem;
      margin-bottom: 0.5rem;
    }
    
    .header p {
      color: white;
      font-size: 1rem;
    }
    
    .card {
      background: white;
      border: 1px solid #e0e0e0;
      border-radius: 10px;
      padding: 2rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .card h2 {
      color: #111;
      font-size: 1.5rem;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    
    .card p {
      color: #666;
      margin-bottom: 1rem;
    }
    
    .info-box {
      background: #f8f9fa;
      padding: 1.25rem;
      border-radius: 8px;
      margin-bottom: 1.5rem;
    }
    
    .info-box p {
      color: #333;
      margin: 0.5rem 0;
    }
    
    .btn {
      display: inline-block;
      padding: 0.85rem 1.5rem;
      background: #ff0000;
      color: white;
      text-decoration: none;
      border-radius: 8px;
      font-weight: 600;
      margin: 0.5rem;
      transition: all 0.3s;
    }
    
    .btn:hover {
      opacity: 0.9;
      transform: translateY(-2px);
    }
    
    .btn-black {
      background: #000;
    }
    
    .btn-green {
      background: #1db954;
    }
    
    .gradient-box {
      background: linear-gradient(135deg, #1db954, #1aa34a);
      padding: 3rem 2rem;
      border-radius: 10px;
      text-align: center;
      margin-bottom: 1.5rem;
    }
    
    .gradient-box h2 {
      color: white;
      margin-bottom: 0.5rem;
    }
    
    .gradient-box p {
      color: rgba(255,255,255,0.9);
      margin-bottom: 1.5rem;
    }
    
    .nav {
      background: #2c3e50;
      padding: 1rem 0;
      margin-bottom: 2rem;
    }
    
    .nav-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 0 1rem;
      display: flex;
      gap: 2rem;
      align-items: center;
    }
    
    .nav a {
      color: white;
      text-decoration: none;
      font-weight: 500;
    }
    
    .nav a:hover {
      color: #667eea;
    }
    
    @media (max-width: 768px) {
      .header h1 {
        font-size: 1.6rem;
      }
      
      .card {
        padding: 1.5rem 1rem;
      }
      
      .btn {
        display: block;
        width: 100%;
        margin: 0.5rem 0;
      }
    }
  </style>
</head>
<body>
  <nav class="nav">
    <div class="nav-container">
      <a href="/">🏠 홈</a>
      <a href="/category/">📁 카테고리</a>
      <a href="/about/">📖 기술자료</a>
      <a href="/music/">🎵 Music</a>
    </div>
  </nav>

  <div class="container">
    <div class="header">
      <h1>🎵 Music</h1>
      <p>아진네트웍스의 음악 채널</p>
    </div>

    <div class="card">
      <h2><span>🎸</span> Ajin Soft Rock Ballad</h2>
      <p>80s-2000s Korean Soft Rock & Ballad</p>
      
      <div class="info-box">
        <p>🎼 <strong>장르:</strong> 80s-2000s 한국 소프트 록 & 발라드</p>
        <p>🎤 <strong>스타일:</strong> 남성 보컬, 감성적 멜로디</p>
        <p>📅 <strong>업로드:</strong> 매주 새로운 곡</p>
      </div>
      
      <a href="https://www.youtube.com/@AjinSoftRock" target="_blank" rel="noopener" class="btn">📺 채널 방문</a>
      <a href="https://www.youtube.com/@AjinSoftRock?sub_confirmation=1" target="_blank" rel="noopener" class="btn btn-black">🔔 구독하기</a>
    </div>

    <div class="card">
      <h2><span>🎞️</span> YouTube Shorts</h2>
      <p>60초 음악 클립</p>
      <a href="https://www.youtube.com/@AjinSoftRock/shorts" target="_blank" rel="noopener" class="btn btn-black">📱 Shorts 보기</a>
    </div>

    <div class="gradient-box">
      <span style="font-size:3.5rem;display:block;margin-bottom:1rem">🎧</span>
      <h2>Coming Soon</h2>
      <p>Spotify에서 곧 만나요</p>
      <a href="https://artists.spotify.com" target="_blank" rel="noopener" class="btn" style="background:white;color:#1db954">Spotify for Artists</a>
    </div>

    <div class="card">
      <h2><span>🔗</span> Links</h2>
      <p>📺 <a href="https://www.youtube.com/@AjinSoftRock" target="_blank" style="color:#667eea">YouTube Channel</a></p>
      <p>📱 <a href="https://www.youtube.com/@AjinSoftRock/shorts" target="_blank" style="color:#667eea">YouTube Shorts</a></p>
      <p>🌐 <a href="https://www.ajinnetworks.co.kr" target="_blank" style="color:#667eea">Official Website</a></p>
    </div>
  </div>

  <footer style="background:#2c3e50;color:white;padding:2rem 1rem;margin-top:3rem;text-align:center">
    <p style="color:white">&copy; 2026 아진네트웍스 주식회사. All rights reserved.</p>
  </footer>
</body>
</html>
