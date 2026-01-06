# backend/app/api/routes.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import shutil
from typing import List

from ..database import get_db
from ..models.resume import Resume
from ..schemas.resume import ResumeUploadResponse, MatchRequest, MatchResponse
from ..services.pdf_extractor import extract_text_from_pdf
from ..services.skill_extractor import extract_skills_from_job_description
from ..services.embeddings import embedding_service
from ..services.matcher import calculate_match_score, generate_match_explanation
from ..utils.faiss_store import faiss_store

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------------------
# 1. Upload Resume
# ------------------------
@router.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        extracted_text = extract_text_from_pdf(file_path)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))
    
    resume = Resume(
        filename=file.filename,
        extracted_text=extracted_text
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    os.remove(file_path)
    
    return ResumeUploadResponse(
        id=resume.id,
        filename=resume.filename,
        extracted_text=extracted_text[:500] + "...",
        message="Resume uploaded successfully"
    )

# ------------------------
# 2. Extract Skills
# ------------------------
@router.post("/extract-skills/{resume_id}")
async def extract_skills(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    try:
        skills = extract_skills_from_job_description(resume.extracted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    resume.skills = skills
    db.commit()
    db.refresh(resume)
    
    return {
        "resume_id": resume.id,
        "skills": skills,
        "message": "Skills extracted successfully"
    }

# ------------------------
# 3. Match Resume with Job  ✅ FIXED
# ------------------------
@router.post("/match", response_model=MatchResponse)
async def match_resume_with_job(
    request: MatchRequest,
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if not resume.skills:
        raise HTTPException(status_code=400, detail="Extract skills first")

    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    # extract JD skills
    job_skills = extract_skills_from_job_description(request.job_description)

    # generate embedding (NO DB storage – FAISS only)
    try:
        resume_embedding = embedding_service.generate_embedding(resume.extracted_text)
        faiss_store.add_embedding(resume.id, resume_embedding)

        # store only reference
        resume.embedding_id = str(resume.id)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding error: {str(e)}")

    # calculate match
    match_result = calculate_match_score(
        resume_text=resume.extracted_text,
        resume_skills=resume.skills,
        job_description=request.job_description,
        job_skills=job_skills
    )

    explanation = generate_match_explanation(
        match_percentage=match_result["match_percentage"],
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"]
    )

    return MatchResponse(
        match_percentage=match_result["match_percentage"],
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"],
        explanation=explanation
    )
