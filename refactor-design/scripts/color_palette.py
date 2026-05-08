#!/usr/bin/env python3
"""
Generate a production-ready HSL color palette from a base hue.

Usage:
    python color_palette.py --hue 220 --name blue
    python color_palette.py --hue 220 --name blue --format tailwind
    python color_palette.py --hue 220 --name blue --format css
    python color_palette.py --hue 220 --name blue --format js
    python color_palette.py --hue 220 --name blue --saturation 80

Based on Refactoring UI principles:
- Light shades need higher saturation to avoid looking washed out.
- Saturation peaks at shade 50 and 600-700, dips at 400-500 (base).
- Greys work best with a slight tint (2-8% saturation).
"""

import argparse
import json
import sys


# Shade lightness targets (0-100 scale)
SHADE_LIGHTNESS = {
    50:  96,
    100: 91,
    200: 84,
    300: 73,
    400: 62,
    500: 50,
    600: 40,
    700: 31,
    800: 22,
    900: 15,
}

# Saturation multipliers per shade (applied to base saturation)
# Light shades boosted, mid-range slightly reduced, darks boosted again
SHADE_SAT_MULTIPLIER = {
    50:  1.35,
    100: 1.20,
    200: 1.10,
    300: 1.00,
    400: 0.90,
    500: 1.00,  # base
    600: 1.05,
    700: 1.10,
    800: 1.05,
    900: 1.00,
}


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def generate_palette(
    hue: int,
    base_saturation: int = 70,
    is_grey: bool = False,
) -> dict[int, tuple[int, int, int]]:
    """Return {shade: (h, s, l)} for all 9 shades."""
    palette = {}
    for shade, lightness in SHADE_LIGHTNESS.items():
        if is_grey:
            # Greys use very low saturation with a slight tint
            sat = clamp(base_saturation, 0, 15)
        else:
            multiplier = SHADE_SAT_MULTIPLIER[shade]
            sat = clamp(base_saturation * multiplier, 5, 100)
        palette[shade] = (hue, int(round(sat)), lightness)
    return palette


def format_css_vars(name: str, palette: dict) -> str:
    lines = [f"  /* {name} */"]
    for shade, (h, s, l) in sorted(palette.items()):
        lines.append(f"  --{name}-{shade}: hsl({h}, {s}%, {l}%);")
    return "\n".join(lines)


def format_tailwind(name: str, palette: dict) -> str:
    lines = [f"        {name}: {{"]
    for shade, (h, s, l) in sorted(palette.items()):
        lines.append(f"          {shade}: 'hsl({h}, {s}%, {l}%)',")
    lines.append("        },")
    return "\n".join(lines)


def format_js_object(name: str, palette: dict) -> str:
    lines = [f"  {name}: {{"]
    for shade, (h, s, l) in sorted(palette.items()):
        lines.append(f"    {shade}: 'hsl({h}, {s}%, {l}%)',")
    lines.append("  },")
    return "\n".join(lines)


def format_json(name: str, palette: dict) -> str:
    obj = {name: {str(shade): f"hsl({h}, {s}%, {l}%)" for shade, (h, s, l) in sorted(palette.items())}}
    return json.dumps(obj, indent=2)


def print_preview(name: str, palette: dict) -> None:
    """Print an ANSI-colored preview of the palette (terminal only)."""
    print(f"\n  Palette: {name}")
    for shade, (h, s, l) in sorted(palette.items()):
        # ANSI approximation: use background color if terminal supports it
        label = f"  {shade:4d}  hsl({h:3d}, {s:3d}%, {l:3d}%)"
        print(label)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate an HSL color palette from a base hue."
    )
    parser.add_argument(
        "--hue", "-H", type=int, required=True,
        help="Base hue (0-360). e.g. 220 for blue, 142 for green, 0 for red."
    )
    parser.add_argument(
        "--name", "-n", type=str, default="color",
        help="Name for the palette (e.g. 'blue', 'primary', 'brand')."
    )
    parser.add_argument(
        "--saturation", "-s", type=int, default=70,
        help="Base saturation for shade-500 (default: 70). Use 5-10 for greys."
    )
    parser.add_argument(
        "--grey", action="store_true",
        help="Generate a grey-scale palette (very low saturation)."
    )
    parser.add_argument(
        "--format", "-f",
        choices=["css", "tailwind", "js", "json", "preview"],
        default="preview",
        help="Output format (default: preview)."
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Write output to this file (default: stdout)."
    )

    args = parser.parse_args()

    if not 0 <= args.hue <= 360:
        print("Error: --hue must be between 0 and 360.", file=sys.stderr)
        return 1

    if not 0 <= args.saturation <= 100:
        print("Error: --saturation must be between 0 and 100.", file=sys.stderr)
        return 1

    palette = generate_palette(
        hue=args.hue,
        base_saturation=args.saturation,
        is_grey=args.grey,
    )

    if args.format == "css":
        output = ":root {\n" + format_css_vars(args.name, palette) + "\n}"
    elif args.format == "tailwind":
        output = (
            "// tailwind.config.js — paste into theme.extend.colors\n"
            "colors: {\n"
            + format_tailwind(args.name, palette)
            + "\n},"
        )
    elif args.format == "js":
        output = "export const colors = {\n" + format_js_object(args.name, palette) + "\n};"
    elif args.format == "json":
        output = format_json(args.name, palette)
    else:  # preview
        print_preview(args.name, palette)
        # Also print CSS for reference
        output = ":root {\n" + format_css_vars(args.name, palette) + "\n}"
        print()

    if args.output:
        with open(args.output, "w") as f:
            f.write(output + "\n")
        print(f"Written to {args.output}")
    else:
        print(output)

    return 0


# Convenience function for use as a library
def build_palette(hue: int, name: str = "color", saturation: int = 70, grey: bool = False) -> dict:
    """Return a dict of {shade_name: 'hsl(h, s%, l%)'} suitable for JSON serialization."""
    palette = generate_palette(hue=hue, base_saturation=saturation, is_grey=grey)
    return {f"{name}-{shade}": f"hsl({h}, {s}%, {l}%)" for shade, (h, s, l) in sorted(palette.items())}


if __name__ == "__main__":
    sys.exit(main())
