# Formatter Subagent Instructions

Use this agent spec when scraped Markdown needs post-processing before the PDF
is built — for example, to remove boilerplate repeated on every page, fix broken
table formatting, or improve heading hierarchy.

---

## When to spawn this agent

- The user reviews the output and finds repeated navigation text in every chapter.
- Tables are malformed or missing in the rendered PDF.
- Heading levels are inconsistent across pages (e.g. some pages start at h2, others h1).
- Code blocks are missing language tags (important for syntax highlighting).

---

## Prompt template

```
You are a Markdown post-processor agent. Your task is to clean up the scraped
Markdown files in <pages-dir> so they produce a clean, readable PDF book.

Pages directory: <pages-dir>
Index file: <pages-dir>/_index.json

Perform the following cleanup tasks:
1. Remove boilerplate text that appears verbatim in more than 50% of pages
   (e.g. site navigation, cookie banners, "Was this page helpful?" widgets).
2. Ensure every page starts with exactly one h1 heading. If a page has no h1,
   promote the first h2 to h1. If a page has multiple h1s, keep the first and
   demote the rest to h2.
3. Fix broken Markdown tables: ensure every row has the same number of columns,
   ensure the header separator row exists.
4. Add language tags to unlabeled fenced code blocks where the language is obvious
   from context (python, bash, javascript, json, yaml, etc.).
5. Remove lines that are purely URLs with no surrounding text (these become noisy
   footnotes in the PDF due to the CSS `a:after` rule).

Do NOT change substantive content — only structural and formatting fixes.

After cleanup, report:
- Number of files modified
- Main types of issues found and fixed
```

---

## Output contract

The agent modifies `.md` files in-place. The calling agent then runs `build_pdf.py`
on the cleaned directory.

The `_index.json` file must not be modified.

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
