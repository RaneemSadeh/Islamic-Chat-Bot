import { useCallback, useEffect, useRef, useState } from 'react';

import { getIslamicBotResponse } from '../services/geminiService';
import { describe, toSirajError } from '../lib/errors';
import { MessageRole } from '../types';
import type { ChatMessage } from '../types';

let counter = 0;
const nextId = (prefix: string) => `${prefix}-${Date.now().toString(36)}-${(counter += 1)}`;

/**
 * Owns a conversation. Keeping it out of `App` means the turn logic - optimistic
 * user message, in-flight guard, cancellation, failure mapping - can be read and
 * tested on its own.
 */
export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inFlight = useRef<AbortController | null>(null);

  useEffect(() => () => inFlight.current?.abort(), []);

  const send = useCallback(async (question: string) => {
    const text = question.trim();
    if (!text || inFlight.current) return;

    setError(null);
    setMessages((prev) => [
      ...prev,
      { id: nextId('user'), role: MessageRole.User, content: text, createdAt: Date.now() },
    ]);
    setIsLoading(true);

    const controller = new AbortController();
    inFlight.current = controller;

    try {
      const answer = await getIslamicBotResponse(text, { signal: controller.signal });
      setMessages((prev) => [
        ...prev,
        {
          id: nextId('assistant'),
          role: MessageRole.Assistant,
          content: answer.rephrasedAnswer,
          originalText: answer.originalText,
          source: answer.source,
          aiNote: answer.aiNote,
          createdAt: Date.now(),
        },
      ]);
    } catch (raw) {
      if (controller.signal.aborted) return;
      const failure = toSirajError(raw);
      setError(describe(failure));
      setMessages((prev) => [
        ...prev,
        {
          id: nextId('error'),
          role: MessageRole.Assistant,
          content: describe(failure),
          errorCode: failure.code,
          createdAt: Date.now(),
        },
      ]);
    } finally {
      inFlight.current = null;
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    inFlight.current?.abort();
    inFlight.current = null;
    setMessages([]);
    setError(null);
    setIsLoading(false);
  }, []);

  return { messages, isLoading, error, send, reset, dismissError: () => setError(null) };
}
