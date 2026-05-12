#!/usr/bin/env python3
"""Validate the Hermes SKILL.md against the agentskills.io spec."""
import re
import sys

SKILL_PATH = "/opt/data/jobs/67303b95-46a7-4715-82ae-7c7141a47b3f/result/hermes/SKILL.md"

with open(SKILL_PATH) as f:
    content = f.read()

fm = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
assert fm, "ERROR: No frontmatter found"
fm_text = fm.group(1)

name_match = re.search(r"^name:\s*(.+)$", fm_text, re.MULTILINE)
name = name_match.group(1).strip() if name_match else None
print(f"name: {name!r}")
assert name == "hermes", f"name must be hermes, got {name!r}"
assert re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$", name), "invalid name format"
assert "--" not in name, "consecutive hyphens not allowed"
assert len(name) <= 64, "name too long"

desc_match = re.search(r"^description:\s*(.+)$", fm_text, re.MULTILINE)
desc = desc_match.group(1).strip() if desc_match else None
print(f"description length: {len(desc)} chars")
assert desc, "description missing"
assert len(desc) <= 1024, f"description too long: {len(desc)}"

body = content[fm.end():]
lines = body.strip().split("\n")
print(f"body lines: {len(lines)}")
assert len(lines) <= 500, f"body too long: {len(lines)} lines"

print("All spec checks passed")
