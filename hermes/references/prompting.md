# Hermes Prompting Guide

Hermes uses the **ChatML** format. Using any other format degrades output quality significantly.

## ChatML format

```
<|im_start|>system
{system_prompt}<|im_end|>
<|im_start|>user
{user_message}<|im_end|>
<|im_start|>assistant
{assistant_response}<|im_end|>
```

### Token notes

- `<|im_start|>` and `<|im_end|>` are **single special tokens**, not character sequences.
- Roles: `system`, `user`, `assistant`, `tool` (for tool results in Hermes 2/3).
- The assistant turn ends with `<|im_end|>` during training; at inference, generation stops there automatically.

## System prompt

```
<|im_start|>system
You are Hermes, a helpful AI assistant.<|im_end|>
```

You can replace the system prompt with any persona or instruction set. Hermes follows system prompts reliably.

### Recommended default system prompt

```
You are Hermes, a helpful, harmless, and honest AI assistant.
```

## Multi-turn conversation

```
<|im_start|>system
You are a Python expert.<|im_end|>
<|im_start|>user
How do I reverse a list?<|im_end|>
<|im_start|>assistant
Use list[::-1] or list.reverse() (in-place).<|im_end|>
<|im_start|>user
Which is faster?<|im_end|>
<|im_start|>assistant
list[::-1] creates a copy; list.reverse() is faster (in-place, O(n)).<|im_end|>
```

## Using with inference frameworks

### llama.cpp / llama-cpp-python

Set `chat_format="chatml"` or pass the ChatML template manually.

```python
from llama_cpp import Llama

llm = Llama(model_path="hermes-3-8b.gguf", chat_format="chatml")
response = llm.create_chat_completion(messages=[
    {"role": "system", "content": "You are Hermes, a helpful assistant."},
    {"role": "user", "content": "Hello!"}
])
```

### vLLM

```python
from vllm import LLM, SamplingParams

llm = LLM(model="NousResearch/Hermes-3-Llama-3.1-8B")
# vLLM auto-detects ChatML from the tokenizer config
```

### Transformers

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("NousResearch/Hermes-3-Llama-3.1-8B")
# Use tokenizer.apply_chat_template() — it knows ChatML
messages = [
    {"role": "system", "content": "You are Hermes."},
    {"role": "user", "content": "What is 2+2?"}
]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
```

## Sampling parameters (recommended)

```
temperature: 0.7
top_p: 0.95
top_k: 40
repetition_penalty: 1.1
max_tokens: 2048
```

For deterministic/structured output (JSON, tool calls): use `temperature=0.0`.

## Common mistakes

- Forgetting the system turn entirely (still works, but quality drops slightly)
- Using `\n\n` between turns instead of ChatML tokens (breaks the model)
- Not closing turns with `<|im_end|>` (causes repetition or truncation)
- Injecting raw text after `<|im_start|>assistant` before letting the model generate
