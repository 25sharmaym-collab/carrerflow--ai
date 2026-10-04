from app.services.skills import extract_skills
from app.services.matcher import analyze
from app.services.ats import ats_check

def test_skill_aliases():
    assert "javascript" in extract_skills("Experienced in JS and ReactJS")

def test_matcher_weighted_result():
    result=analyze("Python FastAPI PostgreSQL Git\nEducation\nProjects\nSkills\nExperience", "Required: Python FastAPI PostgreSQL Docker Git")
    assert result["match_score"] > 50
    assert "docker" in result["missing_skills"]

def test_ats():
    score,warnings=ats_check("Education\nExperience\nProjects\nSkills\n"+"python "*160,{"python"})
    assert score > 0
    assert isinstance(warnings,list)
