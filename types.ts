
export enum MessageRole {
  User = 'user',
  Assistant = 'assistant',
}

export interface Source {
  name: string;
  reference: string;
}

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  source?: Source;
  originalText?: string;
  aiNote?: string;
}

export interface GeminiResponse {
  rephrasedAnswer: string;
  originalText: string;
  source: Source;
  aiNote: string;
}
