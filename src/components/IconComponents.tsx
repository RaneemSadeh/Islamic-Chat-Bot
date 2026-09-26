import React from 'react';

/**
 * Inline icons, so the bundle carries no icon dependency and every glyph
 * inherits `currentColor` from the element that renders it.
 */

type IconProps = { className?: string };

export const UserIcon: React.FC<IconProps> = ({ className = 'w-6 h-6' }) => (
  <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
  </svg>
);

/** The brand mark: a lamp (سراج) drawn as a flame over an open book. */
export const LampIcon: React.FC<IconProps> = ({ className = 'w-6 h-6' }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
    <path
      d="M12 2.5c1.9 2.2 2.9 3.9 2.9 5.3a2.9 2.9 0 1 1-5.8 0c0-1.4 1-3.1 2.9-5.3z"
      fill="currentColor"
    />
    <path
      d="M3.5 13.5h7a1.5 1.5 0 0 1 1.5 1.5 1.5 1.5 0 0 1 1.5-1.5h7M3.5 13.5v6h7a1.5 1.5 0 0 1 1.5 1.5 1.5 1.5 0 0 1 1.5-1.5h7v-6"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="square"
      strokeLinejoin="miter"
    />
  </svg>
);

export const BotIcon = LampIcon;

export const SendIcon: React.FC<IconProps> = ({ className = 'w-5 h-5' }) => (
  <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M2.01 21 23 12 2.01 3 2 10l15 2-15 2z" />
  </svg>
);

export const InfoIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.6}
    aria-hidden="true"
  >
    <circle cx="12" cy="12" r="9" />
    <path d="M12 11v5.5M12 7.75v.5" strokeLinecap="round" />
  </svg>
);

export const BookIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.6}
    aria-hidden="true"
  >
    <path d="M4 4.5h6a2 2 0 0 1 2 2v13a2 2 0 0 0-2-2H4zM20 4.5h-6a2 2 0 0 0-2 2v13a2 2 0 0 1 2-2h6z" />
  </svg>
);

export const QuoteIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M9.5 6.5 7 12.2V18h5.7v-5.8H9.9l1.8-4.1zm8.6 0-2.5 5.7V18h5.7v-5.8h-2.8l1.8-4.1z" />
  </svg>
);

export const CopyIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.6}
    aria-hidden="true"
  >
    <rect x="9" y="9" width="11" height="11" />
    <path d="M15 5.5H4.5V16" />
  </svg>
);

export const CheckIcon: React.FC<IconProps> = ({ className = 'w-4 h-4' }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={2}
    aria-hidden="true"
  >
    <path d="m5 12.5 4.5 4.5L19 7" strokeLinecap="square" />
  </svg>
);

export const WarningIcon: React.FC<IconProps> = ({ className = 'w-5 h-5' }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.7}
    aria-hidden="true"
  >
    <path d="M12 4.5 21 19.5H3z" strokeLinejoin="miter" />
    <path d="M12 10v4.25M12 16.8v.4" strokeLinecap="round" />
  </svg>
);
