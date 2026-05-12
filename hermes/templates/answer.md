# Answer Template

Use this template to craft every Hermes answer. The hard limit is **255 characters** (including spaces and punctuation). Count before you send.

## Template

```
{one-sentence answer to the core question}[. {one essential clarifying detail if needed}]
```

## Counting characters

- 255 characters ≈ 2–3 short sentences, or 1 medium sentence + a code snippet.
- Code snippets count. `ollama run hermes3` is 20 characters.
- If the answer is naturally shorter than 255, stop there — do not pad.

## Examples

**Question:** What is Hermes?

```
Hermes is NousResearch's open-source LLM family, fine-tuned on LLaMA/Mistral for strong instruction following and tool use.
```
(124 chars ✓)

---

**Question:** What prompt format does Hermes use?

```
Hermes uses ChatML: <|im_start|>role\ncontent<|im_end|>. Roles: system, user, assistant, tool.
```
(94 chars ✓)

---

**Question:** How do I run Hermes locally?

```
Easiest: ollama run hermes3. Or download GGUF from HuggingFace and run with llama.cpp --chat-template chatml.
```
(109 chars ✓)

---

**Question:** What models are in Hermes 3?

```
Hermes 3 has 8B, 70B, and 405B variants, all on LLaMA 3.1 base with 128k context. Released Aug 2024.
```
(101 chars ✓)

---

**Question:** How does tool calling work in Hermes?

```
Declare tools as JSON in system prompt. Model outputs <tool_call>{"name":"fn","arguments":{...}}</tool_call>. Return result in tool turn.
```
(137 chars ✓)

---

## When the answer cannot fit in 255 chars

Give the core fact + a pointer:

```
{core fact in ≤200 chars}. Full details: references/{file}.md
```

Example:
```
Hermes 3 405B needs ~230 GB VRAM at 4-bit. Full hardware guide: references/deployment.md
```
(89 chars ✓)

## Anti-patterns to avoid

- Do NOT start with "Sure!", "Of course!", "Great question!" — these waste characters.
- Do NOT repeat the question back.
- Do NOT use markdown headers or bullet lists inside the answer — plain text only.
- Do NOT add trailing "I hope this helps!" or similar.
- Do NOT exceed 255 characters. If you're at 254, stop there.
