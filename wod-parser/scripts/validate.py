#!/usr/bin/env python3
"""
Validate wod-parser JSON output against templates/schema.json.

Usage:
    python3 validate.py output.json
    python3 parse_wod.py --text "..." | python3 validate.py -

Exit code 0 = valid, 1 = invalid (errors printed to stderr).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "templates" / "schema.json"


def _check_type(value, allowed) -> bool:
    types = allowed if isinstance(allowed, list) else [allowed]
    for t in types:
        if t == "null" and value is None:
            return True
        if t == "string" and isinstance(value, str):
            return True
        if t == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if t == "boolean" and isinstance(value, bool):
            return True
        if t == "array" and isinstance(value, list):
            return True
        if t == "object" and isinstance(value, dict):
            return True
    return False


def validate(data, schema, path: str = "$") -> list[str]:
    errors: list[str] = []
    if "type" in schema and not _check_type(data, schema["type"]):
        errors.append(f"{path}: expected type {schema['type']}, got {type(data).__name__}")
        return errors

    if isinstance(data, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in data:
                errors.append(f"{path}: missing required key '{key}'")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in data:
                if key not in props:
                    errors.append(f"{path}: unexpected key '{key}'")
        for key, value in data.items():
            if key in props:
                errors.extend(validate(value, props[key], f"{path}.{key}"))

    if isinstance(data, list) and "items" in schema:
        for i, item in enumerate(data):
            errors.extend(validate(item, schema["items"], f"{path}[{i}]"))

    if isinstance(data, str):
        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append(f"{path}: longer than maxLength {schema['maxLength']} (got {len(data)})")
        if "enum" in schema and data not in schema["enum"]:
            errors.append(f"{path}: value '{data}' not in enum {schema['enum']}")

    if isinstance(data, int) and not isinstance(data, bool):
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(f"{path}: below minimum {schema['minimum']}")

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate.py <output.json | ->", file=sys.stderr)
        return 2
    src = sys.argv[1]
    raw = sys.stdin.read() if src == "-" else Path(src).read_text()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"invalid JSON: {e}", file=sys.stderr)
        return 1

    schema = json.loads(SCHEMA_PATH.read_text())
    errors = validate(data, schema)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("ok", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
