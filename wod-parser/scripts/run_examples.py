#!/usr/bin/env python3
"""
Run the parser against assets/examples.jsonl and verify each output:
  1. matches the stored expected output exactly, AND
  2. validates against templates/schema.json.

Exit code 0 on full pass, 1 on any mismatch or schema violation.

Usage:
    python3 scripts/run_examples.py
    python3 scripts/run_examples.py --update    # rewrite expected outputs from current parser
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from parse_wod import parse  # noqa: E402
from validate import validate  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true", help="Overwrite expected outputs in examples.jsonl")
    args = ap.parse_args()

    examples_path = ROOT / "assets" / "examples.jsonl"
    schema = json.loads((ROOT / "templates" / "schema.json").read_text())

    rows = [json.loads(line) for line in examples_path.read_text().splitlines() if line.strip()]
    fails = 0
    updated = []
    for i, row in enumerate(rows):
        actual = parse(row["input"])
        errs = validate(actual, schema)
        if errs:
            fails += 1
            print(f"#{i+1} schema errors:", file=sys.stderr)
            for e in errs:
                print("  " + e, file=sys.stderr)
        if not args.update and actual != row["expected"]:
            fails += 1
            print(f"#{i+1} mismatch", file=sys.stderr)
            print(f"  expected: {json.dumps(row['expected'])}", file=sys.stderr)
            print(f"  actual:   {json.dumps(actual)}", file=sys.stderr)
        updated.append({"input": row["input"], "expected": actual})

    if args.update:
        with examples_path.open("w") as f:
            for row in updated:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"updated {len(updated)} examples")
        return 0

    if fails:
        print(f"FAIL: {fails} issue(s) across {len(rows)} examples", file=sys.stderr)
        return 1
    print(f"OK: {len(rows)} examples pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
