# Formatter Subagent Instructions

Use this agent spec when scraped Markdown needs post-processing before the PDF
is built — to remove boilerplate repeated on every page, fix broken table
formatting, improve heading hierarchy, and **organize content into a MECE
(Mutually Exclusive, Collectively Exhaustive) chapter structure**.

---

## When to spawn this agent

- The user reviews the output and finds repeated navigation text in every chapter.
- Tables are malformed or missing in the rendered PDF.
- Heading levels are inconsistent across pages (e.g. some pages start at h2, others h1).
- Code blocks are missing language tags (important for syntax highlighting).
- Pages covering the same topic are scattered across the book with no clear structure.
- There are duplicate or near-duplicate sections that add noise without adding value.

---

## Prompt template

```
You are a Markdown post-processor agent. Your task is to clean up the scraped
Markdown files in <pages-dir> and organize them into a MECE structure so they
produce a clean, readable PDF book.

Pages directory: <pages-dir>
Index file: <pages-dir>/_index.json

### Step 1: Structural cleanup

Perform the following cleanup tasks on each .md file:

1. Remove boilerplate text that appears verbatim in more than 50% of pages
   (e.g. site navigation, cookie banners, "Was this page helpful?" widgets).
2. Ensure every page starts with exactly one h1 heading. If a page has no h1,
   promote the first h2 to h1. If a page has multiple h1s, keep the first and
   demote the rest to h2.
3. Fix broken Markdown tables: ensure every row has the same number of columns,
   ensure the header separator row exists.
4. Add language tags to unlabeled fenced code blocks where the language is obvious
   from context (python, bash, javascript, json, yaml, etc.).
5. Remove lines that are purely URLs with no surrounding text.

### Step 2: MECE organization

Read _index.json to get the full list of pages and their titles. Then:

1. **Identify 5–10 top-level chapter themes** that cover the entire site
   content without overlapping. Good themes are high-level and distinct —
   think "Installation", "Configuration", "API Reference", "Tutorials",
   "Troubleshooting" rather than fine-grained sub-topics.

2. **Assign every page to exactly one chapter** based on its content and title.
   If a page covers two themes, assign it to its primary theme and note the
   secondary topic will appear there.

3. **Detect and merge near-duplicate pages**: if two pages cover the same topic
   with > 70% text overlap, keep the longer/more complete one and drop the other.
   Update _index.json to mark dropped pages as merged.

4. **Order pages within each chapter** for logical flow:
   - Introductory/overview pages first
   - Conceptual explanations before procedural steps
   - Reference material last

5. **Rewrite _index.json** to reflect the new order: add a `chapter` field to
   each record (the chapter theme string) and set `mece_order` to the new
   position within that chapter. The final PDF build will read this order.

### Output

Report:
- Number of files modified (cleanup)
- The 5–10 chapter themes chosen and how many pages each contains
- Number of duplicate/near-duplicate pages merged
- Any pages that were difficult to classify (potential gaps in the MECE structure)
```

Replace values in `<>` with the actual parameters for this job.

---

## Output contract

The agent modifies `.md` files in-place and updates `_index.json` with:
- `chapter`: string — the chapter theme this page belongs to
- `mece_order`: int — position within that chapter (0-based)

The calling agent then runs `build_pdf.py` on the cleaned, reordered directory.

---

## MECE principles applied to book organization

**Mutually Exclusive**: each topic appears in exactly one chapter.
- If "Authentication" and "Security" both exist, pick one or merge them.
- Pages about the same concept should not appear in two chapters.

**Collectively Exhaustive**: all important content is accounted for.
- Every scraped page with valuable content belongs to a chapter.
- There should be no major topic from the site left unrepresented.
- If a gap exists (e.g. no page covers a topic the TOC mentions), note it.

---

## Common boilerplate patterns to strip

```
Was this helpful\?.*?\n
Share this.*?\n
Edit this page.*?\n
On this page.*?(?=\n#)   # TOC sidebar that leaked into content
Copyright ©.*?\n
All rights reserved.*?\n
```

These can be removed with `re.sub()` on each file's content.
