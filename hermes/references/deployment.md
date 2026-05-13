# Hermes Deployment Guide

## Overview

Three primary deployment paths:

| Method | Startup time | OpenAI API compat | GPU required | Best for |
|---|---|---|---|---|
| **Ollama** | ~30 seconds | Yes (via `/v1`) | Optional (CPU fallback) | Local dev, quick start |
| **vLLM** | 1–5 minutes | Yes (native) | Yes | Production, high throughput |
| **HuggingFace Transformers** | 2–10 minutes | No (raw) | Recommended | Custom pipelines, fine-tuning |

---

## Ollama

Ollama is the fastest way to get Hermes running locally. It handles GGUF downloading, quantization selection, and model management.

### Install

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Pull and run

```bash
# Hermes 3 8B (recommended for local dev)
ollama run hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF

# Or via bartowski's Q4 quantization (smaller download)
ollama run hf.co/bartowski/Hermes-3-Llama-3.1-8B-GGUF:Q4_K_M
```

### OpenAI-compatible API

Once Ollama is running, it exposes an OpenAI-compatible endpoint at `http://localhost:11434/v1`:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    stop=["<|im_end|>"],
)
print(response.choices[0].message.content)
```

### Hardware requirements (Ollama)

| Model | VRAM (Q4_K_M) | CPU fallback |
|---|---|---|
| Hermes 3 8B | ~5 GB | Yes (slow) |
| Hermes 2 Pro 7B | ~5 GB | Yes (slow) |
| Hermes 3 70B | ~40 GB | Not practical |

---

## vLLM

vLLM is the standard for production deployments. It provides batching, continuous batching, PagedAttention, and a fully OpenAI-compatible API server.

### Install

```bash
pip install vllm
```

### Launch server

```bash
# Hermes 3 8B — full precision (requires ~16 GB VRAM)
vllm serve NousResearch/Hermes-3-Llama-3.1-8B \
  --dtype auto \
  --max-model-len 32768

# With 4-bit AWQ quantization (requires ~6 GB VRAM)
vllm serve NousResearch/Hermes-3-Llama-3.1-8B \
  --quantization awq \
  --dtype auto

# Hermes 3 70B across multiple GPUs
vllm serve NousResearch/Hermes-3-Llama-3.1-70B \
  --tensor-parallel-size 4 \
  --dtype auto
```

The server starts at `http://localhost:8000` with an OpenAI-compatible API.

### Connect via OpenAI client

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="NousResearch/Hermes-3-Llama-3.1-8B",
    messages=[...],
    temperature=0.2,
    max_tokens=1024,
    stop=["<|im_end|>"],
)
```

### vLLM important flags

| Flag | Purpose |
|---|---|
| `--max-model-len` | Reduce from default (128K) to save VRAM |
| `--tensor-parallel-size N` | Split model across N GPUs |
| `--quantization awq` | Load AWQ-quantized model |
| `--quantization gptq` | Load GPTQ-quantized model |
| `--gpu-memory-utilization 0.9` | Fraction of GPU memory to use (default 0.9) |
| `--enforce-eager` | Disable CUDA graphs (slower but less VRAM) |

---

## HuggingFace Transformers

For direct inference, fine-tuning, or custom pipeline work.

### Install

```bash
pip install transformers accelerate torch
```

### Basic inference

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "NousResearch/Hermes-3-Llama-3.1-8B"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the speed of light?"},
]

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.2,
        do_sample=True,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )

response = tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print(response)
```

### 4-bit quantization with bitsandbytes

```bash
pip install bitsandbytes
```

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
)
```

---

## Hardware requirements summary

| Model | Method | Min VRAM | Recommended |
|---|---|---|---|
| Hermes 3 8B | vLLM fp16 | 16 GB | RTX 4090, A10G |
| Hermes 3 8B | Ollama Q4 | 5 GB | RTX 3060 12GB |
| Hermes 3 8B | vLLM AWQ | 6 GB | RTX 3080 10GB |
| Hermes 2 Pro 7B | vLLM fp16 | 14 GB | RTX 4080 |
| Hermes 3 70B | vLLM fp16 | 140 GB | 4× A100 80GB |
| Hermes 3 70B | vLLM AWQ | 40 GB | 2× A100 40GB |
| Hermes 3 70B | Ollama Q4 | 40 GB | 2× A100 40GB |
| Hermes 3 405B | vLLM fp16 | 810 GB | 8× H100 |
| Hermes 3 405B | vLLM AWQ | 210 GB | 4× H100 |

---

## Docker deployment (vLLM)

```dockerfile
FROM vllm/vllm-openai:latest

ENV MODEL=NousResearch/Hermes-3-Llama-3.1-8B
ENV MAX_MODEL_LEN=32768

CMD vllm serve $MODEL --max-model-len $MAX_MODEL_LEN --dtype auto
```

```bash
docker run --gpus all -p 8000:8000 \
  -e HF_TOKEN=$HF_TOKEN \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  hermes-server
```

---

## Environment variables

| Variable | Purpose |
|---|---|
| `HF_TOKEN` | HuggingFace access token (for gated repos) |
| `HF_HOME` | Cache directory for model weights |
| `CUDA_VISIBLE_DEVICES` | Select specific GPUs |
| `VLLM_WORKER_MULTIPROC_METHOD` | Set to `spawn` if fork causes issues |

---

## Gotchas

- **Model weights can be large.** Hermes 3 8B is ~16 GB in fp16. Use a volume mount or shared cache directory across containers.
- **vLLM by default tries to load the full context length into its KV cache.** If you get OOM, reduce `--max-model-len` (e.g., 16384 instead of 128000).
- **Ollama uses its own model management.** Don't mix Ollama and HuggingFace model paths — they use different formats.
- **Chat template must match the model.** Always use `apply_chat_template` from the same tokenizer as the model. Mismatched templates silently degrade output quality.
- **`pad_token_id` needs to be set.** HuggingFace will warn if not set; use `tokenizer.eos_token_id` as the pad token.
