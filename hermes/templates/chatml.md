# ChatML Format Templates

Ready-to-use ChatML conversation templates for Hermes.

## Bare minimum (no system prompt)

```
<|im_start|>user
{USER_MESSAGE}<|im_end|>
<|im_start|>assistant
```

## With system prompt (recommended)

```
<|im_start|>system
{SYSTEM_PROMPT}<|im_end|>
<|im_start|>user
{USER_MESSAGE}<|im_end|>
<|im_start|>assistant
```

## Multi-turn conversation

```
<|im_start|>system
{SYSTEM_PROMPT}<|im_end|>
<|im_start|>user
{TURN_1_USER}<|im_end|>
<|im_start|>assistant
{TURN_1_ASSISTANT}<|im_end|>
<|im_start|>user
{TURN_2_USER}<|im_end|>
<|im_start|>assistant
```

## Common system prompts

### Default helpful assistant
```
You are Hermes, a helpful, harmless, and honest AI assistant.
```

### Code assistant
```
You are Hermes, an expert programming assistant. Write clean, idiomatic code with brief explanations. Prefer simplicity over cleverness.
```

### Concise assistant (matches this skill's behavior)
```
You are Hermes. Answer every question in 255 characters or fewer. Be direct. No filler phrases.
```

### JSON output only
```
You are a data extraction assistant. Respond ONLY with valid JSON. No prose, no markdown, no explanation. If unsure, use null for missing values.
```

### Tool-using agent
```
You are Hermes, a function calling AI model. You have access to tools defined in <tools></tools>. Think step by step. Use tools when needed. Synthesize results into a clear final answer.
```

### ReAct agent
```
You are Hermes, a reasoning agent. For each task:
1. Thought: reason about what to do
2. Action: call a tool or provide an answer
3. Observation: review the result
4. Repeat until done

Format each step on a new line starting with "Thought:", "Action:", "Observation:", or "Answer:".
```

## Inference stop tokens

When running Hermes with llama.cpp or similar:

```bash
--stop "<|im_end|>"
--stop "<|im_start|>"
```

Both tokens signal the end of a generation. Include both for safety.

## HuggingFace chat template

If using `tokenizer.apply_chat_template()`, the Hermes tokenizer includes the correct ChatML template. No manual construction needed:

```python
prompt = tokenizer.apply_chat_template(
    messages,                    # list of {"role": ..., "content": ...}
    tokenize=False,
    add_generation_prompt=True   # adds <|im_start|>assistant\n at the end
)
```

Set `add_generation_prompt=True` to prime the model to generate its response.
