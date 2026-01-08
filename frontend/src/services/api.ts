import axios from 'axios';
import {
  ResumeUploadResponse,
  SkillsResponse,
  MatchRequest,
  MatchResponse,
} from '../types';

const API_BASE = 'http://localhost:8000/api';

// ❌ Do NOT force Content-Type globally
const apiClient = axios.create({
  baseURL: API_BASE,
});

// 1️⃣ Upload resume (FormData + trailing slash)
export const uploadResume = async (
  file: File
): Promise<ResumeUploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(
    `${API_BASE}/upload-resume/`,
    formData
  );

  return response.data;
};

// 2️⃣ Extract skills (POST request)
export const extractSkills = async (
  resumeId: number
): Promise<SkillsResponse> => {
  const response = await apiClient.post(
    `/extract-skills/${resumeId}/`
  );
  return response.data;
};

// 3️⃣ Match resume with job (payload mapped to backend)
export const matchResumeWithJob = async (
  data: MatchRequest
): Promise<MatchResponse> => {
  const payload = {
    resume_id: data.resumeId,       // map resumeId -> resume_id
    job_description: data.job_description,
  };

  const response = await apiClient.post('/match', payload);
  return response.data;
};
