import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from frontend.api_client import get_my_groups, get_matches, get_predictions, create_prediction, update_prediction

_css = os.path.join(os.path.dirname(os.path.dirname(__file__)), "style.css")
if os.path.exists(_css):
    with open(_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("token"):
    st.warning("⚠️ Faça login primeiro.")
    st.stop()

st.markdown("<h1>🎯 Meus Palpites</h1>", unsafe_allow_html=True)

groups = get_my_groups()
if not groups:
    st.info("Entre em um bolão primeiro! Acesse **Ranking** para criar ou entrar.")
    st.stop()

group_map = {g["id"]: g["name"] for g in groups}
sel_group_id = st.selectbox("Bolão", list(group_map.keys()), format_func=lambda x: group_map[x])

STAGES = {
    "group": "Fase de Grupos", "round32": "Oitavas (R32)", "round16": "Round of 16",
    "qf": "Quartas de Final", "sf": "Semifinais", "third": "3º Lugar", "final": "Final",
}
stage = st.selectbox("Fase", list(STAGES.keys()), format_func=lambda x: STAGES[x])

matches = get_matches(stage=stage)
my_preds = get_predictions(bolao_group_id=sel_group_id)
pred_map = {p["match_id"]: p for p in my_preds}

st.markdown("---")

for m in matches:
    home = m.get("home_team") or {}
    away = m.get("away_team") or {}
    home_iso = home.get("iso_code", "xx")
    away_iso = away.get("iso_code", "xx")
    home_name = home.get("name", m.get("match_label", "A definir"))
    away_name = away.get("name", "A definir")
    sched = m.get("scheduled_at", "")[:16].replace("T", " ")
    existing = pred_map.get(m["id"])
    lock_icon = "🔒" if m.get("is_locked") else ("✅" if m.get("is_played") else "🟢")

    with st.expander(f"{lock_icon} Jogo #{m['match_number']} — {home_name} vs {away_name} | {sched}", expanded=False):
        if m.get("is_played"):
            st.success(f"Resultado: **{m['home_score']} × {m['away_score']}**")
            if existing:
                pts = existing.get("points_earned", 0)
                exact = "🎯 Exato!" if existing.get("is_exact") else ("✅ Vencedor" if existing.get("is_winner_correct") else "❌ Miss")
                st.info(f"Seu palpite: {existing['home_score']} × {existing['away_score']} — **{pts} pts** {exact}")
        elif m.get("is_locked"):
            if existing:
                st.info(f"Palpite registrado: **{existing['home_score']} × {existing['away_score']}**")
            else:
                st.warning("Palpites fechados — sem palpite registrado.")
        else:
            h_val = existing["home_score"] if existing else 0
            a_val = existing["away_score"] if existing else 0
            c1, c2, c3, c4, c5 = st.columns([3, 2, 1, 2, 3])
            with c1:
                st.markdown(
                    f'<div style="text-align:center">'
                    f'<img src="https://flagcdn.com/64x48/{home_iso}.png" class="flag-img">'
                    f'<br><b>{home_name}</b></div>',
                    unsafe_allow_html=True,
                )
            with c2:
                h = st.number_input(
                    home_name, 0, 20, h_val,
                    key=f"h_{m['id']}_{sel_group_id}",
                    label_visibility="collapsed",
                )
            with c3:
                st.markdown(
                    "<div style='text-align:center;font-size:1.8em;"
                    "font-weight:900;padding-top:4px'>×</div>",
                    unsafe_allow_html=True,
                )
            with c4:
                a = st.number_input(
                    away_name, 0, 20, a_val,
                    key=f"a_{m['id']}_{sel_group_id}",
                    label_visibility="collapsed",
                )
            with c5:
                st.markdown(
                    f'<div style="text-align:center">'
                    f'<img src="https://flagcdn.com/64x48/{away_iso}.png" class="flag-img">'
                    f'<br><b>{away_name}</b></div>',
                    unsafe_allow_html=True,
                )

            if existing:
                if st.button("✏️ Atualizar Palpite", key=f"upd_{m['id']}_{sel_group_id}"):
                    resp, code = update_prediction(existing["id"], m["id"], sel_group_id, h, a)
                    if code == 200:
                        st.success("✅ Palpite atualizado!")
                        st.rerun()
                    else:
                        st.error(f"❌ {resp.get('detail', 'Erro')}")
            else:
                if st.button("💾 Salvar Palpite", key=f"save_{m['id']}_{sel_group_id}"):
                    resp, code = create_prediction(m["id"], sel_group_id, h, a)
                    if code == 201:
                        st.success("✅ Palpite salvo!")
                        st.rerun()
                    else:
                        st.error(f"❌ {resp.get('detail', 'Erro')}")
