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
.gp-bottom-nav button {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    color: rgba(255,255,255,0.6) !important;
    font-size: 9px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    gap: 1px;
    padding: 6px 10px !important;
    border-radius: 12px !important;
    cursor: pointer;
    width: auto !important;
    min-width: 48px;
    transition: background 0.15s;
    -webkit-tap-highlight-color: transparent;
    transform: none !important;
}
.gp-bottom-nav button:active {
    background: rgba(255,215,0,0.18) !important;
    color: #FFD700 !important;
    transform: none !important;
}
.gp-nav-icon  { font-size: 22px; line-height: 1.1; display: block; }
.gp-nav-label { font-size: 9px;  display: block; }
</style>
"""


def _nav_html(token: str) -> str:
    # Each button: saves token to localStorage then navigates via window.location.href
    # Python restores the session from the ?_st= query param on the target page
    pages = [
        ("Inicio",        "🏠", "Início"),
        ("Jogos",         "⚽", "Jogos"),
        ("Meus_Palpites", "🎯", "Palpites"),
        ("Ranking",       "🏆", "Ranking"),
        ("Conquistas",    "🏅", "Badges"),
    ]
    buttons = "\n".join(
        f"""    <button onclick="gpNav('{name}')">
        <span class="gp-nav-icon">{icon}</span>
        <span class="gp-nav-label">{label}</span>
    </button>"""
        for name, icon, label in pages
    )

    return f"""
<script>
// Persist token in localStorage so mobile navigation can restore session
localStorage.setItem('gp_tk', '{token}');

function gpNav(pageName) {{
    var tk = localStorage.getItem('gp_tk') || '';
    var path = '/' + pageName;
    window.location.href = tk ? path + '?_st=' + encodeURIComponent(tk) : path;
}}
</script>

<nav class="gp-bottom-nav">
{buttons}
</nav>
"""


def render_bottom_nav():
    if not st.session_state.get("token"):
        return
    st.markdown(_NAV_CSS + _nav_html(st.session_state.token), unsafe_allow_html=True)
