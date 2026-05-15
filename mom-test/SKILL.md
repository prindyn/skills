---
name: mom-test
description: Validates a new feature idea before writing any code using The Mom Test methodology. Use this skill whenever a user wants to test, validate, or de-risk a product or feature idea with real customers, conduct customer discovery interviews, evaluate whether an idea is worth building, or turn vague interest into concrete evidence. Triggers on phrases like "I want to validate my idea", "should I build this", "is this worth building", "how do I talk to customers", "customer discovery", "feature validation", "pre-build research", or any request to avoid building the wrong thing.
author: vprindyn@gmail.com
version: "1.0.0"
---

# Mom Test — Feature Validation Skill

Validate a feature idea through customer conversations before writing a single line of code. Based on Rob Fitzpatrick's *The Mom Test*.

## The Core Problem This Skill Solves

Most product teams build the wrong thing because they get false signals: customers say "yes, great idea!" to be polite, then never use it. This skill teaches you to have conversations that surface *truth* instead of *approval*.

## Quick Reference: The Three Rules

1. **Talk about their life, not your idea.** Never pitch during a discovery conversation.
2. **Ask about specifics in the past, not hypotheticals about the future.** "Have you ever…" beats "Would you…"
3. **Talk less, listen more.** Your job is to pull signal, not to persuade.

See `references/mom-test-rules.md` for the full methodology.

## How to Use This Skill

### Step 1 — Prep

Fill out `templates/feature-validation-brief.md` to clarify your hypothesis, your riskiest assumptions, and the customer segment you'll talk to. Use `references/customer-segmentation.md` to narrow to a specific, reachable slice of people.

### Step 2 — Prepare Your Questions

Draft 5–8 questions using `templates/interview-script.md`. Before any conversation, run your question list through the **question-critic** agent (`agents/question-critic.md`) to strip out leading and compliment-fishing questions.

### Step 3 — Find Conversations

Talk to people in the specific segment you defined. Warm intros beat cold outreach. Coffee-shop intercepts, Slack communities, and existing users all work. Aim for 5 conversations minimum before drawing conclusions.

### Step 4 — Conduct the Interview

Use `templates/interview-notes.md` during the call to capture verbatim quotes and flag signal types in real time. Keep the conversation casual — you're curious, not selling. Read `references/red-flags-cheatsheet.md` before your first call.

### Step 5 — Review and Classify

After each conversation, use the **signal-classifier** agent (`agents/signal-classifier.md`) to label each piece of data: Fact, Fluff, or Commitment. Discard fluff. Weight facts and commitments.

### Step 6 — Share Findings

After 5+ conversations, fill out `templates/findings-summary.md` and run it through the **validation-report** agent (`agents/validation-report.md`) to get a build / pause / pivot recommendation with evidence.

## Reference Files

| File | What it covers |
|---|---|
| `references/mom-test-rules.md` | Full methodology: the three rules, why they work |
| `references/good-vs-bad-questions.md` | Side-by-side examples of questions to ask and avoid |
| `references/commitment-signals.md` | What counts as real commitment vs. vague interest |
| `references/customer-segmentation.md` | How to narrow to a specific, reachable customer slice |
| `references/red-flags-cheatsheet.md` | Bad data patterns to catch in real time |

## Agent Files

| File | When to invoke |
|---|---|
| `agents/question-critic.md` | Before any interview — critique and rewrite your question list |
| `agents/interview-coach.md` | During or after a call — identify missed follow-up opportunities |
| `agents/signal-classifier.md` | After a call — label each piece of data (Fact / Fluff / Commitment) |
| `agents/validation-report.md` | After 5+ calls — synthesize into a build/pause/pivot recommendation |

## What Good Looks Like

By the end of this process you should have:
- 3–5 verbatim quotes describing a real, recurring problem (not your solution)
- Evidence of past behavior: workarounds people already use, money/time already spent
- At least one concrete commitment signal (time, money, intro, or reputation on the line)
- A clear decision: **build**, **pause and reframe**, or **pivot**

If you only have compliments and hypothetical interest, you don't have validation yet. Keep talking to people.
