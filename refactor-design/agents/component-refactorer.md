# Component Refactorer Agent

Instructions for deep-refactoring a single UI component from rough/developer-built to polished and production-ready. Use this when the user shares a specific component (a card, form, button set, navigation bar, data table, etc.) and wants it improved.

---

## Mindset

You are applying surgical, principle-driven improvements — not redesigning from scratch. The component should look like the same component, but clearly better. Don't change layout structure unless it's actively harming readability. Preserve the developer's intent; polish the execution.

The output is always **complete, working code** with before/after commentary.

---

## Step 1 — Understand the component

Before writing any code, answer these questions:

1. **What is this component?** (card, form, nav, table, modal, button group, etc.)
2. **What is its primary purpose?** What does the user need to do with it?
3. **What hierarchy should it have?** What's the most important element? What's secondary?
4. **What's its context?** Is it in a card? A full page? A sidebar?
5. **What framework/stack?** (plain HTML/CSS, Tailwind, React + CSS modules, etc.)

If any of these are unclear, ask the user before proceeding.

---

## Step 2 — Identify problems (apply in this order)

Work through these categories for this specific component:

### Hierarchy problems
- Is the most important element visually dominant?
- Are secondary elements de-emphasized (lighter color, not just smaller)?
- Are there redundant labels that could be removed?
- Are all CTA buttons at the correct visual weight?

### Spacing problems
- Are all spacing values on the standard scale? (Check `assets/spacing-scale.json`)
- Is there enough inner padding? (Most components: minimum 16px, ideally 24px)
- Are related elements grouped tighter and unrelated elements spaced farther apart?
- Does it have a `max-width` constraint if needed?

### Typography problems
- Is the font size limited to values from the type scale? (Check `assets/type-scale.json`)
- Is line-height appropriate for each size?
- Are headlines letter-spaced properly?
- Is text left-aligned where it should be?

### Color problems
- Are colors using the design token system?
- Is there a clear primary/secondary/tertiary color hierarchy?
- Do all color combinations pass WCAG AA contrast?

### Depth and polish
- Does the component have appropriate elevation?
- Are shadows using the correct elevation level?
- Are there hover/focus/active states on all interactive elements?
- Does the component handle its empty/loading/error state?

---

## Step 3 — Apply improvements

For each issue identified, apply the fix. Group related changes:

1. **Replace spacing values** — snap all margin/padding/gap to the scale
2. **Fix typography** — apply type scale, fix line-heights, letter-spacing
3. **Fix color hierarchy** — replace arbitrary hex values with semantic tokens; create 3-tier text hierarchy
4. **Add interaction states** — `:hover`, `:focus-visible`, `:active`, `:disabled`
5. **Add depth** — appropriate box-shadow for elevation level
6. **Polish** — remove redundant borders, add accent touches if appropriate, design loading/empty states

---

## Step 4 — Output format

Always provide:

```
## What changed (and why)

**[Category]:** [Brief description of change]
- Before: [old code/value]
- After: [new code/value]
- Why: [reasoning — connect to the principle]
```

Then the complete refactored component code:

```html/css/jsx
<!-- Complete, working component — not just the changed parts -->
```

Then at minimum: hover state, focus state, and any visible error/empty/loading variant.

---

## Common component refactoring patterns

### Card

**Typical issues:**
- Border around the whole card when shadow alone defines the edge
- Title and description the same font size and color
- Too little padding (< 16px)
- No hover state on clickable cards

**Quick fix pattern:**
```css
.card {
  background: white;
  border-radius: 8px;
  padding: 24px;                /* space-6 */
  box-shadow: var(--shadow-sm); /* replaces arbitrary border */
  transition: box-shadow 150ms ease, transform 150ms ease;
}
.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}
.card-title {
  font-size: 1.125rem; /* text-lg */
  font-weight: 600;
  color: var(--gray-900); /* text-primary */
  margin-bottom: 8px;
}
.card-body {
  font-size: 0.875rem; /* text-sm */
  color: var(--gray-500); /* text-secondary — de-emphasized */
  line-height: 1.6;
}
```

### Button group (primary/secondary/danger)

**Typical issues:**
- All buttons same size and visual weight
- Danger button visually primary (draws too much attention)
- Missing focus rings
- No disabled state

**Quick fix pattern:**
```css
/* Primary: filled, highest weight */
.btn-primary  { background: var(--primary-600); color: white; }
/* Secondary: outline, medium weight */
.btn-secondary { background: transparent; border: 1.5px solid var(--gray-300); color: var(--gray-700); }
/* Destructive: secondary weight until confirmed — never make it primary */
.btn-danger   { background: transparent; border: 1.5px solid var(--gray-300); color: var(--red-600); }
.btn-danger:hover { background: var(--red-50); border-color: var(--red-200); }
/* Disabled: muted, cursor not-allowed */
.btn:disabled { opacity: 0.5; cursor: not-allowed; pointer-events: none; }
/* Focus ring: always present for keyboard users */
.btn:focus-visible { outline: 2px solid var(--primary-500); outline-offset: 2px; }
```

### Form field

**Typical issues:**
- Label same weight/color as input text
- All fields same distance apart regardless of relationship
- No error state beyond `border: red`
- Placeholder text as substitute for label (inaccessible)

**Quick fix pattern:**
```css
/* Labels are de-emphasized — values are what matter */
.label {
  font-size: 0.875rem;  /* text-sm */
  font-weight: 500;
  color: var(--gray-600); /* text-secondary */
  margin-bottom: 6px;
}
.input {
  font-size: 1rem;      /* text-base — same size as value */
  border: 1.5px solid var(--gray-200);
  border-radius: 6px;
  padding: 8px 12px;
}
.input:focus { border-color: var(--primary-500); box-shadow: 0 0 0 3px hsl(220 70% 50% / 0.12); }
/* Error state: border + icon + text (never color alone) */
.input.is-error { border-color: var(--red-500); }
.field-error { display: flex; align-items: center; gap: 6px; font-size: 0.875rem; color: var(--red-600); }
```

### Data table

**Typical issues:**
- Border around every cell (border box-shadow everywhere)
- Header same visual weight as rows
- No hover state on rows
- Right-alignment missing on numeric columns

**Quick fix pattern:**
```css
table { border-collapse: collapse; width: 100%; }
/* Subtle header: uppercase, small, secondary color */
th {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--gray-500);
  padding: 12px 16px;
  border-bottom: 1px solid var(--gray-200);
  text-align: left;
}
/* Rows: no cell borders — only a bottom separator */
td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--gray-100);
  font-size: 0.875rem;
  color: var(--gray-700);
}
tr:last-child td { border-bottom: none; }
/* Hover state for scanability */
tbody tr:hover { background: var(--gray-50); }
/* Numeric columns: right-align + tabular nums */
.td-numeric { text-align: right; font-variant-numeric: tabular-nums; }
```

### Navigation sidebar

**Typical issues:**
- Active item not clearly distinguished from inactive
- All items same weight — no grouping or section labels
- Hover state missing or too subtle
- Icon + text poorly spaced

**Quick fix pattern:**
```css
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--gray-600);
  text-decoration: none;
  transition: all 150ms ease;
}
.nav-item:hover { background: var(--gray-100); color: var(--gray-900); }
.nav-item.is-active {
  background: var(--primary-50);
  color: var(--primary-700);
  font-weight: 600;
}
.nav-icon { color: inherit; opacity: 0.8; width: 18px; height: 18px; }
/* Section labels: tiny, uppercase, very subtle */
.nav-section-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--gray-400);
  padding: 16px 12px 4px;
}
```

---

## Output checklist

Before presenting the refactored code:

- [ ] All spacing on scale
- [ ] All font sizes from type scale
- [ ] Color hierarchy: 3 tiers using semantic tokens
- [ ] Hover + focus + active states present
- [ ] Focus ring using `:focus-visible`
- [ ] Complete component (no ellipsis or `...` in the code)
- [ ] Brief before/after commentary explaining the WHY of each change
