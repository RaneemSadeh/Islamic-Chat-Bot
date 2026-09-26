/**
 * Single source of truth for anything that changes between environments.
 *
 * The key is injected at build time by Vite (see `vite.config.ts`). A browser
 * bundle cannot keep a secret: whatever ends up here is readable by anyone who
 * opens dev tools. That is acceptable for a local demo and for a key that is
 * restricted by referrer, and it is the first thing to change when this moves
 * to production - see `docs/ARCHITECTURE.md`.
 */

const readEnv = (name: string): string => {
  const value = (import.meta.env as Record<string, string | undefined>)[name];
  return typeof value === 'string' ? value.trim() : '';
};

export const config = {
  /** Google AI Studio key. Empty in a checkout with no `.env.local`. */
  apiKey: readEnv('VITE_GEMINI_API_KEY'),
  /** Model used for every answer. Flash keeps a chat turn under a second. */
  model: 'gemini-2.5-flash',
  appName: 'سِراج',
  appNameLatin: 'Siraj',
  tagline: 'مساعد معرفي إسلامي يوضّح مصدر كل إجابة',
  version: '1.1.0',
  repositoryUrl: 'https://github.com/RaneemSadeh/Islamic-Chat-Bot',
} as const;

export const hasApiKey = (): boolean => config.apiKey.length > 0;
