# JavaScript-Rendered Pages

Some sites (SPAs, React/Vue/Angular apps, Next.js with client-side rendering)
deliver most content via JavaScript. The default `requests` + BeautifulSoup
approach will fetch an empty shell.

---

## Detecting JS-heavy pages

Signs that a site needs JS rendering:
- The scraped Markdown files are very short (< 50 words) despite visible content in a browser.
- The HTML source shows `<div id="root"></div>` or similar empty mounts.
- The `<noscript>` tag contains the real content.

---

## Playwright fallback (recommended)

[Playwright](https://playwright.dev/python/) is a headless browser automation
library that fully executes JavaScript before returning the rendered HTML.

### Install

```bash
pip install playwright
playwright install chromium
```

### Drop-in usage with scrape.py

Pass `--playwright` to scrape.py (if this flag is supported in your version):

```bash
python scripts/scrape.py \
  --sitemap crawl_output/sitemap.json \
  --output crawl_output/pages/ \
  --playwright \
  --wait-for "main, article, .content"
```

### Manual Playwright snippet

```python
from playwright.sync_api import sync_playwright

def fetch_with_playwright(url: str, wait_selector: str = "body") -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_selector(wait_selector, timeout=10_000)
        html = page.content()
        browser.close()
    return html
```

Replace `resp.text` in scrape.py with the output of `fetch_with_playwright(url)`.

---

## Selenium fallback

An older alternative to Playwright:

```bash
pip install selenium
# Install ChromeDriver matching your Chrome version
```

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=opts)
driver.get(url)
html = driver.page_source
driver.quit()
```

---

## Performance note

Each headless browser page load is ~5–10× slower than a plain HTTP request.
For large sites, consider:
- Running Playwright scraping in parallel (but respect rate limits)
- Scraping only the pages that returned sparse content in the initial pass
- Using `--max-pages` to limit scope
