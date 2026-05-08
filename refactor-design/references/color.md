# Working with Color

Color is where most developer-built UIs fall apart. Not because developers pick bad colors, but because they pick colors without a system. The fix is to define your full palette up front and never deviate from it.

---

## Ditch hex for HSL

Hex colors (`#3b82f6`) tell you nothing about the color. HSL — Hue, Saturation, Lightness — makes color relationships explicit and manipulation intuitive.

```
hsl(H, S%, L%)
  H = hue angle (0–360): 0=red, 120=green, 240=blue
  S = saturation (0–100%): 0%=grey, 100%=vivid
  L = lightness (0–100%): 0%=black, 50%=pure color, 100%=white
```

**Why HSL?**
- To lighten a color: increase L
- To darken a color: decrease L
- To desaturate: decrease S
- To shift hue: adjust H

Hex gives you none of this intuitively. When you see `#93c5fd`, you have to load it into a color picker to understand it. `hsl(213, 97%, 78%)` tells you immediately: a light, vivid, blue.

---

## You need more colors than you think

A complete production palette requires:

| Category | Shades | Purpose |
|----------|--------|---------|
| **Grey** (neutral) | 9 (50–900) | Text, backgrounds, borders, dividers |
| **Primary** | 9 | Brand color, primary actions, links |
| **Success** (green) | 5–9 | Success states, confirmations, positive data |
| **Warning** (yellow/amber) | 5–9 | Warnings, pending states |
| **Danger** (red) | 5–9 | Errors, destructive actions |
| **Info** (blue, optional) | 5–9 | Informational messages |

That's 40–60 color values. Sounds like a lot — it's not. You'll use almost all of them across a real app.

---

## Define shades up front

Each hue needs 9 shades: `50, 100, 200, 300, 400, 500, 600, 700, 800, 900`.

| Shade | Lightness range | Typical use |
|-------|----------------|-------------|
| 50 | 95–97% | Very light background tints |
| 100 | 90–93% | Hover state backgrounds, subtle tints |
| 200 | 83–87% | Borders, light accents |
| 300 | 72–77% | Disabled states, decorative elements |
| 400 | 60–65% | Placeholder text, icons on light bg |
| 500 | 48–53% | Base color — the "pure" version |
| 600 | 38–43% | Darker hover state for actions |
| 700 | 28–33% | Text on light backgrounds, active states |
| 800 | 20–25% | Dark text, dark accents |
| 900 | 13–18% | Near-black text, extreme emphasis |

Use `scripts/color_palette.py` to generate a full palette from a base hue. Or use `assets/color-palettes.json` for pre-built palettes.

---

## Don't let lightness kill your saturation

Light shades at full saturation look vivid. But when you dial up lightness past ~80%, low saturation makes colors look grey and washed out. **Light shades need *more* saturation, not less.**

**Wrong (saturation constant):**
```
hsl(220, 65%, 95%)  -- shade 50, looks grey/washed
hsl(220, 65%, 85%)  -- shade 100
hsl(220, 65%, 50%)  -- shade 500 (base)
```

**Right (saturation boosted for light shades):**
```
hsl(220, 90%, 96%)  -- shade 50, clearly blue-tinted
hsl(220, 80%, 90%)  -- shade 100
hsl(220, 70%, 83%)  -- shade 200
hsl(220, 65%, 50%)  -- shade 500 (base)
hsl(220, 70%, 38%)  -- shade 600 (slightly more saturated when darker)
```

The pattern: **saturation peaks at shade 50 and shade 600–700, and is lowest at shade 400–500**.

---

## Greys don't have to be grey

Pure grey (`hsl(0, 0%, X%)`) feels cold and sterile. Greys that are slightly blue-tinted feel cooler and more modern. Slightly warm greys feel more approachable.

**Cool grey (modern, technical):**
```css
--gray-50:  hsl(220, 14%, 96%);
--gray-100: hsl(220, 13%, 91%);
--gray-200: hsl(220, 11%, 83%);
--gray-300: hsl(220,  9%, 72%);
--gray-400: hsl(220,  7%, 60%);
--gray-500: hsl(220,  6%, 48%);
--gray-600: hsl(220,  8%, 38%);
--gray-700: hsl(220, 10%, 28%);
--gray-800: hsl(220, 13%, 18%);
--gray-900: hsl(220, 15%, 11%);
```

**Warm grey (approachable, editorial):**
```css
--gray-50:  hsl(30, 15%, 97%);
--gray-100: hsl(30, 12%, 92%);
--gray-200: hsl(30,  9%, 84%);
/* ... */
```

**Pro tip:** If your primary color is blue, use cool greys. If it's orange or yellow, use warm greys. Matching grey temperature to your primary hue makes the design feel cohesive.

---

## Accessible doesn't have to mean ugly

WCAG contrast requirements exist to protect readability, not to force ugly colors. It's entirely possible to pass contrast requirements while using beautiful colors.

**Contrast ratios (WCAG AA):**
- Normal text (< 18px): **4.5:1**
- Large text (≥ 18px regular or ≥ 14px bold): **3:1**
- UI components and icons: **3:1**

**Practical accessibility rules:**
1. **Dark text on light background** — shade 700–900 on shade 50–100 — almost always passes.
2. **Light text on dark background** — shade 50–200 on shade 700–900 — almost always passes.
3. **Danger zone:** medium shades (400–500) on white, or light grey text on light backgrounds.

**Quick test approach:**
```python
# Use scripts/audit_design.py --check-contrast to test all text colors
# Or use the WebAIM contrast checker: https://webaim.org/resources/contrastchecker/
```

```css
/* These combinations reliably pass WCAG AA */
color: var(--gray-900); background: var(--gray-50);   /* 17:1 — body text */
color: var(--gray-700); background: white;             /* 10:1 — secondary */
color: var(--gray-500); background: white;             /* 4.5:1 — tertiary */
color: white;           background: var(--primary-600); /* varies — check */
```

---

## Don't rely on color alone

Color can't be the *only* way information is communicated. ~8% of men and ~0.5% of women have some form of color vision deficiency.

**Always pair color with:**
- An icon or shape (red circle × vs. green circle ✓)
- A text label ("Error" not just red styling)
- Position or pattern (in charts, use different line styles)

```html
<!-- Bad: only color signals error -->
<input class="border-red-500" />

<!-- Good: color + icon + text -->
<div>
  <input class="border-red-500" aria-describedby="email-error" />
  <p id="email-error" class="text-red-600 text-sm flex items-center gap-1">
    <svg><!-- error icon --></svg>
    Please enter a valid email address
  </p>
</div>
```

---

## Semantic color usage

**Primary color** — actions the user is most likely to take: primary buttons, active states, links, focus rings, selected states.

**Neutral/grey** — everything else: text, borders, backgrounds, dividers, disabled states, secondary buttons.

**Semantic colors** — status only: green=success/positive, yellow=warning/pending, red=danger/error. Don't use semantic colors decoratively.

```css
/* Status indicators */
.badge-success { background: var(--green-100); color: var(--green-700); }
.badge-warning { background: var(--amber-100); color: var(--amber-700); }
.badge-danger  { background: var(--red-100);   color: var(--red-700); }
.badge-neutral { background: var(--gray-100);  color: var(--gray-700); }
```

---

## Checklist

- [ ] All colors defined in HSL
- [ ] 9 shades defined for each hue (50–900)
- [ ] Saturation boosted on light shades to avoid washed-out appearance
- [ ] Grey palette has a slight tint (cool or warm) to match the brand
- [ ] All text passes WCAG AA contrast (4.5:1 body, 3:1 large)
- [ ] Color never used alone to convey information — always paired with text or icon
- [ ] Semantic colors (red/green/yellow) used for status only, not decoration
