# Book Writing Guide

Principles for producing a book that reads as if written by a knowledgeable author —
not assembled by a script. Adapted from the craft of professional non-fiction and
narrative writing.

The goal is a book a reader picks up and cannot tell was generated from a website.
Every principle here serves that goal.

---

## 1. Start with a winning concept

Before crawling, ask: is this website's content worth a book?

A good book concept:
- Has a clear, specific scope that can be stated in one sentence
- Has an audience that is identifiable and coherent
- Has content rich enough to warrant the format (not just 5 pages of docs)
- Has a natural reading arc — a beginning, a middle, a resolution

If the website is a sprawling marketing site with 10% real content, the book will
reflect that. Curate the scope before you crawl. Better a tight 80-page book than
a bloated 300-page one full of landing pages and CTAs.

---

## 2. Know your reader before you write

The single most important question in writing is: who is this for?

Determine the reader before making any structural decision:
- What does the reader already know? (Don't explain what they know; don't skip what they don't.)
- What does the reader want to accomplish? (Shape the arc around that outcome.)
- How will the reader use this book? (Cover-to-cover? Reference lookup? Quick scan?)

The Preface states this explicitly. Every chapter ordering decision, every example
chosen, every section included or excluded flows from knowing the reader.

---

## 3. Plan before you write

The best writers plan. Even "discovery writers" who improvise their first drafts have
an instinct for where they're going. For a book from a website, that instinct must
be supplied deliberately.

Before scraping:
- Identify the 5–10 top-level chapters
- Determine the reading order (not the crawl order — those are different)
- Identify which pages belong in the Appendix from the start
- Decide what to suppress outright

A well-planned book does not expose its plan to the reader. The chapter order feels
natural, as if it could not be otherwise. That naturalness requires planning.

Fill out `templates/book-plan.md` before starting any crawl.

---

## 4. Begin strong — grab the reader immediately

The first chapter sets the reader's expectation for everything that follows.

**Never open with:**
- A marketing landing page repurposed as Chapter 1
- A glossary
- A chapter titled "Overview" that summarizes what later chapters will say
- A meta-chapter that explains how the book is organized

**Open with:**
- The first concept the reader needs, explained compellingly
- A solved problem that demonstrates the book's value immediately
- The foundational idea that all other ideas depend on
- A concrete example that makes the reader want to know more

The craft principle: begin *in the middle of things*. Trust the reader to follow.
Give them a reason to keep reading before you explain what you're doing.

---

## 5. Build the middle with progressive depth

The middle is where most books fail. Content is present, but it's not ordered for
a reader — it's ordered for a sitemap.

Good middle ordering:
- Concept before application
- Simple before complex
- Abstract before concrete
- Foundational before catalog

Each chapter should feel like it earned its place by building on what came before.
A reader who skips chapters should feel they're missing something — not that the
chapters are interchangeable.

For programming/technical books: introduce the "why" before the "how". A pattern
explained before its motivation is memorized, not understood.

---

## 6. Use examples that illuminate, not examples that fill space

Examples are the most powerful tool in technical writing. They also produce the
most noise when scraped from websites.

Keep examples that:
- Demonstrate the concept at hand, not a tangent
- Show a complete, working unit (not a fragment)
- Progress in complexity as the chapter progresses (simple → realistic → edge case)

Suppress or move to Appendix:
- Examples that are identical across 10 languages (keep one; note the others exist)
- Examples that are 100% code with no surrounding explanation
- Examples that repeat a concept already covered in the main chapter

The goal is an example that makes the reader think "now I see it." An example
that takes 3 pages and shows what was already obvious is just filler.

---

## 7. Write the Preface as an author, not as a tool report

The Preface is the one piece of original writing in this book. It must sound like
a knowledgeable author wrote it for this specific reader.

**The Preface is NOT:**
- A description of how the book was made
- A list of what pages were included
- An explanation of the scraping process
- A meta-commentary on the PDF generation

**The Preface IS:**
- A direct address to the reader
- An honest account of who will benefit and who should probably read something else
- A statement of scope (what's covered, what's not)
- A recommendation on how to read the book (linear? reference? which chapters to skip?)
- An optional statement of the author's perspective or the book's central argument

Use `templates/preface.md` as a starting point. Read it aloud. If it sounds like
software documentation, rewrite it.

---

## 8. Engage the reader's mind — show, don't tell

A book that lists facts is an index. A book that builds understanding is a book.

The difference:
- **Telling:** "The Strategy pattern defines a family of algorithms."
- **Showing:** "Imagine you're writing a navigation app. You need to route by car, by foot, by bike. Naively, you write three `if/else` branches in your routing function. Six months later, the function is 400 lines long and adding a fourth route type means touching every branch. Strategy gives you a way out."

Show the reader what the concept solves before defining it. Give them the problem
before the solution. Make them feel the need before offering the answer.

This principle applies even to dry reference material. The best API documentation
opens with a realistic use case, not a parameter table.

---

## 9. Bring the book to a satisfying close

Most websites end with a sales page or a newsletter signup. Neither makes a good
final chapter.

The book's conclusion should:
- Synthesize what was covered (not summarize — there's a difference)
- Give the reader a sense of what they can now do that they couldn't before
- Point toward natural next steps without being a sales pitch
- Feel like a genuine ending, not a page that happens to come last

If the site has no good conclusion material, write a short one. Two paragraphs is
enough. The reader has invested time; honor that investment with a real ending.

---

## 10. Remove everything that doesn't serve the reader

When in doubt, cut it.

Content that does not serve the reader:
- Navigation text that leaked in from the site
- CTAs and sales language
- Author social promotion
- Legal boilerplate
- Pages that are just lists of links (usually category/tag pages)
- Duplicate content from multiple language variants
- Pages that say "please upgrade" or "buy the full version"

The reader opened this book to learn something. Everything that interrupts that
purpose should be removed. A tighter book is always better than a padded one.

---

## Summary: the author's checklist

Before delivering the PDF:

- [ ] The Preface reads like a knowledgeable author wrote it for this reader
- [ ] Chapter 1 opens with real content, not an overview or marketing page
- [ ] Each chapter follows logically from the one before
- [ ] Examples illuminate concepts rather than filling space
- [ ] No meta-commentary about scraping, crawling, or PDF generation appears anywhere
- [ ] The book ends with a genuine conclusion, not a sales page
- [ ] Everything that doesn't serve the reader has been removed
- [ ] Images (if included) are diagrams, figures, or screenshots — not decorative
- [ ] The index is curated: proper nouns and concept terms, not generic labels
