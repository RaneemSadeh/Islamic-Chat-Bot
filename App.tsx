
import React, { useState, useRef, useEffect } from 'react';
import type { ChatMessage } from './types';
import { MessageRole } from './types';
import { getIslamicBotResponse } from './services/geminiService';
import { Header } from './components/Header';
import { ChatInput } from './components/ChatInput';
import { Message } from './components/Message';

const LoadingIndicator: React.FC = () => (
    <div className="flex items-center justify-center p-4">
      <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse [animation-delay:-0.3s]"></div>
        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse [animation-delay:-0.15s]"></div>
        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
        <span className="text-sm">يفكر...</span>
      </div>
    </div>
);


const App: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const handleSendMessage = async (userMessage: string) => {
    setError(null);
    const newUserMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: MessageRole.User,
      content: userMessage,
    };
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      const response = await getIslamicBotResponse(userMessage);
      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: MessageRole.Assistant,
        content: response.rephrasedAnswer,
        source: response.source,
        originalText: response.originalText,
        aiNote: response.aiNote,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err: any) {
      const errorMessage = err.message || "An unexpected error occurred.";
      setError(errorMessage);
      const errorResponseMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        role: MessageRole.Assistant,
        content: `حدث خطأ: ${errorMessage}`,
      };
      setMessages(prev => [...prev, errorResponseMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <Header />
      <main className="flex-1 overflow-y-auto p-4">
        {messages.map((msg) => (
          <Message key={msg.id} message={msg} />
        ))}
        {isLoading && <LoadingIndicator />}
        {error && <div className="text-center text-red-500 p-4">Error: {error}</div>}
        <div ref={messagesEndRef} />
      </main>
      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default App;
