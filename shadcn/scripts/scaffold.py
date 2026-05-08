#!/usr/bin/env python3
"""
Scaffold shadcn/ui page templates into a target file.

Usage:
  python scripts/scaffold.py --template dashboard --output src/app/dashboard/page.tsx
  python scripts/scaffold.py --template auth --output src/app/login/page.tsx
  python scripts/scaffold.py --template data-table --output src/app/users/page.tsx
  python scripts/scaffold.py --template settings --output src/app/settings/page.tsx
  python scripts/scaffold.py --list
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

TEMPLATE_MAP = {
    "dashboard": "dashboard-layout.tsx",
    "auth": "auth-page.tsx",
    "login": "auth-page.tsx",
    "data-table": "data-table-page.tsx",
    "table": "data-table-page.tsx",
    "settings": "settings-page.tsx",
}

TEMPLATE_DESCRIPTIONS = {
    "dashboard": "Full dashboard with sidebar, header, stats cards, and chart",
    "auth": "Login / sign-up page with tabs and form validation",
    "data-table": "Sortable, filterable data table with TanStack Table",
    "settings": "Settings page with tabs, forms, switches, and selects",
}

TEMPLATE_DEPS = {
    "dashboard": "npx shadcn@latest add card badge avatar separator button sonner sidebar chart",
    "auth": "npx shadcn@latest add card input label button tabs form\nnpm install react-hook-form zod @hookform/resolvers",
    "data-table": "npx shadcn@latest add table button input badge dropdown-menu\nnpm install @tanstack/react-table",
    "settings": "npx shadcn@latest add tabs card input label button switch select separator",
}


def list_templates():
    print("\nAvailable templates:")
    print("=" * 48)
    for name, desc in TEMPLATE_DESCRIPTIONS.items():
        print(f"  {name:<14}  {desc}")
    print()
    print("Usage:")
    print("  python scripts/scaffold.py --template <name> --output <path>")
    print()


def scaffold(template_name: str, output_path: str, force: bool = False):
    # Resolve template filename
    filename = TEMPLATE_MAP.get(template_name)
    if filename is None:
        print(f"✗  Unknown template: '{template_name}'")
        print(f"   Run with --list to see available templates.")
        sys.exit(1)

    template_file = TEMPLATES_DIR / filename
    if not template_file.exists():
        print(f"✗  Template file not found: {template_file}")
        print(f"   Expected at: {template_file.resolve()}")
        sys.exit(1)

    dest = Path(output_path)

    # Check if destination exists
    if dest.exists() and not force:
        print(f"✗  File already exists: {dest}")
        print(f"   Use --force to overwrite.")
        sys.exit(1)

    # Create parent directories
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Copy template
    shutil.copy2(template_file, dest)

    canonical_name = template_name if template_name in TEMPLATE_DEPS else "dashboard"
    deps = TEMPLATE_DEPS.get(canonical_name, "")

    print(f"\n✓  Scaffolded {template_name} template → {dest}")
    print()
    if deps:
        print("Required components — install with:")
        for line in deps.splitlines():
            print(f"  {line}")
    print()
    print("Next steps:")
    print(f"  1. Install the components listed above")
    print(f"  2. Open {dest} and customize for your data/routes")
    print(f"  3. Import and render in your router/page")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold shadcn/ui page templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--template", "-t", help="Template name (see --list)")
    parser.add_argument("--output", "-o", help="Destination file path")
    parser.add_argument("--force", "-f", action="store_true", help="Overwrite if exists")
    parser.add_argument("--list", "-l", action="store_true", help="List available templates")

    args = parser.parse_args()

    if args.list or (not args.template and not args.output):
        list_templates()
        sys.exit(0)

    if not args.template:
        print("✗  --template is required. Use --list to see options.")
        sys.exit(1)

    if not args.output:
        # Default output path based on template name
        defaults = {
            "dashboard": "src/app/dashboard/page.tsx",
            "auth": "src/app/login/page.tsx",
            "login": "src/app/login/page.tsx",
            "data-table": "src/app/data/page.tsx",
            "table": "src/app/data/page.tsx",
            "settings": "src/app/settings/page.tsx",
        }
        args.output = defaults.get(args.template, f"src/app/{args.template}/page.tsx")
        print(f"ℹ  No --output specified. Using default: {args.output}")

    scaffold(args.template, args.output, args.force)


if __name__ == "__main__":
    main()
