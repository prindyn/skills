# Designing Text

Typography is the backbone of UI design. Get it right and everything else becomes easier. Get it wrong and no amount of visual polish will save the design.

---

## Establish a type scale

Limit font sizes to 6–8 values with clear, named purposes. More than that and designers start picking sizes arbitrarily, which breaks visual consistency.

**Recommended scale:**

| Token | Size | Weight | Line-height | Purpose |
|-------|------|--------|-------------|---------|
| `text-xs` | 12px / 0.75rem | 400–500 | 1.5 | Captions, helper text, badges |
| `text-sm` | 14px / 0.875rem | 400 | 1.5 | Small labels, secondary UI text |
| `text-base` | 16px / 1rem | 400 | 1.625 | Body text (default) |
| `text-lg` | 18px / 1.125rem | 400–500 | 1.5 | Lead paragraphs, prominent body |
| `text-2xl` | 24px / 1.5rem | 600–700 | 1.3 | Card headings, section titles |
| `text-3xl` | 30px / 1.875rem | 700 | 1.25 | Page subheadings |
| `text-4xl` | 36px / 2.25rem | 700–800 | 1.2 | Page headings |
| `text-5xl` | 48px / 3rem | 700–900 | 1.1 | Hero / display headings |

**Never** pick a font size that isn't on this scale. If a design calls for something "between" two sizes, either pick the closer one or add a new step with a clear purpose.

### CSS implementation
```css
:root {
  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;
  --text-2xl:  1.5rem;
  --text-3xl:  1.875rem;
  --text-4xl:  2.25rem;
  --text-5xl:  3rem;
}
```

---

## Use good fonts

Font choice signals personality and quality immediately.

**System font stack** (fastest, always looks native):
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
             "Helvetica Neue", Arial, sans-serif;
```

**Recommended Google Fonts pairings:**

| Personality | Heading | Body | Use for |
|-------------|---------|------|---------|
| Modern / SaaS | Inter | Inter | Dashboards, apps, tools |
| Editorial | Fraunces | Source Serif 4 | Blogs, publications |
| Playful / Consumer | Plus Jakarta Sans | DM Sans | Startups, consumer apps |
| Technical | JetBrains Mono | Inter | Dev tools, code-heavy UIs |
| Premium | Playfair Display | Lato | E-commerce, luxury brands |

**Font loading (Google Fonts):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## Keep line length in check

Body text lines longer than 75 characters are hard to read — the eye loses its place at the start of the next line.

```css
/* The ch unit is "width of the 0 character" — good proxy for character count */
.prose {
  max-width: 65ch; /* ~65 characters wide — ideal reading width */
}

/* For UI components with non-prose text, use fixed pixel max-widths */
.card-description {
  max-width: 480px;
}
```

**Signs of a line-length problem:**
- Body copy that stretches the full width of a 1440px screen
- `max-width: 100%` on `.content` — that's not a max-width, that's no constraint

---

## Line-height is proportional to font size

Larger text needs *less* line-height. Smaller text needs *more*. The reason: larger glyphs have more white space built into them, and long lines of large text with lots of line-height feel overwhelming.

```css
/* Display / hero headings */
.text-5xl { line-height: 1.1; }
.text-4xl { line-height: 1.2; }

/* Section headings */
.text-3xl { line-height: 1.25; }
.text-2xl { line-height: 1.3; }

/* Body text (needs more room for readability) */
.text-base { line-height: 1.625; }
.text-sm   { line-height: 1.5; }

/* Tiny text (even more space proportionally) */
.text-xs   { line-height: 1.5; }
```

---

## Baseline align mixed-size text

When two text elements of different sizes appear side by side (e.g. a price `$48` next to a unit `/mo`), align them on their **baselines**, not their centers or tops.

```css
/* Baseline alignment with flex */
.price-wrapper {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price-main  { font-size: 3rem; font-weight: 700; }
.price-unit  { font-size: 1rem; color: var(--text-secondary); }
```

**Why not center-align?** Centering mixed sizes creates an optical illusion where text appears to float at different vertical positions — the eye expects baselines to align.

---

## Align text with readability in mind

Rules of thumb:
- **Left-align** long-form body text — always. Right-align strains the eye.
- **Center-align** is fine for short UI strings: button labels, headings in hero sections, empty states, toasts.
- **Right-align** numbers in table columns — this keeps decimal points and digits in consistent positions.
- **Avoid justify** (`text-align: justify`) — it creates uneven word spacing that harms readability.

```css
/* Numbers in tables: right-align for column scanning */
td.numeric { text-align: right; font-variant-numeric: tabular-nums; }

/* Use tabular numbers for data that changes or needs to align in columns */
.stat-value { font-variant-numeric: tabular-nums; }
```

---

## Letter-spacing

Small adjustments to `letter-spacing` make a disproportionate difference in polish.

**Headlines and display text** — tighten slightly:
```css
.text-5xl { letter-spacing: -0.04em; }
.text-4xl { letter-spacing: -0.03em; }
.text-3xl { letter-spacing: -0.02em; }
.text-2xl { letter-spacing: -0.01em; }
```

**Small all-caps labels** — loosen:
```css
.label-caps {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em; /* adds readability at small sizes */
}
```

**Body text** — leave at `0` (default). Adjusting body letter-spacing usually makes things worse.

---

## Not every link needs a color

In body text, underlining links is often enough. Coloring every link creates visual noise — every occurrence of blue fights for attention against the primary actions and data.

```css
/* Inline links in body prose — underline only */
.prose a {
  color: inherit;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.prose a:hover {
  color: var(--color-primary-600);
}

/* Navigation links, action links — color + weight */
.action-link {
  color: var(--color-primary-600);
  font-weight: 500;
  text-decoration: none;
}
```

---

## Checklist

- [ ] All font sizes come from the type scale (no off-scale sizes)
- [ ] Line-height decreases as font size increases
- [ ] Body text max-width set to `~65ch`
- [ ] Mixed-size inline text is baseline-aligned
- [ ] Headlines have slightly negative letter-spacing; all-caps labels have positive
- [ ] Body text is left-aligned; numeric columns are right-aligned
- [ ] Font family chosen to match the product's personality
- [ ] `font-variant-numeric: tabular-nums` on data values that need to align
