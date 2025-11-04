import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Layout = ({ children }) => {
  const navigate = useNavigate();
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div data-easytag="id1-react/src/components/Layout.jsx" className="flex min-h-screen flex-col">
      <header data-easytag="id2-react/src/components/Layout.jsx" className="border-b border-slate-200 bg-white/80 backdrop-blur">
        <div data-easytag="id3-react/src/components/Layout.jsx" className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
          <nav data-easytag="id4-react/src/components/Layout.jsx" className="flex items-center gap-4">
            <Link data-easytag="id5-react/src/components/Layout.jsx" to="/" className="text-sm font-medium text-slate-700 hover:text-slate-900">Главная</Link>
            <Link data-easytag="id6-react/src/components/Layout.jsx" to="/chat" className="text-sm font-medium text-slate-700 hover:text-slate-900">Чат</Link>
          </nav>
          <div data-easytag="id7-react/src/components/Layout.jsx" className="flex items-center gap-3">
            {!token && (
              <>
                <Link data-easytag="id8-react/src/components/Layout.jsx" to="/login" className="rounded-md border border-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50">Войти</Link>
                <Link data-easytag="id9-react/src/components/Layout.jsx" to="/register" className="rounded-md bg-slate-900 px-3 py-1.5 text-sm text-white hover:bg-slate-800">Регистрация</Link>
              </>
            )}
            {token && (
              <button data-easytag="id10-react/src/components/Layout.jsx" onClick={handleLogout} className="rounded-md border border-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50">Выйти</button>
            )}
          </div>
        </div>
      </header>
      <main data-easytag="id11-react/src/components/Layout.jsx" className="mx-auto w-full max-w-5xl flex-1 px-4 py-6">
        {children}
      </main>
      <footer data-easytag="id12-react/src/components/Layout.jsx" className="border-t border-slate-200 bg-white/60">
        <div data-easytag="id13-react/src/components/Layout.jsx" className="mx-auto max-w-5xl px-4 py-3 text-center text-xs text-slate-500">
          Сервис группового чата — Easyappz
        </div>
      </footer>
    </div>
  );
};

export default Layout;
