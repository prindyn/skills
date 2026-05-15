# PDF Rendering Backends

`build_pdf.py` supports two PDF backends. The script tries WeasyPrint first;
if unavailable or if it raises an exception it falls back to pdfkit.

---

## WeasyPrint (recommended)

WeasyPrint is a pure-Python library that renders HTML+CSS to PDF.
It supports modern CSS including CSS Paged Media (running headers, page numbers).

### Install

```bash
pip install weasyprint
```

On some Linux systems you also need:

```bash
# Debian / Ubuntu
apt-get install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0

# Alpine
apk add pango fontconfig ttf-freefont
```

On macOS:

```bash
brew install pango libffi
pip install weasyprint
```

### Known issues

- **Font rendering**: WeasyPrint uses the system's Fontconfig/Pango stack.
  If fonts look wrong, install additional fonts (`apt-get install fonts-liberation`).
- **SVG**: WeasyPrint renders inline SVG but not all `<img src="*.svg">` reliably.
  Consider converting SVGs to PNG before building.
- **Very large documents**: Memory usage scales with page count.
  For > 1 000 pages, split into volumes.

---

## pdfkit + wkhtmltopdf (fallback)

pdfkit is a Python wrapper around the `wkhtmltopdf` binary, which uses the
Chromium / WebKit rendering engine.

### Install

```bash
pip install pdfkit
```

Then install `wkhtmltopdf`:

```bash
# Debian / Ubuntu
apt-get install wkhtmltopdf

# macOS
brew install --cask wkhtmltopdf

# Windows — download installer from:
# https://wkhtmltopdf.org/downloads.html
```

### Known issues

- `wkhtmltopdf` does not support CSS Paged Media page numbers by default.
  Use the `--header-right "[page]"` option or install the patched version
  with the Qt headers patch applied (available on the official downloads page).
- JavaScript-heavy pages may need `--javascript-delay 2000`.
- Running headers / `string-set` CSS is not supported.

---

## Choosing a backend

| Feature | WeasyPrint | pdfkit |
|---|---|---|
| Pure Python | Yes | No (needs wkhtmltopdf binary) |
| CSS Paged Media | Yes | Partial |
| Page numbers via CSS | Yes | No (needs patched build) |
| Running headers | Yes | No |
| JavaScript rendering | No | Yes (via wkhtmltopdf) |
| Performance on large docs | Good | Good |
| Docker / headless | Easy | Needs wkhtmltopdf + fonts |

For documentation sites and wikis, WeasyPrint is the better choice.
For JavaScript-heavy SPAs, see `references/js-rendering.md`.
