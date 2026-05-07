# Pixel Perfect QA Checklist

Run through this list before handing UI back to the user. Most items are
yes/no. Skim it, fix anything that fails, then ship.

This list is the human-readable mirror of `scripts/audit_pixels.py`. The
script catches mechanical failures (raw hex, off-token spacing); this
checklist catches the things only a careful read-through finds.

## A. Token fidelity

- [ ] Every color value in the output is a CSS variable, Tailwind alias,
      or token lookup — **no raw hex/rgb literals**.
- [ ] Every spacing value (margin, padding, gap, top/left positioning)
      maps to a `spacing.*` token from DESIGN.md.
- [ ] Every corner radius maps to a `rounded.*` token.
- [ ] Every font-size and line-height maps to an entry in DESIGN.md
      `typography:`.
- [ ] No "almost-the-token" drift (e.g. `padding: 15px` when the scale
      is 4 / 8 / 16). If you needed 15, the spec is wrong, not the impl
      — go fix DESIGN.md.

## B. Pixel precision

- [ ] All visible borders sit on whole pixels (no `transform:
      translate(-50%)` on odd-width elements with 1px borders).
- [ ] No accidental sub-pixel widths from flex/grid percentages on
      elements with borders.
- [ ] Outer corner radii on bordered nested shapes follow `outer = inner
      + border-width`.
- [ ] Triangles are equilateral if they're meant to be (height = 86.6%
      of width).

## C. Typography

- [ ] No widows/orphans on critical headings.
- [ ] `line-height` set explicitly (not `normal`) for body and headings.
- [ ] Hyphenation is off (`hyphens: none`) unless intentional — most
      mobile devices don't render hyphens consistently.
- [ ] Text vertical-aligned to objects uses x-height (or is documented
      to use cap-height for ALL CAPS / numerics).
- [ ] Long-word handling (`word-break` / `overflow-wrap`) on
      user-generated content fields.

## D. Worst-case content

- [ ] Each component renders correctly with the longest plausible string
      (try a German or Portuguese translation of every label).
- [ ] Each list/grid renders correctly when **empty**.
- [ ] Each form field renders correctly with an **error** message
      attached.
- [ ] Each loading state has no layout shift between skeleton and real
      content.
- [ ] Avatars/images have a fallback when missing.

## E. States

For every interactive element:

- [ ] Default
- [ ] Hover (pointer)
- [ ] Focus-visible (keyboard) — outline / ring is **not** suppressed
      without replacement
- [ ] Active / pressed
- [ ] Disabled (opacity + cursor + `aria-disabled` + actual `disabled`
      attribute where applicable)
- [ ] Loading (where applicable, e.g. submit buttons)
- [ ] Selected (toggles, segmented controls)

## F. Accessibility (the load-bearing kind)

- [ ] Color is not the only signal for status (✓ / × / ! shapes too).
- [ ] All foreground/background pairs **actually used** in the UI pass
      WCAG AA (4.5:1 for body text, 3:1 for large text and UI
      components).
- [ ] Touch targets are at least 44×44 CSS px on mobile.
- [ ] Form inputs have associated `<label>` (or `aria-label`).
- [ ] Buttons have accessible names (visible text or `aria-label`).
- [ ] Focus order is logical (tab through and check).
- [ ] Motion is gated by `prefers-reduced-motion` for non-essential
      animations.

## G. Hierarchy & affordance

- [ ] Primary action is unambiguously the highest-contrast / largest /
      most-saturated thing in its view.
- [ ] Secondary content is pushed back with **lower contrast first**,
      smaller size second.
- [ ] Buttons look pressable (subtle elevation, hover transition, or
      bordered fill).
- [ ] Scrollable regions hint at overflow (fade, partial item, or
      explicit affordance).

## H. Cross-browser / cross-device

- [ ] Tested at 100% browser zoom and at 200% (text should reflow, not
      clip).
- [ ] Tested at the smallest target viewport (often 320px).
- [ ] Tested with the OS in dark mode if the design supports it.
- [ ] Real device check for mobile-targeted UI (emulators lie).

## I. DESIGN.md hygiene

- [ ] Any new token used in the implementation has been added back to
      DESIGN.md (don't leave one-offs in code).
- [ ] DESIGN.md still lints clean (`scripts/validate_design_md.py`
      DESIGN.md exits 0).
- [ ] If you discovered a gap (e.g. no `error` color, no
      `button-destructive`), you flagged it in the handoff message.

---

## Quick triage when something looks off

Symptom → most likely cause:

- **Edges look fuzzy** → element is on a half-pixel boundary; check
  `transform`, percentage widths, and odd-pixel dimensions.
- **Border thickness varies at corners** → outer-radius rule violated.
- **Text sits low in a button** → centered by bounding box, not
  x-height.
- **Spacing feels arbitrary** → off-token padding/margin somewhere; run
  the audit.
- **Colors are inconsistent across pages** → some component imports a
  raw hex instead of the token.
- **Layout breaks at viewport X** → worst-case content not tested; some
  string is overflowing.
- **Focus ring missing** → someone added `outline: none` without a
  replacement.
