#!/usr/bin/env python3
"""
crawl.py — Breadth-first website crawler.

Discovers all pages reachable from a root URL on the same domain,
respects robots.txt, and outputs a structured sitemap JSON file.

Usage:
    python crawl.py --url https://example.com --output sitemap.json
    python crawl.py --url https://docs.example.com --max-depth 3 --max-pages 100 \
                    --include "docs/" --exclude "(login|signup|tag)" --output sitemap.json
"""

import argparse
import json
import re
import sys
import time
import urllib.robotparser
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; write-book-crawler/1.0; "
        "+https://github.com/agentskills/write-book)"
    )
}


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    # Drop fragment, normalize trailing slash on paths
    path = parsed.path.rstrip("/") or "/"
    normalized = parsed._replace(fragment="", path=path, query=parsed.query)
    return urlunparse(normalized)


def same_domain(url: str, root_parsed) -> bool:
    parsed = urlparse(url)
    return parsed.netloc == root_parsed.netloc


def is_navigable_link(url: str) -> bool:
    """Reject non-HTML resource URLs."""
    skip_exts = {
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp",
        ".pdf", ".zip", ".tar", ".gz", ".mp3", ".mp4", ".avi",
        ".css", ".js", ".woff", ".woff2", ".ttf", ".eot",
        ".xml", ".json", ".csv", ".xlsx", ".docx",
    }
    path = urlparse(url).path.lower()
    return not any(path.endswith(ext) for ext in skip_exts)


def fetch_robots(root_url: str, session: requests.Session) -> urllib.robotparser.RobotFileParser:
    rp = urllib.robotparser.RobotFileParser()
    robots_url = urljoin(root_url, "/robots.txt")
    try:
        resp = session.get(robots_url, timeout=10)
        rp.parse(resp.text.splitlines())
    except Exception:
        pass
    rp.set_url(robots_url)
    return rp


def extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("javascript:"):
            continue
        full_url = urljoin(base_url, href)
        # Strip fragment
        full_url = full_url.split("#")[0]
        links.append(full_url)
    return links


def get_page_title(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    return ""


def crawl(
    root_url: str,
    max_depth: int = 5,
    max_pages: int = 500,
    include_pattern: str | None = None,
    exclude_pattern: str | None = None,
    delay: float = 0.2,
    no_verify_ssl: bool = False,
    respect_robots: bool = True,
) -> list[dict]:
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    session.verify = not no_verify_ssl

    root_parsed = urlparse(root_url)
    robots = fetch_robots(root_url, session) if respect_robots else None

    include_re = re.compile(include_pattern) if include_pattern else None
    exclude_re = re.compile(exclude_pattern) if exclude_pattern else None

    visited: set[str] = set()
    queue: deque[tuple[str, int, str | None]] = deque()
    results: list[dict] = []

    start_norm = normalize_url(root_url)
    queue.append((start_norm, 0, None))
    visited.add(start_norm)

    pbar = tqdm(total=max_pages, desc="Crawling", unit="page")

    while queue and len(results) < max_pages:
        url, depth, parent = queue.popleft()

        if depth > max_depth:
            continue

        if include_re and not include_re.search(url):
            continue
        if exclude_re and exclude_re.search(url):
            continue
        if robots and not robots.can_fetch("*", url):
            continue

        try:
            resp = session.get(url, timeout=15, allow_redirects=True)
            resp.raise_for_status()
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                continue
        except requests.RequestException as exc:
            tqdm.write(f"  SKIP {url} — {exc}")
            continue

        title = get_page_title(resp.text)
        final_url = normalize_url(resp.url)

        entry = {
            "url": final_url,
            "original_url": url,
            "title": title,
            "depth": depth,
            "parent": parent,
        }
        results.append(entry)
        pbar.update(1)
        pbar.set_postfix(depth=depth, pages=len(results))

        if depth < max_depth:
            for link in extract_links(resp.text, final_url):
                norm = normalize_url(link)
                if (
                    norm not in visited
                    and same_domain(link, root_parsed)
                    and is_navigable_link(link)
                ):
                    visited.add(norm)
                    queue.append((norm, depth + 1, final_url))

        time.sleep(delay)

    pbar.close()
    return results


def main():
    parser = argparse.ArgumentParser(description="Crawl a website and produce a sitemap JSON.")
    parser.add_argument("--url", required=True, help="Root URL to start crawling from")
    parser.add_argument("--max-depth", type=int, default=5, help="Maximum link depth (default: 5)")
    parser.add_argument("--max-pages", type=int, default=500, help="Maximum pages to crawl (default: 500)")
    parser.add_argument("--include", default=None, help="Regex: only include matching URLs")
    parser.add_argument("--exclude", default=None, help="Regex: exclude matching URLs")
    parser.add_argument("--delay", type=float, default=0.2, help="Seconds between requests (default: 0.2)")
    parser.add_argument("--no-verify-ssl", action="store_true", help="Skip SSL certificate verification")
    parser.add_argument("--no-robots", action="store_true", help="Ignore robots.txt")
    parser.add_argument("--output", default="sitemap.json", help="Output JSON file (default: sitemap.json)")
    args = parser.parse_args()

    print(f"Starting crawl: {args.url}")
    pages = crawl(
        root_url=args.url,
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        include_pattern=args.include,
        exclude_pattern=args.exclude,
        delay=args.delay,
        no_verify_ssl=args.no_verify_ssl,
        respect_robots=not args.no_robots,
    )

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sitemap = {
        "root_url": args.url,
        "total_pages": len(pages),
        "pages": pages,
    }
    out_path.write_text(json.dumps(sitemap, indent=2, ensure_ascii=False))
    print(f"\nCrawled {len(pages)} pages → {out_path}")


if __name__ == "__main__":
    main()
