# Design System / Brand Kit — [Project Name]

> The single source of truth for visual decisions. Every color, font, button, and spacing on the site comes from this document. Decide it once; reuse forever.

## 1. Color palette

### Primary
- **Brand color:** `#______` — used for: logo, primary CTAs
- **Brand color (dark variant):** `#______` — used for: hover states, headings

### Neutrals
- **Background:** `#FFFFFF` (or off-white `#______`)
- **Body text:** `#______` (dark gray, not pure black — easier on the eyes)
- **Muted text:** `#______` (for captions, helper text)
- **Borders / dividers:** `#______`

### Accents
- **Accent color:** `#______` — sparingly, for highlights or secondary CTAs
- **Success:** `#______` (greens)
- **Warning:** `#______` (yellows/oranges)
- **Error:** `#______` (reds)

### Contrast check
All text/background combos must pass **WCAG AA** at minimum (4.5:1 for body text, 3:1 for large text). Verify with a contrast checker before locking in.

## 2. Typography

### Fonts
- **Headings:** [font name, e.g., "Inter"] — weight 600 or 700
- **Body:** [font name, e.g., "Inter"] — weight 400
- **Optional accent / display:** [font name, used sparingly]

> Pick at most 2 font families. More than that creates visual noise.

### Type scale
| Use | Size | Weight | Line-height |
|---|---|---|---|
| H1 | 48–64px | 700 | 1.1 |
| H2 | 32–40px | 700 | 1.2 |
| H3 | 24–28px | 600 | 1.3 |
| Body | 16–18px | 400 | 1.5 |
| Small | 14px | 400 | 1.5 |

> Sizes scale down on mobile (e.g., H1 → 36px).

## 3. Spacing

Use a consistent scale (8px or 4px base):
- **xs:** 4px
- **sm:** 8px
- **md:** 16px
- **lg:** 32px
- **xl:** 64px
- **2xl:** 128px

> Section padding: typically `xl` top/bottom on desktop, `lg` on mobile.

## 4. Components

### Buttons
- **Primary:** brand color background, white text, [rounded/sharp] corners, padding `md` horizontal / `sm` vertical
- **Secondary:** transparent background, brand-color text and border
- **Hover state:** [darken / shift color / underline]

### Links
- Color: brand color or accent
- Underline: [always / on hover only]

### Form inputs
- Border: 1px [neutral border color]
- Focus state: brand color border
- Error state: error color border + helper text

### Cards
- Background: white (or subtle off-white)
- Border or shadow: pick one, not both
- Corner radius: matches buttons for consistency

## 5. Imagery & icons

- **Photography style:** [describe — e.g., "natural light, real people, no stock-photo handshakes"]
- **Illustration style:** [if applicable]
- **Icon library:** [e.g., Lucide, Heroicons, Font Awesome] — pick one and stick to it

## 6. Voice & tone

- **Adjectives:** [3–5 from the creative brief]
- **Reading level:** aim for 8th grade unless your audience demands otherwise
- **What we never say:** [phrases or jargon to avoid]
