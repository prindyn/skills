---
name: code-refactor
description: Review code and refactor it following "Refactoring and Design Patterns" — covering code smells, refactoring techniques, and the 22 classic GoF design patterns. Use this skill whenever the user wants to improve messy or hard-to-maintain code, identify code smells (long methods, large classes, duplicate code, feature envy, switch statements, etc.), apply named refactoring techniques (Extract Method, Move Field, Replace Conditional with Polymorphism, etc.), migrate toward a design pattern (Factory, Strategy, Observer, Decorator, etc.), reduce technical debt, prepare code for a new feature, clean up during a bug fix, or get a thorough code review with actionable improvements. Activate even when the user says "clean up my code", "this is messy", "help me refactor", or "review this".
author: vprindyn@gmail.com
version: "1.0"
---

# Code Refactor Skill

Guide code review and refactoring sessions using the methodology from *Refactoring and Design Patterns*. The book has two parts that complement each other: Part I teaches you to recognize what is wrong with code and how to fix it mechanically; Part II gives you the target shapes worth moving toward.

## Reference Files

Load these on demand — don't load all at once unless you need everything:

| File | Load when… |
|------|-----------|
| `references/code-smells.md` | Identifying problems in the code |
| `references/refactoring-techniques.md` | Choosing how to fix a detected smell |
| `references/design-patterns.md` | Recommending a structural target to refactor toward |
| `references/quick-reference.md` | Quick smell → technique → pattern lookup |

Supporting tools:
- `scripts/analyze.py` — Static analysis: run against a Python file to detect smells automatically
- `scripts/report.py` — Render a JSON analysis result as a Markdown report
- `templates/refactoring-plan.md` — Fill in when planning a multi-step refactoring
- `templates/review-report.md` — Fill in to deliver a complete code review
- `assets/smell-checklist.md` — Walk through every smell category systematically
- `assets/pattern-decision-tree.md` — Decision guide for selecting the right design pattern
- `agents/smell-detector.md` — Instructions for a dedicated smell-detection sub-pass
- `agents/pattern-advisor.md` — Instructions for a dedicated pattern-recommendation sub-pass

---

## Core Principles (always in context)

**Refactoring** is the controllable process of systematically improving code *without writing new functionality*. The goal is to pay off technical debt. The mantra is clean code and simple design.

**Clean code** is:
- Obvious to other programmers (good names, small units)
- Free of duplication
- Minimal in the number of moving parts
- Passing all tests
- Easier and cheaper to maintain

**How to refactor safely:**
1. Make sure tests exist before starting — if they don't, write them first
2. Work in small steps; run tests after every change
3. Never mix refactoring with new feature development in the same commit
4. The code must be cleaner after than before — if it isn't, you've wasted time

**When to refactor:**
- Rule of Three: first time — just do it; second time — note it; third time — refactor
- When adding a feature: clean the surrounding code first so the new code lands cleanly
- When fixing a bug: cleaning reveals errors
- During code review: last chance before the code is public

---

## Workflow for a Review/Refactor Session

### Step 1 — Understand the code

Read the code without judging it first. Understand what it is supposed to do. Ask the user if anything is unclear about the domain or intent.

### Step 2 — Detect smells

Work through the six smell categories in order (see `references/code-smells.md` for details):

1. **Bloaters** — things that have grown too large (Long Method, Large Class, Primitive Obsession, Long Parameter List, Data Clumps)
2. **Object-Orientation Abusers** — OO used incorrectly (Switch Statements, Temporary Field, Refused Bequest, Alternative Classes with Different Interfaces)
3. **Change Preventers** — code that makes change costly (Divergent Change, Shotgun Surgery, Parallel Inheritance Hierarchies)
4. **Dispensables** — code that adds no value (Comments, Duplicate Code, Lazy Class, Data Class, Dead Code, Speculative Generality)
5. **Couplers** — excessive coupling between classes (Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man)
6. **Other Smells** — Incomplete Library Class

For automated detection on Python files, run: `python scripts/analyze.py <file>`

### Step 3 — Prioritize

Not every smell needs fixing right now. Rank by:
- **Impact on changeability**: change preventers and couplers first
- **Risk of introducing bugs**: smaller, safer refactorings before large structural changes
- **Scope of the current task**: only refactor code you are already touching, unless a dedicated refactoring session is requested

### Step 4 — Select techniques

For each prioritized smell, choose the correct refactoring technique (see `references/refactoring-techniques.md`). Each technique has:
- **Problem** — what situation calls for it
- **Steps** — mechanical, safe transformations
- **Trade-offs** — when not to apply it

### Step 5 — Consider target patterns

After applying techniques, check whether the resulting structure matches a known design pattern (see `references/design-patterns.md`). If a pattern fits, move toward it deliberately — patterns are the catalog of shapes worth moving toward.

### Step 6 — Deliver the result

Use `templates/review-report.md` to structure the output. For planned multi-session work, fill in `templates/refactoring-plan.md`.

---

## Key Judgement Calls

**Don't refactor everything.** A refactoring that does not earn its keep is just rearranged code. A pattern that solves no real problem is complexity in a fancy hat.

**Smell → technique mapping is not 1:1.** Most smells have multiple applicable techniques; choose based on context. Techniques also cross-reference each other — you will rarely apply just one.

**Tests are non-negotiable.** If existing tests break after refactoring, either you made an error or the tests were testing implementation details (and need to be refactored too, ideally to BDD-style).

**Separate refactoring from new features.** At minimum, separate them into different commits. Mixing them makes it impossible to know which change broke what.
