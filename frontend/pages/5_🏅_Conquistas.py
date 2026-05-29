import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.api_client import get_my_groups

_css = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
if os.path.exists(_css):
    with open(_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

st.markdown("<h1>🏅 Conquistas</h1>", unsafe_allow_html=True)

ALL_ACHIEVEMENTS = [
    {"slug": "primeiro_gol",    "name": "Primeiro Gol",    "icon": "⚽", "description": "Fez seu primeiro palpite",                  "bonus": 5},
    {"slug": "em_chamas",       "name": "Em Chamas",       "icon": "🔥", "description": "3 acertos de vencedor consecutivos",         "bonus": 15},
    {"slug": "craque_do_bolao", "name": "Craque do Bolão", "icon": "🎯", "description": "5 placares exatos no torneio",              "bonus": 25},
    {"slug": "polvo",           "name": "Polvo",           "icon": "🐙", "description": "Acertou todos os jogos de uma rodada",       "bonus": 30},
    {"slug": "aguia",           "name": "Águia",           "icon": "🦅", "description": "Previu eliminação de um favorito",           "bonus": 20},
    {"slug": "lenda",           "name": "Lenda",           "icon": "👑", "description": "Acertou placar exato de empate",            "bonus": 10},
    {"slug": "sortudo",         "name": "Sortudo",         "icon": "🎪", "description": "Placar exato no jogo de abertura",          "bonus": 15},
    {"slug": "fantasma",        "name": "Fantasma",        "icon": "👻", "description": "Não apostou em 5 jogos seguidos",           "bonus": 0},
    {"slug": "rei",             "name": "O Rei",           "icon": "🏆", "description": "Acertou o campeão da Copa",                 "bonus": 50},
    {"slug": "100pts",          "name": "Centenário",      "icon": "💯", "description": "Atingiu 100 pontos no bolão",               "bonus": 20},
]


def show_achievement_popup(achievement_name: str, achievement_icon: str, points_bonus: int):
    st.markdown(f"""
    <div class="ach-popup">
        <div class="ach-icon">{achievement_icon}</div>
        <div style="flex:1;">
            <div style="font-size:11px;font-weight:800;color:#FFD700;text-transform:uppercase;letter-spacing:1px;">Conquista desbloqueada!</div>
            <div style="font-family:'Fredoka One',cursive;font-size:15px;color:#fff;">{achievement_name}</div>
        </div>
        <div style="font-family:'Fredoka One',cursive;font-size:18px;color:#FFD700;">+{points_bonus}</div>
    </div>
    """, unsafe_allow_html=True)


user = st.session_state.user or {}
total_pts = user.get("total_points", 0)

# Simple client-side unlock preview based on known stats
unlocked_slugs = set()
if total_pts >= 1:
    unlocked_slugs.add("primeiro_gol")
if total_pts >= 100:
    unlocked_slugs.add("100pts")

st.markdown(f"### {user.get('avatar_emoji','⚽')} {user.get('display_name','Jogador')} — {total_pts} pts")
st.caption("Badges em ouro = desbloqueados. Cinza = ainda não conquistados.")

# Show popups for newly unlocked achievements (tracked per session)
if "shown_ach_popups" not in st.session_state:
    st.session_state.shown_ach_popups = set()

newly_unlocked = unlocked_slugs - st.session_state.shown_ach_popups
if newly_unlocked:
    ach_map = {a["slug"]: a for a in ALL_ACHIEVEMENTS}
    for slug in newly_unlocked:
        if slug in ach_map:
            ach = ach_map[slug]
            show_achievement_popup(ach["name"], ach["icon"], ach["bonus"])
    st.session_state.shown_ach_popups |= newly_unlocked

st.markdown("---")

cols = st.columns(3)
for i, ach in enumerate(ALL_ACHIEVEMENTS):
    unlocked = ach["slug"] in unlocked_slugs
    badge_class = "badge-unlocked" if unlocked else "badge-locked"
    lock = "" if unlocked else "🔒 "
    bonus_text = f"+{ach['bonus']} pts" if ach["bonus"] > 0 else ""
    with cols[i % 3]:
        st.markdown(f"""
        <div class="match-card" style="text-align:center;padding:16px;min-height:140px">
            <div style="font-size:2.5em">{ach['icon']}</div>
            <div class="badge {badge_class}" style="margin:8px 0">{lock}{ach['name']}</div>
            <div style="font-size:0.78em;color:rgba(255,255,255,{'0.7' if unlocked else '0.3'})">{ach['description']}</div>
            {"<div style='font-size:0.72em;color:#FFD700;margin-top:4px'>" + bonus_text + "</div>" if bonus_text else ""}
        </div>
        """, unsafe_allow_html=True)
