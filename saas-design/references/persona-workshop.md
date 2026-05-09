# Proto Persona Workshop Guide

A proto persona is a best-guess representation of the primary user, built from a team's existing knowledge rather than formal research. It is faster and cheaper than full user research while still providing a shared, concrete user model that guides design decisions.

This workshop guide covers a 60–90 minute session suitable for startup founding teams, product managers, or any small group with knowledge of the customer base.

---

## Table of contents

1. Why a proto persona (not full user research)?
2. Before the workshop
3. Phase 1: Warmup — Who are your audience?
4. Phase 2: Proto persona creation
5. Phase 3: User journey exploration
6. After the workshop
7. Limitations and how to address them

---

## 1. Why a proto persona (not full user research)?

Full user research — interviews, surveys, usability testing — produces highly accurate personas but takes weeks and requires access to real users. For early-stage startups or companies beginning a redesign, a proto persona built in a workshop:

- Takes 1–2 hours instead of weeks
- Extracts knowledge the founding team already has but hasn't made explicit
- Creates team alignment (the persona becomes a shared reference, not one person's opinion)
- Is a living document: update it as real customer data is collected

The tradeoff is accuracy. A proto persona reflects team assumptions, which may not match actual user behavior. It should be treated as a starting hypothesis, not a validated fact.

---

## 2. Before the workshop

**Participants:** 2–6 people. Ideal mix includes founders or product leads who talk to customers regularly, and anyone who will make design decisions.

**Preparation:** Ask participants to come prepared to answer: "Who are the current users and future potential users of your website?" Framing this as homework before the session makes the warmup faster.

**Tools:**
- FigJam (recommended) or Miro for remote sessions
- Physical sticky notes and a whiteboard for in-person
- Timer (phone works fine)
- Templates: load `templates/proto-persona.md` and `templates/user-journey-map.md` into the board

**Duration:** 60 minutes minimum; 90 minutes if you want depth in the user journey phase.

---

## 3. Phase 1: Warmup — Who are your audience? (10–15 min)

**Goal:** Surface all possible audience types without filtering. Separate individual contributions before discussion.

**Prompt:** "Make note of all of your audience types — past, present, and future desired. Don't worry about refining just yet. Make a list of ALL types."

**Process:**
1. Give participants 3 minutes to silently write one audience type per sticky note
2. Collect all notes on the board
3. Read through them together and discuss for 5–10 minutes
4. Group related types and identify patterns

**What to look for in the discussion:**
- Who actually makes the purchase decision vs. who uses the product daily? (Often different people in B2B)
- Who influences the buying decision without making it?
- Are there audience types that are aspirational but not yet customers?

**Example output for a regulatory SaaS startup:**
- Head of Regulatory Affairs
- Regulatory Operations Persons
- IT Lead looking for eCTD publishing solutions
- Partners and consulting companies
- Competitors researching the market
- Folks evaluating vendors for the first time

---

## 4. Phase 2: Proto persona creation (25–35 min)

**Goal:** Select the primary user and build a detailed, actionable profile.

**Selecting the persona:** From the warmup output, identify who makes the final purchase decision. In B2B SaaS, this is often a department head or senior manager, not the daily user. Choose this person — designing for the person who decides to buy is usually higher-leverage than designing for the person who uses the product.

**Building the persona — key dimensions:**

### Basic information
- Name (give them a real name — it makes the persona feel real in future discussions)
- Age range
- Gender (use what is most representative of the actual customer base)
- Education background
- Career background and current role
- Geographic context (region, company size)

### Personality traits
Use sliders between opposites — this forces nuanced thinking and avoids stereotypes:

- Introvert ←——→ Extrovert
- Analytical ←——→ Creative
- Busy ←——→ Time-rich
- Organized ←——→ Messy
- Risk-averse ←——→ Risk-taking

**Why this matters for web design:** An introverted, analytical, risk-averse persona does not want to be pressured into a sales call. They want clear, self-service information and evidence-based trust signals (statistics, customer testimonials, case studies).

### Goals and needs
Ask participants: "What does this person need to accomplish?"

Have them write one goal per sticky note, then vote (using heart emojis or dot stickers) to prioritize the top 3–5.

Common B2B SaaS goals:
- Return on investment / cost justification
- Operational efficiency for their team
- Keeping the regulatory/compliance/etc. process working
- Learning and staying current in their field
- Building their professional reputation

### Frustrations
Ask: "What frustrates this person when evaluating and using tools like ours?"

Vote to surface the most critical frustrations.

Common B2B SaaS frustrations:
- Current processes not working, causing team complaints
- Unclear pricing that requires a phone call to understand
- End-to-end process not fully supported — must patch multiple tools
- Promises of features that are not yet delivered
- Being asked to commit to a demo before seeing basic information

**Design implication:** Frustrations directly map to homepage requirements. If the persona hates having to call to get pricing, ensure the homepage gives enough information to evaluate without a call.

---

## 5. Phase 3: User journey exploration (20–30 min)

**Goal:** Map the persona's journey from first hearing about the product to becoming a loyal customer.

Use the **five stages:** Discovery → Interest → Consideration → Acquisition → Loyalty

For each stage, fill in:
- **User steps:** What happens at this stage?
- **User actions:** What does the persona actually do?
- **Goals & experiences:** What is the persona trying to accomplish?
- **Feelings and thoughts:** Use emoji scale (😀😐😕😟) to show emotional state
- **Pain points:** What causes friction or frustration?
- **Opportunities:** How might the website or product address these pain points?

**Facilitation approach:**
1. Fill in user steps first (this is the "skeleton" of the journey)
2. Then add user actions — what does Hillary actually do at each step?
3. Add feelings — this is where it gets interesting. Annotation with emoji creates surprising empathy
4. Identify pain points — where does frustration spike?
5. Close with opportunities — how can the website reduce these friction points?

**Key insight prompt for each stage:** "What does this person need to know/feel/do to move to the next stage?"

**Example journey segment (Discovery → Interest):**

| | Discovery | Interest |
|--|-----------|----------|
| Actions | Finds site via LinkedIn or recommendation | Reads hero section; looks for customer references |
| Goals | Find a new regulatory platform | Understand if this company is legitimate |
| Feelings | 😐 (skeptical, evaluating) | 😐 → 🙂 (if references are visible) |
| Pain points | Hard to find website; it's slow to load | Can't find references from similar customers |
| Opportunities | Optimize SEO/LinkedIn presence | Show customer logos and quotes prominently, early |

See `templates/user-journey-map.md` for the full template.

---

## 6. After the workshop

**Document immediately:** Write up the persona and journey map within 24 hours while memory is fresh. Include images of the FigJam/whiteboard.

**Share with stakeholders:** The persona should become a shared reference. When design decisions are debated later ("should we add this section?"), ask "would Hillary want this?"

**Add to business documents:** If the company has a business plan or product strategy document, add the persona there so it's accessible to future team members.

**Schedule a review:** Proto personas should be updated when new customer data is collected — after user interviews, support tickets analysis, or sales call recordings. Mark the persona document with its creation date.

---

## 7. Limitations and how to address them

| Limitation | Mitigation |
|-----------|-----------|
| Based on team assumptions, not real users | Mark as "proto persona v1" and update after customer interviews |
| May reflect team's wishful thinking about users | Use voting to surface disagreements; don't let one voice dominate |
| Single persona may miss important audience segments | Create a secondary persona for important secondary audiences |
| Workshop findings may become outdated | Review every 6 months; update when significant customer data is available |

---

## References

- Gothelf, J. & Seiden, J. (2021). *Lean UX, 3rd Edition.* O'Reilly Media.
- Laubheimer, P. (2020). 3 Persona Types. Nielsen Norman Group.
- Fairhurst, S. (n.d.). Persona & User Flows workshop, FigJam board. Figma Community.
- Figma & Chin, S. (n.d.). User journey map, FigJam board. Figma Community.
