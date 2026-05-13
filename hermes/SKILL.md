---
name: hermes
description: Comprehensive knowledge base for NousResearch's Hermes LLM family — including all model versions, ChatML prompt formatting, function/tool calling, deployment methods, and agent architecture patterns. Use this skill whenever the user asks about Hermes models, wants to deploy or run Hermes, needs to format prompts or tool calls for Hermes, is debugging Hermes output, comparing Hermes to other models, or building an agent pipeline powered by Hermes. Also trigger when the user mentions Nous Hermes, Hermes 2, Hermes 2 Pro, Hermes 3, or any NousResearch model.
compatibility: Requires internet access for model downloads. Scripts require Python 3.10+ and uv. Deployment options include Ollama, vLLM, or HuggingFace Transformers.
metadata:
  author: hermes-skill
  version: "1.0"
  topic: NousResearch Hermes LLM agent
---

# Hermes Agent — Complete Knowledge Base

Hermes is NousResearch's flagship open-source LLM family, fine-tuned for agentic tasks: function calling, multi-step reasoning, structured output, and persona-based interaction. This skill gives you everything you need to understand, deploy, prompt, and extend Hermes.

## Quick reference

| Model | Base | Params | Context | Key strength |
|---|---|---|---|---|
| Hermes 3 405B | Llama 3.1 | 405B | 128K | Best overall quality |
| Hermes 3 70B | Llama 3.1 | 70B | 128K | Strong + deployable |
| Hermes 3 8B | Llama 3.1 | 8B | 128K | Fast, local-friendly |
| Hermes 2 Pro 7B | Mistral 7B | 7B | 32K | Function calling specialist |
| Hermes 2 Theta 8x7B | Mixtral | 46B MoE | 32K | Mixture-of-experts blend |

See [references/models.md](references/models.md) for full version history, benchmarks, and download links.

## Core concepts

### What makes Hermes different

Hermes models are fine-tuned on high-quality instruction, conversation, and agentic data curated by NousResearch. The key differentiators:

- **Native function/tool calling** — structured XML-wrapped JSON format, consistent across versions
- **Deep instruction alignment** — follows nuanced system prompts reliably
- **Persona stability** — maintains character / role across long conversations
- **Reasoning quality** — supports chain-of-thought and multi-step planning
- **ChatML tokenization** — uses `<|im_start|>` / `<|im_end|>` special tokens

### Prompt format (ChatML)

All Hermes models use the **ChatML** format. Every message is wrapped in role markers:

```
<|im_start|>system
You are a helpful assistant named Hermes.<|im_end|>
<|im_start|>user
What is the capital of France?<|im_end|>
<|im_start|>assistant
```

The model generates from the open `<|im_start|>assistant` token forward. Do **not** close the final assistant tag — the model closes it when done.

See [references/prompt-format.md](references/prompt-format.md) for full details: multi-turn examples, special tokens, sampling parameters, and common mistakes.

### Function / tool calling

Hermes uses an XML-wrapped JSON schema for tool use. The model emits calls inside `<tool_call>` tags; your code injects results inside `<tool_response>` tags.

```
<tool_call>
{"name": "get_weather", "arguments": {"location": "Paris", "unit": "celsius"}}
</tool_call>
```

Respond with:

```
<tool_response>
{"temperature": 18, "condition": "partly cloudy"}
</tool_response>
```

See [references/function-calling.md](references/function-calling.md) for full tool definition schemas, multi-tool calls, parallel calls, and error handling patterns.

### Agent loop architecture

Hermes is designed for the **ReAct** (Reason + Act) pattern:

1. Receive user task + tool list in system prompt
2. Model reasons ("Thought: ...") then emits a `<tool_call>`
3. Your runtime executes the call and returns `<tool_response>`
4. Model resumes reasoning with the result
5. Repeat until model produces a final answer (no tool call in generation)

See [templates/agent-loop.md](templates/agent-loop.md) for a complete agent loop template with system prompt, tool definitions, and loop pseudocode.

## Deployment

Three primary ways to run Hermes:

| Method | Best for | Command |
|---|---|---|
| **Ollama** | Local dev, quick start | `ollama run hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF` |
| **vLLM** | Production, OpenAI API compat | `vllm serve NousResearch/Hermes-3-Llama-3.1-8B` |
| **HuggingFace** | Custom pipelines, fine-tuning | `AutoModelForCausalLM.from_pretrained(...)` |

See [references/deployment.md](references/deployment.md) for full setup instructions, hardware requirements, quantization options, and OpenAI-compatible API configuration.

## Available scripts

- **`scripts/format_prompt.py`** — Format a conversation into ChatML; accepts JSON and outputs a ready-to-send string
- **`scripts/validate_function_call.py`** — Validate a Hermes `<tool_call>` block against a tool schema
- **`scripts/test_connection.py`** — Smoke-test an Ollama or vLLM endpoint to confirm Hermes is responding

## Gotchas

- **Always use `<|im_end|>` after each message.** Omitting it confuses the tokenizer and generates garbage.
- **Do not close the final assistant tag.** Leave the last `<|im_start|>assistant` open — the model appends its response and then closes it.
- **Set `stop=["<|im_end|>"]` in your API call.** Without this, the model will continue generating past its response boundary.
- **Temperature 0 breaks creativity.** For agentic / reasoning tasks, use 0.1–0.3. For creative tasks, 0.7–1.0.
- **Repetition penalty matters.** Values between 1.1 and 1.2 prevent looping. Higher values hurt quality.
- **System prompt length counts.** Very long system prompts (>2K tokens) reduce effective context for user content — keep tool definitions concise.
- **Hermes 2 Pro and Hermes 3 use slightly different tool call formats.** Hermes 3 prefers the `<tool_call>` XML wrapper; Hermes 2 Pro may output bare JSON in some configurations. See [references/function-calling.md](references/function-calling.md#version-differences).
- **GGUF quantization affects function calling.** Q4_K_M is the minimum safe quantization for reliable tool use; Q2 and Q3 degrade structured output significantly.

## Choosing the right model size

- **8B**: Good for single-turn Q&A, simple tool use, low-latency tasks. Runs on a single consumer GPU (16 GB VRAM with Q4).
- **70B**: Best balance of quality and deployability. Requires 2×40 GB or 4×24 GB GPUs at full precision; fits on 1×80 GB with Q4.
- **405B**: Research / high-stakes production use. Needs 4–8×80 GB GPUs or multi-node.
- **Hermes 2 Pro 7B**: If your task is almost entirely function calling and you need the smallest possible footprint.

## Useful links (read-only reference)

For deeper dives, load these references on demand:

- Model versions and benchmarks → [references/models.md](references/models.md)
- Prompt formatting and sampling → [references/prompt-format.md](references/prompt-format.md)
- Function / tool calling → [references/function-calling.md](references/function-calling.md)
- Deployment guide → [references/deployment.md](references/deployment.md)
- System prompt templates → [templates/system-prompt.md](templates/system-prompt.md)
- Agent loop template → [templates/agent-loop.md](templates/agent-loop.md)
- Function definition template → [templates/function-definition.json](templates/function-definition.json)
