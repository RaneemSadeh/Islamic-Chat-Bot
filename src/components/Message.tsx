import React, { useState } from 'react';

import { MessageRole } from '../types';
import type { ChatMessage } from '../types';
import {
  BookIcon,
  CheckIcon,
  CopyIcon,
  InfoIcon,
  LampIcon,
  QuoteIcon,
  UserIcon,
  WarningIcon,
} from './IconComponents';

const SectionLabel: React.FC<{ icon: React.ReactNode; children: React.ReactNode }> = ({
  icon,
  children,
}) => (
  <h4 className="mb-1.5 flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-wide text-slate-500 dark:text-slate-400">
    {icon}
    {children}
  </h4>
);

const OriginalText: React.FC<{ text: string }> = ({ text }) => (
  <section className="mt-4">
    <SectionLabel icon={<QuoteIcon className="h-3.5 w-3.5" />}>النص الأصلي</SectionLabel>
    <blockquote className="border-r-4 border-emerald-700 bg-emerald-50/70 px-4 py-3 leading-loose text-slate-700 dark:bg-emerald-950/30 dark:text-slate-200">
      {text}
    </blockquote>
  </section>
);

const SourceCard: React.FC<{ name: string; reference: string }> = ({ name, reference }) => (
  <section className="mt-4">
    <SectionLabel icon={<BookIcon className="h-3.5 w-3.5" />}>المصدر</SectionLabel>
    <div className="flex flex-wrap items-baseline justify-between gap-2 border border-slate-200 bg-slate-50 px-4 py-3 dark:border-slate-700 dark:bg-slate-800/60">
      <span className="font-bold text-slate-800 dark:text-slate-100">{name}</span>
      <span className="font-mono text-xs text-slate-500 dark:text-slate-400">{reference}</span>
    </div>
  </section>
);

const AiNote: React.FC<{ note: string }> = ({ note }) => (
  <details className="mt-4 border border-dashed border-slate-300 bg-slate-50/60 px-4 py-2 text-xs dark:border-slate-700 dark:bg-slate-800/40">
    <summary className="cursor-pointer list-none text-slate-500 dark:text-slate-400">
      <span className="inline-flex items-center gap-1.5">
        <InfoIcon className="h-3.5 w-3.5" />
        كيف أُنتجت هذه الإجابة
      </span>
    </summary>
    <p dir="ltr" className="mt-2 text-left font-mono leading-relaxed text-slate-500 dark:text-slate-400">
      {note}
    </p>
  </details>
);

const CopyButton: React.FC<{ text: string }> = ({ text }) => {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      /* clipboard blocked - nothing useful to say to the user */
    }
  };

  return (
    <button
      type="button"
      onClick={copy}
      aria-label={copied ? 'تم النسخ' : 'نسخ الإجابة'}
      className="text-slate-400 transition hover:text-emerald-700 dark:hover:text-emerald-400"
    >
      {copied ? <CheckIcon className="h-4 w-4" /> : <CopyIcon className="h-4 w-4" />}
    </button>
  );
};

export const Message: React.FC<{ message: ChatMessage }> = ({ message }) => {
  const isUser = message.role === MessageRole.User;
  const isError = Boolean(message.errorCode);

  if (isUser) {
    return (
      <article className="flex justify-start gap-3 py-3">
        <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center bg-slate-700 text-white dark:bg-slate-600">
          <UserIcon className="h-4 w-4" />
        </span>
        <div className="max-w-[46rem] bg-slate-100 px-4 py-3 text-right leading-loose text-slate-800 dark:bg-slate-800 dark:text-slate-100">
          {message.content}
        </div>
      </article>
    );
  }

  return (
    <article className="flex gap-3 py-3">
      <span
        className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center text-white ${
          isError ? 'bg-rose-700' : 'bg-emerald-700'
        }`}
      >
        {isError ? <WarningIcon className="h-4 w-4" /> : <LampIcon className="h-4 w-4" />}
      </span>

      <div
        className={`w-full max-w-[46rem] border bg-white px-5 py-4 text-right dark:bg-slate-900 ${
          isError
            ? 'border-rose-200 dark:border-rose-900/60'
            : 'border-slate-200 dark:border-slate-800'
        }`}
      >
        <header className="mb-2 flex items-center justify-between gap-3">
          <span className="text-[11px] font-bold uppercase tracking-wide text-slate-400">
            {isError ? 'تعذّر إتمام الطلب' : 'سراج'}
          </span>
          {!isError && <CopyButton text={message.content} />}
        </header>

        <p
          className={`whitespace-pre-wrap leading-loose ${
            isError ? 'text-rose-700 dark:text-rose-300' : 'text-slate-800 dark:text-slate-100'
          }`}
        >
          {message.content}
        </p>

        {message.originalText && <OriginalText text={message.originalText} />}
        {message.source && (
          <SourceCard name={message.source.name} reference={message.source.reference} />
        )}
        {message.aiNote && <AiNote note={message.aiNote} />}
      </div>
    </article>
  );
};
