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
    [data-testid="stSidebarToggleButton"] { display: none !important; }
}
.gp-nav-link {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    text-decoration: none !important;
    color: rgba(255,255,255,0.6) !important;
    font-size: 9px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    gap: 1px !important;
    padding: 6px 10px !important;
    border-radius: 12px !important;
    min-width: 48px !important;
    -webkit-tap-highlight-color: transparent !important;
    transition: background 0.12s, color 0.12s !important;
}
.gp-nav-link:active {
    background: rgba(255,215,0,0.18) !important;
    color: #FFD700 !important;
}
.gp-nav-icon  { font-size: 22px; line-height: 1.1; display: block; }
.gp-nav-label { font-size: 9px; display: block; }
</style>
"""

_PAGES = [
    ("Inicio",        "🏠", "Início"),
    ("Jogos",         "⚽", "Jogos"),
    ("Meus_Palpites", "🎯", "Palpites"),
    ("Ranking",       "🏆", "Ranking"),
    ("Conquistas",    "🏅", "Badges"),
]


def _nav_html(token: str) -> str:
    links = "\n".join(
        f'<a href="/{name}?_st={token}" class="gp-nav-link">'
        f'<span class="gp-nav-icon">{icon}</span>'
        f'<span class="gp-nav-label">{label}</span>'
        f'</a>'
        for name, icon, label in _PAGES
    )
    return f'<nav class="gp-bottom-nav">\n{links}\n</nav>'


def render_bottom_nav():
    if not st.session_state.get("token"):
        return
    st.markdown(_NAV_CSS + _nav_html(st.session_state.token), unsafe_allow_html=True)
