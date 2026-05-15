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
     --min-words 200 \
     --exclude "(sale|pricing|buy|checkout|testimonial|review|faq|payment|forum|userecho|newsletter)" \
     [--main-selector "<CSS_SELECTOR>"] \
     [--keep-external-links] \
     [--no-verify-ssl] \
     [--no-builtin-excludes]

3. When finished, report:
   - Number of pages scraped successfully
   - Number of pages excluded by URL pattern
   - Number of pages skipped as sparse (too few words)
   - Number of errors
   - Path to the output directory and _index.json
   - Any patterns in errors (e.g. all 403s, all empty pages)
```

Replace values in `<>` with the actual parameters for this job.

---

## Content quality defaults

By default, scrape.py applies these filters — do not disable them unless there
is a specific reason:

| Behavior | Flag to change | Why the default matters |
|---|---|---|
| Strip HTML comments | *(always on)* | Removes developer notes and template artifacts from output |
| Remove comment sections | *(always on)* | Strips Disqus, WordPress, utterances blocks |
| Strip e-commerce/forum elements | *(always on)* | Removes pricing, vote widgets, testimonial blocks, UserEcho |
| Strip [code] tag artifacts | *(always on)* | Converts forum-style BBCode to proper fenced code blocks |
| Strip video fallback text | *(always on)* | Removes "Your browser does not support HTML video" lines |
| Strip empty widget labels | *(always on)* | Removes "Complexity:" / "Popularity:" lines with no value |
| Deduplicate H1 | *(always on)* | Title is written in frontmatter; the scraped H1 is stripped so it does not appear twice |
| Exclude e-commerce URLs | *(always on)* | Skips /sale/, /pricing/, /buy, /checkout, /testimonial, /faq, etc. |
| Drop external link URLs | `--keep-external-links` to disable | External URLs become noisy footnotes; the link text alone is cleaner |
| Skip sparse pages (< 200 words) | `--min-words N` to tune | Stub pages pollute the book |

---

## URL exclusion strategy

The scraper has two layers of URL exclusion:

1. **Built-in patterns** (always on unless `--no-builtin-excludes`): skip URLs
   containing sale, pricing, buy, checkout, testimonial, review, faq, payment,
   refund, forum, userecho, newsletter, subscribe, login, logout, signup.

2. **`--exclude` regex** (user-supplied): applies on top of built-in patterns.
   Use this to exclude site-specific non-book pages:
   ```
   --exclude "(about-me|author|facebook|twitter|/zh/|/ja/|/ko/)"
   ```

Pass the same `--exclude` pattern to `crawl.py` so those pages are never crawled
in the first place.

---

## Output contract

The agent must produce:
- `<output-dir>/<index>.md` files — one per page, named by `safe_filename()` logic
- `<output-dir>/_index.json` — index of all pages including:
  - `word_count` per page
  - `error` (null if successful)
  - `suppress` (set by postprocess.py for near-blank / duplicate pages)
  - `code_heavy` (set by postprocess.py for appendix candidates)
  - `chapter` and `mece_order` (set by formatter agent)

---

## Choosing --main-selector

If scrape.py's auto-detection picks up navigation or footer noise, inspect the
HTML source of a representative page and identify the CSS selector for the main
content container. Common values:

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
| Refactoring.guru style | `.content-wrapper article` |

Pass the best match as `--main-selector`.

---

## Handling empty or sparse pages

If many output files are < 100 bytes, the site likely needs JavaScript rendering.
See `references/js-rendering.md` and report this back to the calling agent.

If `--min-words 200` is causing too many pages to be skipped on a site with
legitimately short pages (e.g. a glossary), lower it with `--min-words 50`.
