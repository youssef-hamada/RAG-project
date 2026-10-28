from fastapi.testclient import TestClient
from src.app.api import app

client = TestClient(app)


def test_health_returns_200():
    r = client.get("/health")
    assert r.status_code == 200
    assert "status" in r.json()


def test_chat_requires_question():
    r = client.post("/chat", json={})
    assert r.status_code == 422