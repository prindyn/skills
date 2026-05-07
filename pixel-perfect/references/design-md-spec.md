# DESIGN.md Spec Reference

A condensed reference to the DESIGN.md format (Google `design.md` spec, alpha,
Apache-2.0). Use this when you don't have network access to fetch the full
spec or when you need to reason about validation locally.

For the canonical source, see https://github.com/google-labs-code/design.md.
For the formal authoring workflow with `npx @google/design.md`, use the
sibling `design-md` skill.

## File anatomy

A DESIGN.md file is a Markdown file with **YAML front matter** at the top:

```md
---
version: alpha
name: Heritage
description: Architectural minimalism meets journalistic gravitas.
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
spacing:
  sm: 8px
  md: 16px
  lg: 24px
rounded:
  sm: 4px
  md: 8px
  lg: 16px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
---

## Overview
…prose…

## Colors
…prose…
```

## Required vs optional

Required:

- `name:` (string)
- At least one of `colors:` / `typography:` / `spacing:` / `rounded:` /
  `components:` — usually `colors:` at minimum.

Strongly recommended:

- `version: alpha`
- `description:` (one-line tagline)
- A Markdown body explaining the **why** behind tokens (rationale beats
  values when ambiguity arises).

## Token types

| Type             | Format                                  | Examples                          |
|------------------|-----------------------------------------|-----------------------------------|
| Color            | hex string, sRGB                        | `"#1A1C1E"`, `"#FFF"`             |
| Dimension        | number + unit (`px`, `em`, `rem`, `%`)  | `48px`, `1.25rem`, `"-0.02em"`    |
| Token reference  | `{path.to.token}`                       | `{colors.primary}`, `{rounded.sm}`|
| Typography       | object (see below)                      | see Typography section            |

### Typography object shape

```yaml
h1:
  fontFamily: Public Sans          # string
  fontSize: 3rem                    # dimension
  fontWeight: 700                   # number 100-900
  lineHeight: 1.1                   # unitless ratio
  letterSpacing: "-0.02em"          # quoted dimension (negative needs quotes)
  fontFeature: "tnum"               # OpenType feature, optional
  fontVariation: "wght 700"         # variable-font axis values, optional
```

### Component property whitelist

Components support **only** these properties:

- `backgroundColor`
- `textColor`
- `typography` (a token reference into `typography:`, e.g. `{typography.body-md}`)
- `rounded`
- `padding`
- `size`, `height`, `width`

Anything else produces an `unknown-component-property` warning.

### Component variants

Variants (hover, active, pressed, disabled, focus) are **separate component
entries** at the top level, with related key names:

```yaml
button-primary:
  backgroundColor: "{colors.tertiary}"
button-primary-hover:
  backgroundColor: "{colors.primary}"
button-primary-disabled:
  backgroundColor: "{colors.neutral}"
  textColor: "{colors.secondary}"
```

**Do not** nest them as `button-primary.hover`. The spec rejects nested
variants.

## Token references

Resolve by dotted path from the front-matter root:

- `{colors.primary}` ✅
- `{rounded.sm}` ✅
- `{typography.h1.fontSize}` ✅
- `{primary}` ❌ (no parent)
- `{colors[primary]}` ❌ (only dot syntax)

References are checked at lint time. A broken reference is an error,
not a warning.

## Canonical Markdown sections

If a section appears, it must appear in this order. Duplicate headings
reject the file.

1. Overview (alias: Brand & Style)
2. Colors
3. Typography
4. Layout (alias: Layout & Spacing)
5. Elevation & Depth (alias: Elevation)
6. Shapes
7. Components
8. Do's and Don'ts

Unknown sections are preserved without error. Missing sections are fine.

## Lint rules (what the validator checks)

| Rule                          | Severity    | What it catches                                |
|-------------------------------|-------------|------------------------------------------------|
| `broken-ref`                  | error       | `{colors.missing}` → no such token             |
| `duplicate-section`           | error       | same `## Heading` appears twice                |
| `invalid-color`               | error       | not a valid hex                                |
| `invalid-dimension`           | error       | bad unit, NaN, missing unit                    |
| `invalid-typography`          | error       | typography object missing required keys        |
| `wcag-contrast`               | warning/info| component textColor vs backgroundColor < 4.5:1 |
| `unknown-component-property`  | warning     | component uses property outside whitelist      |

`scripts/validate_design_md.py` in this skill implements the same rules
without requiring `npx`.

## Common pitfalls

- **Quote your hex strings.** YAML treats `#` as comment.
  `primary: #1A1C1E` is wrong; `primary: "#1A1C1E"` is right.
- **Quote negative dimensions.** `letterSpacing: -0.02em` is parsed as a
  YAML flow expression. Quote: `letterSpacing: "-0.02em"`.
- **Use sibling component keys for variants.** Not nested objects.
- **Token path uses dots.** `{colors.primary}`, never `{colors/primary}`
  or `{colors:primary}`.
- **Section order is strict.** If you generate a DESIGN.md from
  unstructured input, reorder before saving.

## Pixel-Perfect-relevant takeaways

When implementing UI from a DESIGN.md:

- **Hex literals in implementation are token drift.** Every color in CSS,
  Tailwind config, or component code should be a CSS variable / Tailwind
  alias / lookup against the token set.
- **Component variants in DESIGN.md become props in code.** A
  `button-primary-hover` entry becomes the `:hover` rule of `<Button
  variant="primary">`, not a separate component.
- **The Markdown body's "why" wins ties.** When two implementations are
  both plausible, the rationale prose tells you which fits the brand.
- **Update DESIGN.md when you discover new tokens.** If you needed an
  `error` color and DESIGN.md only had `primary/secondary/tertiary`, add
  `colors.error` there *first*, then reference it in code.
