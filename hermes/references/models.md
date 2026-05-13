# Hermes Models — Complete Reference

## Model family overview

NousResearch's Hermes series is a family of instruction-tuned and agentic large language models. Each release is built by fine-tuning a publicly available base model on curated high-quality data focused on instruction following, function calling, multi-turn conversation, and reasoning.

---

## Hermes 3 (2024 — current generation)

Based on Meta's **Llama 3.1** architecture. Hermes 3 is the most capable and recommended series for new projects.

### Variants

| Model ID (HuggingFace) | Params | Context | VRAM (fp16) | VRAM (Q4_K_M) |
|---|---|---|---|---|
| `NousResearch/Hermes-3-Llama-3.1-405B` | 405B | 128K | ~810 GB | ~230 GB |
| `NousResearch/Hermes-3-Llama-3.1-70B` | 70B | 128K | ~140 GB | ~40 GB |
| `NousResearch/Hermes-3-Llama-3.1-8B` | 8B | 128K | ~16 GB | ~5 GB |

### Key improvements over Hermes 2

- Extended context to 128K tokens (up from 32K)
- Better multi-step reasoning and planning
- Improved JSON and structured output fidelity
- More reliable parallel tool calls
- Enhanced persona/roleplay consistency across very long conversations
- Better handling of ambiguous instructions (asks clarifying questions rather than guessing)

### Recommended use cases for Hermes 3

- Complex agent pipelines with many tool calls
- Long-document analysis and Q&A
- Code generation and debugging
- Multi-persona assistants
- RAG (Retrieval-Augmented Generation) pipelines

---

## Hermes 2 Pro (2024)

Based on **Mistral 7B v0.1**. Hermes 2 Pro is the gold standard for function-calling in the 7B parameter class.

| Model ID | Params | Context | VRAM (fp16) | VRAM (Q4_K_M) |
|---|---|---|---|---|
| `NousResearch/Hermes-2-Pro-Mistral-7B` | 7B | 32K | ~14 GB | ~5 GB |
| `NousResearch/Hermes-2-Pro-Llama-3-8B` | 8B | 128K | ~16 GB | ~5 GB |

**Best for**: production deployments where 7–8B model size is a hard constraint and function calling accuracy is the top priority.

---

## Hermes 2 Theta (2024)

A **model merge** experiment combining Hermes 2 Pro with Mistral 7B via SLERP / DARE / TIES merging techniques. Intended to blend agentic capability with broader knowledge.

| Model ID | Params | Context |
|---|---|---|
| `NousResearch/Hermes-2-Theta-Llama-3-8B` | 8B | 128K |
| `NousResearch/Hermes-2-Theta-Llama-3-70B` | 70B | 128K |

---

## Hermes 2 (2023–2024)

Based on **Llama 2** and **Mistral** families. First major Hermes generation with strong general instruction following.

| Model ID | Params | Base |
|---|---|---|
| `NousResearch/Nous-Hermes-2-Mistral-7B-DPO` | 7B | Mistral 7B |
| `NousResearch/Nous-Hermes-2-Yi-34B` | 34B | Yi 34B |
| `NousResearch/Nous-Hermes-2-SOLAR-10.7B` | 10.7B | SOLAR |
| `NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO` | 46B MoE | Mixtral 8x7B |
| `NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT` | 46B MoE | Mixtral 8x7B |

---

## Hermes 1 (2023 — legacy)

The original Hermes model, fine-tuned on LLaMA 1. Historically significant but superseded.

| Model ID | Params | Base |
|---|---|---|
| `NousResearch/Nous-Hermes-13b` | 13B | LLaMA 1 13B |

---

## Quantization guide

GGUF quantized versions are available via Bartowski and other community quantizers on Hugging Face.

| Quant | Size reduction | Quality impact | Recommended for |
|---|---|---|---|
| **Q8_0** | ~50% | Negligible | Quality-sensitive production |
| **Q6_K** | ~60% | Very slight | Best balance |
| **Q5_K_M** | ~65% | Slight | Good all-rounder |
| **Q4_K_M** | ~70% | Moderate | **Minimum for reliable function calling** |
| **Q3_K_M** | ~75% | Noticeable | Simple Q&A only |
| **Q2_K** | ~80% | Significant | Not recommended for agents |

**IQ quants** (IQ4_XS, IQ3_M, etc.) from imatrix quantization can offer better quality at equivalent sizes compared to K quants, but require llama.cpp builds that support importance matrix quantization.

---

## Benchmark highlights (Hermes 3 8B vs peers)

| Benchmark | Hermes 3 8B | Llama 3.1 8B Instruct | Mistral 7B v0.3 |
|---|---|---|---|
| MT-Bench | ~8.1 | ~8.0 | ~7.6 |
| HumanEval (code) | ~68% | ~72% | ~60% |
| MMLU | ~68% | ~69% | ~63% |
| Function Call Acc. | ~85%* | ~78%* | ~55%* |
| Instruction Follow | Very high | High | Moderate |

*Approximate — varies by benchmark implementation and tool definition complexity.

---

## Model selection flowchart

```
Need function calling?
├── Yes → Hermes 3 8B (128K context) or Hermes 2 Pro 7B (32K context)
└── No → General reasoning / conversation?
    ├── Best quality → Hermes 3 70B or 405B
    ├── Good + fast → Hermes 3 8B
    └── Local 7B class → Hermes 2 Pro Mistral 7B

Have limited VRAM (<8 GB)?
└── Hermes 3 8B Q4_K_M via Ollama (~5 GB VRAM)

Long documents (>32K tokens)?
└── Hermes 3 series only (128K context)
```

---

## HuggingFace organization

All official models: **https://huggingface.co/NousResearch**

Community GGUF builds by Bartowski: search `bartowski/Hermes-3` on HuggingFace.
