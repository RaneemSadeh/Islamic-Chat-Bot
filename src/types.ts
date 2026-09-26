/** The shared vocabulary of the client. Everything else imports from here. */

export enum MessageRole {
  User = 'user',
  Assistant = 'assistant',
}

/** Where a passage came from: a book or site, and the exact position inside it. */
export interface Source {
  name: string;
  reference: string;
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  createdAt: number;
  /** Present only on grounded assistant replies. */
  source?: Source;
  originalText?: string;
  aiNote?: string;
  /** Set when the turn failed, so the card can render as a failure. */
  errorCode?: string;
}

/** The exact shape the model is required to return. */
export interface GeminiResponse {
  rephrasedAnswer: string;
  originalText: string;
  source: Source;
  aiNote: string;
}
