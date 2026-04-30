# Visual Identity System

This is the largest reference file. It contains the systematic flow that turns a brand's positioning into concrete visual decisions: a color palette, a typography pair, a wordmark direction, photography rules, and supporting visual elements.

The flow is **strategy → expression → documentation**. Don't skip strategy. Visual decisions made without strategic grounding are just personal taste, and personal taste isn't repeatable.

## Stage 1 — Strategy lock-in

### Define the adjectives

Get 3–5 specific adjectives that describe the brand's personality. **Specific** is the key word — "professional", "high-quality", and "modern" are useless because every brand claims them. Push for words that mean something:

- *playful, irreverent, deadpan* (not just "fun")
- *weathered, hand-built, earnest* (not just "authentic")
- *technical, exacting, no-nonsense* (not just "reliable")

If the user gives generic adjectives, ask: "When you say 'professional', do you mean *corporate-and-buttoned-up*, *quietly-authoritative*, or *meticulously-crafted*? Those produce very different brands."

For each adjective, also define an **anti-adjective** — the version that's nearby but wrong. *Fast but not Rushed. Friendly but not Casual. Bold but not Loud.* This catches drift later.

### Pick an archetype (sanity check)

Brands tend to lean into one of 12 archetypes (Jungian framework, used widely in marketing):

Creator, Innocent, Rebel, Sage, Hero, Caregiver, Explorer, Ruler, Magician, Lover, Jester, Everyman.

This isn't a deep analysis — it's a 30-second sanity check. If the adjectives say "playful" but the archetype the user identifies with is "Sage" (deep wisdom, professorial), there's a mismatch to surface. Each archetype has typical visual conventions:

- **Creator**: handcrafted feel, organic textures, expressive typography
- **Innocent**: light colors, simple shapes, clean serifs
- **Rebel**: high contrast, raw textures, distorted/unconventional type
- **Sage**: muted palette, classical serifs, ample whitespace
- **Hero**: bold, saturated, sans-serif, dynamic composition
- **Caregiver**: warm palette, rounded shapes, friendly script
- **Explorer**: earth tones, rugged textures, geometric sans
- **Ruler**: deep colors, classical serifs, structured layouts
- **Magician**: deep purples/teals, refined serifs, mysterious imagery
- **Lover**: rich tones, curved shapes, sensual photography
- **Jester**: bright colors, playful type, asymmetric layouts
- **Everyman**: neutral palette, friendly sans, relatable imagery

Use this as input, not output. The archetype suggests directions; it doesn't dictate.

### Build a mood board (look sideways)

The trap most amateurs fall into: looking at competitors for inspiration. Result — the new brand looks like all the old brands. The professional move is to look at **adjacent industries that share your adjectives**.

If the brand adjectives are "rugged, honest, hand-built" and the business is software, look at outdoor gear brands, traditional carpentry, blacksmithing, vintage motorcycle culture — not at other software.

A mood board should be **20–30 images** that capture the *feeling* of the adjectives. Photography style, color palettes, typography from books/posters, textures, architectural details. The goal is to extract patterns: "the photography is high-contrast and shadowy", "the color palette is muted earth tones with one bright accent", "the typography is heavy serif with tight tracking".

The mood board doesn't appear in the final deliverable, but the patterns it surfaces drive every decision below.

## Stage 2 — Color palette (60-30-10 framework)

The 60-30-10 framework is the difference between an intentional palette and a random one.

- **60% — neutral anchor.** This is the dominant color across most surfaces. Usually an off-white, warm gray, deep charcoal, or near-black. It's not the brand's "color" — it's the canvas.
- **30% — brand color.** This is the signature. The color customers will associate with the brand. Used for headers, key visuals, and strong brand moments. *One* color. Not three.
- **10% — accent color.** For calls-to-action, highlights, and visual interest. Often complementary or contrasting to the brand color. Sparingly used, which is what gives it impact.

### Picking the brand color

The brand color should:

1. **Match the adjectives.** Earth tones for "grounded, authentic". Saturated brights for "playful, energetic". Deep jewel tones for "luxurious, considered". (This is psychological convention; not science but reliably effective.)
2. **Differentiate from competitors.** If every competitor in the space uses blue, picking blue makes the brand invisible. Pick a color that stands out within the category — but doesn't violate category expectations so badly it feels wrong (e.g., a pink law firm raises eyebrows).
3. **Pass accessibility.** WCAG AA requires 4.5:1 contrast for normal text, 3:1 for large text. Test the brand color against the neutral on a contrast checker. If it fails, you have a *display* color, not a *text* color — usable but limited.

### Document the colors completely

Every color needs four code formats:

- **Hex** — for web/digital (e.g., `#B85C3C`)
- **RGB** — for digital design tools (e.g., `184, 92, 60`)
- **CMYK** — for print (e.g., `0, 50, 67, 28`)
- **Pantone** — for professional printing, specialty applications (e.g., PMS 7522 C). Optional but strongly recommended.

Without all four codes, three different vendors will produce three different versions of the same "brand color" — which is what kills consistency.

### Secondary palette (often overlooked)

Beyond the 60-30-10, you also need:

- **Light tint of the brand color** — for backgrounds, hover states, subtle highlights
- **Dark shade of the brand color** — for text on light backgrounds, strong borders
- **A neutral gray scale** — typically 4–5 grays from very light (`#F5F5F5`) to very dark (`#1A1A1A`) for borders, dividers, secondary text
- **Semantic colors** (if it's a digital product) — green for success, red/orange for error, yellow for warning. Pick versions that fit the palette rather than off-the-shelf bootstrap colors.

## Stage 3 — Typography (Rule of Two)

Two fonts. Maximum. One for headlines, one for body.

### The headline font

Carries the brand's personality. This is where you get to be expressive. It's typically:

- **A bold sans-serif** (Inter, Helvetica Neue, Proxima Nova, Montserrat) — clean, modern, versatile
- **A characterful serif** (Playfair Display, Lora, Merriweather, Cormorant) — elegant, traditional, considered
- **A condensed/display font** (Bebas Neue, Oswald, League Spartan) — bold, attention-grabbing, magazine-y
- **A slab serif** (Roboto Slab, Arvo, Zilla Slab) — confident, modern-but-grounded

Pick based on adjectives. Sage/Innocent → serif. Rebel/Hero → bold sans or condensed display. Caregiver/Lover → softer serif or rounded sans.

### The body font

Carries the actual reading load. Personality should be subordinate to readability. This is typically:

- **A workhorse sans-serif** — Inter, Source Sans Pro, Roboto, Open Sans, Lato
- **A readable serif** for long-form content — Merriweather, Lora, Source Serif Pro

The body font should:

1. **Read clearly at 14–16px** on screens
2. **Distinguish similar characters** — `1`, `l`, `I` should look different; `0` and `O` should look different
3. **Have multiple weights available** (regular, semibold, bold at minimum)
4. **Pair harmonically** with the headline font

### Pairing rules

- **Sans + Serif** is the most reliable pair (modern + classic = balanced)
- **Sans + Sans** works if the two have clearly different proportions or weights
- **Serif + Serif** is hard — usually feels muddled
- **Same family, different weights** (e.g., Inter Bold for headline + Inter Regular for body) is safe but less distinctive
- **Avoid trendy fonts** — the font of the month dates the brand. Stick to typefaces that have worked for 10+ years (Helvetica, Inter, Proxima Nova, Merriweather, Lora). The boring answer is the right answer.

### Typography hierarchy (specific sizes)

Document exact specs, not vague descriptors. Example for a website:

| Level | Font | Size | Weight | Tracking | Case |
|---|---|---|---|---|---|
| H1 | Headline font | 48px | Bold (700) | -1% | Sentence case |
| H2 | Headline font | 32px | Bold (700) | -0.5% | Sentence case |
| H3 | Headline font | 24px | Semibold (600) | 0 | Sentence case |
| Body | Body font | 16px | Regular (400) | 0 | Sentence case |
| Caption | Body font | 13px | Regular (400) | +1% | Sentence case |
| Button | Body font | 14px | Semibold (600) | +5% | Title Case |

Print is different (use pt instead of px, generally 1.3× the line-height of screen). Document both if the brand uses both.

## Stage 4 — Logo (wordmark)

The default recommendation is a **wordmark** — the brand name typed in the headline font with deliberate treatment. Not an abstract symbol.

### Why a wordmark

- **Recognition without ad spend.** Symbols only become recognizable through millions of impressions (think Nike's swoosh, Apple's apple, McDonald's arches). New brands don't have that. A wordmark is recognizable from day one because it spells the brand's name.
- **Cheaper to produce.** No designer required. The user can produce a wordmark in 15 minutes in Figma, Canva, or even Google Docs.
- **Versatile.** A wordmark works in any size, on any background, in any color, in any context. Symbols often don't.
- **Trademarkable.** Wordmarks are typically easier to trademark than abstract symbols (which compete with thousands of similar shapes).

### Wordmark treatment

The user types their brand name in the headline font. Then makes deliberate choices:

- **Case**: ALL CAPS (impactful, modern), Title Case (friendly, classical), lowercase (casual, intimate)
- **Weight**: Light, Regular, Medium, Bold, Black — heavier weights = more presence; lighter = more refined
- **Tracking** (letter spacing): tight (-2% to -5%) feels confident and modern (Nike, FedEx); loose (+5% to +10%) feels luxurious and refined (Rolex, Chanel)
- **Hierarchy** (for multi-word names): emphasize one word with bold, de-emphasize others with light weight. This is what turns "Smith Digital Consulting" from a generic phrase into a deliberate logo. (e.g., **SMITH** *digital consulting*)
- **Color**: usually the brand color or a neutral. Avoid gradients and effects.

### The black-and-white test

After designing the wordmark in color, **convert it to pure black on white** and ask: does it still work? If it relies on color to be readable or recognizable, it'll fail in real-world contexts (faxes, embroidery, single-color print, dark mode toggles).

Also test:
- **Pure white on black** — for dark-mode and inverted contexts
- **At 40×40 pixels** — favicon size; verifies the wordmark holds up at thumbnail scale
- **At billboard scale** — verifies it doesn't fall apart when blown up

### Should there ever be a symbol?

A complementary symbol or **monogram** (one or two letters from the wordmark, treated as an icon) is reasonable for:

- Favicons and app icons (where a wordmark can't fit)
- Profile avatars on social platforms
- Reusable brand pattern elements

The monogram should be derivable from the wordmark — same font, same weight, same color logic. Not an unrelated abstract shape. (Think how Airbnb's "A loop" mirrors the type of their wordmark, or how Shopify's bag icon is consistent with their type style.)

If the user really wants an abstract symbol, push back: it's expensive to make memorable, hard to design well without a specialist, and not necessary. Recommend they wait until the business has revenue and brand recognition, then commission a real designer. Don't try to design a meaningful symbol on a 30-minute AI-assisted call.

## Stage 5 — Photography & imagery rules

A brand without photography rules will end up with a "Frankenstein feed" — random images from random sources that don't share a visual language. Define the rules upfront.

### The Visual DNA checklist

For every photo the brand uses, it must match on these axes:

1. **Lighting**: hard or soft? warm or cool color temperature? bright or moody?
2. **Color palette**: vivid or muted? what colors dominate? does it complement the brand palette?
3. **Composition**: minimal/spacious or dense/full-frame? symmetrical or dynamic? centered subject or rule-of-thirds?
4. **Subject matter**: people or objects or environments? close-up or wide? candid or staged?
5. **Post-processing**: natural/un-edited or stylized? same filter strength across all photos?

Define each axis with a clear rule. Example for a "weathered, hand-built, honest" brand:

- Lighting: soft, natural, warm temperature (golden-hour preferred)
- Palette: muted earth tones, occasional pop of brand terracotta
- Composition: close-up details, rule-of-thirds, asymmetric
- Subject: hands at work, tools, materials, finished objects (rarely faces)
- Post: minimal — slight contrast boost, no heavy filters

The rule is what lets the user (or a contractor) reject photos that don't fit, without having to debate it.

### Stock vs. original

If the user can't afford original photography, stock works — but only if filtered carefully. Avoid the obvious "stock look" (overly staged, fake-smile corporate). Sources like Unsplash, Pexels, Death to Stock, and Stocksy lean more authentic.

When mixing stock with original photos, apply consistent post-processing (same color grading, same crop ratios) to make them feel like one family.

## Stage 6 — Supporting elements (icons, textures, patterns)

Pick **one icon style** and stick to it:

- **Outlined** — modern, minimal, works at small sizes (Phosphor, Heroicons, Lucide)
- **Filled/solid** — bold, friendly, more visual weight
- **Hand-drawn** — characterful, casual, distinctive (best for personality-led brands)
- **Two-tone** — some libraries pair an outlined and filled version for emphasis

Mixing icon styles is the visual equivalent of mixing fonts — it screams amateur. Pick one and reject the rest.

For **textures and patterns** (paper grain, gradient meshes, geometric repeats):

- Use them subtly (10–20% opacity) as background elements
- Never compete with text — patterns sit *behind*, not *with*
- One texture/pattern direction per brand. Not three.
- Define the rules: where they appear, where they don't.

## Stage 7 — Test the system

Before declaring the visual identity done, mock it up in 4–5 contexts:

1. **Website homepage** (header, hero, body, CTA)
2. **Social media post** (square format, with brand colors and type)
3. **Business card** (front and back, in monochrome)
4. **Email signature** (just type, must work in plain HTML)
5. **Favicon** at 32×32 pixels

If any of these feel off, refine before locking. Common issues:

- Brand color too light to read on white → darken or use only for accents
- Headline font too thin at small sizes → bump weight
- Wordmark falls apart at 40px → simplify
- Two colors that fight at small sizes → re-balance the palette

## What to deliver

For a complete visual identity request, the user walks away with:

- **3–5 brand adjectives** (and their anti-adjectives)
- **Color palette**: primary brand color + neutral anchor + accent + secondary palette, all with hex/RGB/CMYK
- **Typography pair**: one headline font, one body font, named with download links, plus the hierarchy spec table
- **Wordmark direction**: case, weight, tracking, color — specific enough they can produce the wordmark themselves
- **Photography rules**: 5-axis Visual DNA spec
- **Supporting elements**: icon style chosen, texture rules if applicable
- **A list of mockup contexts** they should test in before locking

Then point them to `brand_guide.md` for assembling all this into a single document.
