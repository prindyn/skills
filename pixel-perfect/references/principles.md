# Pixel Perfect Principles

A condensed, agent-ready version of ustwo's *Pixel Perfect Precision* handbook
(v3, ustwo, public). The original is illustration-heavy; this is the
text-only ruleset — what to actually do when implementing.

Read top-to-bottom once when you start a new project, then jump back to a
specific section when an audit flags a problem.

## 1. Sharp edges (on-pixel rendering)

Straight edges should land on whole pixels. Blurred half-pixel borders are
the most common pixel-perfect failure.

Causes:

- A 1px border on an element with sub-pixel positioning (e.g. flex/grid
  rounding, percent widths that compute to fractional values).
- `transform: translate(-50%, -50%)` on an element with odd-pixel
  width/height — moves the edge by 0.5px.
- Browser-zoom levels other than 100%, or HiDPI rendering mismatches.

Fixes:

- Use whole-pixel widths/heights for any element with a visible border.
- For centered elements with odd width, round-down by 1px or use
  `transform: translate(calc(-50% + 0.5px), calc(-50% + 0.5px))` (rare —
  almost always cleaner to make the dimension even).
- Prefer `outline` over a 1px ghost border when you need a focus ring
  that doesn't shift layout.

## 2. Alignment and spacing

Once edges are sharp, the next layer is *consistent* alignment across
screens. Title bars, back buttons, footers, and primary actions must sit
at the same x/y across every page.

Implement:

- A spacing scale (4 / 8 / 16 / 24 / 32 …) defined once in DESIGN.md
  `spacing:` and referenced everywhere. **No raw `padding: 13px` ever.**
- A grid (CSS grid, container query, or design-system `<Stack>` / `<Inset>`
  primitives). Rows/columns snap to the spacing scale.
- One global container width / max-width per breakpoint, not one per page.

## 3. HSB-first color reasoning

When deriving shade variants of a brand color, work in HSB (a.k.a. HSL):
keep Hue constant, adjust Saturation/Brightness. The numbers are
human-readable and the perceptual relationships hold. RGB makes you guess.

`oklch()` in modern CSS is even better for perceptual lightness — use it
when generating tonal scales programmatically.

DESIGN.md stores the canonical hex values; how you derive them is up to
you, but document the formula in the prose body so future authors don't
re-derive ad-hoc.

## 4. Worst-case content

Every component must survive realistic worst-case content. If you only
test with the lorem-ipsum the designer chose, you ship a fragile UI.

Things to render at least once:

- Longest plausible string. For UI labels, German is usually +30–75%
  longer than English ("Settings" → "Einstellungen", "Configurações").
- Empty states (no items in a list, no search results).
- Error states (failed network, invalid input, expired session).
- Loading states (skeleton, spinner — avoid layout shift).
- Single character + 200-character names.
- Missing avatars / images.

Quick text-bounds heuristics from the handbook:

- `Åy` measures the **maximum vertical extent** of a typeface (ascender +
  descender). Use it when computing line-box heights.
- `WWW…` to a width measures the **maximum horizontal extent** — if `WWW`
  fits, any string of the same character count fits.

## 5. Aligning text to objects

Vertically centering text inside a button is not "center the bounding
box". The visual weight of most typefaces is the **x-height**, which sits
*below* the cap height's geometric center. Centering by bounding box
makes the text look slightly low.

Two correct approaches, depending on the typeface and content:

- **x-height alignment** for mixed-case body content (preferred for most
  buttons, chips, badges).
- **Cap-height alignment** for ALL CAPS labels and numeric-only content
  (no descenders to balance).

In CSS terms, both are achievable with `line-height` matched to the
button height, plus a small `padding-top` correction (1–2px) when the
typeface's metrics demand it. Or use a font-relative unit like `cap` or
`ex` if you have full control.

Pick one rule per project and apply it everywhere — consistency beats
local optimum.

## 6. Aligning text on buttons (cap-vs-x)

Three common rules; pick one and stick with it across the whole UI:

1. Cap height + descender (button height = ascent + descent of font).
2. x-height (button height = x-height + symmetric padding).
3. Cap height + x-height (split the difference; works well for
   numerals + lowercase mixed).

Document the choice in DESIGN.md's typography rationale.

## 7. Object states

Every interactive element ships at least these states. Skipping any of
them is a bug, not a polish item:

- **Default** (resting)
- **Hover** (pointer devices)
- **Focus-visible** (keyboard) — *do not* suppress with `outline: none`
  unless you replace it with something equally visible
- **Active / Pressed**
- **Disabled** (with cursor + opacity + aria-disabled)
- **Loading** (where applicable, e.g. submit buttons)
- **Selected** (toggles, segmented controls)

DESIGN.md encodes these as sibling component entries
(`button-primary`, `button-primary-hover`, `button-primary-disabled`).
Read all variants before implementing.

## 8. Borders and corner radii

The single most often-broken rule: when you nest a bordered shape inside
another, the **outer radius must equal `inner-radius + border-width`**,
not the inner radius itself.

```
   wrong                  right
┌─────────┐            ╭─────────╮
│ ┌─────┐ │            │ ╭─────╮ │
│ │     │ │            │ │     │ │
│ └─────┘ │            │ ╰─────╯ │
└─────────┘            ╰─────────╯
border keeps          border stays
constant width        uniform width
geometrically         visually
```

CSS:

```css
.card { border-radius: 16px; padding: 8px; border: 2px solid var(--c); }
.card > .inner { border-radius: 6px; /* 16 - 8 - 2 = 6 */ }
```

The reverse case — outer is fixed, you derive inner — can produce
inner radii of 0 (square corners) when the math gives a negative. In
that case, "fillet" with a small radius (2–4px) for visual harmony even
though it's mathematically wrong.

## 9. Equilateral triangles in CSS

A naïve CSS triangle (`border-left/-right/-bottom` trick) with equal x
and y dimensions is **isoceles**, not equilateral. To make it
equilateral, scale the height to **86.6%** of the width:

```css
.tri { width: 16px; border-bottom: calc(16px * 0.866) solid var(--c);
       border-left: 8px solid transparent; border-right: 8px solid transparent; }
```

Or use SVG with a proper equilateral path — usually simpler.

## 10. Color and shape semantics

Colors and shapes carry meaning in digital UI. Do not subvert these
without strong reason:

- **Green / check** = success, confirm, go
- **Red / X / triangle (filled)** = error, destructive, stop
- **Yellow / triangle (outline)** = warning
- **Blue / circle (i)** = info, neutral

If DESIGN.md defines `colors.success`, `colors.error`, `colors.warning`,
`colors.info`, use those for these meanings only. Don't use the success
green as a brand accent.

## 11. Visual hierarchy

What the eye lands on first is decided by:

1. **Contrast** (highest contrast wins)
2. **Size** (then largest)
3. **Weight** (then heaviest)
4. **Color** (then most saturated)
5. **Position** (then top-left in LTR, top-right in RTL)

Push secondary content back with **lower contrast first**, smaller size
second. Reducing size while keeping contrast high produces "loud, small
text" which looks shouty.

## 12. Affordance

Make interactive elements look interactive:

- **Buttons** — slight elevation, pressed state, hover transition. Even
  in flat designs, a 50ms hover background shift signals affordance.
- **Scrollable regions** — fade an edge or show partial overflow content
  to communicate "more here".
- **Inputs** — visible border, distinct background, cursor change on
  hover.
- **Links** — underline on hover at minimum; underline always for body
  links.

The opposite — flat, undifferentiated text-as-button — is a usability
regression dressed as minimalism.

## 13. Copy

UI text is part of the design. Bad copy can't be fixed by good layout.

- Address the user as a person, not a system.
- Use sentence case for body labels, Title Case for proper nouns and
  major headings only.
- Verbs on buttons should match the user's intent ("Save changes", not
  "Submit").
- Errors should explain what to do, not just what failed.

Match the tone documented in DESIGN.md's prose body. If there isn't one,
ask.

## 14. Motion

Motion adds character and reinforces affordance, but is easy to overdo.

- Default duration: 150–250ms for most UI transitions; 300–400ms for
  larger spatial moves.
- Easing: `cubic-bezier(0.2, 0, 0, 1)` (Material standard) or the
  project's defined curve. Avoid `linear` for natural-feeling motion.
- **Respect `prefers-reduced-motion`** — wrap non-essential motion in
  `@media (prefers-reduced-motion: no-preference)`.
- Animate transforms and opacity, not `width` / `top` / `left` (those
  cause layout).

## 15. Testing on the actual device

Browser DevTools mobile emulation lies. Real device differs in:

- Pixel density and physical size — text that's "16px and looks fine"
  on a laptop is genuinely small on a 6.1" phone at arm's length.
- Touch target sizing — minimum 44×44pt iOS, 48×48dp Android.
- Color rendering — OLED blacks, P3 gamuts.

Always do a final pass on the real target before calling something done.

## 16. Organisation

Code organisation matters as much as visual organisation. Keep:

- Token definitions in **one place** (the DESIGN.md → generated theme),
  imported by everything else. No duplicated palettes.
- Components in a flat, named structure (`button.tsx`, `card.tsx`),
  with variants as props, not separate files per state.
- Naming consistent with DESIGN.md's component keys (`button-primary`
  → `<Button variant="primary" />`).

When something gets messy, clean it before adding more. Mess compounds.
