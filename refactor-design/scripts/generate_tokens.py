#!/usr/bin/env python3
"""
Generate a complete design token system from a palette configuration.

Produces CSS custom properties, a Tailwind config, or a JS token object
covering: colors, spacing, type scale, shadows, radii, and transitions.

Usage:
    python generate_tokens.py --primary-hue 220 --format css
    python generate_tokens.py --primary-hue 220 --format tailwind --output tailwind.config.js
    python generate_tokens.py --primary-hue 220 --accent-hue 280 --format js

Arguments:
    --primary-hue   Hue for the primary/brand color (0-360)
    --gray-hue      Hue tint for greys (default: same as primary, for cool greys)
    --accent-hue    Optional second accent color
    --format        css | tailwind | js (default: css)
    --output        Output file path (default: stdout)
"""

import argparse
import sys
from color_palette import generate_palette  # co-located script


# ---------------------------------------------------------------------------
# Spacing scale (base-4, geometric)
# ---------------------------------------------------------------------------
SPACING = {
    "0": "0px",
    "px": "1px",
    "0.5": "0.125rem",   # 2px
    "1": "0.25rem",      # 4px
    "1.5": "0.375rem",   # 6px
    "2": "0.5rem",       # 8px
    "2.5": "0.625rem",   # 10px
    "3": "0.75rem",      # 12px
    "3.5": "0.875rem",   # 14px
    "4": "1rem",         # 16px
    "5": "1.25rem",      # 20px
    "6": "1.5rem",       # 24px
    "7": "1.75rem",      # 28px
    "8": "2rem",         # 32px
    "10": "2.5rem",      # 40px
    "12": "3rem",        # 48px
    "14": "3.5rem",      # 56px
    "16": "4rem",        # 64px
    "20": "5rem",        # 80px
    "24": "6rem",        # 96px
    "28": "7rem",        # 112px
    "32": "8rem",        # 128px
    "40": "10rem",       # 160px
    "48": "12rem",       # 192px
    "56": "14rem",       # 224px
    "64": "16rem",       # 256px
}

# ---------------------------------------------------------------------------
# Type scale
# ---------------------------------------------------------------------------
FONT_SIZES = {
    "xs":   ("0.75rem",   {"lineHeight": "1rem"}),       # 12px
    "sm":   ("0.875rem",  {"lineHeight": "1.25rem"}),    # 14px
    "base": ("1rem",      {"lineHeight": "1.625rem"}),   # 16px
    "lg":   ("1.125rem",  {"lineHeight": "1.75rem"}),    # 18px
    "xl":   ("1.25rem",   {"lineHeight": "1.75rem"}),    # 20px
    "2xl":  ("1.5rem",    {"lineHeight": "2rem"}),       # 24px
    "3xl":  ("1.875rem",  {"lineHeight": "2.25rem"}),    # 30px
    "4xl":  ("2.25rem",   {"lineHeight": "2.5rem"}),     # 36px
    "5xl":  ("3rem",      {"lineHeight": "1"}),          # 48px
    "6xl":  ("3.75rem",   {"lineHeight": "1"}),          # 60px
}

FONT_WEIGHTS = {
    "normal":   "400",
    "medium":   "500",
    "semibold": "600",
    "bold":     "700",
    "extrabold":"800",
    "black":    "900",
}

LETTER_SPACINGS = {
    "tighter": "-0.05em",
    "tight":   "-0.025em",
    "normal":  "0em",
    "wide":    "0.025em",
    "wider":   "0.05em",
    "widest":  "0.1em",
}

# ---------------------------------------------------------------------------
# Border radius
# ---------------------------------------------------------------------------
BORDER_RADIUS = {
    "none":  "0px",
    "sm":    "2px",
    "DEFAULT": "4px",
    "md":    "6px",
    "lg":    "8px",
    "xl":    "12px",
    "2xl":   "16px",
    "3xl":   "24px",
    "full":  "9999px",
}

# ---------------------------------------------------------------------------
# Shadows  (using a dark navy tint instead of pure black)
# ---------------------------------------------------------------------------
def build_shadows(shadow_hue: int = 220) -> dict:
    h = shadow_hue
    return {
        "sm": f"0 1px 2px 0 hsl({h} 40% 10% / 0.06)",
        "DEFAULT": f"0 1px 3px 0 hsl({h} 40% 10% / 0.10), 0 1px 2px -1px hsl({h} 40% 10% / 0.10)",
        "md": f"0 4px 6px -1px hsl({h} 40% 10% / 0.10), 0 2px 4px -2px hsl({h} 40% 10% / 0.10)",
        "lg": f"0 10px 15px -3px hsl({h} 40% 10% / 0.10), 0 4px 6px -4px hsl({h} 40% 10% / 0.10)",
        "xl": f"0 20px 25px -5px hsl({h} 40% 10% / 0.10), 0 8px 10px -6px hsl({h} 40% 10% / 0.10)",
        "2xl": f"0 25px 50px -12px hsl({h} 40% 10% / 0.25)",
        "inner": f"inset 0 2px 4px 0 hsl({h} 40% 10% / 0.06)",
        "none": "none",
    }

# ---------------------------------------------------------------------------
# Transitions
# ---------------------------------------------------------------------------
TRANSITION_DURATION = {
    "75":  "75ms",
    "100": "100ms",
    "150": "150ms",
    "200": "200ms",
    "300": "300ms",
    "500": "500ms",
    "700": "700ms",
    "1000": "1000ms",
}

TRANSITION_TIMING = {
    "DEFAULT": "cubic-bezier(0.4, 0, 0.2, 1)",
    "linear": "linear",
    "in": "cubic-bezier(0.4, 0, 1, 1)",
    "out": "cubic-bezier(0, 0, 0.2, 1)",
    "in-out": "cubic-bezier(0.4, 0, 0.2, 1)",
    "spring": "cubic-bezier(0.175, 0.885, 0.32, 1.275)",
}

# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

def palette_to_css_vars(name: str, palette: dict) -> str:
    lines = []
    for shade, (h, s, l) in sorted(palette.items()):
        lines.append(f"  --color-{name}-{shade}: hsl({h} {s}% {l}%);")
    return "\n".join(lines)


def palette_to_tailwind(name: str, palette: dict) -> str:
    lines = [f"      {name}: {{"]
    for shade, (h, s, l) in sorted(palette.items()):
        lines.append(f"        {shade}: 'hsl({h} {s}% {l}%)',")
    lines.append("      },")
    return "\n".join(lines)


def generate_css(primary_hue: int, gray_hue: int, accent_hue: int | None) -> str:
    primary = generate_palette(primary_hue, base_saturation=70)
    gray = generate_palette(gray_hue, base_saturation=8, is_grey=True)
    green = generate_palette(142, base_saturation=69)
    red = generate_palette(0, base_saturation=72)
    amber = generate_palette(38, base_saturation=92)
    blue = generate_palette(217, base_saturation=91)

    palettes = [
        ("primary", primary),
        ("gray", gray),
        ("green", green),
        ("red", red),
        ("amber", amber),
        ("blue", blue),
    ]
    if accent_hue is not None:
        accent = generate_palette(accent_hue, base_saturation=70)
        palettes.append(("accent", accent))

    shadows = build_shadows(gray_hue)

    lines = ["/* Design Tokens — generated by refactor-design/scripts/generate_tokens.py */", "", ":root {", "  /* ── Color Palettes ────────────────────────── */"]
    for name, palette in palettes:
        lines.append(f"\n  /* {name} */")
        lines.append(palette_to_css_vars(name, palette))

    lines.append("\n  /* ── Semantic Color Roles ──────────────────── */")
    lines.extend([
        "  --color-text-primary:   var(--color-gray-900);",
        "  --color-text-secondary: var(--color-gray-600);",
        "  --color-text-tertiary:  var(--color-gray-400);",
        "  --color-text-disabled:  var(--color-gray-300);",
        "  --color-text-inverse:   var(--color-gray-50);",
        "",
        "  --color-bg-base:    var(--color-gray-50);",
        "  --color-bg-surface: #ffffff;",
        "  --color-bg-subtle:  var(--color-gray-100);",
        "",
        "  --color-border:       var(--color-gray-200);",
        "  --color-border-strong:var(--color-gray-300);",
        "  --color-border-focus: var(--color-primary-500);",
        "",
        "  --color-action:       var(--color-primary-600);",
        "  --color-action-hover: var(--color-primary-700);",
        "  --color-danger:       var(--color-red-600);",
        "  --color-success:      var(--color-green-600);",
        "  --color-warning:      var(--color-amber-500);",
    ])

    lines.append("\n  /* ── Spacing ───────────────────────────────── */")
    for k, v in SPACING.items():
        if k not in ("0", "px"):
            lines.append(f"  --space-{k.replace('.', '_')}: {v};")

    lines.append("\n  /* ── Typography ────────────────────────────── */")
    for k, (size, _) in FONT_SIZES.items():
        lines.append(f"  --text-{k}: {size};")

    lines.append("\n  /* ── Border Radius ─────────────────────────── */")
    for k, v in BORDER_RADIUS.items():
        key = k.replace("DEFAULT", "base")
        lines.append(f"  --radius-{key}: {v};")

    lines.append("\n  /* ── Shadows ───────────────────────────────── */")
    for k, v in shadows.items():
        key = k.replace("DEFAULT", "base")
        lines.append(f"  --shadow-{key}: {v};")

    lines.append("\n  /* ── Focus Ring ────────────────────────────── */")
    lines.extend([
        "  --ring-color:  var(--color-primary-500);",
        "  --ring-width:  2px;",
        "  --ring-offset: 2px;",
    ])

    lines.append("\n  /* ── Transitions ───────────────────────────── */")
    for k, v in TRANSITION_DURATION.items():
        lines.append(f"  --duration-{k}: {v};")
    for k, v in TRANSITION_TIMING.items():
        key = k.replace("DEFAULT", "ease")
        lines.append(f"  --ease-{key}: {v};")

    lines.append("}")
    return "\n".join(lines)


def generate_tailwind(primary_hue: int, gray_hue: int, accent_hue: int | None) -> str:
    primary = generate_palette(primary_hue, base_saturation=70)
    gray = generate_palette(gray_hue, base_saturation=8, is_grey=True)
    green = generate_palette(142, base_saturation=69)
    red = generate_palette(0, base_saturation=72)
    amber = generate_palette(38, base_saturation=92)
    blue = generate_palette(217, base_saturation=91)
    shadows = build_shadows(gray_hue)

    palettes = [
        ("primary", primary),
        ("gray", gray),
        ("green", green),
        ("red", red),
        ("amber", amber),
        ("blue", blue),
    ]
    if accent_hue:
        accent = generate_palette(accent_hue, base_saturation=70)
        palettes.append(("accent", accent))

    color_lines = []
    for name, pal in palettes:
        color_lines.append(palette_to_tailwind(name, pal))

    shadow_lines = []
    for k, v in shadows.items():
        shadow_lines.append(f"      '{k}': '{v}',")

    spacing_lines = []
    for k, v in SPACING.items():
        spacing_lines.append(f"      '{k}': '{v}',")

    fs_lines = []
    for k, (size, meta) in FONT_SIZES.items():
        lh = meta.get("lineHeight", "1.5")
        fs_lines.append(f"      {k}: ['{size}', {{ lineHeight: '{lh}' }}],")

    br_lines = []
    for k, v in BORDER_RADIUS.items():
        br_lines.append(f"      {k}: '{v}',")

    return f"""// tailwind.config.js — generated by refactor-design/scripts/generate_tokens.py
/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: ['./src/**/*.{{js,ts,jsx,tsx,html}}'],
  theme: {{
    extend: {{
      colors: {{
{chr(10).join(color_lines)}
      }},
      spacing: {{
{chr(10).join(spacing_lines)}
      }},
      fontSize: {{
{chr(10).join(fs_lines)}
      }},
      fontWeight: {{
        normal:    '400',
        medium:    '500',
        semibold:  '600',
        bold:      '700',
        extrabold: '800',
        black:     '900',
      }},
      borderRadius: {{
{chr(10).join(br_lines)}
      }},
      boxShadow: {{
{chr(10).join(shadow_lines)}
      }},
      letterSpacing: {{
        tighter: '-0.05em',
        tight:   '-0.025em',
        normal:  '0em',
        wide:    '0.025em',
        wider:   '0.05em',
        widest:  '0.1em',
      }},
      transitionDuration: {{
        '75': '75ms',
        '100': '100ms',
        '150': '150ms',
        '200': '200ms',
        '300': '300ms',
        '500': '500ms',
      }},
    }},
  }},
  plugins: [],
}};
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate design tokens from a palette config.")
    parser.add_argument("--primary-hue", type=int, default=220, help="Primary hue (0-360)")
    parser.add_argument("--gray-hue", type=int, default=None, help="Grey tint hue (default: primary-hue)")
    parser.add_argument("--accent-hue", type=int, default=None, help="Optional accent hue")
    parser.add_argument("--format", "-f", choices=["css", "tailwind", "js"], default="css")
    parser.add_argument("--output", "-o", type=str, default=None)
    args = parser.parse_args()

    gray_hue = args.gray_hue if args.gray_hue is not None else args.primary_hue

    if args.format == "css":
        output = generate_css(args.primary_hue, gray_hue, args.accent_hue)
    elif args.format == "tailwind":
        output = generate_tailwind(args.primary_hue, gray_hue, args.accent_hue)
    else:
        print("JS format: convert the CSS output to a JS object manually or use --format tailwind.", file=sys.stderr)
        return 1

    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(f"Written to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
