#!/usr/bin/env python3
"""
validate_design_md.py — Validate a DESIGN.md file (Google design.md spec, alpha).

Mirrors the lint rules of `npx @google/design.md lint` so it works without
network or npm. Returns exit 0 if clean, exit 1 if any error-severity finding.

Usage:
    python validate_design_md.py DESIGN.md
    python validate_design_md.py DESIGN.md --json     # JSON output
    python validate_design_md.py DESIGN.md --no-wcag  # skip contrast checks
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # PyYAML
except ImportError:
    print(
        "error: PyYAML is required. Install with: pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# Spec constants
# ---------------------------------------------------------------------------

CANONICAL_SECTIONS = [
    ["overview", "brand & style", "brand and style"],
    ["colors", "color"],
    ["typography"],
    ["layout", "layout & spacing", "layout and spacing"],
    ["elevation & depth", "elevation"],
    ["shapes"],
    ["components"],
    ["do's and don'ts", "dos and donts", "do's & don'ts"],
]

COMPONENT_PROPERTY_WHITELIST = {
    "backgroundColor",
    "textColor",
    "typography",
    "rounded",
    "padding",
    "size",
    "height",
    "width",
}

DIMENSION_RE = re.compile(r"^-?\d+(\.\d+)?(px|em|rem|%|vh|vw|pt)?$")
HEX_RE = re.compile(r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{4}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")
TOKEN_REF_RE = re.compile(r"^\{([a-zA-Z0-9_.-]+)\}$")
SECTION_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


# ---------------------------------------------------------------------------
# Findings model
# ---------------------------------------------------------------------------

class Finding:
    __slots__ = ("rule", "severity", "message", "path")

    def __init__(self, rule: str, severity: str, message: str, path: str = ""):
        self.rule = rule
        self.severity = severity  # "error" | "warning" | "info"
        self.message = message
        self.path = path

    def to_dict(self) -> dict:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
        }


# ---------------------------------------------------------------------------
# Frontmatter + body split
# ---------------------------------------------------------------------------

def split_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm_text = text[3:end].lstrip("\n")
    body = text[end + 4 :].lstrip("\n")
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"invalid YAML front matter: {e}")
    if not isinstance(fm, dict):
        raise ValueError("front matter must be a mapping (YAML dict)")
    return fm, body


# ---------------------------------------------------------------------------
# Token resolution
# ---------------------------------------------------------------------------

def resolve_ref(fm: dict, ref: str) -> Any | None:
    """Resolve a dotted token path against the frontmatter."""
    parts = ref.split(".")
    node: Any = fm
    for p in parts:
        if not isinstance(node, dict) or p not in node:
            return None
        node = node[p]
    return node


def value_or_resolved(fm: dict, value: Any) -> tuple[Any, bool]:
    """If value is a token reference, resolve it. Returns (resolved, was_ref)."""
    if isinstance(value, str):
        m = TOKEN_REF_RE.match(value.strip())
        if m:
            resolved = resolve_ref(fm, m.group(1))
            return resolved, True
    return value, False


# ---------------------------------------------------------------------------
# Validators per section
# ---------------------------------------------------------------------------

def validate_color(value: Any, path: str, findings: list[Finding]) -> None:
    if not isinstance(value, str) or not HEX_RE.match(value):
        findings.append(
            Finding(
                "invalid-color",
                "error",
                f"not a valid hex color: {value!r}",
                path,
            )
        )


def validate_dimension(value: Any, path: str, findings: list[Finding]) -> None:
    if isinstance(value, (int, float)):
        return  # accept numeric (lineHeight ratios, fontWeight)
    if not isinstance(value, str) or not DIMENSION_RE.match(value):
        findings.append(
            Finding(
                "invalid-dimension",
                "error",
                f"not a valid dimension: {value!r}",
                path,
            )
        )


def validate_typography_entry(name: str, entry: Any, findings: list[Finding]) -> None:
    base = f"typography.{name}"
    if not isinstance(entry, dict):
        findings.append(
            Finding("invalid-typography", "error", "must be a mapping", base)
        )
        return
    if "fontSize" not in entry:
        findings.append(
            Finding("invalid-typography", "error", "missing required key 'fontSize'", base)
        )
    for k in ("fontSize", "letterSpacing"):
        if k in entry:
            validate_dimension(entry[k], f"{base}.{k}", findings)


def validate_token_refs(fm: dict, findings: list[Finding]) -> None:
    """Walk the whole frontmatter looking for {refs} and verify each resolves."""
    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")
        elif isinstance(node, str):
            m = TOKEN_REF_RE.match(node.strip())
            if m and resolve_ref(fm, m.group(1)) is None:
                findings.append(
                    Finding(
                        "broken-ref",
                        "error",
                        f"token reference does not resolve: {{{m.group(1)}}}",
                        path,
                    )
                )

    walk(fm, "")


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------

def validate_components(fm: dict, findings: list[Finding], skip_wcag: bool) -> None:
    components = fm.get("components")
    if components is None:
        return
    if not isinstance(components, dict):
        findings.append(
            Finding("invalid-component", "error", "must be a mapping", "components")
        )
        return

    for name, props in components.items():
        base = f"components.{name}"
        if not isinstance(props, dict):
            findings.append(
                Finding("invalid-component", "error", "must be a mapping", base)
            )
            continue
        for k, v in props.items():
            if k not in COMPONENT_PROPERTY_WHITELIST:
                findings.append(
                    Finding(
                        "unknown-component-property",
                        "warning",
                        f"property not in whitelist: {k!r}",
                        f"{base}.{k}",
                    )
                )
        if not skip_wcag:
            check_wcag(name, props, fm, findings)


# ---------------------------------------------------------------------------
# WCAG contrast
# ---------------------------------------------------------------------------

def hex_to_rgb(hex_str: str) -> tuple[float, float, float] | None:
    s = hex_str.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) == 8:
        s = s[:6]
    if len(s) != 6:
        return None
    try:
        r = int(s[0:2], 16) / 255
        g = int(s[2:4], 16) / 255
        b = int(s[4:6], 16) / 255
    except ValueError:
        return None
    return r, g, b


def relative_luminance(rgb: tuple[float, float, float]) -> float:
    def chan(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str, bg: str) -> float | None:
    a, b = hex_to_rgb(fg), hex_to_rgb(bg)
    if a is None or b is None:
        return None
    la, lb = relative_luminance(a), relative_luminance(b)
    light, dark = max(la, lb), min(la, lb)
    return (light + 0.05) / (dark + 0.05)


def check_wcag(name: str, props: dict, fm: dict, findings: list[Finding]) -> None:
    fg = props.get("textColor")
    bg = props.get("backgroundColor")
    if fg is None or bg is None:
        return
    fg_v, _ = value_or_resolved(fm, fg)
    bg_v, _ = value_or_resolved(fm, bg)
    if not isinstance(fg_v, str) or not isinstance(bg_v, str):
        return
    ratio = contrast_ratio(fg_v, bg_v)
    if ratio is None:
        return
    base = f"components.{name}"
    if ratio < 4.5:
        findings.append(
            Finding(
                "wcag-contrast",
                "warning",
                f"contrast {ratio:.2f}:1 fails WCAG AA (4.5:1) for body text",
                base,
            )
        )
    elif ratio < 7.0:
        findings.append(
            Finding(
                "wcag-contrast",
                "info",
                f"contrast {ratio:.2f}:1 passes AA but fails AAA (7:1)",
                base,
            )
        )


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def section_index(heading: str) -> int:
    h = heading.strip().lower()
    for i, aliases in enumerate(CANONICAL_SECTIONS):
        if h in aliases:
            return i
    return -1  # unknown — preserved without error


def validate_sections(body: str, findings: list[Finding]) -> None:
    headings = SECTION_HEADING_RE.findall(body)
    seen: dict[str, int] = {}
    last_idx = -1
    for h in headings:
        norm = h.strip().lower()
        if norm in seen:
            findings.append(
                Finding(
                    "duplicate-section",
                    "error",
                    f"section appears more than once: {h!r}",
                    f"##{h}",
                )
            )
        else:
            seen[norm] = 1
        idx = section_index(h)
        if idx == -1:
            continue
        if idx < last_idx:
            findings.append(
                Finding(
                    "section-order",
                    "error",
                    f"section {h!r} appears out of canonical order",
                    f"##{h}",
                )
            )
        last_idx = max(last_idx, idx)


# ---------------------------------------------------------------------------
# Top-level validator
# ---------------------------------------------------------------------------

def validate(text: str, skip_wcag: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    try:
        fm, body = split_frontmatter(text)
    except ValueError as e:
        return [Finding("invalid-frontmatter", "error", str(e), "<frontmatter>")]

    if fm is None:
        return [
            Finding(
                "missing-frontmatter",
                "error",
                "DESIGN.md must start with YAML front matter delimited by '---'",
                "<frontmatter>",
            )
        ]

    if "name" not in fm:
        findings.append(
            Finding("missing-required", "error", "missing required key 'name'", "name")
        )

    # Colors
    colors = fm.get("colors", {})
    if isinstance(colors, dict):
        for k, v in colors.items():
            v2, _ = value_or_resolved(fm, v)
            validate_color(v2, f"colors.{k}", findings)

    # Spacing / rounded — both dimension scales
    for section in ("spacing", "rounded"):
        scale = fm.get(section, {})
        if isinstance(scale, dict):
            for k, v in scale.items():
                v2, _ = value_or_resolved(fm, v)
                validate_dimension(v2, f"{section}.{k}", findings)

    # Typography
    typography = fm.get("typography", {})
    if isinstance(typography, dict):
        for name, entry in typography.items():
            validate_typography_entry(name, entry, findings)

    # Components
    validate_components(fm, findings, skip_wcag)

    # Token references (anywhere)
    validate_token_refs(fm, findings)

    # Section order / duplicates
    validate_sections(body, findings)

    return findings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def format_text(findings: list[Finding], path: str) -> str:
    if not findings:
        return f"✓ {path}: clean (0 findings)"
    lines = [f"{path}:"]
    by_sev = {"error": [], "warning": [], "info": []}
    for f in findings:
        by_sev.setdefault(f.severity, []).append(f)
    for sev in ("error", "warning", "info"):
        for f in by_sev[sev]:
            tag = {"error": "✗", "warning": "!", "info": "i"}[sev]
            loc = f" [{f.path}]" if f.path else ""
            lines.append(f"  {tag} {sev}: {f.rule}: {f.message}{loc}")
    err = sum(1 for f in findings if f.severity == "error")
    warn = sum(1 for f in findings if f.severity == "warning")
    info = sum(1 for f in findings if f.severity == "info")
    lines.append(f"  → {err} error(s), {warn} warning(s), {info} info")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to DESIGN.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--no-wcag", action="store_true", help="Skip WCAG checks")
    args = parser.parse_args(argv)

    p = Path(args.path)
    if not p.exists():
        print(f"error: {p} does not exist", file=sys.stderr)
        return 2

    text = p.read_text(encoding="utf-8")
    findings = validate(text, skip_wcag=args.no_wcag)

    if args.json:
        print(
            json.dumps(
                {"path": str(p), "findings": [f.to_dict() for f in findings]},
                indent=2,
            )
        )
    else:
        print(format_text(findings, str(p)))

    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
