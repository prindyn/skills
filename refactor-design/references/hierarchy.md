# Visual Hierarchy

Visual hierarchy is the single most powerful tool in UI design. When it works, users instantly know what to look at, what's most important, and what to do next. When it fails, everything competes and nothing stands out.

---

## Not all elements are equal

Every interface should have a clear primary element — the thing the user is *most* likely there to do. Define three tiers:

- **Primary**: one per section/page. Highest visual weight. Usually the main action or the most critical piece of information.
- **Secondary**: supporting information. Still important, but clearly subordinate.
- **Tertiary**: fine print, metadata, optional actions. Present but not loud.

The mistake most developers make is giving every element equal visual weight because they're all equally important *functionally*. Visual weight is about guiding attention, not about the importance of the content in the abstract.

---

## Size is not the only dimension

Three levers control visual weight:

1. **Font size** — the most obvious, but overused. Don't scale up the primary element so much you break the rhythm.
2. **Font weight** — `font-weight: 700` on a normal-size element pops more than you expect. Reserve bold for 1–2 elements per section.
3. **Color** — dark text vs. medium-grey text vs. light-grey text creates a natural 3-tier hierarchy without touching font size at all.

**Common mistake:** Using a font size hierarchy like `32px → 24px → 18px → 14px → 12px` for 5 hierarchy levels. Instead, use:
- Large font size for the primary heading
- Same or slightly smaller size for body, but high contrast color
- Same body size for secondary text, but medium-grey color
- Small font for tertiary info, light-grey

---

## Don't use grey text on colored backgrounds

Grey text (`color: #9ca3af`) on a white background works because the lightness contrast carries the hierarchy signal.

On a colored background, grey text loses this signal and can actually become unreadable or feel muddy. Two correct approaches:

**Option 1 — Reduce opacity:**
```css
/* Instead of a hard grey hex: */
color: rgba(255, 255, 255, 0.75); /* 75% opacity white on dark bg */
color: rgba(0, 0, 0, 0.5);        /* 50% opacity black on light colored bg */
```

**Option 2 — Use a color-compatible shade:**
Pick a lighter/darker shade of the background hue rather than a neutral grey.
```css
/* On a blue-500 background: */
color: hsl(220, 70%, 90%); /* light blue, not grey */
```

---

## Emphasize by de-emphasizing

One of the most counterintuitive but effective techniques: **to make the important thing stand out, make the less important things quieter** rather than making the important thing louder.

Before (everything loud):
```css
.title     { font-size: 24px; font-weight: 700; color: #111; }
.subtitle  { font-size: 20px; font-weight: 600; color: #222; }
.body      { font-size: 16px; font-weight: 500; color: #333; }
.meta      { font-size: 14px; font-weight: 500; color: #444; }
```

After (primary stays, rest de-emphasized):
```css
.title     { font-size: 24px; font-weight: 700; color: hsl(222, 47%, 11%); }
.subtitle  { font-size: 16px; font-weight: 400; color: hsl(222, 20%, 40%); }
.body      { font-size: 16px; font-weight: 400; color: hsl(222, 15%, 45%); }
.meta      { font-size: 13px; font-weight: 400; color: hsl(222, 10%, 65%); }
```

---

## Labels are a last resort

Labels create visual noise. Before adding a label, ask: does the value make its own meaning clear?

**Remove the label when:**
- The context makes it obvious (`$1,200 / month` — clearly a price)
- The value has a well-understood format (`jan 12, 2024` — clearly a date)
- The label and value together read naturally as prose (`Joined 3 years ago`)

**Keep the label when:**
- The value is ambiguous without it (`"12"` — 12 what?)
- Multiple similar values appear side by side and need differentiation

**When you do use labels, de-emphasize them:**
```css
.label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: hsl(222, 15%, 55%); /* lighter than the value */
}
.value {
  font-size: 16px;
  font-weight: 500;
  color: hsl(222, 47%, 11%);
}
```

---

## Separate visual hierarchy from document hierarchy

HTML semantics (`<h1>`, `<h2>`, `<p>`) define document structure for accessibility and SEO. Visual hierarchy is about appearance. These don't have to match.

An `<h3>` can visually look like small, grey label text. A `<p>` can look like the most prominent element on the screen.

```html
<!-- Semantically an h2, but visually subtle -->
<h2 class="text-xs font-semibold uppercase tracking-widest text-slate-400">
  Recent Activity
</h2>

<!-- Semantically a span, but visually prominent -->
<span class="text-4xl font-bold text-slate-900">$48,200</span>
```

Use `aria-*` attributes to fill in any accessibility gaps when visual and semantic hierarchy diverge.

---

## Balance weight and contrast

Dark, heavy elements (bold black text, filled buttons) draw the eye. Use this intentionally:

- **Primary action**: filled button, bold, high-contrast color
- **Secondary action**: outline button or ghost button, medium contrast
- **Destructive action**: secondary visual weight until confirmed — don't make it visually primary just because it's dangerous

**Icon + text balance:**
A bold icon next to light body text feels unbalanced. Either lighten the icon color or reduce its size. The icon should support the text, not compete with it.

```css
/* Icon and text feel balanced */
.icon { color: hsl(222, 15%, 55%); width: 16px; }
.label { font-size: 14px; color: hsl(222, 47%, 11%); }
```

---

## Checklist

- [ ] Can you identify the primary element at a glance? Is there only one per section?
- [ ] Do you use weight and color (not just size) to create hierarchy?
- [ ] Is secondary/tertiary content visibly lighter, not just slightly smaller?
- [ ] Are labels removed or minimized where the value is self-explanatory?
- [ ] Does grey text appear only on neutral backgrounds?
- [ ] Do interactive elements have clear visual weight that signals their importance?
