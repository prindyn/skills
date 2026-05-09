# SaaS Color Palette Guide

Color is the fastest brand signal — it communicates before words are read. This guide covers color theory for SaaS brands, the industry conventions in B2B tech, and how to build a palette that is both differentiated and credible.

---

## Table of contents

1. The anatomy of a SaaS palette
2. Industry conventions by sector
3. Palette formulas
4. Accessibility requirements
5. Color in UI components
6. What to avoid

---

## 1. The anatomy of a SaaS palette

A complete SaaS color palette has four tiers. Every color in the UI should be traceable back to one of these tiers.

```
TIER 1: Primary
         The dominant brand color. Used in: logo, primary buttons, 
         selected states, headers, key highlights.
         → One color.

TIER 2: Secondary
         Support colors for contrast, section backgrounds, 
         secondary UI elements.
         → 1–2 colors.

TIER 3: Accent
         High-attention colors for hover states, tags, icons, 
         progress indicators.
         → 1–2 colors.

TIER 4: Neutrals
         For backgrounds, text, borders, dividers.
         → White, light gray, mid gray, dark gray/charcoal, black.
```

**Total unique colors in a clean SaaS palette:** 5–8 (excluding neutrals).

Having fewer, well-chosen colors creates more cohesion than many poorly-coordinated colors.

---

## 2. Industry conventions by sector

Understanding what your competitors look like is essential — you need to decide whether to follow convention (credibility) or break from it (differentiation).

### General B2B SaaS
- **Dominant color:** Blue (60%+ of companies). Blue = trust, technology, professionalism.
- **Common accents:** Orange (complementary to blue; warmth + energy), teal (modern, fresh), purple (creative, premium)
- **Typography colors:** Dark gray (#1A1A2E or similar) is preferred over pure black — less harsh on screens
- **Background:** White or very light gray; dark mode (deep navy) increasingly common for product/tech companies

### Life sciences / pharma SaaS
- **Primary:** Blue — reinforces scientific credibility and trust
- **Secondary:** Orange or amber — signals innovation, pipeline progress, warmth (contrast to clinical blue)
- **Avoid as primary:** Green (associated with environmental sectors), red (alarm associations)
- **Tone:** Sophisticated, slightly muted — avoid neon or "fun" colors; the audience is analytical

### Fintech SaaS
- **Primary:** Deep navy or indigo — premium, institutional, reliable
- **Accent:** Green (growth, money) or gold (premium)
- **Avoid:** Casual or playful colors — financial trust is fragile

### HR / People Tech SaaS
- **Primary:** Purple, teal, or warm blue — human, modern, empowering
- **Accent:** Warm coral, amber — human warmth
- **Can use:** More saturated, playful palettes than enterprise B2B

### Developer Tools / Infrastructure SaaS
- **Primary:** Dark background palettes (near-black with accent) — code-editor aesthetic
- **Accent:** Electric green, cyan, orange — signal precision and performance
- **Typography:** Monospace or technical sans-serif

---

## 3. Palette formulas

### Formula A: Complementary (high contrast, energetic)
Choose a primary, then use its complement on the color wheel as secondary.
- Blue primary → Orange secondary
- Indigo primary → Gold/amber secondary
- Teal primary → Coral/orange secondary

**Effect:** High contrast, dynamic, energetic. The most effective for differentiation.

**Example — DnXT Solutions style:**
```
Primary:    DnXT Blue     #1674BA  (from logo)
Secondary:  Orange tawny  #D84C00  (complement — warmth and contrast)
            Indigo dye    #08416E  (dark blue — depth)
Accent:     Seal brown    #522226  (rich, trustworthy)
            Maya blue     #64BBFF  (light — fresh hover states)
Neutral:    Black, White, Light gray #F5F5F5
```

### Formula B: Analogous (harmonious, sophisticated)
Choose a primary, then use neighboring colors on the wheel as secondaries.
- Blue primary → Indigo + teal secondaries
- Blue-gray primary → Navy + slate secondaries

**Effect:** Calm, cohesive, professional. Less dynamic but more premium-feeling.

**Example — Veeva style:**
```
Primary:    Honey orange  #E07400
Secondary:  Navy          #2B3A6B
            Burnt orange  #C05200
Accent:     Amber         #F5A623
            Cyan          #00B4D8
Neutral:    Black, White, Light gray
```

### Formula C: Triadic (vibrant, memorable — use carefully)
Use three colors equally spaced on the color wheel.
- Blue + Orange + Green
- Purple + Orange + Teal

**Effect:** Very energetic and distinctive, but hard to balance without clashing. Reserve for companies with strong visual design expertise.

---

## 4. Accessibility requirements

Color choices must meet WCAG (Web Content Accessibility Guidelines) 2.1 Level AA minimum. This is both a legal requirement in many jurisdictions and a basic quality bar.

### Contrast ratios required

| Text size | Minimum ratio |
|-----------|---------------|
| Body text (< 18px regular, < 14px bold) | 4.5:1 |
| Large text (≥ 18px regular, ≥ 14px bold) | 3:1 |
| UI components (buttons, form borders) | 3:1 |

### How to check
Use the **WebAIM Contrast Checker** (webaim.org/resources/contrastchecker/) — enter foreground and background hex codes.

### Common problem combinations

| Combination | Typical ratio | Status |
|-------------|--------------|--------|
| White text on medium blue (#1674BA) | ~4.8:1 | ✅ Pass |
| White text on light blue (#5BA4CF) | ~2.7:1 | ❌ Fail |
| Dark gray (#333333) on white | ~12.6:1 | ✅ Pass |
| Orange (#E07400) on white | ~3.2:1 | ❌ Fail for body text (ok for large) |
| Dark blue (#08416E) on white | ~10.4:1 | ✅ Pass |

**Practical rule:** White text over any brand color — always check. Many "brand blues" are too light to pass with white text.

### Color blindness considerations
Approximately 8% of males have some form of color vision deficiency. Never use color as the *only* differentiator:
- Form error states: red border + error icon + error text (not just a red border)
- Status indicators: colored dot + text label (not just a colored dot)
- Charts/graphs: use pattern or texture in addition to color

---

## 5. Color in UI components

### Primary button
- Background: Primary color
- Text: White (verify contrast)
- Hover state: 10–15% darker than primary

### Secondary / outline button
- Background: Transparent
- Border: Primary color or dark gray
- Text: Primary color or dark gray

### Hero section
- Background options:
  - White (clean, minimal)
  - Very light tint of primary (2–5% opacity — subtle brand presence)
  - Gradient: primary at low saturation → white, or primary → secondary
  - Glassmorphism: gradient behind a frosted glass overlay

### Section backgrounds (alternating)
Alternate sections between white and a very light neutral or brand tint to create visual separation without hard borders:
```
Section 1 (hero): White or gradient
Section 2: White
Section 3 (testimonials): Light blue (#EBF4FF) or primary at 5% opacity
Section 4: White
Section 5 (contact): Gradient using primary colors — signals completion/action
Footer: Dark navy or charcoal (#1A2A3A)
```

### Text hierarchy
```
H1, H2 headings:  Very dark (near-black) or primary color for accented headings
H3, H4 headings:  Dark gray (#333333)
Body text:        Dark gray (#444444 or #555555 — not pure black)
Caption / label:  Medium gray (#777777)
Disabled:         Light gray (#AAAAAA)
Link:             Primary color (or secondary if primary is low contrast)
```

---

## 6. What to avoid

### Too many colors
Using 6+ distinct hues (excluding neutrals) creates visual chaos. The eye doesn't know where to look. Worse, it signals "we couldn't make a decision."

### Low-contrast combinations
The most common error: light blue background with white text, or gray text on white that "looks fine" but fails accessibility.

### Generic blue + white + gray
Every major B2B SaaS company uses this palette. It communicates nothing distinctive. Add a second color — even a subtle one — to create brand identity.

### Mismatched color temperatures
Warm primary (orange) + cool secondary (blue-gray) can work if deliberate. But mixing warm accents and cool accents randomly creates tension that reads as "unfinished."

### Using color to replace content
Gradients and colorful sections look impressive in screenshots but must still contain meaningful content. Color should enhance the message, not substitute for it.

### Changing the palette mid-project
Agree on the palette before high-fidelity mockups begin. Changing the primary color after mockups are done means rebuilding every screen.

---

## Palette documentation format

When handing off a palette, document each color in this format:

```
DnXT Blue
Hex:    #1674BA
RGB:    22, 116, 186
CMYK:   88, 38, 0, 27
HSL:    206°, 79%, 41%
Usage:  Primary buttons, logo, key highlights, section headers
Notes:  Use white text on this background (contrast: 4.8:1 ✅)
```

Provide this documentation for every color in the palette — primary, secondaries, accents, and all neutrals.
