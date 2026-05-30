"""
Music player — injecta o AudioContext no window.parent para funcionar
mesmo com a sidebar colapsada no mobile (iOS/Android).
"""

# ── Motor de áudio injetado no window.parent ─────────────────────────
_ENGINE_HTML = """<!DOCTYPE html><html><body><script>
(function(){
  var p = window.parent;

  // Evita re-inicializar em reruns do Streamlit (mesma sessão)
  if (p.__gp_ac) return;

  var AC = p.AudioContext || p.webkitAudioContext;
  if (!AC) return;

  var BPM=148, TICK=60/BPM/4;
  var N={
    '_':0,
    'C3':130.81,'D3':146.83,'E3':164.81,'F3':174.61,'G3':196.00,'A3':220.00,
    'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,'G4':392.00,'A4':440.00,'B4':493.88,
    'C5':523.25,'D5':587.33,'E5':659.25,'F5':698.46,'G5':783.99,'A5':880.00,'B5':987.77,
    'C6':1046.50
  };
  var MEL=[['E5',2],['_',1],['A5',1],['G5',2],['E5',2],['A5',2],['C6',2],['B5',2],['A5',2],['G5',2],['_',1],['F5',1],['E5',4],['_',2],['D5',2],['E5',2],['F5',2],['E5',2],['D5',1],['C5',1],['E5',2],['G5',2],['A5',4],['G5',2],['E5',2],['F5',2],['E5',2],['D5',2],['C5',2],['A4',4],['_',4]];
  var HAR=[['C5',2],['_',1],['E5',1],['_',4],['F5',2],['A5',2],['_',4],['E5',2],['_',1],['C5',1],['A4',4],['_',2],['B4',2],['C5',2],['D5',2],['C5',2],['B4',1],['A4',1],['C5',2],['E5',2],['F5',4],['E5',2],['C5',2],['D5',2],['C5',2],['B4',2],['A4',2],['E4',4],['_',4]];
  var BAS=[['A3',4],['A3',4],['A3',4],['A3',4],['F3',4],['F3',4],['F3',4],['F3',4],['C3',4],['C3',4],['E3',4],['E3',4],['D3',4],['D3',4],['A3',4],['A3',4]];
  var LOOP=MEL.reduce(function(s,n){return s+n[1];},0)*TICK;

  var ac=new AC();
  var master=ac.createGain();
  master.gain.setValueAtTime(0.8,ac.currentTime);
  master.connect(ac.destination);

  p.__gp_ac=ac; p.__gp_master=master;
  p.__gp_muted=false; p.__gp_playing=false;

  function note(hz,t,dur,type,vol){
    if(!hz)return;
    var o=ac.createOscillator(),g=ac.createGain();
    o.connect(g);g.connect(master);
    o.type=type; o.frequency.setValueAtTime(hz,t);
    g.gain.setValueAtTime(vol,t);
    g.gain.exponentialRampToValueAtTime(0.00001,t+dur*0.87);
    o.start(t);o.stop(t+dur+0.01);
  }

  function scheduleLoop(start){
    if(!p.__gp_playing)return;
    var t=start;
    MEL.forEach(function(n){var d=n[1]*TICK;note(N[n[0]],t,d,'square',0.13);t+=d;});
    t=start;
    HAR.forEach(function(n){var d=n[1]*TICK;note(N[n[0]],t,d,'square',0.06);t+=d;});
    t=start;
    BAS.forEach(function(n){var d=n[1]*TICK;note(N[n[0]],t,d,'triangle',0.07);t+=d;});
    var delay=Math.max(0,(start+LOOP-ac.currentTime-0.3))*1000;
    p.setTimeout(function(){scheduleLoop(start+LOOP);},delay);
  }

  p.__gp_start=function(){
    ac.resume().then(function(){
      if(!p.__gp_playing){p.__gp_playing=true;scheduleLoop(ac.currentTime+0.1);}
    });
  };

  p.__gp_toggle=function(){
    if(!p.__gp_playing){p.__gp_muted=false;p.__gp_start();return;}
    p.__gp_muted=!p.__gp_muted;
    master.gain.setTargetAtTime(p.__gp_muted?0:0.8,ac.currentTime,0.08);
  };

  // Inicia na primeira interação (toque ou clique em qualquer lugar)
  if(ac.state==='running'){
    p.__gp_start();
  } else {
    function onFirst(){
      p.document.removeEventListener('touchstart',onFirst,true);
      p.document.removeEventListener('click',onFirst,true);
      p.__gp_start();
    }
    p.document.addEventListener('touchstart',onFirst,true);
    p.document.addEventListener('click',onFirst,true);
  }
})();
</script></body></html>"""

# ── Botão de controle na sidebar ──────────────────────────────────────
_BTN_HTML = """<!DOCTYPE html>
<html>
<head>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{background:transparent;height:48px;display:flex;align-items:center;}
#btn{
  display:inline-flex;align-items:center;gap:7px;
  background:rgba(2,15,42,0.95);
  border:1.5px solid #FFD700;border-radius:30px;
  padding:7px 15px 7px 11px;cursor:pointer;
  transition:all 0.2s;box-shadow:0 0 10px rgba(255,215,0,0.3);
  user-select:none;-webkit-user-select:none;
}
#btn:hover{box-shadow:0 0 20px rgba(255,215,0,0.55);transform:scale(1.05);}
#btn:active{transform:scale(0.96);}
#icon{font-size:18px;line-height:1;}
#label{font-size:11px;color:#FFD700;font-weight:800;letter-spacing:1.5px;font-family:monospace;}
</style>
</head>
<body>
<div id="btn" onclick="toggle()">
  <span id="icon">🎵</span>
  <span id="label">SOM</span>
</div>
<script>
function syncBtn(){
  var p=window.parent;
  var muted=p.__gp_muted||false;
  document.getElementById('icon').textContent=muted?'🔇':'🎵';
  document.getElementById('label').textContent=muted?'MUDO':'SOM';
}
function toggle(){
  if(window.parent.__gp_toggle) window.parent.__gp_toggle();
  setTimeout(syncBtn,120);
}
setInterval(syncBtn,500);
</script>
</body></html>"""


def render_music_player():
    import streamlit as st
    import streamlit.components.v1 as components

    # Injeta o motor no window.parent (height=0 → invisível)
    components.html(_ENGINE_HTML, height=0)

    # Botão de controle na sidebar
    with st.sidebar:
        st.markdown(
            "<div style='font-size:12px;color:rgba(255,255,255,0.5);"
            "letter-spacing:1px;margin-bottom:4px'>TRILHA SONORA</div>",
            unsafe_allow_html=True,
        )
        components.html(_BTN_HTML, height=48)
