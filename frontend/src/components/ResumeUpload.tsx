import React, { useState } from 'react';
import { Upload, FileText, Loader2 } from 'lucide-react';
import { uploadResume } from '../services/api';

interface Props {
  onUploadSuccess: (resumeId: number, filename: string) => void;
}

export const ResumeUpload: React.FC<Props> = ({ onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (!selected) return;

    if (!selected.name.endsWith('.pdf')) {
      setError('Only PDF files are allowed');
      return;
    }

    setFile(selected);
    setError('');
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError('');

    try {
      const res = await uploadResume(file);
      onUploadSuccess(res.id, res.filename);
    } catch (err: any) {
      setError(
        err?.response?.data ||
        err?.message ||
        'Upload failed'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>📄 Upload Resume</h2>

      <div className="upload-box">
        <input
          type="file"
          accept=".pdf"
          id="file-input"
          onChange={handleFileChange}
          disabled={loading}
          hidden
        />

        <label htmlFor="file-input" className="file-label">
          <Upload size={40} />
          <p>{file ? file.name : 'Choose PDF file'}</p>
        </label>
      </div>

      {file && (
        <button onClick={handleUpload} disabled={loading} className="btn-primary">
          {loading ? <Loader2 className="spinner" /> : <FileText size={20} />}
          {loading ? 'Uploading...' : 'Upload & Extract Skills'}
        </button>
      )}

      {error && <div className="error">{error}</div>}
    </div>
  );
};
