import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.api_client import get_upcoming, get_my_groups

_css = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
if os.path.exists(_css):
    with open(_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

st.markdown("<h1>🏠 Início</h1>", unsafe_allow_html=True)

st.markdown("### ⏰ Próximos Jogos")
upcoming = get_upcoming()
if not upcoming:
    st.info("Nenhum jogo programado em breve.")
else:
    for m in upcoming[:3]:
        home = m.get("home_team") or {}
        away = m.get("away_team") or {}
        home_iso = home.get("iso_code", "xx")
        away_iso = away.get("iso_code", "xx")
        home_name = home.get("name", m.get("match_label", "A definir"))
        away_name = away.get("name", "A definir")
        sched = m.get("scheduled_at", "")[:16].replace("T", " ")
        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex;align-items:center;justify-content:space-around">
                <div style="text-align:center">
                    <img src="https://flagcdn.com/64x48/{home_iso}.png" class="flag-img" onerror="this.style.display='none'"><br>
                    <span class="team-name">{home_name}</span>
                </div>
                <div style="text-align:center">
                    <div style="font-size:1.4em;color:rgba(255,255,255,0.4)">vs</div>
                    <div style="font-size:0.75em;color:rgba(255,255,255,0.5)">{sched} UTC</div>
                </div>
                <div style="text-align:center">
                    <img src="https://flagcdn.com/64x48/{away_iso}.png" class="flag-img" onerror="this.style.display='none'"><br>
                    <span class="team-name">{away_name}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🏆 Meus Bolões")
groups = get_my_groups()
if not groups:
    st.info("Você ainda não participa de nenhum bolão. Acesse **Ranking** para criar ou entrar em um.")
else:
    for g in groups:
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.markdown(f"**{g['name']}**")
        col2.markdown(f"👥 {g.get('member_count', '?')}")
        col3.markdown(f"`{g['invite_code']}`")
