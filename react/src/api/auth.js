import instance from './axios';

export const register = ({ username, password }) => {
  return instance.post('/api/auth/register/', { username, password });
};

export const login = ({ username, password }) => {
  return instance.post('/api/auth/login/', { username, password });
};

export const me = () => {
  return instance.get('/api/auth/me/');
};
