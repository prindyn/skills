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
| `--exclude` | regex | *(none)* | Skip URLs matching this pattern. Use same pattern as `scrape.py --exclude`. Always include legal/account noise: `(privacy\|terms\|legal\|gdpr\|cookies\|imprint\|about\|sale\|cart\|signup\|login)` |
| `--delay` | float | `0.2` | Seconds to wait between requests |
| `--no-verify-ssl` | flag | `false` | Disable SSL certificate verification |
| `--no-robots` | flag | `false` | Ignore robots.txt restrictions |
| `--output` | path | `sitemap.json` | Output JSON file path |

### Recommended exclude pattern

For most programming/documentation sites, use this combined pattern for both
`crawl.py` and `scrape.py`:

```
(privacy|terms|legal|gdpr|cookies|imprint|about|sale|cart|signup|login|pricing|buy|checkout|testimonials|reviews|faq|payment|refund|forum|community|vote|userecho|newsletter|subscribe|register|account|zh|ja|ko|pl|de|fr|es|pt|ru)
```

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

### Inspect URL list before scraping

After crawling, grep the URL list for junk before committing to scraping:

```bash
python -c "
import json
data = json.loads(open('crawl_output/sitemap.json').read())
for p in data['pages']:
    print(p['url'])
" | grep -iE "(privacy|terms|legal|gdpr|about|cookies|imprint|login|signup|sale|cart|faq|testimonial|review|forum)"
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
| `--no-builtin-excludes` | flag | `false` | Disable built-in exclusion patterns |

### Content quality behavior (always on)

- **HTML comments stripped**: `<!-- ... -->` nodes removed before text extraction
- **Noise elements removed**: `nav`, `header`, `footer`, vote widgets, UserEcho widgets, testimonial blocks, pricing tables, CTA blocks, "In Other Languages" tab rows, author-bio sections, multi-language banners, cookie/GDPR notices
- **CTAs/upsells stripped**: "Tired of reading?", "Get the book now", "Spring SALE", "Buy as a gift", etc.
- **[code] artifacts fixed**: `[code]`/`[/code]` tags converted to proper fenced code blocks
- **Video fallback removed**: "Your browser does not support HTML video." lines stripped
- **Empty widget labels removed**: "Complexity:", "Popularity:" lines with no value stripped
- **H1 deduplicated**: the first `# Heading` in the scraped body is removed (title written in frontmatter)
- **External links converted to text**: `[link text](https://external.com)` → `link text`
- **Sparse pages skipped**: pages with fewer than `--min-words` words are excluded

### Built-in URL exclusions (always on unless `--no-builtin-excludes`)

Pages at URLs matching these patterns are skipped automatically:

```
# Legal / compliance
/(privacy|privacy-policy)
/(terms|terms-of-service|terms-of-use|tos)
/(legal|disclaimer|imprint)
/(gdpr|cookies|cookie-policy)

# Account / auth
/(login|logout|sign-?in|sign-?up|signup|register|account|profile|dashboard)
/(cart|basket|wishlist)

# About
/(about|about-us|about-me)

# E-commerce
/(sale|spring-sale|discount|promo|coupon)
/(pricing|price|buy|purchase|checkout|order|gift|amazon)
/(refund|money-back|guarantee)
/(testimonial|review|customer)
/(faq|payment|payment-method)
/(forum|community|vote|userecho)
/(newsletter|subscribe|sendy)
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

## inspect_sample.py

| Flag | Type | Default | Description |
|---|---|---|---|
| `--pages-dir` | path | *(required)* | Directory with scraped `.md` files and `_index.json` |
| `--n` | int | `5` | Number of files to sample randomly |
| `--max-chars` | int | `3000` | Max characters to print per file |
| `--seed` | int | *(none)* | Random seed for reproducibility |
| `--file` | filename | *(none)* | Inspect a specific file instead of sampling |

**Run this before post-processing or PDF build.** The script also analyzes each
sampled file for common problems: bare URLs, external Markdown links with URLs,
code-heavy pages, sparse pages, CTA patterns, "In Other Languages" blocks, and
legal page content.

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
| `--strip-ctas` | flag | `false` | Strip residual CTA/upsell patterns (second pass after scrape.py) |
| `--min-content-words` | int | `0` | Suppress pages with fewer words (0 = disabled) |

### _index.json fields added by postprocess.py

| Field | Type | Meaning |
|---|---|---|
| `suppress` | bool | `true` = exclude this page from the PDF |
| `suppress_reason` | str | Why the page was suppressed |
| `merged_into` | str | Filename of the page this was merged into |
| `code_heavy` | bool | `true` = page is mostly code; suggest appendix placement |

### _index.json fields set by the formatter agent

| Field | Type | Meaning |
|---|---|---|
| `chapter` | str | Chapter theme this page belongs to |
| `mece_order` | int | Position within that chapter (0-based) |
| `xref_chapter` | str | For appendix pages: name of the main chapter this code relates to |

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
| `--toc-max-entries` | int | `300` | Maximum number of TOC entries |
| `--generate-index` | flag | `true` | Generate alphabetical back-of-book index from H2+ headings |
| `--no-index` | flag | `false` | Disable index generation |
| `--max-index-entries` | int | `0` | Cap index at N entries (0 = no cap). Use when index is noisy. |
| `--index-warn-threshold` | int | `300` | Warn if index would exceed N entries |
| `--running-header` | str | *(= --title)* | Text used as the running header on every page |
| `--auto-preface` | flag | `false` | Generate a generic auto preface if no preface page is found. **Default OFF** — write your own preface instead. |

### Recommended workflow: HTML first, then PDF

Always build HTML first to check for problems before rendering to PDF:

```bash
# Check HTML output
python scripts/build_pdf.py --html-only ...

# Then render PDF
python scripts/build_pdf.py ...
```

Look for in the HTML: blank pages between chapters, raw URLs, noise in first chapters, missing "See also:" cross-references in appendix, noisy index.

### Page-break behavior (no blank pages)

build_pdf.py uses `page-break-before: always` on `.chapter` elements via CSS.
It does NOT emit `<div class="page-break">` between sections. Stacking both
`page-break-after` on a div and `page-break-before` on the next element creates
blank pages. Only one mechanism is used.

### Cross-reference behavior

If the formatter agent has set `xref_chapter` on appendix pages in `_index.json`,
build_pdf.py prepends a `> **See also:** [chapter]` blockquote to each appendix page,
linking readers back to the conceptual explanation in the main content.

### Index behavior

When `--generate-index` is set (default), build_pdf.py collects all H2 and H3
headings from the rendered HTML, filters out generic terms (example, overview,
introduction, summary, note, tip, etc.), sorts alphabetically, and renders a
two-column "Index" section at the back of the book.

If the index has > `--index-warn-threshold` entries (default 300), a warning is
printed. Consider `--no-index` or `--max-index-entries 150` if the index is noisy.

### Auto-preface behavior

By default, `--auto-preface` is OFF. Write your own preface as a `.md` file
and include it as the first chapter in `_index.json`. An auto-generated preface
is generic and adds less value than one that states the audience, scope, and
reading order for this specific book.

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
| `--toc-max-entries` | int | `300` | TOC entry cap |
| `--running-header` | str | *(= title)* | Running header text |
| `--no-index` | flag | `false` | Disable back-of-book index |
| `--deduplicate` / `--no-deduplicate` | flag | on | Page deduplication |
| `--collapse-language-stubs` | flag | `false` | Collapse per-language catalog stubs |
| `--move-code-appendix` | flag | `false` | Move code-heavy pages to appendix |
| `--url-to-footnotes` | flag | `false` | Convert inline URLs to footnotes |
| `--strip-ctas` | flag | `false` | Strip residual CTA/upsell patterns |
| `--auto-preface` | flag | `false` | Generate a generic auto preface (default OFF) |
