---
name: write-book
description: Crawl a website, scrape all discoverable pages, preserve text formatting, and compile the content into a downloadable PDF book. Use this skill whenever the user wants to turn a website, documentation site, wiki, or blog into a PDF book or eBook. Trigger when the user mentions scraping a site to PDF, converting website content to a book, archiving a site as a document, or asks to "make a book from" a URL. Also trigger for requests like "download site as PDF", "scrape and export to book", or "compile website docs into PDF". Use this skill proactively any time a user shares a URL and wants something readable or downloadable from it. Always ask the user for a website URL before proceeding — never start work without one.
author: vprindyn@gmail.com
version: "2.1"
compatibility: Requires Python 3.8+, pip packages listed in scripts/requirements.txt (requests, beautifulsoup4, lxml, html2text, weasyprint or pdfkit, tqdm, Markdown, Pygments, Pillow)
---

# write-book

Crawl a website from a root URL, discover every reachable page on the same domain, scrape textual content while preserving formatting, optionally embed valuable images, clean out site chrome and non-book content, organize into a clean reader-first structure, and compile everything into a well-formatted PDF book with a full table of contents.

---

## Phase 0: Gather intent (ALWAYS do this first — before any other action)

Before installing anything or running any script, ask the user three questions. Do not proceed until you have answers to at least the first two.

### 0-A. Website URL (required)

Ask for the website URL if not already provided. Never start a crawl without one.

> "What website should I turn into a book? Please share the root URL (e.g. `https://docs.example.com`)."

### 0-B. Book type (required — propose variants)

Ask what kind of book the user wants. Present the five variants below and let them choose (or describe something different):

> "What kind of book do you want? Here are five common styles — pick one or describe your own:
>
> 1. **Technical Reference** — Comprehensive coverage with deep index. Best for API docs, full library docs, exhaustive language references.
> 2. **Tutorial / Learning Book** — Progressive learning arc: concepts → examples → exercises. Best for courses, how-to guides, step-by-step content.
> 3. **Conceptual Guide** — Explains patterns, principles, and architecture in narrative depth. Best for design guides, architecture docs, opinionated frameworks.
> 4. **Cookbook / Quick Reference** — Recipe-style chapters, optimized for lookup. Best for command references, cheat-sheet aggregation, pattern libraries.
> 5. **Narrative Explainer** — Flowing prose, story-driven progression. Best for wikis, knowledge bases, or blogs with a coherent arc.
>
> Your choice shapes chapter ordering, depth, and how the Preface is written."

See `references/book-types.md` for structural guidance per type.

### 0-C. Images (required — yes or no)

> "Should I include images from the website in the book? If yes, I'll identify diagrams, screenshots, and figures that add value and embed them — decorative, marketing, and icon images will be excluded."

Record the answer. If yes, follow the image workflow in Step 5b and `references/image-handling.md`.

---

## Core principles (read before starting)

**DO:**
- Ask for the URL, book type, and image preference before starting anything
- Crawl once to list URLs, then grep for junk before scraping
- Inspect 5 random scraped `.md` files before building the PDF
- Exclude `privacy|terms|legal|gdpr|cookies|imprint|about|sale|cart|signup|login` in every crawl
- Strip site CTAs/upsells with a site-specific regex (e.g. "Tired of reading?")
- Drop external link URLs entirely — keep only the link text
- Remove navigation/widget blocks (e.g. "In Other Languages" tab rows) via CSS selectors
- Write your own 1-page Preface as if you are an author — audience, scope, how to read the book
- Write the Preface in an engaging, reader-focused voice (see `templates/preface.md`)
- Add cross-references from appendix code examples back to their main chapter
- Decide upfront whether you're writing one book or two — give Parts clear framing
- Run the mandatory book review checklist (`references/book-review-checklist.md`) before generating the PDF
- Plan the book structure before writing a single line (see `templates/book-plan.md`)
- Select images thoughtfully: only diagrams, figures, and screenshots that illuminate the text

**DON'T:**
- Don't start without a URL from the user
- Don't start without knowing the book type
- Don't explain your process inside the book — no "This book was scraped from...", "The content was organized using...", "We deduplicated X pages..." — the reader does not need to know how you made it
- Don't use the auto-generated preface from `build_pdf.py`; always pass `--no-auto-preface` and write a real preface
- Don't write meta-commentary in chapter introductions ("In this chapter, we gathered all pages about...")
- Don't ship the auto-preface plus a user-written Preface chapter — pick one
- Don't include Terms of Service, Privacy Policy, or GDPR pages
- Don't leave raw `https://` URLs in body text
- Don't let SEO landing pages become your opening chapters
- Don't stack `page-break-before` and `page-break-after` — creates blank pages
- Don't auto-generate a back-of-book index from a noisy site without curating it
- Don't trust the skill's exclusion defaults alone — always check the URL list for legal/account/CTA noise
- Don't rebuild the PDF to check quality — inspect the Markdown first
- Don't crawl every language variant; pick one and exclude the rest
- Don't keep duplicate landing pages (`/`, `/refactoring`, `/design-patterns` are often 80% the same)
- Don't add every image you find — only diagrams, figures, and screenshots that genuinely illuminate the text

---

## Workflow overview

0. **Gather intent** — URL, book type, images (Phase 0 above).
1. **Plan the book** — complete `templates/book-plan.md` before any crawl.
2. **Gather requirements** — confirm page count, filters, output filename.
3. **Install dependencies**
4. **Crawl and inspect URLs** — crawl, print the URL list, grep for junk, re-crawl if needed.
5. **Scrape content** — run `scripts/scrape.py` (with `--keep-images` if user said yes).
   - **5b (images only):** run `scripts/fetch_images.py` to download and filter valuable images.
6. **Inspect a sample** — run `scripts/inspect_sample.py` to review 5 random pages before continuing.
7. **Post-process** — run `scripts/postprocess.py` to deduplicate, strip remaining noise, and flag code-heavy pages.
8. **Organize with MECE** — run the formatter agent to group pages into chapters in reader-first order per the book type chosen in Phase 0.
9. **Write the Preface** — write one original, author-voice page. No meta-commentary. Use `templates/preface.md`.
10. **Book review** — run through `references/book-review-checklist.md`. Fix all issues found before building.
11. **Build the PDF** — HTML first, inspect, then render to PDF. Pass `--no-auto-preface` always.
12. **Deliver** — report path, page count, and file size.

---

## Step-by-step instructions

### 1. Plan the book

Before asking for technical inputs, plan the book structure based on the book type chosen in Phase 0. Fill out `templates/book-plan.md` mentally or on paper:

- **Scope:** What does this book cover? What does it explicitly NOT cover?
- **Reader:** Who is the intended reader? What do they know already?
- **Structure:** One book or two? How many chapters? In what order?
- **Arc:** What is the progression? (Foundational → Applied → Reference? Concept → Pattern → Code?)
- **Voice:** Analytical? Instructional? Narrative? Match the site's content style.

A book with a clear plan reads as if written by an author, not assembled by a script.

See `references/book-types.md` for chapter order recommendations per book type.
See `references/book-writing-guide.md` for principles of book-quality writing and structure.

### 2. Gather requirements

Confirm these inputs with the user **after** Phase 0 but **before** starting a crawl:

| Input | Required | Default | Notes |
|---|---|---|---|
| **Root URL** | Yes | — | Starting page, e.g. `https://docs.example.com` |
| **Target page count** | Yes | — | Approximate number of PDF pages wanted. Use `--max-pages` ≈ target × 3. |
| **Output filename** | No | `book.pdf` | — |
| **Max depth** | No | `5` | Link-hops from root |
| **URL filter** | No | none | Regex pattern pages must match |
| **Content selector** | No | auto | CSS selector for main content, e.g. `.article-body` |
| **Language** | No | English | If site is multi-language, pick one; exclude all others |

Confirm before starting a crawl on large sites (> 200 pages estimated).

### 3. Install dependencies

```bash
pip install -r scripts/requirements.txt
```

If the user wants images, also install Pillow for image validation:

```bash
pip install Pillow
```

If WeasyPrint fails to install (common on headless servers), fall back to `pdfkit` + `wkhtmltopdf`. See `references/pdf-backends.md` for details.

### 4. Crawl and inspect URLs

**Step 4a — Crawl:**

```bash
python scripts/crawl.py \
  --url "https://example.com" \
  --max-depth 5 \
  --max-pages 300 \
  --exclude "(privacy|terms|legal|gdpr|cookies|imprint|about|sale|cart|signup|login|pricing|buy|checkout|testimonials|reviews|faq|payment|refund|forum|community|vote|userecho|newsletter|subscribe|register|account|zh|ja|ko|pl|de|fr|es|pt|ru)" \
  --output crawl_output/sitemap.json
```

**Step 4b — Inspect the URL list before scraping:**

```bash
python -c "
import json
data = json.loads(open('crawl_output/sitemap.json').read())
for p in data['pages']:
    print(p['url'])
" | grep -iE "(privacy|terms|legal|gdpr|about|cookies|imprint|login|signup|sale|cart|faq|testimonial|review|forum|pricing|refund|guarantee|newsletter|subscribe|account|register)"
```

If the grep returns hits, tighten `--exclude` and re-crawl before scraping.

**Step 4c — Check for duplicate landing pages:**

```bash
python -c "
import json
data = json.loads(open('crawl_output/sitemap.json').read())
for p in data['pages']:
    print(p['depth'], p['url'])
" | sort -n | head -30
```

Depth-0 and depth-1 pages are often SEO duplicates. Plan to suppress them in the MECE step.

See `references/crawling-guide.md` and `references/content-exclusions.md`.

### 5. Scrape content

**Without images:**

```bash
python scripts/scrape.py \
  --sitemap crawl_output/sitemap.json \
  --output crawl_output/pages/ \
  --format markdown \
  --exclude "(privacy|terms|legal|gdpr|cookies|imprint|about|sale|cart|signup|login|pricing|buy|checkout|testimonials?|reviews?|faq|payment|refund|forum|userecho)" \
  --min-words 200
```

**With images (user said yes in Phase 0):**

Add `--keep-images` to preserve image references in the scraped Markdown:

```bash
python scripts/scrape.py \
  --sitemap crawl_output/sitemap.json \
  --output crawl_output/pages/ \
  --keep-images \
  --exclude "(privacy|terms|legal|gdpr|cookies|imprint|about|sale|cart|signup|login|pricing|buy|checkout|testimonials?|reviews?|faq|payment|refund|forum|userecho)" \
  --min-words 200
```

### 5b. Fetch and filter images (only if user said yes to images)

After scraping, run the image fetcher to download valuable images and rewrite Markdown references to local paths:

```bash
python scripts/fetch_images.py \
  --pages-dir crawl_output/pages/ \
  --images-dir crawl_output/images/ \
  --root-url "https://example.com"
```

This script:
- Scans all `.md` files for `![alt](url)` image references
- Filters out decorative, marketing, icon, and logo images using URL patterns and alt-text heuristics
- Downloads images that appear to be diagrams, figures, code screenshots, or illustrations
- Rewrites `.md` files to use local paths (`../images/filename.ext`)
- Outputs a manifest at `crawl_output/images/_manifest.json`

Review the manifest and remove any images that are not genuinely useful. See `references/image-handling.md` for full guidance.

### 6. Inspect a sample before continuing

**Before running post-process or building the PDF, always inspect 5 random pages:**

```bash
python scripts/inspect_sample.py \
  --pages-dir crawl_output/pages/ \
  --n 5
```

Look for:
- Raw `https://` URLs still in body text
- Site chrome that slipped through (navigation text, "Was this page helpful?", cookie notices)
- CTA/upsell fragments ("Buy now", "Get the book", "Tired of reading?")
- "In Other Languages" tab lists that are just link lists with no prose
- Pages that are 90% code with no explanation (candidates for appendix)
- SEO landing pages masquerading as content (lots of bullet lists, no depth)
- Meta-commentary about scraping or tool process

Fix patterns before proceeding.

### 7. Post-process scraped content

```bash
python scripts/postprocess.py \
  --pages-dir crawl_output/pages/ \
  --deduplicate \
  --collapse-language-stubs \
  --move-code-appendix \
  --url-to-footnotes \
  --min-content-words 150
```

### 8. Organize content (MECE structure + cross-references)

Run the formatter agent (`agents/formatter-agent.md`) with the book type in mind. The chapter order should reflect the book type chosen in Phase 0:

- **Technical Reference:** Alphabetical or domain-grouped sections with a strong index
- **Tutorial:** Strict beginner → intermediate → advanced progression
- **Conceptual Guide:** Foundational principles → patterns → anti-patterns
- **Cookbook:** Domain-grouped recipes with lookup-optimized structure
- **Narrative:** Thematic arc with conceptual flow

For any type: always put foundational material before advanced, concepts before code, and open with an entry point the reader needs — not an SEO landing page.

See `references/book-types.md` for per-type chapter ordering.

### 9. Write the Preface

Write a single original page in the voice of an informed author — not a tool report. The Preface must read as if a human expert wrote it for this specific reader. Use `templates/preface.md` as a starting point.

**The Preface covers:**
- **Audience:** Who this book is for (skills assumed, role, experience level)
- **Scope:** What topics are covered and, just as importantly, what is NOT
- **How to read:** Reading order recommendation, prerequisites, how to use the index and appendix
- **Value proposition:** Why this material matters and what the reader will take away

**The Preface must NEVER contain:**
- Any mention of web scraping, crawling, or PDF generation
- Any description of how the book was assembled ("We gathered pages from...", "The content was organized by...")
- Any reference to the source website as a website ("scraped from refactoring.guru")
- Any tool names, script names, or process descriptions

Save as `crawl_output/pages/0000_preface.md`. Add to `_index.json` with `"suppress": false`, `"chapter": "Preface"`, `"mece_order": 0`.

### 10. Book review (mandatory — before generating any PDF)

Run through the full checklist in `references/book-review-checklist.md` before calling `build_pdf.py`.

This review catches:
- Meta-commentary about the scraping process anywhere in the book
- Noise that slipped through (CTAs, legal fragments, navigation text)
- Weak opening chapter (SEO content as chapter 1)
- Image quality issues (broken refs, inappropriate images)
- Index quality (too noisy, too sparse)
- Preface quality (does it read as a real preface?)

Fix all issues found. This is faster than discovering problems in the rendered PDF.

### 11. Build the PDF

**Step 11a — Inspect the HTML output first:**

```bash
python scripts/build_pdf.py \
  --sitemap crawl_output/sitemap.json \
  --pages-dir crawl_output/pages/ \
  --template templates/book.html \
  --css assets/book.css \
  --output book.pdf \
  --title "Site Title" \
  --toc-max-depth 3 \
  --toc-max-entries 300 \
  --no-auto-preface \
  --html-only
```

Open the `.html` file and check:
- No blank pages between chapters
- No raw URLs in body text
- No meta-commentary ("This book was generated...", "Pages were deduplicated...")
- Opening chapter is real content, not an SEO landing page
- Images display correctly and are relevant
- "See also:" cross-references in appendix are correct
- Index is curated and useful

**Step 11b — Build the PDF:**

```bash
python scripts/build_pdf.py \
  --sitemap crawl_output/sitemap.json \
  --pages-dir crawl_output/pages/ \
  --template templates/book.html \
  --css assets/book.css \
  --output book.pdf \
  --title "Site Title" \
  --toc-max-depth 3 \
  --toc-max-entries 300 \
  --no-auto-preface \
  --running-header "Book Title" \
  --target-pages 100
```

Always pass `--no-auto-preface`. The auto-preface contains meta-commentary about how the book was assembled and must never appear in a final book.

### 12. Deliver results

Report to the user:
- Absolute path to the PDF
- Total pages scraped / skipped / errored
- PDF page count and file size
- Number of pages deduplicated, suppressed, or moved to appendix
- Number of images included (if images were requested)

---

## Comprehensive exclusion patterns

Apply these to both `crawl.py --exclude` and `scrape.py --exclude`:

```
# Legal / compliance / account
(privacy|terms|terms-of-service|terms-of-use|legal|imprint|disclaimer|gdpr|cookies|cookie-policy)
(about|about-us|about-me)
(login|logout|signin|signup|sign-in|sign-up|register|account|profile|dashboard)
(cart|basket|wishlist)

# E-commerce / sales
(sale|pricing|buy|checkout|gift|amazon|refund|money-back|guarantee|payment)

# Community / support noise
(forum|community|vote|userecho|testimonial|review|customer|comment|faq|support)

# Author personal / social
(facebook|twitter|instagram|newsletter|sendy|subscribe)

# Language/regional stubs (keep only primary language)
/(zh|ja|ko|pl|de|fr|es|pt|ru)/
```

See `references/content-exclusions.md` for complete patterns with examples.

---

## Index curation

The auto-generated index collects every H2/H3 heading from all pages. On a large site, this produces hundreds of entries, many of which are not useful to a reader.

**Evaluate the index before shipping:**
- If the index has > 300 entries, it is likely too noisy — pass `--no-index` to `build_pdf.py`
- If it has 50–300 entries, scan through them: remove generic terms like "Example", "Overview", "Introduction", "Summary"
- A good index has proper nouns, pattern names, technique names, and concept terms — not generic section labels

---

## Error handling

| Problem | Action |
|---|---|
| SSL certificate error | Retry with `--no-verify-ssl` flag |
| Rate limiting (429) | Script applies automatic back-off; increase `--delay` if needed |
| JavaScript-rendered pages | See `references/js-rendering.md` for Playwright fallback |
| WeasyPrint font issues | See `references/pdf-backends.md`; for CJK text install Noto fonts |
| CJK characters rendering as boxes | Install `fonts-noto-cjk` (`apt-get install fonts-noto-cjk`) |
| Blank pages in PDF | Double page-break: remove `<div class="page-break"></div>` between `.chapter` sections |
| H1 printed twice | Pass `--deduplicate-h1` to `scrape.py` (on by default) |
| [code] artifacts in output | Run `postprocess.py` — it converts these to proper fenced code blocks |
| Near-blank pages in PDF | Run `postprocess.py --min-content-words 150` |
| Raw URLs in body text | Run `postprocess.py --url-to-footnotes` |
| Noisy index | Pass `--no-index` or `--max-index-entries 150` |
| Broken image paths in PDF | Run `fetch_images.py` to download images and rewrite paths; see `references/image-handling.md` |
| Image too large / breaks layout | Set max-width in CSS; `fetch_images.py` skips images > 5 MB by default |
| Meta-commentary in preface | Rewrite the preface using `templates/preface.md` — never mention scraping or tools |

---

## Parameters reference

See `references/parameters.md` for the full flag reference for all scripts.

## PDF styling

Default styles are in `assets/book.css`. To customize:
- Edit `assets/book.css` directly, or
- Pass `--css path/to/custom.css` to `build_pdf.py`

See `templates/book.html` for the HTML structure the CSS targets.

## Agent instructions

- `agents/crawler-agent.md` — guidance for spawning a subagent to handle large crawls
- `agents/scraper-agent.md` — guidance for a subagent that scrapes and filters content
- `agents/formatter-agent.md` — guidance for a subagent that post-processes and MECE-organizes scraped Markdown

## Additional references

- `references/book-types.md` — five book types with structure and chapter-order recommendations
- `references/book-writing-guide.md` — principles of quality book writing applied to website-to-book
- `references/book-review-checklist.md` — mandatory pre-PDF quality review checklist
- `references/image-handling.md` — image selection, filtering, and embedding guide
- `references/crawling-guide.md` — crawl scope control, authentication, sitemap XML
- `references/content-exclusions.md` — URL and content patterns to exclude by site type
- `references/js-rendering.md` — Playwright/Selenium fallback for JS-rendered sites
- `references/pdf-backends.md` — WeasyPrint vs. pdfkit, font installation
- `references/parameters.md` — full flag reference for all scripts

## Templates

- `templates/book-plan.md` — fill out before starting any crawl
- `templates/preface.md` — author-voice preface template (no meta-commentary)
- `templates/book.html` — HTML structure for PDF rendering
- `templates/chapter.md` — legacy per-chapter format reference
