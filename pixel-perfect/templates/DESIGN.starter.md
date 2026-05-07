---
version: alpha
name: ProjectName
description: One-line tagline describing the brand's character.
colors:
  # Primary brand color — used for the most important interactive surfaces.
  primary: "#1A1C1E"
  # Secondary — supporting text, borders, secondary actions.
  secondary: "#6C7278"
  # Tertiary / accent — the single high-emphasis call-to-action color.
  tertiary: "#B8422E"
  # Neutral / canvas — the background most content sits on.
  neutral: "#F7F5F2"
  # Semantic colors. Don't reuse these for branding.
  success: "#1F7A3A"
  warning: "#C28A1B"
  error: "#B33A3A"
  info: "#1F5FB3"
typography:
  h1:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  h2:
    fontFamily: Inter
    fontSize: 2rem
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body-lg:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: 400
    lineHeight: 1.5
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.04em"
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  "2xl": 48px
  "3xl": 64px
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
  button-primary-disabled:
    backgroundColor: "#FFFFFF"
    textColor: "{colors.secondary}"
  button-secondary:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: 12px
  card:
    backgroundColor: "#FFFFFF"
    rounded: "{rounded.lg}"
    padding: 24px
  input:
    backgroundColor: "#FFFFFF"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: 12px
---

## Overview

Replace this paragraph with a short statement of the brand's voice — the
*why* behind the choices in the front matter. Two or three sentences is
plenty. The point of this section is to give an agent enough rationale to
break ties when an implementation choice isn't fully determined by the
tokens alone.

Example: "ProjectName is a tools-for-thought app aimed at researchers. The
visual language is sober and precise — tight type, restrained color, ample
white space. Tertiary 'Iron Red' is the single high-emphasis accent and
should be used sparingly: one primary call-to-action per screen."

## Colors

- **Primary (#1A1C1E):** Deep ink. Used for headlines, primary text, and
  hover states on the accent button.
- **Secondary (#6C7278):** Mid-grey for secondary text, dividers, icons.
- **Tertiary (#B8422E):** "Iron Red" — the only high-emphasis accent.
  Reserved for the primary call-to-action and critical badges.
- **Neutral (#F7F5F2):** Warm off-white canvas color. Most content sits on
  this background.
- **Semantic:** `success`, `warning`, `error`, `info` should be used for
  status communication only. Do not use `success` as a brand accent —
  green carries meaning.

## Typography

Inter for everything. The scale is geometric (1.125× per step). `label`
uses tight letter-spacing for ALL CAPS UI labels. Body text is set at
1.5 line-height for legibility; headings drop to 1.1–1.2 because they're
expected to be 1–2 lines.

When centering text on a button or icon, align by **x-height**, not cap
height — Inter's x-height-to-cap ratio is high enough that bounding-box
centering looks low.

## Layout

- Base unit: 8px. The spacing scale is multiples (4 / 8 / 16 / 24 / 32 /
  48 / 64). All margins, paddings, and gaps must reference one of these.
- Container max-width: 1200px on desktop, full-bleed below 768px with a
  16px gutter.
- Vertical rhythm: section spacing of `spacing.2xl` (48px) on desktop,
  `spacing.xl` (32px) on mobile.

## Components

`button-primary` is the only high-emphasis action on a page. There should
be no more than one per visible viewport. `button-secondary` is for
all other actions. Both have hover, focus-visible, and disabled
variants — implement all three or the focus state will be missing for
keyboard users.

`card` is the default container for grouped content. Border-radius is
`rounded.lg` (16px) — when nesting bordered shapes inside a card, the
inner radius should be 16 - padding - border-width per the
outer-radius-rule.

## Do's and Don'ts

- **Do** use the spacing scale exclusively. If you need 13px, the design
  is wrong, not the implementation.
- **Don't** introduce new hex colors in implementation code. Add them
  to this DESIGN.md first, then use the token.
- **Do** ship every interactive element with default + hover +
  focus-visible + active + disabled states.
- **Don't** suppress focus outlines without an equivalent replacement.
- **Do** test with the longest plausible string for every label — the
  German translation of "Settings" is "Einstellungen", a 75% increase.
- **Don't** rely on color alone for status — pair red/green/yellow with
  shapes (✓ × ! i) for accessibility.
