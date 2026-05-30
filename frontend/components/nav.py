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
    color: rgba(255,255,255,0.55) !important;
    font-size: 9px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    gap: 1px;
    padding: 6px 10px !important;
    border-radius: 12px !important;
    cursor: pointer;
    width: auto !important;
    min-width: 48px;
    transition: all 0.18s;
    -webkit-tap-highlight-color: transparent;
}
.gp-bottom-nav button:hover,
.gp-bottom-nav button:active {
    color: #FFD700 !important;
    background: rgba(255,215,0,0.12) !important;
    transform: none !important;
}
.gp-bottom-nav .nav-icon { font-size: 22px; line-height: 1.1; display:block; }
.gp-bottom-nav .nav-label { font-size: 9px; display:block; }
</style>
"""

# Uses sidebar link click simulation to preserve Streamlit session state
_NAV_HTML = """
<nav class="gp-bottom-nav">
    <button onclick="gpNav('Inicio')">
        <span class="nav-icon">🏠</span>
        <span class="nav-label">Início</span>
    </button>
    <button onclick="gpNav('Jogos')">
        <span class="nav-icon">⚽</span>
        <span class="nav-label">Jogos</span>
    </button>
    <button onclick="gpNav('Meus_Palpites')">
        <span class="nav-icon">🎯</span>
        <span class="nav-label">Palpites</span>
    </button>
    <button onclick="gpNav('Ranking')">
        <span class="nav-icon">🏆</span>
        <span class="nav-label">Ranking</span>
    </button>
    <button onclick="gpNav('Conquistas')">
        <span class="nav-icon">🏅</span>
        <span class="nav-label">Badges</span>
    </button>
</nav>

<script>
function gpNav(pageName) {
    // Simulate click on the sidebar nav link — preserves Streamlit WebSocket session
    const links = document.querySelectorAll(
        '[data-testid="stSidebarNav"] a, [data-testid="stSidebarNavItems"] a'
    );
    const target = pageName.toLowerCase().replace(/_/g, ' ');

    for (const link of links) {
        const href = (link.getAttribute('href') || '').toLowerCase();
        const text = (link.textContent || '').toLowerCase().trim();
        if (href.includes(pageName.toLowerCase()) || text.includes(target)) {
            link.click();
            return;
        }
    }

    // Fallback: use history.pushState so the browser doesn't do a hard reload
    // This still uses Streamlit's frontend router
    const path = '/' + pageName;
    window.history.pushState({}, '', path);
    window.dispatchEvent(new PopStateEvent('popstate', { state: {} }));
}
</script>
"""


def render_bottom_nav():
    if not st.session_state.get("token"):
        return
    st.markdown(_NAV_CSS + _NAV_HTML, unsafe_allow_html=True)
