# Hermes Model Variants

A complete reference for all Hermes model releases, sizes, and lineage.

## Hermes 1 (2023)

| Model | Base | Parameters | Notes |
|---|---|---|---|
| Hermes-LLaMA2-13b | LLaMA 2 | 13B | First Hermes release; curated instruction tuning |

- Dataset: GPT-4-generated dataset, ~300k examples
- Focus: Instruction following, coherence, reduced toxicity
- HuggingFace: `NousResearch/Hermes-LLaMA2-13b`

## Hermes 2 (2024)

| Model | Base | Parameters | Notes |
|---|---|---|---|
| Hermes-2-Pro-Mistral-7B | Mistral 7B | 7B | Function calling, JSON mode |
| Hermes-2-Pro-Llama-3-8B | LLaMA 3 | 8B | Strong tool use |
| Hermes-2-Theta-Llama-3-8B | LLaMA 3 | 8B | Merge of Pro + Llama-3-Instruct |
| Hermes-2-Pro-Llama-3-70B | LLaMA 3 | 70B | Large variant |

Key improvements over Hermes 1:
- Structured function calling via `<tool_call>` tags
- JSON mode for structured output
- Better multi-turn coherence
- Stronger code generation

HuggingFace: `NousResearch/Hermes-2-Pro-*`

## Hermes 3 (2024)

| Model | Base | Parameters | Notes |
|---|---|---|---|
| Hermes-3-Llama-3.1-8B | LLaMA 3.1 | 8B | Fast, local-friendly |
| Hermes-3-Llama-3.1-70B | LLaMA 3.1 | 70B | Balanced performance |
| Hermes-3-Llama-3.1-405B | LLaMA 3.1 | 405B | Flagship; SOTA on many benchmarks |

Released August 2024 in partnership with NVIDIA.

Key improvements over Hermes 2:
- Agentic task execution (multi-step planning)
- Superior reasoning and instruction following
- Improved structured output reliability
- Longer context handling (128k tokens on 3.1 base)
- Reduced hallucinations

HuggingFace: `NousResearch/Hermes-3-Llama-3.1-*`

## Choosing the right variant

```
Need speed + local?      → Hermes-3-Llama-3.1-8B
Need balance?            → Hermes-3-Llama-3.1-70B
Need best quality?       → Hermes-3-Llama-3.1-405B
Legacy / limited VRAM?  → Hermes-2-Pro-Mistral-7B
```

## Naming convention

```
Hermes-{generation}-{base_model}-{parameters}
         2 or 3        LLaMA/Mistral  8B/70B/405B
```

## VRAM requirements (approximate, 4-bit quantized)

| Model | VRAM |
|---|---|
| 8B | ~6 GB |
| 70B | ~40 GB |
| 405B | ~230 GB |

For consumer hardware, use 8B. For multi-GPU setups, 70B or 405B.
