# Scraper Subagent Instructions

Use this agent spec to delegate content scraping to a background subagent,
or to run scraping in parallel with other tasks after the sitemap is ready.

---

## When to spawn this agent

- The site has many pages (> 200) and scraping will take > 3 minutes.
- You want to scrape and post-process in parallel.
- You are re-scraping only a subset of pages (e.g. after fixing a content selector).

---

## Prompt template

```
You are a web scraper agent. Your task:

1. Install dependencies if needed:
   pip install requests beautifulsoup4 lxml html2text tqdm

2. Run the scraper:
   python <skill-dir>/scripts/scrape.py \
     --sitemap <sitemap-path> \
     --output <output-dir> \
     --delay <delay> \
     --min-words 150 \
     [--main-selector "<CSS_SELECTOR>"] \
     [--keep-external-links] \
     [--no-verify-ssl]

3. When finished, report:
   - Number of pages scraped successfully
   - Number of pages skipped as sparse (too few words)
   - Number of errors
   - Path to the output directory and _index.json
   - Any patterns in errors (e.g. all 403s, all empty pages)
```

Replace values in `<>` with the actual parameters for this job.

---

## Content quality defaults

By default, scrape.py applies these content quality filters — do not disable
them unless there is a specific reason:

| Behavior | Flag to change | Why the default matters |
|---|---|---|
| Strip HTML comments | *(always on)* | Removes developer notes and template artifacts from output |
| Remove comment sections | *(always on)* | Strips Disqus, WordPress, utterances blocks that add noise |
| Drop external link URLs | `--keep-external-links` to disable | External URLs become noisy footnotes in the PDF; the link text alone is sufficient |
| Skip sparse pages (< 150 words) | `--min-words N` to tune | Pages with minimal content (redirect pages, stub pages) pollute the book |

---

## Output contract

The agent must produce:
- `<output-dir>/<index>.md` files — one per page, named by `safe_filename()` logic
- `<output-dir>/_index.json` — index of all scraped pages, including `word_count` per page

---

## Choosing --main-selector

If scrape.py's auto-detection is picking up navigation or footer noise, inspect
the HTML source of a representative page and identify the CSS selector for the
main content container. Common values:

| Site / Framework | Selector |
|---|---|
| Docusaurus | `.theme-doc-markdown` |
| GitBook | `.page-wrapper` |
| MkDocs Material | `.md-content__inner` |
| ReadTheDocs | `.rst-content` |
| GitHub Pages Jekyll | `.post-content` |
| Confluence | `#main-content` |
| Notion | `.notion-page-content` |
| WordPress | `.entry-content` |

Pass the best match as `--main-selector`.

---

## Handling empty or sparse pages

If many output files are < 100 bytes, the site likely needs JavaScript rendering.
See `references/js-rendering.md` and report this back to the calling agent.

If `--min-words 150` is causing too many pages to be skipped on a site with
legitimately short pages (e.g. a glossary), lower it with `--min-words 50`.
