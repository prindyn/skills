# SaaS Home Page UX Checklist

Use this checklist before launching or presenting a redesigned SaaS website. It is organized by the core UX principles most relevant to B2B SaaS — particularly for analytical, risk-averse decision-makers who skim rather than read.

Review this checklist at two stages:
1. **After wireframing** — to catch structural problems before investing in high-fidelity design
2. **Before launch** — to verify the final implementation

---

## 1. First impression (above the fold)

The content visible before the user scrolls is the most valuable real estate on the page. If this doesn't land, nothing below matters.

- [ ] **Headline communicates the value proposition in ≤ 8 words**
  - Test: can someone outside your industry read the headline and know what the company does?
  - Avoid: "Transforming [industry] through innovation" — meaningless without context
  - Prefer: "Regulatory submissions in half the time" — outcome-focused and specific

- [ ] **Subheadline adds detail in ≤ 2 sentences**
  - Should answer: who is this for? What problem does it solve?

- [ ] **At least one CTA is visible without scrolling**
  - CTA label describes an action + outcome (e.g., "Book a free demo", not just "Get started")

- [ ] **The page loads in < 3 seconds** on a standard connection
  - Use Google PageSpeed Insights to check

- [ ] **Hero visual is relevant to the product** (not generic stock photography of "professionals on laptops")

---

## 2. Trust and social proof

B2B buyers — especially analytical, risk-averse personas — need evidence before they engage. Trust signals must appear early.

- [ ] **Customer testimonials are visible within the first 3 sections**
  - At least 2–3 quotes; real customer photos; full name and title

- [ ] **Testimonials are specific, not generic**
  - Good: "Reduced our eCTD submission time by 40%"
  - Bad: "Highly recommend this platform"

- [ ] **Company size and industry are mentioned in testimonials** (so the reader can self-identify as "a company like that")

- [ ] **Customer logos are present** (if permissions obtained)
  - If no logos available, leading with testimonial photos is a strong alternative

- [ ] **Social proof quantified where possible**
  - Number of customers, years in business, success metrics (if real and verifiable)

- [ ] **Contact information is findable** (email, LinkedIn, physical address if relevant)
  - Not having visible contact info is a significant trust killer for B2B

---

## 3. Navigation and information architecture

- [ ] **Primary navigation has ≤ 6 items**

- [ ] **Navigation labels are plain language** (not invented product names that mean nothing to a new visitor)

- [ ] **CTA button in navigation is visually distinct** (colored button, not just a link)

- [ ] **Footer mirrors the header navigation**

- [ ] **No broken links** (test all navigation links before launch)

- [ ] **Mobile navigation works** (hamburger menu opens and closes; all links tap-friendly)

---

## 4. Content and readability

- [ ] **Body text is ≥ 16px**
  - 14px may look fine on a large monitor; it is straining on a laptop or phone

- [ ] **Contrast ratio passes WCAG AA**
  - Body text: ≥ 4.5:1 contrast against background
  - Large text (≥ 18px): ≥ 3:1 contrast
  - Tool: use WebAIM Contrast Checker (webaim.org/resources/contrastchecker/)

- [ ] **Text blocks are ≤ 5 lines per paragraph**
  - Dense paragraphs are abandoned by skimmers

- [ ] **Each section has a clear heading** — the user should understand the section's purpose in 1 second

- [ ] **Industry jargon is minimized above the fold**
  - If jargon is unavoidable, explain it inline: "eCTD (electronic Common Technical Document) submissions"

- [ ] **No spelling or grammar errors** (have someone unfamiliar with the content proofread)

---

## 5. CTAs (calls to action)

- [ ] **CTAs appear no more than 3 times on the home page**
  - Too many CTAs create friction for analytical buyers who feel pressured

- [ ] **CTA labels vary** — don't repeat the same label everywhere
  - e.g., "Book a demo" → "See how it works" → "Get in touch" — same action, different entry points

- [ ] **Primary CTA uses the primary brand color**

- [ ] **Secondary CTA (if used) uses a lower-emphasis style** (outline button or text link)

- [ ] **After clicking a CTA, something happens immediately** — a form, a calendar, a confirmation
  - "Thank you, we'll be in touch" is acceptable; silence is not

---

## 6. Visual consistency

- [ ] **One typeface family** (or two at most, with clear roles: one for headings, one for body)

- [ ] **Font sizes are consistent within each role** (all H2s are the same size; all body text is the same size)

- [ ] **Color palette uses the defined colors** — no ad-hoc colors introduced during development

- [ ] **Icons use a single style** (all line, all filled, all colored — not mixed)

- [ ] **Images/illustrations use a consistent style** — no mixing of stock photos with flat illustrations with AI art

- [ ] **Spacing is consistent between sections** — sections don't feel randomly spaced

---

## 7. Product clarity

- [ ] **The home page explains what the product does** without requiring a demo or a sales call

- [ ] **Feature descriptions use outcomes, not features**
  - Weak: "Our platform has a document management module"
  - Strong: "Manage all regulatory documents in one place — no more searching across email chains"

- [ ] **Links to product detail pages work** (if product pages exist)

- [ ] **Demo video or product screenshot is present** (helps technical buyers evaluate before committing to a call)

---

## 8. Contact and conversion

- [ ] **Contact form asks for ≤ 4 fields**
  - More fields = fewer completions. Name, email, company, and message are sufficient to start

- [ ] **The acquisition process is explained** ("Submit form → Free consultation → Get started")
  - This demystifies what happens after clicking the CTA

- [ ] **Form submission confirmation works** (test by submitting the form)

- [ ] **Email address for direct contact is visible** (some users won't use forms)

---

## 9. Accessibility

- [ ] **All images have descriptive alt text**

- [ ] **Form inputs have visible labels** (not just placeholder text — placeholder disappears when user types)

- [ ] **Interactive elements are keyboard-navigable** (Tab key should move between links and form fields)

- [ ] **Color is not the only differentiator** (e.g., error states also have a text message, not just a red border)

- [ ] **Font size can be increased** without breaking the layout (test with browser zoom at 125% and 150%)

---

## 10. Performance and technical

- [ ] **Images are optimized** (use WebP format; compress images before upload; lazy-load below-the-fold images)

- [ ] **No console errors** in the browser developer tools

- [ ] **Cookie consent banner is present** (required for GDPR-compliant sites serving EU users)

- [ ] **Privacy Policy page is linked** (required to use analytics, advertising, or contact forms)

- [ ] **SSL certificate is active** (URL shows `https://` — browsers warn users about insecure sites)

- [ ] **Site is mobile-responsive** (test on a real phone, not just browser resize)

- [ ] **LinkedIn sharing preview looks correct** (Open Graph meta tags set: title, description, image)

---

## Scorecard

Count checked items in each section:

| Section | Score | Max |
|---------|-------|-----|
| 1. First impression | /6 | 6 |
| 2. Trust and social proof | /6 | 6 |
| 3. Navigation | /5 | 5 |
| 4. Content and readability | /6 | 6 |
| 5. CTAs | /5 | 5 |
| 6. Visual consistency | /6 | 6 |
| 7. Product clarity | /4 | 4 |
| 8. Contact and conversion | /4 | 4 |
| 9. Accessibility | /5 | 5 |
| 10. Performance | /7 | 7 |
| **Total** | /54 | 54 |

**Interpretation:**
- 50–54: Launch-ready
- 42–49: Minor fixes needed before launch
- 35–41: Moderate issues; address high-priority items before launch
- < 35: Significant work needed; review with design and development team
