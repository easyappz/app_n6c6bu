import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return (
    <div data-easytag="id1-react/src/components/ProtectedRoute.jsx" className="contents">{children}</div>
  );
};

export default ProtectedRoute;
