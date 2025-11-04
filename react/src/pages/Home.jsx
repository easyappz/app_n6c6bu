import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <section data-easytag="id1-react/src/pages/Home.jsx" className="mx-auto max-w-3xl">
      <div data-easytag="id2-react/src/pages/Home.jsx" className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 data-easytag="id3-react/src/pages/Home.jsx" className="mb-2 text-2xl font-semibold text-slate-900">Групповой чат</h1>
        <p data-easytag="id4-react/src/pages/Home.jsx" className="mb-6 text-slate-600">
          Минималистичный чат для зарегистрированных пользователей. Поддерживает отправку текстовых сообщений,
          историю, а также роли и права доступа.
        </p>
        <div data-easytag="id5-react/src/pages/Home.jsx" className="flex flex-wrap gap-3">
          <Link data-easytag="id6-react/src/pages/Home.jsx" to="/login" className="rounded-md border border-slate-300 px-4 py-2 text-sm hover:bg-slate-50">Войти</Link>
          <Link data-easytag="id7-react/src/pages/Home.jsx" to="/register" className="rounded-md bg-slate-900 px-4 py-2 text-sm text-white hover:bg-slate-800">Зарегистрироваться</Link>
          <Link data-easytag="id8-react/src/pages/Home.jsx" to="/chat" className="rounded-md border border-slate-300 px-4 py-2 text-sm hover:bg-slate-50">Перейти в чат</Link>
        </div>
      </div>
    </section>
  );
};

export default Home;
