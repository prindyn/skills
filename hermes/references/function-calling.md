# Hermes Function / Tool Calling — Complete Reference

## Overview

Hermes models use a custom XML-tagged JSON format for tool calls. This format is consistent and parseable without a complex grammar parser. The model emits calls; your runtime executes them and injects the result.

---

## Tool definition format

Define tools in the **system prompt** as a JSON list of schemas. Hermes expects OpenAI-style JSON Schema tool definitions wrapped in a specific XML block.

```xml
<tools>
[
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get current weather conditions for a location.",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City and country, e.g. 'Paris, France'"
          },
          "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "description": "Temperature unit"
          }
        },
        "required": ["location"]
      }
    }
  }
]
</tools>
```

Place the `<tools>` block at the end of your system prompt, before the closing `<|im_end|>` tag.

---

## Tool call format (model output)

When the model decides to call a tool, it emits:

```
<tool_call>
{"name": "get_weather", "arguments": {"location": "Paris, France", "unit": "celsius"}}
</tool_call>
```

Parse this from the assistant's response. The JSON is always on a single logical line (may wrap visually). Strip the `<tool_call>` and `</tool_call>` markers, then `json.loads()` the content.

---

## Tool response format (your injection)

After executing the call, inject the result as a new `tool` role message:

```
<|im_start|>tool
<tool_response>
{"temperature": 18, "condition": "partly cloudy", "humidity": 65}
</tool_response>
<|im_end|>
<|im_start|>assistant
```

Leave the final `<|im_start|>assistant` open so the model continues reasoning.

---

## Multi-tool calls (parallel)

Hermes 3 supports emitting multiple tool calls in a single response. The model may output them sequentially in one generation:

```
<tool_call>
{"name": "get_weather", "arguments": {"location": "Paris, France"}}
</tool_call>
<tool_call>
{"name": "get_weather", "arguments": {"location": "London, UK"}}
</tool_call>
```

Execute all calls in parallel, then inject all responses before resuming:

```
<|im_start|>tool
<tool_response>
{"location": "Paris, France", "temperature": 18}
</tool_response>
<tool_response>
{"location": "London, UK", "temperature": 14}
</tool_response>
<|im_end|>
<|im_start|>assistant
```

---

## Version differences

### Hermes 3 (recommended)

- Uses `<tool_call>` XML wrapper (shown above)
- Reliable parallel tool calls
- Emits `<tool_call>` even inside chain-of-thought reasoning blocks

### Hermes 2 Pro

- Mostly compatible with Hermes 3 format
- Some configurations emit bare JSON without the `<tool_call>` wrapper
- Add explicit instructions in system prompt: `"Always wrap tool calls in <tool_call>...</tool_call> tags."`

### Hermes 2 (older)

- Function calling is less reliable; use Hermes 2 Pro or Hermes 3 for production function calling

---

## Full system prompt template with tools

```
<|im_start|>system
You are a helpful assistant. You have access to tools to help answer questions.

When you need to use a tool, emit a tool call. After receiving the tool response, continue reasoning and provide your final answer.

<tools>
[
  {
    "type": "function",
    "function": {
      "name": "search_web",
      "description": "Search the web for current information.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {"type": "string", "description": "Search query"}
        },
        "required": ["query"]
      }
    }
  }
]
</tools><|im_end|>
<|im_start|>user
What's the latest news about space exploration?<|im_end|>
<|im_start|>assistant
```

---

## Parsing tool calls in Python

```python
import json
import re

def extract_tool_calls(text: str) -> list[dict]:
    """Extract all <tool_call> blocks from model output."""
    pattern = r"<tool_call>\s*(.*?)\s*</tool_call>"
    matches = re.findall(pattern, text, re.DOTALL)
    return [json.loads(m) for m in matches]

def format_tool_response(results: list[dict]) -> str:
    """Format tool results for injection back into the conversation."""
    responses = "\n".join(
        f"<tool_response>\n{json.dumps(r)}\n</tool_response>"
        for r in results
    )
    return f"<|im_start|>tool\n{responses}\n<|im_end|>\n<|im_start|>assistant\n"
```

---

## Error handling patterns

### Tool not found

If the model calls a tool that doesn't exist, respond with an error tool response:

```
<|im_start|>tool
<tool_response>
{"error": "Tool 'unknown_tool' not found. Available tools: search_web, get_weather"}
</tool_response>
<|im_end|>
```

### Tool execution failure

Return structured error information so the model can reason about it:

```json
{
  "error": "API timeout",
  "details": "Request to weather service exceeded 5s timeout",
  "suggestion": "Try again or use cached data"
}
```

### Invalid arguments

```json
{
  "error": "Invalid argument",
  "field": "location",
  "message": "Location must include city and country (e.g. 'Paris, France')"
}
```

---

## Gotchas

- **Parse with regex + json.loads, not eval.** Never use `eval()` on model output.
- **Always validate JSON before execution.** Malformed JSON means the model is confused; re-prompt rather than crashing.
- **Tool response must come before the next assistant turn.** Injecting a tool response and then a new user message without an intervening assistant turn breaks the conversation structure.
- **Tool descriptions are critical.** Vague descriptions ("do something useful") cause the model to misuse tools. One sentence per tool is enough; be specific about inputs and outputs.
- **Required vs. optional parameters matter.** Mark only truly required params as required. Optional params with defaults reduce model errors.
- **Do not put sensitive values in tool responses.** Hermes includes tool responses in its context window and may echo them back to the user.

---

## Advanced: structured JSON output (no tools)

To get pure JSON output without the tool-call wrapper, instruct the model in the system prompt:

```
Respond only with valid JSON. No explanation. No markdown code fences. No commentary.
Your response must be parseable by json.loads().
```

This is useful for data extraction, classification, and structured generation tasks where you don't need a back-and-forth tool loop.
