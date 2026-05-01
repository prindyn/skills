---
name: web-design
description: Use this skill whenever the user wants to decide on or create a web design — choosing a website platform (Squarespace, Wix, WordPress), planning site structure, drafting a homepage, building a brand kit / design system, writing a creative brief, mapping a sitemap, designing CTAs and visual hierarchy, picking colors/fonts/layouts, or running a pre-launch checklist. Trigger this skill even when the user does not say "web design" outright — phrases like "I need a website for my business", "help me plan a landing page", "what platform should I use", "design my homepage", "create a brand kit", or "I'm about to launch a site" all qualify. Lean toward triggering rather than skipping.
---

# Web Design

A guided workflow for *deciding on* and *creating* a website — adapted from the Gentle Media 2025 Guide to Web Design. Designed for non-technical founders, small business owners, creatives, and anyone whose website project would otherwise stall in the "started but never published" 90%.

## Why this skill exists

Most web design help collapses into one of two failure modes:
1. **Jargon dump** — overwhelming the user with technical detail before they've made a single real decision.
2. **Blank canvas** — asking "what do you want?" without giving the user a frame to answer.

This skill solves both by walking the user through *decisions in the right order*, producing concrete artifacts at each stage. The artifacts (creative brief, sitemap, page outlines, design system, pre-launch checklist) are what unblock the project — not abstract advice.

## The core workflow

Always work in this order. Skipping ahead is the most common reason web projects die.

1. **Define the "why"** — purpose, audience, primary user action (the CTA).
2. **Pick a platform** — Squarespace / Wix / WordPress, based on user skill + needs.
3. **Plan the design language** — brand kit (colors, fonts, shapes, tone) before any layout.
4. **Map site structure** — which pages exist, what each page's job is.
5. **Draft each page** — homepage first, then services/products, about, blog, contact.
6. **Pre-launch check** — proofread, test, optimize, set up analytics, back up.
7. **Promote** — email, social, SEO, word of mouth.

When the user shows up mid-stream ("I already picked Squarespace, help me design the homepage"), respect that — jump in at the relevant step but quickly verify the upstream decisions. If they skipped step 1, gently surface it: a homepage with no defined CTA is a dead homepage.

## How to engage with the user

This is a **decision-support skill**, not an "I'll do it for you" skill. The user owns the brand, the voice, the offer. Your job is to:

- **Ask the right questions in the right order** so the user is never staring at a blank page.
- **Recommend a default** when the user is undecided. Decision fatigue kills projects more than wrong decisions do. If unsure, recommend Squarespace (per the source guide's reasoning: best balance of design quality, ease, and all-in-one hosting for non-developers).
- **Produce a concrete artifact** at the end of each step — not just advice. Use the templates in `templates/`.
- **Keep moving forward.** If a decision is reversible, make it and move on. Flag the few that aren't (domain name, platform commitment past trial period).

If you sense the user is at risk of paralysis, name it explicitly and offer a default they can change later.

## When to load reference material

Read files from `references/` only when the situation calls for it — don't load everything up front.

- `references/platform-selection.md` — when the user is comparing Squarespace vs Wix vs WordPress, or asking "which platform should I use?"
- `references/design-principles.md` — when designing or critiquing layouts, choosing colors/fonts, evaluating accessibility, or applying visual hierarchy.
- `references/page-content-guide.md` — when drafting copy or structure for a specific page (home, about, services, blog, contact).
- `references/glossary.md` — when the user (or you) needs a quick definition of UI, UX, CTA, conversion rate, design system, CSS, click path, brand identity.

## When to use templates

Use the templates in `templates/` to produce concrete deliverables. Copy the template content, fill it in *with the user* (ask their answers, don't invent), and present the filled version as the artifact. Templates available:

- `templates/creative-brief.md` — one-page brand + project definition. Use at step 1–3.
- `templates/sitemap.md` — site structure / page list. Use at step 4.
- `templates/homepage-wireframe.md` — homepage section-by-section outline. Use at step 5 for the homepage.
- `templates/page-outline.md` — generic outline for any other page (about, services, contact, etc.). Use at step 5.
- `templates/design-system.md` — brand kit: colors, fonts, spacing, components. Use at step 3.
- `templates/pre-launch-checklist.md` — final QA before publishing. Use at step 6.

Templates are scaffolds, not scripts — adapt them to the user's situation. If the user's project is a single landing page, the sitemap template is overkill; skip it.

## Design principles to keep in your head (cheat sheet)

These come up constantly. Load `references/design-principles.md` for the full treatment.

- **One primary CTA per page.** What single action should this page get a visitor to take? If you can't name it, the page isn't designed yet.
- **Visual hierarchy is subconscious.** Size, color contrast, position, and whitespace tell the eye what matters. Make the most important thing the most prominent thing.
- **Simplicity beats cleverness.** Every element earns its place by serving the CTA. If it doesn't, cut it.
- **Mobile-first.** Most visitors will see this on a phone. Design for that screen first, then expand.
- **Accessibility is design quality.** High contrast, alt text, keyboard navigation, scalable text. Not optional.
- **Consistency across pages.** Same fonts, same colors, same button styles, same nav. The brand kit enforces this.

## Recommending a platform (quick logic)

If the user asks "which platform?" and you don't have time to walk through `references/platform-selection.md`:

- **Default recommendation: Squarespace.** Best for non-developers who want a polished result with minimal hurdles. All-in-one (hosting, domain, SSL, e-commerce). The source guide recommends it for almost everyone.
- **Suggest Wix** if the user explicitly wants pixel-level drag-and-drop control and is willing to spend more time tuning.
- **Suggest WordPress** if the user (a) can write or wants to learn HTML/CSS, (b) needs deep customization or unusual functionality, or (c) is cost-sensitive and willing to manage hosting separately.

State the recommendation, give the one-line "why," and ask if they want to proceed or hear the trade-offs.

## A note on scope

This skill is for *deciding on* and *creating the design of* a website — the planning, structural, and visual decisions. It does not implement the site in code, deploy it, or operate the platform's UI. When the user's question shifts to "how do I actually click through Squarespace's editor to do X" — you can offer general guidance, but the platform's own help docs are authoritative.

If the user wants you to write actual HTML/CSS/JS or implement components, that's adjacent to this skill — handle it as a normal coding task, but keep the design principles above in mind.
