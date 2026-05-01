---
name: wod-parser
description: Convert free-form workout (WOD) note text into a structured JSON timer configuration. Use when a user provides workout notes — CrossFit Hero/Girl WODs, AMRAPs, EMOMs, Tabatas, rep schemes (21-15-9), rounds-for-time, chippers, or hand-written gym whiteboard text — and wants timer-ready JSON with movements, intervals, time cap, and an interpretation line.
---

# wod-parser

Convert raw WOD text into the timer JSON contract below. Most inputs are short (a workout name plus 3–10 lines of movements). The skill is mostly deterministic regex extraction with a small classifier for `workout_type`. When in doubt, fall back to `workout_type: "custom"` and put the meaning into `ai_interpretation`.

## JSON contract (REQUIRED — match exactly)

```json
{
  "workout_type": "for_time | amrap | emom | tabata | rounds_for_time | intervals | rep_scheme | chipper | custom",
  "movements": [
    {"name": "<string>", "reps": <int|null>, "weight": "<string|null>", "distance": "<string|null>", "calories": <int|null>}
  ],
  "intervals": [
    {"duration": <int seconds>, "type": "work" | "rest", "repeat": <bool>}
  ],
  "ai_interpretation": "<one sentence, ≤120 chars>",
  "time_cap": <int seconds | null>
}
```

Every movement object MUST include all five keys (`name`, `reps`, `weight`, `distance`, `calories`); set unused fields to `null`. `name` is always a non-empty string. `intervals` is always present (use `[]` only if truly nothing is timed, but in practice every workout has at least one interval). `ai_interpretation` is a single human sentence ≤120 characters.

## Workflow

1. Read the input. If it has a heading/name line (e.g. `Murph`, `Fran`), keep it for the interpretation.
2. **Classify** `workout_type` using the rules below.
3. **Extract movements** line-by-line; normalize names via `assets/movements.json`.
4. **Build intervals** based on workout_type (see "Interval rules" below).
5. **Compute time_cap** in seconds (null if open-ended for-time and no cap given).
6. Write `ai_interpretation`: one short sentence summarizing the workout (≤120 chars).
7. Validate with `scripts/validate.py` before returning.

For most inputs you can run `python3 scripts/parse_wod.py` and it handles the full pipeline. Use the script as the primary path; only hand-build JSON when the input is unusual enough that the parser misclassifies (rare). The script's output is already schema-valid.

## Quick start

```bash
echo "Fran: 21-15-9 reps for time of 95lb thrusters and pull-ups" | python3 scripts/parse_wod.py
python3 scripts/parse_wod.py --file workout.txt
python3 scripts/parse_wod.py --text "AMRAP 20: 5 pull-ups, 10 push-ups, 15 squats"
```

The script prints schema-valid JSON to stdout. Pass `--pretty` for indented output.

## Classification rules (apply in order, first match wins)

| Pattern in text                                                              | workout_type      |
|------------------------------------------------------------------------------|-------------------|
| "tabata" mentioned                                                           | `tabata`          |
| "EMOM" / "every minute on the minute" / "every X minutes"                    | `emom`            |
| "AMRAP" / "as many rounds as possible" / "as many rounds … in N minutes"     | `amrap`           |
| "X-Y-Z reps" or "21-15-9" style descending ladder                            | `rep_scheme`      |
| "N rounds for time" / "complete N rounds"                                    | `rounds_for_time` |
| Multiple `Rest N (seconds\|minutes)` lines + rounds                          | `intervals`       |
| "For time:" with a long single list of distinct movements (≥5 movements)     | `chipper`         |
| "For time:" otherwise                                                        | `for_time`        |
| Anything else                                                                | `custom`          |

## Interval rules

The `intervals` array describes how the timer should run. Use these mappings:

- **for_time** with `time_cap`:
  `[{"duration": <cap>, "type": "work", "repeat": false}]`
- **for_time** with no cap:
  `[{"duration": 0, "type": "work", "repeat": false}]` (open count-up; consumer treats `0` as "count up until stopped"). Set `time_cap: null`.
- **amrap N min**:
  `[{"duration": N*60, "type": "work", "repeat": false}]`, `time_cap: N*60`.
- **emom N min** with cycle = 60s:
  `[{"duration": 60, "type": "work", "repeat": true}]`, `time_cap: N*60`.
- **emom every M min**:
  `[{"duration": M*60, "type": "work", "repeat": true}]`, `time_cap: total_minutes*60` if known.
- **tabata** (default 8 rounds of 20/10):
  `[{"duration": 20, "type": "work", "repeat": true}, {"duration": 10, "type": "rest", "repeat": true}]`, `time_cap: 240` (4 min for one tabata; multiply if multiple).
- **rounds_for_time** with rest of `R` seconds between rounds:
  `[{"duration": 0, "type": "work", "repeat": true}, {"duration": R, "type": "rest", "repeat": true}]`. `time_cap` = the workout's cap if stated, else null.
- **rounds_for_time** with no rest:
  Same as for_time; one work interval.
- **intervals** (e.g. "3 rounds: 1 min squat clean, 1 min burpees, … rest 1 min"):
  Encode each timed slot as a separate `{duration, type:"work"}` followed by a `{rest}`, with `repeat: true` if the whole circuit cycles. Time_cap = full circuit duration × rounds.
- **rep_scheme** / **chipper**:
  Single open-ended work interval `{duration: <cap or 0>, "type": "work", "repeat": false}`. These are usually for_time-flavored with an internal rep ladder.
- **custom**: best-effort. Prefer one work interval with `time_cap` if any duration is mentioned.

## Movement extraction

Each movement line typically has these fragments in any order:
- **reps**: `21 reps`, `21`, `× 21`, `21x`, `Run 800m` (no rep — distance instead)
- **weight**: `95 pound`, `95lb`, `95#`, `95 kg`, `1.5 pood`, `2-pood`, `40 pound dumbbell`
- **distance**: `Run 800 meters`, `400 m`, `1 mile`, `1K`, `15 ft Rope Climb`
- **calories**: `15 cal row`, `12 calorie bike`, `20/15 cal` (M/F split — store M value)
- **name**: the movement itself, normalized via `assets/movements.json` aliases

Keep `weight` and `distance` as **strings with their unit** (e.g. `"95 lb"`, `"800 m"`, `"1 mi"`). Convert pood to lb only inside `ai_interpretation` if helpful (1 pood ≈ 35 lb, 1.5 pood ≈ 53 lb, 2 pood ≈ 70 lb).

When a line is purely a run/row/bike, the movement's `reps` is null and `distance` (or `calories`) carries the load.

When a workout has reps that change per round (rep_scheme like 21-15-9), record the **movement once** with `reps: null`, then put the ladder in `ai_interpretation` (e.g. `"21-15-9 reps of thrusters and pull-ups for time."`). The rep scheme lives in the description, not duplicated rows.

## ai_interpretation rules

- Single sentence, ≤120 characters (the script truncates at 120 with `…` if needed).
- Lead with the workout type and time/round structure, then the headline movements.
- Examples:
  - `"AMRAP 20 min: 5 pull-ups, 10 push-ups, 15 air squats."`
  - `"21-15-9 thrusters (95 lb) and pull-ups for time."`
  - `"5 rounds for time: 400 m run, 30 ghd sit-ups, 15 deadlifts at 250 lb."`

## Resources in this skill

- `scripts/parse_wod.py` — main parser; CLI and library use.
- `scripts/validate.py` — JSON-schema validator for the output contract.
- `templates/` — empty skeletons per workout type. Use as a starting point when crafting JSON by hand.
- `templates/schema.json` — the JSON schema enforced by the validator.
- `assets/movements.json` — canonical movement names + aliases.
- `assets/units.json` — distance/weight unit normalization tables.
- `assets/examples.jsonl` — input → expected JSON pairs covering each workout_type. Useful to verify changes.

## When to deviate from the parser

The parser handles ~90% of well-formed WOD text. Hand-build JSON when:
- The text describes a workout in narrative form ("warm up, then …").
- Reps differ per round in non-ladder ways (record each round as separate movements with explicit `reps`).
- The user supplies an explicit time_cap that the parser missed (override before returning).

Always validate the final JSON: `python3 scripts/validate.py path/to/output.json`.
