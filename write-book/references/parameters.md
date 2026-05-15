# Script Parameters Reference

Full flag reference for all pipeline scripts.

---

## crawl.py

| Flag | Type | Default | Description |
|---|---|---|---|
| `--url` | str | *(required)* | Root URL to start crawling from |
| `--max-depth` | int | `5` | Maximum link-hop depth from root |
| `--max-pages` | int | `500` | Maximum pages to crawl before stopping |
| `--include` | regex | *(none)* | Only crawl URLs matching this pattern |
| `--exclude` | regex | *(none)* | Skip URLs matching this pattern (use same value as `scrape.py --exclude`) |
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
| `--exclude` | regex | *(none)* | Skip pages whose URL matches this pattern (stacks with built-in excludes) |
| `--no-builtin-excludes` | flag | `false` | Disable built-in e-commerce/forum/testimonial URL exclusions |

### Content quality behavior (always on)

- **HTML comments stripped**: `<!-- ... -->` nodes removed before text extraction
- **Noise elements removed**: `nav`, `header`, `footer`, vote widgets, UserEcho widgets, testimonial blocks, pricing tables, author-bio sections, multi-language banners
- **[code] artifacts fixed**: `[code]`/`[/code]` tags converted to proper fenced code blocks
- **Video fallback removed**: "Your browser does not support HTML video." lines stripped
- **Empty widget labels removed**: "Complexity:", "Popularity:" lines with no value stripped
- **H1 deduplicated**: the first `# Heading` in the scraped body is removed if it matches the page title (title is written once in frontmatter)
- **External links converted to text**: `[link text](https://external.com)` → `link text`
- **Sparse pages skipped**: pages with fewer than `--min-words` words are excluded

### Built-in URL exclusions (always on unless `--no-builtin-excludes`)

Pages at URLs matching these patterns are skipped automatically:

```
/(sale|spring-sale|discount|promo|coupon)
/(pricing|price|buy|purchase|checkout|order|gift|amazon)
/(refund|money-back|guarantee)
/(testimonial|review|customer)
/(faq|payment|payment-method)
/(forum|community|vote|userecho)
/(newsletter|subscribe|sendy)
/(login|logout|signup|register|account)
/(search|tag|category|author)/
```

See `references/content-exclusions.md` for complete patterns and examples.

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

## postprocess.py

| Flag | Type | Default | Description |
|---|---|---|---|
| `--pages-dir` | path | *(required)* | Directory with scraped `.md` files and `_index.json` |
| `--deduplicate` | flag | `false` | Suppress near-duplicate pages (≥ 70% text overlap) |
| `--deduplicate-threshold` | float | `0.70` | Similarity threshold for deduplication (0–1) |
| `--collapse-language-stubs` | flag | `false` | Merge per-language catalog stubs into one representative page |
| `--min-language-stubs` | int | `3` | Minimum number of language variants before collapsing |
| `--move-code-appendix` | flag | `false` | Tag code-heavy pages (≥ 60% code blocks) with `code_heavy: true` |
| `--code-heavy-threshold` | float | `0.60` | Code-block fraction to consider a page code-heavy |
| `--url-to-footnotes` | flag | `false` | Convert bare inline `http://` URLs to Markdown footnotes |
| `--min-content-words` | int | `0` | Suppress pages with fewer words (0 = disabled) |

### _index.json fields added by postprocess.py

| Field | Type | Meaning |
|---|---|---|
| `suppress` | bool | `true` = exclude this page from the PDF |
| `suppress_reason` | str | Why the page was suppressed |
| `merged_into` | str | Filename of the page this was merged into |
| `code_heavy` | bool | `true` = page is mostly code; suggest appendix placement |

---

## build_pdf.py

| Flag | Type | Default | Description |
|---|---|---|---|
| `--sitemap` | path | *(required)* | Path to `sitemap.json` |
| `--pages-dir` | path | *(required)* | Directory containing scraped `.md` files |
| `--template` | path | `templates/book.html` | HTML template file |
| `--css` | path | `assets/book.css` | CSS stylesheet |
| `--output` | path | `book.pdf` | Output PDF path |
| `--title` | str | *(from sitemap root_url)* | Book title shown on title page and running header |
| `--backend` | choice | `auto` | PDF backend: `weasyprint`, `pdfkit`, or `auto` |
| `--html-only` | flag | `false` | Stop after generating HTML; skip PDF render |
| `--target-pages` | int | `0` (off) | Approximate target PDF page count; trims content to fit |
| `--toc-max-depth` | int | `3` | Maximum chapter depth shown in table of contents |
| `--toc-max-entries` | int | `500` | Maximum number of TOC entries |
| `--generate-index` | flag | `true` | Generate alphabetical back-of-book index from H2+ headings |
| `--no-index` | flag | `false` | Disable index generation |
| `--running-header` | str | *(= --title)* | Text used as the running header on every page |
| `--no-preface` | flag | `false` | Do not auto-generate a preface if none exists in content |

### Table of contents behavior

The TOC lists pages at depth ≤ `--toc-max-depth` (default 3), up to
`--toc-max-entries` (default 500). Code-heavy pages are grouped in an
"Appendix" sub-section automatically. Pages marked `suppress: true` in
`_index.json` are excluded.

### Index behavior

When `--generate-index` is set (default), build_pdf.py collects all H2 and H3
headings from the rendered HTML, deduplicates them, sorts alphabetically, and
renders a two-column "Index" section at the back of the book. Links within the
index point back to the relevant chapter sections.

### Running header behavior

The CSS uses `string-set: running-header content()` on `h1` elements. Each
chapter's H1 becomes the running header for that chapter's pages. The value set
by `--running-header` appears on pages before the first H1 (title page, TOC, etc.)
via a hidden `<span class="running-header-value">` element.

### Suppression behavior

Pages are excluded from the PDF if any of these apply:
- `record.get("error")` is truthy in `_index.json`
- `record.get("suppress")` is `true` in `_index.json`
- Content word count is < 50 after loading (near-blank)

---

## run_all.py (convenience wrapper)

Combines crawl → scrape → post-process → build PDF with a single command.

| Flag | Type | Default | Description |
|---|---|---|---|
| `--url` | str | *(required)* | Root URL |
| `--output` | path | `book.pdf` | Final PDF output path |
| `--target-pages` | int | `0` | Target PDF page count; sets `--max-pages = target*3` for crawl |
| `--max-pages` | int | `0` | Hard crawl page cap (overrides target-pages derivation if set) |
| `--work-dir` | path | `write-book-output` | Directory for intermediate files |
| `--title` | str | *(auto)* | Book title |
| `--exclude` | regex | *(none)* | URL exclude regex applied to crawl AND scrape steps |
| `--no-builtin-excludes` | flag | `false` | Disable scraper built-in URL exclusions |
| `--template` | path | `templates/book.html` | HTML template |
| `--css` | path | `assets/book.css` | CSS |
| `--backend` | choice | `auto` | PDF backend |
| `--keep-external-links` | flag | `false` | Keep external link URLs in scraped output |
| `--min-words` | int | `150` | Minimum word count per scraped page |
| `--toc-max-depth` | int | `3` | TOC depth cap |
| `--toc-max-entries` | int | `500` | TOC entry cap |
| `--running-header` | str | *(= title)* | Running header text |
| `--no-index` | flag | `false` | Disable back-of-book index |
| `--deduplicate` / `--no-deduplicate` | flag | on | Page deduplication |
| `--collapse-language-stubs` | flag | `false` | Collapse per-language catalog stubs |
| `--move-code-appendix` | flag | `false` | Move code-heavy pages to appendix |
| `--url-to-footnotes` | flag | `false` | Convert inline URLs to footnotes |
