# Book Plan Template

Fill out this plan before starting any crawl. A clear plan produces a book that
reads as if written by an author. An unclear plan produces a book that reads like
a sitemap dump.

Answer each section before proceeding. You do not need to show this to the user
unless they ask — it is your working document.

---

## 1. Concept and scope

**Website URL:** ___

**Book title (working):** ___

**One-sentence description of the book:**
> [Example: "A practical guide to the 23 Gang of Four design patterns in Python, organized for developers who already know OOP basics."]

**What this book covers:**
-
-
-

**What this book explicitly does NOT cover:**
-
-
-

**Is this one book or two?**
- [ ] One book (the content forms a single coherent arc)
- [ ] Two books (the site has two peer sections of roughly equal depth)
- [ ] One book with Parts (two topics, kept together, each with a Part header)

If two books or Parts, what are the two topics?
- Book/Part 1: ___
- Book/Part 2: ___

---

## 2. Reader profile

**Who is this book for?**
> [Example: "Mid-to-senior software engineers who are fluent in OOP and want to understand design patterns at a conceptual level, not just memorize the Gang of Four catalog."]

**What does the reader already know?** (Don't explain these things)
-
-
-

**What does the reader NOT yet know?** (Explain these things clearly)
-
-
-

**How will the reader use this book?**
- [ ] Cover-to-cover read (progressive learning)
- [ ] Reference lookup (dip in and out by topic)
- [ ] Both (preface should explain which to do when)

---

## 3. Book type

**Type chosen in Phase 0:**
- [ ] Technical Reference
- [ ] Tutorial / Learning Book
- [ ] Conceptual Guide
- [ ] Cookbook / Quick Reference
- [ ] Narrative Explainer

**Rationale:** [Why does this type match the site's content and the reader's goal?]

---

## 4. Chapter plan

List the chapters in reading order. For each chapter, note the pages from the site
that belong there. Don't list more than 10 chapters for most books.

| # | Chapter title | Content pages (approximate) | Notes |
|---|---|---|---|
| 0 | Preface | (original write) | Author-voice, no meta-commentary |
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| … | | | |
| N | Appendix | code-heavy pages | cross-refs to main chapters |

**Chapter ordering principle for this book type:**
> [Example: "Foundational OOP concepts → Pattern catalog grouped by family → Anti-patterns → Extended code listings in Appendix"]

---

## 5. Content to suppress

List known content types to exclude. Review after the crawl to add site-specific patterns.

| Pattern | Reason |
|---|---|
| `/privacy`, `/terms`, `/legal` | Legal pages — not book content |
| `/about`, `/login`, `/signup` | Account/personal pages |
| `/sale`, `/pricing`, `/buy` | E-commerce pages |
| `/forum`, `/community` | Community pages |
| [site-specific 1] | |
| [site-specific 2] | |

**Site-specific exclude regex:**
```
(privacy|terms|legal|gdpr|cookies|about|sale|cart|signup|login|pricing|buy|checkout|testimonials|faq|forum)
```

Add site-specific patterns after reviewing the crawled URL list.

---

## 6. Images

**User requested images?**
- [ ] Yes → run `fetch_images.py` after scraping; review manifest before building
- [ ] No → skip image steps; run scraper without `--keep-images`

**Likely valuable image types on this site:**
- [ ] Architecture/UML diagrams
- [ ] Code output screenshots
- [ ] Tutorial step screenshots
- [ ] Charts and graphs
- [ ] Other: ___

**Known decorative image patterns to skip:**
- ___
- ___

---

## 7. PDF settings

**Target page count:** ___

**Output filename:** ___

**Running header text:** ___

**TOC depth:** 2 or 3 (2 for reference books; 3 for tutorials with deep sections)

**Index:** 
- [ ] Include (useful for reference and conceptual books with many proper nouns)
- [ ] Exclude (better for cookbooks and tutorials where TOC is the navigation tool)

**Backend:**
- [ ] WeasyPrint (preferred)
- [ ] pdfkit + wkhtmltopdf (fallback if WeasyPrint fails)

---

## 8. Preface outline

Draft the key points of the Preface before writing it:

**Opening hook:** [One sentence that draws the reader in — a question, a problem, a surprising fact]

**Audience statement:** [Who this is for, stated plainly]

**Scope statement:** [What's covered and what isn't]

**How to read:** [Linear? Reference? Which chapters to skip if you already know X?]

**Closing thought:** [What the reader will be able to do after finishing]

Write the actual Preface using `templates/preface.md` after the MECE step is done.
