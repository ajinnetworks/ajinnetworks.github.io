---
layout: default
title: Music
permalink: /music/
---

<div class="music-page">
  <div class="music-header">
    <h1>🎵 Music</h1>
    <p>아진네트웍스의 음악 채널을 만나보세요</p>
  </div>

  <!-- YouTube 채널 섹션 -->
  <section class="youtube-section">
    <h2>▶ YOUTUBE CHANNEL</h2>
    
    <!-- Ajin Soft Rock Ballad 채널 안내 -->
    <div class="channel-card">
      <h3>🎸 Ajin Soft Rock Ballad</h3>
      <p class="channel-desc">80s-2000s Korean Soft Rock & Ballad</p>
      
      <!-- 채널 배너 이미지 -->
      <div class="channel-banner">
        <a href="https://www.youtube.com/@AjinSoftRock" target="_blank" rel="noopener noreferrer">
          <img src="https://yt3.googleusercontent.com/ytc/AIdro_placeholder" 
               alt="Ajin Soft Rock Ballad Channel"
               onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22800%22 height=%22200%22><rect width=%22800%22 height=%22200%22 fill=%22%23ff0000%22/><text x=%2250%25%22 y=%2250%25%22 font-size=%2248%22 fill=%22white%22 text-anchor=%22middle%22 dominant-baseline=%22middle%22>🎵 Ajin Soft Rock Ballad</text></svg>'"
               loading="lazy">
        </a>
      </div>
      
      <div class="channel-info">
        <p>🎼 장르: 80s-2000s 한국 소프트 록 & 발라드</p>
        <p>🎤 스타일: 남성 보컬, 감성적 멜로디</p>
        <p>📅 업로드: 매주 새로운 곡 업데이트</p>
      </div>
      
      <div class="channel-actions">
        <a href="https://www.youtube.com/@AjinSoftRock" class="btn btn-youtube" target="_blank" rel="noopener noreferrer">
          📺 채널 방문하기
        </a>
        <a href="https://www.youtube.com/@AjinSoftRock?sub_confirmation=1" class="btn btn-subscribe" target="_blank" rel="noopener noreferrer">
          🔔 구독하기
        </a>
      </div>
    </div>

    <!-- 최신 영상 플레이리스트 (업로드 후 활성화) -->
    <div class="channel-card" id="latest-videos" style="display:none;">
      <h3>🎬 최신 업로드</h3>
      <p class="channel-desc">가장 최근에 업로드된 곡들</p>
      
      <div class="video-grid">
        <!-- JavaScript로 동적 로드 -->
      </div>
    </div>

    <!-- Shorts 채널 -->
    <div class="channel-card">
      <h3>🎞️ Shorts</h3>
      <p class="channel-desc">60초 단위 음악 클립</p>
      
      <div class="shorts-preview">
        <a href="https://www.youtube.com/@AjinSoftRock/shorts" target="_blank" rel="noopener noreferrer">
          <div class="shorts-placeholder">
            <span class="shorts-icon">📱</span>
            <p>YouTube Shorts로 이동</p>
          </div>
        </a>
      </div>
      
      <div class="channel-link">
        <a href="https://www.youtube.com/@AjinSoftRock/shorts" target="_blank" rel="noopener noreferrer">
          📱 Shorts 보기 →
        </a>
      </div>
    </div>
  </section>

  <!-- Spotify 섹션 -->
  <section class="spotify-section">
    <h2>🎧 STEREO</h2>
    <p class="section-desc">Spotify에서도 만나보세요</p>
    
    <div class="spotify-placeholder">
      <div class="spotify-icon">🎧</div>
      <h3>곧 만나요!</h3>
      <p>Ajin Soft Rock Ballad이 곧 Spotify에서도 만나볼 수 있습니다.</p>
      <a href="https://artists.spotify.com" target="_blank" rel="noopener noreferrer" class="btn btn-spotify">
        Spotify for Artists 알아보기
      </a>
    </div>
  </section>

  <!-- SNS & 외부 링크 -->
  <section class="links-section">
    <h2>🔗 Links</h2>
    
    <div class="links-grid">
      <a href="https://www.youtube.com/@AjinSoftRock" class="link-card youtube" target="_blank" rel="noopener noreferrer">
        <span class="link-icon">📺</span>
        <span class="link-text">YouTube Channel</span>
      </a>
      
      <a href="https://www.youtube.com/@AjinSoftRock/shorts" class="link-card shorts" target="_blank" rel="noopener noreferrer">
        <span class="link-icon">📱</span>
        <span class="link-text">YouTube Shorts</span>
      </a>
      
      <a href="https://www.ajinnetworks.co.kr" class="link-card website" target="_blank" rel="noopener noreferrer">
        <span class="link-icon">🌐</span>
        <span class="link-text">Official Website</span>
      </a>
    </div>
  </section>
</div>

<style>
/* 기본 레이아웃 */
.music-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.music-header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
}

.music-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: white !important;
  font-weight: 700;
}

.music-header p {
  font-size: 1.1rem;
  opacity: 0.9;
  color: white !important;
}

/* 섹션 공통 */
.youtube-section,
.spotify-section,
.links-section {
  margin-bottom: 3rem;
}

.youtube-section h2,
.spotify-section h2,
.links-section h2 {
  font-size: 1.6rem;
  margin-bottom: 1rem;
  padding-left: 0.5rem;
  color: #111 !important;
  font-weight: 700;
}

.youtube-section h2 {
  border-left: 4px solid #ff0000;
}

.spotify-section h2 {
  border-left: 4px solid #1db954;
}

.links-section h2 {
  border-left: 4px solid #667eea;
}

.section-desc {
  color: #666 !important;
  margin-bottom: 2rem;
  padding-left: 0.5rem;
  font-size: 1rem;
}

/* 채널 카드 */
.channel-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.channel-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

.channel-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #111 !important;
  font-weight: 700;
}

.channel-desc {
  color: #666 !important;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

/* 채널 배너 */
.channel-banner {
  width: 100%;
  margin-bottom: 1.5rem;
  border-radius: 8px;
  overflow: hidden;
  background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%);
}

.channel-banner img {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.3s ease;
}

.channel-banner:hover img {
  transform: scale(1.05);
}

/* 채널 정보 */
.channel-info {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.channel-info p {
  color: #333 !important;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.channel-info p:last-child {
  margin-bottom: 0;
}

/* 버튼 스타일 */
.channel-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.3s ease;
  text-align: center;
  flex: 1;
  min-width: 150px;
}

.btn-youtube {
  background: #ff0000;
  color: white !important;
  box-shadow: 0 2px 4px rgba(255, 0, 0, 0.2);
}

.btn-youtube:hover {
  background: #cc0000;
  box-shadow: 0 4px 8px rgba(255, 0, 0, 0.3);
  transform: translateY(-2px);
}

.btn-subscribe {
  background: #111;
  color: white !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.btn-subscribe:hover {
  background: #000;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}

.btn-spotify {
  background: #1db954;
  color: white !important;
  box-shadow: 0 2px 4px rgba(29, 185, 84, 0.2);
}

.btn-spotify:hover {
  background: #1aa34a;
  box-shadow: 0 4px 8px rgba(29, 185, 84, 0.3);
  transform: translateY(-2px);
}

/* Shorts 플레이스홀더 */
.shorts-preview {
  margin-bottom: 1.5rem;
}

.shorts-placeholder {
  background: linear-gradient(135deg, #000 0%, #333 100%);
  border-radius: 8px;
  padding: 3rem 2rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.shorts-placeholder:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.shorts-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.shorts-placeholder p {
  color: white !important;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
}

/* Spotify 플레이스홀더 */
.spotify-placeholder {
  background: linear-gradient(135deg, #1db954 0%, #1aa34a 100%);
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  color: white;
}

.spotify-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.spotify-placeholder h3 {
  color: white !important;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.spotify-placeholder p {
  color: rgba(255, 255, 255, 0.9) !important;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

/* 링크 그리드 */
.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.link-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: white;
  border-radius: 10px;
  text-decoration: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.link-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

.link-icon {
  font-size: 2rem;
}

.link-text {
  color: #333 !important;
  font-weight: 600;
  font-size: 1rem;
}

.link-card.youtube {
  border-left: 4px solid #ff0000;
}

.link-card.shorts {
  border-left: 4px solid #000;
}

.link-card.website {
  border-left: 4px solid #667eea;
}

.channel-link {
  text-align: center;
  margin-top: 1rem;
}

.channel-link a {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: #000;
  color: white !important;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.channel-link a:hover {
  background: #333;
  transform: translateY(-2px);
}

/* 모바일 최적화 (768px 이하) */
@media (max-width: 768px) {
  .music-page {
    padding: 1rem 0.75rem;
  }
  
  .music-header {
    padding: 1.5rem 1rem;
    margin-bottom: 2rem;
    border-radius: 12px;
  }
  
  .music-header h1 {
    font-size: 1.8rem;
  }
  
  .music-header p {
    font-size: 0.95rem;
  }
  
  .youtube-section h2,
  .spotify-section h2,
  .links-section h2 {
    font-size: 1.3rem;
    margin-bottom: 0.75rem;
  }
  
  .section-desc {
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }
  
  .channel-card {
    padding: 1.5rem 1rem;
    margin-bottom: 1.5rem;
    border-radius: 10px;
  }
  
  .channel-card h3 {
    font-size: 1.2rem;
  }
  
  .channel-desc {
    font-size: 0.85rem;
    margin-bottom: 1rem;
  }
  
  .channel-info {
    padding: 1rem;
  }
  
  .channel-info p {
    font-size: 0.85rem;
  }
  
  .channel-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    min-width: auto;
  }
  
  .shorts-placeholder {
    padding: 2rem 1rem;
  }
  
  .shorts-icon {
    font-size: 2.5rem;
  }
  
  .spotify-placeholder {
    padding: 2rem 1rem;
  }
  
  .spotify-icon {
    font-size: 3rem;
  }
  
  .spotify-placeholder h3 {
    font-size: 1.4rem;
  }
  
  .spotify-placeholder p {
    font-size: 0.95rem;
  }
  
  .links-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .link-card {
    padding: 1rem;
  }
  
  .link-icon {
    font-size: 1.5rem;
  }
  
  .link-text {
    font-size: 0.9rem;
  }
}

/* 작은 모바일 (480px 이하) */
@media (max-width: 480px) {
  .music-header h1 {
    font-size: 1.5rem;
  }
  
  .music-header p {
    font-size: 0.85rem;
  }
  
  .youtube-section h2,
  .spotify-section h2,
  .links-section h2 {
    font-size: 1.1rem;
  }
  
  .channel-card {
    padding: 1rem 0.75rem;
  }
  
  .channel-card h3 {
    font-size: 1.1rem;
  }
  
  .btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}

/* 다크모드 대응 */
@media (prefers-color-scheme: dark) {
  .channel-card,
  .link-card {
    background: #1e1e1e;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  }
  
  .channel-card h3,
  .link-text {
    color: #ffffff !important;
  }
  
  .channel-desc {
    color: #aaaaaa !important;
  }
  
  .channel-info {
    background: #2a2a2a;
  }
  
  .channel-info p {
    color: #cccccc !important;
  }
}
</style>

<script>
// YouTube Data API로 최신 동영상 로드 (옵션)
// API 키가 있을 경우 활성화
/*
const CHANNEL_ID = 'UC_YOUR_CHANNEL_ID';
const API_KEY = 'YOUR_API_KEY';

async function loadLatestVideos() {
  try {
    const response = await fetch(
      `https://www.googleapis.com/youtube/v3/search?key=${API_KEY}&channelId=${CHANNEL_ID}&part=snippet,id&order=date&maxResults=3`
    );
    const data = await response.json();
    
    if (data.items && data.items.length > 0) {
      document.getElementById('latest-videos').style.display = 'block';
      // 비디오 그리드 렌더링 로직
    }
  } catch (error) {
    console.log('Videos will be available soon');
  }
}

loadLatestVideos();
*/
</script>