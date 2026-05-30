import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.components.session import restore_session
from frontend.components.nav import render_bottom_nav
from frontend.api_client import get_my_groups, get_ranking, create_group, join_group, preview_group

_css = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
if os.path.exists(_css):
    with open(_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

restore_session()

if not st.session_state.get("token"):
    st.switch_page("0_🔐_Login.py")

st.markdown("<h1>🏆 Ranking & Grupos</h1>", unsafe_allow_html=True)

user = st.session_state.user or {}
is_admin = user.get("is_admin", False)

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


TIER_ICONS = {"bronze": "🥉", "silver": "🥈", "gold": "🥇", "platinum": "💎", "legend": "👑"}
POS_COLORS = {1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32"}


def render_ranking(entries: list):
    st.markdown("""
    <div style="background:linear-gradient(90deg,#1A3A5C,#0D2540);padding:10px 16px;
                border-radius:14px 14px 0 0;border-bottom:2px solid rgba(255,215,0,0.3);">
        <b style="font-family:'Fredoka One',cursive;font-size:17px;color:#FFD700;">🏆 Ranking do Bolão</b>
    </div>
    """, unsafe_allow_html=True)

    for e in entries:
        pos   = e.get("position", 0)
        name  = e.get("display_name", "?")
        avatar= e.get("avatar_emoji", "⚽")
        pts   = e.get("total_points", 0)
        tier  = e.get("tier", "bronze")
        exact = e.get("exact_scores", 0)
        wins  = e.get("correct_winners", 0)
        tier_icon = TIER_ICONS.get(tier, "🥉")
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(pos, f"#{pos}")
        color = POS_COLORS.get(pos, "rgba(255,255,255,0.7)")

        c1, c2, c3, c4 = st.columns([0.5, 3, 2, 1])
        with c1:
            st.markdown(
                f"<div style='text-align:center;font-size:20px;padding-top:6px'>{medal}</div>",
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"<div style='padding-top:4px'>"
                f"<b style='color:{color};font-size:15px'>{avatar} {name}</b> "
                f"<span style='font-size:13px'>{tier_icon}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f"<div style='color:rgba(255,255,255,0.6);font-size:12px;padding-top:8px'>"
                f"🎯 {exact} exatos &nbsp;|&nbsp; ✅ {wins} vencedor</div>",
                unsafe_allow_html=True,
            )
        with c4:
            st.markdown(
                f"<div style='text-align:right;font-family:\"Fredoka One\",cursive;"
                f"font-size:18px;color:#FFD700;padding-top:4px'>{pts} pts</div>",
                unsafe_allow_html=True,
            )
        st.markdown(
            "<hr style='margin:0;border:none;border-top:1px solid rgba(255,255,255,0.07)'>",
            unsafe_allow_html=True,
        )


# ── Inicializar state do fluxo de entrada ──────────────────────────
for k, v in [("group_preview", None), ("group_code_input", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

tab_ranking, tab_groups = st.tabs(["📊 Ranking", "👥 Grupos"])

with tab_groups:

    # ── CRIAR BOLÃO (apenas admin) ─────────────────────────────────
    if is_admin:
        st.markdown("#### ➕ Criar Bolão")
        with st.form("new_group"):
            name = st.text_input("Nome do bolão")
            if st.form_submit_button("Criar Bolão", use_container_width=True):
                if name.strip():
                    data, code = create_group(name.strip())
                    if code == 201:
                        st.success("✅ Bolão criado! Compartilhe o código abaixo:")
                        st.markdown(
                            f'<div class="invite-code">{data["invite_code"]}</div>',
                            unsafe_allow_html=True,
                        )
                        st.caption("Envie este código para os participantes via WhatsApp.")
                    else:
                        st.error(f"❌ {data.get('detail', 'Erro ao criar bolão')}")
                else:
                    st.error("Nome do bolão é obrigatório.")
        st.markdown("---")

    # ── ENTRAR EM BOLÃO (todos os usuários) ────────────────────────
    st.markdown("#### 🔗 Entrar em um Bolão")

    # Passo 1 — digitar o código
    if st.session_state.group_preview is None:
        code_val = st.text_input(
            "Código de convite (6 caracteres)",
            value=st.session_state.group_code_input,
            max_chars=6,
            placeholder="Ex: ABC123",
        )
        if st.button("🔍 Verificar código", use_container_width=True):
            code_val = code_val.strip().upper()
            if len(code_val) == 6:
                data, status = preview_group(code_val)
                if status == 200:
                    st.session_state.group_preview = data
                    st.session_state.group_code_input = code_val
                    st.rerun()
                else:
                    st.error(f"❌ {data.get('detail', 'Código inválido')}")
            else:
                st.error("O código deve ter exatamente 6 caracteres.")

    # Passo 2 — confirmação com nome do bolão
    else:
        preview = st.session_state.group_preview
        already = preview.get("already_member", False)

        st.markdown(f"""
        <div class="ach-popup">
            <div class="ach-icon">⚽</div>
            <div>
                <div style="font-family:'Fredoka One',cursive;font-size:18px;color:#FFD700;">{preview['name']}</div>
                <div style="font-size:13px;color:rgba(255,255,255,0.7);">👥 {preview['member_count']} participante(s) · Código: <b>{preview['invite_code']}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if already:
            st.info("ℹ️ Você já é membro deste bolão.")
            if st.button("↩️ Voltar", use_container_width=True):
                st.session_state.group_preview = None
                st.session_state.group_code_input = ""
                st.rerun()
        else:
            col_confirm, col_cancel = st.columns(2)
            with col_confirm:
                if st.button("✅ Confirmar entrada", use_container_width=True):
                    data, status = join_group(preview["invite_code"])
                    if status == 200:
                        st.session_state.group_preview = None
                        st.session_state.group_code_input = ""
                        st.success(f"🎉 Você entrou em **{data['name']}**!")
                        st.rerun()
                    else:
                        st.error(f"❌ {data.get('detail', 'Erro ao entrar no bolão')}")
            with col_cancel:
                if st.button("❌ Cancelar", use_container_width=True):
                    st.session_state.group_preview = None
                    st.session_state.group_code_input = ""
                    st.rerun()

    # ── MEUS BOLÕES ────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🏅 Meus Bolões")
    groups = get_my_groups()
    if not groups:
        st.info("Você ainda não participa de nenhum bolão. Use um código de convite acima!")
    for g in groups:
        cols = st.columns([3, 2, 1])
        with cols[0]:
            st.markdown(f"**{g['name']}**")
        with cols[1]:
            if is_admin:
                st.markdown(f'<span class="invite-code" style="font-size:1em;letter-spacing:4px;padding:4px 8px;">{g["invite_code"]}</span>', unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f"👥 {g.get('member_count', '?')}")

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
        render_ranking(ranking["entries"])

render_bottom_nav()
