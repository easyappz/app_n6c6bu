import instance from './axios';

export const getMessages = ({ limit = 50, offset = 0 } = {}) => {
  const params = new URLSearchParams();
  params.append('limit', String(limit));
  params.append('offset', String(offset));
  return instance.get(`/api/chat/messages/?${params.toString()}`);
};

export const sendMessage = ({ content }) => {
  return instance.post('/api/chat/messages/', { content });
};

export const deleteMessage = (id) => {
  return instance.delete(`/api/chat/messages/${id}/`);
};

export const getRoom = () => {
  return instance.get('/api/chat/room/');
};
