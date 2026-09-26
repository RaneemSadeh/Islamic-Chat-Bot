import React from 'react';

import { config } from '../config';
import { LampIcon } from './IconComponents';

interface HeaderProps {
  onReset: () => void;
  canReset: boolean;
}

export const Header: React.FC<HeaderProps> = ({ onReset, canReset }) => (
  <header className="border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-900/90">
    <div className="mx-auto flex max-w-3xl items-center justify-between gap-4 px-4 py-3">
      <div className="flex items-center gap-3">
        <span className="flex h-11 w-11 items-center justify-center bg-emerald-700 text-white">
          <LampIcon className="h-6 w-6" />
        </span>
        <div>
          <h1 className="text-lg font-bold leading-tight text-slate-900 dark:text-slate-50">
            {config.appName}
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">{config.tagline}</p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={onReset}
          disabled={!canReset}
          className="border border-slate-300 px-3 py-1.5 text-xs font-medium text-slate-600 transition hover:border-slate-400 hover:text-slate-900 disabled:cursor-not-allowed disabled:opacity-40 dark:border-slate-700 dark:text-slate-300 dark:hover:border-slate-500 dark:hover:text-white"
        >
          محادثة جديدة
        </button>
        <span className="hidden font-mono text-[11px] text-slate-400 sm:inline">
          v{config.version}
        </span>
      </div>
    </div>
  </header>
);
