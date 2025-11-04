import React from 'react';

const MessageItem = ({ message, currentUsername, onDelete }) => {
  const isOwn = message?.author?.username === currentUsername;
  return (
    <li
      data-easytag="id1-react/src/components/MessageItem.jsx"
      className={`group relative mb-2 rounded-lg border px-3 py-2 text-sm ${
        isOwn ? 'border-blue-200 bg-blue-50' : 'border-slate-200 bg-white'
      }`}
    >
      <div data-easytag="id2-react/src/components/MessageItem.jsx" className="flex items-start gap-3">
        <div data-easytag="id3-react/src/components/MessageItem.jsx" className="mt-0.5 h-2.5 w-2.5 shrink-0 rounded-full bg-slate-300" />
        <div data-easytag="id4-react/src/components/MessageItem.jsx" className="min-w-0 flex-1">
          <div data-easytag="id5-react/src/components/MessageItem.jsx" className="mb-1 flex items-center gap-2">
            <span data-easytag="id6-react/src/components/MessageItem.jsx" className="font-medium text-slate-800">{message?.author?.username || '—'}</span>
            <span data-easytag="id7-react/src/components/MessageItem.jsx" className="text-xs text-slate-500">
              {message?.created_at ? new Date(message.created_at).toLocaleString() : ''}
            </span>
          </div>
          <p data-easytag="id8-react/src/components/MessageItem.jsx" className="whitespace-pre-wrap break-words text-slate-800">
            {message?.content}
          </p>
        </div>
        {message?.can_delete === true && (
          <button
            data-easytag="id9-react/src/components/MessageItem.jsx"
            onClick={() => onDelete(message.id)}
            className="invisible ml-2 rounded-md border border-slate-300 px-2 py-1 text-xs text-slate-600 hover:bg-slate-50 group-hover:visible"
            title="Удалить сообщение"
          >
            Удалить
          </button>
        )}
      </div>
    </li>
  );
};

export default MessageItem;
