
import React from 'react';
import type { ChatMessage } from '../types';
import { MessageRole } from '../types';
import { UserIcon, BotIcon, InfoIcon } from './IconComponents';

const SourceCard: React.FC<{ name: string; reference: string }> = ({ name, reference }) => (
  <div className="mt-4 border-t border-gray-200 dark:border-gray-700 pt-3">
    <h4 className="text-sm font-semibold text-gray-600 dark:text-gray-300 mb-1">المصدر المعتمد</h4>
    <div className="text-sm text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-800 rounded-lg p-3">
      <p><span className="font-bold">{name}</span></p>
      <p className="text-gray-500 dark:text-gray-400">{reference}</p>
    </div>
  </div>
);

const OriginalText: React.FC<{ text: string }> = ({ text }) => (
    <div className="mt-4">
        <h4 className="text-sm font-semibold text-gray-600 dark:text-gray-300 mb-1">النص الأصلي من المرجع</h4>
        <blockquote className="border-r-4 border-emerald-500 ps-4 py-2 bg-gray-50 dark:bg-gray-800/50 text-gray-700 dark:text-gray-300 italic">
            {text}
        </blockquote>
    </div>
);

const AiNote: React.FC<{ note: string }> = ({ note }) => (
    <div className="mt-4 text-xs text-blue-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-900/50 rounded-lg p-3 flex items-start gap-2">
        <InfoIcon className="w-5 h-5 flex-shrink-0 mt-0.5" />
        <span>{note}</span>
    </div>
);

export const Message: React.FC<{ message: ChatMessage }> = ({ message }) => {
  const isUser = message.role === MessageRole.User;

  return (
    <div className={`flex items-start gap-4 my-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${isUser ? 'bg-blue-500 text-white' : 'bg-emerald-500 text-white'}`}>
        {isUser ? <UserIcon className="w-6 h-6" /> : <BotIcon className="w-6 h-6" />}
      </div>
      <div className={`max-w-2xl rounded-lg p-4 text-right ${isUser ? 'bg-blue-50 dark:bg-blue-900/50' : 'bg-white dark:bg-gray-800 shadow-sm'}`}>
        <p className="text-gray-800 dark:text-gray-100 whitespace-pre-wrap">{message.content}</p>
        {message.originalText && <OriginalText text={message.originalText} />}
        {message.source && <SourceCard name={message.source.name} reference={message.source.reference} />}
        {message.aiNote && <AiNote note={message.aiNote} />}
      </div>
    </div>
  );
};
