# Refactoring Plan

> Fill in one section per refactoring session. Keep this document in the repository alongside the code.

---

## Context

| Field | Value |
|-------|-------|
| **File(s) / Module(s)** | <!-- e.g. src/billing/invoice.py --> |
| **Date started** | |
| **Author** | |
| **Motivation** | <!-- Why is this refactoring needed? Bug-fix prep, new feature, code review finding, scheduled debt payoff? --> |
| **Related issue / ticket** | |

---

## Pre-Conditions

- [ ] The code's intended behavior is understood
- [ ] Existing tests have been run and pass
- [ ] Test coverage is adequate (or tests have been written for the affected code)
- [ ] The scope of this refactoring is defined and bounded (not open-ended cleanup)

---

## Smells Identified

List each smell you are addressing. Copy from `assets/smell-checklist.md` as needed.

| # | Smell | Location (file:line) | Severity | Notes |
|---|-------|----------------------|----------|-------|
| 1 | | | High / Medium / Low | |
| 2 | | | | |
| 3 | | | | |

---

## Refactoring Steps

Break the work into small, independently safe steps. Each step should leave the code in a working state and all tests passing.

| Step | Technique | Target (class/method/field) | Tests to run | Status |
|------|-----------|----------------------------|--------------|--------|
| 1 | Extract Method | `ClassName.longMethod()` | unit/test_billing.py | [ ] |
| 2 | Rename Method | `ClassName.doIt()` → `ClassName.calculateTotal()` | | [ ] |
| 3 | | | | [ ] |
| 4 | | | | [ ] |
| 5 | | | | [ ] |

---

## Target Design

Describe the intended design after all steps are complete.

```
<!-- Sketch the class structure, sequence diagram, or pseudo-code of the target -->
```

If a design pattern is the target, name it here:

**Target Pattern:** <!-- e.g. Strategy, Extract Class → Observer -->

**Why this pattern fits:** <!-- explain the reasoning -->

---

## Trade-offs Accepted

List any trade-offs this refactoring deliberately accepts (e.g., increased method count, temporary code duplication during transition, performance implications).

- 
- 

---

## Post-Conditions

- [ ] All steps completed
- [ ] All tests pass (including any new tests written)
- [ ] Code is reviewed by a second developer
- [ ] Documentation updated (if public API changed)
- [ ] Commits are clean (refactoring commits are separate from feature commits)

---

## Retrospective Notes

What went well? What was harder than expected? What would you do differently?

<!-- Fill in after completion -->
