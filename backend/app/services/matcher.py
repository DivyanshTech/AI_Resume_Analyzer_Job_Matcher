# backend/app/services/matcher.py

import numpy as np
from typing import List, Dict
from .embeddings import embedding_service
from ..utils.faiss_store import faiss_store

def calculate_match_score(
    resume_text: str,
    resume_skills: List[str],
    job_description: str,
    job_skills: List[str]
) -> Dict:
    """
    Calculate semantic match between resume and job description
    Returns: {
        "match_percentage": float,
        "semantic_score": float,
        "skill_overlap_score": float,
        "matched_skills": list,
        "missing_skills": list
    }
    """
    
    # 1. Generate embeddings
    resume_embedding = embedding_service.generate_embedding(resume_text)
    job_embedding = embedding_service.generate_embedding(job_description)
    
    # 2. Compute semantic similarity (60% weight)
    semantic_similarity = embedding_service.compute_similarity(
        resume_embedding, 
        job_embedding
    )
    
    # 3. Compute skill overlap (40% weight)
    resume_skills_lower = [s.lower() for s in resume_skills]
    job_skills_lower = [s.lower() for s in job_skills]
    
    matched_skills = []
    missing_skills = []
    
    for job_skill in job_skills:
        job_skill_lower = job_skill.lower()
        # Exact match or partial match
        if any(job_skill_lower in resume_skill or resume_skill in job_skill_lower 
               for resume_skill in resume_skills_lower):
            matched_skills.append(job_skill)
        else:
            missing_skills.append(job_skill)
    
    # Calculate skill overlap percentage
    if len(job_skills) > 0:
        skill_overlap_score = len(matched_skills) / len(job_skills)
    else:
        skill_overlap_score = 0.0
    
    # 4. Combined score (weighted average)
    match_percentage = (semantic_similarity * 0.6 + skill_overlap_score * 0.4) * 100
    
    return {
        "match_percentage": round(match_percentage, 2),
        "semantic_score": round(semantic_similarity * 100, 2),
        "skill_overlap_score": round(skill_overlap_score * 100, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }


def generate_match_explanation(
    match_percentage: float,
    matched_skills: List[str],
    missing_skills: List[str]
) -> str:
    """
    Generate professional, human-readable explanation locally (free)
    """
    if match_percentage >= 75:
        return (
            f"Strong match ({match_percentage}%). "
            f"Your skills align well with the job requirements. "
            f"Matched {len(matched_skills)} key skills."
        )
    elif match_percentage >= 50:
        return (
            f"Moderate match ({match_percentage}%). "
            f"You have {len(matched_skills)} matching skills. "
            f"Consider developing: {', '.join(missing_skills[:3])}."
        )
    else:
        return (
            f"Low match ({match_percentage}%). "
            f"Focus on acquiring these critical skills: {', '.join(missing_skills[:5])}."
        )
