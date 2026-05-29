_MUSIC_HTML = """<!DOCTYPE html>
<html>
<head>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; display: flex; align-items: center;
         justify-content: flex-start; height: 48px; overflow: hidden; }
  #btn {
    display: inline-flex; align-items: center; gap: 7px;
    background: rgba(2,15,42,0.95);
    border: 1.5px solid #FFD700;
    border-radius: 30px;
    padding: 7px 15px 7px 11px;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 0 10px rgba(255,215,0,0.3);
    user-select: none; -webkit-user-select: none;
  }
  #btn:hover { box-shadow: 0 0 20px rgba(255,215,0,0.55); transform: scale(1.05); }
  #btn:active { transform: scale(0.96); }
  #icon  { font-size: 18px; line-height: 1; }
  #label { font-size: 11px; color: #FFD700; font-weight: 800;
           letter-spacing: 1.5px; font-family: monospace; }
</style>
</head>
<body>
<div id="btn" onclick="toggleMute()">
  <span id="icon">🎵</span>
  <span id="label">SOM</span>
</div>
<script>
(function () {
  /* ─── parâmetros ─────────────────────────── */
  var BPM  = 148;
  var TICK = 60 / BPM / 4;

  /* ─── notas ──────────────────────────────── */
  var N = {
    '_':0,
    'C3':130.81,'D3':146.83,'E3':164.81,'F3':174.61,'G3':196.00,'A3':220.00,
    'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,'G4':392.00,'A4':440.00,'B4':493.88,
    'C5':523.25,'D5':587.33,'E5':659.25,'F5':698.46,'G5':783.99,'A5':880.00,'B5':987.77,
    'C6':1046.50
  };

  /* ─── partitura (FIFA PS1 style — lá menor) ── */
  var MEL = [
    ['E5',2],['_',1],['A5',1],['G5',2],['E5',2],
    ['A5',2],['C6',2],['B5',2],['A5',2],
    ['G5',2],['_',1],['F5',1],['E5',4],
    ['_',2],['D5',2],['E5',2],['F5',2],
    ['E5',2],['D5',1],['C5',1],['E5',2],['G5',2],
    ['A5',4],['G5',2],['E5',2],
    ['F5',2],['E5',2],['D5',2],['C5',2],
    ['A4',4],['_',4]
  ];
  var HAR = [
    ['C5',2],['_',1],['E5',1],['_',4],
    ['F5',2],['A5',2],['_',4],
    ['E5',2],['_',1],['C5',1],['A4',4],
    ['_',2],['B4',2],['C5',2],['D5',2],
    ['C5',2],['B4',1],['A4',1],['C5',2],['E5',2],
    ['F5',4],['E5',2],['C5',2],
    ['D5',2],['C5',2],['B4',2],['A4',2],
    ['E4',4],['_',4]
  ];
  var BAS = [
    ['A3',4],['A3',4],['A3',4],['A3',4],
    ['F3',4],['F3',4],['F3',4],['F3',4],
    ['C3',4],['C3',4],['E3',4],['E3',4],
    ['D3',4],['D3',4],['A3',4],['A3',4]
  ];

  var LOOP = MEL.reduce(function(s,n){return s+n[1];},0)*TICK;

  /* ─── estado ─────────────────────────────── */
  var ac=null, master=null, muted=false, playing=false;

  /* ─── agenda nota ────────────────────────── */
  function note(hz, t, dur, type, vol) {
    if (!hz) return;
    var o=ac.createOscillator(), g=ac.createGain();
    o.connect(g); g.connect(master);
    o.type=type;
    o.frequency.setValueAtTime(hz, t);
    g.gain.setValueAtTime(vol, t);
    g.gain.exponentialRampToValueAtTime(0.00001, t+dur*0.87);
    o.start(t); o.stop(t+dur+0.01);
  }

  /* ─── agenda loop ────────────────────────── */
  function scheduleLoop(start) {
    if (!playing) return;
    var t=start;
    MEL.forEach(function(n){var d=n[1]*TICK; note(N[n[0]],t,d,'square',0.13); t+=d;});
    t=start;
    HAR.forEach(function(n){var d=n[1]*TICK; note(N[n[0]],t,d,'square',0.06); t+=d;});
    t=start;
    BAS.forEach(function(n){var d=n[1]*TICK; note(N[n[0]],t,d,'triangle',0.07); t+=d;});
    var delay=Math.max(0,(start+LOOP-ac.currentTime-0.3))*1000;
    setTimeout(function(){scheduleLoop(start+LOOP);},delay);
  }

  /* ─── começa a tocar ─────────────────────── */
  function startPlaying() {
    ac.resume().then(function() {
      if (!playing) {
        playing = true;
        scheduleLoop(ac.currentTime + 0.1);
      }
      updateBtn();
    });
  }

  /* ─── atualiza botão ─────────────────────── */
  function updateBtn() {
    document.getElementById('icon').textContent  = muted ? '🔇' : '🎵';
    document.getElementById('label').textContent = muted ? 'MUDO' : 'SOM';
  }

  /* ─── mute/unmute (botão) ────────────────── */
  window.toggleMute = function() {
    if (!playing) {
      /* primeira interação veio pelo botão */
      muted = false;
      startPlaying();
      return;
    }
    muted = !muted;
    master.gain.setTargetAtTime(muted?0:0.8, ac.currentTime, 0.08);
    updateBtn();
  };

  /* ─── inicializa AudioContext na carga ───── */
  var AC = window.AudioContext || window.webkitAudioContext;
  if (!AC) return;
  ac = new AC();
  master = ac.createGain();
  master.gain.setValueAtTime(0.8, ac.currentTime);
  master.connect(ac.destination);

  if (ac.state === 'running') {
    /* browser permite autoplay — toca imediatamente */
    playing = true;
    scheduleLoop(ac.currentTime + 0.1);
    updateBtn();
  } else {
    /* browser bloqueou — aguarda qualquer interação na página */
    var doc = (window.parent && window.parent.document) || document;
    function onFirstInteraction() {
      doc.removeEventListener('click',    onFirstInteraction, true);
      doc.removeEventListener('keydown',  onFirstInteraction, true);
      doc.removeEventListener('touchstart',onFirstInteraction, true);
      startPlaying();
    }
    doc.addEventListener('click',     onFirstInteraction, true);
    doc.addEventListener('keydown',   onFirstInteraction, true);
    doc.addEventListener('touchstart',onFirstInteraction, true);
  }
})();
</script>
</body>
</html>"""


def render_music_player():
    import streamlit as st

    with st.sidebar:
        st.markdown(
            "<div style='font-size:12px;color:rgba(255,255,255,0.5);"
            "letter-spacing:1px;margin-bottom:4px'>TRILHA SONORA</div>",
            unsafe_allow_html=True,
        )
        st.iframe(_MUSIC_HTML, height=48)
