#!/usr/bin/env python3
"""
extract_tokens.py — Convert a DESIGN.md file's tokens into usable forms.

Reads the YAML front matter from DESIGN.md and emits one of:

  --format css       CSS custom properties under :root
  --format tailwind  Tailwind-friendly theme JSON (colors, spacing, …)
  --format json      Plain JSON dump of the token tree
  --format scss      SCSS variable file ($color-primary: #…;)

Token references like {colors.primary} are resolved before emission.

Usage:
    python extract_tokens.py DESIGN.md --format css > tokens.css
    python extract_tokens.py DESIGN.md --format tailwind > theme.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("error: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

TOKEN_REF_RE = re.compile(r"^\{([a-zA-Z0-9_.-]+)\}$")


def split_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        raise ValueError("DESIGN.md missing YAML frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("DESIGN.md frontmatter not terminated")
    fm = yaml.safe_load(text[3:end].lstrip("\n")) or {}
    if not isinstance(fm, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return fm


def resolve(fm: dict, value: Any) -> Any:
    """Recursively resolve {token.refs} in any leaf string."""
    if isinstance(value, dict):
        return {k: resolve(fm, v) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve(fm, v) for v in value]
    if isinstance(value, str):
        m = TOKEN_REF_RE.match(value.strip())
        if m:
            parts = m.group(1).split(".")
            node: Any = fm
            for p in parts:
                if not isinstance(node, dict) or p not in node:
                    return value  # unresolved — leave intact
                node = node[p]
            return resolve(fm, node)  # recursive resolve in case it points at a ref
    return value


def kebab(name: str) -> str:
    """Convert camelCase or snake_case to kebab-case."""
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name)
    return s.replace("_", "-").lower()


# ---------------------------------------------------------------------------
# CSS emitter
# ---------------------------------------------------------------------------

def emit_css(fm: dict) -> str:
    out = [":root {"]

    colors = fm.get("colors", {})
    for k, v in colors.items():
        out.append(f"  --color-{kebab(k)}: {resolve(fm, v)};")

    spacing = fm.get("spacing", {})
    for k, v in spacing.items():
        out.append(f"  --space-{kebab(k)}: {resolve(fm, v)};")

    rounded = fm.get("rounded", {})
    for k, v in rounded.items():
        out.append(f"  --rounded-{kebab(k)}: {resolve(fm, v)};")

    typography = fm.get("typography", {})
    for name, entry in typography.items():
        if not isinstance(entry, dict):
            continue
        prefix = f"--font-{kebab(name)}"
        for k, v in entry.items():
            # Drop the redundant "font" prefix from the property half of the
            # variable name (we already have --font-… up front). So
            # "fontFamily" → "family", "fontSize" → "size", "fontWeight" →
            # "weight". Other keys (lineHeight, letterSpacing) keep their
            # kebab form.
            short = kebab(k)
            if short.startswith("font-"):
                short = short[len("font-"):]
            out.append(f"  {prefix}-{short}: {resolve(fm, v)};")

    out.append("}")

    # Component classes — we emit them as utility-ish CSS rules
    components = fm.get("components", {})
    if components:
        out.append("")
        for name, props in components.items():
            if not isinstance(props, dict):
                continue
            sel = component_selector(name)
            out.append(f"{sel} {{")
            if "backgroundColor" in props:
                out.append(f"  background-color: {resolve_color(fm, props['backgroundColor'])};")
            if "textColor" in props:
                out.append(f"  color: {resolve_color(fm, props['textColor'])};")
            if "rounded" in props:
                out.append(f"  border-radius: {resolve_color(fm, props['rounded'])};")
            if "padding" in props:
                out.append(f"  padding: {resolve_color(fm, props['padding'])};")
            for dim in ("size", "height", "width"):
                if dim in props:
                    css_prop = "min-height" if dim == "size" else dim
                    out.append(f"  {css_prop}: {resolve_color(fm, props[dim])};")
            out.append("}")

    return "\n".join(out) + "\n"


def resolve_color(fm: dict, v: Any) -> Any:
    return resolve(fm, v)


def component_selector(name: str) -> str:
    """Convert `button-primary-hover` → `.button-primary:hover`."""
    states = ("hover", "active", "focus", "disabled", "selected", "pressed")
    parts = name.rsplit("-", 1)
    if len(parts) == 2 and parts[1] in states:
        pseudo = "focus-visible" if parts[1] == "focus" else parts[1]
        return f".{parts[0]}:{pseudo}"
    return f".{name}"


# ---------------------------------------------------------------------------
# Tailwind emitter
# ---------------------------------------------------------------------------

def emit_tailwind(fm: dict) -> str:
    theme: dict[str, Any] = {}

    colors = {k: resolve(fm, v) for k, v in fm.get("colors", {}).items()}
    if colors:
        theme["colors"] = colors

    spacing = {k: resolve(fm, v) for k, v in fm.get("spacing", {}).items()}
    if spacing:
        theme["spacing"] = spacing

    rounded = {k: resolve(fm, v) for k, v in fm.get("rounded", {}).items()}
    if rounded:
        theme["borderRadius"] = rounded

    typography = fm.get("typography", {})
    if typography:
        font_family: dict[str, list[str]] = {}
        font_size: dict[str, Any] = {}
        for name, entry in typography.items():
            if not isinstance(entry, dict):
                continue
            family = resolve(fm, entry.get("fontFamily"))
            if family:
                font_family[name] = [str(family), "system-ui", "sans-serif"]
            size = resolve(fm, entry.get("fontSize"))
            if size:
                opts = {}
                lh = resolve(fm, entry.get("lineHeight"))
                ls = resolve(fm, entry.get("letterSpacing"))
                fw = resolve(fm, entry.get("fontWeight"))
                if lh is not None:
                    opts["lineHeight"] = str(lh)
                if ls is not None:
                    opts["letterSpacing"] = str(ls)
                if fw is not None:
                    opts["fontWeight"] = str(fw)
                font_size[name] = [str(size), opts] if opts else str(size)
        if font_family:
            theme["fontFamily"] = font_family
        if font_size:
            theme["fontSize"] = font_size

    return json.dumps(theme, indent=2) + "\n"


# ---------------------------------------------------------------------------
# JSON emitter
# ---------------------------------------------------------------------------

def emit_json(fm: dict) -> str:
    keep = {"name", "description", "version", "colors", "typography",
            "spacing", "rounded", "components"}
    out = {k: resolve(fm, v) for k, v in fm.items() if k in keep}
    return json.dumps(out, indent=2) + "\n"


# ---------------------------------------------------------------------------
# SCSS emitter
# ---------------------------------------------------------------------------

def emit_scss(fm: dict) -> str:
    lines = []
    for k, v in fm.get("colors", {}).items():
        lines.append(f"$color-{kebab(k)}: {resolve(fm, v)};")
    for k, v in fm.get("spacing", {}).items():
        lines.append(f"$space-{kebab(k)}: {resolve(fm, v)};")
    for k, v in fm.get("rounded", {}).items():
        lines.append(f"$rounded-{kebab(k)}: {resolve(fm, v)};")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

EMITTERS = {
    "css": emit_css,
    "tailwind": emit_tailwind,
    "json": emit_json,
    "scss": emit_scss,
}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to DESIGN.md")
    parser.add_argument(
        "--format",
        choices=list(EMITTERS),
        default="css",
        help="Output format (default: css)",
    )
    parser.add_argument(
        "--out",
        help="Write to file instead of stdout",
    )
    args = parser.parse_args(argv)

    p = Path(args.path)
    if not p.exists():
        print(f"error: {p} does not exist", file=sys.stderr)
        return 2

    text = p.read_text(encoding="utf-8")
    try:
        fm = split_frontmatter(text)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    output = EMITTERS[args.format](fm)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
