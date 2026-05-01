#!/usr/bin/env python3
"""
Convert free-form WOD text into the wod-parser JSON contract.

Usage:
    python3 parse_wod.py --text "AMRAP 20: 5 pull-ups, 10 push-ups, 15 squats"
    python3 parse_wod.py --file workout.txt
    echo "Fran: 21-15-9 thrusters and pull-ups" | python3 parse_wod.py
    python3 parse_wod.py --pretty < workout.txt

Output: schema-valid JSON to stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def load_movements() -> dict[str, str]:
    """Build alias -> canonical map from assets/movements.json."""
    data = json.loads((ASSETS_DIR / "movements.json").read_text())
    alias_map: dict[str, str] = {}
    for entry in data["movements"]:
        canonical = entry["canonical"]
        for alias in entry["aliases"]:
            alias_map[_normalize_alias(alias)] = canonical
        alias_map[_normalize_alias(canonical)] = canonical
    return alias_map


def _normalize_alias(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 \-]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s


WORD_TO_INT = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "fifteen": 15, "twenty": 20, "thirty": 30, "fifty": 50,
    "hundred": 100,
}


def _word_or_int(token: str) -> int | None:
    token = token.lower().strip()
    if token.isdigit():
        return int(token)
    return WORD_TO_INT.get(token)


# ---------- classification ----------

REP_LADDER_RE = re.compile(r"\b(\d+(?:\s*-\s*\d+){1,})\b")  # e.g. 21-15-9, 50-40-30-20-10


def classify(text: str) -> str:
    t = text.lower()
    if "tabata" in t:
        return "tabata"
    if "emom" in t or "every minute on the minute" in t or re.search(r"every\s+\d+\s+minute", t):
        return "emom"
    if "amrap" in t or "as many rounds" in t or "as many reps" in t:
        return "amrap"
    if REP_LADDER_RE.search(t) and ("for time" in t or "rep rounds" in t or "reps of" in t or "reps for time" in t):
        return "rep_scheme"
    if re.search(r"\b(\w+)\s+rounds?\s+for\s+time", t):
        return "rounds_for_time"
    if re.search(r"\b(\w+)\s+rounds?\s*,\s*each\s+for\s+time", t):
        return "rounds_for_time"
    if "rest" in t and re.search(r"rest\s+\d+\s+(seconds?|minutes?)", t) and "rounds" in t:
        return "intervals"
    if "for time" in t:
        movement_lines = _movement_lines(text)
        if len(movement_lines) >= 5:
            return "chipper"
        return "for_time"
    return "custom"


# ---------- helpers ----------

HEADER_KEYWORDS = (
    "rounds", "for time", "amrap", "emom", "tabata", "as many rounds",
    "as many reps", "minutes as you can", "rep rounds", "reps for time",
    "complete as many",
)


def _strip_header(line: str) -> str:
    """If a line is a 'descriptor of: <tail>' header, return just the tail.

    Examples:
        "21-15-9 reps for time of 95lb thrusters and pull-ups"
            -> "95lb thrusters and pull-ups"
        "Three rounds for time of:"  -> ""
        "AMRAP 20: 5 pull-ups, 10 push-ups"  -> "5 pull-ups, 10 push-ups"
    """
    low = line.lower()
    if not any(k in low for k in HEADER_KEYWORDS):
        if low.startswith("amrap"):
            pass
        else:
            return line
    # Split on 'of', 'of:', ':' that follows a header keyword
    m = re.search(r"\bof\b\s*:?\s*", line, re.IGNORECASE)
    if m:
        tail = line[m.end():].strip(" .,:")
        return tail
    m = re.search(r":\s*", line)
    if m and any(k in low[: m.start()] for k in HEADER_KEYWORDS):
        return line[m.end():].strip(" .,")
    return ""


def _split_lines(text: str) -> list[str]:
    raw = re.split(r"[\n;]+", text)
    return [ln.strip(" \t-•·*") for ln in raw if ln.strip(" \t-•·*")]


def _split_movement_clauses(s: str) -> list[str]:
    """Split a single string of movements into clauses by ',', '+', '/', or ' and '/' then '."""
    parts = re.split(r"\s*[,+/]\s*|\s+and\s+|\s+then\s+", s)
    return [p.strip(" .,;:") for p in parts if p.strip(" .,;:")]


_DURATION_ONLY_RE = re.compile(r"^\d+\s*(s|sec|secs|second|seconds|m|min|minute|minutes)\s+(on|off|work|rest)$", re.IGNORECASE)


_TABATA_NAME_RE = re.compile(r"\btabata\s+([a-z][a-z\s\-]*?)(?=\s*[:.,]|$)", re.IGNORECASE)


def _movement_lines(text: str) -> list[str]:
    """Return a flat list of movement clauses, expanding inline header tails."""
    out: list[str] = []
    for line in _split_lines(text):
        low = line.lower()
        if low.startswith("rest "):
            continue
        if "if you" in low or "post rounds" in low or low.startswith("begin "):
            continue
        if any(k in low for k in HEADER_KEYWORDS):
            tail = _strip_header(line)
            if tail:
                out.extend(_split_movement_clauses(tail))
            # Try to pull a movement name out of "Tabata <name>" or "EMOM 12 of <name>"
            m = _TABATA_NAME_RE.search(line)
            if m:
                cand = m.group(1).strip()
                if cand and cand.lower() not in ("squats:", "of"):
                    out.append(cand)
            continue
        out.append(line)
    return out


def parse_time_cap(text: str) -> int | None:
    """Look for explicit time caps: 'time cap of 20 minutes', '20-minute time cap'."""
    t = text.lower()
    m = re.search(r"time\s*cap\s*(?:of)?\s*(\d+)\s*(min|minute|minutes|sec|seconds|s)?", t)
    if m:
        n = int(m.group(1))
        unit = (m.group(2) or "min")
        return n if unit.startswith("s") and unit != "min" else n * 60
    m = re.search(r"(\d+)\s*-\s*minute\s*time\s*cap", t)
    if m:
        return int(m.group(1)) * 60
    return None


def parse_amrap_minutes(text: str) -> int | None:
    t = text.lower()
    m = re.search(r"amrap\s*(\d+)", t)
    if m:
        return int(m.group(1))
    m = re.search(r"as\s+many\s+rounds[^\d]*(\d+)\s*minute", t)
    if m:
        return int(m.group(1))
    m = re.search(r"in\s+(\w+)\s+minute", t)
    if m:
        n = _word_or_int(m.group(1))
        if n:
            return n
    return None


def parse_emom_minutes(text: str) -> tuple[int | None, int | None]:
    """Returns (cycle_seconds, total_minutes)."""
    t = text.lower()
    cycle = 60
    m = re.search(r"every\s+(\d+)\s+minute", t)
    if m:
        cycle = int(m.group(1)) * 60
    m = re.search(r"emom\s*(\d+)", t)
    if m:
        return cycle, int(m.group(1))
    m = re.search(r"for\s+(\d+)\s+minute", t)
    if m:
        return cycle, int(m.group(1))
    return cycle, None


def parse_rounds(text: str) -> int | None:
    t = text.lower()
    m = re.search(r"(\w+)\s+rounds?\s*,?\s*(?:each\s+)?for\s+time", t)
    if m:
        return _word_or_int(m.group(1))
    m = re.search(r"complete\s+(\w+)\s+rounds?", t)
    if m:
        return _word_or_int(m.group(1))
    m = re.search(r"(\d+)\s+rounds?", t)
    if m:
        return int(m.group(1))
    m = re.search(r"\b(\w+)\s+rounds?\b", t)
    if m:
        return _word_or_int(m.group(1))
    return None


def parse_rest_seconds(text: str) -> int | None:
    m = re.search(r"rest\s+(\d+)\s*(seconds?|minutes?|min|sec|s)?", text.lower())
    if not m:
        return None
    n = int(m.group(1))
    unit = m.group(2) or "seconds"
    return n if unit.startswith(("s", "S")) and not unit.startswith("min") else n * 60


def parse_rep_ladder(text: str) -> list[int] | None:
    m = REP_LADDER_RE.search(text)
    if not m:
        return None
    parts = re.split(r"\s*-\s*", m.group(1))
    nums = [int(p) for p in parts if p.isdigit()]
    return nums if len(nums) >= 2 else None


# ---------- movement extraction ----------

WEIGHT_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(lb|lbs|pound|pounds|#|kg|kgs|kilo|kilos|kilogram|kilograms|pood|poods)\b",
    re.IGNORECASE,
)
DISTANCE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(meters?|metres?|m|kilometers?|km|miles?|mi|feet|ft|yards?|yd)\b",
    re.IGNORECASE,
)
DISTANCE_K_RE = re.compile(r"(\d+(?:\.\d+)?)\s*K\b", re.IGNORECASE)  # 1K, 2K, 5k
CALORIES_RE = re.compile(r"(\d+)\s*(?:/\s*\d+\s*)?(?:cal|calorie|calories|kcal)\b", re.IGNORECASE)
REPS_RE = re.compile(r"(\d+)\s*(?:reps?|x|×|@)?", re.IGNORECASE)
LEADING_REPS_RE = re.compile(r"^\s*(\d+)\b")
TRAILING_REPS_RE = re.compile(r",\s*(\d+)\s*reps?", re.IGNORECASE)


def normalize_weight(value: str, unit: str) -> str:
    u = unit.lower().rstrip(".")
    if u in ("lb", "lbs", "pound", "pounds", "#"):
        n = float(value)
        return f"{int(n) if n.is_integer() else n} lb"
    if u in ("kg", "kgs", "kilo", "kilos", "kilogram", "kilograms"):
        n = float(value)
        return f"{int(n) if n.is_integer() else n} kg"
    if u in ("pood", "poods"):
        n = float(value)
        return f"{int(n) if n.is_integer() else n} pood"
    return f"{value} {unit}"


def normalize_distance(value: str, unit: str) -> str:
    u = unit.lower().rstrip(".s")
    n = float(value)
    n_str = str(int(n)) if n.is_integer() else str(n)
    if u in ("m", "meter", "metre"):
        return f"{n_str} m"
    if u in ("km", "kilometer"):
        return f"{n_str} km"
    if u in ("mi", "mile"):
        return f"{n_str} mi"
    if u in ("ft", "foot", "feet", "'"):
        return f"{n_str} ft"
    if u in ("yd", "yard"):
        return f"{n_str} yd"
    return f"{n_str} {unit}"


def extract_movement(line: str, alias_map: dict[str, str]) -> dict[str, Any] | None:
    """Pull (name, reps, weight, distance, calories) from a single line."""
    raw = line.strip(" \t-•·*,.;:")
    if not raw:
        return None
    if raw.lower().startswith("rest "):
        return None
    if _DURATION_ONLY_RE.match(raw):
        return None

    name: str | None = None
    weight: str | None = None
    distance: str | None = None
    calories: int | None = None
    reps: int | None = None

    work = " " + raw + " "

    m = WEIGHT_RE.search(work)
    if m:
        weight = normalize_weight(m.group(1), m.group(2))
        work = work[: m.start()] + " " + work[m.end():]

    m = DISTANCE_RE.search(work)
    if m:
        distance = normalize_distance(m.group(1), m.group(2))
        work = work[: m.start()] + " " + work[m.end():]
    else:
        m = DISTANCE_K_RE.search(work)
        if m:
            distance = f"{m.group(1)} km"
            work = work[: m.start()] + " " + work[m.end():]

    m = CALORIES_RE.search(work)
    if m:
        calories = int(m.group(1))
        work = work[: m.start()] + " " + work[m.end():]

    m = TRAILING_REPS_RE.search(work)
    if m:
        reps = int(m.group(1))
        work = work[: m.start()] + " " + work[m.end():]
    else:
        m = LEADING_REPS_RE.search(work.lstrip())
        if m:
            reps = int(m.group(1))
            work = work.replace(m.group(0), " ", 1)

    cleaned = re.sub(r"\s+", " ", work).strip(" ,;:.")
    cleaned = re.sub(r"\b(reps?|each arm|right arm|left arm|each side)\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^\s*\d+\s*", "", cleaned).strip(" ,;:.")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    canon = match_canonical(cleaned, alias_map) if cleaned else None
    if canon:
        name = canon
    elif cleaned:
        name = cleaned.lower()

    if not name:
        if distance:
            name = "run"
        elif calories is not None:
            name = "row"
        else:
            return None

    # Drop bare title-like lines: no rep/weight/distance/cal, and the name didn't
    # match the canonical movement vocabulary. These are usually workout names
    # ("Murph", "Fran") or section headings, not movements.
    if (
        canon is None
        and reps is None
        and weight is None
        and distance is None
        and calories is None
    ):
        return None

    return {
        "name": name,
        "reps": reps,
        "weight": weight,
        "distance": distance,
        "calories": calories,
    }


def match_canonical(name: str, alias_map: dict[str, str]) -> str | None:
    norm = _normalize_alias(name)
    if norm in alias_map:
        return alias_map[norm]
    # try last 1–4 word suffixes
    parts = norm.split()
    for size in range(min(4, len(parts)), 0, -1):
        suffix = " ".join(parts[-size:])
        if suffix in alias_map:
            return alias_map[suffix]
    # try any sub-window
    for i in range(len(parts)):
        for j in range(i + 1, len(parts) + 1):
            chunk = " ".join(parts[i:j])
            if chunk in alias_map:
                return alias_map[chunk]
    return None


# ---------- intervals + interpretation ----------

def build_intervals_and_cap(workout_type: str, text: str) -> tuple[list[dict[str, Any]], int | None]:
    cap = parse_time_cap(text)
    if workout_type == "amrap":
        n = parse_amrap_minutes(text) or 20
        secs = n * 60
        return [{"duration": secs, "type": "work", "repeat": False}], secs
    if workout_type == "emom":
        cycle, total = parse_emom_minutes(text)
        cycle = cycle or 60
        total = total or 10
        return [{"duration": cycle, "type": "work", "repeat": True}], total * 60
    if workout_type == "tabata":
        return [
            {"duration": 20, "type": "work", "repeat": True},
            {"duration": 10, "type": "rest", "repeat": True},
        ], 240
    if workout_type == "rounds_for_time":
        rest = parse_rest_seconds(text)
        if rest:
            return [
                {"duration": 0, "type": "work", "repeat": True},
                {"duration": rest, "type": "rest", "repeat": True},
            ], cap
        return [{"duration": cap or 0, "type": "work", "repeat": False}], cap
    if workout_type == "intervals":
        rest = parse_rest_seconds(text) or 60
        return [
            {"duration": 60, "type": "work", "repeat": True},
            {"duration": rest, "type": "rest", "repeat": True},
        ], cap
    # for_time / chipper / rep_scheme / custom
    return [{"duration": cap or 0, "type": "work", "repeat": False}], cap


def build_interpretation(workout_type: str, text: str, movements: list[dict[str, Any]]) -> str:
    names = [m["name"] for m in movements if m.get("name")]
    head = ", ".join(names[:3]) if names else "mixed movements"
    if len(names) > 3:
        head += f" (+{len(names) - 3} more)"

    if workout_type == "amrap":
        n = parse_amrap_minutes(text) or 20
        out = f"AMRAP {n} min: {head}."
    elif workout_type == "emom":
        cycle, total = parse_emom_minutes(text)
        cycle = (cycle or 60) // 60
        total = total or 10
        out = f"EMOM {total} min ({cycle} min cycle): {head}."
    elif workout_type == "tabata":
        out = f"Tabata 20s/10s x 8: {head}."
    elif workout_type == "rep_scheme":
        ladder = parse_rep_ladder(text)
        scheme = "-".join(str(x) for x in ladder) if ladder else "ladder"
        out = f"{scheme} reps for time: {head}."
    elif workout_type == "rounds_for_time":
        rounds = parse_rounds(text)
        out = f"{rounds or '?'} rounds for time: {head}."
    elif workout_type == "chipper":
        out = f"For time chipper: {head}."
    elif workout_type == "intervals":
        out = f"Intervals: {head}."
    elif workout_type == "for_time":
        out = f"For time: {head}."
    else:
        out = f"Custom workout: {head}."

    if len(out) > 120:
        out = out[:117].rstrip() + "..."
    return out


# ---------- main pipeline ----------

def parse(text: str) -> dict[str, Any]:
    text = text.strip()
    alias_map = load_movements()

    workout_type = classify(text)

    movements: list[dict[str, Any]] = []
    seen: set[tuple] = set()
    for line in _movement_lines(text):
        mv = extract_movement(line, alias_map)
        if not mv:
            continue
        key = (mv["name"], mv["reps"], mv["weight"], mv["distance"], mv["calories"])
        if key in seen:
            continue
        seen.add(key)
        movements.append(mv)

    # rep_scheme: collapse repeated movements with varying reps to single entries with reps=null
    if workout_type == "rep_scheme":
        collapsed: list[dict[str, Any]] = []
        for mv in movements:
            existing = next((c for c in collapsed if c["name"] == mv["name"]), None)
            if existing:
                existing["reps"] = None
            else:
                m2 = dict(mv)
                m2["reps"] = None
                collapsed.append(m2)
        movements = collapsed

    if not movements:
        movements = [{
            "name": "unspecified",
            "reps": None,
            "weight": None,
            "distance": None,
            "calories": None,
        }]

    intervals, cap = build_intervals_and_cap(workout_type, text)
    interpretation = build_interpretation(workout_type, text, movements)

    return {
        "workout_type": workout_type,
        "movements": movements,
        "intervals": intervals,
        "ai_interpretation": interpretation,
        "time_cap": cap,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--text", help="WOD text directly on the command line")
    src.add_argument("--file", help="Path to a file containing WOD text")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text()
    elif args.text:
        text = args.text
    else:
        if sys.stdin.isatty():
            parser.error("Provide --text, --file, or pipe text via stdin")
        text = sys.stdin.read()

    out = parse(text)
    indent = 2 if args.pretty else None
    print(json.dumps(out, indent=indent, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
