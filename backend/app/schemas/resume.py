from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ResumeUploadResponse(BaseModel):
    id: int
    filename: str
    extracted_text: str
    message: str
    
class SkillsResponse(BaseModel):
    resume_id: int
    skills: List[str]
    
class MatchRequest(BaseModel):
    resume_id: int
    job_description: str
    
class MatchResponse(BaseModel):
    match_percentage: float
    matched_skills: List[str]
    missing_skills: List[str]
    explanation: str