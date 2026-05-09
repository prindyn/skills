---
name: saas-design
description: Full end-to-end guide for redesigning a SaaS company's website using design thinking. Use this skill whenever the user wants to redesign a SaaS homepage or website, improve UX/UI for a software product site, apply design thinking to web design, run a competitive review or persona workshop, create a visual identity for a SaaS brand, build wireframes or mockups, or audit an existing B2B website. Trigger on phrases like "redesign our website", "improve our SaaS homepage", "run a design thinking process", "create a new visual identity", "competitive analysis of our site", "persona workshop", "wireframe our homepage", or any request involving SaaS brand or UX improvement.
compatibility: Designed for Claude Code and Claude.ai. No special tools required beyond a text editor and design software (Figma recommended).
metadata:
  source: "Joshi, J. (2025). Redesigning a SaaS company's website using design thinking. Metropolia University of Applied Sciences."
  method: Double Diamond (Design Council)
  version: "1.0"
---

# SaaS Website Redesign Using Design Thinking

This skill guides a complete website redesign for a SaaS company using the **Double Diamond** design process: Discover → Define → Develop → Deliver. The process is iterative — expect to revisit earlier phases as new information surfaces.

## When to use this skill

Use this whenever a SaaS company needs to:
- Redesign or refresh their website (especially the home page)
- Understand their users better before making design decisions
- Differentiate themselves from competitors
- Create or update a visual identity
- Build wireframes, site maps, or high-fidelity mockups

---

## Process overview

```
DISCOVER          DEFINE           DEVELOP           DELIVER
────────          ──────           ───────           ───────
Audit current     Proto persona    Site map          Hi-fi mockups
website           workshop         
                                   Lo-fi wireframes  Visual identity
Competitive       User journey     
review            mapping          Mood boards       Handoff assets
```

Each phase feeds the next. Start with Discover even if you feel you already know the users — the research almost always reveals surprises.

---

## Phase 1: Discover

**Goal:** Understand the current situation and the competitive landscape before designing anything.

### 1a. Audit the existing website

Review the company's current website across three lenses:

| Lens | What to assess |
|------|---------------|
| **Usability** | Navigation clarity, information hierarchy, load speed, mobile responsiveness, CTA placement |
| **Branding** | Tagline, brand voice (1st vs. 3rd person), key messages, tone consistency |
| **Visual design** | Color palette cohesion, typography consistency, image style (stock vs. illustration vs. custom), whitespace |

Document findings with screenshots. Flag issues like: inconsistent icon styles, variable font sizes, CTAs that repeat too often, or sections that contradict each other.

See `templates/competitive-review-table.md` for a structured worksheet.

### 1b. Competitive review

Select 3–5 direct competitors. For each, build a **site map** of their home page, then evaluate against the same three lenses (usability, branding, visual design).

**How to pick competitors:** Start from the company's business plan or known market context. Choose companies customers are likely to compare you against.

**What to look for across all competitors:**
- What sections do all of them include? (These are table stakes.)
- Where does each competitor excel vs. stumble?
- What visual conventions does the industry use? (e.g., life sciences SaaS tends to use blue + sans-serif fonts)
- What would make this company stand out positively?

Common patterns in SaaS competitive landscapes:
- Blue dominates as the primary color; complement with orange or green for warmth
- All-caps section labels and thin icon sets signal "corporate tech"
- Companies using illustrations (Storyset-style) feel more approachable than those relying on stock photos
- Testimonials and customer logos appear on almost every high-converting SaaS homepage

Full methodology: see `references/competitive-review.md`.

---

## Phase 2: Define

**Goal:** Synthesize research into a shared understanding of who the user is and what they need.

### 2a. Proto persona workshop

Facilitate a 60–90 minute workshop with the founding team or key stakeholders. Run three phases:

1. **Warmup** — Ask participants to brainstorm all audience types (past, present, future) using sticky notes. Three minutes, no filtering.
2. **Persona creation** — From the warmup results, pick the primary decision-maker and flesh them out: demographics, personality traits, goals, frustrations. Use dot-voting to surface what matters most.
3. **User journey exploration** — Map the persona's journey from discovering the product through to becoming a loyal customer. For each stage, capture: actions, feelings, pain points, and opportunities.

For B2B SaaS, the primary decision-maker is often **not** the daily user. Typically:
- An IT Lead or Ops Manager finds the tool
- They escalate to a Head of Department who makes the final call
- The Head tends to be analytical, risk-averse, and time-poor — they want efficiency and evidence, not enthusiasm

See `templates/proto-persona.md` and `templates/user-journey-map.md`.  
Full facilitation guide: `references/persona-workshop.md`.

### 2b. Synthesize workshop findings

After the workshop, extract the key design implications:
- What does the primary user need to see immediately (above the fold)?
- What builds trust for this persona? (social proof, logos, stats, certifications)
- What do they find frustrating in websites? (jargon, no pricing, required phone calls)
- How did they likely find the site? (LinkedIn, recommendation, search)

These findings directly drive the site map and wireframe decisions in Phase 3.

---

## Phase 3: Develop

**Goal:** Translate insights into a concrete design structure and visual direction.

### 3a. Site map

Create a site map for the redesigned home page before touching any visual design. The map forces decisions about information priority without getting distracted by aesthetics.

Recommended home page structure for B2B SaaS:

```
Header (nav links, CTA)
│
├── Hero — Tagline + 1-sentence description + CTA + visual element
├── Why us — Key differentiators + social proof (stats/ratings)
├── Customer reviews — Quotes with photos (carousel works well)
├── Products/Services — Short descriptions with icons
├── Get in touch — Visualized steps + contact form
└── Footer — Contacts, social links, nav mirror
```

Key decisions to justify in the site map:
- Customer reviews appear early (before products) to establish trust
- Keep the page short — busy B2B users scroll quickly and skim
- Each section should serve a single purpose; avoid redundant CTAs
- "Get in touch" steps demystify the acquisition process

See `templates/site-map.md` for the full template.

### 3b. Mood boards and visual identity

Before wireframing, align on visual direction. Create 2–3 mood boards representing different style paths:

| Style | Character | When to choose |
|-------|-----------|----------------|
| **Illustrations** | Warm, human, approachable | Differentiating from corporate competitors; B2B with human buyers |
| **Futuristic/data** | Tech-forward, abstract | AI/data products; audience values innovation above approachability |
| **Minimalist** | Clean, premium, trustworthy | Mature markets; audience is skeptical of over-design |

Present mood boards to stakeholders and let them choose. This prevents design-by-committee later.

**Visual identity decisions to make:**
- **Primary color:** Use the logo color as anchor; build the palette around it
- **Secondary colors:** Add 1–2 complementary or analogous colors for contrast and warmth
- **Accent colors:** 1–2 for highlights, buttons, and interactive elements
- **Typography:** One geometric sans-serif font family, varied by weight (Bold, Medium, Light). Two fonts maximum — one for headings, one for body.
- **Visual elements:** Choose a single style and commit: illustrations, icons, gradients, photography, or abstract shapes — not a mix

See `references/visual-identity.md` for detailed color and typography guidance.  
See `assets/color-palette-guide.md` for a SaaS color reference.

### 3c. Low-fidelity wireframes

With the site map approved and visual direction chosen, sketch the layout using low-fidelity wireframes. Use placeholder blocks (X for images, star icons for feature icons, gray boxes for text).

Design for the busy user: they will first skim the page before reading. Each section must communicate its core message in a 1-second glance through:
- A clear heading
- A supporting subheading or 2–3 bullet points
- An icon or visual anchor
- One CTA per section maximum

Iterate wireframes before adding color or real content. Get stakeholder sign-off on the structure before moving to high-fidelity.

---

## Phase 4: Deliver

**Goal:** Produce final design assets ready for implementation.

### 4a. High-fidelity mockups

Apply the visual identity to the approved wireframes. Key techniques that work well for SaaS sites:

- **Glassmorphism + gradients** for a fresh, modern feel (especially effective for hero sections)
- **Illustrations with consistent style** (e.g., Storyset) rather than mixed stock photography
- **Photo-first testimonials** — real customer photos with name and title massively improve credibility
- **Color-matched customer photos** — tint or border photos to stay within brand palette
- **Animated hero element** (subtle motion graphic) — differentiates from static competitors

Deliver mockups as Figma files with annotated sections explaining design decisions.

### 4b. Visual identity handoff

Compile a visual identity document covering:
- Logo usage rules
- Color palette with hex, RGB, and CMYK values
- Typography scale (heading sizes, body, captions)
- Icon style and approved icon set
- Illustration style and sourcing
- Do/Don't examples for brand application

### 4c. Implementation notes

If the site will be built in WordPress or a similar CMS:
- Specify which sections can use theme templates vs. custom blocks
- Note any third-party plugins needed (e.g., slider, form builder, carousel)
- Document any motion/animation specs separately
- Flag images that need color-matching to brand palette

---

## Common pitfalls to avoid

| Pitfall | Why it hurts | Fix |
|---------|-------------|-----|
| Skipping competitive review | Reinvents what competitors do poorly; misses table stakes | Always review 3+ competitors |
| Generic stock photography | Erodes trust; everyone uses the same Shutterstock faces | Use illustrations or real customer photos |
| Multiple CTA repetitions | Frustrates analytical users (feels pushy) | One CTA per section; vary the label |
| Too much jargon above the fold | Confuses non-specialist buyers | Test your tagline on someone outside the industry |
| Inconsistent visual style | Makes the brand look unfinished | Commit to one illustration/icon style |
| No social proof | High-risk B2B buyers need evidence | Customer quotes + logos + stats are non-negotiable |
| Long, cluttered pages | Busy personas bounce | Cut every section that doesn't answer "why choose us?" |

---

## Reference files

- `references/double-diamond.md` — Full Double Diamond methodology
- `references/competitive-review.md` — Competitive review process and scoring
- `references/persona-workshop.md` — Workshop facilitation guide with timing
- `references/visual-identity.md` — Visual identity system for SaaS brands

## Templates

- `templates/competitive-review-table.md` — Worksheet for reviewing competitor sites
- `templates/proto-persona.md` — Proto persona canvas
- `templates/user-journey-map.md` — User journey map with stages
- `templates/site-map.md` — Home page site map template
- `templates/homepage-wireframe.md` — Section-by-section wireframe brief

## Assets

- `assets/saas-ux-checklist.md` — Pre-launch UX checklist for SaaS home pages
- `assets/color-palette-guide.md` — SaaS color theory and palette formulas
