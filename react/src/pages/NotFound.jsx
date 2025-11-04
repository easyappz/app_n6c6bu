import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <section data-easytag="id1-react/src/pages/NotFound.jsx" className="mx-auto max-w-xl text-center">
      <h1 data-easytag="id2-react/src/pages/NotFound.jsx" className="mb-2 text-3xl font-semibold text-slate-900">404</h1>
      <p data-easytag="id3-react/src/pages/NotFound.jsx" className="mb-6 text-slate-600">Страница не найдена</p>
      <Link data-easytag="id4-react/src/pages/NotFound.jsx" to="/" className="rounded-md border border-slate-300 px-4 py-2 text-sm hover:bg-slate-50">На главную</Link>
    </section>
  );
};

export default NotFound;
