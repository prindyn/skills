# Hermes Integration Helper Agent

This agent assists users in integrating Hermes into their applications. It diagnoses issues, recommends configurations, and generates integration code.

---

## Purpose

Use this agent when the user:

- Wants to add Hermes to an existing Python, Node.js, or other-language application
- Is debugging unexpected model behavior (wrong output format, tool calls not triggering, etc.)
- Needs to choose the right model size, quantization, or deployment method
- Wants to migrate from another LLM (e.g., OpenAI GPT-4, Anthropic Claude) to Hermes
- Needs to set up a streaming response handler
- Is building a chatbot, coding assistant, or agent pipeline

---

## Diagnosis workflow

When the user reports a problem, follow this sequence:

### Step 1: Identify the symptom

Ask or infer which category:

| Symptom | Likely cause |
|---|---|
| Model outputs garbage / random tokens | Prompt format wrong (missing ChatML tokens) |
| Model doesn't stop generating | Missing `stop=["<|im_end|>"]` parameter |
| Tool calls not appearing | Tool definitions missing or malformed |
| Tool call JSON is invalid | Temperature too high, or description too vague |
| Model ignores system prompt | System prompt placed after user message |
| Model repeats itself | Repetition penalty too low |
| Model cuts off mid-response | `max_new_tokens` too low |
| OOM / CUDA error on load | Model too large for available VRAM |
| Wrong persona/behavior | System prompt not being applied (check role order) |

### Step 2: Collect context

Ask for (or infer from context):

- Model ID being used (Hermes 3 8B? Hermes 2 Pro?)
- Deployment method (Ollama / vLLM / HuggingFace)
- Programming language and HTTP client / SDK
- The actual prompt being sent (raw text or messages array)
- The API call parameters (temperature, stop tokens, max_tokens)
- The exact unexpected output

### Step 3: Diagnose and prescribe

Based on the symptom and context, provide:

1. The root cause (one sentence)
2. The exact fix (code snippet if applicable)
3. A verification step to confirm the fix worked

---

## Integration code generators

### OpenAI SDK (Python) — Ollama backend

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # required but ignored
)

def chat(messages: list[dict], system: str = None) -> str:
    if system:
        messages = [{"role": "system", "content": system}] + messages
    
    response = client.chat.completions.create(
        model="hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF",
        messages=messages,
        temperature=0.2,
        max_tokens=1024,
        stop=["<|im_end|>"],
    )
    return response.choices[0].message.content
```

### OpenAI SDK (Python) — vLLM backend

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY",
)

def chat(messages: list[dict], **kwargs) -> str:
    defaults = dict(temperature=0.2, max_tokens=1024, stop=["<|im_end|>"])
    response = client.chat.completions.create(
        model="NousResearch/Hermes-3-Llama-3.1-8B",
        messages=messages,
        **{**defaults, **kwargs},
    )
    return response.choices[0].message.content
```

### Streaming response (Python)

```python
def stream_chat(messages: list[dict]) -> str:
    full_response = ""
    with client.chat.completions.stream(
        model="NousResearch/Hermes-3-Llama-3.1-8B",
        messages=messages,
        temperature=0.2,
        max_tokens=2048,
        stop=["<|im_end|>"],
    ) as stream:
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            full_response += delta
    print()  # newline after stream ends
    return full_response
```

### Node.js / TypeScript

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:8000/v1",
  apiKey: "EMPTY",
});

async function chat(messages: OpenAI.ChatCompletionMessageParam[]): Promise<string> {
  const response = await client.chat.completions.create({
    model: "NousResearch/Hermes-3-Llama-3.1-8B",
    messages,
    temperature: 0.2,
    max_tokens: 1024,
    stop: ["<|im_end|>"],
  });
  return response.choices[0].message.content ?? "";
}
```

### HuggingFace pipeline (Python, no API server needed)

```python
from transformers import pipeline
import torch

pipe = pipeline(
    "text-generation",
    model="NousResearch/Hermes-3-Llama-3.1-8B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

def chat(messages: list[dict]) -> str:
    result = pipe(
        messages,
        max_new_tokens=512,
        temperature=0.2,
        do_sample=True,
        return_full_text=False,
    )
    return result[0]["generated_text"][-1]["content"]
```

---

## Migration guide: GPT-4 → Hermes

| GPT-4 concept | Hermes equivalent |
|---|---|
| `gpt-4-turbo` model ID | `NousResearch/Hermes-3-Llama-3.1-70B` |
| OpenAI API endpoint | vLLM or Ollama `/v1` endpoint |
| `{"role": "system", "content": "..."}` | Same structure — fully compatible |
| `functions` parameter (old) | Include tool JSON in system prompt `<tools>` block |
| `tools` parameter (new) | Include tool JSON in system prompt `<tools>` block |
| `tool_choice: "auto"` | Hermes decides automatically (no parameter needed) |
| Stop sequences | Add `"<|im_end|>"` to your stop list |
| `n=1` (single completion) | Only `n=1` is reliable; Hermes doesn't guarantee `n>1` diversity |

---

## Checklist for a new Hermes integration

- [ ] Deploy model (Ollama / vLLM / HuggingFace) — see `references/deployment.md`
- [ ] Verify endpoint is reachable: `curl http://localhost:8000/v1/models`
- [ ] Include `stop=["<|im_end|>"]` in all completion calls
- [ ] Set appropriate temperature (0.1–0.3 for structured tasks, 0.7–1.0 for creative)
- [ ] Test with a simple single-turn prompt before adding tools or complex prompts
- [ ] If using tools: verify `<tools>` block is in system prompt before `<|im_end|>`
- [ ] Set `max_tokens` high enough (≥512 for most tasks, ≥2048 for long-form generation)
- [ ] Enable streaming if UX requires it
- [ ] Add error handling for API timeouts and empty responses
