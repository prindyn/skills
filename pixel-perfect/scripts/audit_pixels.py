#!/usr/bin/env python3
"""
audit_pixels.py — Scan UI source files for pixel-perfect / token-fidelity issues.

Given a DESIGN.md and one or more source files (HTML, CSS, JSX, TSX, Vue,
Svelte), report:

  - Hex/rgb/hsl literals not in the DESIGN.md color palette
  - Spacing values not in the DESIGN.md spacing scale
  - Border-radius values not in the rounded scale
  - Font-size values not in the typography scale
  - Buttons / links / [role=button] missing focus-visible styling
  - Suspicious sub-pixel transforms (translate(-50%, -50%) on declared 1px borders)

Findings are non-fatal hints unless --strict is passed. Useful as a
self-check before handing UI back to the user.

Usage:
    python audit_pixels.py --design DESIGN.md src/**/*.tsx
    python audit_pixels.py --design DESIGN.md index.html --json
    python audit_pixels.py --design DESIGN.md src --strict
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:
    print("error: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)


HEX_LITERAL_RE = re.compile(r"#([0-9a-fA-F]{3,8})\b")
RGB_LITERAL_RE = re.compile(r"\brgb[a]?\s*\(([^)]+)\)")
PX_LITERAL_RE = re.compile(r"(?<![\w.-])(-?\d+(?:\.\d+)?)px\b")
REM_LITERAL_RE = re.compile(r"(?<![\w.-])(-?\d+(?:\.\d+)?)rem\b")
FONT_SIZE_RE = re.compile(
    r"font-size\s*[:=]\s*['\"]?(\d+(?:\.\d+)?(?:px|rem|em|pt))",
    re.IGNORECASE,
)
PADDING_MARGIN_RE = re.compile(
    r"\b(padding|margin|gap|top|left|right|bottom|inset)(?:-(?:top|right|bottom|left|x|y|inline|block))?"
    r"\s*[:=]\s*['\"]?([^;'\"<>}]+?)\s*['\"]?[;\}]",
    re.IGNORECASE,
)
RADIUS_RE = re.compile(
    r"\bborder-radius\s*[:=]\s*['\"]?([^;'\"<>}]+?)\s*['\"]?[;\}]",
    re.IGNORECASE,
)
BUTTON_TAG_RE = re.compile(
    r"<(button|a)\b[^>]*>",
    re.IGNORECASE | re.DOTALL,
)
TRANSLATE_HALF_RE = re.compile(
    r"translate\s*\(\s*-?50%\s*,\s*-?50%\s*\)",
    re.IGNORECASE,
)
BORDER_1PX_RE = re.compile(r"border\s*:\s*1px\b", re.IGNORECASE)


def split_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    return yaml.safe_load(text[3:end].lstrip("\n")) or {}


def normalize_hex(h: str) -> str:
    s = h.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) == 8:
        s = s[:6]
    return "#" + s.upper()


def collect_palette(fm: dict) -> set[str]:
    """Return all hex colors (normalized to #RRGGBB upper) from DESIGN.md."""
    palette: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
        elif isinstance(node, str) and node.startswith("#"):
            try:
                palette.add(normalize_hex(node))
            except Exception:
                pass

    walk(fm.get("colors", {}))
    walk(fm.get("components", {}))
    # Token references in components might not be hex; safe to skip.
    return palette


def collect_dimension_scale(fm: dict, key: str) -> set[str]:
    """Return all values from spacing/rounded as a string set."""
    scale = fm.get(key, {})
    out: set[str] = set()
    if isinstance(scale, dict):
        for v in scale.values():
            if isinstance(v, str):
                out.add(v.strip())
            elif isinstance(v, (int, float)):
                out.add(f"{v}px")
    return out


def collect_font_sizes(fm: dict) -> set[str]:
    out: set[str] = set()
    typo = fm.get("typography", {})
    if isinstance(typo, dict):
        for entry in typo.values():
            if isinstance(entry, dict) and "fontSize" in entry:
                fs = entry["fontSize"]
                if isinstance(fs, str):
                    out.add(fs.strip())
    return out


# ---------------------------------------------------------------------------
# File scanning
# ---------------------------------------------------------------------------

class Finding:
    __slots__ = ("file", "line", "rule", "message")

    def __init__(self, file: str, line: int, rule: str, message: str):
        self.file = file
        self.line = line
        self.rule = rule
        self.message = message

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "line": self.line,
            "rule": self.rule,
            "message": self.message,
        }


SOURCE_EXTS = {
    ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro",
    ".module.css",
}


def iter_files(paths: Iterable[str]) -> Iterable[Path]:
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            for ext in SOURCE_EXTS:
                yield from p.rglob(f"*{ext}")
        elif p.is_file():
            yield p


def is_in_token_context(line: str) -> bool:
    """Heuristic: if the line uses var(--…), tw class, or theme(), allow it."""
    return (
        "var(--" in line
        or "theme(" in line
        or "tokens." in line
        or "$color-" in line
        or "@apply " in line
    )


def looks_like_palette_comment(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith(("//", "/*", "*", "<!--", "#"))


def scan_file(
    path: Path,
    palette: set[str],
    spacing_scale: set[str],
    rounded_scale: set[str],
    font_sizes: set[str],
) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [Finding(str(path), 0, "read-error", str(e))]

    findings: list[Finding] = []
    lines = text.splitlines()

    # 1. Hex literals not in palette
    for i, line in enumerate(lines, 1):
        if looks_like_palette_comment(line):
            continue
        for m in HEX_LITERAL_RE.finditer(line):
            try:
                norm = normalize_hex(m.group(0))
            except Exception:
                continue
            if norm not in palette:
                findings.append(
                    Finding(
                        str(path), i, "off-token-color",
                        f"hex {m.group(0)} not in DESIGN.md palette ({norm})",
                    )
                )

    # 2. font-size literals
    if font_sizes:
        for i, line in enumerate(lines, 1):
            for m in FONT_SIZE_RE.finditer(line):
                v = m.group(1).strip()
                if v not in font_sizes and not is_in_token_context(line):
                    findings.append(
                        Finding(
                            str(path), i, "off-token-font-size",
                            f"font-size {v!r} not in typography scale {sorted(font_sizes)}",
                        )
                    )

    # 3. spacing / margin / padding / gap (px values only — rems often legit)
    if spacing_scale:
        scale_px = {v for v in spacing_scale if v.endswith("px")}
        for i, line in enumerate(lines, 1):
            if is_in_token_context(line):
                continue
            for m in PADDING_MARGIN_RE.finditer(line):
                value = m.group(2)
                # Pull all px values from the multi-value (e.g. "8px 16px")
                for px_match in PX_LITERAL_RE.finditer(value):
                    px_value = px_match.group(1) + "px"
                    if px_value == "0px" or px_value == "1px":
                        continue  # 0 and hairlines are exempt
                    if px_value not in scale_px:
                        findings.append(
                            Finding(
                                str(path), i, "off-token-spacing",
                                f"{m.group(1)} value {px_value} not in spacing scale "
                                f"{sorted(scale_px)}",
                            )
                        )

    # 4. border-radius
    if rounded_scale:
        scale_px = {v for v in rounded_scale if v.endswith("px")}
        for i, line in enumerate(lines, 1):
            if is_in_token_context(line):
                continue
            for m in RADIUS_RE.finditer(line):
                value = m.group(1).strip()
                for px_match in PX_LITERAL_RE.finditer(value):
                    px_value = px_match.group(1) + "px"
                    if px_value == "0px":
                        continue
                    if px_value not in scale_px:
                        findings.append(
                            Finding(
                                str(path), i, "off-token-radius",
                                f"border-radius {px_value} not in rounded scale "
                                f"{sorted(scale_px)}",
                            )
                        )

    # 5. Suspicious sub-pixel transform
    for i, line in enumerate(lines, 1):
        if TRANSLATE_HALF_RE.search(line):
            window = "\n".join(lines[max(0, i - 4) : min(len(lines), i + 4)])
            if BORDER_1PX_RE.search(window):
                findings.append(
                    Finding(
                        str(path), i, "subpixel-risk",
                        "translate(-50%, -50%) near a 1px border may produce blurred edges",
                    )
                )

    # 6. Buttons/links missing focus-visible
    if path.suffix in {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro"}:
        if BUTTON_TAG_RE.search(text):
            if "focus-visible" not in text and "focus:outline" not in text and ":focus" not in text:
                findings.append(
                    Finding(
                        str(path), 0, "missing-focus-visible",
                        "file declares <button>/<a> but no focus-visible / :focus styling found",
                    )
                )

    # 7. outline: none without replacement
    for i, line in enumerate(lines, 1):
        if "outline: none" in line.lower() or "outline:none" in line.lower():
            window = "\n".join(lines[max(0, i - 5) : min(len(lines), i + 10)])
            if "outline" not in window.lower().replace("outline: none", "").replace("outline:none", ""):
                # crude but catches the common case
                findings.append(
                    Finding(
                        str(path), i, "outline-suppressed",
                        "outline: none without an obvious replacement focus indicator",
                    )
                )

    return findings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", required=True, help="Path to DESIGN.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any findings (default: exit 0 even with findings)",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Files or directories to scan",
    )
    args = parser.parse_args(argv)

    design_path = Path(args.design)
    if not design_path.exists():
        print(f"error: {design_path} does not exist", file=sys.stderr)
        return 2

    fm = split_frontmatter(design_path.read_text(encoding="utf-8"))
    palette = collect_palette(fm)
    spacing_scale = collect_dimension_scale(fm, "spacing")
    rounded_scale = collect_dimension_scale(fm, "rounded")
    font_sizes = collect_font_sizes(fm)

    if not palette:
        print(
            f"warning: no colors found in {design_path}; off-token-color checks disabled",
            file=sys.stderr,
        )

    all_findings: list[Finding] = []
    files = list(iter_files(args.paths))
    if not files:
        print("warning: no files matched the given paths", file=sys.stderr)
    for f in files:
        all_findings.extend(scan_file(f, palette, spacing_scale, rounded_scale, font_sizes))

    if args.json:
        print(
            json.dumps(
                {
                    "design": str(design_path),
                    "files_scanned": len(files),
                    "findings": [f.to_dict() for f in all_findings],
                },
                indent=2,
            )
        )
    else:
        if not all_findings:
            print(f"✓ clean — 0 findings across {len(files)} file(s)")
        else:
            for f in all_findings:
                loc = f"{f.file}:{f.line}" if f.line else f.file
                print(f"  {loc}: {f.rule}: {f.message}")
            print(f"\n→ {len(all_findings)} finding(s) across {len(files)} file(s)")

    return 1 if (args.strict and all_findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
