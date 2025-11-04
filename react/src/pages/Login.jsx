import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/auth';

const Login = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const onSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const { data } = await login({ username, password });
      if (data?.token) {
        localStorage.setItem('token', data.token);
        navigate('/chat');
      }
    } catch (err) {
      setError(err?.response?.data?.detail || 'Ошибка авторизации');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section data-easytag="id1-react/src/pages/Login.jsx" className="mx-auto max-w-md">
      <div data-easytag="id2-react/src/pages/Login.jsx" className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 data-easytag="id3-react/src/pages/Login.jsx" className="mb-6 text-xl font-semibold">Авторизация</h1>
        <form data-easytag="id4-react/src/pages/Login.jsx" onSubmit={onSubmit} className="space-y-4">
          <div data-easytag="id5-react/src/pages/Login.jsx" className="space-y-1">
            <label data-easytag="id6-react/src/pages/Login.jsx" htmlFor="username" className="text-sm text-slate-700">Логин</label>
            <input
              data-easytag="id7-react/src/pages/Login.jsx"
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-400"
              placeholder="Введите логин"
            />
          </div>
          <div data-easytag="id8-react/src/pages/Login.jsx" className="space-y-1">
            <label data-easytag="id9-react/src/pages/Login.jsx" htmlFor="password" className="text-sm text-slate-700">Пароль</label>
            <input
              data-easytag="id10-react/src/pages/Login.jsx"
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-400"
              placeholder="Введите пароль"
            />
          </div>

          {error && (
            <div data-easytag="id11-react/src/pages/Login.jsx" className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
              {error}
            </div>
          )}

          <button
            data-easytag="id12-react/src/pages/Login.jsx"
            type="submit"
            disabled={loading}
            className="w-full rounded-md bg-slate-900 px-4 py-2 text-sm text-white hover:bg-slate-800 disabled:opacity-60"
          >
            {loading ? 'Вход...' : 'Войти'}
          </button>
        </form>
      </div>
    </section>
  );
};

export default Login;
