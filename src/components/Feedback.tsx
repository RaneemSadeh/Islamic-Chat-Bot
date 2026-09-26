import React from 'react';

import { WarningIcon } from './IconComponents';

/** The three dots shown while a turn is in flight. */
export const LoadingIndicator: React.FC = () => (
  <div
    role="status"
    aria-live="polite"
    className="flex items-center gap-2 px-2 py-4 text-sm text-slate-500 dark:text-slate-400"
  >
    <span className="flex gap-1">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="h-1.5 w-1.5 animate-pulse bg-emerald-600"
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </span>
    يبحث في المصادر…
  </div>
);

/** A banner for a failure that is not tied to one message - a missing key, say. */
export const Notice: React.FC<{
  tone?: 'warn' | 'error';
  children: React.ReactNode;
  onDismiss?: () => void;
}> = ({ tone = 'warn', children, onDismiss }) => {
  const palette =
    tone === 'error'
      ? 'border-rose-300 bg-rose-50 text-rose-800 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-200'
      : 'border-amber-300 bg-amber-50 text-amber-900 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-200';

  return (
    <div role="alert" className={`flex items-start gap-3 border px-4 py-3 text-sm ${palette}`}>
      <WarningIcon className="mt-0.5 h-4 w-4 shrink-0" />
      <p className="flex-1 leading-relaxed">{children}</p>
      {onDismiss && (
        <button
          type="button"
          onClick={onDismiss}
          aria-label="إخفاء التنبيه"
          className="shrink-0 px-1 text-lg leading-none opacity-60 transition hover:opacity-100"
        >
          ×
        </button>
      )}
    </div>
  );
};
