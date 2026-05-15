#!/usr/bin/env python3
"""
inspect_sample.py — Sample and display N random scraped Markdown files.

Run this BEFORE post-processing or PDF build to spot-check content quality.
Prints file name, word count, URL, and first --max-chars characters of each page.

Inspection checklist:
  - Raw https:// URLs still in body text (should be stripped or converted to footnotes)
  - Site chrome that slipped through (navigation text, cookie notices, "Was this page helpful?")
  - CTA/upsell fragments ("Buy now", "Get the book", "Tired of reading?")
  - "In Other Languages" tab lists that are mostly just links
  - Pages that are 90% code with no explanation (appendix candidates)
  - SEO landing pages masquerading as content (bullet lists, no depth)

Usage:
    python scripts/inspect_sample.py --pages-dir crawl_output/pages/ --n 5
    python scripts/inspect_sample.py --pages-dir crawl_output/pages/ --n 10 --seed 42
    python scripts/inspect_sample.py --pages-dir crawl_output/pages/ --file 0042_some_page.md
"""

import argparse
import json
import random
import re
import sys
from pathlib import Path


def word_count(text: str) -> int:
    return len(text.split())


def count_bare_urls(text: str) -> int:
    return len(re.findall(r'(?<!\()(?<!\[)\bhttps?://\S+', text))


def count_external_md_links(text: str) -> int:
    return len(re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)', text))


def code_fraction(text: str) -> float:
    total = word_count(text)
    if total == 0:
        return 0.0
    code_words = sum(word_count(b) for b in re.findall(r'```.*?```', text, re.DOTALL))
    return code_words / total


def check_cta_patterns(text: str) -> list:
    patterns = [
        (r'tired of reading', "CTA: 'Tired of reading?'"),
        (r'get the (book|course|ebook)', "CTA: 'Get the book/course'"),
        (r'buy (now|today|as a gift)', "CTA: 'Buy now/today'"),
        (r'add to cart', "CTA: 'Add to cart'"),
        (r'spring sale|summer sale', "Sales banner"),
        (r'money.back guarantee', "Sales: 'Money-back guarantee'"),
        (r'this product is (only )?available in english', "Language sales notice"),
        (r'was this (page|article) helpful', "Site chrome: 'Was this helpful?'"),
        (r'share this (page|post|article)', "Site chrome: 'Share this'"),
        (r'in other languages', "Nav widget: 'In Other Languages'"),
        (r'privacy policy|terms of (service|use)', "Legal page leaked"),
        (r'cookie', "Cookie/GDPR notice"),
    ]
    hits = []
    lower = text.lower()
    for pattern, label in patterns:
        if re.search(pattern, lower):
            hits.append(label)
    return hits


def analyze_page(text: str) -> dict:
    wc = word_count(text)
    bare_urls = count_bare_urls(text)
    ext_links = count_external_md_links(text)
    code_frac = code_fraction(text)
    cta_hits = check_cta_patterns(text)
    issues = []
    if bare_urls > 0:
        issues.append(f"{bare_urls} bare https:// URL(s) in body")
    if ext_links > 0:
        issues.append(f"{ext_links} external Markdown link(s) with URL (should be text-only)")
    if code_frac > 0.6:
        issues.append(f"Code-heavy: {code_frac:.0%} of words are in code blocks (appendix candidate)")
    if wc < 100:
        issues.append(f"Very sparse: only {wc} words")
    issues.extend(cta_hits)
    return {
        "word_count": wc,
        "bare_urls": bare_urls,
        "external_links": ext_links,
        "code_fraction": code_frac,
        "issues": issues,
    }


def format_separator(label: str = "", width: int = 70) -> str:
    if label:
        pad = max(0, width - len(label) - 4)
        return "═" * 2 + f" {label} " + "═" * pad
    return "═" * width


def inspect_file(rec: dict, pages_dir: Path, max_chars: int, index: int, total: int):
    filename = rec.get("filename", "")
    url = rec.get("url", "")
    title = rec.get("title", "")
    stored_wc = rec.get("word_count", "?")

    md_path = pages_dir / filename
    if not md_path.exists():
        print(f"[{index}/{total}] {filename} — FILE NOT FOUND")
        return

    content = md_path.read_text(encoding="utf-8")
    analysis = analyze_page(content)

    print(format_separator(f"{index}/{total}: {filename}"))
    print(f"URL:        {url}")
    print(f"Title:      {title}")
    print(f"Words:      {analysis['word_count']} (index: {stored_wc})")
    print(f"Code:       {analysis['code_fraction']:.0%} of words in code blocks")

    if analysis["issues"]:
        print(f"⚠ Issues:")
        for issue in analysis["issues"]:
            print(f"   • {issue}")
    else:
        print("✓ No obvious issues detected")

    print("─" * 70)
    preview = content[:max_chars]
    if len(content) > max_chars:
        preview += f"\n\n... [{len(content) - max_chars} more characters] ..."
    print(preview)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a random sample of scraped Markdown files before post-processing."
    )
    parser.add_argument(
        "--pages-dir", required=True,
        help="Directory with scraped .md files and _index.json"
    )
    parser.add_argument(
        "--n", type=int, default=5,
        help="Number of files to sample (default: 5)"
    )
    parser.add_argument(
        "--max-chars", type=int, default=3000,
        help="Max characters to print per file (default: 3000)"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--file", default=None,
        help="Inspect a specific filename instead of sampling randomly"
    )
    parser.add_argument(
        "--active-only", action="store_true", default=True,
        help="Only sample pages without errors or suppress flag (default: on)"
    )
    args = parser.parse_args()

    pages_dir = Path(args.pages_dir)
    index_path = pages_dir / "_index.json"

    if not index_path.exists():
        print(f"ERROR: _index.json not found in {pages_dir}", file=sys.stderr)
        sys.exit(1)

    index = json.loads(index_path.read_text(encoding="utf-8"))

    if args.file:
        rec = next((r for r in index if r.get("filename") == args.file), None)
        if not rec:
            print(f"ERROR: filename '{args.file}' not found in _index.json", file=sys.stderr)
            sys.exit(1)
        inspect_file(rec, pages_dir, args.max_chars, 1, 1)
        return

    active = [r for r in index if not r.get("error") and not r.get("suppress")]

    if not active:
        print("No active pages found to sample.", file=sys.stderr)
        sys.exit(1)

    if args.seed is not None:
        random.seed(args.seed)

    n = min(args.n, len(active))
    sample = random.sample(active, n)

    total_active = len(active)
    total_index = len(index)
    suppressed = sum(1 for r in index if r.get("suppress"))
    errored = sum(1 for r in index if r.get("error"))

    print(format_separator("write-book: Markdown Sample Inspection"))
    print(f"Pages directory:  {pages_dir}")
    print(f"Total in index:   {total_index}  (active: {total_active}, suppressed: {suppressed}, errors: {errored})")
    print(f"Sampling:         {n} random active pages")
    print()
    print("Look for: bare URLs, CTAs/upsells, navigation noise, legal pages, code-only pages, SEO fluff")
    print(format_separator())
    print()

    for i, rec in enumerate(sample, 1):
        inspect_file(rec, pages_dir, args.max_chars, i, n)

    print(format_separator("End of sample"))
    print()
    print("If you spotted issues above, fix scraper patterns and re-scrape before building the PDF.")
    print("Rebuilding the PDF to discover noise is much slower than fixing it in Markdown.")


if __name__ == "__main__":
    main()
