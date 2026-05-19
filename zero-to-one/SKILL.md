---
name: zero-to-one
description: Generate bold, original startup ideas grounded in Peter Thiel's Zero to One framework. Use this skill whenever the user wants to brainstorm new business concepts, explore startup opportunities, find underserved markets, stress-test an idea against monopoly thinking, or answer the contrarian question "what valuable company is nobody building?" Trigger even when the user mentions entrepreneurship, new ventures, business ideas, market gaps, innovation, side projects, or asks what to build next — this skill goes far beyond generic brainstorming by applying first-principles thinking to find genuinely 0-to-1 opportunities.
author: vprindyn@gmail.com
version: "1.0"
---

# Zero to One: Startup Idea Generator

This skill helps you generate startup ideas the way Peter Thiel teaches in *Zero to One* — not by copying what works, but by finding the secrets, contrarian truths, and unexploited monopoly niches that most people overlook.

## Core mental model

Going from **0 to 1** means creating something genuinely new — vertical progress, a new category, a new kind of value. Going from **1 to n** means copying what already exists. Only 0-to-1 companies can become truly great businesses, because copying earns thin margins in crowded markets while originality earns monopoly profits.

The central question to ask at every stage: **"What valuable company is nobody building?"**

## How this skill works

Run through these stages in order. You can stop early if the user already has an idea and just wants criticism or iteration.

### Stage 1 — Surface the contrarian insight

Start by asking the user (or reasoning through it yourself if enough context is available):

> "What important truth do very few people agree with you on?"

A good contrarian insight takes the form: *"Most people believe X, but the truth is the opposite of X."* Shallow answers ("our educational system is broken") don't count because many people already agree. The insight must be genuinely unpopular — something that makes people uncomfortable or dismissive when they hear it.

If the user cannot articulate one, help them find it by probing:
- What frustrates them daily that others seem to accept as normal?
- What do experts in a field get systematically wrong?
- What trend is real but being applied to the wrong problem?
- What is considered "settled" that is actually still wide open?

The startup idea should flow naturally from this insight. If it doesn't surprise anyone, keep digging.

### Stage 2 — Generate ideas using secrets

Thiel's definition of a secret: *a truth that exists but hasn't been widely discovered*. Most great startups are built on secrets about nature (how things work) or secrets about people (what people want but won't say). Ask:

- What does this person know that most people don't?
- What do customers want that no existing product gives them?
- What inefficiency or friction is so normalized that no one's questioning it?
- What would happen if you applied a technology from one domain to an entirely different one?

Generate at least **3–5 distinct ideas** before narrowing. Cast wide, then filter with the monopoly test below.

See `references/idea-generation-framework.md` for structured prompts and example secrets across domains.

### Stage 3 — Apply the monopoly test

Every idea must be evaluated against these four monopoly characteristics. A great startup idea should have a plausible path to at least two or three of these:

1. **Proprietary technology** — Is there a core capability that would be 10× better than anything available? Not marginally better — an order of magnitude better. The clearest path: invent something entirely new, or radically improve an existing solution (as PayPal made eBay payments 10× faster, Amazon offered 10× more book selection).

2. **Network effects** — Does the product get more valuable as more people use it? If yes, can it start with a tiny initial market where network effects kick in immediately (not requiring the whole world to join at once)?

3. **Economies of scale** — Does the unit cost fall dramatically as the business scales? Software businesses have nearly zero marginal cost per additional user. Service businesses often don't scale this way.

4. **Branding** — Is there a coherent identity that could make competitors feel like generic substitutes? Branding alone never works — it must sit on top of real substance.

Reject ideas that are **purely competitive**: if the product is only incrementally better and the market is large and crowded, the business will never escape thin margins.

See `references/market-analysis.md` for the full monopoly evaluation checklist.

### Stage 4 — Choose the starting market

Even the best idea fails with the wrong launch market. The launch market should be:

- **Small and specific** — A startup can dominate it in 1–3 years
- **Underserved or ignored** — Large incumbents aren't paying serious attention to it
- **A natural beachhead** — The path from this niche to adjacent, bigger markets is clear

Red flags: "We're going after 1% of a $100B market" (too diffuse, no beachhead); "We're disrupting [giant industry]" (framing suggests fighting, not creating).

The goal is to be the **last mover** — not first, but the one who makes the final great leap in a niche and then expands from that unassailable position.

### Stage 5 — Output format

For each idea (or the one idea being developed), produce:

```
## [Idea Name]

**The secret:** [The contrarian truth or hidden insight this is built on]

**What it does:** [One sentence description of the product or service]

**Starting market:** [The specific, small market to dominate first]

**Path to monopoly:** [Which of the four characteristics apply and how]

**Why now:** [What has changed that makes this possible today but not five years ago]

**The risk:** [The most honest critique — what would have to be true for this to fail]
```

If the user wants to explore further, invoke the agents in `agents/` as needed.

## When to use the specialized agents

- To rigorously critique an idea against Thiel's 7 questions → `agents/idea-critic.md`
- To systematically scout sectors for hidden opportunities → `agents/market-scout.md`

## Important principles to apply throughout

- **Don't disrupt** — Framing around "disrupting" an existing industry is a red flag. It means the company defines itself through its enemies. The goal is to create something new, not fight an existing category.
- **Definite optimism** — Vague optimism ("AI will change everything") is not a startup idea. A good idea is concrete enough to have a specific plan.
- **Bold is better than timid** — A bad plan is better than no plan. Incrementalism leads to local maxima. Aim for the global maximum even if you have to revise the path.
- **Sales matter as much as product** — An idea without a distribution strategy is incomplete.
