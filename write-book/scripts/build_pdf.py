#!/usr/bin/env python3
"""
build_pdf.py — Assemble scraped Markdown pages into a PDF book.

Reads the page index produced by scrape.py / postprocess.py and the sitemap
from crawl.py, renders each page to HTML using the book template, then converts
to PDF via WeasyPrint (primary) or pdfkit (fallback).

Key features:
  - Full table of contents (all chapters and sections, not just top-level)
  - Alphabetical back-of-book index from H2+ headings (curated by default)
  - Running header normalization via --running-header
  - Blank and near-blank page suppression (respects suppress:true in _index.json)
  - Code-heavy page relegation to appendix (respects code_heavy:true)
  - Cross-references from appendix pages back to their main chapter
  - URL footnote rendering via Python-Markdown footnotes extension
  - No double page-breaks: section breaks use page-break-before only
  - Local image path resolution for images downloaded by fetch_images.py

Page-break strategy (avoids blank pages):
  Every section element uses CSS page-break-before: always.
  Do NOT add <div class="page-break"> between sections — that stacks two
  consecutive breaks and creates blank pages. The .page-break div is reserved
  for transitions where the following element has no page-break-before rule.

IMPORTANT: Always pass --no-auto-preface and write your own Preface as a .md file.
The auto-preface is off by default. If you enable it, ensure it contains no
meta-commentary about scraping, crawling, or PDF generation.

Usage:
    python build_pdf.py \\
        --sitemap crawl_output/sitemap.json \\
        --pages-dir crawl_output/pages/ \\
        --template templates/book.html \\
        --css assets/book.css \\
        --output book.pdf \\
        --title "My Book" \\
        --toc-max-depth 3 \\
        --toc-max-entries 300 \\
        --no-auto-preface \\
        --running-header "My Book" \\
        --target-pages 100
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

import markdown as md_lib
from markdown.extensions import codehilite, fenced_code, tables, toc

MARKDOWN_EXTENSIONS = [
    "markdown.extensions.extra",        # tables, footnotes, attr_list, etc.
    "markdown.extensions.codehilite",   # syntax highlighting
    "markdown.extensions.fenced_code",
    "markdown.extensions.toc",
    "markdown.extensions.admonition",
    "markdown.extensions.nl2br",
    "markdown.extensions.footnotes",    # [^N]: footnote support
]

# Index entries to exclude even when --generate-index is on.
# These are generic section labels that add noise but no navigational value.
_GENERIC_INDEX_TERMS = {
    "example", "examples", "overview", "introduction", "summary",
    "conclusion", "usage", "see also", "note", "notes", "tip", "tips",
    "warning", "warnings", "references", "further reading", "next steps",
    "prerequisites", "requirements", "installation", "setup", "configuration",
    "troubleshooting", "faq", "frequently asked questions",
}


def md_to_html(text: str) -> tuple[str, str]:
    """Convert Markdown to HTML. Returns (html_body, first_h1_title)."""
    md = md_lib.Markdown(
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
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
    return html, title


def extract_headings(html: str, min_level: int = 2, max_level: int = 3) -> list[dict]:
    """Extract headings from rendered HTML for index generation."""
    headings = []
    for m in re.finditer(r"<h([2-6])[^>]*>(.*?)</h\1>", html, re.DOTALL | re.IGNORECASE):
        level = int(m.group(1))
        if min_level <= level <= max_level:
            text = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            if text:
                headings.append({"text": text, "level": level})
    return headings


def build_toc_html(
    pages_meta: list[dict],
    max_depth: int = 3,
    max_entries: int = 300,
) -> str:
    """Build a full HTML table of contents.

    Lists every chapter and section up to max_depth and max_entries.
    Chapters in the appendix group are listed under a separate heading.
    Uses page-break-before in CSS — do not add a page-break div after this element.
    """
    lines = ["<nav id='toc'><h2>Table of Contents</h2><ol class='toc-list'>"]
    count = 0
    in_appendix = False

    for i, meta in enumerate(pages_meta):
        if count >= max_entries:
            break
        depth = meta.get("depth", 0)
        if depth > max_depth:
            continue

        # Insert appendix separator
        if meta.get("code_heavy") and not in_appendix:
            in_appendix = True
            lines.append("</ol><h3 class='toc-section-label'>Appendix</h3><ol class='toc-list toc-appendix'>")

        title = meta.get("title") or f"Chapter {count + 1}"
        title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        anchor = f"page-{i}"
        indent_class = f"toc-depth-{min(depth, 4)}"
        lines.append(f"<li class='{indent_class}'><a href='#{anchor}'>{title}</a></li>")
        count += 1

    lines.append("</ol></nav>")
    return "\n".join(lines)


def build_index_html(
    all_headings: list[dict],
    max_entries: int = 0,
    exclude_terms: set | None = None,
) -> str:
    """Build an alphabetical back-of-book index from collected headings.

    Headings are sorted alphabetically, grouped by first letter, and rendered
    as a two-column index section at the end of the book.

    Generic section labels (example, overview, note, etc.) are filtered out
    because they add noise without helping readers navigate.

    The index section uses page-break-before in CSS.
    """
    if not all_headings:
        return ""

    filter_set = _GENERIC_INDEX_TERMS.copy()
    if exclude_terms:
        filter_set |= {t.lower().strip() for t in exclude_terms}

    seen: set[str] = set()
    unique: list[dict] = []
    for h in all_headings:
        key = h["text"].lower().strip()
        # Filter generic terms and very short entries
        if key in filter_set or len(key) <= 2:
            continue
        if key not in seen:
            seen.add(key)
            unique.append(h)

    if not unique:
        return ""

    unique.sort(key=lambda h: h["text"].lower())

    if max_entries and len(unique) > max_entries:
        print(
            f"  Index: trimmed from {len(unique)} to {max_entries} entries "
            f"(--max-index-entries). Consider --no-index if still noisy."
        )
        unique = unique[:max_entries]

    parts = [
        "<section id='book-index' class='book-index'>",
        "<h1>Index</h1>",
        "<div class='index-columns'>",
    ]

    current_letter = ""
    for h in unique:
        first = h["text"][0].upper()
        if first != current_letter:
            current_letter = first
            parts.append(f"<div class='index-letter'>{current_letter}</div>")
        text = h["text"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        indent = "index-sub" if h["level"] > 2 else ""
        parts.append(f"<div class='index-entry {indent}'>{text}</div>")

    parts += ["</div>", "</section>"]
    return "\n".join(parts)


def build_title_page(title: str, root_url: str, date: str, running_header: str) -> str:
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_header = running_header.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # No page-break div after this — the TOC element uses page-break-before in CSS
    return f"""
<div id="title-page" class="title-page">
  <h1 class="book-title">{safe_title}</h1>
  <p class="book-date">{date}</p>
  <!-- running-header meta consumed by CSS string-set -->
  <span class="running-header-value" style="display:none">{safe_header}</span>
</div>
"""


def build_auto_preface_html(title: str) -> str:
    """Generate a minimal placeholder preface (opt-in only, via --auto-preface).

    STRONGLY PREFER writing a real Preface as a .md file in the pages directory
    and passing --no-auto-preface (the default). A real preface speaks directly
    to the reader about audience, scope, and how to use the book.

    This placeholder contains no meta-commentary about scraping or assembly.
    """
    safe = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
<section id="auto-preface" class="chapter">
<h1>Preface</h1>
<p>This book brings together material on <em>{safe}</em>, organized for
a reader working through the subject in depth. Foundational concepts appear
before advanced applications. The appendix contains extended code listings
cross-referenced from their relevant chapters.</p>
<p>Use the table of contents for navigating by topic, and the index at the back
for locating specific terms and techniques.</p>
</section>
"""


def load_template(template_path: Path) -> str:
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
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

    Heuristic: 1 PDF page ≈ 500 words. Keep the most content-rich pages up
    to the word budget, then restore original order.
    """
    words_budget = target_pages * 500
    total_words = sum(p.get("word_count", len(p["content"].split())) for p in pages_data)

    if total_words <= words_budget:
        return pages_data

    tagged = []
    for idx, page in enumerate(pages_data):
        wc = page.get("word_count") or len(page["content"].split())
        tagged.append((idx, wc, page))

    tagged.sort(key=lambda t: -t[1])
    kept_indices = set()
    running = 0
    for idx, wc, _ in tagged:
        if running + wc > words_budget * 1.1:
            break
        kept_indices.add(idx)
        running += wc

    result = [page for idx, _, page in sorted(tagged, key=lambda t: t[0]) if idx in kept_indices]
    print(f"  target-pages filter: kept {len(result)}/{len(pages_data)} pages "
          f"(~{running // 500} estimated PDF pages)")
    return result


def render_page_section(
    page: dict,
    anchor: str,
    all_headings: list[dict],
    generate_index: bool,
) -> str:
    """Render one page to an HTML section.

    No trailing page-break div is emitted. The CSS page-break-before: always
    on .chapter handles the break before each new section. Stacking both
    page-break-after (on a .page-break div) and page-break-before (on .chapter)
    creates blank pages — use only one mechanism.
    """
    content = page["content"]

    # Prepend cross-reference if this page has one (set by formatter agent)
    xref = page.get("xref_chapter", "")
    if xref:
        safe_xref = xref.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        content = f"> **See also:** {safe_xref}\n\n" + content

    html_body, _ = md_to_html(content)

    if generate_index:
        all_headings.extend(extract_headings(html_body))

    return f"""
<section id="{anchor}" class="chapter">
{html_body}
</section>
"""


def render_full_html(
    title: str,
    root_url: str,
    pages_data: list[dict],
    template: str,
    css: str,
    toc_max_depth: int = 3,
    toc_max_entries: int = 300,
    generate_index: bool = True,
    max_index_entries: int = 0,
    running_header: str = "",
    include_auto_preface: bool = False,
    index_warn_threshold: int = 300,
) -> str:
    date_str = datetime.now().strftime("%B %d, %Y")
    effective_header = running_header or title

    parts = [build_title_page(title, root_url, date_str, effective_header)]

    # Auto-preface: only when explicitly requested AND no preface page is in content.
    # Always prefer a user-written preface .md file as the first chapter.
    if include_auto_preface:
        has_preface = any(
            re.search(r'\bpreface\b|\bintroduction\b|\bintro\b', p.get("title", ""), re.IGNORECASE)
            for p in pages_data
        )
        if not has_preface:
            parts.append(build_auto_preface_html(title))

    # TOC — CSS uses page-break-before: always so no page-break div needed before or after
    main_pages = [p for p in pages_data if not p.get("code_heavy")]
    appendix_pages = [p for p in pages_data if p.get("code_heavy")]

    toc_html = build_toc_html(
        main_pages + appendix_pages,
        max_depth=toc_max_depth,
        max_entries=toc_max_entries,
    )
    parts.append(toc_html)
    # No page-break div here: the first .chapter uses page-break-before: always

    # Collect headings for back-of-book index
    all_headings: list[dict] = []

    # Main content sections — no page-break divs between them
    for i, page in enumerate(main_pages):
        parts.append(render_page_section(
            page, f"page-{page['_original_index']}",
            all_headings, generate_index,
        ))

    # Appendix header and code-heavy pages
    if appendix_pages:
        # Build back-reference map: main chapter name → list of appendix page titles
        main_chapter_names = sorted(
            {p.get("chapter", "") for p in main_pages if p.get("chapter")},
        )

        appendix_intro = (
            "<p>The following pages contain extended code listings. "
            "They are gathered here to preserve the reading flow of the main chapters.</p>"
        )
        if main_chapter_names:
            chapter_list = ", ".join(
                f"<em>{c}</em>" for c in main_chapter_names[:8]
            )
            appendix_intro += (
                f"<p>Each listing includes a cross-reference back to its main chapter "
                f"({chapter_list}).</p>"
            )

        parts.append(
            "<section class='appendix-header chapter'>"
            "<h1>Appendix: Code Examples</h1>"
            f"{appendix_intro}"
            "</section>"
            # No page-break div: the first appendix .chapter uses page-break-before
        )
        for page in appendix_pages:
            parts.append(render_page_section(
                page, f"page-{page['_original_index']}",
                all_headings, generate_index,
            ))

    # Back-of-book index
    # The .book-index section has page-break-before: always in CSS — no page-break div needed
    if generate_index:
        if all_headings and len(all_headings) > index_warn_threshold:
            print(
                f"\n  WARNING: Index would have {len(all_headings)} entries — "
                f"likely too noisy to be useful. "
                f"Consider --no-index or --max-index-entries {index_warn_threshold}."
            )
        index_html = build_index_html(
            all_headings,
            max_entries=max_index_entries,
        )
        if index_html:
            parts.append(index_html)

    body = "\n".join(parts)
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    full_html = template.replace("{{BOOK_TITLE}}", safe_title)
    full_html = full_html.replace("{{CSS}}", css)
    full_html = full_html.replace("{{BODY}}", body)
    return full_html


def render_pdf_weasyprint(html: str, output_path: Path, base_url: str | None = None):
    try:
        from weasyprint import HTML, CSS
        html_obj = HTML(string=html, base_url=base_url)
        html_obj.write_pdf(str(output_path))
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
        "--toc-max-depth", type=int, default=3,
        help="Maximum chapter depth shown in the table of contents (default: 3)"
    )
    parser.add_argument(
        "--toc-max-entries", type=int, default=300,
        help="Maximum number of entries in the table of contents (default: 300)"
    )
    parser.add_argument(
        "--generate-index", action="store_true", default=True,
        help="Generate an alphabetical back-of-book index from H2+ headings (default: on)"
    )
    parser.add_argument(
        "--no-index", action="store_true",
        help="Disable back-of-book index generation"
    )
    parser.add_argument(
        "--max-index-entries", type=int, default=0,
        help="Cap the number of index entries (0 = no cap). Use when the index is too noisy."
    )
    parser.add_argument(
        "--index-warn-threshold", type=int, default=300,
        help="Warn if index would exceed this many entries (default: 300)"
    )
    parser.add_argument(
        "--running-header", default="",
        help="Text used as the running header on every page. Defaults to --title."
    )
    parser.add_argument(
        "--no-auto-preface", action="store_true", default=False,
        help="(Kept for backwards compatibility — auto-preface is already OFF by default. "
             "Always prefer a user-written preface .md file.)"
    )
    parser.add_argument(
        "--auto-preface", action="store_true", default=False,
        help="Generate a minimal placeholder preface if no preface page is found in content. "
             "Default OFF — write your own preface as a .md file instead. "
             "The generated preface contains no meta-commentary about scraping."
    )
    parser.add_argument(
        "--base-url", default="",
        help="Base URL for resolving local image paths in WeasyPrint. "
             "Set to the pages-dir absolute path for local image references."
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

    # Use pages_dir as base URL for WeasyPrint so local image paths resolve correctly
    base_url = args.base_url or pages_dir.resolve().as_uri()

    print(f"Assembling book from {len(index)} pages...")

    pages_data = []
    for i, record in enumerate(index):
        # Skip errored, sparse, and suppressed pages
        if record.get("error"):
            continue
        if record.get("suppress"):
            continue
        md_file = pages_dir / record["filename"]
        if not md_file.exists():
            continue
        content = md_file.read_text(encoding="utf-8")
        # Skip near-blank pages (very short content after cleanup)
        if len(content.split()) < 50:
            continue
        pages_data.append({
            "title": record.get("title", ""),
            "depth": record.get("mece_order", record.get("depth", 0)),
            "url": record.get("url", ""),
            "word_count": record.get("word_count", 0),
            "code_heavy": record.get("code_heavy", False),
            "chapter": record.get("chapter", ""),
            "xref_chapter": record.get("xref_chapter", ""),
            "content": content,
            "_original_index": i,
        })

    suppressed = sum(1 for r in index if r.get("suppress"))
    print(f"  {len(pages_data)} pages with content")
    print(f"  {suppressed} pages suppressed (near-blank, duplicate, or flagged)")
    print(f"  {sum(1 for r in index if r.get('error'))} pages with errors (skipped)")
    print(f"  {sum(1 for p in pages_data if p.get('code_heavy'))} code-heavy pages → appendix")
    xref_count = sum(1 for p in pages_data if p.get("xref_chapter"))
    if xref_count:
        print(f"  {xref_count} appendix pages have cross-references to main chapters")

    if args.target_pages > 0:
        pages_data = filter_to_target_pages(pages_data, args.target_pages)

    template = load_template(template_path)
    css = load_css(css_path)

    html = render_full_html(
        book_title, root_url, pages_data, template, css,
        toc_max_depth=args.toc_max_depth,
        toc_max_entries=args.toc_max_entries,
        generate_index=not args.no_index,
        max_index_entries=args.max_index_entries,
        running_header=args.running_header or book_title,
        include_auto_preface=args.auto_preface,
        index_warn_threshold=args.index_warn_threshold,
    )

    html_path = output_path.with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    print(f"  HTML written: {html_path} ({html_path.stat().st_size // 1024} KB)")
    print(f"\n  Inspect the HTML before building the PDF:")
    print(f"  Open {html_path} and check for blank pages, raw URLs, noise in the first few chapters.")
    print(f"  Also verify: no meta-commentary about scraping or assembly appears anywhere.")

    if args.html_only:
        print("Done (HTML only mode).")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = False
    if args.backend in ("weasyprint", "auto"):
        print("  Rendering PDF via WeasyPrint...")
        success = render_pdf_weasyprint(html, output_path, base_url=base_url)

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
