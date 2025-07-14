'use client';

import { useState } from 'react';

export default function Register({ onSwitch }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch('https://deeptoneai.onrender.com/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (res.ok && data.success) {
        alert('Registration successful! You can now login.');
        onSwitch(); // switch to login screen
      } else {
        alert(data.error || data.message || 'Registration failed.');
      }
    } catch (err) {
      console.error(err);
      alert('Error during registration. Please try again later.');
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
