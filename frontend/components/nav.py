import streamlit as st

_NAV_CSS = """
<style>
.gp-bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 62px;
    background: linear-gradient(180deg, #0D2540ee, #1A3A5Cee);
    border-top: 2px solid rgba(255,215,0,0.35);
    display: none;
    align-items: center;
    justify-content: space-around;
    z-index: 999999;
    padding-bottom: env(safe-area-inset-bottom);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}
@media (max-width: 768px) {
    .gp-bottom-nav { display: flex !important; }
    [data-testid="stMainBlockContainer"] { padding-bottom: 80px !important; }
    /* Remove FAB - agora temos bottom nav */
    [data-testid="stSidebarToggleButton"] { display: none !important; }
}
.gp-bottom-nav a {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none !important;
    color: rgba(255,255,255,0.55) !important;
    font-size: 9px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    gap: 1px;
    padding: 6px 10px;
    border-radius: 12px;
    transition: all 0.18s;
    min-width: 48px;
    -webkit-tap-highlight-color: transparent;
}
.gp-bottom-nav a:hover {
    color: #FFD700 !important;
    background: rgba(255,215,0,0.12) !important;
}
.gp-bottom-nav .nav-icon { font-size: 22px; line-height: 1.1; }
</style>
"""

_NAV_HTML = """
<nav class="gp-bottom-nav">
    <a href="/Inicio">
        <span class="nav-icon">🏠</span>
        <span>Início</span>
    </a>
    <a href="/Jogos">
        <span class="nav-icon">⚽</span>
        <span>Jogos</span>
    </a>
    <a href="/Meus_Palpites">
        <span class="nav-icon">🎯</span>
        <span>Palpites</span>
    </a>
    <a href="/Ranking">
        <span class="nav-icon">🏆</span>
        <span>Ranking</span>
    </a>
    <a href="/Conquistas">
        <span class="nav-icon">🏅</span>
        <span>Badges</span>
    </a>
</nav>
"""


def render_bottom_nav():
    if not st.session_state.get("token"):
        return
    st.markdown(_NAV_CSS + _NAV_HTML, unsafe_allow_html=True)
