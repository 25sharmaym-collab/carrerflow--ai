from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    resume_text: str = Field(min_length=20, max_length=100000)
    job_description: str = Field(min_length=20, max_length=50000)

class AnalysisResult(BaseModel):
    match_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    preferred_matches: list[str]
    ats_score: int
    ats_warnings: list[str]
    suggestions: list[str]
    interview_questions: list[str]

class AnalyzeResponse(AnalysisResult):
    analysis_id: int | None = None
    provider: str = "rule_based"
