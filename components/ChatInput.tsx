
import React, { useState } from 'react';
import { SendIcon } from './IconComponents';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
      <div className="relative">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          placeholder="اسأل سؤالك هنا..."
          className="w-full p-3 ps-4 pe-14 text-right bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-full focus:outline-none focus:ring-2 focus:ring-emerald-500 resize-none"
          rows={1}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="absolute left-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-emerald-500 text-white hover:bg-emerald-600 disabled:bg-emerald-300 disabled:cursor-not-allowed"
          disabled={isLoading || !inputValue.trim()}
        >
          <SendIcon className="w-5 h-5" />
        </button>
      </div>
    </form>
  );
};
