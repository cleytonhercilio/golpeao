import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.api_client import get_matches

_css = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
if os.path.exists(_css):
    with open(_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

st.markdown("<h1>⚽ Jogos</h1>", unsafe_allow_html=True)

STAGES = {
    "group": "Fase de Grupos", "round32": "Oitavas (R32)", "round16": "Round of 16",
    "qf": "Quartas de Final", "sf": "Semifinais", "third": "3º Lugar", "final": "Final",
}

stage = st.selectbox("Fase", list(STAGES.keys()), format_func=lambda x: STAGES[x])
group_filter = None
if stage == "group":
    gf = st.selectbox("Grupo", ["Todos"] + list("ABCDEFGHIJKL"))
    if gf != "Todos":
        group_filter = gf

matches = get_matches(stage=stage, group=group_filter)
if not matches:
    st.info("Nenhum jogo encontrado.")
else:
    for m in matches:
        home = m.get("home_team") or {}
        away = m.get("away_team") or {}
        home_iso = home.get("iso_code", "xx")
        away_iso = away.get("iso_code", "xx")
        home_name = home.get("name", "A definir")
        away_name = away.get("name", "A definir")
        sched = m.get("scheduled_at", "")[:16].replace("T", " ")

        if m.get("is_played"):
            mid_html = f'<div class="score-display">{m["home_score"]} × {m["away_score"]}</div>'
        elif m.get("is_locked"):
            mid_html = '<div style="text-align:center;color:#FF6B35;font-size:1.2em">🔒 Fechado</div>'
        else:
            mid_html = '<div style="text-align:center;color:#7FFF00">🟢 Aberto</div>'

        label = m.get("match_label") or f"{home_name} vs {away_name}"
        st.markdown(f"""
        <div class="match-card">
            <div style="font-size:0.72em;color:rgba(255,255,255,0.4);margin-bottom:8px">
                Jogo #{m['match_number']} | {sched} UTC | {m.get('venue','')[:40]}
            </div>
            <div style="display:flex;align-items:center;justify-content:space-around">
                <div style="text-align:center;width:35%">
                    <img src="https://flagcdn.com/64x48/{home_iso}.png" class="flag-img" onerror="this.style.display='none'"><br>
                    <span class="team-name">{home_name}</span>
                </div>
                <div style="width:30%">{mid_html}</div>
                <div style="text-align:center;width:35%">
                    <img src="https://flagcdn.com/64x48/{away_iso}.png" class="flag-img" onerror="this.style.display='none'"><br>
                    <span class="team-name">{away_name}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
