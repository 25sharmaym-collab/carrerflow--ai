from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.routes.health import router as health_router
from app.api.routes.analysis import router as analysis_router
from app.api.routes.resumes import router as resumes_router

Base.metadata.create_all(bind=engine)
app=FastAPI(title="CareerFlow AI API",version="1.0.0",description="Resume parsing, ATS checks and job matching API")
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(health_router)
app.include_router(analysis_router)
app.include_router(resumes_router)

@app.get("/")
def root(): return {"name":"CareerFlow AI API","version":"1.0.0","docs":"/docs"}
