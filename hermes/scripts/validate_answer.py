#!/usr/bin/env python3
"""Validate that a Hermes skill response meets the 255-character limit and format rules."""

import sys
import re


def validate(response: str) -> dict:
    char_count = len(response)
    length_ok = char_count <= 255

    # Check for disallowed markdown (headers and bullet lists at line start)
    has_headers = bool(re.search(r"^#{1,6}\s", response, re.MULTILINE))
    has_bullets = bool(re.search(r"^[\-\*]\s", response, re.MULTILINE))
    format_ok = not has_headers and not has_bullets

    # Check for filler phrases
    filler_patterns = [
        r"^Sure[!,]",
        r"^Great question",
        r"^Of course",
        r"^Absolutely",
        r"I hope this helps",
        r"Feel free to ask",
    ]
    has_filler = any(re.search(p, response, re.IGNORECASE) for p in filler_patterns)

    passed = length_ok and format_ok and not has_filler

    return {
        "passed": passed,
        "char_count": char_count,
        "length_ok": length_ok,
        "format_ok": format_ok,
        "has_filler": has_filler,
        "issues": [
            *(["Too long ({} chars, max 255)".format(char_count)] if not length_ok else []),
            *(["Contains markdown headers"] if has_headers else []),
            *(["Contains bullet lists"] if has_bullets else []),
            *(["Contains filler phrases"] if has_filler else []),
        ],
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_answer.py '<response text>'")
        print("       echo '<response>' | validate_answer.py -")
        sys.exit(1)

    if sys.argv[1] == "-":
        response = sys.stdin.read().strip()
    else:
        response = sys.argv[1]

    result = validate(response)

    status = "PASS" if result["passed"] else "FAIL"
    print(f"[{status}] {result['char_count']} chars")

    if result["issues"]:
        for issue in result["issues"]:
            print(f"  - {issue}")
    else:
        print("  All checks passed.")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
