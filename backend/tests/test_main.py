from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_health():
    r=client.get("/health")
    assert r.status_code==200 and r.json()=={"status":"ok"}

def test_versioned_analysis():
    r=client.post("/api/v1/analyze",json={"resume_text":"Python FastAPI PostgreSQL Git Education Experience Projects Skills "+"x "*40,"job_description":"Python FastAPI PostgreSQL Docker Git"})
    assert r.status_code==200
    data=r.json()
    assert 0<=data["match_score"]<=100
    assert "docker" in data["missing_skills"]

def test_root():
    assert client.get("/").status_code==200
