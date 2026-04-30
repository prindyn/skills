# The Seven Mistakes — Condensed Reference

A compressed working version of the listicle. Use this as your diagnostic and rewrite playbook.

---

## 1. Writing novels instead of instructions

**What it looks like:** the user opens with industry, audience, goals, history, and reasons before stating what they want. The actual instruction is buried in paragraph 3.

**Why it fails:** LLMs use attention to weight input. A wall of context dilutes the signal. The model can't tell whether your company's mission is the focus or your actual ask is. It guesses, and often guesses wrong — producing output that "sounds relevant but misses your requirements."

**Diagnostic cues:**
- Instruction is <25% of total prompt length
- Multiple paragraphs of "we are a…" or "our company…" before the ask
- Reasons / justifications for *why* the user wants the output (the model doesn't need these)

**The fix:** write API documentation, not a creative brief.
- Lead with the imperative: "Write three subject lines…"
- Keep only context that *changes the output*
- Test: "If I delete this sentence, does output quality drop?" If no, delete.

**Worked example from the source:**

Before:
> "We're a B2B SaaS company in the project management space targeting mid-market companies with 50-200 employees who currently use spreadsheets…"

After:
> "Write three benefit-focused subject lines for a project management tool. Target: operations managers at 50-200 person companies. Tone: professional but approachable. Each under 50 characters."

Same request, ~75% less text, dramatically better results.

---

## 2. Skipping output format specifications

**What it looks like:** prompt specifies *what* to write but says nothing about *how it should look* — length, structure, format. User then spends 15 minutes reformatting by hand. Repeat across every prompt → hours weekly.

**Why it fails:** when format isn't specified, the model picks. Sometimes it aligns with what you need. Usually it doesn't.

**Diagnostic cues:** search the prompt for words like "words," "bullets," "list," "JSON," "markdown," "headers," "sections," length numbers. None? → flag this.

**The fix:** treat format as a first-class requirement, not a polish step.

Specify, in order of common need:
- **Length:** "Write 250–300 words" / "Exactly 5 bullet points"
- **Structure:** "Output as numbered list" / "Format as JSON with keys for title, description, tags"
- **Sections:** "Include sections for: Problem, Solution, Implementation Steps, Expected Results"
- **Visual elements:** "Use H2 headers for each main section"

**Worked example:**
```
Format requirements:
- Use H2 headers for each main section
- Include exactly 3 bullet points per section
- Each bullet: 15-25 words
- End with single-sentence key takeaway
- Total length: 400-500 words
```

Format specs usually improve content quality too — they force more deliberate organization.

---

## 3. Testing prompts only once before production

**What it looks like:** user writes a prompt, runs it, output looks great, they save it and start using it for client work. Two weeks later it produces something completely wrong.

**Why it fails:** LLMs are probabilistic, not deterministic. Same prompt → different outputs each run, sometimes structurally different. One good run is luck, not validation.

**Diagnostic cues:** user says "it worked when I tested it," "I ran it once and it looked great," or is putting a prompt into recurring/automated use without mentioning multi-run testing.

**The fix:** before trusting any prompt for repeated use, run it 5–10 times. Read all outputs side by side.

Look for consistency in:
- Structure
- Quality
- Tone
- Constraint adherence

If you see significant variation, the prompt is under-constrained — either ambiguous or missing format/constraint specs. Tighten and re-test.

The math: testing 5× takes 5 minutes. Discovering the prompt is unreliable after 10 client projects takes 5 hours to fix.

---

## 4. Ignoring model-specific syntax and capabilities

**What it looks like:** user crafts a great prompt for ChatGPT, then sends the exact same prompt to Claude. Output is different or worse. They conclude Claude is worse and stick with what they had.

**Why it fails:** models aren't interchangeable. Different strengths, different syntax preferences, different content policies.

**Adaptation patterns:**

**For Claude:** use XML-style tags. The model is trained to recognize them.
```
<instructions>...</instructions>
<context>...</context>
<example>...</example>
```

**For GPT:** split the role.
- System message → role definition, persona, guidelines
- User message → the specific task

**Refusals:** Claude tends to refuse certain requests GPT-4 handles fine, and vice versa. Reframing in model-appropriate language usually solves it.

**The fix:**
- Build working knowledge of each model the user uses regularly
- Maintain model-specific versions of important prompts
- Read the official prompting docs (Anthropic / OpenAI publish them; most users skip)

Analogy: you wouldn't write identical SQL for PostgreSQL and MySQL. LLMs deserve the same care.

---

## 5. Burying critical instructions at the end

**What it looks like:** prompt opens with context, then adds the critical constraint last: "Oh, and keep it under 100 words" or "don't mention competitors." Output ignores the constraint.

**Why it fails:** LLMs show **primacy bias** — earlier tokens get more weight. Constraints at the end land as afterthoughts.

**Diagnostic cues:**
- Word limits, "must not," "do not include," or other non-negotiables appearing in the last third of the prompt
- Constraints embedded mid-paragraph rather than visually separated

**The fix:** invert the structure. Lead with the non-negotiables.

**Worked example:**

Before:
> "I'm working on a marketing campaign for our productivity app. We're targeting remote workers. The market is crowded with competitors like Asana and Monday. Can you write a LinkedIn post? Keep it under 150 words and don't mention competitors."

After:
> "Write a LinkedIn post, maximum 150 words, no competitor mentions. Topic: productivity app for remote workers. Key differentiator: AI-powered async features. Context: market includes Asana, Monday but we're not naming them."

Same information, requirements first.

**Visual reinforcement:**
- Bullet the constraints at the top
- Use labels: `Requirements:`, `Constraints:`, `Must:`, `Must not:`
- Line breaks between critical instructions and supporting info

---

## 6. Assuming the model shares your context

**What it looks like:** user opens a new chat and writes "Now do the same thing but for the enterprise segment." They reference "the approach we discussed" or "our target audience" that was never defined. Output misses entirely because the model doesn't know what they're talking about.

**Why it fails:** every new chat starts from zero context. The model doesn't remember previous chats, doesn't know your product, audience, or norms. Context that's vivid in your head is invisible to it.

**Diagnostic cues:** pronouns and references with no antecedent in the current prompt:
- "the same thing"
- "our audience" / "our usual tone"
- "as before" / "the approach we discussed"
- "this project" (with no description of the project)

**The fix:** make every prompt self-contained. Before writing the instruction, ask: "What does the model need to know to do this well?" Then write it down.

For recurring contexts (your product, your audience, your style guide), build **reusable context blocks** — saved snippets you paste in. This turns slow context-setting into fast context-setting.

When referring to previous output, be specific: not "do the same thing" but "write another product description using the same format: 2–3 sentences on benefits, followed by 3 bullet points listing features."

---

## 7. Manually tweaking instead of building reusable templates

**What it looks like:** user writes a product description prompt, tweaks the output, ships. Next week, writes a similar prompt from scratch, tweaks again. Repeat for months. Same problem, solved repeatedly instead of solved once.

**Why it fails:** every solve-from-scratch is a missed opportunity to build leverage. The cycle compounds into massive time waste.

**Diagnostic cue:** user describes recurring work, or has shown you several similar prompts in the same conversation.

**The fix:** when you spot a pattern, extract a template. Keep the structure and constraints; bracket the variables.

**Worked example:**
```
Write an introduction for a blog post about [TOPIC].
Target audience: [AUDIENCE].
Tone: [TONE].
Length: 150-200 words.
Structure: hook, context, preview of main points.
```

Now they fill in brackets — same quality, ~80% less time.

**The math:** template takes 10 minutes to build. Used twice per week, saves 5 minutes each time. Positive return after 2 weeks. Compounds indefinitely.

**Where to store:** note-taking app, text expander, prompt library — the storage method matters less than having one. The user's prompt library should be an appreciating asset, not a blank slate every time.

---

## Default rewrite shape

When applying fixes, structure the rewritten prompt in this order:

```
[1] Core instruction (one imperative line)
[2] Format requirements (bulleted)
[3] Constraints / non-negotiables
[4] Context (only what changes the output)
[5] Examples (if relevant)
```

For Claude, wrap structured pieces in XML-style tags.
For GPT, split [4]–[5] into the system message and [1]–[3] into the user message.

---

## Quick diagnostic table

| Symptom in user's prompt | Mistake |
|---|---|
| Backstory dominates, instruction buried | #1 Novels |
| No length / structure / format mentioned | #2 No format spec |
| "I ran it once and it worked" | #3 One-shot trust |
| Generic prompt for Claude or GPT | #4 Model-blind |
| Word limit / "don't…" near the end | #5 Buried constraints |
| "the same thing," "our audience" | #6 Assumed context |
| "I do this every week" | #7 No template |
