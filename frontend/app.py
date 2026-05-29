import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from frontend.api_client import login, register, me
from frontend.components.music_player import render_music_player

st.set_page_config(
    page_title="GolPeão ⚽",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

_css_path = os.path.join(os.path.dirname(__file__), "style.css")
if os.path.exists(_css_path):
    with open(_css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session state init
for key, default in [("token", None), ("user", None), ("active_group", None)]:
    if key not in st.session_state:
        st.session_state[key] = default


def _render_login():
    st.markdown("<h1 style='text-align:center'>⚽ GolPeão</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;color:rgba(255,255,255,0.6)'>"
        "Bolão Gamificado — Copa do Mundo 2026</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    tab_login, tab_register = st.tabs(["🔑 Entrar", "🎉 Criar Conta"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar", use_container_width=True):
                token, err = login(username, password)
                if token:
                    st.session_state.token = token
                    st.session_state.user = me()
                    st.rerun()
                else:
                    st.error(f"❌ {err}")

    with tab_register:
        with st.form("register_form"):
            new_username = st.text_input("Nome de usuário")
            new_email = st.text_input("Email")
            new_display = st.text_input("Nome de exibição")
            new_avatar = st.selectbox("Avatar", ["⚽", "🏆", "🎯", "🔥", "⚡", "🦅", "🐙", "👑"])
            new_password = st.text_input("Senha", type="password")
            if st.form_submit_button("Criar Conta", use_container_width=True):
                data, code = register(new_username, new_email, new_password, new_display, new_avatar)
                if code == 201:
                    st.success("✅ Conta criada! Faça login na aba ao lado.")
                else:
                    st.error(f"❌ {data.get('detail', 'Erro ao criar conta')}")


def _render_sidebar():
    user = st.session_state.user
    if not user:
        return
    with st.sidebar:
        tier = user.get("tier", "bronze")
        tier_class = f"tier-{tier}"
        st.markdown(f"""
        <div style="text-align:center;padding:10px 0">
            <div style="font-size:3em">{user['avatar_emoji']}</div>
            <div style="font-weight:bold;font-size:1.1em;margin:4px 0">{user['display_name']}</div>
            <span class="tier-badge {tier_class}">{tier.capitalize()}</span>
            <div style="margin-top:8px;color:var(--copa-gold);font-weight:bold;font-size:1.2em">
                {user['total_points']} pts
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.active_group = None
            st.rerun()


if not st.session_state.token:
    _render_login()
else:
    _render_sidebar()
    render_music_player()
    st.markdown("<h2>🏠 Bem-vindo ao GolPeão!</h2>", unsafe_allow_html=True)
    user = st.session_state.user
    if user:
        st.markdown(
            f"Olá, **{user['display_name']}**! Use o menu lateral para navegar entre as páginas.",
            unsafe_allow_html=True,
        )
    st.info("🏆 Copa do Mundo FIFA 2026 — EUA / Canadá / México")
    st.markdown("---")
    st.markdown("**Navegação:**")
    st.markdown("- 🏠 **Início** — Próximos jogos e seus bolões")
    st.markdown("- ⚽ **Jogos** — Todos os jogos por fase/grupo")
    st.markdown("- 🎯 **Meus Palpites** — Registre e edite palpites")
    st.markdown("- 🏆 **Ranking** — Classificação e grupos")
    st.markdown("- 🏅 **Conquistas** — Seus badges")
