---
name: write-book
description: Crawl a website, scrape all discoverable pages, preserve text formatting, and compile the content into a downloadable PDF book. Use this skill whenever the user wants to turn a website, documentation site, wiki, or blog into a PDF book or eBook. Trigger when the user mentions scraping a site to PDF, converting website content to a book, archiving a site as a document, or asks to "make a book from" a URL. Also trigger for requests like "download site as PDF", "scrape and export to book", or "compile website docs into PDF".
author: vprindyn@gmail.com
version: "1.0.0"
compatibility: Requires Python 3.8+, pip packages listed in scripts/requirements.txt (requests, beautifulsoup4, lxml, html2text, weasyprint or pdfkit, tqdm)
---

# write-book

Crawl a website from a root URL, discover every reachable page on the same domain, scrape textual content while preserving formatting, and compile everything into a well-structured PDF book.

## Workflow overview

1. **Receive input** — get a root URL from the user and optional parameters (depth limit, page limit, output filename, include/exclude URL patterns).
2. **Crawl the site** — run `scripts/crawl.py` to map all reachable pages.
3. **Scrape content** — run `scripts/scrape.py` to extract and clean text from each discovered page.
4. **Assemble book** — run `scripts/build_pdf.py` to merge content using the HTML template and render a PDF.
5. **Deliver the PDF** — report the output path and any crawl statistics.

---

## Step-by-step instructions

### 1. Validate input

Ask the user for:
- **Root URL** (required): the starting page, e.g. `https://docs.example.com`
- **Output filename** (optional, default: `book.pdf`)
- **Max depth** (optional, default: `5`): how many link-hops from root
- **Max pages** (optional, default: `500`): cap to avoid runaway crawls
- **URL filter** (optional): regex pattern pages must match to be included
- **Exclude pattern** (optional): regex pattern for URLs to skip (e.g. login, tag, search pages)

Confirm with the user before starting a crawl on large sites (> 200 pages estimated).

### 2. Install dependencies

```bash
pip install -r scripts/requirements.txt
```

If WeasyPrint fails to install (common on headless servers), fall back to `pdfkit` + `wkhtmltopdf`. See `references/pdf-backends.md` for details.

### 3. Crawl the site

```bash
python scripts/crawl.py \
  --url "https://example.com" \
  --max-depth 5 \
  --max-pages 500 \
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

Each page is saved as a Markdown file in `crawl_output/pages/`, preserving:
- Headings (h1–h6 → `#`–`######`)
- Paragraphs
- Bold / italic / code spans
- Ordered and unordered lists
- Blockquotes
- Code blocks (fenced)
- Tables

### 5. Build the PDF

```bash
python scripts/build_pdf.py \
  --sitemap crawl_output/sitemap.json \
  --pages-dir crawl_output/pages/ \
  --template templates/book.html \
  --css assets/book.css \
  --output book.pdf \
  --title "Site Title"
```

The script:
1. Reads pages in sitemap order (breadth-first by depth, then alphabetical within depth).
2. Renders each Markdown page to HTML using the book template.
3. Inserts a title page, auto-generated table of contents, chapter breaks, and page numbers.
4. Renders the full HTML document to PDF via WeasyPrint (or pdfkit fallback).

### 6. Deliver results

Report to the user:
- Absolute path to the PDF
- Total pages scraped / skipped / errored
- PDF page count
- File size

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
- `agents/formatter-agent.md` — guidance for a subagent that post-processes scraped Markdown
