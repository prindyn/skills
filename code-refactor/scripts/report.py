#!/usr/bin/env python3
"""
Render a JSON analysis result (from analyze.py --json) into a structured
Markdown refactoring report.

Usage:
    python analyze.py myfile.py --json | python report.py
    python report.py analysis.json
    python report.py analysis.json --output report.md

The report sections follow the review-report.md template.
"""

import sys
import json
import argparse
from collections import defaultdict
from datetime import date
from pathlib import Path


SMELL_PRIORITY = {
    # Change preventers and couplers → highest urgency
    "Feature Envy": 1,
    "Inappropriate Intimacy": 1,
    "Switch Statements": 1,
    "Divergent Change": 1,
    "Shotgun Surgery": 1,
    # Bloaters → high urgency
    "Long Method": 2,
    "Large Class": 2,
    "Long Parameter List": 2,
    "Data Clumps": 2,
    # OO abusers
    "Temporary Field": 3,
    "Refused Bequest": 3,
    # Dispensables
    "Duplicate Code": 3,
    "Magic Number": 3,
    "Dead Code": 4,
    "Lazy Class": 4,
    "Speculative Generality": 4,
    # Fallback
    "Message Chains": 3,
    "Middle Man": 4,
}

PRIORITY_LABEL = {1: "Critical", 2: "High", 3: "Medium", 4: "Low"}


def priority_of(smell_name: str) -> int:
    return SMELL_PRIORITY.get(smell_name, 3)


def generate_report(result: dict) -> str:
    file_path = result.get("file", "unknown")
    total_lines = result.get("total_lines", "?")
    issues = result.get("issues", [])
    today = date.today().isoformat()

    lines = []

    # Header
    lines += [
        f"# Code Refactoring Report",
        f"",
        f"**File:** `{file_path}`  ",
        f"**Date:** {today}  ",
        f"**Total lines analyzed:** {total_lines}  ",
        f"**Issues found:** {len(issues)}  ",
        "",
    ]

    if not issues:
        lines.append("No code smells detected. The code looks clean.")
        return "\n".join(lines)

    # Executive summary
    by_priority = defaultdict(list)
    for issue in issues:
        p = priority_of(issue["smell"])
        by_priority[p].append(issue)

    lines += ["## Executive Summary", ""]
    for p in sorted(by_priority.keys()):
        label = PRIORITY_LABEL[p]
        count = len(by_priority[p])
        lines.append(f"- **{label}:** {count} issue(s)")
    lines.append("")

    # Issues by priority
    lines += ["## Issues by Priority", ""]
    for p in sorted(by_priority.keys()):
        label = PRIORITY_LABEL[p]
        items = by_priority[p]
        lines += [f"### {label} Priority", ""]
        by_smell = defaultdict(list)
        for item in items:
            by_smell[item["smell"]].append(item)
        for smell, smell_items in sorted(by_smell.items()):
            lines += [f"#### {smell}", ""]
            for item in smell_items:
                lines.append(f"- **Line {item['line']}** — `{item['name']}`")
                lines.append(f"  - *Detail:* {item['detail']}")
                lines.append(f"  - *Recommended technique:* {item['technique']}")
            lines.append("")

    # Refactoring plan
    lines += ["## Recommended Refactoring Plan", ""]
    lines += [
        "Apply refactorings in this order (safest first):",
        "",
    ]
    step = 1
    for p in sorted(by_priority.keys()):
        label = PRIORITY_LABEL[p]
        items = by_priority[p]
        # Deduplicate by technique
        seen_techniques = set()
        for item in items:
            if item["technique"] not in seen_techniques:
                lines.append(
                    f"{step}. [{label}] Apply **{item['technique']}** "
                    f"— addresses `{item['name']}` (line {item['line']})"
                )
                seen_techniques.add(item["technique"])
                step += 1
    lines.append("")

    # Principles reminder
    lines += [
        "## Refactoring Checklist",
        "",
        "- [ ] Tests exist and pass before starting",
        "- [ ] Each refactoring step is small and independently tested",
        "- [ ] New functionality is NOT added during refactoring",
        "- [ ] All existing tests pass after each step",
        "- [ ] Code is cleaner after than before",
        "",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Render analyze.py JSON output as a Markdown report."
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="JSON file from analyze.py --json (default: stdin)",
    )
    parser.add_argument(
        "--output",
        help="Output Markdown file (default: stdout)",
    )
    args = parser.parse_args()

    if args.input:
        data = json.loads(Path(args.input).read_text())
    else:
        data = json.load(sys.stdin)

    # Handle both single-file result and list of results
    if isinstance(data, list):
        reports = [generate_report(r) for r in data]
        report = "\n\n---\n\n".join(reports)
    else:
        report = generate_report(data)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
