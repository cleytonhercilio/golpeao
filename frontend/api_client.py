import requests
import streamlit as st

API_BASE = "http://localhost:8000"


def _headers() -> dict:
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def register(username: str, email: str, password: str, display_name: str, avatar_emoji: str = "⚽"):
    r = requests.post(f"{API_BASE}/auth/register", json={
        "username": username, "email": email, "password": password,
        "display_name": display_name, "avatar_emoji": avatar_emoji,
    }, timeout=10)
    return r.json(), r.status_code


def login(username: str, password: str):
    r = requests.post(f"{API_BASE}/auth/login", json={"username": username, "password": password}, timeout=10)
    if r.status_code == 200:
        return r.json()["access_token"], None
    return None, r.json().get("detail", "Erro ao fazer login")


def me() -> dict:
    r = requests.get(f"{API_BASE}/auth/me", headers=_headers(), timeout=10)
    return r.json() if r.status_code == 200 else None


def get_matches(stage: str = None, group: str = None) -> list:
    params = {}
    if stage:
        params["stage"] = stage
    if group:
        params["group"] = group
    r = requests.get(f"{API_BASE}/matches/", params=params, headers=_headers(), timeout=10)
    return r.json() if r.status_code == 200 else []


def get_upcoming() -> list:
    r = requests.get(f"{API_BASE}/matches/upcoming", headers=_headers(), timeout=10)
    return r.json() if r.status_code == 200 else []


def get_predictions(bolao_group_id: int = None, match_id: int = None) -> list:
    params = {}
    if bolao_group_id:
        params["bolao_group_id"] = bolao_group_id
    if match_id:
        params["match_id"] = match_id
    r = requests.get(f"{API_BASE}/predictions/", params=params, headers=_headers(), timeout=10)
    return r.json() if r.status_code == 200 else []


def create_prediction(match_id: int, bolao_group_id: int, home_score: int, away_score: int, predicted_winner_id: int = None):
    r = requests.post(f"{API_BASE}/predictions/", json={
        "match_id": match_id, "bolao_group_id": bolao_group_id,
        "home_score": home_score, "away_score": away_score,
        "predicted_winner_id": predicted_winner_id,
    }, headers=_headers(), timeout=10)
    return r.json(), r.status_code


def update_prediction(pred_id: int, match_id: int, bolao_group_id: int, home_score: int, away_score: int):
    r = requests.put(f"{API_BASE}/predictions/{pred_id}", json={
        "match_id": match_id, "bolao_group_id": bolao_group_id,
        "home_score": home_score, "away_score": away_score,
    }, headers=_headers(), timeout=10)
    return r.json(), r.status_code


def get_my_groups() -> list:
    r = requests.get(f"{API_BASE}/groups/", headers=_headers(), timeout=10)
    return r.json() if r.status_code == 200 else []


def create_group(name: str):
    r = requests.post(f"{API_BASE}/groups/", json={"name": name}, headers=_headers(), timeout=10)
    return r.json(), r.status_code


def join_group(invite_code: str):
    r = requests.post(f"{API_BASE}/groups/join", params={"invite_code": invite_code}, headers=_headers(), timeout=10)
    return r.json(), r.status_code


def get_ranking(group_id: int) -> dict:
    r = requests.get(f"{API_BASE}/ranking/{group_id}", headers=_headers(), timeout=10)
    return r.json() if r.status_code == 200 else None


def set_match_result(match_id: int, home_score: int, away_score: int):
    r = requests.post(f"{API_BASE}/admin/matches/{match_id}/result",
                      json={"home_score": home_score, "away_score": away_score},
                      headers=_headers(), timeout=10)
    return r.json(), r.status_code


def get_pending_results() -> list:
    r = requests.get(f"{API_BASE}/admin/matches/pending-results", headers=_headers(), timeout=10)
    return r.json() if r.status_code == 200 else []
