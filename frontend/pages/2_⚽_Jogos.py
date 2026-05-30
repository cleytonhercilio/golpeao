import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.components.session import restore_session
from frontend.components.nav import render_bottom_nav
from frontend.api_client import get_matches

_css = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
if os.path.exists(_css):
    with open(_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

restore_session()

if not st.session_state.get("token"):
    st.switch_page("0_🔐_Login.py")

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


def _flag(iso, name):
    return (
        f'<img src="https://flagcdn.com/w80/{iso}.png"'
        f' onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'"'
        f' style="width:52px;height:36px;border-radius:8px;border:2px solid rgba(255,255,255,0.25);object-fit:cover;box-shadow:0 2px 6px rgba(0,0,0,0.4);"'
        f' alt="{name}">'
        f'<span style="display:none;width:52px;height:36px;border-radius:8px;background:#2C5F8A;align-items:center;justify-content:center;font-size:22px;">🌍</span>'
    )


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
        group_name = m.get("group_name", "")
        stage_val = m.get("stage", stage)
        group_label = f"Grupo {group_name}" if group_name else stage_val.upper()
        venue_short = (m.get("venue") or "")[:30] + ("..." if len(m.get("venue") or "") > 30 else "")

        if m.get("is_played"):
            badge = '<span class="badge-done">Encerrado</span>'
            center_html = f'<div class="score-display">{m["home_score"]} × {m["away_score"]}</div>'
        elif m.get("is_locked"):
            badge = '<span class="badge-lock">🔒 Fechado</span>'
            center_html = '<div class="score-display" style="opacity:.35">? × ?</div>'
        else:
            badge = '<span class="badge-open">Aberto</span>'
            center_html = '<div class="score-display" style="opacity:.35">? × ?</div>'

        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="font-size:11px;font-weight:800;color:#A0C8FF;text-transform:uppercase;letter-spacing:1px;">
                    Jogo #{m['match_number']} · {sched} UTC · {venue_short}
                </span>
                {badge}
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;">
                    {_flag(home_iso, home_name)}
                    <span style="font-size:13px;font-weight:900;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.5);text-align:center;">{home_name}</span>
                </div>
                <div style="display:flex;flex-direction:column;align-items:center;gap:4px;min-width:86px;">
                    {center_html}
                </div>
                <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;">
                    {_flag(away_iso, away_name)}
                    <span style="font-size:13px;font-weight:900;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.5);text-align:center;">{away_name}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

render_bottom_nav()
