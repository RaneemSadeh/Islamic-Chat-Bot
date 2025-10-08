
import React from 'react';
import { BotIcon } from './IconComponents';

export const Header: React.FC = () => {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-md p-4 flex items-center justify-between border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3">
            <div className="bg-emerald-500 text-white p-2 rounded-lg">
                <BotIcon className="w-7 h-7" />
            </div>
            <div>
                <h1 className="text-xl font-bold text-gray-800 dark:text-white">الشات بوت الإسلامي</h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">مدعوم بنظام الاسترجاع المعزز (RAG)</p>
            </div>
        </div>
        <div className="text-xs text-gray-400">
            v1.0.0
        </div>
    </header>
  );
};
