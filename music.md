---
layout: page
title: 🎵 Music
permalink: /music/
---

<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

<style>
.music-wrap{width:100%;max-width:400px;margin:0 auto;font-family:'Space Mono',monospace}
.cov{position:relative;width:100%;height:200px;background:#111115;overflow:hidden;border-radius:12px;margin-bottom:0}
.cov-img{width:100%;height:100%;object-fit:cover;position:absolute;inset:0;display:none;border-radius:12px}
.cov-ph{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px}
.vinyl{width:86px;height:86px;border-radius:50%;background:repeating-conic-gradient(#1a1a1e 0deg 10deg,#222228 10deg 20deg);display:flex;align-items:center;justify-content:center}
.vinyl.sp{animation:vs 2.5s linear infinite}
@keyframes vs{to{transform:rotate(360deg)}}
.vc{width:24px;height:24px;border-radius:50%;background:#e8a030;display:flex;align-items:center;justify-content:center}
.vd{width:6px;height:6px;border-radius:50%;background:#0a0a0c}
.cov-ov{position:absolute;inset:0;background:linear-gradient(to bottom,transparent 50%,#0d0d0f 100%);border-radius:12px}
.cbadge{position:absolute;top:10px;left:12px;font-size:8px;color:#e8a030;border:1px solid #e8a030;border-radius:3px;padding:2px 6px;letter-spacing:2px;background:rgba(10,10,12,0.85)}
.cnum{position:absolute;top:10px;right:12px;font-size:9px;color:#888;letter-spacing:1px}
.player-body{background:#0d0d0f;border-radius:0 0 12px 12px;padding:0;border:1px solid #222228;border-top:none}
.inf{padding:12px 18px 6px}
.tt{font-family:'Bebas Neue',cursive;font-size:22px;color:#f0ece0;letter-spacing:1px;line-height:1.1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ta{font-size:9px;color:#e8a030;letter-spacing:2px;margin-top:2px}
.ty{font-size:8px;color:#555;letter-spacing:1px;margin-top:1px}
.vu-row{display:flex;gap:3px;padding:8px 18px 5px;align-items:flex-end;height:34px}
.vb{flex:1;border-radius:2px;background:#1a1a1e;min-height:3px;transition:height 0.08s,background 0.08s}
.ps{padding:0 18px 8px}
.pt-row{display:flex;justify-content:space-between;font-size:9px;color:#555;margin-bottom:5px;letter-spacing:1px}
.prog-bar{width:100%;height:3px;background:#222228;border-radius:2px;cursor:pointer;position:relative}
.prog-fill{height:100%;background:#e8a030;border-radius:2px;width:0%}
.prog-thumb{position:absolute;width:11px;height:11px;border-radius:50%;background:#f0ece0;top:50%;transform:translate(-50%,-50%);left:0%;pointer-events:none}
.ctrl{display:flex;align-items:center;justify-content:center;gap:14px;padding:4px 18px 8px}
.xb{background:none;border:none;cursor:pointer;color:#555;padding:6px;display:flex;align-items:center;transition:color 0.15s}
.xb:hover{color:#e8a030}
.play-btn{width:50px;height:50px;border-radius:50%;background:#e8a030;color:#0a0a0c;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform 0.1s,background 0.15s}
.play-btn:hover{background:#f0b848}
.play-btn:active{transform:scale(0.92)}
.vol-row{display:flex;align-items:center;gap:8px;padding:0 18px 8px}
.vol-lbl{font-size:9px;color:#555;letter-spacing:2px;min-width:22px}
.vol-track{flex:1;height:3px;background:#222228;border-radius:2px;cursor:pointer;position:relative}
.vol-fill{height:100%;background:#555;border-radius:2px;width:80%}
.vol-thumb{position:absolute;width:10px;height:10px;border-radius:50%;background:#f0ece0;top:50%;transform:translate(-50%,-50%);left:80%}
.vol-val{font-size:9px;color:#555;min-width:22px;text-align:right}
.status-bar{font-size:8px;padding:0 18px 6px;letter-spacing:1px;min-height:13px;color:#555}
.status-bar.ok{color:#2ecc71}.status-bar.er{color:#e74c3c}.status-bar.ld{color:#e8a030}
.live-dot{display:inline-block;width:5px;height:5px;border-radius:50%;background:#e8a030;margin-right:4px;animation:pu 1s ease-in-out infinite alternate;vertical-align:middle}
@keyframes pu{from{opacity:0.3}to{opacity:1}}
.tabs{display:flex;border-top:1px solid #1a1a1e}
.tab-btn{flex:1;padding:9px 0;font-size:9px;color:#555;letter-spacing:2px;text-align:center;cursor:pointer;border:none;background:none;font-family:'Space Mono',monospace;transition:color 0.15s}
.tab-btn.ac{color:#e8a030;border-bottom:2px solid #e8a030;background:#0a0a0c}
.panel{min-height:160px;background:#0a0a0c}
.pl-item{display:flex;align-items:center;gap:10px;padding:9px 18px;cursor:pointer;border-bottom:1px solid #111115;transition:background 0.1s}
.pl-item:hover{background:#111115}
.pl-item.ac{background:#131318}
.pl-num{font-size:9px;color:#2a2a2e;min-width:14px;flex-shrink:0}
.pl-body{flex:1;overflow:hidden}
.pl-title{font-size:11px;color:#666;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:color 0.15s}
.pl-artist{font-size:8px;color:#2a2a2e;margin-top:1px;letter-spacing:1px}
.pl-dur{font-size:9px;color:#2a2a2e;flex-shrink:0}
.pl-item.ac .pl-num{color:#e8a030}
.pl-item.ac .pl-title{color:#f0ece0}
.pl-item.has-url .pl-dur{color:#2ecc71}
.add-panel{padding:14px 18px;display:flex;flex-direction:column;gap:8px;background:#0a0a0c}
.add-lbl{font-size:8px;color:#555;letter-spacing:2px;margin-bottom:3px}
.add-row{display:flex;gap:5px}
.add-inp{flex:1;background:#141416;border:1px solid #2a2a2e;border-radius:6px;color:#888;font-family:'Space Mono',monospace;font-size:9px;padding:7px 10px;outline:none;min-width:0;transition:border-color 0.15s}
.add-inp:focus{border-color:#e8a030;color:#f0ece0}
.add-inp::placeholder{color:#252528}
.add-btn{background:#1e1e22;border:none;border-radius:6px;color:#888;font-family:'Space Mono',monospace;font-size:9px;padding:7px 10px;cursor:pointer;font-weight:700;white-space:nowrap;transition:background 0.15s,color 0.15s}
.add-btn:hover{background:#e8a030;color:#0a0a0c}
.eq{display:inline-flex;gap:1px;align-items:flex-end;height:9px}
.eq span{width:2px;background:#e8a030;border-radius:1px;animation:eq 0.5s ease-in-out infinite alternate}
.eq span:nth-child(2){animation-delay:.15s}.eq span:nth-child(3){animation-delay:.3s}
@keyframes eq{from{height:2px}to{height:9px}}
</style>

<div class="music-wrap">
  <div class="cov" id="covSec">
    <div class="cov-ph" id="covPh">
      <div class="vinyl" id="vinyl"><div class="vc"><div class="vd"></div></div></div>
    </div>
    <img class="cov-img" id="covImg" alt="album cover">
    <div class="cov-ov"></div>
    <span class="cbadge">STEREO</span>
    <span class="cnum" id="covNum">01 / 05</span>
  </div>

  <div class="player-body">
    <div class="inf">
      <div class="tt" id="tTitle">Yesterday Once More</div>
      <div class="ta" id="tArtist">THE CARPENTERS</div>
      <div class="ty" id="tYear">1973 · Soft Rock</div>
    </div>
    <div class="vu-row" id="vuRow"></div>
    <div class="ps">
      <div class="pt-row"><span id="curT">0:00</span><span id="totT">--:--</span></div>
      <div class="prog-bar" id="progBar">
        <div class="prog-fill" id="progFill"></div>
        <div class="prog-thumb" id="progThumb"></div>
      </div>
    </div>
    <div class="ctrl">
      <button class="xb" onclick="prevT()"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6 6h2v12H6zm3.5 6 8.5 6V6z"/></svg></button>
      <button class="xb" onclick="seek(-10)"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M11 18V6l-8.5 6 8.5 6zm.5-6 8.5 6V6l-8.5 6z"/></svg></button>
      <button class="play-btn" id="playBtn" onclick="togglePlay()">
        <svg id="playIcon" width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
      </button>
      <button class="xb" onclick="seek(10)"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M4 18l8.5-6L4 6v12zm9-12v12l8.5-6L13 6z"/></svg></button>
      <button class="xb" onclick="nextT()"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg></button>
    </div>
    <div class="vol-row">
      <span class="vol-lbl">VOL</span>
      <div class="vol-track" id="volTrack" onclick="setVol(event)">
        <div class="vol-fill" id="volFill"></div>
        <div class="vol-thumb" id="volThumb"></div>
      </div>
      <span class="vol-val" id="volVal">80</span>
    </div>
    <div class="status-bar" id="statusBar"><span class="live-dot"></span>Ajin Soft Rock Ballad Player</div>
    <div class="tabs">
      <button class="tab-btn ac" onclick="showTab('pl',this)">PLAYLIST</button>
      <button class="tab-btn" onclick="showTab('add',this)">ADD TRACK</button>
    </div>
    <div class="panel" id="panelPl"><div id="playlist"></div></div>
    <div class="panel" id="panelAdd" style="display:none">
      <div class="add-panel">
        <div>
          <div class="add-lbl">트랙 선택</div>
          <select class="add-inp" id="trackSel" style="width:100%;cursor:pointer">
            <option value="2">03 — 그대 없는 밤</option>
            <option value="3">04 — 빗속의 기억</option>
            <option value="4">05 — 새벽 두 시</option>
          </select>
        </div>
        <div>
          <div class="add-lbl">GitHub Raw MP3 URL</div>
          <div class="add-row">
            <input class="add-inp" id="audioUrl" placeholder="https://raw.githubusercontent.com/...mp3">
            <button class="add-btn" onclick="addAudio()">SET</button>
          </div>
        </div>
        <div>
          <div class="add-lbl">앨범 커버 URL</div>
          <div class="add-row">
            <input class="add-inp" id="coverUrl" placeholder="https://...jpg">
            <button class="add-btn" onclick="addCover()">SET</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<audio id="aud" preload="none" crossorigin="anonymous"></audio>

<script>
const RAW='https://raw.githubusercontent.com/ajinnetworks/Ajin-Soft-Rock-Ballad/main/';
const tracks=[
  {title:'Yesterday Once More',artist:'The Carpenters',year:'1973 · Soft Rock',dur:'--:--',secs:0,url:RAW+'Carpenters%20_Yesterday%20Once%20More.mp3',cover:''},
  {title:'Time in a Bottle',artist:'Jim Croce',year:'1973 · Folk Rock',dur:'--:--',secs:0,url:RAW+"Jim%20Croce%27s%20-Time%20in-%20a%20-Bottle.mp3",cover:''},
  {title:'그대 없는 밤',artist:'Ajin Soft Rock Ballad',year:'2025 · Korean Ballad',dur:'4:02',secs:242,url:'',cover:''},
  {title:'빗속의 기억',artist:'Ajin Soft Rock Ballad',year:'2025 · Korean Ballad',dur:'3:48',secs:228,url:'',cover:''},
  {title:'새벽 두 시',artist:'Ajin Soft Rock Ballad',year:'2025 · Korean Ballad',dur:'4:30',secs:270,url:'',cover:''},
];
let ci=0,playing=false,curSec=0,vuInt=null;
const aud=document.getElementById('aud');
const vuR=document.getElementById('vuRow');
for(let i=0;i<24;i++){const d=document.createElement('div');d.className='vb';d.style.height='3px';vuR.appendChild(d);}
const vbs=[...vuR.children];
function vuC(p){return p<0.55?'#2ecc71':p<0.8?'#e8a030':'#e74c3c';}
function animVU(){if(!playing){vbs.forEach(b=>{b.style.height='3px';b.style.background='#1a1a1e';});return;}const base=Math.random()*0.5+0.35;vbs.forEach((b,i)=>{const w=Math.sin(i/24*Math.PI)*0.6+0.4;const h=Math.max(3,Math.round((base*w+Math.random()*0.2)*26));b.style.height=h+'px';b.style.background=vuC(h/26);});}
function fmt(s){if(!s||s<=0)return '--:--';return Math.floor(s/60)+':'+String(Math.floor(s%60)).padStart(2,'0');}
function setSt(msg,type=''){const el=document.getElementById('statusBar');el.innerHTML=type?'· '+msg:'<span class="live-dot"></span>'+msg;el.className='status-bar'+(type?' '+type:'');}
function showTab(n,btn){document.getElementById('panelPl').style.display=n==='pl'?'block':'none';document.getElementById('panelAdd').style.display=n==='add'?'block':'none';document.querySelectorAll('.tab-btn').forEach(t=>t.classList.remove('ac'));btn.classList.add('ac');}
function updateUI(){const t=tracks[ci];document.getElementById('tTitle').textContent=t.title;document.getElementById('tArtist').textContent=t.artist;document.getElementById('tYear').textContent=t.year;document.getElementById('covNum').textContent=String(ci+1).padStart(2,'0')+' / '+String(tracks.length).padStart(2,'0');document.getElementById('vinyl').className='vinyl'+(playing?' sp':'');if(t.cover){document.getElementById('covImg').src=t.cover;document.getElementById('covImg').style.display='block';document.getElementById('covPh').style.display='none';}else{document.getElementById('covImg').style.display='none';document.getElementById('covPh').style.display='flex';}renderPL();}
function renderPL(){document.getElementById('playlist').innerHTML=tracks.map((t,i)=>`<div class="pl-item${i===ci?' ac':''}${t.url?' has-url':''}" onclick="selT(${i})"><span class="pl-num">${i===ci&&playing?'<span class="eq"><span></span><span></span><span></span></span>':String(i+1).padStart(2,'0')}</span><div class="pl-body"><div class="pl-title">${t.title}</div><div class="pl-artist">${t.artist}</div></div><span class="pl-dur">${t.url?'▶':'ADD'}</span></div>`).join('');}
function updateProg(){const t=tracks[ci];const pct=t.secs>0?Math.min(100,curSec/t.secs*100):0;const p=pct.toFixed(1)+'%';document.getElementById('progFill').style.width=p;document.getElementById('progThumb').style.left=p;document.getElementById('curT').textContent=fmt(curSec);}
aud.addEventListener('timeupdate',()=>{if(!aud.paused){curSec=aud.currentTime;updateProg();}});
aud.addEventListener('loadedmetadata',()=>{const d=Math.floor(aud.duration);tracks[ci].secs=d;tracks[ci].dur=fmt(d);document.getElementById('totT').textContent=fmt(d);setSt('재생 준비 완료 — '+tracks[ci].title,'ok');renderPL();});
aud.addEventListener('ended',()=>nextT());
aud.addEventListener('error',()=>setSt('로드 실패 — URL 확인 필요','er'));
aud.addEventListener('waiting',()=>setSt('버퍼링 중...','ld'));
aud.addEventListener('playing',()=>setSt('재생 중'));
function startVU(){clearInterval(vuInt);vuInt=setInterval(animVU,85);}
function stopVU(){clearInterval(vuInt);animVU();}
function loadT(idx,auto){ci=idx;curSec=0;aud.pause();aud.src='';const t=tracks[idx];document.getElementById('totT').textContent=t.dur;updateProg();if(t.url){aud.src=t.url;aud.volume=parseInt(document.getElementById('volVal').textContent)/100;aud.load();if(auto)aud.play().catch(()=>{});setSt('로딩 중 — '+t.title,'ld');}else{setSt('ADD TRACK 탭에서 URL을 추가해 주세요','er');}updateUI();}
function togglePlay(){if(!tracks[ci].url){setSt('URL 없음','er');return;}playing=!playing;if(playing){if(!aud.src){aud.src=tracks[ci].url;aud.load();}aud.play().catch(()=>{});startVU();}else{aud.pause();stopVU();}document.getElementById('playIcon').innerHTML=playing?'<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>':'<path d="M8 5v14l11-7z"/>';updateUI();}
function selT(i){playing=true;document.getElementById('playIcon').innerHTML='<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';startVU();loadT(i,true);}
function prevT(){selT((ci-1+tracks.length)%tracks.length);}
function nextT(){selT((ci+1)%tracks.length);}
function seek(s){const n=Math.max(0,aud.currentTime+s);aud.currentTime=n;curSec=n;updateProg();}
document.getElementById('progBar').addEventListener('click',function(e){if(!tracks[ci].secs)return;const r=this.getBoundingClientRect();const t=Math.round((e.clientX-r.left)/r.width*tracks[ci].secs);aud.currentTime=t;curSec=t;updateProg();});
function setVol(e){const r=document.getElementById('volTrack').getBoundingClientRect();const v=Math.min(100,Math.max(0,Math.round((e.clientX-r.left)/r.width*100)));document.getElementById('volFill').style.width=v+'%';document.getElementById('volThumb').style.left=v+'%';document.getElementById('volVal').textContent=v;aud.volume=v/100;}
function addAudio(){const idx=parseInt(document.getElementById('trackSel').value);const url=document.getElementById('audioUrl').value.trim();if(!url){setSt('URL을 입력해 주세요','er');return;}tracks[idx].url=url;setSt(tracks[idx].title+' 등록 완료','ok');renderPL();document.getElementById('audioUrl').value='';}
function addCover(){const idx=parseInt(document.getElementById('trackSel').value);const url=document.getElementById('coverUrl').value.trim();if(!url){setSt('이미지 URL을 입력해 주세요','er');return;}tracks[idx].cover=url;if(ci===idx){const img=document.getElementById('covImg');img.src=url;img.style.display='block';document.getElementById('covPh').style.display='none';}setSt(tracks[idx].title+' 커버 등록 완료','ok');document.getElementById('coverUrl').value='';}
aud.volume=0.8;loadT(0,false);
</script>
