---
name: write-book
description: Crawl a website, scrape all discoverable pages, preserve text formatting, and compile the content into a downloadable PDF book. Use this skill whenever the user wants to turn a website, documentation site, wiki, or blog into a PDF book or eBook. Trigger when the user mentions scraping a site to PDF, converting website content to a book, archiving a site as a document, or asks to "make a book from" a URL. Also trigger for requests like "download site as PDF", "scrape and export to book", or "compile website docs into PDF". Use this skill proactively any time a user shares a URL and wants something readable or downloadable from it.
author: vprindyn@gmail.com
version: "1.2.0"
compatibility: Requires Python 3.8+, pip packages listed in scripts/requirements.txt (requests, beautifulsoup4, lxml, html2text, weasyprint or pdfkit, tqdm, Markdown, Pygments)
---

# write-book

Crawl a website from a root URL, discover every reachable page on the same domain, scrape textual content while preserving formatting, clean out site chrome and non-book content, organize into a clean reader-first structure, and compile everything into a well-formatted PDF book with a full table of contents and index.

## Workflow overview

1. **Gather requirements** — ask the user for the root URL, desired page count, and any filters.
2. **Crawl the site** — run `scripts/crawl.py` to map all reachable pages.
3. **Scrape content** — run `scripts/scrape.py` to extract clean text, excluding e-commerce, testimonial, forum, and FAQ pages automatically.
4. **Post-process** — run `scripts/postprocess.py` to strip remaining site chrome, fix [code] artifacts, deduplicate headings, convert URLs to footnotes, and flag near-blank pages.
5. **Organize with MECE** — run the formatter agent to group pages into mutually exclusive, collectively exhaustive chapters in reader-first order.
6. **Assemble book** — run `scripts/build_pdf.py` to merge content using the HTML template, generate a full table of contents, render an alphabetical index, and produce a PDF.
7. **Deliver the PDF** — report the output path and crawl statistics.

---

## Step-by-step instructions

### 1. Gather requirements (ask before doing anything else)

Ask the user for these inputs **before** starting any crawl:

| Input | Required | Default | Notes |
|---|---|---|---|
| **Root URL** | Yes | — | Starting page, e.g. `https://docs.example.com` |
| **Target page count** | Yes | — | Approximate number of PDF pages wanted (e.g. 50, 100, 200). Use `--max-pages` ≈ target × 3. |
| **Output filename** | No | `book.pdf` | — |
| **Max depth** | No | `5` | Link-hops from root |
| **URL filter** | No | none | Regex pattern pages must match |
| **Exclude pattern** | No | none | Regex for URLs to skip (login, tag, search, pricing, faq, etc.) |
| **Book title** | No | auto | Shown on title page and running headers |
| **Content selector** | No | auto | CSS selector for main content, e.g. `.article-body` |

Confirm before starting a crawl on large sites (> 200 pages estimated).

**Important:** Do not crawl before all required inputs are collected and confirmed.

### 2. Install dependencies

```bash
pip install -r scripts/requirements.txt
```

If WeasyPrint fails to install (common on headless servers), fall back to `pdfkit` + `wkhtmltopdf`. See `references/pdf-backends.md` for details.

### 3. Crawl the site

Use `--max-pages` derived from the user's target page count (target × 3). Exclude non-book URLs at this stage to avoid scraping pages that will be discarded later:

```bash
python scripts/crawl.py \
  --url "https://example.com" \
  --max-depth 5 \
  --max-pages 300 \
  --exclude "(sale|pricing|buy|checkout|testimonials|reviews|faq|payment|refund|forum|community|vote|userecho)" \
  --output crawl_output/sitemap.json
```

This produces `sitemap.json` — an ordered list of page URLs with metadata (title, depth, parent URL).

See `references/crawling-guide.md` for scope-control strategies and `references/content-exclusions.md` for recommended exclude patterns by site type.

### 4. Scrape content

```bash
python scripts/scrape.py \
  --sitemap crawl_output/sitemap.json \
  --output crawl_output/pages/ \
  --format markdown \
  --exclude "(sale|pricing|buy|checkout|testimonials?|reviews?|faq|payment|refund|forum|userecho)" \
  --min-words 200
```

The scraper automatically:
- **Strips HTML comments**, comment sections (Disqus, WordPress, utterances), ads, navigation, sidebars
- **Removes noise elements**: vote widgets, follow buttons, social banners, multi-language sales notices, UserEcho forum widgets, testimonial blocks, pricing tables
- **Strips site chrome from Markdown output**: [code]/[/code] artifacts, video-fallback text ("Your browser does not support HTML video"), bare (/sendy/form) link artifacts, empty widget labels ("Complexity:", "Popularity:" with no value, "Vote __ 0 __ 0 Undo __ Follow"), orphan navigation file-tree lines
- **Deduplicates the H1** — the chapter title is written once in the frontmatter; the matching H1 is stripped from the scraped body so it does not appear twice
- **Drops external link URLs** — replaces `[text](https://external.com)` with just `text`; internal same-domain links are kept
- **Skips sparse pages** — pages with fewer than `--min-words` words are excluded

Each page is saved as a Markdown file in `crawl_output/pages/`.

### 5. Post-process scraped content

Run the post-processor to apply deeper cleanup that requires reading full file content:

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
- **Deduplicates near-identical pages** (> 70% text overlap) — keeps the longest version, marks others as merged in `_index.json`
- **Collapses per-language stub catalogs** — when the same 20+ pattern links appear across 5+ language-variant pages with no unique prose, merges them into one "Available in multiple languages" stub
- **Flags code-heavy pages** — pages where > 60% of word count is inside code blocks are tagged `code_heavy: true` in `_index.json` so the formatter agent can decide whether to move them to an appendix
- **Converts bare URLs to footnotes** — inline `http://...` URLs in text become `[^N]` references with a footnote block at page end
- **Suppresses near-blank pages** — pages with fewer than `--min-content-words` words after cleanup are marked `suppress: true` and excluded from the PDF build

### 6. Organize content (MECE structure)

Before building the PDF, run the formatter agent (`agents/formatter-agent.md`) to reorganize content into a MECE structure ordered for a reader, not a crawler.

For a typical design-pattern or programming reference site, the recommended chapter order is:
1. Preface / Introduction
2. Foundational Principles (SOLID, OOP concepts, etc.)
3. Catalog (Creational → Structural → Behavioral patterns)
4. Code Smells / Anti-patterns
5. Refactoring Techniques
6. Appendix (code listings, language examples)

The formatter groups pages into 5–10 cohesive chapters and reorders pages within each chapter for logical flow.

### 7. Build the PDF

```bash
python scripts/build_pdf.py \
  --sitemap crawl_output/sitemap.json \
  --pages-dir crawl_output/pages/ \
  --template templates/book.html \
  --css assets/book.css \
  --output book.pdf \
  --title "Site Title" \
  --toc-max-depth 3 \
  --toc-max-entries 500 \
  --generate-index \
  --running-header "Book Title" \
  --target-pages 100
```

The script:
1. Reads pages in MECE chapter order (from `_index.json` `mece_order` field).
2. Renders each Markdown page to HTML using the book template.
3. Inserts a title page, a **full table of contents** (all patterns, smells, and techniques, up to `--toc-max-entries`), chapter breaks, and page numbers.
4. Generates an **alphabetical index** from H2+ headings across all chapters.
5. Normalizes **running headers** to the value set by `--running-header` (or the chapter title set by `string-set` in CSS).
6. Suppresses pages marked `suppress: true` in `_index.json`.
7. If `--target-pages` is set, trims the lowest-value pages to approach the target count.
8. Renders the full HTML document to PDF via WeasyPrint (or pdfkit fallback).

### 8. Deliver results

Report to the user:
- Absolute path to the PDF
- Total pages scraped / skipped / errored
- PDF page count and file size
- Number of pages deduplicated, suppressed, or moved to appendix

---

## Common exclusion patterns

For sites that mix book content with e-commerce, community, and support content, add these to both `crawl.py --exclude` and `scrape.py --exclude`:

```
# E-commerce / sales
(sale|pricing|buy[-_]now|checkout|purchase|gift|amazon|guarantee|refund|money-back|payment)

# Community / support
(forum|community|vote|userecho|testimonial|review|customer|comment|faq|support)

# Author personal / social
(about-me|author|facebook|twitter|instagram|newsletter|sendy|subscribe)

# Language/regional stubs (keep only primary language)
/(zh|ja|ko|pl|de|fr|es|pt|ru)/
```

See `references/content-exclusions.md` for complete patterns with examples.

---

## Error handling

| Problem | Action |
|---|---|
| SSL certificate error | Retry with `--no-verify-ssl` flag |
| Rate limiting (429) | Script applies automatic back-off; increase `--delay` if needed |
| JavaScript-rendered pages | See `references/js-rendering.md` for Playwright fallback |
| WeasyPrint font issues | See `references/pdf-backends.md`; for CJK text install Noto fonts |
| CJK characters rendering as boxes | Install `fonts-noto-cjk` (`apt-get install fonts-noto-cjk`) and WeasyPrint will pick them up via Fontconfig |
| Circular redirects | Crawler deduplicates by normalized URL; redirects followed once |
| Very large sites (1000+ pages) | Use `--max-pages` to cap; consider splitting by domain section |
| TOC too long | Default cap is 500 entries at depth ≤ 3; adjust with `--toc-max-entries` |
| H1 printed twice | Pass `--deduplicate-h1` to `scrape.py` (on by default); or run `postprocess.py` |
| [code] artifacts in output | Run `postprocess.py` — it converts these to proper fenced code blocks |
| Near-blank pages in PDF | Run `postprocess.py --min-content-words 150` to flag and suppress them |

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
