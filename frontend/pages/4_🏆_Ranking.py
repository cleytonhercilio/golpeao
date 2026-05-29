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
        for e in ranking["entries"]:
            pos = e["position"]
            medal = ["🥇", "🥈", "🥉"][pos - 1] if pos <= 3 else f"#{pos}"
            pos_class = f"rank-{pos}" if pos <= 3 else ""
            tier_class = f"tier-{e['tier']}"
            st.markdown(f"""
            <div class="match-card" style="padding:12px 20px;margin:6px 0">
                <div style="display:flex;align-items:center;gap:16px">
                    <div class="{pos_class}" style="min-width:40px;font-size:1.5em;text-align:center">{medal}</div>
                    <div style="font-size:2em">{e['avatar_emoji']}</div>
                    <div style="flex:1">
                        <div style="font-weight:bold">{e['display_name']}</div>
                        <span class="tier-badge {tier_class}">{e['tier'].capitalize()}</span>
                    </div>
                    <div style="text-align:right">
                        <div style="color:var(--copa-gold);font-weight:900;font-size:1.3em">{e['total_points']} pts</div>
                        <div style="font-size:0.78em;color:rgba(255,255,255,0.5)">
                            🎯 {e['exact_scores']} exatos &nbsp;|&nbsp; ✅ {e['correct_winners']} venc.
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
