# Hermes Tool Use & Function Calling

Hermes 2 Pro and Hermes 3 support tool use (function calling) natively via a structured `<tool_call>` XML format.

## Overview

Tool calling in Hermes follows a 4-step cycle:

1. System prompt declares available tools as JSON schema
2. User asks something requiring a tool
3. Assistant emits a `<tool_call>` block
4. Tool result is injected in a `tool` turn; assistant produces final answer

## Tool definition format

Declare tools in the system prompt as a JSON array:

```
<|im_start|>system
You are a function calling AI model. You are provided with function signatures within <tools></tools> tags. Call functions using <tool_call></tool_call> tags.

<tools>
[
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City name, e.g. Paris"
          },
          "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "default": "celsius"
          }
        },
        "required": ["location"]
      }
    }
  }
]
</tools><|im_end|>
```

## Tool call (assistant turn)

When the model needs a tool, it outputs:

```
<|im_start|>assistant
<tool_call>
{"name": "get_weather", "arguments": {"location": "Paris", "unit": "celsius"}}
</tool_call><|im_end|>
```

One `<tool_call>` block per call. For parallel calls, emit multiple blocks:

```
<tool_call>
{"name": "get_weather", "arguments": {"location": "Paris"}}
</tool_call>
<tool_call>
{"name": "get_weather", "arguments": {"location": "London"}}
</tool_call>
```

## Tool result (tool turn)

Inject the result using the `tool` role:

```
<|im_start|>tool
<tool_response>
{"temperature": 22, "condition": "sunny", "humidity": 60}
</tool_response><|im_end|>
```

For multiple parallel calls, include one `<tool_response>` per result in the same turn.

## Final assistant response

After tool results, the model synthesizes the answer:

```
<|im_start|>assistant
The weather in Paris is 22°C and sunny with 60% humidity.<|im_end|>
```

## Complete example

```
<|im_start|>system
You are a function calling AI model.

<tools>
[{"type": "function", "function": {"name": "add", "description": "Add two numbers", "parameters": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}, "required": ["a", "b"]}}}]
</tools><|im_end|>
<|im_start|>user
What is 17 + 25?<|im_end|>
<|im_start|>assistant
<tool_call>
{"name": "add", "arguments": {"a": 17, "b": 25}}
</tool_call><|im_end|>
<|im_start|>tool
<tool_response>
{"result": 42}
</tool_response><|im_end|>
<|im_start|>assistant
17 + 25 = 42.<|im_end|>
```

## JSON mode (structured output without tools)

For structured output without defining tools, prompt directly:

```
<|im_start|>system
Respond only with valid JSON. No explanation, no markdown.
Schema: {"name": string, "age": number}<|im_end|>
<|im_start|>user
Parse: "Alice is 30 years old."<|im_end|>
<|im_start|>assistant
{"name": "Alice", "age": 30}<|im_end|>
```

Use `temperature=0` for reliable JSON output.

## Gotchas

- Tool name must exactly match the declared function name (case-sensitive).
- `arguments` must be a valid JSON object, not a string.
- The model may hallucinate tool calls if the tool description is vague — be specific.
- If the model skips tool calling and answers directly, your system prompt may be missing the `<tools>` block.
- Hermes 2 Pro supports parallel tool calls; Hermes 1 does not.
