# Book Review Checklist

Run this checklist after Step 9 (Write the Preface) and before Step 11 (Build the PDF).
Fix every issue found. Do not generate the PDF until all critical items pass.

Items marked **[CRITICAL]** will produce an obviously broken book if skipped.
Items marked **[IMPORTANT]** significantly affect quality.
Items marked **[NICE]** are improvements that matter but are not blockers.

---

## Section 1: Meta-commentary (no mentions of the tool process)

**[CRITICAL]** Scan every `.md` file for these patterns. If found, remove them:

```bash
grep -rn -i "scraped from\|crawled from\|compiled from\|assembled from\|generated from" crawl_output/pages/
grep -rn -i "this document is\|this book was\|pages were deduplicated\|content was organized" crawl_output/pages/
grep -rn -i "we scraped\|we crawled\|we gathered\|we deduplicated\|we organized" crawl_output/pages/
grep -rn -i "postprocess\|build_pdf\|scrape\.py\|crawl\.py\|write-book" crawl_output/pages/
grep -rn -i "offline reading\|offline edition\|this compiled edition" crawl_output/pages/
```

Any match in the main content or preface is a critical defect. Fix before building.

**[CRITICAL]** Check the Preface specifically:
- Does it mention the source website as a "website" or "online resource we scraped"? → Rewrite
- Does it explain the PDF generation process? → Remove those sentences
- Does it list how many pages were included? → Remove (this is a tool metric, not reader value)
- Does it sound like it was written by a knowledgeable author? → Keep

---

## Section 2: Opening content quality

**[CRITICAL]** Check the first chapter (after the Preface):

```bash
head -50 crawl_output/pages/0001_*.md
```

- Is Chapter 1 an SEO landing page? (Signs: lots of bullet lists, no depth, sells the site)
  → Suppress it and promote the next substantive chapter
- Is Chapter 1 a navigation index? (Signs: just a list of links or section titles)
  → Suppress it
- Does Chapter 1 actually teach or explain something? → Keep

**[IMPORTANT]** Check the Preface (`0000_preface.md`):
- Does it address the reader directly? ("If you're a software engineer who...")
- Does it state scope clearly? ("This book covers X. It does not cover Y.")
- Does it recommend a reading approach? ("Read cover-to-cover" or "Use as a reference")
- Is it at least 150 words? (Shorter prefaces are usually superficial)
- Is it under 600 words? (Longer prefaces lose the reader before the book starts)

---

## Section 3: Noise and site chrome

**[CRITICAL]** Run inspect_sample on a larger sample before the final build:

```bash
python scripts/inspect_sample.py --pages-dir crawl_output/pages/ --n 10
```

Check for:
- Raw `https://` URLs in body text → Run `postprocess.py --url-to-footnotes`
- "Was this helpful?" / "Share this" / "Edit this page" → Fix in scraper patterns
- "Buy now" / "Get the book" / "Tired of reading?" → Fix in scraper patterns
- "Cookie notice" / "GDPR" / "privacy" → These pages should have been excluded
- Navigation file-tree artifacts (bare lines like "Intro / Button / Component") → Fix patterns

**[IMPORTANT]** Check for legal page leakage:

```bash
grep -rn -i "privacy policy\|terms of service\|terms of use\|cookie policy\|imprint" crawl_output/pages/ | grep -v "^Binary"
```

Any matches indicate a legal/compliance page leaked through. Suppress those files in `_index.json`.

**[IMPORTANT]** Check for CTA fragments:

```bash
grep -rn -i "add to cart\|money.back\|spring sale\|buy as a gift\|tired of reading" crawl_output/pages/
```

---

## Section 4: Content structure

**[IMPORTANT]** Verify chapter ordering reflects the book type chosen in Phase 0:

- Tutorial: Does Chapter 2+ assume what Chapter 1 teaches? Good. Does Chapter 2 assume
  what Chapter 5 teaches? Problem — reorder.
- Reference: Are chapters grouped by domain? Good. Are chapters alphabetical within domain?
  Also good. Is it crawl order? Problem.
- Conceptual: Are foundational concepts before patterns? Are patterns before anti-patterns?

**[IMPORTANT]** Check for duplicate content:

```bash
python scripts/postprocess.py --pages-dir crawl_output/pages/ --deduplicate --dry-run 2>/dev/null | grep "would suppress"
```

If postprocess already ran, check `_index.json` for `"suppress": true` entries and verify
that the reason is legitimate.

**[NICE]** Verify chapter page counts are balanced:
- No chapter should have fewer than 2 pages (probably should merge it into another chapter)
- No chapter should have more than 30% of the book's pages (probably should split it)

---

## Section 5: Images (only if user requested images)

**[CRITICAL]** Verify no broken image references:

```bash
grep -rn '!\[' crawl_output/pages/ | grep -v "crawl_output/images/" | grep "http"
```

Any `![alt](http://...)` reference that still points to an external URL means
`fetch_images.py` did not process that image. Either run it again or remove the reference.

**[IMPORTANT]** Open `crawl_output/images/_manifest.json` and review:
- Are any images obviously decorative (avatars, logos, social icons)? Remove them from
  the manifest and delete the reference in the `.md` file.
- Are any images broken (download failed, 404)? Remove the reference.
- Are the images that remain genuinely useful — diagrams, figures, screenshots that
  illuminate the text?

**[NICE]** Check that images have descriptive alt text:

```bash
grep -rn '!\[\](' crawl_output/pages/
```

Empty alt text (`![]()`) is inaccessible. Add a brief description.

---

## Section 6: Table of contents and index

**[IMPORTANT]** Check TOC size:

```bash
python -c "
import json
idx = json.loads(open('crawl_output/pages/_index.json').read())
active = [r for r in idx if not r.get('suppress') and not r.get('error')]
print(f'{len(active)} active pages → estimated TOC entries')
"
```

- Under 50 entries: the book may be too thin
- Over 300 entries: the TOC will be overwhelming; consider increasing `--toc-max-depth` to 2

**[IMPORTANT]** Check if an index will be useful:
- Run `build_pdf.py --html-only` and count `<div class='index-entry'>` elements in the HTML
- If > 300 unique headings: pass `--no-index` — the TOC is the better navigation tool
- If 50–300: review for generic terms; pass `--index-exclude-terms` to remove them

---

## Section 7: Final HTML review (before PDF render)

**[CRITICAL]** Run `build_pdf.py --html-only` and open the HTML file. Verify:

- [ ] Title page shows the correct book title (not a URL)
- [ ] Table of contents entries are meaningful (not "Untitled" or URL slugs)
- [ ] No blank pages between chapters (double page-break issue)
- [ ] No raw URLs in body text anywhere
- [ ] No "This document was compiled from..." or similar text anywhere
- [ ] Chapter 1 is genuine content
- [ ] Preface reads as an author-written page
- [ ] Images (if included) display correctly and are positioned in context
- [ ] Appendix pages have "See also:" cross-references to main chapters
- [ ] Index (if present) is curated and useful

Once all items pass, build the PDF.
