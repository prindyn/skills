# Formatter Subagent Instructions

Use this agent spec when scraped Markdown needs post-processing before the PDF
is built — to remove boilerplate repeated on every page, fix broken table
formatting, improve heading hierarchy, organize content into a MECE chapter
structure ordered for a reader, and handle site-specific artifacts.

---

## When to spawn this agent

- The user reviews the output and finds repeated navigation text in every chapter.
- Tables are malformed or missing in the rendered PDF.
- Heading levels are inconsistent across pages (e.g. some pages start at h2, others h1).
- Code blocks are missing language tags (important for syntax highlighting).
- Pages covering the same topic are scattered across the book with no clear structure.
- There are duplicate or near-duplicate sections that add noise without adding value.
- The book reads in site-crawl order rather than logical reading order.
- Code-heavy pages (tagged `code_heavy: true` in `_index.json`) need to be grouped as an appendix.

---

## Prompt template

```
You are a Markdown post-processor agent. Your task is to clean up the scraped
Markdown files in <pages-dir> and organize them into a MECE structure so they
produce a clean, readable PDF book ordered for a human reader.

Pages directory: <pages-dir>
Index file: <pages-dir>/_index.json

### Step 1: Structural cleanup

Perform the following cleanup tasks on each .md file:

1. Remove boilerplate text that appears verbatim in more than 50% of pages
   (e.g. site navigation, cookie banners, "Was this page helpful?" widgets).
   
2. Ensure every page starts with exactly one h1 heading. If a page has no h1,
   promote the first h2 to h1. If a page has multiple h1s, keep the first and
   demote the rest to h2. (The leading H1 was already deduplicated by scrape.py,
   but verify no double-titles slipped through.)

3. Fix broken Markdown tables: ensure every row has the same number of columns,
   ensure the header separator row exists.

4. Add language tags to unlabeled fenced code blocks where the language is obvious
   from context (python, bash, javascript, json, yaml, etc.).

5. Remove lines that are purely URLs with no surrounding text.

6. Remove any remaining site-chrome artifacts not caught by scrape.py:
   - "P.S. Track me on Facebook / Twitter / Instagram" lines
   - "Hi, I'm [Author], I've been programming since I was X…" author-chat paragraphs
   - Newsletter signup CTAs ("Get the book", "Buy now", "Add to cart")
   - Refactoring.guru-style: "Spring SALE", "Buy as a gift", "Money-back guarantee"
   - UserEcho forum fragments: "1 month ago • updated", "Add a new one", "by UserEcho"
   - Vote/follow widget text: "Vote __ 0 __ 0 Undo __ Follow"
   - Empty widget labels: "Complexity:" or "Popularity:" alone on a line
   - "Show next review" / "Your browser does not support HTML video" lines
   - Multi-language notices: "This product is only available in English"
   - Sidebar navigation file-tree artifacts (bare lines like "Navigation / Intro / buttons / Button")

### Step 2: MECE organization — reader-first order

Read _index.json to get the full list of pages and their titles. Then:

1. **Identify 5–10 top-level chapter themes** that cover the entire site
   content without overlapping. For a design-pattern / programming reference
   site, follow this canonical reader order:
   
   1. Preface / Introduction  
   2. Foundational Principles (OOP, SOLID, etc.)  
   3. Creational Patterns  
   4. Structural Patterns  
   5. Behavioral Patterns  
   6. Code Smells / Anti-patterns  
   7. Refactoring Techniques  
   8. Appendix (code listings, extended examples)

   Adapt this template to the actual content, but always order conceptual
   material before patterns, and patterns before smells/refactoring.

2. **Assign every page to exactly one chapter** based on its content and title.
   If a page covers two themes, assign it to its primary theme.

3. **Detect and suppress near-duplicate pages**: if two pages cover the same
   topic with > 70% text overlap, keep the longer/more complete one and mark
   the other as merged in _index.json. (postprocess.py may have already done
   this — check `suppress` field before re-deduplicating.)

4. **Handle code-heavy pages** (`code_heavy: true` in _index.json): assign
   them to the Appendix chapter rather than the main narrative. They are
   already tagged; just set their chapter accordingly.

5. **Collapse per-language stubs**: if multiple pages differ only in a language
   suffix (e.g. /design-patterns/swift, /design-patterns/java) and contain
   the same list of pattern links with no unique prose, suppress all but one
   and add a note like "Also available for: Swift, Java, PHP…" to the keeper.
   (postprocess.py --collapse-language-stubs may have already handled this.)

6. **Deduplicate catalog overview pages**: if "Code Smells Overview" appears
   2–3 times with identical or near-identical content, keep one.

7. **Order pages within each chapter** for logical flow:
   - Introductory/overview pages first
   - Conceptual explanations before procedural steps
   - Reference/catalog pages after conceptual ones
   - Extended code listings last (or in appendix)

8. **Rewrite _index.json** to reflect the new order: add a `chapter` field
   (the chapter theme string) and set `mece_order` to the new position
   within that chapter. The PDF build reads this order.

### Output

Report:
- Number of files modified (cleanup)
- The 5–10 chapter themes chosen and how many pages each contains
- Number of duplicate/near-duplicate pages merged or suppressed
- Number of language stubs collapsed
- Number of code-heavy pages moved to appendix
- Any pages that were difficult to classify
```

Replace values in `<>` with the actual parameters for this job.

---

## Output contract

The agent modifies `.md` files in-place and updates `_index.json` with:
- `chapter`: string — the chapter theme this page belongs to
- `mece_order`: int — position within that chapter (0-based)
- `suppress`: true — for any pages identified as duplicates or stubs

The calling agent then runs `build_pdf.py` on the cleaned, reordered directory.

---

## MECE principles applied to book organization

**Mutually Exclusive**: each topic appears in exactly one chapter.
- If "Authentication" and "Security" both exist, pick one or merge them.
- Catalog overview pages that appear 2–3 times should be merged to one.

**Collectively Exhaustive**: all important content is accounted for.
- Every active page belongs to a chapter.
- No major topic from the site is left unrepresented.

---

## Common boilerplate patterns to strip

```regex
# Basic site chrome
Was this helpful\?.*?\n
Share this.*?\n
Edit this page.*?\n
On this page.*?(?=\n#)   # TOC sidebar that leaked into content
Copyright ©.*?\n
All rights reserved.*?\n

# Author chat / social promo
P\.S\. Track me on (Facebook|Twitter|Instagram|social media).*?\n
Hi,?\s+I'?m [A-Z][a-z]+,?\s+(I'?ve been|I'?m a).*?\n
(Follow|Join) me on.*?\n

# E-commerce / sales
Spring SALE.*?\n
(Buy|Purchase) (now|as a gift).*?\n
Money-back guarantee.*?\n
(Add to cart|Checkout|Purchase).*?\n
Can I buy (on Amazon|this book).*?\n
How is this better than ChatGPT.*?\n

# Community / forum fragments
\d+\s+months?\s+ago\s*[•·]\s*updated.*?\n
Add a new one\s*\n
by UserEcho\s*\n
Vote\s+_+\s*\d*.*?\n

# Widget labels with no value
^(Complexity|Popularity|Difficulty|Rating)\s*:\s*$
```

Apply these with `re.sub()` on each file's content, then collapse 3+ blank lines to 2.

---

## Reader-first vs. crawler-first ordering

Site crawlers follow link order; books follow comprehension order. When reordering:
- Always put "what is X?" before "how to apply X"
- Always put foundational concepts before the pattern catalog
- Always put the catalog before code smells and refactoring techniques
- Group language-specific examples in an appendix or note them inline
- Do not scatter the same concept across multiple non-adjacent chapters
