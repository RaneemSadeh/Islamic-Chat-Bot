/**
 * Every failure the user can see has a code, so the UI can explain what went
 * wrong in Arabic instead of leaking a provider stack trace into the chat.
 */

export type SirajErrorCode =
  | 'MISSING_API_KEY'
  | 'NETWORK'
  | 'RATE_LIMITED'
  | 'INVALID_RESPONSE'
  | 'UNKNOWN';

export class SirajError extends Error {
  readonly code: SirajErrorCode;

  constructor(code: SirajErrorCode, message: string, options?: { cause?: unknown }) {
    super(message, options as ErrorOptions);
    this.name = 'SirajError';
    this.code = code;
  }
}

/** User-facing copy. Arabic, because the whole interface is Arabic. */
export const ERROR_MESSAGES: Record<SirajErrorCode, string> = {
  MISSING_API_KEY:
    'لم يتم ضبط مفتاح Gemini. أضف VITE_GEMINI_API_KEY إلى ملف ‎.env.local ثم أعد تشغيل التطبيق.',
  NETWORK: 'تعذّر الوصول إلى الخدمة. تحقّق من اتصالك بالإنترنت وحاول مرة أخرى.',
  RATE_LIMITED: 'تم تجاوز الحد المسموح من الطلبات. انتظر قليلاً ثم أعد المحاولة.',
  INVALID_RESPONSE:
    'وصلت إجابة غير مكتملة من النموذج، ولم يتم عرضها حتى لا تظهر معلومة بلا مصدر.',
  UNKNOWN: 'حدث خطأ غير متوقع. راجع سجلّ المتصفح لمزيد من التفاصيل.',
};

export const toSirajError = (error: unknown): SirajError => {
  if (error instanceof SirajError) return error;

  const raw = error instanceof Error ? error.message : String(error);
  const text = raw.toLowerCase();

  if (text.includes('429') || text.includes('quota') || text.includes('rate')) {
    return new SirajError('RATE_LIMITED', raw, { cause: error });
  }
  if (text.includes('fetch') || text.includes('network') || text.includes('failed to')) {
    return new SirajError('NETWORK', raw, { cause: error });
  }
  return new SirajError('UNKNOWN', raw, { cause: error });
};

export const describe = (error: unknown): string => ERROR_MESSAGES[toSirajError(error).code];
