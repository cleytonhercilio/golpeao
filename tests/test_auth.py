import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base
from app.dependencies import get_db


@pytest.fixture(scope="function")
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def test_register_user(client):
    r = client.post("/auth/register", json={
        "username": "joao", "email": "joao@test.com",
        "password": "senha123", "display_name": "João"
    })
    assert r.status_code == 201
    data = r.json()
    assert data["username"] == "joao"
    assert "password_hash" not in data


def test_register_duplicate_username(client):
    payload = {"username": "joao", "email": "joao@test.com", "password": "senha123", "display_name": "João"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/register", json={**payload, "email": "outro@test.com"})
    assert r.status_code == 400


def test_register_duplicate_email(client):
    client.post("/auth/register", json={"username": "joao", "email": "joao@test.com", "password": "senha123", "display_name": "João"})
    r = client.post("/auth/register", json={"username": "maria", "email": "joao@test.com", "password": "senha123", "display_name": "Maria"})
    assert r.status_code == 400


def test_login(client):
    client.post("/auth/register", json={
        "username": "joao", "email": "joao@test.com",
        "password": "senha123", "display_name": "João"
    })
    r = client.post("/auth/login", json={"username": "joao", "password": "senha123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "username": "joao", "email": "joao@test.com",
        "password": "senha123", "display_name": "João"
    })
    r = client.post("/auth/login", json={"username": "joao", "password": "errada"})
    assert r.status_code == 401


def test_me(client):
    client.post("/auth/register", json={
        "username": "joao", "email": "joao@test.com",
        "password": "senha123", "display_name": "João"
    })
    token = client.post("/auth/login", json={"username": "joao", "password": "senha123"}).json()["access_token"]
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["username"] == "joao"


def test_me_no_token(client):
    r = client.get("/auth/me")
    assert r.status_code == 401
