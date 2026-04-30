# Domain Name Selection

The user has a brand name (or a shortlist). Now they need the actual web address. The hard part isn't checking availability — it's deciding what to do when the obvious `.com` is taken, which is true for ~95% of dictionary words and most short brand names.

## The hierarchy of domain options

In order of how strong each is for a new brand:

1. **`brandname.com`** — the gold standard. If available, take it.
2. **`getbrandname.com` / `trybrandname.com` / `usebrandname.com`** — common SaaS workaround. Mid-tier; works fine if the user expects type-in traffic to be minimal.
3. **`brandname.co`** — close to .com, common for tech startups. Tier 2.
4. **`brandname.io` / `.app` / `.studio` / `.design`** — modern TLDs. Strong signal of the category. Good for tech/dev/creative; weaker for general consumer.
5. **`brandname.[country code]`** — `.uk`, `.de`, `.au`, `.fr`. Strong for local/regional businesses, weaker for global plays.
6. **Hyphenated or alternative-spelling `.com`** — `brand-name.com`, `branduname.com`. **Generally avoid** — hard to communicate verbally and feels off.
7. **`.net`, `.org`, `.biz`, `.info`** — outdated. `.org` is fine for non-profits and only non-profits. The others signal "the .com was taken and we settled."

## Decision framework

Walk the user through these questions in order:

1. **Is the exact-match `.com` available?** → Buy it now, don't wait. Use a registrar with WHOIS privacy (Namecheap, Porkbun, Cloudflare Registrar are good defaults).

2. **If the `.com` is taken, who owns it and is it for sale?**
    - **Active business with a similar name** → drop the name. Don't fight an existing company in a related space.
    - **Active business in a totally unrelated industry** → you can probably coexist (a hardware store and a SaaS sharing a name will never confuse customers), but expect minor SEO friction forever.
    - **Parked/for sale** → consider the price. Domains in the $1k–$10k range are reasonable for a brand the user is committing to. Domains over $20k almost always aren't worth it for a new business — that money is better spent on the business itself, with a different name or a tier-2 TLD.
    - **Someone using it casually (a personal blog, an old portfolio)** → you can sometimes reach out and offer to buy it for a few hundred dollars. No guarantees.

3. **What kind of business is this?**
    - **Consumer brand** → push hard for `.com`. Consumers default to typing `.com`. Even sophisticated consumers reach for it.
    - **Tech/SaaS** → `.com`, `.io`, `.app`, `.co` are all acceptable. SaaS audiences understand modern TLDs.
    - **Local service business** → exact-match `.com` ideal, country code TLD acceptable, anything else weak.
    - **Creative/portfolio** → `.studio`, `.design`, `.art` can work and signal the category.

4. **How much traffic comes from people typing the URL vs. clicking a link?**
    - **High type-in traffic** (memorable consumer brand) → `.com` is essential. Wrong TLD = customers landing on competitor's site.
    - **Almost all click traffic** (SaaS, B2B, content) → TLD matters less. Optimize for the brand decision, then pick the best available TLD.

## When to change the name to get a better domain

If the user's preferred name has a hopelessly taken `.com` and only weak alternatives, it's worth surfacing the question: **is this name worth the friction?**

The cost of a non-`.com` domain (or a `getbrand.com` workaround) is real but bounded — millions of successful businesses use them. The cost of a *bad* domain (long, hyphenated, weird TLD, easy to misspell) compounds over years.

A useful test: **Have the user say their domain out loud, including the TLD, as if to a stranger over the phone.** If "trybrandname.com" or "brand.studio" rolls off the tongue, fine. If they're hedging or stumbling, that's friction they'll feel for the life of the business.

If the friction is too high, suggest they pick their #2 or #3 name candidate where the `.com` is clean, rather than fighting for the #1 candidate's compromise domain.

## Practical tactics for finding alternatives

When the obvious `.com` is gone, generate alternatives by:

- **Adding a verb or article**: `getX`, `tryX`, `useX`, `meetX`, `theX`
- **Adding the category word**: `Xapp`, `Xhq`, `Xstudio`, `Xco`, `Xlabs`
- **Adding a regional or descriptive modifier**: `XNYC`, `XLondon`, `Xclub`
- **Trying the plural or a verb form**: if `bird.com` is gone, try `birds.com` or `birdy.com`
- **Trying a related or evocative word entirely**: if the chosen name is `Tide`, also check `Wave`, `Crest`, `Ebb`

## Domains to definitely avoid

- **Hyphens**: `acme-co.com`. Verbal nightmare ("acme dash co"), gets confused with the non-hyphenated version, signals "the real .com was taken."
- **Numbers in place of words**: `4you`, `2go`. Felt clever in 2005. Today reads as dated and amateur.
- **Multiple TLDs that conflict**: if `brand.com` and `brand.co` are different companies, you'll lose customers to the other one constantly. If you can't get the matching `.com`, at least make sure there's no big competitor on the variant.
- **Unicode characters**: domains with accents or non-Latin chars are technically possible but break copy-paste, autocomplete, and most users' mental models. Skip.

## Things to verify before they buy

- **Trademark conflict in the same industry.** A domain you can register isn't a brand you can defend. If a similarly-named company exists in the same category, get a trademark search done before launching.
- **Social handles.** Check Instagram, Twitter/X, TikTok, LinkedIn for the same handle. Inconsistency across channels is a real cost. Tools like `namechk.com` check many platforms at once.
- **Past use of the domain.** Old `archive.org` snapshots can reveal if the domain previously hosted something problematic (gambling, spam, adult content) that might still affect Google's view of it. Use a tool like `wayback machine` or `expireddomains.net` to check.
- **Email-friendly.** Will the founder be giving out an email at this domain? If the domain is hard to spell or contains non-obvious words, every email handoff becomes a moment of friction.

## What to deliver

When the user comes to you for domain help, your output should be:

1. **`.com` availability** for their top 3 name candidates (do the actual lookup if you have web access; otherwise instruct them how)
2. **A ranked list of available alternatives** for each, using the hierarchy above
3. **A clear recommendation**: "Go with `brand.com` if open. If taken, my recommendation is `getbrand.com` over `brand.io` because [reason specific to their business type]."
4. **Buy-now reminders**: domains can be registered the same day, and squatters do watch DNS lookups. If the user's preferred domain is available, encourage them to register *now*, not "this weekend."
