# Creating Depth & Finishing Touches

The difference between a design that feels "flat and lifeless" and one that feels polished often comes down to depth cues and finishing details. Neither requires overblown visuals — small, precise touches go a long way.

---

## Creating Depth

### Emulate a consistent light source

Real-world objects look three-dimensional because light hits them from above and slightly in front. Shadows fall down and slightly to the right of the light source. Surfaces facing the light are lighter; surfaces facing away are darker.

Pick **one** light source direction and stick to it throughout the design. The convention is light from above-left.

```css
/* Consistent light source: offset-x slightly right, offset-y down */
--shadow-sm:  0 1px  2px 0 hsla(220, 40%, 10%, 0.05);
--shadow-md:  0 4px  6px -1px hsla(220, 40%, 10%, 0.10),
              0 2px  4px -2px  hsla(220, 40%, 10%, 0.10);
--shadow-lg:  0 10px 15px -3px hsla(220, 40%, 10%, 0.10),
              0 4px  6px -4px  hsla(220, 40%, 10%, 0.10);
--shadow-xl:  0 20px 25px -5px hsla(220, 40%, 10%, 0.10),
              0 8px  10px -6px hsla(220, 40%, 10%, 0.10);
--shadow-2xl: 0 25px 50px -12px hsla(220, 40%, 10%, 0.25);
```

**Note on shadow color:** Don't use pure black (`rgba(0,0,0, X)`). Use a dark, slightly saturated version of your brand's hue. It looks natural, not muddy.

---

### Shadows convey elevation

Map your shadows to elevation levels. Use elevation consistently — elements at the same conceptual layer should always use the same shadow.

| Elevation level | Shadow | Use for |
|----------------|--------|---------|
| Flat (0) | none | Cards resting on the page, table rows |
| Raised (1) | `--shadow-sm` | Buttons, inputs, subtle cards |
| Floating (2) | `--shadow-md` | Dropdowns, tooltips, popovers |
| Overlay (3) | `--shadow-lg` | Sticky headers, sidebars |
| Modal (4) | `--shadow-xl` | Modals, dialogs, full sidebars |
| Extreme (5) | `--shadow-2xl` | Full-page overlays, drawer panels |

```css
.card          { box-shadow: none; border: 1px solid var(--gray-200); }
.card-raised   { box-shadow: var(--shadow-sm); }
.dropdown      { box-shadow: var(--shadow-md); }
.sticky-header { box-shadow: var(--shadow-lg); }
.modal         { box-shadow: var(--shadow-xl); }
```

---

### Shadows have two parts

The most convincing shadows use two layers:
1. A **direct shadow** — close, sharp, low opacity (the umbra)
2. An **ambient shadow** — large, blurry, very low opacity (the penumbra)

```css
/* Two-part shadow */
box-shadow:
  0  1px  3px 0   hsla(220, 40%, 10%, 0.12),   /* direct */
  0  1px  2px -1px hsla(220, 40%, 10%, 0.08);  /* ambient */
```

This is what makes Tailwind's `shadow-md` look better than a naive single-layer shadow.

---

### Even flat designs can have depth

Depth doesn't require shadows. Background color differences create subtle layering:

```css
/* Page → section → card → element */
body          { background: hsl(220, 14%, 96%); } /* gray-50 */
.panel        { background: white; }
.card         { background: hsl(220, 14%, 98%); } /* off-white */
.card-header  { background: hsl(220, 13%, 95%); } /* slightly darker */
```

**Overlap elements** to suggest layering:
```css
.card-avatar {
  margin-top: -1.5rem;  /* pulls the avatar up into the card header */
  position: relative;
  z-index: 1;
}
```

---

## Finishing Touches

### Supercharge the defaults

Style the elements browsers render badly by default:
- `<select>` — use a custom appearance with a chevron icon
- `<input type="range">` — custom track and thumb
- `<input type="checkbox">` / `<input type="radio">` — use a CSS-only or JS-based custom component
- `<details>` / `<summary>` — custom disclosure triangles
- `scrollbar` — style it in WebKit browsers

```css
/* Custom checkbox example */
input[type="checkbox"] {
  appearance: none;
  width: 1rem;
  height: 1rem;
  border: 1.5px solid var(--gray-300);
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 150ms;
}

input[type="checkbox"]:checked {
  background: var(--primary-600);
  border-color: var(--primary-600);
  background-image: url("data:image/svg+xml,..."); /* checkmark */
}

input[type="checkbox"]:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

---

### Add color with accent borders

A simple `border-left` or `border-top` in the primary color is one of the cheapest ways to add visual interest and brand personality.

```css
/* Left accent border on a card */
.card-accent {
  border-left: 4px solid var(--primary-500);
  padding-left: var(--space-6);
}

/* Top accent on a section header */
.section-header-accent {
  border-top: 3px solid var(--primary-500);
  padding-top: var(--space-4);
}

/* Alert-style accent (with matching tinted background) */
.alert-info {
  border-left: 4px solid var(--blue-500);
  background: var(--blue-50);
  padding: var(--space-4) var(--space-6);
  border-radius: 0 8px 8px 0;
}
```

---

### Decorate your backgrounds

Empty backgrounds feel unfinished. Subtle decoration adds richness without distraction.

**Subtle dot grid:**
```css
.bg-dots {
  background-image: radial-gradient(var(--gray-300) 1px, transparent 1px);
  background-size: 20px 20px;
}
```

**Subtle line grid:**
```css
.bg-grid {
  background-image:
    linear-gradient(var(--gray-100) 1px, transparent 1px),
    linear-gradient(90deg, var(--gray-100) 1px, transparent 1px);
  background-size: 40px 40px;
}
```

**Gradient blob (hero sections):**
```css
.bg-blob {
  background:
    radial-gradient(ellipse 80% 60% at 20% -20%, hsl(220, 80%, 96%), transparent),
    radial-gradient(ellipse 60% 80% at 80% 110%, hsl(280, 60%, 96%), transparent),
    white;
}
```

---

### Don't overlook empty states

Empty states are the first thing a new user sees. A blank table or empty list with no explanation is confusing and unmotivating.

Every empty state should have:
1. An **illustration or icon** — even a simple SVG icon is better than nothing
2. A **heading** — brief, explains what's missing
3. A **description** — one sentence about what will appear here
4. A **primary action** — helps the user get started immediately

See `templates/component-empty-state.html` for a complete implementation.

```html
<!-- Minimal empty state structure -->
<div class="empty-state">
  <div class="empty-state-icon"><!-- SVG icon --></div>
  <h3 class="empty-state-heading">No projects yet</h3>
  <p class="empty-state-body">
    Create your first project to start tracking work.
  </p>
  <a href="/new" class="btn-primary">Create project</a>
</div>
```

---

### Use fewer borders

Borders are the designer's crutch — a way to separate things when spacing hasn't done its job. Look at every border and ask: could I remove this and use spacing instead?

**Replace borders with:**
```css
/* Instead of a border between list items: */
.list-item + .list-item { padding-top: var(--space-4); } /* spacing only */

/* Instead of a bordered card: */
.card {
  background: white;
  border-radius: 8px;
  box-shadow: var(--shadow-sm); /* shadow implies edges */
}

/* Instead of a horizontal rule between sections: */
.section + .section { margin-top: var(--space-16); } /* space alone */
```

**When borders are still useful:**
- Separating the header area of a card from its body (within the same card)
- Table row separators in dense data tables
- Input focus rings (not decorative, functional)
- Subtle page/section dividers where background changes aren't available

---

### Think outside the box

Some elements can break expected patterns to add visual delight:
- Slightly rotate an illustration or badge (`transform: rotate(-3deg)`)
- Offset a card shadow asymmetrically to suggest a specific direction
- Use a `border-radius` that matches the brand personality (tight=corporate, generous=friendly)
- Make the active navigation item "punch out" with a contrasting background

```css
/* A "stacked cards" depth effect */
.card-stack {
  position: relative;
}
.card-stack::before {
  content: "";
  position: absolute;
  inset: -4px -4px 4px;
  background: var(--primary-100);
  border-radius: inherit;
  z-index: -1;
  transform: rotate(-1deg);
}
```

---

## Checklist

- [ ] Consistent light source for all shadows (down and slightly right)
- [ ] 5 elevation levels defined with distinct box-shadow tokens
- [ ] Shadows use dark tinted hsl color, not pure black
- [ ] At least one finishing detail added: accent border, background texture, or layered depth
- [ ] All empty states have icon + heading + description + action
- [ ] Borders replaced with spacing where possible
- [ ] Custom styles applied to browser-default form elements
