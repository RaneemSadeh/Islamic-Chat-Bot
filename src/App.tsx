import React, { useEffect, useRef } from 'react';

import { ChatInput } from './components/ChatInput';
import { EmptyState } from './components/EmptyState';
import { LoadingIndicator, Notice } from './components/Feedback';
import { Header } from './components/Header';
import { Message } from './components/Message';
import { hasApiKey } from './config';
import { ERROR_MESSAGES } from './lib/errors';
import { useChat } from './hooks/useChat';

const App: React.FC = () => {
  const { messages, isLoading, error, send, reset, dismissError } = useChat();
  const endOfList = useRef<HTMLDivElement>(null);
  const keyMissing = !hasApiKey();

  useEffect(() => {
    endOfList.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [messages, isLoading]);

  return (
    <div className="flex h-dvh flex-col bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
      <Header onReset={reset} canReset={messages.length > 0} />

      <main className="flex-1 overflow-y-auto">
        <div className="mx-auto flex min-h-full max-w-3xl flex-col px-4 py-4">
          {keyMissing && (
            <div className="mb-4">
              <Notice tone="warn">{ERROR_MESSAGES.MISSING_API_KEY}</Notice>
            </div>
          )}

          {error && !keyMissing && (
            <div className="mb-4">
              <Notice tone="error" onDismiss={dismissError}>
                {error}
              </Notice>
            </div>
          )}

          {messages.length === 0 ? (
            <div className="flex flex-1 items-center justify-center">
              <EmptyState onPick={send} disabled={keyMissing || isLoading} />
            </div>
          ) : (
            <div className="flex flex-col">
              {messages.map((message) => (
                <Message key={message.id} message={message} />
              ))}
            </div>
          )}

          {isLoading && <LoadingIndicator />}
          <div ref={endOfList} />
        </div>
      </main>

      <ChatInput onSendMessage={send} isLoading={isLoading} disabled={keyMissing} />
    </div>
  );
};

export default App;
