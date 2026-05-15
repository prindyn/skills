#!/usr/bin/env python3
"""
scrape.py — Content scraper for crawled pages.

Reads a sitemap JSON produced by crawl.py, fetches each page,
extracts the main content, and saves it as Markdown preserving
headings, lists, code blocks, bold/italic, tables, and blockquotes.

Usage:
    python scrape.py --sitemap sitemap.json --output pages/
    python scrape.py --sitemap sitemap.json --output pages/ \
                     --main-selector "article.content" --delay 0.3
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

import html2text
import requests
from bs4 import BeautifulSoup, Tag
from tqdm import tqdm


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; write-book-scraper/1.0; "
        "+https://github.com/agentskills/write-book)"
    )
}

# CSS selectors tried in order to find the main content block.
# The first one that matches and contains substantive text wins.
MAIN_CONTENT_SELECTORS = [
    "main",
    "article",
    '[role="main"]',
    ".content",
    ".main-content",
    ".post-content",
    ".entry-content",
    ".page-content",
    ".docs-content",
    ".markdown-body",
    "#content",
    "#main",
    "#main-content",
]

# Elements to strip before conversion (navigation, ads, etc.)
NOISE_SELECTORS = [
    "nav", "header", "footer", "aside",
    ".nav", ".navbar", ".sidebar", ".toc",
    ".breadcrumb", ".pagination", ".cookie-banner",
    ".advertisement", ".ad", "[aria-hidden='true']",
    "script", "style", "noscript",
]


def configure_html2text() -> html2text.HTML2Text:
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0          # don't hard-wrap lines
    h.protect_links = True
    h.wrap_links = False
    h.mark_code = True
    h.unicode_snob = True
    h.pad_tables_in_html = True
    h.bypass_tables = False
    h.ignore_tables = False
    return h


def find_main_content(soup: BeautifulSoup, custom_selector: str | None = None) -> Tag | None:
    if custom_selector:
        el = soup.select_one(custom_selector)
        if el:
            return el

    for sel in MAIN_CONTENT_SELECTORS:
        el = soup.select_one(sel)
        if el and len(el.get_text(strip=True)) > 200:
            return el

    return soup.body or soup


def strip_noise(element: Tag) -> Tag:
    for sel in NOISE_SELECTORS:
        for tag in element.select(sel):
            tag.decompose()
    return element


def html_to_markdown(html_fragment: str) -> str:
    converter = configure_html2text()
    md = converter.handle(html_fragment)
    # Collapse excessive blank lines (> 2 consecutive)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def scrape_page(
    url: str,
    session: requests.Session,
    main_selector: str | None = None,
    no_verify_ssl: bool = False,
) -> dict:
    try:
        resp = session.get(url, timeout=20, verify=not no_verify_ssl)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            return {"error": f"Non-HTML content-type: {content_type}", "markdown": ""}
    except requests.RequestException as exc:
        return {"error": str(exc), "markdown": ""}

    soup = BeautifulSoup(resp.text, "lxml")

    # Extract title
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    elif soup.find("h1"):
        title = soup.find("h1").get_text(strip=True)

    # Extract meta description
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_desc = meta["content"].strip()

    main = find_main_content(soup, main_selector)
    main = strip_noise(main)
    markdown = html_to_markdown(str(main))

    return {
        "title": title,
        "meta_description": meta_desc,
        "url": resp.url,
        "markdown": markdown,
        "error": None,
    }


def safe_filename(url: str, index: int) -> str:
    parsed_path = url.split("//", 1)[-1]  # strip scheme
    parsed_path = re.sub(r"[^a-zA-Z0-9_\-/]", "_", parsed_path)
    parsed_path = parsed_path.strip("/").replace("/", "__")
    parsed_path = re.sub(r"_+", "_", parsed_path)
    if not parsed_path:
        parsed_path = "page"
    return f"{index:04d}_{parsed_path[:120]}.md"


def main():
    parser = argparse.ArgumentParser(description="Scrape pages listed in a sitemap JSON.")
    parser.add_argument("--sitemap", required=True, help="Path to sitemap.json from crawl.py")
    parser.add_argument("--output", default="pages", help="Output directory for Markdown files")
    parser.add_argument("--main-selector", default=None, help="CSS selector for main content")
    parser.add_argument("--delay", type=float, default=0.3, help="Seconds between requests")
    parser.add_argument("--no-verify-ssl", action="store_true", help="Skip SSL certificate verification")
    args = parser.parse_args()

    sitemap_path = Path(args.sitemap)
    if not sitemap_path.exists():
        print(f"ERROR: sitemap file not found: {sitemap_path}", file=sys.stderr)
        sys.exit(1)

    sitemap = json.loads(sitemap_path.read_text())
    pages = sitemap.get("pages", [])
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    index_records = []
    errors = []

    for i, page in enumerate(tqdm(pages, desc="Scraping", unit="page")):
        url = page.get("url", "")
        result = scrape_page(url, session, args.main_selector, args.no_verify_ssl)

        filename = safe_filename(url, i)
        filepath = out_dir / filename

        if result["error"]:
            errors.append({"url": url, "error": result["error"]})
            tqdm.write(f"  ERROR {url} — {result['error']}")
            filepath.write_text(f"# Error\n\nFailed to scrape: {url}\n\nReason: {result['error']}\n")
        else:
            title = result["title"] or page.get("title", "Untitled")
            front = f"# {title}\n\n"
            if result["meta_description"]:
                front += f"> {result['meta_description']}\n\n"
            front += f"_Source: {url}_\n\n---\n\n"
            filepath.write_text(front + result["markdown"] + "\n")

        index_records.append({
            "index": i,
            "url": url,
            "title": result.get("title") or page.get("title", ""),
            "filename": filename,
            "depth": page.get("depth", 0),
            "error": result.get("error"),
        })

        time.sleep(args.delay)

    # Write index
    index_path = out_dir / "_index.json"
    index_path.write_text(json.dumps(index_records, indent=2, ensure_ascii=False))

    ok = sum(1 for r in index_records if not r["error"])
    print(f"\nScraped {ok}/{len(pages)} pages successfully. {len(errors)} errors.")
    print(f"Files saved to: {out_dir}")
    if errors:
        print(f"Errors logged; see {index_path} for details.")


if __name__ == "__main__":
    main()
