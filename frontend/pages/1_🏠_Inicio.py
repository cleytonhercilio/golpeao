import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.components.session import restore_session
from frontend.components.nav import render_bottom_nav
from frontend.api_client import get_upcoming, get_my_groups

_css = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
if os.path.exists(_css):
    with open(_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

restore_session()

if not st.session_state.get("token"):
    st.switch_page("0_🔐_Login.py")


def render_hud_html(user, next_match_countdown: str = "Em breve") -> str:
    pts = user.get("total_points", 0)
    tier_map = {
        "bronze": "🥉 Bronze", "silver": "🥈 Prata", "gold": "🥇 Ouro",
        "platinum": "💎 Platina", "legend": "👑 Lenda",
    }
    tier_label = tier_map.get(user.get("tier", "bronze"), "🥉 Bronze")
    return f"""
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
        <div class="hud-pill hud-gold">
            <span style="width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#FFD700,#FF8C00);border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:900;color:#7A3800;">★</span>
            <span style="font-family:'Fredoka One',cursive;font-size:16px;color:#FFD700;">{pts} pts</span>
        </div>
        <div class="hud-pill hud-gold" style="border-color:rgba(255,215,0,0.4);">
            <span style="font-size:14px;">{tier_label}</span>
        </div>
        <div class="hud-pill hud-purple" style="margin-left:auto;">
            <span style="font-size:14px;">⏱</span>
            <span style="font-family:'Fredoka One',cursive;font-size:14px;color:#C39BD3;">{next_match_countdown}</span>
        </div>
    </div>
    """


def _flag(iso, name):
    return (
        f'<img src="https://flagcdn.com/w80/{iso}.png"'
        f' onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'"'
        f' style="width:52px;height:36px;border-radius:8px;border:2px solid rgba(255,255,255,0.25);object-fit:cover;box-shadow:0 2px 6px rgba(0,0,0,0.4);"'
        f' alt="{name}">'
        f'<span style="display:none;width:52px;height:36px;border-radius:8px;background:#2C5F8A;align-items:center;justify-content:center;font-size:22px;">🌍</span>'
    )


st.markdown("<h1>🏠 Início</h1>", unsafe_allow_html=True)

user = st.session_state.user or {}
if user:
    st.markdown(render_hud_html(user), unsafe_allow_html=True)

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
        group_name = m.get("group_name", "")
        stage_val = m.get("stage", "group")
        group_label = f"Grupo {group_name}" if group_name else stage_val.upper()
        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="font-size:11px;font-weight:800;color:#A0C8FF;text-transform:uppercase;letter-spacing:1px;">{group_label} · {sched} UTC</span>
                <span class="badge-open">Aberto</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;">
                    {_flag(home_iso, home_name)}
                    <span style="font-size:13px;font-weight:900;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.5);text-align:center;">{home_name}</span>
                </div>
                <div style="display:flex;flex-direction:column;align-items:center;gap:4px;min-width:86px;">
                    <div class="score-display" style="opacity:.35">? × ?</div>
                </div>
                <div style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1;">
                    {_flag(away_iso, away_name)}
                    <span style="font-size:13px;font-weight:900;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.5);text-align:center;">{away_name}</span>
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

render_bottom_nav()
