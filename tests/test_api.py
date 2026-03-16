from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_logs_endpoint():
    response = client.get("/logs?filename=log1.txt&limit=2")
    assert response.status_code == 200
    assert "entries" in response.json()


def test_logs_keyword():
    response = client.get("/logs?filename=apache/log3.txt&keyword=404")
    assert response.status_code == 200
