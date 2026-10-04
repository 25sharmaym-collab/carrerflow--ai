from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analysis():
    response = client.post("/api/analyze", json={
        "resume_text": "Python FastAPI PostgreSQL Git",
        "job_description": "Python FastAPI PostgreSQL Docker Git"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["match_score"] == 80
    assert "docker" in data["missing_skills"]
