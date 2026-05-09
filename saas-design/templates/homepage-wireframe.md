# Homepage Wireframe Brief

Use this template to plan each section of the homepage wireframe before opening Figma (or your design tool). Filling this in first prevents blank-canvas paralysis and ensures design decisions are backed by user insights.

**Convention:**
- `[IMAGE]` = image placeholder (X box)
- `[ICON]` = icon placeholder (star box)
- `[TEXT]` = text placeholder (lorem ipsum)
- `CTA` = call-to-action button

---

## Section 0: Cookie consent banner

**Purpose:** Legal compliance for EU/international users.

**Layout:**
```
┌──────────────────────────────────────────────────────────────┐
│ 🍪 We use cookies to improve your experience.               │
│ [Customize]  [Reject all]  [Accept all]           ────────  │
└──────────────────────────────────────────────────────────────┘
```

**Design notes:** Position fixed to bottom of viewport. Keep copy minimal — link to Privacy Policy. Use subtle background that doesn't overwhelm the page content.

---

## Section 1: Header / Navigation

**Purpose:** Global navigation and primary CTA — visible on every page.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [LOGO]    Products  Services  About  Blog       [CTA BTN]  │
└─────────────────────────────────────────────────────────────┘
```

**Content checklist:**
- [ ] Logo (SVG preferred — scales without blur)
- [ ] Navigation links (max 5): ____, ____, ____, ____, ____
- [ ] Optional: Customer login link (separate from main nav)
- [ ] CTA button label: ________________

**Design notes:** On scroll, consider a sticky header with background blur (glassmorphism). The CTA button should use the primary brand color to stand out from the navigation links.

---

## Section 2: Hero

**Purpose:** Establish what the company does and why it matters — within the first 2 seconds of landing.

**Layout option A (text left, visual right):**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  [HEADLINE — 4–8 words]        ┌───────────────────────┐  │
│  [Subheadline — 1–2 sentences] │                       │  │
│                                │  [HERO ILLUSTRATION   │  │
│  [PRIMARY CTA]                 │   OR MOTION GRAPHIC]  │  │
│                                │                       │  │
│                                └───────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Layout option B (centered, visual behind):**
```
┌──────────────────────────────────────────────────────────────┐
│          [GRADIENT / ILLUSTRATION BACKGROUND]                │
│                                                              │
│              [HEADLINE — 4–8 words]                          │
│           [Subheadline — 1–2 sentences]                      │
│                                                              │
│                    [PRIMARY CTA]                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Content checklist:**
- [ ] Headline: ___________________________ (avoid jargon; write for a non-specialist reader)
- [ ] Subheadline (1–2 sentences): ___________________________
- [ ] CTA label: ___________________________ (e.g., "Book a demo", "See how it works")
- [ ] Visual: ☐ Illustration  ☐ Motion graphic  ☐ Screenshot  ☐ Video  ☐ Abstract gradient

**Design notes:**
- Headline test: can someone outside your industry understand what you do in 5 seconds?
- Avoid ALL CAPS in the headline — it reads as shouting
- For B2B: avoid excitement/hype language ("revolutionary", "game-changing") — use outcome language ("faster drug submissions", "your regulatory process, simplified")

---

## Section 3: Why us / Differentiators

**Purpose:** Establish credibility and key selling points. Convince the skeptical visitor this company is worth investigating further.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│          [Section heading: "What Sets Us Apart"]            │
│                                                             │
│   ┌────────────┐   ┌────────────┐   ┌────────────┐        │
│   │   [STAT]   │   │   [STAT]   │   │  [RATING]  │        │
│   │  [label]   │   │  [label]   │   │  [label]   │        │
│   └────────────┘   └────────────┘   └────────────┘        │
│                                                             │
│   [TAGLINE / SECONDARY MESSAGE — 1 sentence]               │
│   [Optional: supporting paragraph — 2–3 lines max]         │
│   [OPTIONAL: IMAGE representing the value]                  │
└─────────────────────────────────────────────────────────────┘
```

**Content checklist:**
- [ ] Section headline: ___________________________
- [ ] Stat 1: ______ + label: ______________________
- [ ] Stat 2: ______ + label: ______________________
- [ ] Stat or rating 3: ______ + label: _______________
- [ ] Supporting message: ___________________________

**Design notes:** Statistics must be real and sourced. If you don't have statistics yet, use differentiator columns instead (3 icons + titles + 2-sentence descriptions). Avoid unsubstantiated superlatives ("best", "fastest", "industry-leading").

---

## Section 4: Customer Feedback / Social Proof

**Purpose:** Build trust through peer validation. For analytical, risk-averse B2B buyers, this section is often the deciding factor.

**Layout option A (carousel with photo):**
```
┌─────────────────────────────────────────────────────────────┐
│           [Section heading: "Our Customer Feedback"]        │
│           [Optional subheading]                             │
│                                                             │
│  ◀  ┌──────────────────────────────────────────────┐  ▶   │
│     │  [CUSTOMER PHOTO]  "[Quote — 2–4 sentences]"  │      │
│     │                     Name, Title, Company      │      │
│     └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

**Layout option B (3 cards, no carousel):**
```
┌────────────────────────────────────────────────────────────┐
│         [Section heading: "What Our Customers Say"]        │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ [PHOTO]      │  │ [PHOTO]      │  │ [PHOTO]      │    │
│  │ "[Quote]"    │  │ "[Quote]"    │  │ "[Quote]"    │    │
│  │ Name, Title  │  │ Name, Title  │  │ Name, Title  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└────────────────────────────────────────────────────────────┘
```

**Content checklist:**
- [ ] Customer 1: Name _____, Title _____, Company _____, Quote: _____
- [ ] Customer 2: Name _____, Title _____, Company _____, Quote: _____
- [ ] Customer 3: Name _____, Title _____, Company _____, Quote: _____
- [ ] Customer photos: ☐ Real photos obtained  ☐ Using placeholder until photos collected
- [ ] Optional: customer logos row (if logos obtained and permissions granted)

**Design notes:**
- Real photos are non-negotiable — stock faces in testimonials destroy credibility
- Quotes must be specific ("Reduced our submission time by 3 weeks") not vague ("Great product")
- Get written permission before displaying customer names and companies

---

## Section 5: Products / Services

**Purpose:** Introduce the product portfolio clearly and efficiently. The user is now in evaluation mode.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│           [Section heading: "What We Offer"]                │
│           [Optional subheading]                             │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │  [ICON]               [ICON]              [ICON]    │  │
│   │  [Feature name]       [Feature name]      [Feature] │  │
│   │  [1–2 sentence desc]  [1–2 sentence desc] [desc]    │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│   │ [ICON]     │  │ [ICON]     │  │ [ICON]     │          │
│   │ [Product]  │  │ [Product]  │  │ [Service]  │          │
│   │ [Desc]     │  │ [Desc]     │  │ [Desc]     │          │
│   │ [Learn >]  │  │ [Learn >]  │  │ [Learn >]  │          │
│   └────────────┘  └────────────┘  └────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

**Content checklist:**
- [ ] Section headline: ___________________________
- [ ] Product/feature 1: Name _____, Description (1–2 sentences): _____
- [ ] Product/feature 2: Name _____, Description: _____
- [ ] Product/feature 3: Name _____, Description: _____
- [ ] Additional products/services: _____
- [ ] Icon style: ☐ Line icons  ☐ Filled icons  ☐ Custom illustrations

**Design notes:** Descriptions should be in plain language. Avoid technical acronyms unless your persona definitely knows them. Each product card "Learn more" link should go to a dedicated product page.

---

## Section 6: Blog / Resources (optional)

**Only include this section if 3+ blog posts exist.** An empty or outdated blog section signals neglect.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│               [Section heading: "Resources"]                │
│                                                             │
│  ┌─────────────────────┐  ┌────────────────────────────┐  │
│  │ [ARTICLE THUMBNAIL] │  │ [ARTICLE THUMBNAIL]         │  │
│  │ [Article title]     │  │ [Article title]             │  │
│  │ [Date + category]   │  │ [Date + category]           │  │
│  │ [Read more →]       │  │ [Read more →]               │  │
│  └─────────────────────┘  └────────────────────────────┘  │
│                            [See all posts →]               │
└─────────────────────────────────────────────────────────────┘
```

---

## Section 7: Get in Touch / Contact

**Purpose:** Convert interest into contact. Demystify the process by showing exactly what happens after submission.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│         [Section heading: "Get in Touch"]                   │
│         ["Let us help you [outcome]"]                       │
│                                                             │
│   Step 1 ───────→ Step 2 ───────→ Step 3                   │
│   Submit form     Free consult     Meet your goals          │
│   [icon]          [icon]           [icon]                   │
│                                                             │
│   ┌──────────────────────────────────┐                      │
│   │ Name: [___________________]      │                      │
│   │ Email: [__________________]      │                      │
│   │ Company: [________________]      │                      │
│   │ Message: [________________]      │                      │
│   │          [________________]      │                      │
│   │                   [SUBMIT CTA]   │                      │
│   └──────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

**Content checklist:**
- [ ] Step 1 label: ___________________________
- [ ] Step 2 label: ___________________________
- [ ] Step 3 label: ___________________________
- [ ] Form fields (keep to 3–4 minimum): ___________________________
- [ ] Submit button label: ___________________________
- [ ] Confirmation message after submission: ___________________________

**Design notes:** The 3-step visualization is critical — it shows the user exactly what happens after they submit, reducing the anxiety of "contacting sales." Keep the form short. Every additional field reduces completion rate.

---

## Footer

**Purpose:** Reference navigation for users who reach the bottom; legal and contact information.

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [LOGO]                                                     │
│  [Short company description — 2–3 sentences]  [LinkedIn]   │
│                                                             │
│  Company          Products         Services     Legal       │
│  About us         Product 1        Service 1    Privacy     │
│  Our team         Product 2        Service 2    Terms       │
│  Careers          Product 3        Contact      Cookies     │
│                                                             │
│  © [Year] [Company name]. All rights reserved.             │
└─────────────────────────────────────────────────────────────┘
```

---

## Wireframe review checklist

Before handing off to high-fidelity design, confirm:

- [ ] Every section has a clear, single purpose
- [ ] CTAs are varied (not the same button label repeated 4 times)
- [ ] Information hierarchy flows logically (trust → evidence → products → contact)
- [ ] Customer social proof appears before the product pitch
- [ ] No section requires the user to call for basic information
- [ ] Footer mirrors header navigation
- [ ] Client has reviewed and approved the wireframe structure
