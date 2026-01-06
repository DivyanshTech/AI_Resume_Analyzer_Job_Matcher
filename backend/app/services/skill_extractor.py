# skill_extractor.py
import re
from typing import List

# Example list of common skills
COMMON_SKILLS = [
    "Python", "Java", "C++", "FastAPI", "Django", "Flask", 
    "PostgreSQL", "MySQL", "Docker", "Kubernetes", "AWS", 
    "Git", "REST", "SQL", "HTML", "CSS", "JavaScript"
]

def extract_skills_from_job_description(job_description: str) -> List[str]:
    """
    Extract skills from job description using simple keyword matching.
    """
    job_description_lower = job_description.lower()
    matched_skills = []

    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', job_description_lower):
            matched_skills.append(skill)

    return matched_skills
