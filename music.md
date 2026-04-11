---
layout: default
title: Music
permalink: /music/
---

<div class="music-container">
  <!-- 간단한 헤더 (배경 없음) -->
  <div class="music-title">
    <h1>🎵 Music</h1>
    <p>아진네트웍스의 음악 채널</p>
  </div>

  <!-- YouTube 채널 -->
  <section class="music-section">
    <h2>▶ YouTube Channel</h2>
    
    <div class="music-card">
      <div class="card-header">
        <span class="icon">🎸</span>
        <h3>Ajin Soft Rock Ballad</h3>
      </div>
      <p class="card-desc">80s-2000s Korean Soft Rock & Ballad</p>
      
      <div class="info-box">
        <p>🎼 장르: 80s-2000s 한국 소프트 록 & 발라드</p>
        <p>🎤 스타일: 남성 보컬, 감성적 멜로디</p>
        <p>📅 업로드: 매주 새로운 곡</p>
      </div>
      
      <div class="button-group">
        <a href="https://www.youtube.com/@AjinSoftRock" target="_blank" rel="noopener" class="btn btn-red">
          📺 채널 방문
        </a>
        <a href="https://www.youtube.com/@AjinSoftRock?sub_confirmation=1" target="_blank" rel="noopener" class="btn btn-black">
          🔔 구독하기
        </a>
      </div>
    </div>

    <div class="music-card">
      <div class="card-header">
        <span class="icon">🎞️</span>
        <h3>Shorts</h3>
      </div>
      <p class="card-desc">60초 음악 클립</p>
      
      <a href="https://www.youtube.com/@AjinSoftRock/shorts" target="_blank" rel="noopener" class="shorts-box">
        <span class="shorts-icon">📱</span>
        <p>YouTube Shorts로 이동</p>
      </a>
    </div>
  </section>

  <!-- Spotify -->
  <section class="music-section">
    <h2>🎧 Streaming</h2>
    
    <div class="spotify-box">
      <span class="spotify-icon">🎧</span>
      <h3>Coming Soon</h3>
      <p>Spotify에서 곧 만나요</p>
      <a href="https://artists.spotify.com" target="_blank" rel="noopener" class="btn btn-green">
        Spotify for Artists
      </a>
    </div>
  </section>

  <!-- Links -->
  <section class="music-section">
    <h2>🔗 Links</h2>
    
    <div class="links">
      <a href="https://www.youtube.com/@AjinSoftRock" target="_blank" rel="noopener" class="link-item">
        <span>📺</span>
        <div>
          <strong>YouTube Channel</strong>
          <small>@AjinSoftRock</small>
        </div>
      </a>
      
      <a href="https://www.youtube.com/@AjinSoftRock/shorts" target="_blank" rel="noopener" class="link-item">
        <span>📱</span>
        <div>
          <strong>YouTube Shorts</strong>
          <small>60초 클립</small>
        </div>
      </a>
      
      <a href="https://www.ajinnetworks.co.kr" target="_blank" rel="noopener" class="link-item">
        <span>🌐</span>
        <div>
          <strong>Official Website</strong>
          <small>아진네트웍스(주)</small>
        </div>
      </a>
    </div>
  </section>
</div>

<style>
/* 전역 초기화 - 모든 배경 이미지 제거 */
.music-container,
.music-container *,
.music-title,
.music-section,
.music-card {
  background-image: none !important;
  background: none !important;
}

/* 컨테이너 */
.music-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* 타이틀 */
.music-title {
  text-align: center;
  padding: 2rem 1rem;
  margin-bottom: 2rem;
  background-color: #667eea !important;
  background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border-radius: 12px;
}

.music-title h1 {
  font-size: 2rem;
  color: white !important;
  margin: 0 0 0.5rem 0;
  font-weight: 700;
}

.music-title p {
  font-size: 1rem;
  color: rgba(255,255,255,0.9) !important;
  margin: 0;
}

/* 섹션 */
.music-section {
  margin-bottom: 3rem;
}

.music-section h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111 !important;
  margin-bottom: 1.5rem;
  padding-left: 0.5rem;
  border-left: 4px solid #ff0000;
}

/* 카드 */
.music-card {
  background-color: white !important;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.icon {
  font-size: 1.5rem;
}

.music-card h3 {
  font-size: 1.4rem;
  color: #111 !important;
  margin: 0;
  font-weight: 700;
}

.card-desc {
  color: #666 !important;
  margin: 0 0 1.5rem 0;
  font-size: 0.9rem;
}

/* 정보 박스 */
.info-box {
  background-color: #f5f5f5 !important;
  padding: 1.25rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.info-box p {
  color: #333 !important;
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.info-box p:last-child {
  margin-bottom: 0;
}

/* 버튼 */
.button-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  flex: 1;
  min-width: 140px;
  padding: 0.75rem 1.25rem;
  text-align: center;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  display: inline-block;
}

.btn-red {
  background-color: #ff0000 !important;
  color: white !important;
}

.btn-red:hover {
  background-color: #cc0000 !important;
  transform: translateY(-2px);
}

.btn-black {
  background-color: #000 !important;
  color: white !important;
}

.btn-black:hover {
  background-color: #333 !important;
  transform: translateY(-2px);
}

.btn-green {
  background-color: #1db954 !important;
  color: white !important;
}

.btn-green:hover {
  background-color: #1aa34a !important;
  transform: translateY(-2px);
}

/* Shorts 박스 */
.shorts-box {
  display: block;
  background-color: #000 !important;
  background-image: linear-gradient(135deg, #000 0%, #333 100%) !important;
  padding: 2.5rem 1.5rem;
  border-radius: 8px;
  text-align: center;
  text-decoration: none;
  margin-bottom: 1.5rem;
  transition: transform 0.3s ease;
}

.shorts-box:hover {
  transform: scale(1.02);
}

.shorts-icon {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 0.75rem;
}

.shorts-box p {
  color: white !important;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

/* Spotify 박스 */
.spotify-box {
  background-color: #1db954 !important;
  background-image: linear-gradient(135deg, #1db954 0%, #1aa34a 100%) !important;
  padding: 3rem 2rem;
  border-radius: 12px;
  text-align: center;
}

.spotify-icon {
  font-size: 3.5rem;
  display: block;
  margin-bottom: 1rem;
}

.spotify-box h3 {
  color: white !important;
  font-size: 1.6rem;
  margin: 0 0 0.5rem 0;
  font-weight: 700;
}

.spotify-box p {
  color: rgba(255,255,255,0.9) !important;
  font-size: 1rem;
  margin: 0 0 1.5rem 0;
}

/* 링크 */
.links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.link-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background-color: white !important;
  border-radius: 10px;
  text-decoration: none;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  border-left: 4px solid #667eea;
  transition: all 0.3s ease;
}

.link-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

.link-item > span {
  font-size: 2rem;
  flex-shrink: 0;
}

.link-item strong {
  display: block;
  color: #111 !important;
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.link-item small {
  display: block;
  color: #666 !important;
  font-size: 0.85rem;
}

/* 모바일 */
@media (max-width: 768px) {
  .music-container {
    padding: 1.5rem 1rem;
  }
  
  .music-title {
    padding: 1.5rem 1rem;
  }
  
  .music-title h1 {
    font-size: 1.6rem;
  }
  
  .music-section h2 {
    font-size: 1.3rem;
  }
  
  .music-card {
    padding: 1.5rem 1rem;
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
  
  .links {
    grid-template-columns: 1fr;
  }
  
  .shorts-box {
    padding: 2rem 1rem;
  }
  
  .shorts-icon {
    font-size: 2rem;
  }
  
  .spotify-box {
    padding: 2rem 1.5rem;
  }
  
  .spotify-icon {
    font-size: 2.5rem;
  }
}
</style>
