#!/usr/bin/env python3
"""
build_pdf.py — Assemble scraped Markdown pages into a PDF book.

Reads the page index produced by scrape.py and the sitemap from crawl.py,
renders each page to HTML using the book template, then converts to PDF
via WeasyPrint (primary) or pdfkit (fallback).

The table of contents is kept concise: only top-level chapters (depth 0–1)
are shown, capped at --toc-max-entries. If --target-pages is set, pages are
trimmed to low-value content to approach that approximate PDF page count.

Usage:
    python build_pdf.py \
        --sitemap crawl_output/sitemap.json \
        --pages-dir crawl_output/pages/ \
        --template templates/book.html \
        --css assets/book.css \
        --output book.pdf \
        --title "My Book" \
        --target-pages 100
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

import markdown
from markdown.extensions import codehilite, fenced_code, tables, toc

MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",        # tables, footnotes, attr_list, etc.
    "markdown.extensions.codehilite",   # syntax highlighting
    "markdown.extensions.fenced_code",
    "markdown.extensions.toc",
    "markdown.extensions.admonition",
    "markdown.extensions.nl2br",
]


def md_to_html(text: str) -> tuple[str, str]:
    """Convert Markdown to HTML. Returns (html_body, first_h1_title)."""
    md = markdown.Markdown(
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs={
            "markdown.extensions.codehilite": {
                "guess_lang": False,
                "css_class": "highlight",
            },
            "markdown.extensions.toc": {
                "title": "",
                "toc_depth": 3,
            },
        },
    )
    html = md.convert(text)
    # Extract first H1 for chapter title
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
    return html, title


def build_toc_html(
    pages_meta: list[dict],
    max_depth: int = 1,
    max_entries: int = 30,
) -> str:
    """Build a concise HTML table of contents.

    Only pages at depth <= max_depth are listed, and no more than max_entries
    total. This keeps the TOC short and navigable rather than exhaustive.
    """
    lines = ["<nav id='toc'><h2>Table of Contents</h2><ol class='toc-list'>"]
    count = 0
    for i, meta in enumerate(pages_meta):
        if count >= max_entries:
            break
        depth = meta.get("depth", 0)
        if depth > max_depth:
            continue
        title = meta.get("title") or f"Chapter {count + 1}"
        # Escape HTML special characters in title
        title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        anchor = f"page-{i}"
        indent_class = f"toc-depth-{min(depth, 4)}"
        lines.append(f"<li class='{indent_class}'><a href='#{anchor}'>{title}</a></li>")
        count += 1
    lines.append("</ol></nav>")
    return "\n".join(lines)


def build_title_page(title: str, root_url: str, date: str) -> str:
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
<div id="title-page" class="title-page">
  <h1 class="book-title">{safe_title}</h1>
  <p class="book-source">Source: {root_url}</p>
  <p class="book-date">Generated: {date}</p>
</div>
<div class="page-break"></div>
"""


def load_template(template_path: Path) -> str:
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    # Minimal fallback template
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{{BOOK_TITLE}}</title>
<style>{{CSS}}</style>
</head>
<body>
{{BODY}}
</body>
</html>"""


def load_css(css_path: Path) -> str:
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    return ""


def filter_to_target_pages(pages_data: list[dict], target_pages: int) -> list[dict]:
    """Trim pages to approximate the target PDF page count.

    A rough heuristic: 1 PDF page ≈ 500 words of content. Keep the most
    content-rich pages up to the word budget, then restore original order.
    """
    words_budget = target_pages * 500
    total_words = sum(p.get("word_count", len(p["content"].split())) for p in pages_data)

    if total_words <= words_budget:
        return pages_data  # already within budget

    # Tag each page with its original position and estimated word count
    tagged = []
    for idx, page in enumerate(pages_data):
        wc = page.get("word_count") or len(page["content"].split())
        tagged.append((idx, wc, page))

    # Sort by word count descending (richest content first), then take until budget
    tagged.sort(key=lambda t: -t[1])
    kept_indices = set()
    running = 0
    for idx, wc, _ in tagged:
        if running + wc > words_budget * 1.1:  # 10% tolerance
            break
        kept_indices.add(idx)
        running += wc

    # Restore original order
    result = [page for idx, _, page in sorted(tagged, key=lambda t: t[0]) if idx in kept_indices]
    print(f"  target-pages filter: kept {len(result)}/{len(pages_data)} pages "
          f"(~{running // 500} estimated PDF pages)")
    return result


def render_full_html(
    title: str,
    root_url: str,
    pages_data: list[dict],
    template: str,
    css: str,
    toc_max_depth: int = 1,
    toc_max_entries: int = 30,
) -> str:
    date_str = datetime.now().strftime("%B %d, %Y")
    parts = [build_title_page(title, root_url, date_str)]
    toc_html = build_toc_html(pages_data, max_depth=toc_max_depth, max_entries=toc_max_entries)
    parts.append(toc_html)
    parts.append('<div class="page-break"></div>')

    for i, page in enumerate(pages_data):
        anchor = f"page-{i}"
        html_body, _ = md_to_html(page["content"])
        chapter = f"""
<section id="{anchor}" class="chapter">
{html_body}
</section>
<div class="page-break"></div>
"""
        parts.append(chapter)

    body = "\n".join(parts)
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    full_html = template.replace("{{BOOK_TITLE}}", safe_title)
    full_html = full_html.replace("{{CSS}}", css)
    full_html = full_html.replace("{{BODY}}", body)
    return full_html


def render_pdf_weasyprint(html: str, output_path: Path):
    try:
        from weasyprint import HTML, CSS
        HTML(string=html).write_pdf(str(output_path))
        return True
    except ImportError:
        return False
    except Exception as exc:
        print(f"WeasyPrint error: {exc}", file=sys.stderr)
        return False


def render_pdf_pdfkit(html: str, output_path: Path, css_path: Path | None):
    try:
        import pdfkit
        options = {
            "encoding": "UTF-8",
            "enable-local-file-access": "",
            "print-media-type": "",
            "quiet": "",
        }
        if css_path and css_path.exists():
            pdfkit.from_string(html, str(output_path), options=options, css=str(css_path))
        else:
            pdfkit.from_string(html, str(output_path), options=options)
        return True
    except ImportError:
        return False
    except Exception as exc:
        print(f"pdfkit error: {exc}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Build a PDF book from scraped pages.")
    parser.add_argument("--sitemap", required=True, help="Path to sitemap.json")
    parser.add_argument("--pages-dir", required=True, help="Directory with scraped .md files")
    parser.add_argument("--template", default="templates/book.html", help="HTML template file")
    parser.add_argument("--css", default="assets/book.css", help="CSS stylesheet file")
    parser.add_argument("--output", default="book.pdf", help="Output PDF filename")
    parser.add_argument("--title", default="", help="Book title (defaults to site title from sitemap)")
    parser.add_argument("--backend", choices=["weasyprint", "pdfkit", "auto"], default="auto")
    parser.add_argument("--html-only", action="store_true", help="Output HTML only, skip PDF rendering")
    parser.add_argument(
        "--target-pages", type=int, default=0,
        help="Approximate target PDF page count. Trims low-value pages to approach this count."
    )
    parser.add_argument(
        "--toc-max-depth", type=int, default=1,
        help="Maximum chapter depth shown in the table of contents (default: 1)"
    )
    parser.add_argument(
        "--toc-max-entries", type=int, default=30,
        help="Maximum number of entries in the table of contents (default: 30)"
    )
    args = parser.parse_args()

    sitemap_path = Path(args.sitemap)
    pages_dir = Path(args.pages_dir)
    template_path = Path(args.template)
    css_path = Path(args.css)
    output_path = Path(args.output)

    if not sitemap_path.exists():
        print(f"ERROR: sitemap not found: {sitemap_path}", file=sys.stderr)
        sys.exit(1)

    sitemap = json.loads(sitemap_path.read_text())
    index_path = pages_dir / "_index.json"
    if not index_path.exists():
        print(f"ERROR: page index not found: {index_path}", file=sys.stderr)
        sys.exit(1)

    index = json.loads(index_path.read_text())
    root_url = sitemap.get("root_url", "")
    book_title = args.title or sitemap.get("root_url", "Website Book")

    print(f"Assembling book from {len(index)} pages...")

    pages_data = []
    for i, record in enumerate(index):
        if record.get("error"):
            continue
        md_file = pages_dir / record["filename"]
        if not md_file.exists():
            continue
        content = md_file.read_text(encoding="utf-8")
        pages_data.append({
            "title": record.get("title", ""),
            "depth": record.get("depth", 0),
            "url": record.get("url", ""),
            "word_count": record.get("word_count", 0),
            "content": content,
            "_original_index": i,
        })

    print(f"  {len(pages_data)} pages with content (skipped {len(index) - len(pages_data)} errors/missing)")

    # Apply target-pages filtering if requested
    if args.target_pages > 0:
        pages_data = filter_to_target_pages(pages_data, args.target_pages)

    template = load_template(template_path)
    css = load_css(css_path)

    html = render_full_html(
        book_title, root_url, pages_data, template, css,
        toc_max_depth=args.toc_max_depth,
        toc_max_entries=args.toc_max_entries,
    )

    html_path = output_path.with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    print(f"  HTML written: {html_path} ({html_path.stat().st_size // 1024} KB)")

    if args.html_only:
        print("Done (HTML only mode).")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = False
    if args.backend in ("weasyprint", "auto"):
        print("  Rendering PDF via WeasyPrint...")
        success = render_pdf_weasyprint(html, output_path)

    if not success and args.backend in ("pdfkit", "auto"):
        print("  WeasyPrint unavailable or failed, trying pdfkit...")
        success = render_pdf_pdfkit(html, output_path, css_path)

    if success:
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"\nPDF written: {output_path} ({size_mb:.2f} MB)")
    else:
        print("\nERROR: Could not render PDF. HTML saved as fallback.")
        print("Install WeasyPrint: pip install weasyprint")
        print("Or install pdfkit + wkhtmltopdf: pip install pdfkit && apt-get install wkhtmltopdf")
        sys.exit(1)


if __name__ == "__main__":
    main()
