# Content Exclusion Patterns

Patterns for excluding non-book content from scraped websites. Apply these
to `crawl.py --exclude` (to avoid crawling entirely) and `scrape.py --exclude`
(to skip pages in the sitemap). Some patterns are also handled as HTML element
removal in the scraper.

---

## URL patterns by content type

### E-commerce and sales pages

```regex
/(sale|spring-sale|summer-sale|promo|discount|coupon)
/(pricing|price|price-list)
/(buy|buy-now|purchase|order|add-to-cart)
/(checkout|cart|basket)
/(gift|buy-as-a-gift|gift-card)
/(amazon|buy-on-amazon)
/(refund|money-back|guarantee|returns)
/(payment|payment-method|payment-options)
```

**Example** (combined for `--exclude`):
```
(sale|pricing|buy|checkout|gift|amazon|refund|payment|guarantee)
```

### Testimonials and reviews

```regex
/(testimonials?|reviews?|customer-stories|case-studies)
/(success-stories|what-people-say)
```

### Community and support forums

```regex
/(forum|community|userecho|discuss|discussions?)
/(vote|votes|voting)
/(support|help-desk|helpdesk)
```

### Author personal and social pages

```regex
/(about-me|about-us|team|author)
/(blog|personal|journal)
/(newsletter|subscribe|mailing-list|sendy)
/(social|facebook|twitter|instagram|youtube)
```

### FAQ and support documents

```regex
/(faq|frequently-asked|questions)
/(how-to-buy|how-to-pay|is-it-on-amazon)
/(languages|available-languages|translations)
```

### Authentication and accounts

```regex
/(login|logout|sign-?in|sign-?up|register|account|profile|dashboard)
```

### Navigation artifacts (search, tags, categories)

```regex
/search(\?|/)
/(tag|tags|category|categories|archive|author)/
\?page=
\?p=\d+
```

### Regional and language variants (keep only primary)

```regex
# Non-English language subpaths — remove if you want English only
/(zh|ja|ko|pl|de|fr|es|pt|ru|uk|ar|it|nl)/
```

---

## Combined exclude pattern examples

**Minimal exclude** (just e-commerce and auth):
```
(sale|pricing|buy|checkout|payment|login|register)
```

**Comprehensive exclude** for a programming reference site like refactoring.guru:
```
(sale|pricing|buy|checkout|gift|amazon|refund|payment|guarantee|testimonial|review|faq|forum|community|userecho|newsletter|subscribe|login|register|about-me|author|facebook|twitter)
```

**Language-filter** (English only, exclude CJK and Eastern European):
```
/(zh|ja|ko|pl|ru|uk|de|fr|es|pt)/
```

---

## HTML elements stripped by scrape.py

The following CSS selectors are stripped from page HTML before conversion,
in addition to standard navigation (`nav`, `header`, `footer`, `aside`):

### Community / forum widgets
```css
[class*="userecho"], [id*="userecho"], .ue-widget
[class*="forum"], [id*="forum"]
.community-widget
[class*="vote"], [id*="vote"]
[class*="follow"], [id*="follow"]
.like-button, .share-button, .social-share
```

### Testimonials / reviews
```css
.testimonials, .testimonial, .testimonials-section
.reviews, .review-section, .customer-reviews
[class*="testimonial"], [id*="testimonial"]
```

### E-commerce / pricing
```css
.pricing, .price-table, .pricing-table
.checkout, .buy-now, .purchase-section
.sale-banner, .promo-banner, .offer-banner
[class*="pricing"], [id*="pricing"]
```

### Author bios / social
```css
.author-bio, .author-info, .author-card
.social-links, .newsletter-signup
[class*="newsletter"]
```

### Multi-language sales banners
```css
.language-notice, .translation-notice
[class*="language-banner"], [class*="lang-notice"]
```

---

## Markdown-level patterns removed by scrape.py

Applied to the converted Markdown text as regex substitutions:

| Pattern | What it removes |
|---|---|
| `\[/?code\]` | BBCode `[code]`/`[/code]` tags |
| `\(/[a-z0-9_/-]+/form[^)]*\)` | Form link artifacts like `(/sendy/form)` |
| `Your browser does not support HTML video\.?` | Video fallback text |
| `^(Complexity\|Popularity)\s*:\s*$` | Empty widget labels |
| `Vote\s+_+\s*\d*.*?` | Vote widget text |
| `Show next review\s*` | Review pagination controls |
| `Add a new one\s*` | UserEcho "add" prompt |
| `by UserEcho\s*` | UserEcho footer branding |
| `\d+\s+months?\s+ago\s*[•·]\s*updated` | Forum timestamps |
| `This product is only available in English\.?` | Language sales notice |
| `^\s*https?://\S+\s*$` | URL-only lines |
| `\([a-z0-9.-]+\.[a-z]{2,}/[a-z0-9/_-]+\)` | URL slugs in parentheses |

---

## Patterns removed by formatter agent (manual or post-processing)

These require reading the full page context and are best handled by the
formatter agent or a human review:

| Pattern | Notes |
|---|---|
| "P.S. Track me on Facebook…" | Author-chat postscripts at end of pages |
| "Hi, I'm Alexander, I've been programming…" | Author biography paragraphs |
| "Get the book / Buy now / Add to cart" | Sales CTAs mixed into content |
| "Spring SALE", "Buy as a gift" | Promotional banners near top of page |
| "Can I buy on Amazon?" / "How is this better than ChatGPT?" | FAQ mixed into content |
| Sidebar navigation file-tree lines | Lines like "Navigation / Intro / buttons / Button / MacOSButton" |
| Per-language link lists (no prose) | 20+ links repeated across 9 language stubs |

---

## CJK font handling

If the site contains Chinese, Japanese, or Korean characters, install Noto CJK
fonts before running WeasyPrint:

```bash
# Debian / Ubuntu
apt-get install fonts-noto-cjk

# macOS
brew install --cask font-noto-sans-cjk-sc font-noto-serif-cjk-sc

# Alpine
apk add font-noto-cjk
```

The `book.css` includes a CJK font fallback stack (Noto Serif CJK, Source Han Serif,
PingFang SC, Microsoft YaHei, Hiragino Mincho Pro) that WeasyPrint will use once
these fonts are installed. Without them, CJK characters render as □ boxes.

If you want to **omit** CJK content entirely rather than fix font rendering, add
the relevant language paths to `--exclude`:
```
/(zh|ja|ko)/
```
