---
name: write-book
description: Crawl a website, scrape all discoverable pages, preserve text formatting, and compile the content into a downloadable PDF book. Use this skill whenever the user wants to turn a website, documentation site, wiki, or blog into a PDF book or eBook. Trigger when the user mentions scraping a site to PDF, converting website content to a book, archiving a site as a document, or asks to "make a book from" a URL. Also trigger for requests like "download site as PDF", "scrape and export to book", or "compile website docs into PDF".
author: vprindyn@gmail.com
version: "1.1.0"
compatibility: Requires Python 3.8+, pip packages listed in scripts/requirements.txt (requests, beautifulsoup4, lxml, html2text, weasyprint or pdfkit, tqdm)
---

# write-book

Crawl a website from a root URL, discover every reachable page on the same domain, scrape textual content while preserving formatting, organize it into a clean MECE structure, and compile everything into a well-structured PDF book.

## Workflow overview

1. **Gather requirements** — ask the user for the root URL, desired page count, and any filters.
2. **Crawl the site** — run `scripts/crawl.py` to map all reachable pages.
3. **Scrape content** — run `scripts/scrape.py` to extract clean text; strips HTML comments, comment sections, and external links automatically.
4. **Organize with MECE** — run the formatter agent to group pages into mutually exclusive, collectively exhaustive chapters.
5. **Assemble book** — run `scripts/build_pdf.py` to merge content using the HTML template and render a PDF with a concise table of contents.
6. **Deliver the PDF** — report the output path and crawl statistics.

---

## Step-by-step instructions

### 1. Gather requirements (ask before doing anything else)

Ask the user for these inputs **before** starting any crawl:

| Input | Required | Default | Notes |
|---|---|---|---|
| **Root URL** | Yes | — | Starting page, e.g. `https://docs.example.com` |
| **Target page count** | Yes | — | Approximate number of PDF pages the user wants (e.g. 50, 100, 200). Use this to size the crawl: set `--max-pages` ≈ target × 3 as a starting point. |
| **Output filename** | No | `book.pdf` | — |
| **Max depth** | No | `5` | Link-hops from root |
| **URL filter** | No | none | Regex pattern pages must match |
| **Exclude pattern** | No | none | Regex for URLs to skip (login, tag, search pages, etc.) |

Confirm with the user before starting a crawl on large sites (> 200 pages estimated).

**Important:** Do not crawl before all required inputs are collected and confirmed.

### 2. Install dependencies

```bash
pip install -r scripts/requirements.txt
```

If WeasyPrint fails to install (common on headless servers), fall back to `pdfkit` + `wkhtmltopdf`. See `references/pdf-backends.md` for details.

### 3. Crawl the site

Use `--max-pages` derived from the user's target page count (target × 3):

```bash
python scripts/crawl.py \
  --url "https://example.com" \
  --max-depth 5 \
  --max-pages 300 \
  --output crawl_output/sitemap.json
```

This produces `sitemap.json` — an ordered list of page URLs with metadata (title, depth, parent URL).

### 4. Scrape content

```bash
python scripts/scrape.py \
  --sitemap crawl_output/sitemap.json \
  --output crawl_output/pages/ \
  --format markdown
```

The scraper automatically:
- **Strips HTML comments** (`<!-- ... -->`) and code comments embedded in content
- **Removes comment sections** (Disqus, WordPress comments, utterances, giscus)
- **Drops external links** — replaces `[text](https://external.com)` with just `text`; keeps internal same-domain links intact
- **Skips sparse pages** — pages with fewer than 150 words are excluded as low-value
- Preserves headings, paragraphs, bold/italic, code blocks, tables, and lists

Each page is saved as a Markdown file in `crawl_output/pages/`.

### 5. Organize content (MECE structure)

Before building the PDF, run the formatter agent (`agents/formatter-agent.md`) to reorganize content into a MECE structure:

- **Mutually Exclusive**: each topic appears in exactly one chapter — no duplicate or overlapping sections
- **Collectively Exhaustive**: all important content is covered; pages that duplicate an existing chapter are merged, not repeated

The formatter groups pages into 5–10 cohesive top-level chapters and reorders pages within each chapter for logical flow.

### 6. Build the PDF

```bash
python scripts/build_pdf.py \
  --sitemap crawl_output/sitemap.json \
  --pages-dir crawl_output/pages/ \
  --template templates/book.html \
  --css assets/book.css \
  --output book.pdf \
  --title "Site Title" \
  --target-pages 100
```

The script:
1. Reads pages in MECE chapter order.
2. Renders each Markdown page to HTML using the book template.
3. Inserts a title page, a **concise table of contents** (top-level chapters only, max 30 entries), chapter breaks, and page numbers.
4. If `--target-pages` is set, trims the lowest-value pages to approach the target count.
5. Renders the full HTML document to PDF via WeasyPrint (or pdfkit fallback).

### 7. Deliver results

Report to the user:
- Absolute path to the PDF
- Total pages scraped / skipped / errored
- PDF page count and file size

---

## Error handling

| Problem | Action |
|---|---|
| SSL certificate error | Retry with `--no-verify-ssl` flag |
| Rate limiting (429) | Script applies automatic back-off; increase `--delay` if needed |
| JavaScript-rendered pages | See `references/js-rendering.md` for Playwright fallback |
| WeasyPrint font issues | See `references/pdf-backends.md` |
| Circular redirects | Crawler deduplicates by normalized URL; redirects followed once |
| Very large sites (1000+ pages) | Use `--max-pages` to cap; consider splitting by domain section |
| TOC too long | Default cap is 30 entries at depth ≤ 1; increase with `--toc-max-entries` |

---

## Parameters reference

See `references/parameters.md` for the full flag reference for all three scripts.

## PDF styling

Default styles are in `assets/book.css`. To customize:
- Edit `assets/book.css` directly, or
- Pass `--css path/to/custom.css` to `build_pdf.py`

See `templates/book.html` for the HTML structure the CSS targets.

## Agent instructions

- `agents/crawler-agent.md` — guidance for spawning a subagent to handle large crawls
- `agents/scraper-agent.md` — guidance for a subagent that scrapes and filters content
- `agents/formatter-agent.md` — guidance for a subagent that post-processes and MECE-organizes scraped Markdown
