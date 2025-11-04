import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';

import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Chat from './pages/Chat';
import NotFound from './pages/NotFound';

function App() {
  useEffect(() => {
    const routes = ['/', '/login', '/register', '/chat', '*'];
    if (typeof window !== 'undefined' && typeof window.handleRoutes === 'function') {
      window.handleRoutes(routes);
    }
  }, []);

  return (
    <BrowserRouter>
      <div data-easytag="id1-react/src/App.js" className="min-h-screen bg-slate-50 text-slate-900">
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/chat"
              element={
                <ProtectedRoute>
                  <Chat />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Layout>
      </div>
    </BrowserRouter>
  );
}

export default App;
