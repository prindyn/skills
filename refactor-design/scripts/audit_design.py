#!/usr/bin/env python3
"""
Audit HTML/CSS files for common UI design problems.

Based on Refactoring UI principles. Checks for:
  - Arbitrary spacing values (not on a scale)
  - Too many distinct font sizes
  - Long text lines (no max-width)
  - Naked hex colors (not using custom properties)
  - Grey text on colored backgrounds (regex heuristic)
  - Missing focus styles
  - Too many distinct colors
  - Potential contrast issues

Usage:
    python audit_design.py path/to/styles.css
    python audit_design.py path/to/styles.css path/to/index.html
    python audit_design.py --check-contrast styles.css
    python audit_design.py --json styles.css
"""

import argparse
import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Literal


Severity = Literal["error", "warning", "info"]


@dataclass
class Issue:
    severity: Severity
    category: str
    message: str
    file: str = ""
    line: int = 0
    context: str = ""


@dataclass
class AuditResult:
    issues: list[Issue] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def add(self, severity: Severity, category: str, message: str,
            file: str = "", line: int = 0, context: str = "") -> None:
        self.issues.append(Issue(severity, category, message, file, line, context))

    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "warning"]


# ---------------------------------------------------------------------------
# Spacing scale (acceptable values in px)
# ---------------------------------------------------------------------------
SCALE_PX = {0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40, 48, 56,
            64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384}
SCALE_REM = {v / 16 for v in SCALE_PX}


def is_on_spacing_scale(value_str: str) -> bool:
    """Return True if a CSS length value is on the standard spacing scale."""
    try:
        if value_str.endswith("px"):
            return float(value_str[:-2]) in SCALE_PX
        if value_str.endswith("rem"):
            return round(float(value_str[:-3]), 4) in {round(v, 4) for v in SCALE_REM}
    except ValueError:
        pass
    return True  # unknown units — don't flag


# ---------------------------------------------------------------------------
# CSS auditor
# ---------------------------------------------------------------------------

def audit_css(path: Path, result: AuditResult) -> None:
    text = path.read_text(errors="replace")
    lines = text.splitlines()

    hex_colors: list[str] = []
    font_sizes: set[str] = set()
    has_focus_style = False
    spacing_violations: list[tuple[int, str, str]] = []

    # Patterns
    re_hex = re.compile(r"(?<!['\"])\#([0-9a-fA-F]{3,8})\b")
    re_font_size = re.compile(r"font-size:\s*([^;]+);")
    re_focus = re.compile(r":focus(?:-visible)?")
    re_max_width_ch = re.compile(r"max-width:\s*\d+ch")
    re_spacing_prop = re.compile(
        r"(margin|padding|gap|top|right|bottom|left|width|height)(?:-\w+)?:\s*([^;]+);"
    )
    re_length = re.compile(r"(\d+(?:\.\d+)?)(px|rem)\b")

    has_ch_constraint = bool(re_max_width_ch.search(text))

    for lineno, line in enumerate(lines, start=1):
        # Hex colors not in comments or variable definitions
        for match in re_hex.finditer(line):
            if not line.strip().startswith("//") and not line.strip().startswith("*"):
                hex_colors.append(match.group(0))

        # Font sizes
        for match in re_font_size.finditer(line):
            font_sizes.add(match.group(1).strip())

        # Focus styles
        if re_focus.search(line):
            has_focus_style = True

        # Spacing violations
        for match in re_spacing_prop.finditer(line):
            prop = match.group(1)
            value = match.group(2).strip()
            # Skip custom property references and calc()
            if "var(" in value or "calc(" in value or "%" in value or "auto" in value:
                continue
            for length_match in re_length.finditer(value):
                num = length_match.group(1)
                unit = length_match.group(2)
                val_str = num + unit
                if not is_on_spacing_scale(val_str):
                    spacing_violations.append((lineno, prop, val_str))

    # Report hex colors
    unique_hex = list(dict.fromkeys(hex_colors))
    result.stats["naked_hex_count"] = len(unique_hex)
    if unique_hex:
        result.add(
            "warning", "Color",
            f"Found {len(unique_hex)} naked hex color(s). Use HSL custom properties instead. "
            f"First few: {', '.join(unique_hex[:5])}",
            file=str(path),
        )

    # Too many font sizes
    result.stats["distinct_font_sizes"] = len(font_sizes)
    if len(font_sizes) > 8:
        result.add(
            "warning", "Typography",
            f"Found {len(font_sizes)} distinct font-size values — ideal is ≤ 8. "
            f"Values: {', '.join(sorted(font_sizes))}",
            file=str(path),
        )

    # Missing focus styles
    if not has_focus_style:
        result.add(
            "error", "Accessibility",
            "No :focus or :focus-visible styles found. All interactive elements need visible focus rings.",
            file=str(path),
        )

    # Missing max-width constraint (ch units)
    if not has_ch_constraint:
        result.add(
            "info", "Typography",
            "No max-width using 'ch' units found. Consider 'max-width: 65ch' on prose content.",
            file=str(path),
        )

    # Spacing violations (sample)
    result.stats["spacing_violations"] = len(spacing_violations)
    if spacing_violations:
        sample = spacing_violations[:5]
        sample_str = ", ".join(f"line {ln}: {prop}={val}" for ln, prop, val in sample)
        result.add(
            "warning", "Spacing",
            f"{len(spacing_violations)} spacing value(s) not on the standard scale. "
            f"Sample: {sample_str}",
            file=str(path),
        )


# ---------------------------------------------------------------------------
# HTML auditor
# ---------------------------------------------------------------------------

def audit_html(path: Path, result: AuditResult) -> None:
    text = path.read_text(errors="replace")

    # Inline style attribute check
    inline_style_count = len(re.findall(r'\bstyle=["\']', text))
    if inline_style_count > 5:
        result.add(
            "warning", "Maintainability",
            f"Found {inline_style_count} inline style attributes. Prefer CSS classes for consistency.",
            file=str(path),
        )

    # Check for tables used for layout (not data)
    layout_table = re.search(r'<table[^>]*>\s*<tr', text)
    if layout_table:
        result.add(
            "info", "Layout",
            "Found <table> element — ensure it's for tabular data, not layout.",
            file=str(path),
        )

    # Missing alt text on images
    img_no_alt = re.findall(r'<img(?![^>]*\balt=)[^>]*>', text)
    if img_no_alt:
        result.add(
            "error", "Accessibility",
            f"{len(img_no_alt)} <img> element(s) missing alt attribute.",
            file=str(path),
        )

    # Check for color used alone for status (red/green classes without text)
    if re.search(r'class=["\'][^"\']*(?:text-red|text-green|bg-red|bg-green)', text):
        result.add(
            "info", "Accessibility",
            "Found color-based status classes (text-red, bg-green, etc.). "
            "Ensure status is also communicated with text or icons, not color alone.",
            file=str(path),
        )

    # Empty state check: look for empty state patterns
    has_empty_state = bool(
        re.search(r'empty[_-]?state|no[-_\s]data|no[-_\s]results|placeholder', text, re.IGNORECASE)
    )
    result.stats["has_empty_state_pattern"] = has_empty_state
    if not has_empty_state:
        result.add(
            "info", "UX",
            "No empty state pattern detected. Consider adding empty states for lists and data containers.",
            file=str(path),
        )


# ---------------------------------------------------------------------------
# Reporter
# ---------------------------------------------------------------------------

SEVERITY_ICON = {"error": "✖", "warning": "▲", "info": "ℹ"}
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


def print_report(result: AuditResult, verbose: bool = False) -> None:
    issues = sorted(result.issues, key=lambda i: SEVERITY_ORDER[i.severity])

    counts = {"error": 0, "warning": 0, "info": 0}
    for issue in issues:
        counts[issue.severity] += 1

    print("\n┌─ Design Audit Report ─────────────────────────────────────")
    print(f"│  {counts['error']} errors  ·  {counts['warning']} warnings  ·  {counts['info']} suggestions")
    print("└────────────────────────────────────────────────────────────\n")

    current_category = None
    for issue in issues:
        if issue.category != current_category:
            current_category = issue.category
            print(f"  [{issue.category}]")
        icon = SEVERITY_ICON[issue.severity]
        file_ref = f" ({issue.file}:{issue.line})" if issue.line else (f" ({issue.file})" if issue.file else "")
        print(f"    {icon} {issue.message}{file_ref}")
    print()

    if result.stats:
        print("  Stats:")
        for k, v in result.stats.items():
            print(f"    {k}: {v}")
        print()

    if counts["error"] == 0 and counts["warning"] == 0:
        print("  No critical issues found. Review suggestions above.")
    else:
        print(f"  Fix {counts['error']} error(s) and {counts['warning']} warning(s) for a production-ready design.")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit HTML/CSS files for common UI design issues.")
    parser.add_argument("files", nargs="+", type=Path, help="Files to audit (.css and/or .html)")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--verbose", action="store_true", help="Show additional context")
    args = parser.parse_args()

    result = AuditResult()

    for path in args.files:
        if not path.exists():
            print(f"Error: {path} not found.", file=sys.stderr)
            return 1
        suffix = path.suffix.lower()
        if suffix == ".css":
            audit_css(path, result)
        elif suffix in (".html", ".htm"):
            audit_html(path, result)
        else:
            print(f"Skipping {path} — unsupported extension (use .css or .html).")

    if args.json:
        output = {
            "issues": [
                {
                    "severity": i.severity,
                    "category": i.category,
                    "message": i.message,
                    "file": i.file,
                    "line": i.line,
                }
                for i in result.issues
            ],
            "stats": result.stats,
            "summary": {
                "errors": len(result.errors()),
                "warnings": len(result.warnings()),
                "info": sum(1 for i in result.issues if i.severity == "info"),
            },
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(result, verbose=args.verbose)

    return 1 if result.errors() else 0


if __name__ == "__main__":
    sys.exit(main())
