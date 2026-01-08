// Response after uploading a resume
export interface ResumeUploadResponse {
  id: number;
  filename: string;
  message: string;
  // extracted_text removed: backend does not return it
}

// Response for skills extraction
export interface SkillsResponse {
  resume_id: number;       // matches backend
  skills: string[];
}

// Request to match resume with a job
export interface MatchRequest {
  resumeId: number;        // frontend state uses camelCase
  job_description: string;
}

// Response after matching resume with job
export interface MatchResponse {
  match_percentage: number;
  matched_skills: string[];
  missing_skills: string[];
  explanation: string;
}
