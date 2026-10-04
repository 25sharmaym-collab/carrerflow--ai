from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.models import Analysis
from app.db.session import get_db
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.matcher import analyze
router=APIRouter(prefix="/api/v1",tags=["analysis"])

@router.post("/analyze",response_model=AnalyzeResponse)
def create_analysis(request:AnalyzeRequest,db:Session=Depends(get_db)):
    result=analyze(request.resume_text,request.job_description)
    row=Analysis(resume_id=None,job_description=request.job_description,match_score=result["match_score"],result=result)
    # Standalone text analysis does not require a stored resume relationship.
    row.resume_id=None
    db.add(row); db.commit(); db.refresh(row)
    return AnalyzeResponse(**result,analysis_id=row.id)
