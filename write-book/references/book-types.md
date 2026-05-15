# Book Types Reference

Five book types to propose to the user in Phase 0. Each type has a different structure,
chapter ordering, and reading experience. Match the book type to the site's content style
and the reader's likely goal.

---

## Type 1: Technical Reference

**Best for:** API documentation, full library references, exhaustive language specs, SDK docs.

**Reader goal:** Look up specific things quickly. Not read cover-to-cover.

**Signature traits:**
- Strong back-of-book index (the primary navigation tool)
- Dense table of contents
- Each chapter = one domain area or namespace
- Chapters ordered by domain, not by learning curve
- Code examples are primary, prose is secondary
- Appendix: edge cases, deprecated features, migration notes

**Chapter order template:**
1. Preface — who this reference is for and how to use it
2. Quick-Start / Getting Started (the one tutorial-style chapter)
3. Core Concepts (essential mental models, 1–2 chapters)
4. Domain A — all features/methods/flags for that area
5. Domain B
6. Domain C … (repeat per domain)
7. Configuration Reference
8. Appendix — deprecated APIs, version differences, error codes
9. Back-of-book Index (must be curated, not noisy)

**Index guidance:** A reference book lives or dies by its index. Curate aggressively. Every proper noun, method name, class name, flag name should be indexed. Generic terms ("Example", "Usage") should not.

**TOC depth:** 3 (show sub-sections so readers can navigate without opening each chapter)

---

## Type 2: Tutorial / Learning Book

**Best for:** Courses, step-by-step guides, how-to documentation, learning paths.

**Reader goal:** Build a skill progressively. Read mostly in order.

**Signature traits:**
- Strong narrative progression — each chapter builds on the last
- Chapter 1 must be accessible to the intended beginner
- Concepts before tools; principles before syntax
- Code examples appear after explanation, not before
- Exercises or "what you learned" summaries help
- Appendix: cheat sheets, reference cards, next-steps resources

**Chapter order template:**
1. Preface — who this book is for, prerequisites, what you'll be able to do at the end
2. Introduction — why this matters, the big picture
3. Part I: Foundations — the concepts a beginner needs first
4. Part II: Core Skills — the practical application of those concepts
5. Part III: Advanced Topics — extension, customization, edge cases
6. Conclusion — putting it all together, next steps
7. Appendix — quick-reference cards, cheat sheets, further reading

**Preface tone:** Encouraging, accessible. State explicitly what skills are assumed and what will be taught. Avoid jargon in the first paragraph.

**Opening chapter rule:** Chapter 1 must deliver a win — a working example, a solved problem, a concept fully understood. Never open with a dry overview chapter.

---

## Type 3: Conceptual Guide

**Best for:** Design pattern libraries, architecture guides, opinionated frameworks, philosophy docs.

**Reader goal:** Understand why, not just how. Build mental models.

**Signature traits:**
- Prose-heavy with code as illustration, not primary content
- Chapters explain principles; examples demonstrate them
- Connections between concepts are as important as the concepts themselves
- Anti-patterns and smells have their own chapter (equally important as patterns)
- Appendix: language-specific implementations, extended code listings

**Chapter order template:**
1. Preface — the philosophy behind this material, who benefits most
2. Foundational Principles (OOP, SOLID, DRY — whatever underlies the domain)
3. Core Concepts — the central ideas explained in depth
4. Pattern / Technique Catalog — grouped by theme, not alphabetically
5. Anti-patterns / Code Smells — what to avoid and why
6. Applying the Concepts — realistic worked examples
7. Appendix — code listings in multiple languages, extended examples
8. Index

**Key rule:** Every pattern/concept must answer three questions: What is it? When do you use it? What goes wrong if you don't? A conceptual guide that only answers the first question is a glossary, not a book.

---

## Type 4: Cookbook / Quick Reference

**Best for:** Command-line tools, recipe collections, cheat-sheet aggregations, pattern libraries with code.

**Reader goal:** Find a specific recipe and copy-paste or adapt it. Not read in order.

**Signature traits:**
- Short, self-contained chapters (each "recipe" stands alone)
- Consistent chapter structure: Problem → Solution → Discussion
- Heavy use of code blocks; minimal narrative prose
- TOC is the primary navigation tool
- Strong index for cross-referencing recipes
- No assumed reading order — chapters are not dependent on each other

**Chapter order template:**
1. Preface — how to use this cookbook, conventions used
2. [Domain A] Recipes — e.g. "File I/O", "Network", "Authentication"
3. [Domain B] Recipes
4. [Domain C] Recipes … (repeat per domain)
5. Appendix — common patterns across domains, quick-reference tables
6. Index

**Recipe structure per chapter:**

```
## Problem
What specific task does this recipe solve?

## Solution
The code. Show it immediately.

## Discussion
Why this approach? When does it fail? What are the alternatives?
```

**Chapter length:** Keep recipes short. 1–3 pages per recipe is ideal. A recipe that runs to 5+ pages probably needs to be split.

---

## Type 5: Narrative Explainer

**Best for:** Knowledge bases, wikis with a coherent topic arc, blogs on a single subject, long-form explainers.

**Reader goal:** Understand a subject in depth. More linear than lookup, more discursive than tutorial.

**Signature traits:**
- Flowing prose as the primary medium
- Code and examples appear where they illuminate text, not as the focus
- Chapters have narrative continuity — they reference each other
- The book has an argument or perspective, not just information
- Opens with "why this matters" and closes with synthesis
- Appendix: sources, further reading, raw reference material

**Chapter order template:**
1. Preface — the author's perspective, who this is for, what question the book answers
2. Chapter 1 — The opening hook: why does this matter? What problem does it solve?
3. Chapter 2–N — Building the case: concepts, evidence, examples, complications
4. The Turn — the most complex or surprising idea; the place where conventional wisdom breaks
5. Synthesis — how the pieces fit together; what to do with this understanding
6. Conclusion — what the reader now knows, and where to go next
7. Appendix — sources, glossary, technical details

**Voice:** Knowledgeable but accessible. Avoid passive voice. Use "you" to address the reader directly. Use examples from the real world, not hypotheticals.

**Opening rule (from strong non-fiction writing):** Begin in the middle of things. Don't open with "This book is about X." Open with a scene, a problem, a surprising fact, or a question. Give the reader a reason to keep reading before you explain what you're doing.

---

## Choosing between one book and two

If the site has two peer top-level sections of roughly equal depth (e.g. `/design-patterns` and `/refactoring`), treat them as two books rather than one large book with two halves.

**Two-book signal:**
- Two topics that a reader would buy separately
- Combined page count would exceed 300 pages
- The intended reader differs between sections
- Each section has its own introduction and is self-contained

**One book with Parts:**
- If keeping combined: use named Parts (`# Part I: Design Patterns`, `# Part II: Refactoring`)
- Each Part gets a 1-paragraph framing page stating what the Part covers
- The Preface explains the two-part structure upfront
