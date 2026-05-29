import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.api_client import get_matches, set_match_result, get_pending_results

_css = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
if os.path.exists(_css):
    with open(_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

user = st.session_state.user or {}
if not user.get("is_admin"):
    st.error("⛔ Acesso restrito a administradores.")
    st.stop()

st.markdown("<h1>⚙️ Painel Admin</h1>", unsafe_allow_html=True)
st.warning("⚠️ Área restrita. Os resultados inseridos recalculam todos os palpites automaticamente.")

STAGES = {
    "group": "Fase de Grupos", "round32": "Oitavas (R32)", "round16": "Round of 16",
    "qf": "Quartas", "sf": "Semifinais", "third": "3º Lugar", "final": "Final",
}
stage = st.selectbox("Fase", list(STAGES.keys()), format_func=lambda x: STAGES[x])
matches = get_matches(stage=stage)
unplayed = [m for m in matches if not m.get("is_played")]

if not unplayed:
    st.success("✅ Todos os jogos desta fase já têm resultado!")
else:
    st.markdown(f"**{len(unplayed)} jogo(s) sem resultado:**")
    for m in unplayed:
        home = m.get("home_team") or {}
        away = m.get("away_team") or {}
        home_name = home.get("name", m.get("match_label", "A definir"))
        away_name = away.get("name", "A definir")
        sched = m.get("scheduled_at", "")[:16].replace("T", " ")

        with st.expander(f"Jogo #{m['match_number']} — {home_name} vs {away_name} | {sched}"):
            col1, col2, col3 = st.columns([2, 1, 2])
            col1.markdown(f"**{home_name}**")
            h = col1.number_input("Gols Casa", 0, 20, 0, key=f"ah_{m['id']}")
            col2.markdown("<div style='text-align:center;padding-top:28px;font-size:1.5em'>×</div>", unsafe_allow_html=True)
            col3.markdown(f"**{away_name}**")
            a = col3.number_input("Gols Fora", 0, 20, 0, key=f"aa_{m['id']}")

            if st.button(f"✅ Registrar Resultado", key=f"res_{m['id']}"):
                data, code = set_match_result(m["id"], h, a)
                if code == 200:
                    st.success(f"✅ {data.get('message', 'Resultado registrado!')}")
                    st.rerun()
                else:
                    st.error(f"❌ {data.get('detail', 'Erro ao registrar')}")
