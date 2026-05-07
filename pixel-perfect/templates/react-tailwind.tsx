/**
 * Pixel Perfect starter — React + Tailwind.
 *
 * Setup:
 *   1. Generate theme.json from DESIGN.md:
 *        python scripts/extract_tokens.py DESIGN.md --format tailwind > theme.json
 *   2. Wire it into tailwind.config.js:
 *        const theme = require('./theme.json');
 *        module.exports = {
 *          theme: { extend: { colors: theme.colors, spacing: theme.spacing,
 *                              borderRadius: theme.borderRadius,
 *                              fontFamily: theme.fontFamily,
 *                              fontSize: theme.fontSize } }
 *        };
 *   3. Use the named tokens (bg-primary, p-md, rounded-sm, text-h1) — never
 *      ad-hoc values like p-[13px] or bg-[#1a1c1e].
 *   4. Run scripts/audit_pixels.py over your built source before shipping.
 */

import { type ButtonHTMLAttributes, type ReactNode } from 'react';

// -----------------------------------------------------------------------------
// Button
// -----------------------------------------------------------------------------

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary';
  children: ReactNode;
};

/**
 * Implements every variant from DESIGN.md.components.button-* including:
 * default, hover, focus-visible, active, disabled, plus a 44px min-height
 * touch target.
 */
export function Button({
  variant = 'primary',
  className = '',
  children,
  ...props
}: ButtonProps) {
  const base =
    'inline-flex items-center justify-center min-h-[44px] px-md py-sm ' +
    'font-semibold rounded-sm transition-colors duration-150 ' +
    'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 ' +
    'disabled:cursor-not-allowed motion-reduce:transition-none';

  const variants = {
    primary:
      'bg-tertiary text-white ' +
      'hover:bg-primary ' +
      'focus-visible:outline-primary ' +
      'active:translate-y-px ' +
      'disabled:bg-neutral disabled:text-secondary',
    secondary:
      'bg-neutral text-primary ' +
      'hover:bg-neutral/80 ' +
      'focus-visible:outline-primary ' +
      'active:translate-y-px ' +
      'disabled:opacity-50',
  } as const;

  return (
    <button className={`${base} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}

// -----------------------------------------------------------------------------
// Card
// -----------------------------------------------------------------------------

type CardProps = {
  children: ReactNode;
  className?: string;
};

/**
 * Outer-radius rule: card uses rounded-lg (16px), padding is p-lg (24px).
 * If you nest a bordered shape inside, give it rounded-sm (4px) — never
 * reuse the outer 16px on inner shapes.
 */
export function Card({ children, className = '' }: CardProps) {
  return (
    <div className={`bg-white rounded-lg p-lg border border-black/10 ${className}`}>
      {children}
    </div>
  );
}

// -----------------------------------------------------------------------------
// Page composition
// -----------------------------------------------------------------------------

export default function ExamplePage() {
  return (
    <main className="bg-neutral text-primary min-h-screen">
      <div className="max-w-[1200px] mx-auto px-md py-2xl">
        <h1 className="text-h1 font-bold mb-lg">Example heading</h1>

        {/*
          During QA, swap this with:
            - a 200-word paragraph (worst-case length)
            - a single-character title (worst-case shortness)
            - the German translation (worst-case width)
        */}
        <p className="max-w-[65ch] mb-md">
          Replace this body text with realistic worst-case content during the
          audit pass.
        </p>

        <Card>
          <p className="mb-md">
            Card content using only token-driven values. No raw hex, no
            ad-hoc spacing.
          </p>
          <Button variant="primary">Primary action</Button>
        </Card>
      </div>
    </main>
  );
}
