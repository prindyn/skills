---
name: pixel-perfect
description: Build pixel-perfect UI implementations from a project's DESIGN.md design-system file. Use this skill whenever the user asks to implement, scaffold, refine, or audit UI from a DESIGN.md, mentions "pixel perfect", "match the design", "build the design", "honor the design tokens", wants components/pages/screens that exactly match a design system spec, or wants a precision audit (alignment, spacing, on-pixel edges, typography, contrast, corner radii) of existing markup. Also use it when the user says they have brand/style instructions in DESIGN.md and wants code that obeys them. If DESIGN.md is missing, this skill will help create a stub before proceeding.
license: MIT
metadata:
  hermes:
    tags: [design, design-system, ui, pixel-perfect, design-md, frontend, css, tailwind, accessibility, ustwo]
    related_skills: [design-md, popular-web-designs, claude-design, sketch]
---

# Pixel Perfect

Translate a project's `DESIGN.md` into UI code that is **pixel-precise,
token-faithful, and accessible** — and audit existing code against the same
spec. The skill marries two ideas:

1. **DESIGN.md as the contract.** A plain-text design-system file at the
   project root (Google's `design.md` spec) defines colors, typography,
   spacing, radii, and components. Every value the UI uses must come from
   there. No off-spec hex codes, no guessed paddings.
2. **Pixel Perfect Precision principles** (ustwo handbook). On-pixel edges,
   real alignment over auto-alignment, x-height-centered text, correct outer
   radii (`outer = inner + border`), worst-case content (longest copy /
   translations), and visual-hierarchy-driven layout.

## When to use this skill

Trigger on phrasings like:

- "Build/implement/scaffold the [page|component|screen] from our DESIGN.md"
- "Make this match the design", "make it pixel perfect", "honor the tokens"
- "Audit this HTML/JSX against DESIGN.md"
- "Generate the homepage following our design system"
- "We have a DESIGN.md — build X"

If the user mentions a design system file or token spec but it isn't called
DESIGN.md, still use this skill — DESIGN.md is the canonical name but the
workflow is the same for any token JSON/YAML. Convert it to DESIGN.md as
step 1.

## Hard requirements

This skill **requires `DESIGN.md` at the project root**. Without it there is
no source of truth and the output cannot be pixel-perfect by definition.

If `DESIGN.md` is missing:

1. Tell the user, briefly, what DESIGN.md is (1–2 sentences) and that it's
   needed.
2. Offer two paths:
   - **(a)** scaffold one from `templates/DESIGN.starter.md` and ask them
     to fill in brand details, OR
   - **(b)** if they have a Figma/PDF/screenshot/style guide, infer tokens
     from it into a draft DESIGN.md.
3. Do not start writing UI code until DESIGN.md exists.

For the formal authoring workflow (lint, diff, WCAG), the `design-md` skill
handles that side. This skill consumes DESIGN.md and produces UI.

## Workflow

Follow these steps in order. Steps 1–3 are setup; 4–6 are the build loop.

### 1. Locate and read DESIGN.md

```bash
test -f DESIGN.md && echo "found" || echo "missing"
```

Read it fully. Pay attention to:

- `colors:` — these are the **only** colors allowed in output, except where
  DESIGN.md explicitly delegates (e.g. user-uploaded media).
- `typography:` — every text style maps to one of these named scales
  (`h1`, `body-md`, etc.). Do not invent sizes.
- `spacing:` and `rounded:` — every margin, padding, gap, and corner radius
  must reference one of these.
- `components:` — high-emphasis components have explicit specs and variants
  (`button-primary-hover` etc. — sibling keys, never nested).
- The Markdown body's rationale ("why" behind values) — use it to break ties
  when a layout decision isn't fully token-determined.

If DESIGN.md is malformed, run `scripts/validate_design_md.py DESIGN.md`
before proceeding. Fix or report errors.

### 2. Extract tokens to a usable form

Run `scripts/extract_tokens.py DESIGN.md --format <css|tailwind|json>` to
emit:

- **CSS variables** (`:root { --color-primary: #1A1C1E; … }`)
- **Tailwind theme extension** (drop into `tailwind.config.js`)
- **Plain JSON** (for JS frameworks, design-token pipelines)

Pick the format matching the user's project. If the project already has a
generated theme file from `npx @google/design.md export`, prefer that.

### 3. Pick a stack-appropriate template

`templates/` contains starting points:

- `html-page.html` — vanilla HTML + CSS variables
- `react-tailwind.tsx` — React component using Tailwind classes that map to
  DESIGN.md tokens
- `vue-css.vue` — Vue SFC with scoped CSS using vars
- `DESIGN.starter.md` — a stub DESIGN.md when the project has none

These are starting points, not finished output. Adapt them to the user's
existing code style and folder layout. Do **not** dump a template into a
project that already has its own conventions — match what's there.

### 4. Build with Pixel Perfect discipline

Apply the principles from `references/principles.md` while writing code.
The high-leverage ones, distilled:

- **Tokens only.** Every color, size, radius, and spacing value must be a
  reference to a DESIGN.md token (or a CSS variable / Tailwind class
  derived from one). If you find yourself typing a raw hex or `padding:
  13px`, stop and find the token.
- **On-pixel edges.** Use whole-pixel widths/heights. Avoid sub-pixel
  positioning that produces blurred borders. Watch for transforms
  (`translate(-50%, -50%)`) on odd-dimension elements.
- **x-height alignment for text vs. icons.** When centering text against a
  bullet, icon, or shape, account for the typeface's x-height — the visual
  center is below the geometric center for most fonts. Use
  `vertical-align`, `line-height`, or a small translate to correct.
- **Outer radius rule.** When nesting a bordered shape inside another,
  `outer-radius = inner-radius + border-width` keeps the stroke uniform.
  Don't reuse the inner radius as the outer.
- **Worst-case content.** Render every component at least once with the
  longest plausible copy (German "Einstellungen" instead of "Settings",
  Portuguese "Configurações", a 2-line translation, an empty state, an
  error state). Use `WWW…` for max width and `Åy` for max height when
  reasoning about text bounds.
- **Equilateral triangles.** If you need a CSS triangle and want it
  equilateral, scale the height to **86.6%** of the geometric height.
- **States are first-class.** For every interactive element, ship default
  + hover + active + focus + disabled. DESIGN.md gives you the variants
  (`button-primary-hover` etc.); don't skip them.
- **Visual hierarchy via contrast and weight, not size alone.** Push
  secondary content back with lower contrast, not just smaller type.
- **Affordance.** Buttons should look pressable. Scrollable regions should
  hint at overflow (a fading edge, partial content). Inputs should look
  inputtable.

`references/principles.md` covers the full set with examples for each.

### 5. Self-audit before showing the user

Run `scripts/audit_pixels.py <html-or-source-glob> --design DESIGN.md` to
catch:

- Hex/rgb literals not in the token set
- Off-token spacing values (e.g. `padding: 13px` when the scale is 4 / 8 /
  16 / 24)
- Hard-coded font sizes outside the typography scale
- Missing focus states on `<button>` / `<a>` / `[role="button"]`
- WCAG contrast failures on token combinations actually used in the
  components

Fix anything it flags. The audit is non-destructive — it prints findings
with file:line and why.

Then run through `references/qa-checklist.md` (the human checklist, ~25
items grouped by category). It's quick — most of it is yes/no. Don't skip
the worst-case-content row; that's where most "looks great in mock, breaks
in prod" bugs live.

### 6. Hand off

When presenting the result:

1. Show the file(s) you wrote/changed.
2. Show the audit output (or "clean — 0 findings").
3. Call out any DESIGN.md gaps you noticed (e.g. "spec doesn't define a
   destructive button variant — I used `colors.error` from `colors:` but
   you may want a `button-destructive` component entry"). These are
   feedback for the design-system author, not blockers.
4. If you added new tokens, edit DESIGN.md to register them — do not
   leave one-off values in the implementation.

## Framework guidance

`references/frameworks.md` covers per-framework specifics: how to wire
DESIGN.md tokens into Tailwind, CSS Modules, styled-components, vanilla
extract, SwiftUI, and Jetpack Compose. Read it when the user's stack is
not vanilla HTML.

## Why this skill exists

Most "design system" output from LLMs drifts: plausible hex codes that
weren't in the brand palette, paddings that vary by 1–2px between
components, focus states that were skipped, German text that overflows.
Each of those is small; together they're the difference between a UI
that feels designed and one that feels generated. Treating DESIGN.md as a
strict contract — and running an audit that catches token drift before
the user sees the output — closes that gap. The pixel-perfect principles
from the ustwo handbook are what designers do reflexively; encoding them
explicitly lets a model match that instinct on the first pass.

## Files in this skill

- `references/design-md-spec.md` — token format, section order, lint rules
  (mirror of the Google spec, included so the model doesn't need network)
- `references/principles.md` — the ustwo Pixel Perfect Precision
  principles, grouped and explained
- `references/qa-checklist.md` — the pre-handoff checklist
- `references/frameworks.md` — token wiring per framework
- `scripts/validate_design_md.py` — schema + reference + WCAG check (no
  network, no npm)
- `scripts/extract_tokens.py` — DESIGN.md → CSS / Tailwind / JSON
- `scripts/audit_pixels.py` — scan source files for off-token values
- `templates/DESIGN.starter.md` — DESIGN.md stub
- `templates/html-page.html` — vanilla HTML + CSS-vars starter
- `templates/react-tailwind.tsx` — React + Tailwind starter
- `templates/vue-css.vue` — Vue SFC starter
