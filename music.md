---
layout: default
title: Music
permalink: /music/
---

<style>
/* 긴급 배경 제거 - 최우선 순위 */
* {
  background-image: none !important;
}

body, main, .page-content, .wrapper {
  background: white !important;
}
</style>

<div class="music-page-clean">
  <div class="music-header-clean">
    <h1>🎵 Music</h1>
    <p>아진네트웍스의 음악 채널</p>
  </div>

  <section class="youtube-section-clean">
    <h2>▶ YouTube Channel</h2>
    
    <div class="channel-card-clean">
      <div class="card-header-clean">
        <span>🎸</span>
        <h3>Ajin Soft Rock Ballad</h3>
      </div>
      <p class="desc">80s-2000s Korean Soft Rock & Ballad</p>
      
      <div class="info">
        <p>🎼 장르: 80s-2000s 한국 소프트 록 & 발라드</p>
        <p>🎤 스타일: 남성 보컬, 감성적 멜로디</p>
        <p>📅 업로드: 매주 새로운 곡</p>
      </div>
      
      <div class="buttons">
        <a href="https://www.youtube.com/@AjinSoftRock" target="_blank">📺 채널 방문</a>
        <a href="https://www.youtube.com/@AjinSoftRock?sub_confirmation=1" target="_blank">🔔 구독</a>
      </div>
    </div>

    <div class="channel-card-clean">
      <div class="card-header-clean">
        <span>🎞️</span>
        <h3>Shorts</h3>
      </div>
      <p class="desc">60초 음악 클립</p>
      
      <a href="https://www.youtube.com/@AjinSoftRock/shorts" target="_blank" class="shorts-link">
        <span>📱</span>
        <p>YouTube Shorts로 이동</p>
      </a>
    </div>
  </section>

  <section class="spotify-section-clean">
    <h2>🎧 Streaming</h2>
    
    <div class="spotify">
      <span>🎧</span>
      <h3>Coming Soon</h3>
      <p>Spotify에서 곧 만나요</p>
      <a href="https://artists.spotify.com" target="_blank">Spotify for Artists</a>
    </div>
  </section>

  <section class="links-section-clean">
    <h2>🔗 Links</h2>
    
    <div class="links">
      <a href="https://www.youtube.com/@AjinSoftRock" target="_blank">
        <span>📺</span>
        <div>
          <strong>YouTube Channel</strong>
          <small>@AjinSoftRock</small>
        </div>
      </a>
      
      <a href="https://www.youtube.com/@AjinSoftRock/shorts" target="_blank">
        <span>📱</span>
        <div>
          <strong>YouTube Shorts</strong>
          <small>60초 클립</small>
        </div>
      </a>
      
      <a href="https://www.ajinnetworks.co.kr" target="_blank">
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
.music-page-clean {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
  background: white;
}

.music-header-clean {
  text-align: center;
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 12px;
  margin-bottom: 2rem;
}

.music-header-clean h1 {
  font-size: 2rem;
  color: white;
  margin: 0 0 0.5rem;
}

.music-header-clean p {
  font-size: 1rem;
  color: rgba(255,255,255,0.9);
  margin: 0;
}

.youtube-section-clean,
.spotify-section-clean,
.links-section-clean {
  margin-bottom: 3rem;
}

.youtube-section-clean h2,
.spotify-section-clean h2,
.links-section-clean h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 1.5rem;
  padding-left: 0.5rem;
  border-left: 4px solid #ff0000;
}

.channel-card-clean {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-header-clean {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.card-header-clean span {
  font-size: 1.5rem;
}

.channel-card-clean h3 {
  font-size: 1.4rem;
  color: #111;
  margin: 0;
}

.channel-card-clean .desc {
  color: #666;
  margin: 0 0 1.5rem;
  font-size: 0.9rem;
}

.channel-card-clean .info {
  background: #f5f5f5;
  padding: 1.25rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.channel-card-clean .info p {
  color: #333;
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.channel-card-clean .buttons {
  display: flex;
  gap: 1rem;
}

.channel-card-clean .buttons a {
  flex: 1;
  padding: 0.75rem;
  text-align: center;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  background: #ff0000;
  color: white;
}

.channel-card-clean .buttons a:last-child {
  background: #000;
}

.channel-card-clean .buttons a:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.shorts-link {
  display: block;
  background: linear-gradient(135deg, #000, #333);
  padding: 2.5rem 1.5rem;
  border-radius: 8px;
  text-align: center;
  text-decoration: none;
  margin-bottom: 1.5rem;
}

.shorts-link span {
  font-size: 2.5rem;
  display: block;
  margin-bottom: 0.75rem;
}

.shorts-link p {
  color: white;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.spotify {
  background: linear-gradient(135deg, #1db954, #1aa34a);
  padding: 3rem 2rem;
  border-radius: 12px;
  text-align: center;
}

.spotify span {
  font-size: 3.5rem;
  display: block;
  margin-bottom: 1rem;
}

.spotify h3 {
  color: white;
  font-size: 1.6rem;
  margin: 0 0 0.5rem;
}

.spotify p {
  color: rgba(255,255,255,0.9);
  font-size: 1rem;
  margin: 0 0 1.5rem;
}

.spotify a {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: white;
  color: #1db954;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
}

.links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.links a {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: white;
  border-radius: 10px;
  text-decoration: none;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  border-left: 4px solid #667eea;
}

.links a:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

.links a > span {
  font-size: 2rem;
}

.links strong {
  display: block;
  color: #111;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.links small {
  display: block;
  color: #666;
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  .music-page-clean {
    padding: 1.5rem 1rem;
  }
  
  .music-header-clean {
    padding: 1.5rem 1rem;
  }
  
  .music-header-clean h1 {
    font-size: 1.6rem;
  }
  
  .channel-card-clean {
    padding: 1.5rem 1rem;
  }
  
  .channel-card-clean .buttons {
    flex-direction: column;
  }
  
  .links {
    grid-template-columns: 1fr;
  }
  
  .shorts-link {
    padding: 2rem 1rem;
  }
  
  .spotify {
    padding: 2rem 1.5rem;
  }
}
</style>
