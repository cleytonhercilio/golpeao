import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.api_client import get_my_groups, get_ranking, create_group, join_group

_css = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
if os.path.exists(_css):
    with open(_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

st.markdown("<h1>🏆 Ranking & Grupos</h1>", unsafe_allow_html=True)

user = st.session_state.user or {}
if user:
    pts = user.get("total_points", 0)
    tier_map = {
        "bronze": "🥉 Bronze", "silver": "🥈 Prata", "gold": "🥇 Ouro",
        "platinum": "💎 Platina", "legend": "👑 Lenda",
    }
    tier_label = tier_map.get(user.get("tier", "bronze"), "🥉 Bronze")
    st.markdown(f"""
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
        <div class="hud-pill hud-gold">
            <span style="width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#FFD700,#FF8C00);border:2px solid #fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:900;color:#7A3800;">★</span>
            <span style="font-family:'Fredoka One',cursive;font-size:16px;color:#FFD700;">{pts} pts</span>
        </div>
        <div class="hud-pill hud-gold" style="border-color:rgba(255,215,0,0.4);">
            <span style="font-size:14px;">{tier_label}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_ranking_html(entries: list) -> str:
    tier_icons = {"bronze": "🥉", "silver": "🥈", "gold": "🥇", "platinum": "💎", "legend": "👑"}
    rows = ""
    for e in entries:
        pos = e.get("position", 0)
        name = e.get("display_name", "?")
        avatar = e.get("avatar_emoji", "⚽")
        pts = e.get("total_points", 0)
        tier = e.get("tier", "bronze")
        tier_icon = tier_icons.get(tier, "🥉")
        exact = e.get("exact_scores", 0)
        winners = e.get("correct_winners", 0)

        if pos == 1:   pos_class = "rank-1"
        elif pos == 2: pos_class = "rank-2"
        elif pos == 3: pos_class = "rank-3"
        else:          pos_class = "rank-n"

        rows += f"""
        <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;border-bottom:1px solid rgba(255,255,255,0.07);">
            <div class="{pos_class}" style="width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Fredoka One',cursive;font-size:14px;font-weight:900;flex-shrink:0;">{pos}</div>
            <div style="width:32px;height:32px;border-radius:50%;background:#234870;border:2px solid rgba(255,255,255,0.2);display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">{avatar}</div>
            <div style="flex:1;font-size:14px;font-weight:900;color:#fff;">{name} <span style="font-size:12px">{tier_icon}</span></div>
            <div style="font-size:11px;color:rgba(255,255,255,0.5);">🎯 {exact} | ✅ {winners}</div>
            <div style="font-family:'Fredoka One',cursive;font-size:15px;color:#FFD700;">{pts}</div>
        </div>
        """
    return f"""
    <div class="rank-card">
        <div style="background:linear-gradient(90deg,#234870,#1A3A5C);padding:8px 14px;display:flex;align-items:center;gap:8px;border-bottom:2px solid rgba(255,215,0,0.2);">
            <span style="font-family:'Fredoka One',cursive;font-size:16px;color:#FFD700;">🏆 Ranking do Bolão</span>
        </div>
        {rows}
    </div>
    """


tab_ranking, tab_groups = st.tabs(["📊 Ranking", "👥 Grupos"])

with tab_groups:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ➕ Criar Bolão")
        with st.form("new_group"):
            name = st.text_input("Nome do bolão")
            if st.form_submit_button("Criar", use_container_width=True):
                if name.strip():
                    data, code = create_group(name.strip())
                    if code == 201:
                        st.success(f"✅ Bolão criado!")
                        st.markdown(f'<div class="invite-code">{data["invite_code"]}</div>', unsafe_allow_html=True)
                        st.caption("Compartilhe este código!")
                    else:
                        st.error(f"❌ {data.get('detail', 'Erro')}")
                else:
                    st.error("Nome é obrigatório.")
    with col2:
        st.markdown("#### 🔗 Entrar em Bolão")
        with st.form("join_group"):
            code = st.text_input("Código de convite (6 letras)")
            if st.form_submit_button("Entrar", use_container_width=True):
                if code.strip():
                    data, status = join_group(code.strip().upper())
                    if status == 200:
                        st.success(f"✅ Você entrou em **{data['name']}**!")
                        st.rerun()
                    else:
                        st.error(f"❌ {data.get('detail', 'Erro')}")

    st.markdown("---")
    st.markdown("#### 🏅 Meus Bolões")
    groups = get_my_groups()
    if not groups:
        st.info("Você ainda não participa de nenhum bolão.")
    for g in groups:
        st.markdown(f"**{g['name']}** — Código: `{g['invite_code']}` — 👥 {g.get('member_count', '?')} membros")

with tab_ranking:
    groups = get_my_groups()
    if not groups:
        st.info("Entre em um bolão para ver o ranking!")
        st.stop()

    group_map = {g["id"]: g["name"] for g in groups}
    gid = st.selectbox("Bolão", list(group_map.keys()), format_func=lambda x: group_map[x])

    ranking = get_ranking(gid)
    if not ranking or not ranking.get("entries"):
        st.info("Nenhum palpite registrado ainda.")
    else:
        st.markdown(render_ranking_html(ranking["entries"]), unsafe_allow_html=True)
