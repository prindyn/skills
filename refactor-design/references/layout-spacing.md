# Layout and Spacing

Spacing is what separates designs that look professional from ones that feel cramped and thrown-together. The key insight: **more whitespace almost always looks better**, and using a consistent spacing scale makes everything feel intentional.

---

## Establish a spacing scale

Stop picking arbitrary pixel values. Define a scale once and stick to it. Every padding, margin, gap, and size value should come from this list.

**Recommended scale (base-4, geometric):**

| Token | Value | Use case |
|-------|-------|----------|
| `space-1` | 4px | Tight gaps between related micro-elements (icon + label) |
| `space-2` | 8px | Default compact padding, close relationships |
| `space-3` | 12px | Comfortable inner padding for small components |
| `space-4` | 16px | Default padding, standard gap |
| `space-6` | 24px | Breathing room inside sections |
| `space-8` | 32px | Separation between distinct elements |
| `space-12` | 48px | Between sections within a view |
| `space-16` | 64px | Between major sections |
| `space-24` | 96px | Hero/feature-level vertical breathing room |
| `space-32` | 128px | Max vertical breathing room |

**Why a geometric scale?** The ratios between steps feel natural. The jump from 4→8 is +4px; from 64→96 is +32px. Proportionally similar, which trains the eye.

### CSS custom properties
```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-24: 6rem;     /* 96px */
  --space-32: 8rem;     /* 128px */
}
```

---

## Start with too much white space

When in doubt, add more whitespace than feels necessary — then pull it back if it feels *too* airy. 

It's almost impossible to make a design feel too roomy in practice. But cramped designs feel rushed, untrustworthy, and harder to read.

**Practical default inner padding for common components:**

```css
/* Card */
.card { padding: var(--space-6); } /* 24px — start here */

/* Button */
.btn { padding: var(--space-2) var(--space-4); } /* 8px 16px */

/* Input */
.input { padding: var(--space-2) var(--space-3); } /* 8px 12px */

/* Section gap */
.section + .section { margin-top: var(--space-16); } /* 64px */
```

---

## You don't have to fill the whole screen

Wide content doesn't mean better content. Constraining content width often:
- Improves readability (shorter line lengths)
- Creates natural breathing room
- Focuses attention

**Recommended max-widths:**

```css
/* Prose / long-form content */
.prose { max-width: 65ch; }

/* UI content area */
.content { max-width: 768px; }

/* Wide layouts (dashboards, data tables) */
.wide { max-width: 1280px; }

/* Center any of these */
.container {
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--space-6);
  padding-right: var(--space-6);
}
```

Narrow columns surrounded by plenty of negative space often look *more* polished than full-width layouts.

---

## Grids are overrated

CSS Grid is powerful, but forcing everything into a uniform grid often fights the content's natural shape. Use grids for:
- Multi-column layouts where columns should be equal
- Dashboards with card tiles
- Image galleries

Don't use grids for:
- Forms (use vertical stacks with consistent spacing)
- Navigation menus
- Content that flows naturally

**Sidebar layouts:**
A fixed-width sidebar + flexible content area is often better than a percentage-based grid:

```css
.layout {
  display: grid;
  grid-template-columns: 240px 1fr; /* fixed sidebar, fluid content */
  gap: var(--space-8);
}
```

---

## Relative sizing doesn't scale

Using `em` units for spacing creates inconsistency: a `.card` with `padding: 1.5em` will have different actual padding depending on its font-size, which cascades in unexpected ways.

Prefer:
- `rem` for anything that should stay consistent regardless of local font size
- `ch` for line-length constraints
- Logical values (`padding-inline`, `margin-block`) for RTL support

```css
/* Avoid — padding depends on local font-size */
.card { padding: 1.5em; }

/* Better — always 24px regardless of context */
.card { padding: 1.5rem; }
```

---

## Avoid ambiguous spacing

Spacing communicates relationship. Elements that are close together feel related; elements that are far apart feel separate.

**The rule:** The space *inside* a group should be smaller than the space *between* groups.

```css
/* Form field group: label and input are close, fields are further apart */
.field + .field { margin-top: var(--space-6); }  /* 24px between fields */
.field label    { margin-bottom: var(--space-1); } /* 4px label-to-input */

/* Section: section heading close to its content, far from the next section */
.section-heading { margin-bottom: var(--space-4); } /* 16px */
.section + .section { margin-top: var(--space-16); } /* 64px */
```

**Common mistake:** Equal spacing everywhere. If a form has `margin: 16px` between every element — between the section heading and first field, between fields, between field groups — nothing groups and the form reads as a flat list.

---

## Height sizing

Avoid setting explicit heights on content containers unless you have a specific reason. Let content determine height; use `min-height` when you need a minimum.

```css
/* Bad — breaks when content is long */
.card { height: 200px; overflow: hidden; }

/* Good — grows with content, has a minimum */
.card { min-height: 120px; padding: var(--space-6); }
```

For equal-height cards in a grid:
```css
.card-grid { display: grid; align-items: stretch; }
.card { display: flex; flex-direction: column; }
.card-body { flex: 1; } /* pushes footer to bottom */
```

---

## Checklist

- [ ] All spacing values come from the defined scale (no arbitrary px values)
- [ ] Plenty of padding inside components — at least 16px, usually 24px
- [ ] Content has a max-width set (`65ch` for prose, `768-1280px` for UI)
- [ ] Spacing clearly groups related elements (less inside groups, more between groups)
- [ ] No `em`-based spacing outside of typography-specific contexts
- [ ] Explicit heights avoided in favor of padding + `min-height`
