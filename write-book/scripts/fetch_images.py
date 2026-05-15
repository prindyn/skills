#!/usr/bin/env python3
"""
fetch_images.py — Download and filter images from scraped Markdown pages.

Scans the pages directory for Markdown image references (![alt](url)), applies
heuristic filtering to identify valuable images (diagrams, figures, screenshots),
downloads them to a local images directory, rewrites the .md files to use local
relative paths, and produces a manifest for manual review.

Valuable images: diagrams, architecture figures, code output screenshots,
tutorial step-by-step screenshots, charts, and illustrations that illuminate text.

Skipped images: logos, avatars, icons, banners, social media imagery, decorative
hero images, tracking pixels, and anything under --min-width pixels wide.

Usage:
    python fetch_images.py \\
        --pages-dir crawl_output/pages/ \\
        --images-dir crawl_output/images/ \\
        --root-url https://example.com

    python fetch_images.py \\
        --pages-dir crawl_output/pages/ \\
        --images-dir crawl_output/images/ \\
        --root-url https://example.com \\
        --dry-run \\
        --min-width 150 \\
        --max-size-mb 2
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; write-book-image-fetcher/1.0; "
        "+https://github.com/agentskills/write-book)"
    )
}

# URL path segments that strongly indicate a decorative/noise image
_SKIP_URL_PATTERNS = re.compile(
    r"/(logo|avatar|icon|badge|banner|hero|background|favicon|sprite|pixel"
    r"|tracking|analytics|social|share|twitter|facebook|instagram|linkedin"
    r"|youtube|promo|sale|ad|ads|coupon|affiliate|partner|sponsor"
    r"|placeholder|dummy|sample-image)[^/]*\.(png|jpg|jpeg|gif|svg|webp)$",
    re.IGNORECASE,
)

# URL path segments that suggest a valuable image
_KEEP_URL_PATTERNS = re.compile(
    r"/(diagram|figure|fig|img|image|images|assets|screenshot|output|example"
    r"|pattern|architecture|schema|chart|graph|illustration|tutorial|step"
    r"|flow|sequence|uml|class-diagram|component|structure)[^/]*\.(png|jpg|jpeg|gif|svg|webp)$",
    re.IGNORECASE,
)

# Alt text keywords that suggest decorative images
_SKIP_ALT_KEYWORDS = {
    "logo", "icon", "avatar", "photo", "picture", "banner", "badge",
    "share", "facebook", "twitter", "linkedin", "youtube", "instagram",
    "arrow", "bullet", "star", "check", "checkmark", "close", "menu",
    "search", "home", "back", "next", "prev", "previous",
}

# Alt text keywords that suggest valuable images
_KEEP_ALT_KEYWORDS = {
    "diagram", "figure", "example", "output", "screenshot", "illustration",
    "architecture", "flow", "chart", "graph", "schema", "structure", "pattern",
    "step", "result", "demo", "preview", "sequence", "uml", "class",
    "component", "interface", "model",
}

# Regex to find Markdown image references: ![alt text](url)
_MD_IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)\)')

# Image extensions considered processable
_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def classify_image(url: str, alt_text: str) -> tuple[str, str]:
    """Return (verdict, reason): 'keep' or 'skip' and why."""
    path = urlparse(url).path.lower()
    alt = alt_text.lower().strip()

    # Skip very short / non-URL paths that are likely data URIs or relative fragments
    if url.startswith("data:"):
        return "skip", "data URI"

    ext = Path(path).suffix.lower()
    if ext not in _IMAGE_EXTENSIONS and ext != "":
        return "skip", f"non-image extension: {ext}"

    # Check URL for explicit skip patterns
    if _SKIP_URL_PATTERNS.search(path):
        return "skip", f"URL matches decorative pattern"

    # Check alt text for explicit skip keywords
    alt_words = set(re.split(r"\W+", alt))
    if alt_words & _SKIP_ALT_KEYWORDS and not (alt_words & _KEEP_ALT_KEYWORDS):
        return "skip", f"alt text suggests decorative: '{alt_text}'"

    # Check URL for explicit keep patterns
    if _KEEP_URL_PATTERNS.search(path):
        return "keep", f"URL matches diagram/figure pattern"

    # Check alt text for keep keywords
    if alt_words & _KEEP_ALT_KEYWORDS:
        return "keep", f"alt text suggests valuable: '{alt_text}'"

    # Neutral: keep by default if a substantive alt text exists
    if len(alt) > 5 and not alt_words <= _SKIP_ALT_KEYWORDS:
        return "keep", f"has substantive alt text: '{alt_text}'"

    return "skip", "no clear signal of value (no alt text or decorative alt)"


def check_dimensions(image_path: Path, min_width: int) -> tuple[bool, str]:
    """Return (ok, reason). Requires Pillow. Returns True if Pillow not available."""
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            w, h = img.size
            if w < min_width:
                return False, f"too narrow: {w}px < {min_width}px (likely icon)"
            if h > 0 and w / h > 6:
                return False, f"banner-shaped: {w}×{h} (aspect ratio {w/h:.1f}:1)"
        return True, f"{w}×{h}px"
    except ImportError:
        return True, "Pillow not installed — dimension check skipped"
    except Exception as exc:
        return True, f"dimension check failed: {exc}"


def safe_image_filename(url: str, index: int) -> str:
    path = urlparse(url).path
    name = Path(path).name
    name = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
    if not name or name == "_":
        name = f"image_{index}"
    ext = Path(name).suffix.lower()
    if ext not in _IMAGE_EXTENSIONS:
        ext = ".png"
        name = name + ext
    stem = Path(name).stem[:80]
    return f"{index:04d}_{stem}{ext}"


def download_image(
    url: str,
    dest_path: Path,
    session: requests.Session,
    max_size_bytes: int,
    no_verify_ssl: bool = False,
) -> tuple[bool, str]:
    """Download image to dest_path. Returns (success, message)."""
    try:
        resp = session.get(url, timeout=20, stream=True, verify=not no_verify_ssl)
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "")
        if not any(t in content_type for t in ["image/", "svg", "octet-stream"]):
            return False, f"non-image Content-Type: {content_type}"

        size = 0
        chunks = []
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                size += len(chunk)
                if size > max_size_bytes:
                    return False, f"too large: > {max_size_bytes // (1024*1024)} MB"
                chunks.append(chunk)

        dest_path.write_bytes(b"".join(chunks))
        return True, f"{size // 1024} KB"

    except requests.RequestException as exc:
        return False, str(exc)


def resolve_url(url: str, root_url: str, page_url: str = "") -> str:
    """Resolve a potentially relative image URL to an absolute URL."""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    if url.startswith("//"):
        scheme = urlparse(root_url).scheme
        return f"{scheme}:{url}"
    base = page_url or root_url
    return urljoin(base, url)


def process_pages(
    pages_dir: Path,
    images_dir: Path,
    root_url: str,
    session: requests.Session,
    min_width: int,
    max_size_bytes: int,
    delay: float,
    dry_run: bool,
    no_verify_ssl: bool,
) -> list[dict]:
    """Scan all .md files, filter images, download keepers, rewrite references."""
    manifest = []
    image_index = 0
    downloaded_urls: dict[str, str] = {}  # url → local filename (deduplicate)

    md_files = sorted(pages_dir.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {pages_dir}", file=sys.stderr)
        return manifest

    print(f"Scanning {len(md_files)} .md files for images...")

    for md_file in md_files:
        if md_file.name == "_index.json":
            continue

        content = md_file.read_text(encoding="utf-8")
        matches = list(_MD_IMAGE_RE.finditer(content))

        if not matches:
            continue

        modified = content
        file_changed = False

        for m in matches:
            alt_text = m.group(1)
            img_url_raw = m.group(2)
            img_url = resolve_url(img_url_raw, root_url)

            verdict, reason = classify_image(img_url, alt_text)

            entry = {
                "original_url": img_url,
                "alt_text": alt_text,
                "referenced_in": [md_file.name],
                "filter_verdict": verdict,
                "filter_reason": reason,
            }

            if verdict == "skip":
                print(f"  SKIP  {img_url[:80]} — {reason}")
                manifest.append(entry)
                continue

            # Already downloaded this URL in a previous file
            if img_url in downloaded_urls:
                local_name = downloaded_urls[img_url]
                rel_path = f"../images/{local_name}"
                modified = modified.replace(m.group(0), f"![{alt_text}]({rel_path})")
                file_changed = True
                entry["local_path"] = str(images_dir / local_name)
                entry["reused"] = True
                manifest.append(entry)
                continue

            local_name = safe_image_filename(img_url, image_index)
            image_index += 1
            local_path = images_dir / local_name

            if dry_run:
                print(f"  WOULD DOWNLOAD  {img_url[:80]}")
                entry["local_path"] = str(local_path)
                entry["dry_run"] = True
                downloaded_urls[img_url] = local_name
                manifest.append(entry)
                continue

            ok, msg = download_image(img_url, local_path, session, max_size_bytes, no_verify_ssl)
            if not ok:
                print(f"  FAIL  {img_url[:80]} — {msg}")
                entry["download_error"] = msg
                entry["filter_verdict"] = "skip"
                manifest.append(entry)
                continue

            # Dimension check
            dim_ok, dim_msg = check_dimensions(local_path, min_width)
            if not dim_ok:
                print(f"  SKIP (dims)  {img_url[:80]} — {dim_msg}")
                local_path.unlink(missing_ok=True)
                entry["filter_verdict"] = "skip"
                entry["filter_reason"] = dim_msg
                manifest.append(entry)
                continue

            print(f"  OK  {img_url[:70]} → {local_name} ({msg}, {dim_msg})")

            rel_path = f"../images/{local_name}"
            modified = modified.replace(m.group(0), f"![{alt_text}]({rel_path})")
            file_changed = True
            downloaded_urls[img_url] = local_name

            entry["local_path"] = str(local_path)
            entry["size_msg"] = msg
            entry["dimensions"] = dim_msg
            manifest.append(entry)

            time.sleep(delay)

        if file_changed and not dry_run:
            md_file.write_text(modified, encoding="utf-8")

    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Download and filter images referenced in scraped Markdown pages."
    )
    parser.add_argument("--pages-dir", required=True, help="Directory of scraped .md files")
    parser.add_argument(
        "--images-dir", default="crawl_output/images/",
        help="Directory to save downloaded images (default: crawl_output/images/)"
    )
    parser.add_argument("--root-url", required=True, help="Base URL for resolving relative image paths")
    parser.add_argument(
        "--min-width", type=int, default=200,
        help="Minimum image width in pixels; narrower images are skipped as icons (default: 200)"
    )
    parser.add_argument(
        "--max-size-mb", type=float, default=5.0,
        help="Maximum image file size in MB; larger images are skipped (default: 5.0)"
    )
    parser.add_argument(
        "--delay", type=float, default=0.2,
        help="Seconds between image downloads (default: 0.2)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be downloaded without downloading or modifying .md files"
    )
    parser.add_argument(
        "--no-verify-ssl", action="store_true",
        help="Skip SSL certificate verification"
    )
    args = parser.parse_args()

    pages_dir = Path(args.pages_dir)
    images_dir = Path(args.images_dir)

    if not pages_dir.exists():
        print(f"ERROR: pages directory not found: {pages_dir}", file=sys.stderr)
        sys.exit(1)

    if not args.dry_run:
        images_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    max_size_bytes = int(args.max_size_mb * 1024 * 1024)

    manifest = process_pages(
        pages_dir=pages_dir,
        images_dir=images_dir,
        root_url=args.root_url,
        session=session,
        min_width=args.min_width,
        max_size_bytes=max_size_bytes,
        delay=args.delay,
        dry_run=args.dry_run,
        no_verify_ssl=args.no_verify_ssl,
    )

    total = len(manifest)
    downloaded = sum(1 for e in manifest if e.get("filter_verdict") == "keep" and not e.get("download_error") and not e.get("reused") and not e.get("dry_run"))
    skipped = sum(1 for e in manifest if e.get("filter_verdict") == "skip")

    print(f"\nImage processing complete:")
    print(f"  Total image references found: {total}")
    print(f"  Downloaded: {downloaded}")
    print(f"  Skipped (decorative/noise/error): {skipped}")

    if not args.dry_run:
        manifest_path = images_dir / "_manifest.json"
        manifest_data = {
            "root_url": args.root_url,
            "total_found": total,
            "downloaded": downloaded,
            "skipped": skipped,
            "images": manifest,
        }
        manifest_path.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False))
        print(f"  Manifest saved: {manifest_path}")
        print(f"\nNext step: review {manifest_path} and remove any images that are not")
        print(f"genuinely useful. Then run build_pdf.py to generate the final PDF.")
    else:
        print("  (dry-run: no files downloaded, no .md files modified)")


if __name__ == "__main__":
    main()
