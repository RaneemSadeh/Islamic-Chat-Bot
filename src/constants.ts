/** Copy and fixtures that belong to the product, not to any one component. */

export const SUGGESTED_QUESTIONS: readonly string[] = [
  'ما حكم الصلاة في أول الوقت؟',
  'ما شروط صحة الصيام لمن يسافر في رمضان؟',
  'كيف تُحسب زكاة المال المدّخر؟',
  'ما آداب طلب العلم عند السلف؟',
];

export const DISCLAIMER =
  'هذه الإجابات مولّدة آلياً لأغراض التعلّم والبحث، وليست فتوى. راجع المصدر المذكور وأهل العلم قبل العمل بها.';

export const EMPTY_STATE = {
  title: 'ابدأ بسؤال',
  body: 'اكتب سؤالك بالعربية، وستحصل على شرح مبسّط مع النص الأصلي والمصدر الذي استند إليه.',
} as const;
