from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "sports-partner"


def test_api_ping():
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json()["message"] == "pong"
