from fastapi import APIRouter,File,UploadFile,HTTPException,Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models import Resume
from app.db.session import get_db
from app.services.parser import extract_text,sections
router=APIRouter(prefix="/api/v1/resumes",tags=["resumes"])

@router.post("")
async def upload_resume(file:UploadFile=File(...),db:Session=Depends(get_db)):
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024: raise HTTPException(413,"File is too large.")
    try: text=extract_text(file.filename or "resume.txt",data)
    except ValueError as e: raise HTTPException(400,str(e))
    row=Resume(filename=file.filename or "resume",text=text); db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id,"filename":row.filename,"characters":len(text),"sections":sections(text)}

@router.get("/{resume_id}")
def get_resume(resume_id:int,db:Session=Depends(get_db)):
    row=db.get(Resume,resume_id)
    if not row: raise HTTPException(404,"Resume not found")
    return {"id":row.id,"filename":row.filename,"text":row.text,"sections":sections(row.text),"created_at":row.created_at}
