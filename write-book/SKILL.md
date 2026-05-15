---
name: write-book
description: Crawl a website, scrape all discoverable pages, preserve text formatting, and compile the content into a downloadable PDF book. Use this skill whenever the user wants to turn a website, documentation site, wiki, or blog into a PDF book or eBook. Trigger when the user mentions scraping a site to PDF, converting website content to a book, archiving a site as a document, or asks to "make a book from" a URL. Also trigger for requests like "download site as PDF", "scrape and export to book", or "compile website docs into PDF". Use this skill proactively any time a user shares a URL and wants something readable or downloadable from it.
author: vprindyn@gmail.com
version: "2.0"
compatibility: Requires Python 3.8+, pip packages listed in scripts/requirements.txt (requests, beautifulsoup4, lxml, html2text, weasyprint or pdfkit, tqdm, Markdown, Pygments)
---

# write-book

Crawl a website from a root URL, discover every reachable page on the same domain, scrape textual content while preserving formatting, clean out site chrome and non-book content, organize into a clean reader-first structure, and compile everything into a well-formatted PDF book with a full table of contents.

---

## Core principles (read before starting)

**DO:**
- Crawl once to list URLs, then grep for junk before scraping
- Inspect 5 random scraped `.md` files before building the PDF
- Exclude `privacy|terms|legal|gdpr|cookies|imprint|about|sale|cart|signup|login` in every crawl
- Strip site CTAs/upsells with a site-specific regex (e.g. "Tired of reading?")
- Drop external link URLs entirely — keep only the link text
- Remove navigation/widget blocks (e.g. "In Other Languages" tab rows) via CSS selectors
- Write your own 1-page Preface that states audience, scope, and how to read the book
- Add cross-references from appendix code examples back to their main chapter
- Decide upfront whether you're writing one book or two — give Parts clear framing

**DON'T:**
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

---

## Workflow overview

1. **Decide the book structure** — one book or two? Parts? Framing?
2. **Gather requirements** — ask for the root URL, page count, and filters.
3. **Crawl and inspect URLs** — crawl, print the URL list, grep for junk, re-crawl if needed.
4. **Scrape content** — run `scripts/scrape.py` with comprehensive exclusion patterns.
5. **Inspect a sample** — run `scripts/inspect_sample.py` to review 5 random pages before continuing.
6. **Post-process** — run `scripts/postprocess.py` to deduplicate, strip remaining noise, and flag code-heavy pages.
7. **Organize with MECE** — run the formatter agent to group pages into chapters in reader-first order; set `xref_chapter` on appendix pages for cross-references.
8. **Write a Preface** — write one original page covering audience, scope, and how to read the book. Save it as `crawl_output/pages/0000_preface.md` and mark it first in `_index.json`.
9. **Build the PDF** — run `scripts/build_pdf.py`. Inspect the HTML output for noise before rendering to PDF.
10. **Deliver** — report path, page count, and file size.

---

## Step-by-step instructions

### 1. Decide the book structure

Before asking for a URL, decide (or ask the user):
- **One book or two?** A site with "Refactoring" AND "Design Patterns" as peer top-level sections may warrant two books, each with a clear scope. If you try to fit both into one book, give each a named Part (e.g. `# Part I: Design Patterns` and `# Part II: Refactoring`). Don't blend them with no framing.
- **SEO landing pages:** The root `/`, `/refactoring`, and `/design-patterns` pages on many sites are marketing pages that overlap 80%. Plan to suppress them as duplicates.
- **Audience:** Who is this book for? (senior engineers? learners? a specific team?) This shapes the Preface and which content to prioritize.

### 2. Gather requirements

Ask the user for these inputs **before** starting any crawl:

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

If WeasyPrint fails to install (common on headless servers), fall back to `pdfkit` + `wkhtmltopdf`. See `references/pdf-backends.md` for details.

### 4. Crawl and inspect URLs

**Step 4a — Crawl:**

Use the comprehensive exclude pattern that covers both e-commerce AND legal/account noise:

```bash
python scripts/crawl.py \
  --url "https://example.com" \
  --max-depth 5 \
  --max-pages 300 \
  --exclude "(privacy|terms|legal|gdpr|cookies|imprint|about|sale|cart|signup|login|pricing|buy|checkout|testimonials|reviews|faq|payment|refund|forum|community|vote|userecho|newsletter|subscribe|register|account|zh|ja|ko|pl|de|fr|es|pt|ru)" \
  --output crawl_output/sitemap.json
```

**Step 4b — Inspect the URL list before scraping:**

Print the crawled URLs and look for junk that slipped through:

```bash
python -c "
import json
data = json.loads(open('crawl_output/sitemap.json').read())
for p in data['pages']:
    print(p['url'])
" | grep -iE "(privacy|terms|legal|gdpr|about|cookies|imprint|login|signup|sale|cart|faq|testimonial|review|forum|pricing|refund|guarantee|newsletter|subscribe|account|register)"
```

If the grep returns hits, tighten `--exclude` and re-crawl before scraping. Scraping first wastes time and introduces noise.

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

See `references/crawling-guide.md` for scope-control strategies and `references/content-exclusions.md` for recommended exclude patterns by site type.

### 5. Scrape content

```bash
python scripts/scrape.py \
  --sitemap crawl_output/sitemap.json \
  --output crawl_output/pages/ \
  --format markdown \
  --exclude "(privacy|terms|legal|gdpr|cookies|imprint|about|sale|cart|signup|login|pricing|buy|checkout|testimonials?|reviews?|faq|payment|refund|forum|userecho)" \
  --min-words 200
```

The scraper automatically:
- **Strips HTML comments**, comment sections (Disqus, WordPress, utterances), ads, navigation, sidebars
- **Removes noise elements**: vote widgets, follow buttons, social banners, "In Other Languages" tab rows, multi-language sales notices, UserEcho forum widgets, testimonial blocks, pricing tables
- **Strips site CTAs/upsells** via regex: "Tired of reading?", "Get the book now", "Buy today", etc.
- **Strips site chrome from Markdown output**: [code]/[/code] artifacts, video-fallback text, empty widget labels ("Complexity:", "Popularity:"), vote widget text, orphan navigation file-tree lines
- **Deduplicates the H1** — the chapter title is written once; the matching H1 is stripped from the body
- **Drops external link URLs** — replaces `[text](https://external.com)` with just `text`
- **Skips sparse pages** — pages with fewer than `--min-words` words are excluded
- **Skips legal/account pages** — privacy, terms, legal, gdpr, cookies, imprint pages are excluded by default

Each page is saved as a Markdown file in `crawl_output/pages/`.

### 6. Inspect a sample before continuing

**Before running post-process or building the PDF, always inspect 5 random pages:**

```bash
python scripts/inspect_sample.py \
  --pages-dir crawl_output/pages/ \
  --n 5
```

Look for:
- Raw `https://` URLs still in body text (should be footnotes or stripped)
- Site chrome that slipped through (navigation text, "Was this page helpful?", cookie notices)
- CTA/upsell fragments ("Buy now", "Get the book", "Tired of reading?")
- "In Other Languages" tab lists that are just link lists with no prose
- Pages that are 90% code with no explanation (candidates for appendix)
- SEO landing pages masquerading as content (lots of bullet lists, no depth)

If you find noise in the sample, fix the scraper patterns and re-scrape before proceeding. This is faster than rebuilding the PDF to discover the same problems.

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

The post-processor:
- **Deduplicates near-identical pages** (> 70% text overlap) — keeps the longest version
- **Collapses per-language stub catalogs** — merges 5+ language-variant pages with the same link lists
- **Flags code-heavy pages** — pages where > 60% of word count is inside code blocks are tagged `code_heavy: true` for appendix placement
- **Converts bare URLs to footnotes** — inline `http://...` URLs become `[^N]` references
- **Suppresses near-blank pages** — pages below `--min-content-words` are marked `suppress: true`

### 8. Organize content (MECE structure + cross-references)

Run the formatter agent (`agents/formatter-agent.md`) to:
1. Reorganize content into a MECE structure ordered for a reader
2. Assign every page to a chapter (`chapter` field in `_index.json`)
3. Set `mece_order` position within each chapter
4. For code-heavy (appendix) pages, set `xref_chapter` to the name of the main chapter this code belongs to — the PDF builder uses this to add a "See also: [chapter]" cross-reference

For a design-pattern or programming reference site, the recommended chapter order is:
1. Preface (user-written — see Step 9)
2. Foundational Principles (SOLID, OOP concepts, etc.)
3. Catalog — Creational Patterns
4. Catalog — Structural Patterns
5. Catalog — Behavioral Patterns
6. Code Smells / Anti-patterns
7. Refactoring Techniques
8. Appendix (code listings, extended language examples)

If the site has two peer topic areas (e.g. Design Patterns AND Refactoring), consider two separate books rather than one large book with two halves.

### 9. Write the Preface

Write a single original page (not scraped) that covers:
- **Audience**: who this book is for (e.g. "mid-to-senior software engineers familiar with OOP")
- **Scope**: what topics are covered and, just as importantly, what is NOT covered
- **How to read**: reading order recommendation (cover-to-cover vs. reference lookup), prerequisites, how to use the appendix

Save it as `crawl_output/pages/0000_preface.md`. Add it to `_index.json` with `"suppress": false`, `"chapter": "Preface"`, and `"mece_order": 0`.

**Do not use the auto-generated preface from `build_pdf.py`.** Pass `--no-auto-preface` to suppress it. One preface, written by you, is always better than a generic auto-generated one.

### 10. Build the PDF

**Step 10a — Inspect the HTML output first:**

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

Open the `.html` file and check for:
- Blank pages between chapters (caused by double page-break — fix in the CSS or remove `.page-break` divs)
- Raw URLs still in body text
- SEO landing pages as the first "real" chapters
- Appendix pages missing "See also:" cross-references back to their main chapter
- Index with > 300 entries that is mostly heading noise (pass `--no-index` if so)

**Step 10b — Build the PDF:**

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

### 11. Deliver results

Report to the user:
- Absolute path to the PDF
- Total pages scraped / skipped / errored
- PDF page count and file size
- Number of pages deduplicated, suppressed, or moved to appendix

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

The auto-generated index collects every H2/H3 heading from all pages. On a large site, this produces hundreds of entries, many of which are not useful to a reader (e.g. "Example", "Usage", "See also" repeated across 50 chapters).

**Evaluate the index before shipping:**
- If the index has > 300 entries, it is likely too noisy to be useful — pass `--no-index` to `build_pdf.py`
- If it has 50–300 entries, scan through them: remove generic terms like "Example", "Overview", "Introduction", "Summary" by passing `--index-exclude-terms "Example,Overview,Introduction,Summary"`
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
| Blank pages in PDF | Double page-break: remove `<div class="page-break"></div>` between `.chapter` sections — the CSS `page-break-before: always` already handles breaks |
| H1 printed twice | Pass `--deduplicate-h1` to `scrape.py` (on by default) |
| [code] artifacts in output | Run `postprocess.py` — it converts these to proper fenced code blocks |
| Near-blank pages in PDF | Run `postprocess.py --min-content-words 150` to flag and suppress them |
| Raw URLs in body text | Run `postprocess.py --url-to-footnotes`; also verify `scrape.py` dropped external link URLs |
| Noisy index | Pass `--no-index` or `--toc-max-entries 300 --no-index` and rely on the TOC for navigation |

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

- `references/crawling-guide.md` — crawl scope control, authentication, sitemap XML
- `references/content-exclusions.md` — URL and content patterns to exclude by site type
- `references/js-rendering.md` — Playwright/Selenium fallback for JS-rendered sites
- `references/pdf-backends.md` — WeasyPrint vs. pdfkit, font installation
