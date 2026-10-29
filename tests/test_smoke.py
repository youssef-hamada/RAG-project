"""Minimal smoke tests that run in CI without an index or an API key."""
from fastapi.testclient import TestClient
from src.app.api import app
from src.config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K

client = TestClient(app)


def test_health_endpoint_returns_json():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert "status" in body


def test_chat_validation_rejects_empty():
    r = client.post("/chat", json={"question": ""})
    assert r.status_code == 422


def test_config_constants_are_sane():
    assert CHUNK_OVERLAP < CHUNK_SIZE
    assert TOP_K >= 1