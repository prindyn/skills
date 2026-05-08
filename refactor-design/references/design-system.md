# Building a Design System

A design system is a constrained set of design tokens — spacing, type, color, shadows, radii — plus the components built from them. Getting the tokens right first makes everything else consistent automatically.

---

## Output formats

The same token system can be expressed in three ways. Choose based on the project's stack:

| Stack | Format | Generate with |
|-------|--------|--------------|
| Vanilla CSS / PostCSS | CSS custom properties | `scripts/generate_tokens.py --format css` |
| Tailwind CSS | `tailwind.config.js` | `scripts/generate_tokens.py --format tailwind` |
| CSS-in-JS (Emotion, Stitches) | JS object | `scripts/generate_tokens.py --format js` |

Use `templates/design-tokens.css` and `templates/tailwind.config.js` as hand-editable starting points.

---

## Token categories

### Primitive tokens

Raw values — no semantic meaning yet:

```css
/* Colors */
--blue-50:  hsl(217, 91%, 97%);
--blue-500: hsl(217, 91%, 60%);
--blue-900: hsl(217, 91%, 17%);

/* Spacing */
--space-4: 1rem;
--space-8: 2rem;

/* Font sizes */
--font-base: 1rem;
--font-2xl: 1.5rem;
```

### Semantic tokens

Map primitive tokens to roles. These are what components actually use:

```css
/* Text roles */
--text-primary:   var(--gray-900);
--text-secondary: var(--gray-600);
--text-tertiary:  var(--gray-400);
--text-disabled:  var(--gray-300);
--text-inverse:   var(--gray-50);

/* Background roles */
--bg-base:        var(--gray-50);  /* page background */
--bg-surface:     white;           /* cards, panels */
--bg-subtle:      var(--gray-100); /* subtle backgrounds within surfaces */
--bg-overlay:     hsla(220, 40%, 10%, 0.4);

/* Border roles */
--border-default: var(--gray-200);
--border-strong:  var(--gray-300);
--border-focus:   var(--primary-500);

/* Interactive */
--color-primary:        var(--blue-600);
--color-primary-hover:  var(--blue-700);
--color-primary-subtle: var(--blue-50);
--color-danger:         var(--red-600);
--color-success:        var(--green-600);
--color-warning:        var(--amber-500);
```

---

## Component tokens

The last layer — tokens specific to a single component type. These override semantic tokens for component-level consistency:

```css
/* Button */
--btn-radius:          6px;
--btn-font-weight:     600;
--btn-padding-y:       var(--space-2);
--btn-padding-x:       var(--space-4);

/* Input */
--input-radius:        6px;
--input-border:        var(--border-default);
--input-border-focus:  var(--border-focus);
--input-padding-y:     var(--space-2);
--input-padding-x:     var(--space-3);

/* Card */
--card-radius:         8px;
--card-padding:        var(--space-6);
--card-shadow:         var(--shadow-sm);
--card-border:         var(--border-default);
```

---

## Border radius scale

Like spacing, radii should come from a scale:

```css
--radius-sm:   4px;   /* Tags, badges, small inputs */
--radius-md:   6px;   /* Buttons, inputs */
--radius-lg:   8px;   /* Cards, modals */
--radius-xl:   12px;  /* Feature cards, large modals */
--radius-2xl:  16px;  /* Hero elements, large callouts */
--radius-full: 9999px; /* Pills, avatars, circular buttons */
```

**Personality signals:**
- Small radii (`2–4px`) → precise, corporate, technical
- Medium radii (`6–8px`) → modern, balanced (default for most apps)
- Large radii (`12–16px`) → friendly, consumer, playful

---

## Transition tokens

Consistent animation makes interactions feel cohesive:

```css
--duration-fast:    100ms; /* hover color changes, tiny feedback */
--duration-normal:  200ms; /* most UI transitions */
--duration-slow:    300ms; /* modal enter/exit, larger movements */
--duration-slower:  500ms; /* page-level transitions */

--ease-default:    cubic-bezier(0.4, 0, 0.2, 1); /* material easing */
--ease-spring:     cubic-bezier(0.175, 0.885, 0.32, 1.275); /* springy */
--ease-decelerate: cubic-bezier(0, 0, 0.2, 1); /* modal enter */
--ease-accelerate: cubic-bezier(0.4, 0, 1, 1);  /* modal exit */
```

---

## Focus ring token

Focus rings must be visible and consistent. Define them once:

```css
--ring-offset:   2px;
--ring-width:    2px;
--ring-color:    var(--primary-500);

/* Apply with: */
.focusable:focus-visible {
  outline: var(--ring-width) solid var(--ring-color);
  outline-offset: var(--ring-offset);
  border-radius: inherit;
}
```

---

## Generating design tokens

Run the generator script for a complete token file:

```bash
# CSS custom properties
python scripts/generate_tokens.py \
  --primary-hue 220 \
  --gray-hue 220 \
  --format css \
  --output tokens.css

# Tailwind config
python scripts/generate_tokens.py \
  --primary-hue 220 \
  --gray-hue 220 \
  --format tailwind \
  --output tailwind.config.js

# JavaScript object
python scripts/generate_tokens.py \
  --primary-hue 220 \
  --gray-hue 220 \
  --format js \
  --output tokens.js
```

Or use a secondary hue for an accent color:
```bash
python scripts/generate_tokens.py \
  --primary-hue 220 \   # blue
  --accent-hue 280 \    # purple
  --gray-hue 220 \
  --format tailwind
```

---

## Checklist

- [ ] Primitive tokens defined for all values (no naked hex/px values in components)
- [ ] Semantic tokens map primitives to roles (text-primary, bg-surface, etc.)
- [ ] Border radius scale defined and used consistently
- [ ] Focus ring token defined and applied to all interactive elements
- [ ] Animation duration and easing tokens defined
- [ ] Token file exported in the format matching the project's stack
