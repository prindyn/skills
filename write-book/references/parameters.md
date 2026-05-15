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

---

## run_all.py (convenience wrapper)

Combines all three scripts with a single command. Accepts all flags from
crawl.py and scrape.py plus:

| Flag | Type | Default | Description |
|---|---|---|---|
| `--url` | str | *(required)* | Root URL |
| `--output` | path | `book.pdf` | Final PDF output path |
| `--work-dir` | path | `write-book-output` | Directory for intermediate files |
| `--title` | str | *(auto)* | Book title |
| `--template` | path | `templates/book.html` | HTML template |
| `--css` | path | `assets/book.css` | CSS |
| `--backend` | choice | `auto` | PDF backend |
