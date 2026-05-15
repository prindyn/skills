# Content Exclusion Patterns

Patterns for excluding non-book content from scraped websites. Apply these
to `crawl.py --exclude` (to avoid crawling entirely) and `scrape.py --exclude`
(to skip pages in the sitemap). Some patterns are also handled as HTML element
removal in the scraper.

**Always inspect the URL list after crawling** (before scraping) to catch pages
that slipped through. The default exclusions target e-commerce — always add
site-specific patterns for legal, account, and CTA noise.

---

## URL patterns by content type

### Legal / compliance pages

These must be excluded from every book — they contain no readable content
and are legally required disclaimers, not instructional material.

```regex
/(privacy|privacy-policy)
/(terms|terms-of-service|terms-of-use|tos)
/(legal|disclaimer|imprint)
/(gdpr|cookies|cookie-policy|cookie-notice)
```

**Example** (combined):
```
(privacy|terms|legal|gdpr|cookies|imprint|disclaimer)
```

### Account and authentication pages

```regex
/(login|logout|sign-?in|sign-?up|signup|register)
/(account|profile|dashboard|my-account)
/(cart|basket|wishlist)
```

**Example** (combined):
```
(login|logout|signup|register|account|cart|basket)
```

### About / personal pages

```regex
/(about|about-us|about-me)
/(team|contact|contact-us)
```

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

### Navigation artifacts (search, tags, categories)

```regex
/search(\?|/)
/(tag|tags|category|categories|archive|author)/
\?page=
\?p=\d+
```

### Regional and language variants (keep only primary)

```regex
# Non-English language subpaths — exclude if you want English only
/(zh|ja|ko|pl|de|fr|es|pt|ru|uk|ar|it|nl)/
```

---

## Comprehensive exclude pattern for a programming reference site

Combine legal, account, sales, community, and language noise into one pattern.
Use this for both `crawl.py --exclude` AND `scrape.py --exclude`:

```
(privacy|terms|legal|gdpr|cookies|imprint|about|sale|cart|signup|login|pricing|buy|checkout|gift|amazon|refund|payment|guarantee|testimonial|review|faq|forum|community|userecho|newsletter|subscribe|register|account|zh|ja|ko|pl|de|fr|es|pt|ru)
```

---

## URL inspection after crawling

After running `crawl.py`, inspect the URL list before scraping:

```bash
python -c "
import json
data = json.loads(open('crawl_output/sitemap.json').read())
for p in data['pages']:
    print(p['url'])
" | grep -iE "(privacy|terms|legal|gdpr|about|cookies|imprint|login|signup|sale|cart|faq|testimonial|review|forum|pricing|refund|guarantee|newsletter|subscribe|account|register)"
```

If this grep returns hits, add them to `--exclude` and re-crawl. Scraping
pages that will be discarded wastes time and introduces noise.

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

### CTA / upsell blocks
```css
.cta, .cta-block, .cta-section
[class*="cta-"], [id*="cta-"]
.upsell, [class*="upsell"], [id*="upsell"]
.buy-box, .purchase-box, .get-book
```

### "In Other Languages" navigation tabs
```css
.language-tabs, .lang-tabs
[class*="language-tab"], [class*="lang-tab"]
.in-other-languages, [class*="other-languages"]
.available-in, [class*="available-in"]
.translations-list, [class*="translation"]
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

### Legal / compliance notices
```css
.cookie-consent, .gdpr-notice, .privacy-notice
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
| `In Other Languages\s*` | "In Other Languages" tab headers |
| `Tired of reading\?.*` | CTA upsell opener |
| `(Get\|Download\|Buy) the (book\|course\|ebook)` | Book/course CTAs |
| `Spring SALE.*` | Seasonal sale banners |
| `Money-back guarantee.*` | Sales guarantee lines |
| `Was this (page\|article) helpful\?.*` | Feedback widget text |
| `Share this (page\|post\|article).*` | Social share prompts |
| `P\.S\. Track me on.*` | Author social postscripts |
| `^\s*https?://\S+\s*$` | URL-only lines |
| `\([a-z0-9.-]+\.[a-z]{2,}/[a-z0-9/_-]+\)` | URL slugs in parentheses |

---

## Patterns removed by postprocess.py (--strip-ctas)

A second-pass cleanup for patterns that survive HTML→Markdown conversion:

| Pattern | Notes |
|---|---|
| Multi-line "Tired of reading?" blocks | Full paragraph removed |
| "Hi, I'm Alexander, I've been programming…" | Author biography paragraphs |
| "Buy as a gift" | Promotional links near top of page |
| "Can I buy on Amazon?" / "Is it on Amazon?" | FAQ mixed into content |
| "How is this better than ChatGPT?" | Marketing FAQ |
| "In Other Languages" list blocks | Tab rows that survived scraper |
| Copyright / All rights reserved lines | Footer text |

---

## Patterns removed by formatter agent (manual review)

These require reading the full page context:

| Pattern | Notes |
|---|---|
| Sidebar navigation file-tree lines | Lines like "Navigation / Intro / buttons / Button / MacOSButton" |
| Per-language link lists (no prose) | 20+ links repeated across 9 language stubs |
| Duplicate landing pages | /, /refactoring, /design-patterns with 80% overlap |

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
these fonts are installed.

To **omit** CJK content entirely rather than fix font rendering:
```
--exclude "/(zh|ja|ko)/"
```
