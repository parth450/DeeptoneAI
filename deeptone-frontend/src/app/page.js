'use client';

import { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import Login from '../components/Login';
import Register from '../components/Register';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Cell,
} from 'recharts';

export default function Home() {
  const [showLogin, setShowLogin] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const [history, setHistory] = useState([]);
  const [selectedPrediction, setSelectedPrediction] = useState(null);

  const handleLoginSuccess = (uname) => {
    setUsername(uname);
    setIsLoggedIn(true);
    localStorage.setItem('username', uname);
    fetchHistory(uname);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername('');
    setHistory([]);
    setShowLogin(true);
    localStorage.removeItem('username');
    setSelectedPrediction(null);
  };

  const fetchHistory = async (uname) => {
    try {
      const res = await fetch(`https://deeptoneai.onrender.com/history/${uname}`);
      const data = await res.json();
      if (Array.isArray(data)) {
        setHistory(data);
      } else {
        setHistory([]);
      }
    } catch (err) {
      console.error('Error fetching history:', err);
      setHistory([]);
    }
  };

  useEffect(() => {
    const savedUsername = localStorage.getItem('username');
    if (savedUsername) {
      handleLoginSuccess(savedUsername);
    }
  }, []);

  const renderSelectedResult = () => {
    if (!selectedPrediction) return null;

    const chartData = [
      { metric: 'Accuracy', value: selectedPrediction.accuracy, fill: 'orange' },
      { metric: 'Recall', value: selectedPrediction.recall, fill: 'blue' },
      { metric: 'Precision', value: selectedPrediction.precision, fill: 'yellow' },
      { metric: 'F1 Score', value: selectedPrediction.f1_score, fill: 'red' },
    ];

    return (
      <div className="mt-10 p-6 bg-slate-800 rounded-lg shadow text-white w-full max-w-2xl">
        <h3 className="text-xl font-bold text-teal-300 mb-4 text-center">📂 Selected History Result</h3>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <p><strong>Prediction:</strong> {selectedPrediction.prediction}</p>
          <p><strong>File:</strong> {selectedPrediction.filename}</p>
          <p><strong>Accuracy:</strong> {selectedPrediction.accuracy}</p>
          <p><strong>Recall:</strong> {selectedPrediction.recall}</p>
          <p><strong>Precision:</strong> {selectedPrediction.precision}</p>
          <p><strong>F1 Score:</strong> {selectedPrediction.f1_score}</p>
        </div>

        <div className="mt-6 w-full" style={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="metric" stroke="#e2e8f0" />
              <YAxis domain={[0, 1]} stroke="#e2e8f0" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1e293b',
                  borderColor: '#334155',
                  color: '#f1f5f9'
                }}
              />
              <Bar dataKey="value" name="Metric">
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-4 text-center">
          <button
            onClick={() => setSelectedPrediction(null)}
            className="text-sm text-gray-400 hover:text-white"
          >
            Clear Result
          </button>
        </div>
      </div>
    );
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white">
      {!isLoggedIn ? (
        <div className="flex flex-col items-center justify-center min-h-screen px-4 py-10">
          <header className="text-center mb-10">
            <h1 className="text-4xl sm:text-5xl font-bold text-teal-400 mb-4">Deeptone AI</h1>
            <p className="text-lg text-gray-300 max-w-2xl mx-auto">
              Detect deepfake voice audios with cutting-edge AI. Upload your audio and receive accurate predictions.
            </p>
            <ul className="text-sm sm:text-base mt-6 text-left max-w-md mx-auto space-y-1 text-teal-100 list-disc pl-5">
              <li>🎧 Upload audio & check authenticity</li>
              <li>📊 Get prediction with accuracy, recall, precision</li>
              <li>🧠 Powered by ML & MFCC audio features</li>
              <li>🔐 Secure login & history saved</li>
            </ul>
          </header>

          <div className="bg-gray-800 p-6 rounded-xl shadow-xl w-full max-w-sm mx-auto">
            {showLogin ? (
              <>
                <h2 className="text-xl mb-4 text-center">Login</h2>
                <Login onSwitch={() => setShowLogin(false)} onLoginSuccess={handleLoginSuccess} />
              </>
            ) : (
              <>
                <h2 className="text-xl mb-4 text-center">Register</h2>
                <Register onSwitch={() => setShowLogin(true)} onLoginSuccess={handleLoginSuccess} />
              </>
            )}
          </div>
        </div>
      ) : (
        <div className="flex min-h-screen">
          {/* Sidebar - History */}
          <aside className="w-64 bg-slate-900 p-6 border-r border-gray-700">
            <h2 className="text-xl font-semibold text-teal-300 mb-4">📁 History</h2>
            <ul className="text-gray-300 space-y-4 text-sm overflow-y-auto max-h-screen pr-2">
              {history.length === 0 ? (
                <li>No history yet</li>
              ) : (
                history.map((item) => (
                  <li
                    key={item._id}
                    onClick={() => setSelectedPrediction(item)}
                    className="border-b border-gray-700 pb-2 cursor-pointer hover:bg-gray-800 rounded px-2"
                  >
                    <p><strong>Prediction:</strong> {item.prediction}</p>
                    <p><strong>File:</strong> {item.filename}</p>
                    <p className="text-gray-400 text-xs">
                      {new Date(item.timestamp).toLocaleString()}
                    </p>
                  </li>
                ))
              )}
            </ul>
          </aside>

          {/* Main Upload Section */}
          <div className="flex-1 relative flex flex-col items-center justify-start p-6">
            {/* Top-right user icon */}
            <div className="absolute top-4 right-6 z-10">
              <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="w-10 h-10 rounded-full bg-teal-400 text-black font-bold text-xl hover:bg-teal-300 flex items-center justify-center"
              >
                {username[0].toUpperCase()}
              </button>

              {showDropdown && (
                <div className="absolute right-0 mt-2 w-40 bg-gray-800 rounded shadow-lg py-2 text-sm text-white z-20">
                  <div className="px-4 py-2 border-b border-gray-600">{username}</div>
                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-2 hover:bg-gray-700"
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>

            {/* Upload UI */}
            <div className="w-full max-w-2xl flex flex-col items-center justify-center">
              <FileUpload
                username={username}
                refreshHistory={() => fetchHistory(username)}
              />
            </div>

            {/* Result from selected history item */}
            {renderSelectedResult()}
          </div>
        </div>
      )}
    </main>
  );
}
