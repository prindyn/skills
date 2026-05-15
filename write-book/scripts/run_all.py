#!/usr/bin/env python3
"""
run_all.py — One-shot pipeline: crawl → scrape → build PDF.

Orchestrates crawl.py, scrape.py, and build_pdf.py in sequence,
managing the working directory and passing arguments through.

Usage:
    python run_all.py --url https://example.com --output book.pdf
    python run_all.py --url https://docs.example.com \
        --title "Example Docs" \
        --max-depth 4 --max-pages 200 \
        --output example-docs.pdf \
        --work-dir /tmp/write-book-example
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], label: str):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  $ {' '.join(cmd)}\n")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"\nERROR: {label} failed with exit code {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="End-to-end: crawl site → scrape → PDF book")
    parser.add_argument("--url", required=True, help="Root URL to crawl")
    parser.add_argument("--output", default="book.pdf", help="Output PDF path")
    parser.add_argument("--title", default="", help="Book title")
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--max-pages", type=int, default=500)
    parser.add_argument("--include", default=None, help="URL include regex")
    parser.add_argument("--exclude", default=None, help="URL exclude regex")
    parser.add_argument("--main-selector", default=None, help="CSS selector for main content")
    parser.add_argument("--delay", type=float, default=0.25, help="Seconds between requests")
    parser.add_argument("--no-verify-ssl", action="store_true")
    parser.add_argument("--no-robots", action="store_true")
    parser.add_argument("--backend", choices=["weasyprint", "pdfkit", "auto"], default="auto")
    parser.add_argument("--work-dir", default="write-book-output", help="Working directory for intermediate files")
    parser.add_argument("--template", default=None, help="Custom HTML template path")
    parser.add_argument("--css", default=None, help="Custom CSS path")
    args = parser.parse_args()

    here = Path(__file__).parent
    work = Path(args.work_dir)
    work.mkdir(parents=True, exist_ok=True)
    sitemap = work / "sitemap.json"
    pages_dir = work / "pages"
    template = args.template or str(here.parent / "templates" / "book.html")
    css = args.css or str(here.parent / "assets" / "book.css")

    # Step 1: Crawl
    crawl_cmd = [
        sys.executable, str(here / "crawl.py"),
        "--url", args.url,
        "--max-depth", str(args.max_depth),
        "--max-pages", str(args.max_pages),
        "--delay", str(args.delay),
        "--output", str(sitemap),
    ]
    if args.include:
        crawl_cmd += ["--include", args.include]
    if args.exclude:
        crawl_cmd += ["--exclude", args.exclude]
    if args.no_verify_ssl:
        crawl_cmd.append("--no-verify-ssl")
    if args.no_robots:
        crawl_cmd.append("--no-robots")
    run(crawl_cmd, "Step 1/3: Crawl site")

    # Step 2: Scrape
    scrape_cmd = [
        sys.executable, str(here / "scrape.py"),
        "--sitemap", str(sitemap),
        "--output", str(pages_dir),
        "--delay", str(args.delay),
    ]
    if args.main_selector:
        scrape_cmd += ["--main-selector", args.main_selector]
    if args.no_verify_ssl:
        scrape_cmd.append("--no-verify-ssl")
    run(scrape_cmd, "Step 2/3: Scrape content")

    # Step 3: Build PDF
    build_cmd = [
        sys.executable, str(here / "build_pdf.py"),
        "--sitemap", str(sitemap),
        "--pages-dir", str(pages_dir),
        "--template", template,
        "--css", css,
        "--output", args.output,
        "--backend", args.backend,
    ]
    if args.title:
        build_cmd += ["--title", args.title]
    run(build_cmd, "Step 3/3: Build PDF")

    print(f"\nAll done! Book written to: {args.output}")


if __name__ == "__main__":
    main()
