# Script Parameters Reference

Full flag reference for all three pipeline scripts.

---

## crawl.py

| Flag | Type | Default | Description |
|---|---|---|---|
| `--url` | str | *(required)* | Root URL to start crawling from |
| `--max-depth` | int | `5` | Maximum link-hop depth from root |
| `--max-pages` | int | `500` | Maximum pages to crawl before stopping |
| `--include` | regex | *(none)* | Only crawl URLs matching this pattern |
| `--exclude` | regex | *(none)* | Skip URLs matching this pattern |
| `--delay` | float | `0.2` | Seconds to wait between requests |
| `--no-verify-ssl` | flag | `false` | Disable SSL certificate verification |
| `--no-robots` | flag | `false` | Ignore robots.txt restrictions |
| `--output` | path | `sitemap.json` | Output JSON file path |

### sitemap.json output structure

```json
{
  "root_url": "https://example.com",
  "total_pages": 42,
  "pages": [
    {
      "url": "https://example.com/page",
      "original_url": "https://example.com/page",
      "title": "Page Title",
      "depth": 1,
      "parent": "https://example.com"
    }
  ]
}
```

---

## scrape.py

| Flag | Type | Default | Description |
|---|---|---|---|
| `--sitemap` | path | *(required)* | Path to `sitemap.json` from crawl.py |
| `--output` | path | `pages` | Output directory for `.md` files |
| `--main-selector` | CSS selector | *(auto)* | Force a specific content container |
| `--delay` | float | `0.3` | Seconds between requests |
| `--no-verify-ssl` | flag | `false` | Disable SSL certificate verification |
| `--keep-external-links` | flag | `false` | Keep external link URLs (default: strip URLs, keep text) |
| `--min-words` | int | `150` | Skip pages with fewer words than this threshold |

### Content quality behavior (always on)

- **HTML comments stripped**: `<!-- ... -->` nodes are removed before text extraction
- **Comment sections removed**: Disqus, WordPress comments, utterances, giscus blocks are stripped along with other noise elements
- **External links converted to text**: `[link text](https://external.com)` → `link text` — the URL is dropped to avoid noisy PDF footnotes. Internal (same-domain) links are kept intact.
- **Sparse pages skipped**: pages with fewer than `--min-words` words are excluded and recorded as errors in `_index.json`

### Auto content detection

When `--main-selector` is not given, scrape.py tries these selectors in order,
picking the first that contains > 200 characters of text:

```
main, article, [role="main"], .content, .main-content, .post-content,
.entry-content, .page-content, .docs-content, .markdown-body,
#content, #main, #main-content
```

If none match, the entire `<body>` is used.

### _index.json structure

```json
[
  {
    "index": 0,
    "url": "https://example.com",
    "title": "Home",
    "filename": "0000_example_com.md",
    "depth": 0,
    "word_count": 423,
    "error": null
  }
]
```

---

## build_pdf.py

| Flag | Type | Default | Description |
|---|---|---|---|
| `--sitemap` | path | *(required)* | Path to `sitemap.json` |
| `--pages-dir` | path | *(required)* | Directory containing scraped `.md` files |
| `--template` | path | `templates/book.html` | HTML template file |
| `--css` | path | `assets/book.css` | CSS stylesheet |
| `--output` | path | `book.pdf` | Output PDF path |
| `--title` | str | *(from sitemap root_url)* | Book title shown on title page |
| `--backend` | choice | `auto` | PDF backend: `weasyprint`, `pdfkit`, or `auto` |
| `--html-only` | flag | `false` | Stop after generating HTML; skip PDF render |
| `--target-pages` | int | `0` (off) | Approximate target PDF page count; trims content to fit |
| `--toc-max-depth` | int | `1` | Maximum chapter depth shown in table of contents |
| `--toc-max-entries` | int | `30` | Maximum number of TOC entries |

### Table of contents behavior

The TOC is intentionally kept short: only pages at depth ≤ `--toc-max-depth`
(default: 1) are listed, with a hard cap of `--toc-max-entries` (default: 30).
This gives readers a navigable overview without listing every sub-page.

### Target pages behavior

When `--target-pages N` is set, the script estimates ~500 words per PDF page
and drops the lowest-value (shortest) pages until the word budget is met.
This is a heuristic — actual PDF page count also depends on images, tables,
and code blocks.

---

## run_all.py (convenience wrapper)

Combines all three scripts with a single command. Accepts all flags from
crawl.py and scrape.py plus:

| Flag | Type | Default | Description |
|---|---|---|---|
| `--url` | str | *(required)* | Root URL |
| `--output` | path | `book.pdf` | Final PDF output path |
| `--target-pages` | int | `0` | Target PDF page count; sets `--max-pages = target*3` for crawl |
| `--max-pages` | int | `0` | Hard crawl page cap (overrides target-pages derivation if set) |
| `--work-dir` | path | `write-book-output` | Directory for intermediate files |
| `--title` | str | *(auto)* | Book title |
| `--template` | path | `templates/book.html` | HTML template |
| `--css` | path | `assets/book.css` | CSS |
| `--backend` | choice | `auto` | PDF backend |
| `--keep-external-links` | flag | `false` | Keep external link URLs in scraped output |
| `--min-words` | int | `150` | Minimum word count per scraped page |
| `--toc-max-depth` | int | `1` | TOC depth cap |
| `--toc-max-entries` | int | `30` | TOC entry cap |
