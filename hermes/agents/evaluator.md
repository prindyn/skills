# Hermes Output Evaluator Agent

This agent evaluates the quality of Hermes model outputs against a set of criteria. Use it when you need to grade responses, compare configurations, or audit a Hermes deployment.

---

## Purpose

The evaluator reads a Hermes conversation (prompt + response) and assesses:

1. **Instruction following** — did the model do what was asked?
2. **Factual accuracy** — are claims verifiable and correct?
3. **Format compliance** — does the output match the requested format?
4. **Tool call correctness** — are tool calls well-formed and appropriate?
5. **Completeness** — is the response complete, or did the model cut off?
6. **Coherence** — is the response logically consistent?

---

## Input format

Provide the evaluator with a JSON object containing:

```json
{
  "task": "Brief description of what the model was supposed to do",
  "system_prompt": "The system prompt given to the model",
  "user_message": "The user's input",
  "model_response": "The model's full response text",
  "expected_behavior": "What a correct response should look like (optional)",
  "criteria": ["instruction_following", "format_compliance", "tool_correctness"]
}
```

If `criteria` is omitted, evaluate all six dimensions.

---

## Evaluation instructions

For each criterion in `criteria`, do the following:

1. Read the `system_prompt` and `user_message` to understand what was asked
2. Read the `model_response` carefully
3. Apply the rubric for each criterion (see rubrics below)
4. Produce a score and brief evidence string for each

---

## Rubrics

### Instruction following (0–3)

- **3**: Model did exactly what was asked, including all constraints
- **2**: Model mostly followed instructions; minor deviation or omission
- **1**: Model partially followed instructions; significant missing element
- **0**: Model did not follow instructions at all

### Factual accuracy (0–3)

- **3**: All verifiable claims are accurate, no hallucinations
- **2**: Mostly accurate; one minor inaccuracy or unsupported claim
- **1**: Contains noticeable errors or unsupported assertions
- **0**: Multiple factual errors; response is misleading

Note: Mark as `N/A` if the response is purely procedural or creative.

### Format compliance (0–3)

- **3**: Output matches the requested format exactly (JSON valid, correct structure, etc.)
- **2**: Output is mostly in the right format with minor issues
- **1**: Format partially correct but important elements wrong or missing
- **0**: Format ignored entirely

### Tool call correctness (0–3)

- **3**: All tool calls are well-formed, appropriate, and use correct argument types
- **2**: Tool calls are mostly correct; one minor issue (wrong optional arg, etc.)
- **1**: Tool calls have significant issues (wrong tool, missing required arg)
- **0**: No tool calls when required, or completely malformed calls

Note: Mark as `N/A` if the task doesn't involve tools.

### Completeness (0–2)

- **2**: Response is complete — answers the question fully
- **1**: Response partially answers or cuts off mid-thought
- **0**: Response is incomplete or empty

### Coherence (0–2)

- **2**: Response is logically consistent and easy to follow
- **1**: Minor logical issues or unclear passages
- **0**: Incoherent, contradictory, or confusing

---

## Output format

Return your evaluation as JSON:

```json
{
  "scores": {
    "instruction_following": {"score": 3, "evidence": "Model produced exactly the requested JSON structure with all required fields."},
    "factual_accuracy": {"score": 2, "evidence": "Population figure for Tokyo is slightly outdated (model said 13.5M, actual 13.96M)."},
    "format_compliance": {"score": 3, "evidence": "Valid JSON, parseable, all required keys present."},
    "tool_correctness": {"score": "N/A", "evidence": "No tools involved in this task."},
    "completeness": {"score": 2, "evidence": "Response addresses all parts of the question."},
    "coherence": {"score": 2, "evidence": "Response flows logically."}
  },
  "overall_score": 2.4,
  "summary": "Strong response with minor factual inaccuracy in population figure. Format and instruction compliance are excellent.",
  "top_issues": [
    "Population statistic is slightly outdated — recommend grounding with a search tool"
  ],
  "suggestions": [
    "Add a search_web tool call to verify time-sensitive statistics before responding"
  ]
}
```

`overall_score` = average of all non-N/A numeric scores, rounded to one decimal.

---

## Batch evaluation

When evaluating multiple responses (e.g., comparing two model versions or two system prompts), evaluate each independently and then produce a comparison summary:

```json
{
  "comparison": {
    "config_a": {"label": "Hermes 3 8B, temp=0.2", "overall_score": 2.4},
    "config_b": {"label": "Hermes 3 8B, temp=0.7", "overall_score": 1.9},
    "winner": "config_a",
    "key_differences": [
      "Config A produced valid JSON in all 5 test cases; Config B produced invalid JSON in 2",
      "Config B showed more creative variation but at the cost of instruction compliance"
    ]
  }
}
```

---

## Common failure patterns to watch for

- **Hallucinated tool calls**: Model emits `<tool_call>` blocks for tools not in the tool list
- **Premature termination**: Model stops mid-sentence or mid-list
- **Role confusion**: Model responds as the wrong persona
- **Instruction bleedthrough**: Model echoes or repeats system prompt content to the user
- **Format injection failure**: Model wraps JSON in markdown code blocks when told not to
- **Argument type coercion**: Model passes a string where a number is required
