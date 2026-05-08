# Design Auditor Agent

Instructions for running a comprehensive UI design audit on an existing interface (HTML/CSS, React/Vue components, screenshots, or a live URL).

The goal is to produce an actionable, prioritized report that the developer can act on immediately — not a list of abstract design principles.

---

## Audit protocol

Work through each category below in order. For each issue found, record:
- **What** the problem is (specific, concrete — cite CSS values, class names, or screenshot regions)
- **Why** it matters (how it degrades the user experience)
- **Fix** the specific change needed (concrete CSS/code, not vague advice)

---

### Category 1 — Visual Hierarchy

Scan every view and ask: can I tell what's most important at a glance?

**Check for:**

- [ ] **Flat hierarchy** — all text nearly the same size and color. Fix: Introduce 3-tier text colors (primary/secondary/tertiary) using `--color-text-primary`, `--color-text-secondary`, `--color-text-tertiary`.
- [ ] **Size-only hierarchy** — size is the only differentiator, no use of weight or color. Fix: De-emphasize secondary elements with lighter color before increasing primary size.
- [ ] **No clear primary action** — multiple CTAs with equal weight. Fix: One filled/primary button per section; make others secondary/ghost.
- [ ] **Redundant labels** — labels that say the same thing as the value (e.g., "Name: Jordan Diaz"). Fix: Remove the label or restructure to let the value speak.
- [ ] **Grey text on colored background** — grey hex color on a non-white background. Fix: Use opacity (e.g., `rgba(255,255,255,0.75)`) or a same-hue lighter shade.
- [ ] **Icon-text weight mismatch** — bold icon next to light text (or vice versa). Fix: Match icon color to the text's hierarchy level.

**Hierarchy audit output format:**
```
HIERARCHY — [Severity: High/Medium/Low]
Location: [component/selector/line]
Problem: [description]
Fix: [specific CSS or code change]
```

---

### Category 2 — Spacing

Look at every component and check if spacing feels intentional.

**Check for:**

- [ ] **Arbitrary spacing values** — values like `13px`, `7px`, `22px` that aren't on the spacing scale. Run: `scripts/audit_design.py styles.css` to find these automatically.
- [ ] **Too tight** — padding under 12px on most interactive elements (buttons, inputs, cards). Fix: Minimum `padding: 8px 16px` for buttons; `24px` for cards.
- [ ] **Equal spacing everywhere** — the gap between a label and its input is the same as between field groups. Fix: Make intra-group spacing smaller than inter-group spacing.
- [ ] **Full-screen content** — content with no `max-width` stretching the full viewport. Fix: `max-width: 65ch` for prose; `max-width: 768–1280px` for UI content.
- [ ] **Explicit heights** — `height: 200px` on content containers. Fix: Use `padding` + `min-height` instead.
- [ ] **Grid forcing** — everything in a grid including items that shouldn't be (single-column content, sequential labels). Fix: Remove grid; use vertical flex with spacing.

**Spacing audit output format:**
```
SPACING — [Severity]
Location: [selector or component]
Problem: [e.g., "padding: 13px 22px — not on scale"]
Fix: [e.g., "padding: 12px 24px (space-3 space-6)"]
```

---

### Category 3 — Typography

**Check for:**

- [ ] **Too many font sizes** — more than 8 distinct values. Grep: `grep -E 'font-size:' *.css | sort | uniq -c | sort -rn`
- [ ] **Line length too long** — body text without `max-width`. Signs: full-width paragraphs on desktop, no `ch` units anywhere.
- [ ] **Constant line-height** — `line-height: 1.5` on all elements including headings. Fix: `1.1–1.2` for large headings.
- [ ] **Body text centered** — `text-align: center` on paragraphs longer than 2 lines. Fix: Left-align all prose.
- [ ] **Loose headlines** — `h1`/`h2` with `letter-spacing: 0` or positive letter-spacing. Fix: `-0.02em` to `-0.04em` on headings.
- [ ] **Tight all-caps** — small uppercase labels without positive letter-spacing. Fix: `letter-spacing: 0.05–0.1em`.
- [ ] **Baseline misalignment** — mixed-size inline text center-aligned instead of baseline-aligned. Fix: `align-items: baseline` on flex containers.
- [ ] **System font fallback missing** — font stack that doesn't fall back gracefully if the web font fails to load.

---

### Category 4 — Color

**Check for:**

- [ ] **Naked hex values** — `#3b82f6` directly in CSS instead of a custom property. Run: `scripts/audit_design.py styles.css` (reports these).
- [ ] **No shade system** — colors defined one at a time with no palette. Fix: Use `scripts/color_palette.py` to generate a full palette.
- [ ] **Washed-out light shades** — light shades at full base saturation look grey. Fix: Boost saturation on light shades (see `references/color.md`).
- [ ] **Pure grey** — `hsl(0, 0%, X%)` with zero saturation. Fix: Add a 6–14% saturation tint matching the brand hue.
- [ ] **Color-only status** — error states that use only `color: red` with no icon or text. Fix: Add error icon + text alongside color change.
- [ ] **Contrast failures** — medium-toned text on medium-toned backgrounds. Quick check: shade-400 on white is ~4.5:1 (borderline); shade-500 on white is ~3:1 (fails for normal text). Use `assets/color-palettes.json` for safe combinations.

---

### Category 5 — Depth and Polish

**Check for:**

- [ ] **Inconsistent shadows** — some elements have `box-shadow: 2px 2px 5px black`, others use `0 1px 3px rgba(0,0,0,0.1)`. Fix: Define 5 elevation levels and use them consistently.
- [ ] **Pure black shadows** — `rgba(0,0,0,X)` shadows look muddy. Fix: Use a dark tinted version of the brand hue.
- [ ] **No empty states** — list/table components with no visual treatment for zero items. Fix: See `templates/component-empty-state.html`.
- [ ] **Border overuse** — borders between every list item, around every section, between every element. Ask: could spacing or a background color difference replace this border?
- [ ] **Missing hover/focus/active states** — interactive elements with no state transitions. Fix: At minimum, add `:hover` background change and `:focus-visible` ring.
- [ ] **Default browser styles** — unstyled `<select>`, default checkboxes, browser-default scrollbars. Fix: Style form elements to match the design system.
- [ ] **No personality** — the design uses only default element styles with no distinguishing touches. Fix: Pick one personality detail — an accent border color, a background texture, a custom illustration.

---

### Category 6 — Accessibility

**Check for:**

- [ ] **Missing focus rings** — `outline: none` or `outline: 0` without a `focus-visible` replacement. Fix: Never remove focus styling without providing an equivalent.
- [ ] **Missing `alt` text** — `<img>` without `alt` attribute.
- [ ] **Color alone for info** — error/success conveyed only by color change with no text or icon.
- [ ] **Insufficient contrast** — body text with less than 4.5:1 contrast ratio; large text with less than 3:1.
- [ ] **Missing ARIA labels** — icon-only buttons without `aria-label`.
- [ ] **No semantic HTML** — `<div>` used for everything instead of `<button>`, `<nav>`, `<main>`, `<article>`, etc.

---

## Report output

Structure the final report as:

```
# Design Audit Report
Generated: [date]
Files audited: [list]

## Critical Issues (fix before launch)
[issues that break usability or accessibility]

## High Priority (strong visual impact)
[visual hierarchy problems, spacing inconsistencies at scale]

## Medium Priority (polish and consistency)
[typography fixes, color system improvements]

## Low Priority / Nice to Have
[finishing touches, personality details]

## Positive Notes
[things that are already working well — always include at least 2-3]

## Quick Wins
[changes that take < 30 minutes and have high visual impact]
```

Always end with "Quick Wins" — 3–5 changes that take minimal time but make the biggest visual difference. These give the developer immediate wins and build momentum.

---

## Running the automated audit

For CSS/HTML files:
```bash
python scripts/audit_design.py path/to/styles.css path/to/index.html
# JSON output:
python scripts/audit_design.py --json styles.css
```

For a complete token scaffold from scratch:
```bash
python scripts/generate_tokens.py --primary-hue 220 --format css --output tokens.css
```

For a palette review:
```bash
python scripts/color_palette.py --hue 220 --name primary --format preview
```
