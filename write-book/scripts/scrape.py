#!/usr/bin/env python3
"""
scrape.py — Content scraper for crawled pages.

Reads a sitemap JSON produced by crawl.py, fetches each page,
extracts the main content, and saves it as Markdown preserving
headings, lists, code blocks, bold/italic, tables, and blockquotes.

By default:
  - HTML comments are stripped
  - Comment sections (Disqus, WordPress, etc.) are removed
  - E-commerce, testimonial, forum, and FAQ elements are stripped
  - Legal / account pages (privacy, terms, gdpr, cookies, imprint, about, login, signup) are excluded
  - "In Other Languages" navigation tab rows are stripped via CSS selectors
  - Site CTAs and upsells are stripped via regex ("Tired of reading?", "Get the book", etc.)
  - [code]/[/code] artifacts are converted to fenced code blocks
  - "Your browser does not support HTML video" lines are removed
  - Empty widget labels (Complexity:, Popularity:, Vote counts) are removed
  - Orphan sidebar/navigation file-tree lines are removed
  - Multi-language sales banners are removed
  - External links are replaced with their link text (URL dropped)
  - Images are stripped by default; use --keep-images to preserve image references
  - The leading H1 in scraped body is deduplicated (it is written once in frontmatter)
  - Pages with fewer than --min-words words are skipped as low-value
  - Pages whose URL matches --exclude are skipped

Usage:
    python scrape.py --sitemap sitemap.json --output pages/
    python scrape.py --sitemap sitemap.json --output pages/ \\
                     --main-selector "article.content" --delay 0.3
    python scrape.py --sitemap sitemap.json --output pages/ \\
                     --exclude "(sale|pricing|testimonial|faq|forum)" \\
                     --keep-external-links --keep-images --min-words 200
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import html2text
import requests
from bs4 import BeautifulSoup, Comment, Tag
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

# Elements to strip before conversion (navigation, ads, comment sections, etc.)
NOISE_SELECTORS = [
    # Layout chrome
    "nav", "header", "footer", "aside",
    ".nav", ".navbar", ".sidebar", ".toc",
    ".breadcrumb", ".pagination", ".cookie-banner",
    ".advertisement", ".ad", "[aria-hidden='true']",
    "script", "style", "noscript",
    # Comment / community sections
    "#comments", ".comments", ".comment-section", ".comment-list",
    ".comments-area", ".comment-respond", ".comment-form",
    "[id*='disqus']", "[class*='disqus']",
    ".utterances", ".giscus",
    "[id='respond']", ".wp-comment-cookies-consent",
    # Vote / follow widgets
    "[class*='vote']", "[id*='vote']",
    "[class*='follow']", "[id*='follow']",
    ".like-button", ".share-button", ".social-share",
    # UserEcho / community forum widgets
    "[class*='userecho']", "[id*='userecho']",
    ".ue-widget", ".ue_widget",
    "[class*='forum']", "[id*='forum']",
    ".community-widget",
    # Testimonials / reviews
    ".testimonials", ".testimonial", ".testimonials-section",
    ".reviews", ".review-section", ".customer-reviews",
    "[class*='testimonial']", "[id*='testimonial']",
    # E-commerce / pricing
    ".pricing", ".price-table", ".pricing-table",
    ".checkout", ".buy-now", ".purchase-section",
    ".sale-banner", ".promo-banner", ".offer-banner",
    "[class*='pricing']", "[id*='pricing']",
    # CTA / upsell blocks
    ".cta", ".cta-block", ".cta-section",
    "[class*='cta-']", "[id*='cta-']",
    ".upsell", "[class*='upsell']", "[id*='upsell']",
    ".buy-box", ".purchase-box", ".get-book",
    "[class*='buy-box']", "[class*='purchase-box']",
    # "In Other Languages" navigation tabs
    ".language-tabs", ".lang-tabs",
    "[class*='language-tab']", "[class*='lang-tab']",
    ".in-other-languages", "[class*='other-languages']",
    ".available-in", "[class*='available-in']",
    ".translations-list", "[class*='translation']",
    # Language / regional sales banners
    ".language-notice", ".translation-notice",
    "[class*='language-banner']", "[class*='lang-notice']",
    # Author bios / social promo blocks
    ".author-bio", ".author-info", ".author-card",
    ".social-links", ".newsletter-signup",
    "[class*='newsletter']",
    # Media fallback containers
    ".video-fallback", "[class*='video-placeholder']",
    # Misc noise
    ".cookie-consent", ".gdpr-notice", ".privacy-notice",
    ".back-to-top", "[class*='back-to-top']",
    ".related-posts", ".related-articles",
    "[class*='related']",
]

# Regex to match external Markdown links: [text](http://...)
_EXTERNAL_LINK_RE = re.compile(r'\[([^\]]+)\]\((https?://[^)]+)\)')

# Patterns to clean from Markdown output after HTML→Markdown conversion
_MD_CLEANUP_PATTERNS = [
    # [code] and [/code] tags left over from BBCode / forum-style markup
    (re.compile(r'\[/?code\]', re.IGNORECASE), ''),
    # (/sendy/form) and similar form link artifacts in parentheses
    (re.compile(r'\(/[a-z0-9_/-]+/form[^)]*\)', re.IGNORECASE), ''),
    # "Your browser does not support HTML video." line
    (re.compile(r'Your browser does not support HTML video\.?\s*\n?', re.IGNORECASE), ''),
    # Empty widget labels: "Complexity:" or "Popularity:" with nothing after
    (re.compile(r'^(Complexity|Popularity|Difficulty|Rating)\s*:\s*$', re.MULTILINE | re.IGNORECASE), ''),
    # Vote widget text: "Vote __ 0 __ 0 Undo __ Follow" style
    (re.compile(r'Vote\s+_+\s*\d*\s*_+\s*\d*\s*(Undo)?\s*_+\s*(Follow)?\s*\n?', re.IGNORECASE), ''),
    # Show next review / pagination controls
    (re.compile(r'Show next review\s*\n?', re.IGNORECASE), ''),
    (re.compile(r'Add a new one\s*\n?', re.IGNORECASE), ''),
    (re.compile(r'by UserEcho\s*\n?', re.IGNORECASE), ''),
    # "N month(s) ago • updated" forum timestamps
    (re.compile(r'\d+\s+months?\s+ago\s*[•·]\s*updated\s*\n?', re.IGNORECASE), ''),
    # Multi-language sales banners
    (re.compile(
        r'(This (product|book|course) is (currently )?only available in English\.?\s*\n?'
        r'|Этот продукт доступен только на английском\.?\s*\n?'
        r'|このプロダクトは英語のみです\.?\s*\n?'
        r'|이 제품은 영어로만 제공됩니다\.?\s*\n?'
        r'|此产品仅提供英文版\.?\s*\n?)',
        re.IGNORECASE
    ), ''),
    # "In Other Languages" tab row artifacts
    (re.compile(r'^In Other Languages\s*\n?', re.MULTILINE | re.IGNORECASE), ''),
    (re.compile(r'^Available in:.*?\n?', re.MULTILINE | re.IGNORECASE), ''),
    # Site CTAs / upsells
    (re.compile(r'Tired of reading\?.*?\n', re.IGNORECASE | re.DOTALL), ''),
    (re.compile(r'(Get|Download|Buy)\s+(the\s+)?(book|course|ebook|pdf)\s+(now|today|here)\.?\s*\n?', re.IGNORECASE), ''),
    (re.compile(r'(Check out|Read)\s+(our|the)\s+(free|new|full)\s+.*?course.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'\*\*(Buy|Purchase|Order)\s+(now|today)\*\*.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Spring SALE.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Summer SALE.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Money-back guarantee.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Buy as a gift.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'(Add to cart|Checkout|Purchase)\s*\n?', re.IGNORECASE), ''),
    (re.compile(r'Can I buy (on Amazon|this book).*?\n?', re.IGNORECASE), ''),
    # Author chat / social promo
    (re.compile(r'P\.?S\.?\s+Track me on (Facebook|Twitter|Instagram|social media).*?\n?', re.IGNORECASE), ''),
    (re.compile(r'(Follow|Join) me on (Facebook|Twitter|Instagram|social media).*?\n?', re.IGNORECASE), ''),
    # "Was this page helpful?" site chrome
    (re.compile(r'Was this (page|article|post)\s+helpful\?.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Share this (page|post|article).*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Edit this page.*?\n?', re.IGNORECASE), ''),
    # URL-only lines (bare http links on their own line, no surrounding prose)
    (re.compile(r'^\s*https?://\S+\s*$', re.MULTILINE), ''),
    # Breadcrumb URL slugs in parentheses: (refactoring.guru/design-patterns/strategy)
    (re.compile(r'\([a-z0-9.-]+\.[a-z]{2,}/[a-z0-9/_-]+\)', re.IGNORECASE), ''),
    # Trailing whitespace on lines
    (re.compile(r'[ \t]+$', re.MULTILINE), ''),
]

# Navigation sidebar artifacts: bare indented file-tree lines
_NAV_TREE_RE = re.compile(
    r'^(?:Navigation|Intro|buttons?|Button|MacOSButton|WindowsButton|LinuxButton'
    r'|Component|Factory|Abstract|Concrete|Client|Context|State|Strategy'
    r'|Observer|Subject|Decorator|Wrapper|Singleton|Prototype|Builder'
    r'|Adapter|Bridge|Composite|Facade|Flyweight|Proxy|Command|Iterator'
    r'|Mediator|Memento|Template|Visitor|Chain)\s*$',
    re.MULTILINE
)

# URL patterns for pages that should be excluded from a book.
# These cover legal, account, sales, community, and navigation noise.
_DEFAULT_EXCLUDE_URL_PATTERNS = [
    # Legal / compliance
    r'/(privacy|privacy-policy)',
    r'/(terms|terms-of-service|terms-of-use|tos)',
    r'/(legal|disclaimer|imprint)',
    r'/(gdpr|cookies|cookie-policy)',
    # Account / auth
    r'/(login|logout|sign-?in|sign-?up|signup|register|account|profile|dashboard)',
    r'/(cart|basket|wishlist)',
    # About / personal
    r'/(about|about-us|about-me)',
    # E-commerce / sales
    r'/(sale|spring-sale|summer-sale|discount|promo|coupon)',
    r'/(pricing|price|buy|purchase|checkout|order|gift|amazon)',
    r'/(refund|money-back|guarantee)',
    r'/(testimonial|review|customer)',
    r'/(faq|payment|payment-method)',
    r'/(forum|community|userecho)',
    r'/(newsletter|subscribe|sendy)',
    r'/(search|tag|category|author)/',
]


def configure_html2text(keep_images: bool = False) -> html2text.HTML2Text:
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = not keep_images  # preserve image refs when --keep-images is set
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


def strip_html_comments(element: Tag) -> Tag:
    """Remove all HTML comment nodes (<!-- ... -->) from the element tree."""
    for comment in element.find_all(text=lambda text: isinstance(text, Comment)):
        comment.extract()
    return element


def strip_external_links(md: str, root_domain: str | None = None) -> str:
    """Replace external Markdown links with their link text, dropping the URL."""
    def replace_link(m: re.Match) -> str:
        text, url = m.group(1), m.group(2)
        if root_domain and root_domain in url:
            return m.group(0)
        return text

    return _EXTERNAL_LINK_RE.sub(replace_link, md)


def clean_markdown(md: str) -> str:
    """Apply post-conversion cleanup patterns to Markdown text."""
    for pattern, replacement in _MD_CLEANUP_PATTERNS:
        md = pattern.sub(replacement, md)
    # Remove orphan navigation sidebar lines
    md = _NAV_TREE_RE.sub('', md)
    # Collapse runs of 3+ blank lines to 2
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()


def strip_leading_h1(md: str, title: str) -> str:
    """Remove the first H1 from the Markdown body if it duplicates the page title.

    The scraper writes '# Title' as a frontmatter header, so the same heading
    appearing again at the top of the scraped body produces a duplicate.
    """
    lines = md.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('# '):
            # Always remove the first H1 — it is re-added as the chapter header
            rest = '\n'.join(lines[i + 1:])
            return rest.lstrip('\n')
    return md


def is_excluded_url(url: str, exclude_re: re.Pattern | None = None) -> bool:
    """Return True if the URL matches an exclusion pattern."""
    if exclude_re and exclude_re.search(url):
        return True
    for pat in _DEFAULT_EXCLUDE_URL_PATTERNS:
        if re.search(pat, url, re.IGNORECASE):
            return True
    return False


def count_words(text: str) -> int:
    return len(text.split())


def html_to_markdown(html_fragment: str, keep_images: bool = False) -> str:
    converter = configure_html2text(keep_images=keep_images)
    md = converter.handle(html_fragment)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def scrape_page(
    url: str,
    session: requests.Session,
    main_selector: str | None = None,
    no_verify_ssl: bool = False,
    root_domain: str | None = None,
    keep_external_links: bool = False,
    keep_images: bool = False,
    min_words: int = 150,
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
    main = strip_html_comments(main)
    main = strip_noise(main)
    markdown = html_to_markdown(str(main), keep_images=keep_images)

    # Drop external link URLs, keeping only the visible text
    if not keep_external_links:
        markdown = strip_external_links(markdown, root_domain)

    # Remove leading H1 duplicate (title is written in frontmatter)
    markdown = strip_leading_h1(markdown, title)

    # Apply post-conversion cleanup (CTAs, nav noise, etc.)
    markdown = clean_markdown(markdown)

    word_count = count_words(markdown)
    if word_count < min_words:
        return {
            "error": f"Sparse page ({word_count} words, min {min_words})",
            "markdown": "",
            "sparse": True,
        }

    return {
        "title": title,
        "meta_description": meta_desc,
        "url": resp.url,
        "markdown": markdown,
        "word_count": word_count,
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
    parser.add_argument(
        "--keep-external-links", action="store_true",
        help="Keep external link URLs in output (default: strip URLs, keep link text only)"
    )
    parser.add_argument(
        "--keep-images", action="store_true",
        help="Preserve image references (![alt](url)) in Markdown output. "
             "By default images are stripped. Use with fetch_images.py to download "
             "and filter images after scraping."
    )
    parser.add_argument(
        "--min-words", type=int, default=150,
        help="Minimum word count to include a page (default: 150; lower = include sparser pages)"
    )
    parser.add_argument(
        "--exclude", default=None,
        help="Regex: skip pages whose URL matches this pattern (e.g. 'sale|pricing|faq|testimonial'). "
             "Applied in addition to built-in exclusions."
    )
    parser.add_argument(
        "--no-builtin-excludes", action="store_true",
        help="Disable built-in URL exclusion patterns (e-commerce, legal, account, testimonials, forums). "
             "Use when the site you are scraping legitimately has these URL segments."
    )
    args = parser.parse_args()

    sitemap_path = Path(args.sitemap)
    if not sitemap_path.exists():
        print(f"ERROR: sitemap file not found: {sitemap_path}", file=sys.stderr)
        sys.exit(1)

    sitemap = json.loads(sitemap_path.read_text())
    pages = sitemap.get("pages", [])
    root_url = sitemap.get("root_url", "")
    root_domain = urlparse(root_url).netloc if root_url else None

    exclude_re = re.compile(args.exclude, re.IGNORECASE) if args.exclude else None

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    if args.keep_images:
        print("  --keep-images enabled: image references will be preserved in Markdown output.")
        print("  Run fetch_images.py after scraping to download and filter images.")

    index_records = []
    errors = []
    sparse_skipped = 0
    excluded_url = 0

    for i, page in enumerate(tqdm(pages, desc="Scraping", unit="page")):
        url = page.get("url", "")

        # URL-based exclusion (built-in + user-supplied)
        if not args.no_builtin_excludes and is_excluded_url(url, exclude_re):
            excluded_url += 1
            tqdm.write(f"  SKIP (excluded URL) {url}")
            index_records.append({
                "index": i,
                "url": url,
                "title": page.get("title", ""),
                "filename": safe_filename(url, i),
                "depth": page.get("depth", 0),
                "error": "excluded: URL pattern matched",
            })
            continue
        elif args.no_builtin_excludes and exclude_re and exclude_re.search(url):
            excluded_url += 1
            tqdm.write(f"  SKIP (excluded URL) {url}")
            index_records.append({
                "index": i,
                "url": url,
                "title": page.get("title", ""),
                "filename": safe_filename(url, i),
                "depth": page.get("depth", 0),
                "error": "excluded: URL pattern matched",
            })
            continue

        result = scrape_page(
            url, session,
            main_selector=args.main_selector,
            no_verify_ssl=args.no_verify_ssl,
            root_domain=root_domain,
            keep_external_links=args.keep_external_links,
            keep_images=args.keep_images,
            min_words=args.min_words,
        )

        filename = safe_filename(url, i)
        filepath = out_dir / filename

        if result.get("sparse"):
            sparse_skipped += 1
            tqdm.write(f"  SKIP (sparse) {url} — {result['error']}")
            index_records.append({
                "index": i,
                "url": url,
                "title": page.get("title", ""),
                "filename": filename,
                "depth": page.get("depth", 0),
                "error": result["error"],
            })
            time.sleep(args.delay)
            continue

        if result["error"]:
            errors.append({"url": url, "error": result["error"]})
            tqdm.write(f"  ERROR {url} — {result['error']}")
            filepath.write_text(f"# Error\n\nFailed to scrape: {url}\n\nReason: {result['error']}\n")
        else:
            title = result["title"] or page.get("title", "Untitled")
            # Write title once; the H1 duplicate has already been stripped from the body
            front = f"# {title}\n\n"
            if result["meta_description"]:
                front += f"> {result['meta_description']}\n\n"
            # Source URL omitted from body — stored in _index.json for traceability
            filepath.write_text(front + result["markdown"] + "\n")

        index_records.append({
            "index": i,
            "url": url,
            "title": result.get("title") or page.get("title", ""),
            "filename": filename,
            "depth": page.get("depth", 0),
            "word_count": result.get("word_count", 0),
            "error": result.get("error"),
        })

        time.sleep(args.delay)

    # Write index
    index_path = out_dir / "_index.json"
    index_path.write_text(json.dumps(index_records, indent=2, ensure_ascii=False))

    ok = sum(1 for r in index_records if not r.get("error"))
    print(f"\nScraped {ok}/{len(pages)} pages successfully.")
    print(f"  Excluded (URL pattern): {excluded_url}")
    print(f"  Skipped (sparse/low-value): {sparse_skipped}")
    print(f"  Errors: {len(errors)}")
    print(f"Files saved to: {out_dir}")
    if args.keep_images:
        print(f"\nImages preserved in Markdown. Next step: run fetch_images.py to download:")
        print(f"  python scripts/fetch_images.py --pages-dir {out_dir} --images-dir crawl_output/images/ --root-url <URL>")
    else:
        print(f"\nNext step: inspect a sample before post-processing:")
        print(f"  python scripts/inspect_sample.py --pages-dir {out_dir} --n 5")
    if errors:
        print(f"Errors logged; see {index_path} for details.")


if __name__ == "__main__":
    main()
