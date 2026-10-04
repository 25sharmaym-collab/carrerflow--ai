from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="CareerFlow AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=20)
    job_description: str = Field(min_length=20)

class AnalyzeResponse(BaseModel):
    match_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]

SKILL_KEYWORDS = [
    "python", "java", "c++", "javascript", "typescript", "react",
    "next.js", "node.js", "fastapi", "sql", "postgresql", "mongodb",
    "docker", "git", "github", "machine learning", "scikit-learn",
    "pandas", "numpy", "aws", "rest api"
]

def extract_skills(text: str) -> set[str]:
    normalized = text.lower()
    return {skill for skill in SKILL_KEYWORDS if skill in normalized}

def analyze(resume_text: str, job_description: str) -> AnalyzeResponse:
    resume = extract_skills(resume_text)
    required = extract_skills(job_description)
    matched = sorted(resume & required)
    missing = sorted(required - resume)
    score = round(len(matched) / len(required) * 100) if required else 0
    suggestions = [
        f"Add evidence for {skill} if you genuinely have that skill."
        for skill in missing
    ]
    if not suggestions:
        suggestions = ["Prioritize measurable project results and concrete technical evidence."]
    return AnalyzeResponse(
        match_score=score,
        matched_skills=matched,
        missing_skills=missing,
        suggestions=suggestions,
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_resume(request: AnalyzeRequest):
    return analyze(request.resume_text, request.job_description)
