'use client';

import { useState } from 'react';

export default function Register({ onSwitch, onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch('https://deeptoneai.up.railway.app/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (res.ok && data.success) {
        // ✅ Auto-login after registration
        const loginRes = await fetch('https://deeptoneai.up.railway.app/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password }),
        });

        const loginData = await loginRes.json();

        if (loginRes.ok && loginData.success) {
          onLoginSuccess(loginData.username); // 🎉 Login success
        } else {
          alert(loginData.error || 'Registered, but failed to log in');
        }
      } else {
        alert(data.error || 'Registration failed');
      }
    } catch (err) {
      console.error('Registration error:', err);
      alert('Error during registration');
    }
  };

  return (
    <form onSubmit={handleRegister} className="flex flex-col space-y-4">
      <input
        type="text"
        placeholder="Username"
        className="bg-gray-700 text-white p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-400"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        className="bg-gray-700 text-white p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-400"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button
        type="submit"
        className="bg-teal-400 text-slate-900 font-semibold py-2 rounded-md hover:bg-teal-300 transition"
      >
        Register
      </button>
      <p className="text-sm text-center text-gray-300">
        Already have an account?{' '}
        <button
          type="button"
          className="text-teal-400 hover:underline"
          onClick={onSwitch}
        >
          Login
        </button>
      </p>
    </form>
  );
}
