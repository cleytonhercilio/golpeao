import streamlit as st
import streamlit.components.v1 as components


def render_bottom_nav():
    if not st.session_state.get("token"):
        return

    token = st.session_state.token

    # Injeta o nav diretamente no document.body via iframe (window.parent.document)
    # Isso escapa do contexto de posicionamento do Streamlit e garante position:fixed real
    html = f"""
<!DOCTYPE html><html><body>
<script>
(function() {{
    var parent = window.parent;
    var doc = parent.document;

    // Evita duplicação
    var old = doc.getElementById('gp-bottom-nav');
    if (old) old.remove();

    var oldStyle = doc.getElementById('gp-nav-style');
    if (oldStyle) oldStyle.remove();

    // Estilo global
    var style = doc.createElement('style');
    style.id = 'gp-nav-style';
    style.textContent = [
        '#gp-bottom-nav {{',
        '  position: fixed !important;',
        '  bottom: 0 !important;',
        '  left: 0 !important;',
        '  right: 0 !important;',
        '  height: 62px;',
        '  background: linear-gradient(180deg,#0D2540ee,#1A3A5Cee);',
        '  border-top: 2px solid rgba(255,215,0,0.35);',
        '  display: none;',
        '  align-items: center;',
        '  justify-content: space-around;',
        '  z-index: 2147483647;',
        '  padding-bottom: env(safe-area-inset-bottom);',
        '  backdrop-filter: blur(8px);',
        '  -webkit-backdrop-filter: blur(8px);',
        '}}',
        '@media (max-width: 768px) {{',
        '  #gp-bottom-nav {{ display: flex !important; }}',
        '  [data-testid="stMainBlockContainer"] {{ padding-bottom: 80px !important; }}',
        '  [data-testid="stSidebarToggleButton"] {{ display: none !important; }}',
        '}}'
    ].join('');
    doc.head.appendChild(style);

    // Cria o nav
    var nav = doc.createElement('nav');
    nav.id = 'gp-bottom-nav';

    var pages = [
        ['Inicio',        '🏠', 'Início'],
        ['Jogos',         '⚽', 'Jogos'],
        ['Meus_Palpites', '🎯', 'Palpites'],
        ['Ranking',       '🏆', 'Ranking'],
        ['Conquistas',    '🏅', 'Badges']
    ];

    var linkStyle = [
        'display:flex',
        'flex-direction:column',
        'align-items:center',
        'text-decoration:none',
        'color:rgba(255,255,255,0.6)',
        'font-size:9px',
        'font-family:Nunito,sans-serif',
        'font-weight:800',
        'gap:1px',
        'padding:6px 10px',
        'border-radius:12px',
        'min-width:48px',
        '-webkit-tap-highlight-color:transparent'
    ].join(';');

    pages.forEach(function(p) {{
        var a = doc.createElement('a');
        a.href = '/' + p[0] + '?_st=' + encodeURIComponent('{token}');
        a.setAttribute('style', linkStyle);
        a.innerHTML =
            '<span style="font-size:22px;line-height:1.1;display:block">' + p[1] + '</span>' +
            '<span style="font-size:9px">' + p[2] + '</span>';
        nav.appendChild(a);
    }});

    doc.body.appendChild(nav);
}})();
</script>
</body></html>
"""

    components.html(html, height=0)
