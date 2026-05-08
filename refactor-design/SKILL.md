---
name: refactor-design
description: Transform rough, developer-built UIs into polished, production-ready interfaces using proven visual design principles from Refactoring UI. Use this skill whenever the user wants to improve UI appearance, refactor styles or CSS, fix visual design problems, make a page "look better" or "more professional", create a design system, generate a color palette, build a spacing scale, set up a type scale, or audit an existing interface. Trigger even when the user only says "clean this up", "make it look nicer", "the design looks off", or "it feels amateurish" — those are exactly the scenarios this skill was built for.
compatibility: Web projects — HTML/CSS, React, Vue, Svelte, Tailwind CSS, plain CSS custom properties, or any CSS-in-JS setup.
metadata:
  author: skill-creator
  version: "1.0"
  source: Refactoring UI by Adam Wathan & Steve Schoger
---

# Refactor Design

Systematic process for turning a working-but-rough UI into something that looks intentional and production-ready. Grounded in *Refactoring UI* (Wathan & Schoger) — practical, code-focused design advice, not abstract theory.

## Core principle

Good UI design is mostly about **restraint and systems**. Limit your choices up front (spacing scale, type scale, color palette), then make everything consistent. Most amateur-looking UIs fail because they have 20 different font sizes, arbitrary pixel values for spacing, and colors picked ad-hoc. Fix the system first; the components follow.

---

## Reference files (read as needed)

| File | When to read it |
|------|----------------|
| `references/hierarchy.md` | Visual hierarchy feels flat or everything competes for attention |
| `references/layout-spacing.md` | Spacing feels cramped, inconsistent, or arbitrary |
| `references/typography.md` | Text feels hard to read, sizes feel random, lines are too long |
| `references/color.md` | Colors look muddy, palette feels ad-hoc, accessibility concerns |
| `references/depth-finishing.md` | UI feels flat or unpolished; empty states, borders, shadows |
| `references/design-system.md` | Building a token system from scratch (CSS vars, Tailwind config) |

---

## Workflow

### 1. Audit — diagnose before prescribing

Run `scripts/audit_design.py` on the project's HTML/CSS, or mentally check these heuristics:

- **Hierarchy**: Can you tell what's most important in 3 seconds? Is there one clear primary action per section?
- **Spacing**: Are spacings arbitrary pixels or from a scale? Is there enough breathing room?
- **Typography**: More than 6 font sizes? Lines longer than 75 characters? Centered body text?
- **Color**: Colors defined as one-off hex values? No shades defined up front? Grey text on colored backgrounds?
- **Borders**: Borders everywhere? Could spacing or background color replace them?
- **Empty states**: What does the page look like before any data?

Read `agents/design-auditor.md` for a thorough component-by-component audit protocol.

### 2. Establish design tokens

Before touching any component, lock down the system. Use `scripts/generate_tokens.py` to scaffold the token file, or copy from `templates/design-tokens.css` / `templates/tailwind.config.js`.

**Spacing scale** (geometric, base-4):
```
4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 192 · 256px
```

**Type scale** (6–8 sizes max, each with a clear semantic role):
```
12px caption · 14px small · 16px body · 18px lead
24px h3 · 30px h2 · 36px h1 · 48px display
```

**Color palette** — 9 shades (50–900) per hue, defined in HSL. See `references/color.md` for palette construction. Use `scripts/color_palette.py` to generate any palette from a base hue.

### 3. Fix visual hierarchy

Read `references/hierarchy.md`. The most common fixes:

- Replace font-size-only hierarchy with **weight + color + size together**
- De-emphasize secondary text with a lighter color rather than making primary text louder
- Remove decorative labels — let values speak for themselves
- Ensure one and only one primary CTA per section

### 4. Fix layout and spacing

Read `references/layout-spacing.md`.

- Start with **too much** white space and pull back — cramped always looks worse
- Snap every spacing value to the spacing scale
- Set a `max-width` on content (prose: `65ch`; page content: `768–1024px`)
- Reduce spacing inside a group *and* increase spacing between groups to show relationships

### 5. Fix typography

Read `references/typography.md`.

- Cap body text at `max-width: 65ch`
- Line-height: `1.5–1.7` for body, `1.2–1.3` for headlines
- Baseline-align mixed-size text (not center-align)
- Letter-spacing: tighten headlines (`-0.025em`), loosen all-caps labels (`0.05–0.1em`)

### 6. Fix color

Read `references/color.md`.

- Rebuild palette in HSL
- Use pre-built palettes from `assets/color-palettes.json` as a starting point
- Check contrast ratios: 4.5:1 for body text, 3:1 for large text (WCAG AA)
- Never convey information by color alone — pair with icon, label, or pattern

### 7. Polish and finish

Read `references/depth-finishing.md`.

- Define 5 elevation levels with box-shadow tokens
- Replace border-heavy layouts with spacing + subtle background shifts
- Design empty states — they're the first thing new users see
- Add personality cheaply: a colored `border-left` or `border-top` accent, a subtle background texture, a well-chosen icon

---

## Output rules

- **Match the project stack** — Tailwind classes, CSS custom properties, or CSS-in-JS depending on what's already in use.
- **Complete snippets only** — always output the full component, not just changed lines.
- **Include all states** — hover, focus, active, disabled. Don't leave interactive elements stateless.
- **Mobile-first** — default to single-column, then add responsive variants.
- **Accessible** — sufficient contrast, focus rings, semantic HTML, no color-only cues.

When refactoring existing code, show a before/after diff with a brief explanation of *why* each change was made — this builds the user's design intuition over time.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/generate_tokens.py` | Scaffold design token file (CSS vars, Tailwind config, or JS) |
| `scripts/audit_design.py` | Scan HTML/CSS files and report hierarchy, spacing, and color issues |
| `scripts/color_palette.py` | Generate a full 9-shade HSL color palette from a base hue |

## Templates

| Template | Use for |
|----------|--------|
| `templates/design-tokens.css` | CSS custom properties design system |
| `templates/tailwind.config.js` | Tailwind CSS design system configuration |
| `templates/component-card.html` | Well-structured card component |
| `templates/component-form.html` | Polished form with proper hierarchy |
| `templates/component-empty-state.html` | Empty state component |

## Agents

- `agents/design-auditor.md` — Full design audit protocol for an existing UI
- `agents/component-refactorer.md` — Deep-dive refactoring of a single component
