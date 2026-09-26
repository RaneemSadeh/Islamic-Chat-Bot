import { GoogleGenAI, Type } from '@google/genai';

import { config, hasApiKey } from '../config';
import { SirajError, toSirajError } from '../lib/errors';
import type { GeminiResponse } from '../types';

/**
 * The only module in the client that knows a model provider exists.
 *
 * Scope, stated plainly: this is a *presentation* of a RAG answer, not a RAG
 * pipeline. There is no index in the browser and no retrieval step - the model
 * is asked to return the passage it relied on and to name its source, and the
 * interface renders that as a citation. Treat citations as leads to verify,
 * not as verified references. `rag_console/` is the variant that really does
 * retrieve, over documents you supply.
 *
 * Replacing this file with a call to your own retrieval backend is the whole
 * migration: nothing else in the client imports the provider SDK.
 */

const SYSTEM_INSTRUCTION = `أنت "سراج"، مساعد معرفي إسلامي يجيب بالعربية الفصحى المبسّطة.

قواعد ملزمة:
1. اربط كل إجابة بنصّ شرعي أو نقل معتبر، وأورد النص كما هو في الحقل originalText دون تصرّف.
2. حدّد المصدر بدقة في الحقل source: اسم الكتاب أو الموقع، ورقم الحديث أو الصفحة أو رقم الفتوى.
3. في الحقل rephrasedAnswer اشرح النص بلغة واضحة موجّهة لسؤال المستخدم تحديداً، دون إطالة.
4. إذا كانت المسألة خلافية فاذكر ذلك صراحةً، وإذا كانت تحتاج مفتياً فوجّه المستخدم إلى أهل العلم.
5. لا تُقدّم معلومة لا تستطيع نسبتها إلى مصدر؛ قل إن المسألة تحتاج إلى مراجعة متخصص.
6. اكتب في الحقل aiNote سطراً واحداً بالإنجليزية يوضّح كيف أُنتجت الإجابة وحدود الثقة فيها.

أعد كائن JSON واحداً مطابقاً للمخطط المطلوب، دون أي نص خارجه.`;

/** The contract the interface is built around - see `docs/diagrams/04-answer-contract.svg`. */
const RESPONSE_SCHEMA = {
  type: Type.OBJECT,
  properties: {
    rephrasedAnswer: {
      type: Type.STRING,
      description: 'شرح عربي واضح للإجابة، مصاغ ليجيب عن سؤال المستخدم تحديداً.',
    },
    originalText: {
      type: Type.STRING,
      description: 'النص الأصلي المنقول من المصدر، بلا تصرّف.',
    },
    source: {
      type: Type.OBJECT,
      properties: {
        name: {
          type: Type.STRING,
          description: "اسم المصدر، مثل 'صحيح البخاري' أو 'إسلام ويب'.",
        },
        reference: {
          type: Type.STRING,
          description: "الموضع داخل المصدر: رقم الحديث أو الصفحة أو رقم الفتوى.",
        },
      },
      required: ['name', 'reference'],
    },
    aiNote: {
      type: Type.STRING,
      description: 'A one-line English note on how the answer was produced and how far to trust it.',
    },
  },
  required: ['rephrasedAnswer', 'originalText', 'source', 'aiNote'],
} as const;

let client: GoogleGenAI | null = null;

const getClient = (): GoogleGenAI => {
  if (!hasApiKey()) {
    throw new SirajError('MISSING_API_KEY', 'VITE_GEMINI_API_KEY is not set.');
  }
  client ??= new GoogleGenAI({ apiKey: config.apiKey });
  return client;
};

const isNonEmptyString = (value: unknown): value is string =>
  typeof value === 'string' && value.trim().length > 0;

/**
 * A partial answer is worse than no answer here: a missing source turns a
 * citation into an unsourced claim. Reject anything off-contract.
 */
function parseResponse(rawText: string): GeminiResponse {
  let payload: unknown;
  try {
    payload = JSON.parse(rawText);
  } catch (cause) {
    throw new SirajError('INVALID_RESPONSE', 'Model returned text that is not valid JSON.', {
      cause,
    });
  }

  const candidate = payload as Partial<GeminiResponse> | null;
  const source = candidate?.source;

  const complete =
    !!candidate &&
    isNonEmptyString(candidate.rephrasedAnswer) &&
    isNonEmptyString(candidate.originalText) &&
    !!source &&
    isNonEmptyString(source.name) &&
    isNonEmptyString(source.reference);

  if (!complete) {
    throw new SirajError('INVALID_RESPONSE', 'Model response did not satisfy the answer contract.');
  }

  return {
    rephrasedAnswer: candidate.rephrasedAnswer!.trim(),
    originalText: candidate.originalText!.trim(),
    source: { name: source.name.trim(), reference: source.reference.trim() },
    aiNote: isNonEmptyString(candidate.aiNote)
      ? candidate.aiNote.trim()
      : 'Generated without a retrieval step; verify the citation before relying on it.',
  };
}

export async function getIslamicBotResponse(
  query: string,
  options: { signal?: AbortSignal } = {},
): Promise<GeminiResponse> {
  const trimmed = query.trim();
  if (!trimmed) {
    throw new SirajError('UNKNOWN', 'Empty question.');
  }

  try {
    const response = await getClient().models.generateContent({
      model: config.model,
      contents: `سؤال المستخدم: "${trimmed}"`,
      config: {
        systemInstruction: SYSTEM_INSTRUCTION,
        responseMimeType: 'application/json',
        responseSchema: RESPONSE_SCHEMA as never,
        abortSignal: options.signal,
      },
    });

    const text = response.text;
    if (!isNonEmptyString(text)) {
      throw new SirajError('INVALID_RESPONSE', 'Model returned an empty payload.');
    }
    return parseResponse(text);
  } catch (error) {
    const wrapped = toSirajError(error);
    if (import.meta.env.DEV) {
      console.error(`[siraj:${wrapped.code}]`, wrapped.cause ?? wrapped);
    }
    throw wrapped;
  }
}
