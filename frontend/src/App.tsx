import React, { useState } from 'react';
import { ResumeUpload } from './components/ResumeUpload';
import { SkillsList } from './components/SkillsList';
import { JobInput } from './components/JobInput';
import { MatchResults } from './components/MatchResults';
import { extractSkills, matchResumeWithJob } from './services/api';
import { MatchResponse } from './types';
import './App.css';

function App() {
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [filename, setFilename] = useState('');
  const [skills, setSkills] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [matchResult, setMatchResult] = useState<MatchResponse | null>(null);
  const [step, setStep] = useState<'upload' | 'skills' | 'match'>('upload');

  const handleUploadSuccess = async (id: number, name: string) => {
    setResumeId(id);
    setFilename(name);
    setLoading(true);

    try {
      const res = await extractSkills(id);
      setSkills(res.skills);
      setStep('skills');
    } finally {
      setLoading(false);
    }
  };

  const handleMatch = async (jobDescription: string) => {
    if (!resumeId) return;

    setLoading(true);
    setMatchResult(null);

    try {
      const res = await matchResumeWithJob({
        resumeId,
        job_description: jobDescription,
      });
      setMatchResult(res);
      setStep('match');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResumeId(null);
    setFilename('');
    setSkills([]);
    setMatchResult(null);
    setStep('upload');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1> AI Resume Analyzer</h1>
        <p>Semantic matching powered by ML</p>
      </header>

      <main className="app-main">
        {step === 'upload' && (
          <ResumeUpload onUploadSuccess={handleUploadSuccess} />
        )}

        {step === 'skills' && (
          <div className="two-column">
            <div>
              <div className="resume-info">
                <strong>📎 Resume:</strong> {filename}
              </div>
              <SkillsList skills={skills} />
            </div>
            <JobInput onMatch={handleMatch} loading={loading} />
          </div>
        )}

        {step === 'match' && matchResult && (
          <>
            <MatchResults result={matchResult} />
            <button onClick={reset} className="btn-secondary">
              🔄 Analyze Another Resume
            </button>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
