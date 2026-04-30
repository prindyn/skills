# The Brand Guide (5-Page Brand Bible)

A brand without a written guide drifts within months. Whoever made the decisions forgets the exact hex code, the next contractor uses a different font, and within a year the brand looks like five different brands.

The guide doesn't have to be 50 pages. It needs to be **5 pages** that anyone (the founder, a contractor, a future hire) can follow without asking questions.

## Why 5 pages, not 50

Brand guides written by big agencies often run 80+ pages because they're priced by the page. Most of that content is never read. A 5-page guide is read; a 50-page guide is searched through, partially.

The goal is **prevent mistakes, not win design awards**. The guide is a reference tool, not a portfolio piece.

## The 5 sections

### Page 1 — Identity & Voice

The strategic foundation. Half a page is enough.

- **One-sentence brand description**: who we serve and what we do.
- **3–5 brand adjectives** with anti-adjectives ("Bold but not Loud").
- **Tone of voice**: how the brand sounds in writing. 2–3 sentences max. Example: *"We sound like a knowledgeable friend, not a textbook. Direct, specific, occasionally dry. We use 'you' and 'we' freely. We don't use jargon or marketing-speak."*
- **One-line "what we never do"**: explicit boundaries. *"We never use stock photos of laughing-people-in-suits. We never write headlines in all-caps. We never apologize for being deliberate."*

### Page 2 — Logo Usage

The wordmark in approved forms, with the rules around it.

- **Primary logo**: the wordmark in the brand color, on a white background.
- **Alternative versions**: monochrome black, monochrome white (for dark backgrounds), monogram (if applicable).
- **Clear space rule**: the invisible margin around the logo where nothing else can intrude. Define this as a multiple of a logo element (e.g., "the height of the letter X in the wordmark"). Not "20 pixels" — that doesn't scale.
- **Minimum size**: smallest the logo can appear and still be legible. Usually 1 inch in print, 100–150 pixels on screen.
- **Approved backgrounds**: solid brand colors, solid neutrals, photography (with sufficient contrast).
- **Prohibited modifications**: don't stretch, don't rotate, don't add drop-shadows or effects, don't change colors, don't crop or recolor portions.

A "Do and Don't" visual section with 4–6 examples is the most useful single thing in a brand guide. It catches the abuse cases that abstract rules miss.

### Page 3 — Colors

The full palette with all code formats.

For each color:

| Name | Hex | RGB | CMYK | Pantone | Usage |
|---|---|---|---|---|---|
| Primary (e.g. "Terracotta") | `#B85C3C` | 184, 92, 60 | 0, 50, 67, 28 | PMS 7522 C | Headers, CTAs, brand moments |
| Anchor (e.g. "Charcoal") | `#222222` | 34, 34, 34 | 0, 0, 0, 87 | — | Body text, primary surfaces |
| Accent (e.g. "Sage") | `#8FA98F` | 143, 169, 143 | 15, 0, 15, 34 | PMS 5635 C | Highlights, secondary CTAs |
| Tint (light brand) | `#F5E1D8` | 245, 225, 216 | 0, 8, 12, 4 | — | Backgrounds, hover states |
| Shade (dark brand) | `#5C2D1B` | 92, 45, 27 | 0, 51, 71, 64 | — | Text on light backgrounds |

Plus a 4–5 step neutral gray scale.

Add usage rules:

- "Primary on Anchor" → the most important brand combination, used for hero moments
- "Anchor on Tint" → most readable combination for body text
- "Never use Primary on Accent" → fails contrast, looks muddy

### Page 4 — Typography

Both fonts named, with download links and the hierarchy spec.

- **Headline font**: name, weight options used, where to download (Google Fonts URL, Adobe Fonts ID, or vendor link)
- **Body font**: same
- **Hierarchy table** (from `visual_identity.md`): H1, H2, H3, body, caption, button — each with size, weight, tracking, case
- **Pairing rules**: "Headline font is never used for body. Body font is never used for headlines larger than 24px."
- **Fallback fonts**: if the primary fonts can't load (system constraints, email rendering), fall back to system fonts that match the *category* — sans-serif fallback for sans-serif headline, serif fallback for serif headline.

### Page 5 — Imagery & Supporting Elements

Photography rules + icons + textures + the "what good looks like" examples.

- **Photography Visual DNA**: the 5-axis checklist (lighting / palette / composition / subject / post-processing) from `visual_identity.md`. Each axis with a one-sentence rule.
- **3–5 example photos** that are "on-brand", with brief annotations explaining why.
- **3–5 example photos** that are "off-brand", with annotations explaining what's wrong (too saturated, too staged, wrong subject matter, etc.).
- **Icon style**: which library, with link. Rule: "Use only [outlined/filled/hand-drawn] style. Never mix."
- **Texture/pattern rules** (if applicable): which textures, where they appear, opacity, what they're never used for.

## File format

The brand guide should be a **single PDF**. Not a Notion page (people accessing it without your account get blocked). Not a Figma file (requires Figma access). Not a Google Doc (changes silently).

PDF is the most portable, version-stable, contractor-friendly format. Export it from whatever tool the user designs it in.

## Distribution

After the PDF is built:

- **Where it lives**: a single canonical URL (cloud storage like Dropbox, Google Drive, or a dedicated brand-asset hub like Frontify if the brand is bigger). Same URL forever — even when the file updates, the link stays the same.
- **Who gets it**: every contractor, freelancer, or vendor who touches anything brand-related. Send it as part of the project kick-off email, before they ask.
- **Versioning**: filename includes a date or version number (e.g., `BrandGuide_v2_2026-04.pdf`). Keep old versions in an archive folder, but always point people to the current one.

## Update protocol

The guide *will* need to evolve. When that happens:

1. Don't do micro-updates. Wait until you have at least 3 changes worth making, then update the guide once.
2. Bump the version number. Add a "What's changed in v3" page at the front.
3. Re-send the link to active contractors. Don't assume they'll go check.
4. Archive the old version with a clear version stamp.

## A note on how big the brand guide should be

For a solopreneur or a brand with no employees yet, **5 pages is right**. Anything more is over-engineered.

For a brand with a team of 5+, you might extend to 10–15 pages — adding sections on email signature templates, social media post templates, presentation slide templates, and onboarding for new hires.

For a brand with 50+ people or external agencies producing volume, a full design system (Figma component library, code tokens, Storybook for digital products) is appropriate. But that's not what we're building here. We're building the *first* version, which gets the brand to "professional and consistent" with minimum effort.
