import React from 'react';
import { CheckCircle } from 'lucide-react';

interface Props {
  skills: string[];
}

export const SkillsList: React.FC<Props> = ({ skills }) => {
  return (
    <div className="skills-container">
      <h3>✅ Extracted Skills ({skills.length})</h3>
      <div className="skills-grid">
        {skills.map((skill, idx) => (
          <div key={idx} className="skill-chip">
            <CheckCircle size={16} />
            <span>{skill}</span>
          </div>
        ))}
      </div>
    </div>
  );
};