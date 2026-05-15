# Web Crawling Guide

Tips and strategies for getting complete, clean coverage of a website.

---

## Starting URL selection

The starting URL determines which pages are reachable via `<a href>` links.

| Site type | Recommended starting URL |
|---|---|
| Documentation site | Root or `/docs/` index |
| Blog | Homepage or `/blog/` archive |
| Wiki | Main page / index |
| Single-page app | See `js-rendering.md` |

If the site has a sitemap XML (`/sitemap.xml` or `/sitemap_index.xml`), you can
pre-seed the crawl with all known URLs instead of following links. Check by
visiting `https://example.com/sitemap.xml` in a browser.

---

## Controlling scope with --include / --exclude

These accept Python regular expressions matched against the full URL.

**Include only a documentation sub-section:**

```bash
--include "/docs/"
```

**Exclude login, search, and tag pages:**

```bash
--exclude "(login|logout|sign-?up|register|search|/tag/|/category/|/author/)"
```

**Exclude query-string pages (pagination, filters):**

```bash
--exclude "\?"
```

**Only English pages on a multi-language site:**

```bash
--include "/en/"
--exclude "/(fr|de|es|ja|zh)/"
```

---

## Depth and page limits

`--max-depth` controls how many link-hops from the root URL are followed.
`--max-pages` caps the total regardless of depth.

| Site size | Suggested settings |
|---|---|
| Small site (< 50 pages) | `--max-depth 10 --max-pages 100` |
| Medium docs (50–300 pages) | `--max-depth 6 --max-pages 400` |
| Large site (300–1000 pages) | `--max-depth 5 --max-pages 800` |
| Very large / scrape a section | Use `--include` to narrow scope |

---

## Rate limiting and politeness

The default `--delay 0.2` waits 200 ms between requests.
For public sites you don't own, use at least `--delay 1.0`.
For sites with a rate limit, watch for HTTP 429 responses in the output and
increase `--delay` accordingly.

The crawler respects `robots.txt` by default. Pass `--no-robots` only on sites
you own or have explicit permission to crawl.

---

## Handling authentication

crawl.py does not handle authentication. For sites behind a login:

1. Log in using a browser.
2. Copy the session cookies (e.g. from browser DevTools → Application → Cookies).
3. Add a `Cookie` header to the session in `crawl.py`:

```python
session.headers["Cookie"] = "sessionid=abc123; csrftoken=xyz"
```

Or use environment variables and load them in the script.

---

## Sitemap XML

If `sitemap.xml` is available, you can skip crawling entirely and feed the URLs
directly to `scrape.py`. Write a small script to parse the XML and produce a
`sitemap.json` in the expected format:

```python
import xml.etree.ElementTree as ET, json

tree = ET.parse("sitemap.xml")
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [loc.text for loc in tree.findall(".//sm:loc", ns)]
pages = [{"url": u, "title": "", "depth": 1, "parent": None} for u in urls]
sitemap = {"root_url": urls[0], "total_pages": len(pages), "pages": pages}
with open("sitemap.json", "w") as f:
    json.dump(sitemap, f, indent=2)
```
