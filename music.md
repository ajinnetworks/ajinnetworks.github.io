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
    
    <!-- Ajin Soft Rock Ballad 플레이리스트 -->
    <div class="channel-card">
      <h3>🎸 Ajin Soft Rock Ballad</h3>
      <p class="channel-desc">80s-2000s Korean Soft Rock & Ballad</p>
      
      <div class="video-container">
        <iframe 
          src="https://www.youtube.com/embed/videoseries?list=PLYOURPLAYLISTIDhere" 
          title="Ajin Soft Rock Ballad Playlist" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          allowfullscreen
          loading="lazy">
        </iframe>
      </div>
      
      <div class="channel-link">
        <a href="https://www.youtube.com/@AjinSoftRockBallad" target="_blank" rel="noopener noreferrer">
          채널 바로가기 →
        </a>
      </div>
    </div>

    <!-- Shorts 채널 -->
    <div class="channel-card">
      <h3>🎬 Shorts 채널</h3>
      <p class="channel-desc">60초 단위 음악 클립</p>
      
      <div class="video-container shorts-container">
        <iframe 
          src="https://www.youtube.com/embed/videoseries?list=PLYOURSHORTSPLAYLISTIDhere" 
          title="Shorts Playlist" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
          allowfullscreen
          loading="lazy">
        </iframe>
      </div>
      
      <div class="channel-link">
        <a href="https://www.youtube.com/@YourShortsChannel" target="_blank" rel="noopener noreferrer">
          Shorts 보기 →
        </a>
      </div>
    </div>
  </section>

  <!-- Spotify 임베드 (선택사항) -->
  <section class="spotify-section" style="margin-top: 3rem;">
    <h2>🎧 STEREO</h2>
    <div class="spotify-container">
      <iframe 
        style="border-radius:12px" 
        src="https://open.spotify.com/embed/playlist/YOUR_SPOTIFY_PLAYLIST_ID?utm_source=generator" 
        width="100%" 
        height="380" 
        frameBorder="0" 
        allowfullscreen="" 
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
        loading="lazy">
      </iframe>
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
}

.music-header p {
  font-size: 1.1rem;
  opacity: 0.9;
  color: white !important;
}

/* YouTube 섹션 */
.youtube-section h2 {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  padding-left: 0.5rem;
  border-left: 4px solid #ff0000;
  color: #111 !important;
}

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
}

.channel-desc {
  color: #666 !important;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

/* 반응형 비디오 컨테이너 */
.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
  height: 0;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 1rem;
  background: #000;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

/* Shorts는 9:16 비율 */
.shorts-container {
  padding-bottom: 177.78%; /* 9:16 비율 */
  max-width: 400px;
  margin: 0 auto 1rem;
}

/* 채널 링크 */
.channel-link {
  text-align: center;
  margin-top: 1rem;
}

.channel-link a {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: #ff0000;
  color: white !important;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
  transition: background 0.3s ease;
}

.channel-link a:hover {
  background: #cc0000;
}

/* Spotify 섹션 */
.spotify-section h2 {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  padding-left: 0.5rem;
  border-left: 4px solid #1db954;
  color: #111 !important;
}

.spotify-container {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 모바일 최적화 */
@media (max-width: 768px) {
  .music-page {
    padding: 1rem 0.75rem;
  }
  
  .music-header {
    padding: 1.5rem 1rem;
    margin-bottom: 2rem;
  }
  
  .music-header h1 {
    font-size: 1.8rem;
  }
  
  .music-header p {
    font-size: 0.95rem;
  }
  
  .youtube-section h2,
  .spotify-section h2 {
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
  }
  
  .channel-card {
    padding: 1.5rem 1rem;
    margin-bottom: 1.5rem;
  }
  
  .channel-card h3 {
    font-size: 1.2rem;
  }
  
  .channel-desc {
    font-size: 0.85rem;
  }
  
  /* 모바일에서 Shorts 비율 조정 */
  .shorts-container {
    padding-bottom: 177.78%; /* 9:16 유지 */
    max-width: 100%;
  }
  
  .channel-link a {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }
}

/* 다크모드 대응 */
@media (prefers-color-scheme: dark) {
  .channel-card {
    background: #1e1e1e;
  }
  
  .channel-card h3 {
    color: #ffffff !important;
  }
  
  .channel-desc {
    color: #aaaaaa !important;
  }
}
</style>