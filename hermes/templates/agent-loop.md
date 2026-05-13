# Hermes Agent Loop Template

This template implements a complete ReAct (Reason + Act) agent loop around a Hermes model. It covers the conversation structure, the execution loop, and error recovery.

---

## Full system prompt for an agent

```
<|im_start|>system
You are an autonomous AI agent. You reason step by step, use tools to gather information and take actions, and produce a final answer once you have everything you need.

Process:
1. Understand the user's goal
2. Plan the steps needed (you can think aloud)
3. Use tools one at a time or in parallel as needed
4. After each tool response, re-assess: do you have enough to answer?
5. When you have everything, give a clear, direct final answer

<tools>
[
  {
    "type": "function",
    "function": {
      "name": "search_web",
      "description": "Search the web for up-to-date information.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {"type": "string", "description": "Search query string"}
        },
        "required": ["query"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "read_file",
      "description": "Read the contents of a local file.",
      "parameters": {
        "type": "object",
        "properties": {
          "path": {"type": "string", "description": "Absolute or relative file path"}
        },
        "required": ["path"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "run_python",
      "description": "Execute a Python code snippet and return stdout.",
      "parameters": {
        "type": "object",
        "properties": {
          "code": {"type": "string", "description": "Python code to execute"}
        },
        "required": ["code"]
      }
    }
  }
]
</tools><|im_end|>
```

---

## Python agent loop implementation

```python
import json
import re
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")
MODEL = "NousResearch/Hermes-3-Llama-3.1-8B"
MAX_TURNS = 20

SYSTEM_PROMPT = """..."""  # your system prompt above

def extract_tool_calls(text: str) -> list[dict]:
    pattern = r"<tool_call>\s*(.*?)\s*</tool_call>"
    matches = re.findall(pattern, text, re.DOTALL)
    return [json.loads(m) for m in matches]

def execute_tool(call: dict) -> dict:
    """Dispatch a tool call to your actual tool implementations."""
    name = call["name"]
    args = call.get("arguments", {})
    
    if name == "search_web":
        return search_web(args["query"])
    elif name == "read_file":
        return read_file(args["path"])
    elif name == "run_python":
        return run_python(args["code"])
    else:
        return {"error": f"Unknown tool: {name}. Available: search_web, read_file, run_python"}

def format_tool_responses(results: list[dict]) -> str:
    responses = "\n".join(
        f"<tool_response>\n{json.dumps(r, ensure_ascii=False)}\n</tool_response>"
        for r in results
    )
    return responses

def run_agent(user_message: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
    
    for turn in range(MAX_TURNS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=2048,
            stop=["<|im_end|>"],
        )
        
        assistant_text = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_text})
        
        tool_calls = extract_tool_calls(assistant_text)
        
        if not tool_calls:
            # No tool calls — model is done
            # Strip any trailing reasoning markers if present
            final = assistant_text.split("</thinking>")[-1].strip()
            return final
        
        # Execute all tool calls (can be parallelized)
        results = [execute_tool(tc) for tc in tool_calls]
        
        # Inject tool responses
        tool_turn = format_tool_responses(results)
        messages.append({"role": "tool", "content": tool_turn})
    
    return "Agent reached maximum turn limit without completing the task."


# Example usage
if __name__ == "__main__":
    answer = run_agent("What is the current population of Tokyo?")
    print(answer)
```

---

## Conversation history after 2 tool calls

This shows the exact message structure for a 2-turn tool interaction:

```
[system] You are an agent... <tools>...</tools>
[user] What is the weather in Paris and London?
[assistant] I'll check both cities for you.
<tool_call>
{"name": "get_weather", "arguments": {"location": "Paris, France"}}
</tool_call>
<tool_call>
{"name": "get_weather", "arguments": {"location": "London, UK"}}
</tool_call>
[tool] <tool_response>
{"location": "Paris, France", "temp": 18, "condition": "partly cloudy"}
</tool_response>
<tool_response>
{"location": "London, UK", "temp": 14, "condition": "rainy"}
</tool_response>
[assistant] Here are the current weather conditions:
- **Paris**: 18°C, partly cloudy
- **London**: 14°C, rainy
```

---

## Stopping conditions

The loop terminates when:

1. **No tool call in response** — model has its answer
2. **Empty generation** — model produced nothing (shouldn't happen; retry once)
3. **MAX_TURNS reached** — safety limit hit; return partial result with a note
4. **Model emits a "done" signal** — some configurations use `<|im_end|>` as EOS, which the `stop` parameter handles

---

## Error recovery patterns

### Model produced malformed JSON in tool call

```python
try:
    call = json.loads(raw)
except json.JSONDecodeError:
    # Inject a helpful error rather than crashing
    messages.append({
        "role": "tool",
        "content": '<tool_response>\n{"error": "Could not parse tool call JSON. Please re-emit with valid JSON."}\n</tool_response>'
    })
    continue  # Let the model retry
```

### Tool execution raised an exception

```python
try:
    result = execute_tool(call)
except Exception as e:
    result = {"error": str(e), "type": type(e).__name__}
```

### Infinite loop detection

```python
seen_calls = set()
for call in tool_calls:
    key = (call["name"], json.dumps(call.get("arguments", {}), sort_keys=True))
    if key in seen_calls:
        # Model is repeating the same call — inject a hint
        result = {"error": "This tool was already called with identical arguments. The result was already provided. Please use the existing result."}
    else:
        seen_calls.add(key)
        result = execute_tool(call)
```
