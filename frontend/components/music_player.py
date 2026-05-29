MUSIC_PLAYER_HTML = """
<style>
#gp-music-player {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 99999;
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(2, 15, 42, 0.92);
    border: 1.5px solid #FFD700;
    border-radius: 30px;
    padding: 9px 18px 9px 14px;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 0 14px rgba(255,215,0,0.35);
    user-select: none;
    -webkit-user-select: none;
}
#gp-music-player:hover {
    box-shadow: 0 0 26px rgba(255,215,0,0.6);
    transform: scale(1.06);
    border-color: #fff;
}
#gp-music-player:active { transform: scale(0.97); }
#gp-music-icon  { font-size: 20px; line-height: 1; }
#gp-music-label { font-size: 11px; color: #FFD700; font-weight: 800;
                  letter-spacing: 1.5px; font-family: monospace; }
</style>

<div id="gp-music-player" onclick="gpToggleMusic()" title="Trilha sonora">
    <span id="gp-music-icon">🎵</span>
    <span id="gp-music-label">SOM</span>
</div>

<script>
(function () {
    /* ── guard: só inicializa uma vez por sessão de página ── */
    if (window._gpMusicReady) {
        var icon  = document.getElementById('gp-music-icon');
        var label = document.getElementById('gp-music-label');
        if (icon && window._gpMusic) {
            icon.textContent  = window._gpMusic.muted ? '🔇' : '🎵';
            label.textContent = window._gpMusic.muted ? 'MUDO' : 'SOM';
        }
        return;
    }
    window._gpMusicReady = true;

    /* ── parâmetros de tempo ── */
    var BPM  = 148;
    var TICK = 60 / BPM / 4;   /* duração de uma semínima */

    /* ── tabela de frequências ── */
    var N = {
        '_'  : 0,
        'C3' : 130.81, 'D3' : 146.83, 'E3' : 164.81, 'F3' : 174.61,
        'G3' : 196.00, 'A3' : 220.00, 'B3' : 246.94,
        'C4' : 261.63, 'D4' : 293.66, 'E4' : 329.63, 'F4' : 349.23,
        'G4' : 392.00, 'A4' : 440.00, 'B4' : 493.88,
        'C5' : 523.25, 'D5' : 587.33, 'E5' : 659.25, 'F5' : 698.46,
        'G5' : 783.99, 'A5' : 880.00, 'B5' : 987.77, 'C6' : 1046.50
    };

    /*
     * ── melodia principal — estilo FIFA PS1 ─────────────────
     *  Lá menor, 8 compassos de 4/4
     *  Cada entrada: [nota, duração_em_semicolcheias]
     *  Total: 64 semicolcheias = 8 compassos
     */
    var MELODY = [
        /* compasso 1 */ ['E5',2],['_',1],['A5',1],['G5',2],['E5',2],
        /* compasso 2 */ ['A5',2],['C6',2],['B5',2],['A5',2],
        /* compasso 3 */ ['G5',2],['_',1],['F5',1],['E5',4],
        /* compasso 4 */ ['_',2],['D5',2],['E5',2],['F5',2],
        /* compasso 5 */ ['E5',2],['D5',1],['C5',1],['E5',2],['G5',2],
        /* compasso 6 */ ['A5',4],['G5',2],['E5',2],
        /* compasso 7 */ ['F5',2],['E5',2],['D5',2],['C5',2],
        /* compasso 8 */ ['A4',4],['_',4]
    ];

    /* ── contramelo (harmonia) ── */
    var HARM = [
        ['C5',2],['_',1],['E5',1],['_',4],
        ['F5',2],['A5',2],['_',4],
        ['E5',2],['_',1],['C5',1],['A4',4],
        ['_',2],['B4',2],['C5',2],['D5',2],
        ['C5',2],['B4',1],['A4',1],['C5',2],['E5',2],
        ['F5',4],['E5',2],['C5',2],
        ['D5',2],['C5',2],['B4',2],['A4',2],
        ['E4',4],['_',4]
    ];

    /* ── baixo ── */
    var BASS = [
        ['A3',4],['A3',4],
        ['A3',4],['A3',4],
        ['F3',4],['F3',4],
        ['F3',4],['F3',4],
        ['C3',4],['C3',4],
        ['E3',4],['E3',4],
        ['D3',4],['D3',4],
        ['A3',4],['A3',4]
    ];

    /* duração total do loop */
    var LOOP_DUR = MELODY.reduce(function (s, n) { return s + n[1]; }, 0) * TICK;

    /* estado global */
    var music = { ctx: null, master: null, muted: false, started: false };
    window._gpMusic = music;

    /* ── agenda uma nota individual ── */
    function note(freq, t, dur, type, vol) {
        if (!freq) return;
        var osc = music.ctx.createOscillator();
        var g   = music.ctx.createGain();
        osc.connect(g);
        g.connect(music.master);
        osc.type = type;
        osc.frequency.setValueAtTime(freq, t);
        g.gain.setValueAtTime(vol, t);
        g.gain.exponentialRampToValueAtTime(0.00001, t + dur * 0.88);
        osc.start(t);
        osc.stop(t + dur + 0.01);
    }

    /* ── agenda um loop completo a partir de startTime ── */
    function scheduleLoop(startTime) {
        if (!music.started) return;

        var t = startTime;
        MELODY.forEach(function (n) {
            var d = n[1] * TICK;
            note(N[n[0]], t, d, 'square', 0.13);
            t += d;
        });

        t = startTime;
        HARM.forEach(function (n) {
            var d = n[1] * TICK;
            note(N[n[0]], t, d, 'square', 0.06);
            t += d;
        });

        t = startTime;
        BASS.forEach(function (n) {
            var d = n[1] * TICK;
            note(N[n[0]], t, d, 'triangle', 0.07);
            t += d;
        });

        /* agenda o próximo loop 300 ms antes deste terminar */
        var delay = Math.max(0, (startTime + LOOP_DUR - music.ctx.currentTime - 0.3)) * 1000;
        setTimeout(function () { scheduleLoop(startTime + LOOP_DUR); }, delay);
    }

    /* ── inicia o AudioContext e começa o loop ── */
    function startMusic() {
        if (!music.ctx) {
            var AC = window.AudioContext || window.webkitAudioContext;
            if (!AC) return;
            music.ctx    = new AC();
            music.master = music.ctx.createGain();
            music.master.gain.setValueAtTime(0.8, music.ctx.currentTime);
            music.master.connect(music.ctx.destination);
        }
        if (music.ctx.state === 'suspended') music.ctx.resume();
        if (!music.started) {
            music.started = true;
            scheduleLoop(music.ctx.currentTime + 0.15);
        }
    }

    /* ── atualiza visual do botão ── */
    function updateBtn() {
        var icon  = document.getElementById('gp-music-icon');
        var label = document.getElementById('gp-music-label');
        if (icon)  icon.textContent  = music.muted ? '🔇' : '🎵';
        if (label) label.textContent = music.muted ? 'MUDO' : 'SOM';
    }

    /* ── função pública: toggle ── */
    window.gpToggleMusic = function () {
        if (!music.started) {
            startMusic();
            music.muted = false;
        } else {
            music.muted = !music.muted;
            music.master.gain.setTargetAtTime(
                music.muted ? 0 : 0.8,
                music.ctx.currentTime,
                0.08
            );
        }
        updateBtn();
    };
})();
</script>
"""


def render_music_player():
    import streamlit as st
    st.markdown(MUSIC_PLAYER_HTML, unsafe_allow_html=True)
