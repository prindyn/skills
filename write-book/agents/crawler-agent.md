# Crawler Subagent Instructions

Use this agent spec when the main agent needs to delegate a large or slow crawl
to a background subagent, or when a crawl and a scrape should run concurrently.

---

## When to spawn this agent

- The site has more than ~300 estimated pages and the crawl will take > 2 minutes.
- You want to crawl and scrape in parallel (crawler feeds pages to the scraper as they arrive).
- The user wants progress updates while the crawl runs.

---

## Prompt template

```
You are a web crawler agent. Your task:

1. Install dependencies if needed:
   pip install requests beautifulsoup4 lxml tqdm

2. Run the crawler:
   python <skill-dir>/scripts/crawl.py \
     --url "<ROOT_URL>" \
     --max-depth <DEPTH> \
     --max-pages <MAX_PAGES> \
     --delay <DELAY> \
     --output <OUTPUT_DIR>/sitemap.json \
     [--include "<INCLUDE_PATTERN>"] \
     [--exclude "<EXCLUDE_PATTERN>"] \
     [--no-verify-ssl] \
     [--no-robots]

3. When finished, report:
   - Total pages found
   - Any errors or skipped URLs (summarize, don't list all)
   - Path to the sitemap.json file
```

Replace values in `<>` with the actual parameters for this job.

---

## Output contract

The agent must produce:
- `<output_dir>/sitemap.json` — valid JSON matching the sitemap schema in `references/parameters.md`

The calling agent reads this file and passes it to the scraper.

---

## Error handling guidance

If the crawl finds 0 pages:
- Check whether the root URL is accessible (try `curl -I <url>`)
- Check whether the site requires JavaScript rendering (see `references/js-rendering.md`)
- Check whether `--include` is too narrow

If the crawl is slow (< 1 page/sec):
- Increase `--delay` is not the issue — lower it carefully
- Consider narrowing scope with `--include` or reducing `--max-depth`
