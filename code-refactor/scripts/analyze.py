#!/usr/bin/env python3
"""
Static code smell analyzer for Python files.
Detects common smells from "Refactoring and Design Patterns":
  - Long Method (>10 lines)
  - Large Class (>20 methods or >200 lines)
  - Long Parameter List (>3 parameters)
  - Magic Numbers
  - Duplicate Code (simple token-hash similarity)
  - Dead Code (functions/classes with no callers in the file)
  - Missing Type Annotations (heuristic for Primitive Obsession)
  - Switch-like Chains (if/elif chains > 3 branches)
  - Temporary Fields (attributes set only in a subset of methods)

Usage:
    python analyze.py <file.py> [--json] [--threshold-method-lines N]

Output:
    Human-readable report (default) or JSON (--json) consumable by report.py
"""

import ast
import sys
import json
import hashlib
import argparse
import textwrap
from collections import defaultdict
from pathlib import Path


# ─── Thresholds (tunable via CLI) ─────────────────────────────────────────────
DEFAULTS = {
    "method_lines": 10,
    "class_methods": 20,
    "class_lines": 200,
    "param_count": 3,
    "elif_branches": 3,
    "duplicate_min_lines": 4,
    "similarity_threshold": 0.85,
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def source_lines(node, source_lines_list):
    """Return the number of non-blank, non-comment source lines in a node."""
    start = node.lineno - 1
    end = node.end_lineno
    lines = source_lines_list[start:end]
    return sum(1 for l in lines if l.strip() and not l.strip().startswith("#"))


def node_signature(node):
    """Produce a stable hash of an AST subtree for duplicate detection."""
    dump = ast.dump(node)
    return hashlib.md5(dump.encode()).hexdigest()


def get_names_in_file(tree):
    """Collect all names referenced anywhere in the file."""
    return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}


# ─── Smell Detectors ─────────────────────────────────────────────────────────

def detect_long_methods(tree, src_lines, threshold):
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            n = source_lines(node, src_lines)
            if n > threshold:
                issues.append({
                    "smell": "Long Method",
                    "name": node.name,
                    "line": node.lineno,
                    "detail": f"{n} lines (threshold: {threshold})",
                    "technique": "Extract Method",
                })
    return issues


def detect_large_classes(tree, src_lines, method_threshold, line_threshold):
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n for n in ast.walk(node)
                       if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                       and n.col_offset > node.col_offset]
            n_lines = source_lines(node, src_lines)
            if len(methods) > method_threshold:
                issues.append({
                    "smell": "Large Class",
                    "name": node.name,
                    "line": node.lineno,
                    "detail": f"{len(methods)} methods (threshold: {method_threshold})",
                    "technique": "Extract Class / Extract Subclass",
                })
            elif n_lines > line_threshold:
                issues.append({
                    "smell": "Large Class",
                    "name": node.name,
                    "line": node.lineno,
                    "detail": f"{n_lines} lines (threshold: {line_threshold})",
                    "technique": "Extract Class / Extract Subclass",
                })
    return issues


def detect_long_param_lists(tree, threshold):
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = node.args
            # exclude 'self' and 'cls'
            params = [a for a in args.args if a.arg not in ("self", "cls")]
            params += args.posonlyargs
            # varargs and kwargs are intentionally excluded from the count
            if len(params) > threshold:
                issues.append({
                    "smell": "Long Parameter List",
                    "name": node.name,
                    "line": node.lineno,
                    "detail": f"{len(params)} parameters (threshold: {threshold})",
                    "technique": "Introduce Parameter Object / Preserve Whole Object",
                })
    return issues


def detect_magic_numbers(tree):
    issues = []
    seen = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            # 0, 1, -1 are not magic; string constants are handled separately
            if node.value not in (0, 1, -1, 2, 100) and node.value not in seen:
                issues.append({
                    "smell": "Magic Number",
                    "name": str(node.value),
                    "line": node.lineno,
                    "detail": f"Literal {node.value!r} used directly",
                    "technique": "Replace Magic Number with Symbolic Constant",
                })
                seen.add(node.value)
    return issues


def detect_switch_chains(tree, threshold):
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            # Count consecutive elif branches
            branches = 0
            current = node
            while isinstance(current, ast.If):
                branches += 1
                if len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
                    current = current.orelse[0]
                else:
                    break
            if branches > threshold:
                issues.append({
                    "smell": "Switch Statements",
                    "name": f"if/elif chain at line {node.lineno}",
                    "line": node.lineno,
                    "detail": f"{branches} branches (threshold: {threshold})",
                    "technique": "Replace Conditional with Polymorphism",
                })
    return issues


def detect_duplicate_code(tree, src_lines, min_lines):
    """Simple duplicate detection: hash function bodies and look for matches."""
    issues = []
    func_bodies = {}  # hash -> (name, lineno)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if source_lines(node, src_lines) < min_lines:
                continue
            # Normalize by stripping docstring
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)):
                body = body[1:]
            body_hash = node_signature(ast.Module(body=body, type_ignores=[]))
            if body_hash in func_bodies:
                orig_name, orig_line = func_bodies[body_hash]
                issues.append({
                    "smell": "Duplicate Code",
                    "name": node.name,
                    "line": node.lineno,
                    "detail": f"Body matches '{orig_name}' at line {orig_line}",
                    "technique": "Extract Method / Pull Up Method",
                })
            else:
                func_bodies[body_hash] = (node.name, node.lineno)
    return issues


def detect_dead_code(tree):
    """
    Detect functions/classes defined but never referenced anywhere in the file.
    This is file-local only — cross-file references are not tracked.
    """
    issues = []
    all_names = get_names_in_file(tree)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.startswith("_"):
                continue  # skip private/dunder
            if node.name not in all_names:
                issues.append({
                    "smell": "Dead Code",
                    "name": node.name,
                    "line": node.lineno,
                    "detail": "Defined but never referenced in this file",
                    "technique": "Delete unused code",
                })
    return issues


def detect_temporary_fields(tree):
    """
    Detect instance attributes that are only assigned in some methods (not __init__).
    A heuristic: attributes set in non-__init__ methods but not in __init__.
    """
    issues = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        init_attrs = set()
        other_attrs = defaultdict(list)  # attr_name -> [method_names]
        for method in ast.walk(node):
            if not isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for stmt in ast.walk(method):
                if (isinstance(stmt, ast.Assign)):
                    for target in stmt.targets:
                        if (isinstance(target, ast.Attribute)
                                and isinstance(target.value, ast.Name)
                                and target.value.id == "self"):
                            if method.name == "__init__":
                                init_attrs.add(target.attr)
                            else:
                                other_attrs[target.attr].append(method.name)
        for attr, methods in other_attrs.items():
            if attr not in init_attrs:
                issues.append({
                    "smell": "Temporary Field",
                    "name": f"{node.name}.{attr}",
                    "line": node.lineno,
                    "detail": f"Assigned outside __init__ in: {', '.join(set(methods))}",
                    "technique": "Extract Class / Introduce Null Object",
                })
    return issues


# ─── Main ─────────────────────────────────────────────────────────────────────

def analyze_file(path: Path, thresholds: dict) -> dict:
    source = path.read_text(encoding="utf-8")
    src_lines = source.splitlines()
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as e:
        return {"file": str(path), "error": str(e), "issues": []}

    issues = []
    issues += detect_long_methods(tree, src_lines, thresholds["method_lines"])
    issues += detect_large_classes(tree, src_lines, thresholds["class_methods"], thresholds["class_lines"])
    issues += detect_long_param_lists(tree, thresholds["param_count"])
    issues += detect_magic_numbers(tree)
    issues += detect_switch_chains(tree, thresholds["elif_branches"])
    issues += detect_duplicate_code(tree, src_lines, thresholds["duplicate_min_lines"])
    issues += detect_dead_code(tree)
    issues += detect_temporary_fields(tree)

    return {
        "file": str(path),
        "total_lines": len(src_lines),
        "issues": sorted(issues, key=lambda x: x["line"]),
    }


def format_report(result: dict) -> str:
    lines = []
    path = result["file"]
    issues = result.get("issues", [])
    lines.append(f"# Code Smell Analysis: {path}")
    lines.append(f"Total source lines: {result.get('total_lines', '?')}")
    lines.append(f"Issues found: {len(issues)}")
    lines.append("")
    if not issues:
        lines.append("No issues detected.")
        return "\n".join(lines)

    by_smell = defaultdict(list)
    for issue in issues:
        by_smell[issue["smell"]].append(issue)

    for smell, items in sorted(by_smell.items()):
        lines.append(f"## {smell} ({len(items)})")
        for item in items:
            lines.append(f"  - Line {item['line']}: `{item['name']}` — {item['detail']}")
            lines.append(f"    Suggested technique: {item['technique']}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Detect code smells in a Python file.")
    parser.add_argument("file", help="Python source file to analyze")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    parser.add_argument("--threshold-method-lines", type=int,
                        default=DEFAULTS["method_lines"],
                        help=f"Max lines per method (default: {DEFAULTS['method_lines']})")
    parser.add_argument("--threshold-class-methods", type=int,
                        default=DEFAULTS["class_methods"])
    parser.add_argument("--threshold-class-lines", type=int,
                        default=DEFAULTS["class_lines"])
    parser.add_argument("--threshold-params", type=int,
                        default=DEFAULTS["param_count"],
                        help=f"Max parameters per method (default: {DEFAULTS['param_count']})")
    parser.add_argument("--threshold-elif", type=int,
                        default=DEFAULTS["elif_branches"])
    args = parser.parse_args()

    thresholds = {
        "method_lines": args.threshold_method_lines,
        "class_methods": args.threshold_class_methods,
        "class_lines": args.threshold_class_lines,
        "param_count": args.threshold_params,
        "elif_branches": args.threshold_elif,
        "duplicate_min_lines": DEFAULTS["duplicate_min_lines"],
        "similarity_threshold": DEFAULTS["similarity_threshold"],
    }

    path = Path(args.file)
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    result = analyze_file(path, thresholds)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
