#!/usr/bin/env python3
# /// script
# dependencies = ["jsonschema>=4.0"]
# ///
"""
Validate a Hermes <tool_call> block against a tool schema definition.

Use this to confirm that the model's function call:
  1. Is syntactically valid JSON
  2. References a tool that exists in your tool list
  3. Passes JSON Schema validation for the tool's parameters
  4. Includes all required parameters
  5. Doesn't include unknown parameters

Usage:
    # Validate a raw tool_call string
    uv run scripts/validate_function_call.py \\
        --call '<tool_call>{"name":"get_weather","arguments":{"location":"Paris"}}</tool_call>' \\
        --tools tools.json

    # Validate JSON directly (without XML wrapper)
    uv run scripts/validate_function_call.py \\
        --call '{"name":"get_weather","arguments":{"location":"Paris"}}' \\
        --tools tools.json

    # Validate all tool calls found in a model response
    uv run scripts/validate_function_call.py \\
        --response response.txt \\
        --tools tools.json

Exit codes:
    0  All calls valid
    1  One or more validation errors
    2  Input error (bad JSON, missing file, etc.)
"""

import argparse
import json
import re
import sys

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def extract_tool_calls_from_text(text: str) -> list[str]:
    """Extract all <tool_call>...</tool_call> blocks from text."""
    pattern = r"<tool_call>\s*(.*?)\s*</tool_call>"
    return re.findall(pattern, text, re.DOTALL)


def parse_tool_call(raw: str) -> dict:
    """Parse a tool call string (with or without XML wrapper) into a dict."""
    # Strip XML wrapper if present
    stripped = re.sub(r"</?tool_call>", "", raw).strip()
    return json.loads(stripped)


def load_tools(path: str) -> list[dict]:
    """Load a tools JSON array from a file."""
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "tools" in data:
        return data["tools"]
    raise ValueError("tools file must be a JSON array or an object with a 'tools' key")


def build_tool_index(tools: list[dict]) -> dict[str, dict]:
    """Build a name → function_schema index from a tools list."""
    index = {}
    for tool in tools:
        if tool.get("type") == "function" and "function" in tool:
            fn = tool["function"]
            index[fn["name"]] = fn
        elif "name" in tool:
            index[tool["name"]] = tool
    return index


def validate_call(call: dict, tool_index: dict) -> list[str]:
    """Validate a parsed tool call dict. Returns a list of error strings (empty = valid)."""
    errors = []

    name = call.get("name")
    if not name:
        errors.append("Missing 'name' field in tool call")
        return errors

    if name not in tool_index:
        available = sorted(tool_index.keys())
        errors.append(f"Unknown tool '{name}'. Available tools: {available}")
        return errors

    tool_fn = tool_index[name]
    params_schema = tool_fn.get("parameters", {})
    arguments = call.get("arguments", {})

    # Check required fields
    required = params_schema.get("required", [])
    for req_field in required:
        if req_field not in arguments:
            errors.append(f"Missing required parameter '{req_field}' for tool '{name}'")

    # Check for unknown parameters
    known_props = set(params_schema.get("properties", {}).keys())
    if known_props:
        for arg_key in arguments.keys():
            if arg_key not in known_props:
                errors.append(f"Unknown parameter '{arg_key}' for tool '{name}'. Known: {sorted(known_props)}")

    # Full JSON Schema validation (if jsonschema available)
    if HAS_JSONSCHEMA and params_schema and not errors:
        try:
            jsonschema.validate(instance=arguments, schema=params_schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")

    return errors


def format_result(call_str: str, call: dict | None, errors: list[str], index: int) -> str:
    lines = [f"--- Call #{index + 1} ---"]
    if call:
        lines.append(f"  Tool: {call.get('name', '<none>')}")
        args = call.get("arguments", {})
        if args:
            lines.append(f"  Args: {json.dumps(args, ensure_ascii=False)}")
    else:
        lines.append(f"  Raw: {call_str[:80]!r}")

    if errors:
        lines.append(f"  Status: INVALID ({len(errors)} error(s))")
        for err in errors:
            lines.append(f"    - {err}")
    else:
        lines.append("  Status: VALID")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Hermes <tool_call> blocks against a tool schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--call", help="Raw tool call string (with or without XML wrapper)")
    input_group.add_argument("--response", help="Path to a file containing a model response with tool calls")

    parser.add_argument("--tools", required=True, help="Path to JSON file with tool definitions")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    # Load tools
    try:
        tools = load_tools(args.tools)
        tool_index = build_tool_index(tools)
    except FileNotFoundError:
        print(f"Error: Tools file not found: {args.tools}", file=sys.stderr)
        sys.exit(2)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading tools: {e}", file=sys.stderr)
        sys.exit(2)

    if not tool_index:
        print("Error: No tools found in the tools file. Check the format.", file=sys.stderr)
        sys.exit(2)

    # Collect raw call strings
    raw_calls = []
    if args.call:
        raw_calls = [args.call]
    elif args.response:
        try:
            with open(args.response) as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: Response file not found: {args.response}", file=sys.stderr)
            sys.exit(2)
        raw_calls = extract_tool_calls_from_text(text)
        if not raw_calls:
            # Try treating the whole file as a single call
            raw_calls = [text.strip()]

    if not raw_calls:
        print("No tool calls found in the provided response.", file=sys.stderr)
        sys.exit(0)

    # Validate each call
    results = []
    all_valid = True

    for i, raw in enumerate(raw_calls):
        try:
            call = parse_tool_call(raw)
        except json.JSONDecodeError as e:
            results.append({"index": i, "raw": raw, "parsed": None, "errors": [f"Invalid JSON: {e}"]})
            all_valid = False
            continue

        errors = validate_call(call, tool_index)
        results.append({"index": i, "raw": raw, "parsed": call, "errors": errors})
        if errors:
            all_valid = False

    if args.json:
        output = {
            "all_valid": all_valid,
            "call_count": len(results),
            "tools_loaded": sorted(tool_index.keys()),
            "results": results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        if not HAS_JSONSCHEMA:
            print("Note: jsonschema not installed — schema type validation skipped. Run: uv add jsonschema", file=sys.stderr)

        for i, r in enumerate(results):
            print(format_result(r["raw"], r["parsed"], r["errors"], i))

        print(f"\nSummary: {sum(1 for r in results if not r['errors'])}/{len(results)} valid")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
