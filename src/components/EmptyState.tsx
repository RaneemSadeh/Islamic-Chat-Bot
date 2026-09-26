import React from 'react';

import { EMPTY_STATE, SUGGESTED_QUESTIONS } from '../constants';
import { LampIcon } from './IconComponents';

interface EmptyStateProps {
  onPick: (question: string) => void;
  disabled?: boolean;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ onPick, disabled }) => (
  <div className="flex flex-col items-center px-2 py-12 text-center">
    <span className="mb-5 flex h-14 w-14 items-center justify-center border border-emerald-700 text-emerald-700 dark:text-emerald-400">
      <LampIcon className="h-7 w-7" />
    </span>
    <h2 className="text-xl font-bold text-slate-800 dark:text-slate-100">{EMPTY_STATE.title}</h2>
    <p className="mt-2 max-w-md leading-relaxed text-slate-500 dark:text-slate-400">
      {EMPTY_STATE.body}
    </p>

    <ul className="mt-7 grid w-full max-w-xl gap-2 sm:grid-cols-2">
      {SUGGESTED_QUESTIONS.map((question) => (
        <li key={question}>
          <button
            type="button"
            disabled={disabled}
            onClick={() => onPick(question)}
            className="w-full border border-slate-200 bg-white px-4 py-3 text-right text-sm leading-relaxed text-slate-700 transition hover:border-emerald-700 hover:text-emerald-800 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-300 dark:hover:border-emerald-500 dark:hover:text-emerald-300"
          >
            {question}
          </button>
        </li>
      ))}
    </ul>
  </div>
);
