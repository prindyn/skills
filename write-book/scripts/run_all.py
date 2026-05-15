#!/usr/bin/env python3
"""
run_all.py — One-shot pipeline: crawl → scrape → [fetch images] → post-process → build PDF.

Orchestrates crawl.py, scrape.py, fetch_images.py (optional), postprocess.py,
and build_pdf.py in sequence, managing the working directory and passing arguments.

Usage:
    python run_all.py --url https://example.com --output book.pdf
    python run_all.py --url https://docs.example.com \\
        --title "Example Docs" \\
        --target-pages 100 \\
        --max-depth 4 \\
        --output example-docs.pdf \\
        --keep-images \\
        --work-dir /tmp/write-book-example

Note: After crawling, run_all.py prints the URL list so you can inspect it
for junk before scraping proceeds. Use --inspect-urls to print and pause.
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
    parser = argparse.ArgumentParser(description="End-to-end: crawl site → scrape → post-process → PDF book")
    parser.add_argument("--url", required=True, help="Root URL to crawl")
    parser.add_argument("--output", default="book.pdf", help="Output PDF path")
    parser.add_argument("--title", default="", help="Book title")
    parser.add_argument(
        "--target-pages", type=int, default=0,
        help="Approximate target PDF page count. Sets --max-pages = target*3 for crawling "
             "and trims low-value pages in build step to approach the target."
    )
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--max-pages", type=int, default=0,
                        help="Hard cap on crawled pages (overrides target-pages calculation if set)")
    parser.add_argument("--include", default=None, help="URL include regex")
    parser.add_argument(
        "--exclude", default=None,
        help="URL exclude regex applied to both crawl and scrape steps. "
             "Always include legal/account noise: "
             "'(privacy|terms|legal|gdpr|cookies|imprint|about|sale|cart|signup|login)'"
    )
    parser.add_argument("--main-selector", default=None, help="CSS selector for main content")
    parser.add_argument("--delay", type=float, default=0.25, help="Seconds between requests")
    parser.add_argument("--no-verify-ssl", action="store_true")
    parser.add_argument("--no-robots", action="store_true")
    parser.add_argument("--backend", choices=["weasyprint", "pdfkit", "auto"], default="auto")
    parser.add_argument("--work-dir", default="write-book-output", help="Working directory for intermediate files")
    parser.add_argument("--template", default=None, help="Custom HTML template path")
    parser.add_argument("--css", default=None, help="Custom CSS path")
    parser.add_argument(
        "--keep-external-links", action="store_true",
        help="Keep external link URLs in scraped content (default: strip, keep link text only)"
    )
    parser.add_argument(
        "--keep-images", action="store_true",
        help="Preserve image references in scraped content and run fetch_images.py "
             "to download and filter valuable images (diagrams, screenshots, figures). "
             "Requires the user to have confirmed image inclusion in Phase 0."
    )
    parser.add_argument(
        "--min-width", type=int, default=200,
        help="Minimum image width in pixels when --keep-images is set (default: 200)"
    )
    parser.add_argument(
        "--max-image-size-mb", type=float, default=5.0,
        help="Maximum image file size in MB when --keep-images is set (default: 5.0)"
    )
    parser.add_argument(
        "--min-words", type=int, default=150,
        help="Minimum word count for a page to be included (default: 150)"
    )
    parser.add_argument(
        "--toc-max-depth", type=int, default=3,
        help="Maximum depth shown in table of contents (default: 3)"
    )
    parser.add_argument(
        "--toc-max-entries", type=int, default=300,
        help="Maximum entries in table of contents (default: 300)"
    )
    parser.add_argument(
        "--running-header", default="",
        help="Running header text shown at top of every page"
    )
    parser.add_argument(
        "--no-index", action="store_true",
        help="Disable alphabetical back-of-book index generation"
    )
    parser.add_argument(
        "--no-builtin-excludes", action="store_true",
        help="Disable scraper's built-in URL exclusions (e-commerce, legal, testimonial, forum, auth)"
    )
    # Post-processing flags
    parser.add_argument(
        "--deduplicate", action="store_true", default=True,
        help="Deduplicate near-identical pages (default: on)"
    )
    parser.add_argument(
        "--no-deduplicate", action="store_true",
        help="Disable deduplication"
    )
    parser.add_argument(
        "--collapse-language-stubs", action="store_true",
        help="Collapse per-language stub catalog pages into one"
    )
    parser.add_argument(
        "--move-code-appendix", action="store_true",
        help="Move code-heavy pages to an appendix section"
    )
    parser.add_argument(
        "--url-to-footnotes", action="store_true",
        help="Convert bare inline URLs to Markdown footnotes"
    )
    parser.add_argument(
        "--strip-ctas", action="store_true",
        help="Strip residual CTA/upsell patterns (second pass after scrape.py)"
    )
    parser.add_argument(
        "--auto-preface", action="store_true", default=False,
        help="Generate a minimal placeholder preface page (default OFF — write your own preface instead)"
    )
    args = parser.parse_args()

    here = Path(__file__).parent
    work = Path(args.work_dir)
    work.mkdir(parents=True, exist_ok=True)
    sitemap = work / "sitemap.json"
    pages_dir = work / "pages"
    images_dir = work / "images"
    template = args.template or str(here.parent / "templates" / "book.html")
    css = args.css or str(here.parent / "assets" / "book.css")

    # Determine max-pages for the crawl step
    if args.target_pages > 0 and args.max_pages == 0:
        max_pages = args.target_pages * 3
        print(f"target-pages={args.target_pages} → crawling up to {max_pages} source pages")
    elif args.max_pages > 0:
        max_pages = args.max_pages
    else:
        max_pages = 500

    # Step 1: Crawl
    crawl_cmd = [
        sys.executable, str(here / "crawl.py"),
        "--url", args.url,
        "--max-depth", str(args.max_depth),
        "--max-pages", str(max_pages),
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
    run(crawl_cmd, "Step 1/5: Crawl site")

    # Print URL list after crawl so you can spot junk before scraping
    print("\n  Crawled URL list (inspect for noise before scraping):")
    print("  " + "-" * 58)
    try:
        import json
        data = json.loads(sitemap.read_text())
        for p in data.get("pages", [])[:50]:
            print(f"  {p['depth']:>2}  {p['url']}")
        total = len(data.get("pages", []))
        if total > 50:
            print(f"  ... and {total - 50} more. See {sitemap} for full list.")
        print()
        print("  Tip: if you see privacy|terms|legal|gdpr|about|login|signup pages above,")
        print("  add them to --exclude and re-run. Scraping noise is slower to fix later.")
    except Exception:
        pass
    print("  " + "-" * 58)

    # Step 2: Scrape
    scrape_cmd = [
        sys.executable, str(here / "scrape.py"),
        "--sitemap", str(sitemap),
        "--output", str(pages_dir),
        "--delay", str(args.delay),
        "--min-words", str(args.min_words),
    ]
    if args.main_selector:
        scrape_cmd += ["--main-selector", args.main_selector]
    if args.no_verify_ssl:
        scrape_cmd.append("--no-verify-ssl")
    if args.keep_external_links:
        scrape_cmd.append("--keep-external-links")
    if args.keep_images:
        scrape_cmd.append("--keep-images")
    if args.exclude:
        scrape_cmd += ["--exclude", args.exclude]
    if args.no_builtin_excludes:
        scrape_cmd.append("--no-builtin-excludes")
    run(scrape_cmd, "Step 2/5: Scrape content")

    # Step 3: Fetch and filter images (only when --keep-images requested)
    step_num = 3
    if args.keep_images:
        fetch_cmd = [
            sys.executable, str(here / "fetch_images.py"),
            "--pages-dir", str(pages_dir),
            "--images-dir", str(images_dir),
            "--root-url", args.url,
            "--min-width", str(args.min_width),
            "--max-size-mb", str(args.max_image_size_mb),
            "--delay", str(args.delay),
        ]
        if args.no_verify_ssl:
            fetch_cmd.append("--no-verify-ssl")
        run(fetch_cmd, f"Step 3/5: Fetch and filter images")
        print(f"\n  Review {images_dir}/_manifest.json to verify only valuable images were kept.")
        step_num = 4
    else:
        step_num = 3

    # Step 4 (or 3): Post-process
    total_steps = 5 if args.keep_images else 4
    postprocess_cmd = [
        sys.executable, str(here / "postprocess.py"),
        "--pages-dir", str(pages_dir),
        "--min-content-words", str(args.min_words),
    ]
    if not args.no_deduplicate:
        postprocess_cmd.append("--deduplicate")
    if args.collapse_language_stubs:
        postprocess_cmd.append("--collapse-language-stubs")
    if args.move_code_appendix:
        postprocess_cmd.append("--move-code-appendix")
    if args.url_to_footnotes:
        postprocess_cmd.append("--url-to-footnotes")
    if args.strip_ctas:
        postprocess_cmd.append("--strip-ctas")
    run(postprocess_cmd, f"Step {step_num}/{total_steps}: Post-process and clean")
    step_num += 1

    # Step 5 (or 4): Build PDF
    build_cmd = [
        sys.executable, str(here / "build_pdf.py"),
        "--sitemap", str(sitemap),
        "--pages-dir", str(pages_dir),
        "--template", template,
        "--css", css,
        "--output", args.output,
        "--backend", args.backend,
        "--toc-max-depth", str(args.toc_max_depth),
        "--toc-max-entries", str(args.toc_max_entries),
    ]
    if args.title:
        build_cmd += ["--title", args.title]
    if args.target_pages > 0:
        build_cmd += ["--target-pages", str(args.target_pages)]
    if args.running_header:
        build_cmd += ["--running-header", args.running_header]
    if args.no_index:
        build_cmd.append("--no-index")
    if args.auto_preface:
        build_cmd.append("--auto-preface")
    if args.keep_images:
        # Pass base URL so WeasyPrint can resolve local image paths
        build_cmd += ["--base-url", pages_dir.resolve().as_uri()]
    run(build_cmd, f"Step {step_num}/{total_steps}: Build PDF")

    print(f"\nAll done! Book written to: {args.output}")
    print(f"Inspect the .html output at {Path(args.output).with_suffix('.html')} before distributing.")
    print(f"\nIMPORTANT: Review the HTML for any meta-commentary about scraping or assembly.")
    print(f"No such text should appear in the final book.")


if __name__ == "__main__":
    main()
