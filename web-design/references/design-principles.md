# Design Principles

The handful of fundamentals that, applied consistently, separate a website that works from one that doesn't. Adapted from the Gentle Media 2025 Guide to Web Design and standard UX practice.

## 1. Consistency / branding

A consistent look and feel across the site reinforces the brand and makes navigation predictable. The user shouldn't feel like they walked into a different building when they click to a new page.

- **Brand kit:** colors, typography, imagery style, voice — defined once, applied everywhere. (See `templates/design-system.md`.)
- **Uniform UI elements:** buttons, headers, footers, form fields look the same everywhere.
- **Predictable navigation:** menu in the same place on every page; links behave the same way.

If you're designing an e-commerce site, the product page, checkout, and confirmation email should all feel like they came from the same brand. Breaking visual continuity erodes trust.

## 2. Visual hierarchy

The arrangement of elements that tells the visitor's eye *what to look at first*. The visitor doesn't think about it consciously — that's the point. The page either guides them well or it doesn't.

Tools you have:
- **Size & scale:** larger = more important. The headline is the biggest text; the CTA is the boldest button.
- **Color & contrast:** the only element in your accent color should be the thing you most want clicked.
- **Position:** top and center get seen first. The most important thing belongs there.
- **Whitespace:** what surrounds an element makes it feel important. Crowding hides what matters.

**Application:** on a homepage, the headline should be the largest text, the primary CTA should be the only element in your accent color, supporting info should be smaller and lower. If a visitor's eye wanders, the hierarchy is broken.

## 3. Simplicity & clarity

The most common web design mistake is doing too much. Every element on the page either serves the primary CTA or steals attention from it.

- **Purpose test:** for each element on a page, ask "does this serve the page's CTA?" If no, cut it.
- **Limit fonts:** at most 2 type families.
- **Limit colors:** brand color + neutrals + 1 accent. Anything else is decoration looking for a job.
- **Clear navigation:** a visitor should find the main pages within 1 second. If they can't, the menu is too clever.

A product page should focus on the product image, description, and "Buy" button. Adding a sidebar of "you might also like," a chat widget, a banner, a popup, and a footer megamenu *on the same page* is how you get a 0% conversion rate.

## 4. Responsive / mobile-first design

Most visitors will see the site on a phone. Design for that screen first; the desktop version is the *expansion*, not the primary.

- **Flexible layouts:** content flows to fit any screen size.
- **Scalable images:** never load a 4000px-wide hero image on a phone.
- **Mobile-first means mobile-priority:** if a section can't survive on a small screen, it's probably not essential on desktop either.
- **Test on real devices**, not just the browser's responsive simulator. Real iPhones and Androids reveal problems simulators hide.

## 5. Accessibility

Designing so that as many people as possible can use the site — including those with visual, motor, or cognitive disabilities. Required by law in many places, but more importantly, *just good design*.

- **Contrast:** text vs. background must pass WCAG AA (4.5:1 for body, 3:1 for large text). Verify with a contrast tool.
- **Alt text:** every meaningful image describes what it shows, for screen readers.
- **Keyboard navigation:** the entire site usable without a mouse. Tab through your forms.
- **Readable fonts:** clear, legible, sized at least 16px for body.
- **Scalable text:** users should be able to zoom in 200% without breaking the layout.

Bonus: alt text and clear semantic structure also help SEO. Accessibility and SEO overlap heavily.

## 6. Engaging visuals & media (use wisely)

Visuals draw people in but can also clutter. The bar is high: every image should *do work*.

- **High-quality images.** Poor-quality images make the whole site feel cheap. Optimize for web (compress, modern formats like WebP).
- **Relevant imagery.** Generic stock photos (the handshake, the headset call center) hurt more than they help — they signal "we didn't bother."
- **Balanced media mix.** Photos, illustrations, video, and graphics complement content; they don't replace it.
- **Hero video:** can substantially increase time on page and conversion, *if* it loads fast and works on mobile.

## 7. Content & typography

Visuals get attention; content keeps it. Typography is half the design.

- **Readable fonts.** Sans-serif (Inter, Helvetica, system-ui) for body text on screens. Save script and decorative fonts for very limited use.
- **Hierarchy in text.** Clear H1/H2/H3 sizes guide the reader. The H1 is the largest; subheads step down predictably.
- **Line spacing & alignment.** Body text wants 1.4–1.6 line-height. Left-aligned for long-form (centered paragraphs are hard to read).
- **Concise content.** Visitors skim. Make headlines and bullets scannable; bury detail under "read more" if needed.
- **Tone:** matches the brand. Formal, friendly, technical, playful — pick one and hold it consistently.

## 8. User-centered design (UCD)

Design for the actual humans who will visit, not the imaginary ideal visitor. UCD is a process: research, design, test, iterate.

- **Know the audience.** Demographics, goals, pain points, level of tech comfort.
- **User testing.** Watch a real person try to do the primary task. Don't help. Note where they hesitate or fail.
- **Empathy.** Walk through the site as if you'd never seen it. What feels confusing? Slow? Annoying?
- **Iterate.** Ship, watch what happens (analytics, session recordings, user feedback), refine. The site is never "done."

## 9. CTAs (Calls to Action)

The CTA is where design becomes outcome. A beautiful site that doesn't convert is not a successful site.

- **Clear, action-oriented language.** "Get Started," "Book a Call," "Download the Guide." Not "Click here" or "Learn more" alone.
- **Prominent placement.** Top of the page (in the hero), at the end of content, and at the end of any sales pitch. The visitor should never have to hunt.
- **Visual standout.** Contrasting color, bold font, generous whitespace around it. The CTA button should look unmistakably like a button you can click.
- **Context-relevant.** A CTA at the end of a blog post should relate to the post's topic, not generically push the homepage offer.
- **One primary CTA per page.** Multiple competing CTAs reduce action on all of them.

## How these principles interact

These aren't independent rules — they reinforce each other. A well-designed page has clear visual hierarchy *because* it's simple, accessibility *because* contrast and clear type were prioritized, and conversion *because* the CTA is unmistakable. When in doubt about a design decision, hold it up against this list and ask which principle it serves.
