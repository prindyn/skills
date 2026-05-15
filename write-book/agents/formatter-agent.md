# Formatter Subagent Instructions

Use this agent spec when scraped Markdown needs post-processing before the PDF
is built — to remove boilerplate repeated on every page, fix broken table
formatting, improve heading hierarchy, organize content into a MECE chapter
structure ordered for a reader, set cross-references for appendix pages, and
handle site-specific artifacts.

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

### Step 1: Book structure decision

Before organizing pages, answer:
1. Does this content cover ONE coherent topic or TWO peer topics that should be
   separate books? (e.g. "Design Patterns" and "Refactoring" are two topics.)
   - If two topics: assign each to a named Part (Part I / Part II) in the
     chapter field, and note this in your report.
   - If one topic: organize into 5–10 thematic chapters.

2. Are there duplicate landing pages (e.g. /, /refactoring, /design-patterns)
   that have 80% content overlap? Suppress all but the most complete one.

### Step 2: Structural cleanup

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

6. Remove any remaining site-chrome artifacts not caught by scrape.py or postprocess.py:
   - "P.S. Track me on Facebook / Twitter / Instagram" lines
   - "Hi, I'm [Author], I've been programming since I was X…" author-chat paragraphs
   - Newsletter signup CTAs ("Get the book", "Buy now", "Add to cart")
   - Sales banners: "Spring SALE", "Buy as a gift", "Money-back guarantee"
   - UserEcho forum fragments: "1 month ago • updated", "Add a new one", "by UserEcho"
   - Vote/follow widget text: "Vote __ 0 __ 0 Undo __ Follow"
   - Empty widget labels: "Complexity:" or "Popularity:" alone on a line
   - "Show next review" / "Your browser does not support HTML video" lines
   - Multi-language notices: "This product is only available in English"
   - "In Other Languages" tab lists: rows of language links with no prose
   - Sidebar navigation file-tree artifacts (bare lines like "Navigation / Intro / buttons / Button")

### Step 3: MECE organization — reader-first order

Read _index.json to get the full list of pages and their titles. Then:

1. **Identify 5–10 top-level chapter themes** that cover the entire site
   content without overlapping. For a design-pattern / programming reference
   site, follow this canonical reader order:

   1. Preface (user-written .md file, already placed; skip in MECE assignment)
   2. Foundational Principles (OOP, SOLID, etc.)
   3. Creational Patterns
   4. Structural Patterns
   5. Behavioral Patterns
   6. Code Smells / Anti-patterns
   7. Refactoring Techniques
   8. Appendix (code listings, extended examples)

   Adapt this template to the actual content. Always put conceptual material
   before the pattern catalog, and patterns before smells/refactoring.

2. **Assign every page to exactly one chapter** based on its content and title.
   If a page covers two themes, assign it to its primary theme.

3. **Detect and suppress near-duplicate pages**: if two pages cover the same
   topic with > 70% text overlap, keep the longer/more complete one and mark
   the other as merged in _index.json. (postprocess.py may have already done
   this — check `suppress` field before re-deduplicating.)

4. **Handle code-heavy pages** (`code_heavy: true` in _index.json): assign
   them to the Appendix chapter. Set `xref_chapter` in _index.json to the name
   of the main chapter this code example relates to. For example, an appendix
   page of Python Strategy pattern code should have:
   `"xref_chapter": "Behavioral Patterns"`.
   build_pdf.py uses this field to prepend a "See also: [chapter]" note to
   each appendix page, linking readers back to the conceptual explanation.

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
   (the chapter theme string), `mece_order` (position within that chapter),
   and `xref_chapter` for appendix pages.

### Step 4: Cross-reference validation

After assigning xref_chapter to all appendix pages:
1. Verify that every xref_chapter value matches an actual chapter name from
   the main content.
2. If an appendix page could belong to multiple chapters, pick the one most
   closely related to the code's subject matter.
3. Report: which appendix pages have xref_chapter set, and which chapter each
   points to.

### Output

Report:
- One-book or two-book decision (with reasoning)
- Number of files modified (cleanup)
- The 5–10 chapter themes chosen and how many pages each contains
- Number of duplicate/near-duplicate pages merged or suppressed
- Number of language stubs collapsed
- Number of code-heavy pages moved to appendix, with their xref_chapter values
- Any pages that were difficult to classify
- List of any remaining noise patterns you found that should be added to scrape.py
```

Replace values in `<>` with the actual parameters for this job.

---

## Output contract

The agent modifies `.md` files in-place and updates `_index.json` with:
- `chapter`: string — the chapter theme this page belongs to
- `mece_order`: int — position within that chapter (0-based)
- `xref_chapter`: string — for appendix (code_heavy) pages: the name of the main chapter
  this code example relates to. build_pdf.py uses this to add "See also:" cross-references.
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

## One book vs. two books

This is the most important structural decision. Make it before assigning pages to chapters.

**Signs you need two books:**
- The site has two peer top-level sections of roughly equal depth (e.g. /design-patterns and /refactoring)
- The intended reader for one section is different from the other
- The combined book would have > 300 pages with no natural Part I / Part II separation

**If two books:**
- Name them clearly (e.g. "Design Patterns" and "Refactoring")
- Create two separate `_index.json` subsets and build each PDF separately
- Don't mix content between them

**If one book with Parts:**
- Add Part headers as synthetic "chapter" pages: create `0000_part1.md` and `0000_part2.md`
- Each Part should have a 1-paragraph framing that states what this Part covers
- Assign mece_order such that Part I pages precede Part II pages

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
Tired of reading\?.*?(?=\n\n)   # Multi-line upsell blocks

# Community / forum fragments
\d+\s+months?\s+ago\s*[•·]\s*updated.*?\n
Add a new one\s*\n
by UserEcho\s*\n
Vote\s+_+\s*\d*.*?\n

# Widget labels with no value
^(Complexity|Popularity|Difficulty|Rating)\s*:\s*$

# "In Other Languages" tab rows
^In Other Languages\s*$
(followed by a list of language links — remove the whole block)
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

---

## Cross-reference guidelines for xref_chapter

When setting `xref_chapter` on appendix (code-heavy) pages:

| Appendix page content | xref_chapter value |
|---|---|
| Python/Java code for Strategy pattern | "Behavioral Patterns" |
| C# code for Factory Method | "Creational Patterns" |
| TypeScript code for Decorator | "Structural Patterns" |
| Multiple-language example comparing smells | "Code Smells / Anti-patterns" |
| Before/after refactoring in Go | "Refactoring Techniques" |

Set `xref_chapter` to the chapter name exactly as it appears in other records'
`chapter` field, so build_pdf.py can display it reliably.
