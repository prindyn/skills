# Hermes Deployment Guide

All deployment options for running Hermes locally or via API.

## Option 1: Ollama (easiest local setup)

```bash
# Install Ollama (Mac/Linux/Windows)
curl -fsSL https://ollama.com/install.sh | sh

# Pull and run Hermes 3 8B
ollama run hermes3

# Pull specific variant
ollama pull nous-hermes2         # Hermes 2 (Mistral)
ollama pull nous-hermes2:34b     # Hermes 2 34B
ollama pull hermes3              # Hermes 3 8B
ollama pull hermes3:70b          # Hermes 3 70B
```

Ollama automatically handles ChatML formatting. Use via REST:

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "hermes3",
  "messages": [{"role": "user", "content": "Hello!"}]
}'
```

## Option 2: llama.cpp (GGUF, maximum control)

```bash
# Install llama.cpp
brew install llama.cpp  # Mac
# or build from source: https://github.com/ggerganov/llama.cpp

# Download GGUF model from HuggingFace
# Recommended: NousResearch/Hermes-3-Llama-3.1-8B-GGUF

# Run with ChatML template
./llama-cli \
  -m Hermes-3-Llama-3.1-8B.Q4_K_M.gguf \
  --chat-template chatml \
  -p "You are Hermes, a helpful AI assistant." \
  -cnv
```

Python binding:

```python
from llama_cpp import Llama

llm = Llama(
    model_path="Hermes-3-Llama-3.1-8B.Q4_K_M.gguf",
    chat_format="chatml",
    n_ctx=8192,
    n_gpu_layers=-1,  # Use all GPU layers
)

response = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are Hermes, a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    temperature=0.7,
    max_tokens=256,
)
print(response["choices"][0]["message"]["content"])
```

## Option 3: HuggingFace Transformers

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "NousResearch/Hermes-3-Llama-3.1-8B"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are Hermes, a helpful assistant."},
    {"role": "user", "content": "Explain photosynthesis in one sentence."},
]

prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.7, do_sample=True)
response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
print(response)
```

## Option 4: vLLM (high-throughput serving)

```bash
pip install vllm

python -m vllm.entrypoints.openai.api_server \
  --model NousResearch/Hermes-3-Llama-3.1-8B \
  --dtype bfloat16 \
  --max-model-len 32768
```

Then use via OpenAI-compatible API:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

response = client.chat.completions.create(
    model="NousResearch/Hermes-3-Llama-3.1-8B",
    messages=[{"role": "user", "content": "Hello, Hermes!"}],
)
print(response.choices[0].message.content)
```

## Option 5: Cloud APIs

Hermes 3 is available through:

| Provider | Model name | Notes |
|---|---|---|
| NVIDIA NIM | `nousresearch/hermes-3-llama-3.1-405b` | Optimized inference |
| Together AI | `NousResearch/Hermes-3-Llama-3.1-405B-FP8-tput` | FP8, high throughput |
| Fireworks AI | `accounts/fireworks/models/hermes-3-llama3p1-405b` | Fast inference |
| Perplexity | Via pplx-api | Check current availability |

## VRAM requirements

| Model | Full precision | 8-bit | 4-bit (Q4_K_M) |
|---|---|---|---|
| 8B | ~16 GB | ~9 GB | ~5 GB |
| 70B | ~140 GB | ~70 GB | ~40 GB |
| 405B | ~810 GB | ~405 GB | ~230 GB |

## Recommended hardware

- **Consumer (8B)**: RTX 3090/4090 (24 GB VRAM), M1/M2 Mac (16 GB+ unified memory)
- **Workstation (70B)**: 2× A100 80GB or 4× RTX 3090
- **Server (405B)**: 4–8× A100 80GB or H100 cluster
