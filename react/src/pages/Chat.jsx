import React, { useEffect, useRef, useState } from 'react';
import { getMessages, sendMessage, deleteMessage, getRoom } from '../api/chat';
import { me } from '../api/auth';
import MessageItem from '../components/MessageItem';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);
  const [room, setRoom] = useState(null);
  const bottomRef = useRef(null);
  const pollingRef = useRef(null);

  const fetchAll = async () => {
    try {
      const [{ data: meData }, { data: roomData }, { data: msgData }] = await Promise.all([
        me(),
        getRoom(),
        getMessages({ limit: 50, offset: 0 }),
      ]);
      setUser(meData);
      setRoom(roomData);
      const list = Array.isArray(msgData?.results) ? msgData.results : [];
      setMessages(list);
    } catch (err) {
      setError('Не удалось загрузить данные');
    } finally {
      setLoading(false);
      scrollToBottom();
    }
  };

  const fetchMessagesOnly = async () => {
    try {
      const { data } = await getMessages({ limit: 50, offset: 0 });
      const list = Array.isArray(data?.results) ? data.results : [];
      setMessages(list);
    } catch (err) {
      // keep previous messages; optionally set error
    } finally {
      scrollToBottom();
    }
  };

  const scrollToBottom = () => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    fetchAll();
    pollingRef.current = setInterval(() => {
      fetchMessagesOnly();
    }, 3000);
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const onSubmit = async (e) => {
    e.preventDefault();
    const trimmed = content.trim();
    if (!trimmed) return;
    try {
      await sendMessage({ content: trimmed });
      setContent('');
      await fetchMessagesOnly();
    } catch (err) {
      setError('Не удалось отправить сообщение');
    }
  };

  const onDelete = async (id) => {
    try {
      await deleteMessage(id);
      await fetchMessagesOnly();
    } catch (err) {
      setError('Не удалось удалить сообщение');
    }
  };

  if (loading) {
    return (
      <div data-easytag="id1-react/src/pages/Chat.jsx" className="text-center text-slate-600">Загрузка...</div>
    );
  }

  return (
    <section data-easytag="id2-react/src/pages/Chat.jsx" className="mx-auto flex max-w-3xl flex-col gap-4">
      <div data-easytag="id3-react/src/pages/Chat.jsx" className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
        <div data-easytag="id4-react/src/pages/Chat.jsx" className="mb-3 flex items-center justify-between">
          <h2 data-easytag="id5-react/src/pages/Chat.jsx" className="text-lg font-semibold text-slate-900">{room?.name || 'Чат'}</h2>
          {user?.role && (
            <span data-easytag="id6-react/src/pages/Chat.jsx" className="rounded-md border border-slate-200 px-2 py-1 text-xs text-slate-600">Роль: {user.role}</span>
          )}
        </div>
        <ul data-easytag="id7-react/src/pages/Chat.jsx" className="max-h-[50vh] overflow-y-auto pr-1">
          {messages.map((m) => (
            <MessageItem key={m.id} message={m} currentUsername={user?.username} onDelete={onDelete} />
          ))}
          <li data-easytag="id8-react/src/pages/Chat.jsx" ref={bottomRef} />
        </ul>
      </div>

      {error && (
        <div data-easytag="id9-react/src/pages/Chat.jsx" className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <form data-easytag="id10-react/src/pages/Chat.jsx" onSubmit={onSubmit} className="flex items-end gap-2">
        <div data-easytag="id11-react/src/pages/Chat.jsx" className="flex-1">
          <label data-easytag="id12-react/src/pages/Chat.jsx" htmlFor="message" className="mb-1 block text-xs text-slate-600">
            Сообщение
          </label>
          <textarea
            data-easytag="id13-react/src/pages/Chat.jsx"
            id="message"
            rows={3}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full resize-y rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-400"
            placeholder="Напишите сообщение..."
          />
        </div>
        <button data-easytag="id14-react/src/pages/Chat.jsx" type="submit" className="h-[42px] shrink-0 rounded-md bg-slate-900 px-4 text-sm text-white hover:bg-slate-800">
          Отправить
        </button>
      </form>
    </section>
  );
};

export default Chat;
