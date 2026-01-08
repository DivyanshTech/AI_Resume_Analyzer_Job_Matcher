import React from 'react';
import { MatchResponse } from '../types';
import { TrendingUp, CheckCircle2, XCircle } from 'lucide-react';

interface Props {
  result: MatchResponse;
}

export const MatchResults: React.FC<Props> = ({ result }) => {
  const getScoreColor = (score: number) => {
    if (score >= 75) return '#10b981'; // Green
    if (score >= 50) return '#f59e0b'; // Orange
    return '#ef4444'; // Red
  };

  return (
    <div className="results-container">
      <h2>✔ Match Analysis</h2>

      {/* Match Percentage */}
      <div className="score-card">
        <div
          className="score-circle"
          style={{ borderColor: getScoreColor(result.match_percentage) }}
        >
          <span className="score-number">{result.match_percentage}%</span>
          <TrendingUp size={24} style={{ color: getScoreColor(result.match_percentage) }} />
        </div>
        <p className="score-label">Match Score</p>
      </div>

      {/* Explanation */}
      <div className="explanation-box">
        <p>{result.explanation}</p>
      </div>

      {/* Skills Breakdown */}
      <div className="skills-breakdown">
        {/* Matched Skills */}
        {result.matched_skills.length > 0 && (
          <div className="skills-section">
            <h3>
              <CheckCircle2 size={20} color="#10b981" />
              Matched Skills ({result.matched_skills.length})
            </h3>
            <div className="skills-grid">
              {result.matched_skills.map((skill, idx) => (
                <span key={idx} className="skill-tag matched">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Missing Skills */}
        {result.missing_skills.length > 0 && (
          <div className="skills-section">
            <h3>
              <XCircle size={20} color="#ef4444" />
              Missing Skills ({result.missing_skills.length})
            </h3>
            <div className="skills-grid">
              {result.missing_skills.map((skill, idx) => (
                <span key={idx} className="skill-tag missing">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};