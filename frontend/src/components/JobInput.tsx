import React, { useState } from 'react';
import { Briefcase, Loader2 } from 'lucide-react';

interface Props {
  onMatch: (jobDescription: string) => void;
  loading: boolean;
}

export const JobInput: React.FC<Props> = ({ onMatch, loading }) => {
  const [jobDesc, setJobDesc] = useState('');

  const handleSubmit = () => {
    if (jobDesc.trim()) onMatch(jobDesc);
  };

  return (
    <div className="job-input-container">
      <h2>💼 Job Description</h2>

      <textarea
        placeholder="Paste the job description here..."
        value={jobDesc}
        onChange={(e) => setJobDesc(e.target.value)}
        rows={8}
        disabled={loading}
        className="job-textarea"
      />

      <button
        onClick={handleSubmit}
        disabled={!jobDesc.trim() || loading}
        className="btn-primary"
      >
        {loading ? <Loader2 className="spinner" /> : <Briefcase size={20} />}
        {loading ? 'Analyzing...' : 'Find Match'}
      </button>
    </div>
  );
};
