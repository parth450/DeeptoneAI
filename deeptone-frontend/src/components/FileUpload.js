'use client';

import { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Cell,
} from 'recharts';

export default function FileUpload({ username, refreshHistory, onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [resultData, setResultData] = useState(null);
  const [previewURL, setPreviewURL] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.size <= 100 * 1024 * 1024) {
      setFile(selected);
      setPreviewURL(URL.createObjectURL(selected));
    } else {
      alert('File is too large. Max size is 100MB.');
    }
  };

  const handleAnalyze = async () => {
    if (!file) return alert('Please choose a file.');
    if (!username) return alert('User not logged in.');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('username', username);

    setLoading(true);
    setResultData(null);

    try {
      const res = await fetch('https://deeptoneai.onrender.com/predict', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Status ${res.status} – ${text}`);
      }

      const data = await res.json();
      setResultData(data);

      if (refreshHistory) refreshHistory();
      if (onUploadComplete) onUploadComplete(data);

    } catch (err) {
      console.error('Analyze Error:', err);
      alert('⚠️ Failed to analyze audio. Backend may be asleep or not reachable. Please try again in 30–60 seconds.');
    } finally {
      setLoading(false);
    }
  };

  const chartData = resultData ? [
    { metric: 'Accuracy', value: resultData.accuracy, fill: 'orange' },
    { metric: 'Recall', value: resultData.recall, fill: 'blue' },
    { metric: 'Precision', value: resultData.precision, fill: 'yellow' },
    { metric: 'F1 Score', value: resultData.f1_score, fill: 'red' },
  ] : [];

  return (
    <div
      className="flex flex-col items-center p-8 rounded-lg shadow-xl w-full max-w-2xl mx-auto text-white"
      style={{ backgroundColor: '#0f172a' }}
    >
      <label className="border-2 border-dashed border-teal-400 p-6 w-full text-center rounded-md text-white cursor-pointer mb-4 hover:bg-slate-800 transition">
        Choose Audio
        <input
          type="file"
          accept=".wav,.mp3,.m4a"
          className="hidden"
          onChange={handleFileChange}
        />
      </label>

      {previewURL && (
        <audio className="mb-4" controls src={previewURL}></audio>
      )}

      <button
        onClick={handleAnalyze}
        disabled={!file || loading}
        className="bg-teal-400 text-slate-900 font-semibold px-6 py-2 rounded-md hover:bg-teal-300 transition disabled:opacity-50"
      >
        {loading ? 'Analyzing...' : 'Analyze Audio'}
      </button>

      <p className="text-sm text-gray-300 mt-2">
        Supported formats: WAV, MP3, M4A (Max size: 100MB)
      </p>

      {resultData && (
        <div className="mt-6 w-full bg-slate-800 p-6 rounded text-left text-white">
          <h3 className="text-xl font-bold text-teal-300 mb-4 text-center">Analysis Result</h3>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <p><strong>Prediction:</strong> {resultData.prediction}</p>
            <p><strong>File:</strong> {resultData.filename}</p>
            <p><strong>Accuracy:</strong> {resultData.accuracy}</p>
            <p><strong>Recall:</strong> {resultData.recall}</p>
            <p><strong>Precision:</strong> {resultData.precision}</p>
            <p><strong>F1 Score:</strong> {resultData.f1_score}</p>
          </div>

          <div className="mt-6 w-full" style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="metric" stroke="#e2e8f0" />
                <YAxis domain={[0, 1]} stroke="#e2e8f0" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f1f5f9' }}
                />
                <Bar dataKey="value" name="Metric">
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}
