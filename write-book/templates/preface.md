# Preface Template

Use this template to write the book's Preface. Replace every `[...]` placeholder
with content specific to this book and its reader.

Save the finished file as `crawl_output/pages/0000_preface.md`.

**Critical rules:**
- Write in the voice of a knowledgeable author addressing the reader directly
- Never mention scraping, crawling, PDF generation, or tool names
- Never explain how the book was assembled or how many pages were processed
- Aim for 200–500 words — long enough to be useful, short enough to respect the reader's time
- Read it aloud before saving — if it sounds like software documentation, rewrite it

---

## Template

```markdown
# Preface

[Opening hook — a question, a problem, or a surprising observation that draws
the reader in. Do not open with "This book is about X." Open with something
that makes the reader want to read the next sentence.]

[Example for a design patterns book:
"If you've ever inherited a codebase where every change ripples unpredictably
through the entire system, you already know why design patterns matter.
The patterns in this book are not theoretical abstractions — they are
hard-won solutions to problems that repeat across every language, every team,
and every decade of software development."]

---

[Audience paragraph — who this book is for, stated plainly. Include both who
it IS for and, if helpful, who it is NOT for.]

[Example:
"This book is for software engineers who already understand object-oriented
programming and want to move from writing code that works to writing code that
lasts. You should be comfortable reading and writing classes, interfaces, and
inheritance hierarchies in at least one OOP language. If you're still learning
the basics of programming, a foundational course will serve you better here."]

---

[Scope paragraph — what's covered and what isn't. Be specific about both.]

[Example:
"The book covers all 23 Gang of Four design patterns, organized by family —
Creational, Structural, and Behavioral. Each pattern is explained with a
concrete motivation, a clear solution structure, and working code examples.
What this book does not cover: language-specific frameworks, architectural
patterns (MVC, CQRS), or distributed systems patterns — those deserve books
of their own."]

---

[How to read paragraph — recommend an approach based on the book type.]

[For a reference book:
"You don't need to read this book front to back. If you're facing a specific
design problem, use the table of contents to find the relevant pattern family.
If you're newer to patterns, start with the Foundational Principles chapter
before diving into the catalog — the patterns will make more sense with that
context."]

[For a tutorial book:
"The chapters build on each other. Resist the temptation to skip ahead — each
chapter introduces concepts that later chapters depend on. The Appendix contains
extended code examples you can return to after completing the main chapters."]

---

[Closing — what the reader will be able to do, think, or build after reading.
Be specific. Avoid vague promises like "improve your skills."]

[Example:
"By the end of this book, you'll be able to recognize common design problems
by name, choose the right structural solution, and explain your architectural
decisions to your team in a shared vocabulary. You'll also know which patterns
to be suspicious of — the ones that add complexity without proportional benefit.
That skepticism is as valuable as the patterns themselves."]
```

---

## Anti-patterns to avoid in the Preface

**Don't write this:**
> "This document is a compiled edition of [website], assembled for offline reading.
> Content has been organized thematically for a reading experience rather than
> following the original site navigation order."

**Write this instead:**
> "Design patterns are one of those topics that make more sense the second time
> you encounter them. This book is organized to give you that second encounter
> right — foundational concepts first, so that when you reach the pattern catalog,
> you already have the vocabulary to understand why each pattern exists."

---

**Don't write this:**
> "We scraped 247 pages from refactoring.guru and deduplicated 43 near-identical
> entries before organizing the remaining content into 8 chapters."

**Write this instead:**
> "This is a complete reference to the patterns most commonly applied in
> object-oriented systems — from the simplest structural improvements to the
> more sophisticated behavioral arrangements that separate maintainable codebases
> from fragile ones."

---

The difference: one version tells the reader about the production process.
The other version speaks directly to why the reader picked up this book.
Only the second version serves the reader.
