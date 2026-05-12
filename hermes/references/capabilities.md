# Hermes Capabilities & Strengths

## Core strengths

### Instruction following
Hermes excels at following complex, multi-part instructions. It respects:
- System prompt personas and constraints
- Output format requirements (JSON, markdown, bullet lists, etc.)
- Negative constraints ("do not", "never", "avoid")
- Length constraints

This is the primary reason NousResearch built Hermes — to create a model that reliably does what it's told.

### Tool use & agentic behavior
Hermes 2 Pro and Hermes 3 are among the strongest open-source models for:
- Single-step function calling
- Parallel function calling (multiple tools at once)
- Multi-step agentic loops (call tool → observe result → call next tool)
- ReAct-style reasoning (Reason + Act cycles)

### Structured output
Hermes reliably produces well-formed:
- JSON objects and arrays
- XML structures
- Markdown tables
- Code (Python, JS, Bash, SQL, etc.)

### Reasoning
Hermes 3 (especially 70B and 405B) performs competitively with GPT-4-class models on:
- Mathematical reasoning
- Logical deduction
- Multi-step problem solving
- Code debugging

### Low hallucination rate
Hermes is specifically trained to say "I don't know" rather than fabricate. This is a deliberate design goal from NousResearch's data curation process.

### Code generation
Strong across major languages. Particularly good at:
- Python (data science, scripting, FastAPI, Django)
- JavaScript / TypeScript
- Bash scripting
- SQL

## Benchmark highlights (Hermes 3 - 405B)

| Benchmark | Score | Context |
|---|---|---|
| MT-Bench | ~9.0 | Strong instruction following |
| HumanEval | ~85% | Code generation |
| GSM8K | ~95% | Math reasoning |
| TruthfulQA | ~70% | Reduced hallucination |

*(Scores are approximate; check HuggingFace model cards for exact figures.)*

## Context window

| Generation | Context Length |
|---|---|
| Hermes 1 | 4,096 tokens |
| Hermes 2 (Mistral base) | 32,768 tokens |
| Hermes 2 (LLaMA 3 base) | 8,192 tokens |
| Hermes 3 (LLaMA 3.1 base) | 131,072 tokens (128k) |

## Languages

Primarily English, with reasonable performance in:
- French, German, Spanish, Italian (Western European)
- Chinese, Japanese, Korean (East Asian)
- Portuguese, Dutch, Russian

Performance degrades for low-resource languages.

## What Hermes is NOT good at

- **Real-time information**: No internet access; knowledge cutoff depends on base model training.
- **Multimodal input**: Text only (no images, audio, or video).
- **Guaranteed safety**: While reduced-toxicity, Hermes is NOT safety-tuned to the level of production APIs like Claude or GPT-4.
- **Tiny hardware**: 8B model is minimum for quality; 70B+ for complex tasks.

## Comparison vs other open models

| Model | Instruction | Tool Use | Context | Size |
|---|---|---|---|---|
| Hermes 3 405B | ★★★★★ | ★★★★★ | 128k | 405B |
| Hermes 3 70B | ★★★★☆ | ★★★★☆ | 128k | 70B |
| Llama 3.1 70B Instruct | ★★★★☆ | ★★★☆☆ | 128k | 70B |
| Mistral 7B Instruct | ★★★☆☆ | ★★☆☆☆ | 32k | 7B |
| Hermes 3 8B | ★★★★☆ | ★★★★☆ | 128k | 8B |
