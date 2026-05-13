# Hermes Prompt Format — Complete Reference

## ChatML

All Hermes models use **ChatML** (Chat Markup Language), a token-level conversation format originating from OpenAI's GPT-4 fine-tuning framework. Hermes uses the same `<|im_start|>` / `<|im_end|>` special tokens as its delimiter pair.

---

## Special tokens

| Token | ID (Llama 3.1 tokenizer) | Meaning |
|---|---|---|
| `<|im_start|>` | 128006 | Begin a message turn |
| `<|im_end|>` | 128009 | End a message turn |
| `<|begin_of_text|>` | 128000 | Start of the full sequence |
| `<|end_of_text|>` | 128001 | End of the full sequence (EOS) |

These tokens are part of the **tokenizer vocabulary**, not plain text. Never insert them as literal character sequences in raw string manipulation — always use the tokenizer's `apply_chat_template()` method or construct them properly.

---

## Message roles

| Role | Usage |
|---|---|
| `system` | Initial instructions, persona, tool definitions, constraints |
| `user` | Human turn |
| `assistant` | Model turn (also used for injecting few-shot examples) |
| `tool` | Tool call result injected by the runtime |

---

## Single-turn format

```
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
What is 2 + 2?<|im_end|>
<|im_start|>assistant
```

The model generates its response starting from the open `assistant` block and appends `<|im_end|>` when done.

---

## Multi-turn format

```
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
Tell me a joke.<|im_end|>
<|im_start|>assistant
Why don't scientists trust atoms? Because they make up everything!<|im_end|>
<|im_start|>user
That's terrible. Give me a better one.<|im_end|>
<|im_start|>assistant
```

---

## System prompt best practices

### Length
Keep system prompts under **500 tokens** for best results. Beyond 1K tokens you're consuming context that the model uses for reasoning. Tool definitions are an exception — use as many as needed, but keep individual descriptions concise.

### Persona definition
```
<|im_start|>system
You are Hermes, a knowledgeable and direct AI assistant. You give concise, accurate answers. When uncertain, you say so rather than guessing. You never make up facts.
<|im_end|>
```

### Task scoping
```
<|im_start|>system
You are a Python code reviewer. Your only job is to review Python code for bugs, style issues, and security vulnerabilities. Do not answer questions unrelated to code review.
<|im_end|>
```

### Response format instructions
```
<|im_start|>system
Always respond in JSON with this structure:
{"answer": "...", "confidence": 0.0-1.0, "sources": ["..."]}
<|im_end|>
```

---

## Using `apply_chat_template`

The recommended way to format prompts in Python is via HuggingFace's tokenizer:

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("NousResearch/Hermes-3-Llama-3.1-8B")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, who are you?"},
]

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,  # adds the open <|im_start|>assistant tag
)
```

`add_generation_prompt=True` appends the open `<|im_start|>assistant\n` so the model knows to generate a response.

---

## Sampling parameters

These defaults work well for most tasks. Adjust based on the use case.

| Parameter | Agentic / precise | Creative / chat | Notes |
|---|---|---|---|
| `temperature` | 0.1–0.3 | 0.7–1.0 | Higher = more varied |
| `top_p` | 0.9 | 0.95 | Nucleus sampling cutoff |
| `top_k` | 40 | 50 | Vocabulary cutoff per step |
| `repetition_penalty` | 1.1–1.2 | 1.05–1.1 | Prevents loops |
| `max_new_tokens` | task-dependent | 512–2048 | Cap generation length |

**Stop tokens**: Always set `stop=["<|im_end|>"]` (or the equivalent EOS token ID `128009`). Without a stop token the model will generate through the end of the turn and begin the next turn.

```python
# vLLM / OpenAI-compat API
response = client.chat.completions.create(
    model="hermes-3-8b",
    messages=messages,
    temperature=0.2,
    max_tokens=1024,
    stop=["<|im_end|>"],
)
```

---

## Few-shot examples

Inject worked examples as `assistant` turns before the real user query:

```
<|im_start|>system
You extract structured data from text. Output only JSON.<|im_end|>
<|im_start|>user
Text: "John Smith, age 34, called on 2024-01-15."<|im_end|>
<|im_start|>assistant
{"name": "John Smith", "age": 34, "date": "2024-01-15"}<|im_end|>
<|im_start|>user
Text: "Alice Johnson (28) emailed on March 3rd."<|im_end|>
<|im_start|>assistant
```

The model will pattern-match and output JSON for the new input.

---

## Chain-of-thought prompting

Hermes responds well to explicit reasoning requests:

```
<|im_start|>system
Before answering, think step by step. Write your reasoning inside <thinking>...</thinking> tags, then give your final answer.
<|im_end|>
```

The model will produce:

```
<thinking>
The user wants to know X. Step 1: ... Step 2: ...
</thinking>

Final answer: ...
```

---

## Common formatting mistakes

| Mistake | Effect | Fix |
|---|---|---|
| Missing `<|im_end|>` after a message | Tokenizer confusion, degraded output | Always close each turn |
| Closing the final `assistant` tag | Model doesn't generate (token budget exhausted) | Leave last `assistant` tag open |
| Using plain text instead of tokens | Works partially but not reliable | Use `apply_chat_template` |
| No system prompt at all | Model defaults to generic behavior | Always include a system prompt |
| System prompt after user message | Ignored or confuses turn order | System prompt must be first |
| Inconsistent newline style | Minor quality degradation | Use `\n` consistently |
