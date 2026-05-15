#!/usr/bin/env python3
"""
postprocess.py — Deep cleanup and deduplication for scraped Markdown pages.

Runs after scrape.py and before the formatter agent / build_pdf.py.
Handles problems that require reading full file content or comparing
multiple files against each other.

Operations:
  --deduplicate        Detect and suppress near-duplicate pages (> 70% text overlap)
  --collapse-language-stubs
                       Merge per-language catalog stubs into one representative page
  --move-code-appendix Tag code-heavy pages (> 60% code) for appendix placement
  --url-to-footnotes   Convert bare inline URLs to Markdown footnotes
  --strip-ctas         Strip residual CTA/upsell patterns not caught by scrape.py
  --min-content-words  Mark pages below this word count as suppress:true

Usage:
    python postprocess.py --pages-dir pages/ --deduplicate --url-to-footnotes
    python postprocess.py --pages-dir pages/ \\
        --deduplicate --collapse-language-stubs --move-code-appendix \\
        --url-to-footnotes --strip-ctas --min-content-words 150
"""

import argparse
import json
import re
import sys
from pathlib import Path
from difflib import SequenceMatcher


# Regex to find bare http(s) URLs in body text (not already inside a Markdown link)
_BARE_URL_RE = re.compile(
    r'(?<!\()(?<!\[)\b(https?://[^\s\)\]\'"<>]+)',
    re.IGNORECASE
)

# Languages whose stub catalog pages should be collapsed
_LANGUAGE_NAMES = [
    "swift", "typescript", "java", "python", "php", "ruby", "rust",
    "go", "c-sharp", "csharp", "kotlin", "scala", "dart", "lua",
    "javascript", "cpp", "c-plus-plus",
]

_LANGUAGE_SLUG_RE = re.compile(
    r'/(' + '|'.join(_LANGUAGE_NAMES) + r')/?$',
    re.IGNORECASE
)

# CTA/upsell patterns to strip during post-processing
# These are a second pass for patterns that scrape.py may have missed,
# especially multi-line upsell blocks that only become visible after
# HTML→Markdown conversion.
_CTA_PATTERNS = [
    (re.compile(r'Tired of reading\?.*?(?=\n\n|\Z)', re.IGNORECASE | re.DOTALL), ''),
    (re.compile(r'(Get|Download|Buy)\s+(the\s+)?(book|course|ebook|pdf)\s+(now|today|here)\.?\s*\n?', re.IGNORECASE), ''),
    (re.compile(r'Spring (SALE|Sale).*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Summer (SALE|Sale).*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Money-back guarantee.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Buy as a gift.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'(Add to cart|Checkout|Purchase)\s*\n?', re.IGNORECASE), ''),
    (re.compile(r'Can I buy (on Amazon|this book).*?\n?', re.IGNORECASE), ''),
    (re.compile(r'How is this better than ChatGPT.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Is it on Amazon.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'P\.?S\.?\s+Track me on (Facebook|Twitter|Instagram).*?\n?', re.IGNORECASE), ''),
    (re.compile(r'(Follow|Join) me on (Facebook|Twitter|Instagram).*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Hi,?\s+I\'?m [A-Z][a-z]+,?\s+(I\'?ve been|I\'?m a).*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Was this (page|article|post)\s+helpful\?.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Share this (page|post|article).*?\n?', re.IGNORECASE), ''),
    (re.compile(r'Copyright\s*©.*?\n?', re.IGNORECASE), ''),
    (re.compile(r'All rights reserved.*?\n?', re.IGNORECASE), ''),
    # "In Other Languages" blocks that scrape.py missed (text after CSS stripping)
    (re.compile(r'In Other Languages\s*\n(\s*[-*]\s*.+\n)+', re.IGNORECASE), ''),
    (re.compile(r'^In Other Languages\s*$', re.MULTILINE | re.IGNORECASE), ''),
    # Trailing whitespace
    (re.compile(r'[ \t]+$', re.MULTILINE), ''),
]


def load_index(pages_dir: Path) -> list[dict]:
    index_path = pages_dir / "_index.json"
    if not index_path.exists():
        print(f"ERROR: _index.json not found in {pages_dir}", file=sys.stderr)
        sys.exit(1)
    return json.loads(index_path.read_text(encoding="utf-8"))


def save_index(pages_dir: Path, index: list[dict]) -> None:
    index_path = pages_dir / "_index.json"
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False))


def read_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def word_count(text: str) -> int:
    return len(text.split())


def code_ratio(text: str) -> float:
    """Return the fraction of words that are inside fenced code blocks."""
    total = word_count(text)
    if total == 0:
        return 0.0
    code_words = sum(
        word_count(block)
        for block in re.findall(r'```.*?```', text, re.DOTALL)
    )
    return code_words / total


def text_similarity(a: str, b: str) -> float:
    """Return sequence similarity ratio between two strings (0–1)."""
    words_a = ' '.join(a.lower().split())
    words_b = ' '.join(b.lower().split())
    return SequenceMatcher(None, words_a[:4000], words_b[:4000]).ratio()


def convert_urls_to_footnotes(md: str) -> str:
    """Replace bare inline URLs with footnote references.

    Bare URLs inside body text (not inside a Markdown link already) are
    replaced with [^N] and collected into a footnote block at the end of
    the page. This cleans up the reading flow while preserving source references.
    """
    footnotes: list[str] = []
    counter = [0]  # mutable int for closure

    def replace(m: re.Match) -> str:
        url = m.group(1)
        counter[0] += 1
        footnotes.append(f"[^{counter[0]}]: {url}")
        return f"[^{counter[0]}]"

    cleaned = _BARE_URL_RE.sub(replace, md)

    if footnotes:
        cleaned = cleaned.rstrip() + "\n\n" + "\n".join(footnotes) + "\n"

    return cleaned


def strip_ctas(pages_dir: Path, index: list[dict]) -> list[dict]:
    """Apply CTA/upsell pattern stripping to all active pages.

    This is a second-pass cleanup for patterns that scrape.py may have
    missed — especially multi-line upsell blocks and author self-promotion
    that only appears as readable text after HTML→Markdown conversion.
    """
    print("  CTA/upsell stripping pass...")
    cleaned = 0
    for rec in index:
        if rec.get("error") or rec.get("suppress"):
            continue
        path = pages_dir / rec["filename"]
        text = read_file(path)
        updated = text
        for pattern, replacement in _CTA_PATTERNS:
            updated = pattern.sub(replacement, updated)
        # Collapse excess blank lines
        updated = re.sub(r'\n{3,}', '\n\n', updated).strip() + '\n'
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            cleaned += 1

    print(f"    Cleaned CTAs/upsells from {cleaned} pages")
    return index


def deduplicate(pages_dir: Path, index: list[dict], threshold: float = 0.70) -> list[dict]:
    """Suppress near-duplicate pages, keeping the longest version of each cluster."""
    print("  Deduplication pass...")
    active = [r for r in index if not r.get("error") and not r.get("suppress")]
    contents: dict[str, str] = {}
    for rec in active:
        path = pages_dir / rec["filename"]
        contents[rec["filename"]] = read_file(path)

    suppress_set: set[str] = set()
    merged_into: dict[str, str] = {}

    for i, rec_a in enumerate(active):
        if rec_a["filename"] in suppress_set:
            continue
        text_a = contents[rec_a["filename"]]
        for rec_b in active[i + 1:]:
            if rec_b["filename"] in suppress_set:
                continue
            text_b = contents[rec_b["filename"]]
            sim = text_similarity(text_a, text_b)
            if sim >= threshold:
                # Keep the longer one
                if len(text_b) > len(text_a):
                    suppress_set.add(rec_a["filename"])
                    merged_into[rec_a["filename"]] = rec_b["filename"]
                    break
                else:
                    suppress_set.add(rec_b["filename"])
                    merged_into[rec_b["filename"]] = rec_a["filename"]

    suppressed = 0
    for rec in index:
        if rec["filename"] in suppress_set:
            rec["suppress"] = True
            rec["merged_into"] = merged_into.get(rec["filename"], "")
            suppressed += 1

    print(f"    Suppressed {suppressed} near-duplicate pages")
    return index


def collapse_language_stubs(pages_dir: Path, index: list[dict], min_langs: int = 3) -> list[dict]:
    """Collapse per-language stub catalog pages into one representative page.

    Stub pages are identified by:
    1. URL ending in a known language name slug
    2. Content that is mostly a list of links with little prose

    When 3+ such stubs share the same link structure, keep the first and suppress the rest,
    adding a note that the pattern is available in multiple languages.
    """
    print("  Language stub collapse pass...")

    # Group by URL without the language suffix
    stub_groups: dict[str, list[dict]] = {}
    for rec in index:
        if rec.get("error") or rec.get("suppress"):
            continue
        url = rec.get("url", "")
        m = _LANGUAGE_SLUG_RE.search(url)
        if m:
            base_url = url[: m.start()]
            stub_groups.setdefault(base_url, []).append(rec)

    collapsed = 0
    for base_url, group in stub_groups.items():
        if len(group) < min_langs:
            continue
        # Check that all are stub-like (< 400 words, mostly links)
        stub_like = []
        for rec in group:
            text = read_file(pages_dir / rec["filename"])
            wc = word_count(text)
            link_count = len(re.findall(r'\[.+?\]\(.+?\)', text))
            if wc < 400 and link_count >= 10:
                stub_like.append(rec)

        if len(stub_like) < min_langs:
            continue

        # Sort by word count descending, keep the richest version
        stub_like.sort(key=lambda r: r.get("word_count", 0), reverse=True)
        keeper = stub_like[0]
        lang_names = []
        for rec in stub_like[1:]:
            url = rec.get("url", "")
            m = _LANGUAGE_SLUG_RE.search(url)
            if m:
                lang_names.append(m.group(1))
            rec["suppress"] = True
            rec["merged_into"] = keeper["filename"]
            collapsed += 1

        # Append a note to the keeper page
        if lang_names:
            keeper_path = pages_dir / keeper["filename"]
            text = read_file(keeper_path)
            note = (
                "\n\n---\n\n"
                f"*Also available for: {', '.join(lang_names)}. "
                "See the online edition for language-specific examples.*\n"
            )
            keeper_path.write_text(text + note, encoding="utf-8")

    print(f"    Collapsed {collapsed} language stub pages")
    return index


def tag_code_heavy(pages_dir: Path, index: list[dict], threshold: float = 0.60) -> list[dict]:
    """Tag pages where the majority of content is code blocks.

    These are candidates to move to an appendix rather than the main narrative.
    The formatter agent reads the code_heavy flag in _index.json and should also
    set xref_chapter to the name of the main chapter this code belongs to.
    """
    print("  Code-heavy page tagging pass...")
    tagged = 0
    for rec in index:
        if rec.get("error") or rec.get("suppress"):
            continue
        text = read_file(pages_dir / rec["filename"])
        if code_ratio(text) >= threshold:
            rec["code_heavy"] = True
            tagged += 1

    print(f"    Tagged {tagged} code-heavy pages (formatter agent should set xref_chapter on these)")
    return index


def apply_url_to_footnotes(pages_dir: Path, index: list[dict]) -> list[dict]:
    """Convert bare inline URLs to Markdown footnote references in all active pages."""
    print("  URL-to-footnotes pass...")
    converted = 0
    for rec in index:
        if rec.get("error") or rec.get("suppress"):
            continue
        path = pages_dir / rec["filename"]
        text = read_file(path)
        updated = convert_urls_to_footnotes(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            converted += 1

    print(f"    Converted URLs to footnotes in {converted} pages")
    return index


def suppress_short_pages(pages_dir: Path, index: list[dict], min_words: int) -> list[dict]:
    """Mark pages below min_words as suppress:true so build_pdf.py skips them."""
    print(f"  Suppressing pages with fewer than {min_words} words...")
    suppressed = 0
    for rec in index:
        if rec.get("error") or rec.get("suppress"):
            continue
        text = read_file(pages_dir / rec["filename"])
        wc = word_count(text)
        if wc < min_words:
            rec["suppress"] = True
            rec["suppress_reason"] = f"near-blank: {wc} words after cleanup"
            suppressed += 1
    print(f"    Suppressed {suppressed} near-blank pages")
    return index


def main():
    parser = argparse.ArgumentParser(
        description="Post-process scraped Markdown pages: dedup, cleanup, index prep."
    )
    parser.add_argument("--pages-dir", required=True, help="Directory with scraped .md files and _index.json")
    parser.add_argument(
        "--deduplicate", action="store_true",
        help="Detect and suppress near-duplicate pages (threshold: 70%% text overlap)"
    )
    parser.add_argument(
        "--deduplicate-threshold", type=float, default=0.70,
        help="Similarity threshold for deduplication (0–1, default: 0.70)"
    )
    parser.add_argument(
        "--collapse-language-stubs", action="store_true",
        help="Merge per-language stub catalog pages into one representative page"
    )
    parser.add_argument(
        "--min-language-stubs", type=int, default=3,
        help="Minimum number of language stubs before collapsing (default: 3)"
    )
    parser.add_argument(
        "--move-code-appendix", action="store_true",
        help="Tag code-heavy pages (>60%% code blocks) with code_heavy:true for appendix placement"
    )
    parser.add_argument(
        "--code-heavy-threshold", type=float, default=0.60,
        help="Fraction of word count in code blocks to consider a page code-heavy (default: 0.60)"
    )
    parser.add_argument(
        "--url-to-footnotes", action="store_true",
        help="Convert bare inline http:// URLs to Markdown footnote references"
    )
    parser.add_argument(
        "--strip-ctas", action="store_true",
        help="Strip residual CTA/upsell patterns from all pages (second pass after scrape.py)"
    )
    parser.add_argument(
        "--min-content-words", type=int, default=0,
        help="Suppress pages with fewer than this many words after cleanup (default: 0 = disabled)"
    )
    args = parser.parse_args()

    pages_dir = Path(args.pages_dir)
    if not pages_dir.is_dir():
        print(f"ERROR: pages directory not found: {pages_dir}", file=sys.stderr)
        sys.exit(1)

    index = load_index(pages_dir)
    print(f"Loaded {len(index)} records from _index.json")

    if args.strip_ctas:
        index = strip_ctas(pages_dir, index)

    if args.deduplicate:
        index = deduplicate(pages_dir, index, threshold=args.deduplicate_threshold)

    if args.collapse_language_stubs:
        index = collapse_language_stubs(pages_dir, index, min_langs=args.min_language_stubs)

    if args.move_code_appendix:
        index = tag_code_heavy(pages_dir, index, threshold=args.code_heavy_threshold)

    if args.url_to_footnotes:
        index = apply_url_to_footnotes(pages_dir, index)

    if args.min_content_words > 0:
        index = suppress_short_pages(pages_dir, index, args.min_content_words)

    save_index(pages_dir, index)

    active = sum(1 for r in index if not r.get("suppress") and not r.get("error"))
    suppressed = sum(1 for r in index if r.get("suppress"))
    code_heavy = sum(1 for r in index if r.get("code_heavy"))
    print(f"\nPost-processing complete.")
    print(f"  Active pages: {active}")
    print(f"  Suppressed:   {suppressed}")
    print(f"  Code-heavy:   {code_heavy}  (tagged for appendix — set xref_chapter in formatter agent)")
    print(f"  Index saved:  {pages_dir / '_index.json'}")
    print(f"\nNext: run the formatter agent, then inspect sample before building PDF.")


if __name__ == "__main__":
    main()
