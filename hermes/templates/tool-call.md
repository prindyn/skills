# Hermes Tool Call Templates

Copy-paste templates for the Hermes tool calling format. Use these when helping users set up function calling with Hermes.

## Minimal system prompt with one tool

```
<|im_start|>system
You are a function calling AI model. You have access to the following tools:

<tools>
[
  {
    "type": "function",
    "function": {
      "name": "TOOL_NAME",
      "description": "TOOL_DESCRIPTION",
      "parameters": {
        "type": "object",
        "properties": {
          "PARAM_NAME": {
            "type": "PARAM_TYPE",
            "description": "PARAM_DESCRIPTION"
          }
        },
        "required": ["PARAM_NAME"]
      }
    }
  }
]
</tools>

When you need to call a tool, use this exact format:
<tool_call>
{"name": "TOOL_NAME", "arguments": {"PARAM_NAME": "VALUE"}}
</tool_call><|im_end|>
```

## Tool result injection template

```
<|im_start|>tool
<tool_response>
{
  "result": "RESULT_VALUE"
}
</tool_response><|im_end|>
```

## Full single-tool conversation

```
<|im_start|>system
You are a function calling AI model.

<tools>
[{"type": "function", "function": {"name": "get_time", "description": "Get current time for a timezone", "parameters": {"type": "object", "properties": {"timezone": {"type": "string", "description": "IANA timezone, e.g. Europe/Paris"}}, "required": ["timezone"]}}}]
</tools><|im_end|>
<|im_start|>user
What time is it in Tokyo?<|im_end|>
<|im_start|>assistant
<tool_call>
{"name": "get_time", "arguments": {"timezone": "Asia/Tokyo"}}
</tool_call><|im_end|>
<|im_start|>tool
<tool_response>
{"time": "2024-08-15T14:32:00+09:00", "formatted": "2:32 PM JST"}
</tool_response><|im_end|>
<|im_start|>assistant
It's 2:32 PM JST in Tokyo.<|im_end|>
```

## Parallel tool calls template

```
<|im_start|>assistant
<tool_call>
{"name": "TOOL_NAME_1", "arguments": {"PARAM": "VALUE_1"}}
</tool_call>
<tool_call>
{"name": "TOOL_NAME_2", "arguments": {"PARAM": "VALUE_2"}}
</tool_call><|im_end|>
<|im_start|>tool
<tool_response>
{"result": "RESULT_1"}
</tool_response>
<tool_response>
{"result": "RESULT_2"}
</tool_response><|im_end|>
```

## Python integration template

```python
import json
from llama_cpp import Llama

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "TOOL_NAME",
            "description": "TOOL_DESCRIPTION",
            "parameters": {
                "type": "object",
                "properties": {
                    "PARAM": {"type": "string", "description": "PARAM_DESC"}
                },
                "required": ["PARAM"],
            },
        },
    }
]

SYSTEM_PROMPT = f"""You are a function calling AI model.

<tools>
{json.dumps(TOOLS, indent=2)}
</tools>

When calling a tool, use:
<tool_call>
{{"name": "TOOL_NAME", "arguments": {{...}}}}
</tool_call>"""

llm = Llama(model_path="hermes-3-8b.gguf", chat_format="chatml", n_ctx=4096)

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "USER_QUERY"},
]

response = llm.create_chat_completion(messages=messages, temperature=0.0)
assistant_msg = response["choices"][0]["message"]["content"]

# Parse tool call from assistant message
if "<tool_call>" in assistant_msg:
    call_json = assistant_msg.split("<tool_call>")[1].split("</tool_call>")[0].strip()
    tool_call = json.loads(call_json)
    # Execute tool_call["name"] with tool_call["arguments"]
    # Then inject result and call again
```
