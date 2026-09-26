import React, { useLayoutEffect, useRef, useState } from 'react';

import { DISCLAIMER } from '../constants';
import { SendIcon } from './IconComponents';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

const MAX_ROWS_PX = 168;

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading, disabled }) => {
  const [value, setValue] = useState('');
  const textarea = useRef<HTMLTextAreaElement>(null);

  // Grow with the content up to a ceiling, then scroll inside the box.
  useLayoutEffect(() => {
    const el = textarea.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = `${Math.min(el.scrollHeight, MAX_ROWS_PX)}px`;
  }, [value]);

  const blocked = isLoading || disabled;
  const canSend = value.trim().length > 0 && !blocked;

  const submit = (event?: React.FormEvent) => {
    event?.preventDefault();
    if (!canSend) return;
    onSendMessage(value);
    setValue('');
  };

  return (
    <div className="border-t border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <form onSubmit={submit} className="mx-auto max-w-3xl px-4 py-3">
        <div className="flex items-end gap-2 border border-slate-300 bg-slate-50 p-2 focus-within:border-emerald-600 dark:border-slate-700 dark:bg-slate-800">
          <label htmlFor="question" className="sr-only">
            اكتب سؤالك
          </label>
          <textarea
            id="question"
            ref={textarea}
            value={value}
            onChange={(event) => setValue(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                submit();
              }
            }}
            rows={1}
            disabled={blocked}
            placeholder={disabled ? 'أضف مفتاح Gemini لتفعيل المحادثة' : 'اسأل سؤالك هنا…'}
            className="max-h-[168px] flex-1 resize-none bg-transparent px-2 py-1.5 text-right text-slate-900 outline-none placeholder:text-slate-400 disabled:cursor-not-allowed dark:text-slate-100"
          />
          <button
            type="submit"
            disabled={!canSend}
            aria-label="إرسال السؤال"
            className="flex h-9 w-9 shrink-0 items-center justify-center bg-emerald-700 text-white transition hover:bg-emerald-800 disabled:cursor-not-allowed disabled:bg-slate-300 dark:disabled:bg-slate-700"
          >
            <SendIcon className="h-4 w-4 -scale-x-100" />
          </button>
        </div>
        <p className="mt-2 text-center text-[11px] leading-relaxed text-slate-400">{DISCLAIMER}</p>
      </form>
    </div>
  );
};
