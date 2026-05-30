import streamlit as st
from frontend.api_client import me


def restore_session():
    """Restaura sessão do parâmetro de URL passado pela navegação mobile."""
    if st.session_state.get("token"):
        return

    url_token = st.query_params.get("_st")
    if not url_token:
        return

    st.session_state.token = url_token
    user = me()
    if user:
        st.session_state.user = user
        try:
            del st.query_params["_st"]
        except Exception:
            pass
    else:
        st.session_state.token = None
