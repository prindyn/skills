# Image Handling Guide

How to decide which images to include, how to download them, and how to embed
them in the final PDF book.

---

## When to include images

Images add value when they show something that words cannot convey as efficiently:
- Architecture diagrams showing component relationships
- UML diagrams for design patterns
- Before/after screenshots showing a transformation
- Terminal/REPL output showing what code produces
- Charts and graphs that visualize data
- Step-by-step tutorial screenshots with clear sequence

Images do NOT add value when they are:
- Decorative hero images or background illustrations
- Author headshots or team photos
- Social media preview images
- Marketing banners ("Buy now!", "Spring SALE")
- Site logos and favicon-style icons
- Language/framework logos used as bullet decorations
- Cookie consent or GDPR notice imagery

The rule of thumb: an image earns its place if removing it would make the text
harder to understand. A purely decorative image just adds file size.

---

## The fetch_images.py script

`scripts/fetch_images.py` automates image filtering and downloading.

```bash
python scripts/fetch_images.py \
  --pages-dir crawl_output/pages/ \
  --images-dir crawl_output/images/ \
  --root-url "https://example.com"
```

**What it does:**
1. Scans all `.md` files in `--pages-dir` for `![alt](url)` image references
2. Applies filtering heuristics (see below) to skip decorative/marketing images
3. Downloads images that pass the filter to `--images-dir`
4. Rewrites `.md` image references from absolute URLs to relative local paths
5. Writes a manifest at `--images-dir/_manifest.json`

**Key flags:**

| Flag | Default | Description |
|---|---|---|
| `--pages-dir` | required | Directory of scraped .md files |
| `--images-dir` | `crawl_output/images/` | Where to save downloaded images |
| `--root-url` | required | Base URL for resolving relative image paths |
| `--min-width` | 200 | Skip images narrower than N pixels (icon threshold) |
| `--max-size-mb` | 5 | Skip images larger than N MB |
| `--delay` | 0.2 | Seconds between image downloads |
| `--dry-run` | off | Print what would be downloaded, don't download |
| `--no-verify-ssl` | off | Skip SSL verification |

---

## Filtering heuristics

The script uses two layers of heuristics to decide whether an image is valuable.

### Layer 1: URL pattern matching

**Likely decorative — skip:**
```
/logo
/avatar
/icon
/badge
/banner
/hero
/background
/favicon
/social
/share
/twitter
/facebook
/instagram
/linkedin
/youtube
/sprite
/pixel
/tracking
/analytics
/ad/
/ads/
/promo
/sale
```

**Likely valuable — keep:**
```
/diagram
/figure
/img/
/images/
/assets/
/screenshot
/output
/example
/pattern
/architecture
/schema
/chart
/graph
/illustration
/tutorial
```

### Layer 2: Alt text analysis

**Alt text suggesting value:** "diagram", "figure", "example", "output", "screenshot",
"illustration", "architecture", "flow", "chart", "graph", "schema", "structure",
"pattern", "step"

**Alt text suggesting noise:** "logo", "icon", "avatar", "photo", "picture", "banner",
"badge", "share", "facebook", "twitter", empty alt text with a decorative URL

### Layer 3: Image dimensions (requires Pillow)

Images narrower than `--min-width` (default 200px) are almost certainly icons
or decorative bullets. Skip them.

Very wide, very short images (aspect ratio > 5:1) are usually banners. Skip them.

---

## Manual review after downloading

After running `fetch_images.py`, review `crawl_output/images/_manifest.json`:

```json
{
  "images": [
    {
      "original_url": "https://example.com/img/singleton-diagram.png",
      "local_path": "crawl_output/images/singleton-diagram.png",
      "alt_text": "Singleton class diagram",
      "referenced_in": ["0042_design-patterns__singleton.md"],
      "width": 640,
      "height": 480,
      "size_kb": 28,
      "filter_verdict": "keep",
      "filter_reason": "URL contains 'diagram', alt text contains 'diagram'"
    }
  ],
  "total_found": 87,
  "downloaded": 23,
  "skipped": 64
}
```

For each downloaded image, ask:
- Is this image in context? (Is it adjacent to text that references it?)
- Does it illuminate the text, or is it just visual noise?
- Is it high enough quality to appear in a PDF? (Blurry screenshots are worse than no screenshot)

Delete images that don't pass this review by:
1. Removing the file from `crawl_output/images/`
2. Removing the `![alt](../images/filename)` reference from the corresponding `.md` file
3. Updating `_manifest.json` (optional, for your own tracking)

---

## Image embedding in the PDF

WeasyPrint handles local image paths correctly when the HTML references them
as relative paths from the HTML file's location. The `fetch_images.py` script
rewrites references to use relative paths that work with the build step.

If images are not appearing in the HTML preview:
1. Verify the local file exists at `crawl_output/images/filename.ext`
2. Check that the `.md` reference uses `../images/filename.ext` (not an absolute URL)
3. When running `build_pdf.py`, pass `--pages-dir crawl_output/pages/` so the
   relative paths resolve correctly

**pdfkit / wkhtmltopdf note:** wkhtmltopdf requires the `--enable-local-file-access`
flag to embed local images. This is set by default in `build_pdf.py`.

---

## CSS for images in the book

The default `assets/book.css` already includes:

```css
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1em auto;
}
```

This prevents images from overflowing the page and centers them. For images that
should appear inline (small icons that slipped through), add a CSS class:

```css
img.inline {
  display: inline;
  margin: 0;
  vertical-align: middle;
  height: 1.2em;
}
```

For full-page diagrams, add a caption by surrounding the image with a figure block
in the Markdown:

```markdown
![Architecture diagram](../images/architecture.png)
*Figure 3: The three-layer architecture showing how requests flow.*
```

---

## Common issues

| Problem | Cause | Fix |
|---|---|---|
| Image not appearing in HTML | Broken relative path | Check path in .md file; verify file exists |
| Image too large, breaks layout | No max-width constraint | Already handled by CSS; check if custom CSS overrides it |
| Image is blurry | Low-resolution source | Remove the reference; describe in text instead |
| PDF file size too large | Too many high-res images | Reduce image count; use `--max-size-mb 1` in fetch_images.py |
| SVG not rendering in WeasyPrint | WeasyPrint SVG support varies | Convert to PNG first: `cairosvg input.svg -o output.png` |
| External image URL still in .md | fetch_images.py skipped it | Add `--root-url` correctly; or manually download and rewrite |
