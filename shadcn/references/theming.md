# shadcn/ui Theming Guide

shadcn/ui themes are defined as CSS custom properties (HSL values without the `hsl()` wrapper) in your global stylesheet. This lets Tailwind utilities like `bg-primary` and `text-muted-foreground` automatically pick up your theme.

---

## CSS Variable Reference

All values are HSL in the format `H S% L%` (no `hsl()` wrapper — Tailwind adds that).

### Semantic Color Tokens

| Variable | Tailwind Class | Purpose |
|---|---|---|
| `--background` | `bg-background` | Page background |
| `--foreground` | `text-foreground` | Primary text |
| `--card` | `bg-card` | Card background |
| `--card-foreground` | `text-card-foreground` | Card text |
| `--popover` | `bg-popover` | Popover background |
| `--popover-foreground` | `text-popover-foreground` | Popover text |
| `--primary` | `bg-primary` / `text-primary` | Brand/action color |
| `--primary-foreground` | `text-primary-foreground` | Text on primary |
| `--secondary` | `bg-secondary` | Secondary surface |
| `--secondary-foreground` | `text-secondary-foreground` | Text on secondary |
| `--muted` | `bg-muted` | Subdued backgrounds |
| `--muted-foreground` | `text-muted-foreground` | Subdued text |
| `--accent` | `bg-accent` | Accent/hover states |
| `--accent-foreground` | `text-accent-foreground` | Text on accent |
| `--destructive` | `bg-destructive` | Danger/error |
| `--destructive-foreground` | `text-destructive-foreground` | Text on destructive |
| `--border` | `border-border` | Default borders |
| `--input` | `border-input` | Input borders |
| `--ring` | `ring-ring` | Focus rings |
| `--radius` | — | Base border radius (used by components) |

### Chart Color Tokens

| Variable | Used In |
|---|---|
| `--chart-1` | First data series |
| `--chart-2` | Second data series |
| `--chart-3` | Third data series |
| `--chart-4` | Fourth data series |
| `--chart-5` | Fifth data series |

---

## Complete Default Theme (Zinc base)

Add this to your `globals.css`. See `assets/globals.css` for the full stylesheet.

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 240 10% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 240 10% 3.9%;
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 240 5.9% 10%;
    --radius: 0.5rem;
    --chart-1: 12 76% 61%;
    --chart-2: 173 58% 39%;
    --chart-3: 197 37% 24%;
    --chart-4: 43 74% 66%;
    --chart-5: 27 87% 67%;
  }

  .dark {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;
    --card: 240 10% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 240 10% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 240 5.9% 10%;
    --secondary: 240 3.7% 15.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 240 3.7% 15.9%;
    --muted-foreground: 240 5% 64.9%;
    --accent: 240 3.7% 15.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 3.7% 15.9%;
    --input: 240 3.7% 15.9%;
    --ring: 240 4.9% 83.9%;
    --chart-1: 220 70% 50%;
    --chart-2: 160 60% 45%;
    --chart-3: 30 80% 55%;
    --chart-4: 280 65% 60%;
    --chart-5: 340 75% 55%;
  }
}
```

---

## Changing the Base Color

The easiest way to retheme is to swap the base color palette. Run `npx shadcn@latest init` in a fresh project and pick a different base, or manually replace your CSS variables.

### Slate theme (`--primary: 222.2 47.4% 11.2%`)

```css
:root {
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --accent: 210 40% 96.1%;
  --accent-foreground: 222.2 47.4% 11.2%;
  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 222.2 47.4% 11.2%;
}
```

### Blue accent brand color

```css
:root {
  --primary: 221.2 83.2% 53.3%;    /* blue-600 equivalent */
  --primary-foreground: 210 40% 98%;
  --ring: 221.2 83.2% 53.3%;
}
```

### Green brand color

```css
:root {
  --primary: 142.1 76.2% 36.3%;    /* green-600 equivalent */
  --primary-foreground: 355.7 100% 99%;
  --ring: 142.1 76.2% 36.3%;
}
```

---

## Border Radius

`--radius` controls all component rounding. Components derive their own radius from this:

```css
:root {
  --radius: 0.5rem;   /* default: medium rounding */
}
```

| Value | Look |
|---|---|
| `0rem` | Sharp corners (squared) |
| `0.3rem` | Subtle rounding |
| `0.5rem` | Default |
| `0.75rem` | Pronounced rounding |
| `1rem` | Very rounded |

---

## Dark Mode Setup

### next-themes (Next.js)

```bash
npm install next-themes
```

```tsx
// app/providers.tsx
"use client"
import { ThemeProvider } from "next-themes"

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
      {children}
    </ThemeProvider>
  )
}

// app/layout.tsx
import { Providers } from "./providers"
export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body><Providers>{children}</Providers></body>
    </html>
  )
}
```

### Theme toggle component

```tsx
"use client"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
```

### Vanilla (no framework)

```ts
// Toggle dark mode:
document.documentElement.classList.toggle("dark")

// Persist preference:
const theme = localStorage.getItem("theme") ?? "light"
document.documentElement.classList.add(theme)
```

---

## Tailwind v4 Theming

Tailwind v4 uses a CSS-first configuration. If you're on v4, use the `@theme` block instead of `tailwind.config.ts`:

```css
/* globals.css */
@import "tailwindcss";

@theme {
  --color-background: hsl(var(--background));
  --color-foreground: hsl(var(--foreground));
  --color-primary: hsl(var(--primary));
  --color-primary-foreground: hsl(var(--primary-foreground));
  /* ... map all semantic tokens */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}
```

---

## Custom Fonts

```css
/* globals.css */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

```ts
// tailwind.config.ts
import { fontFamily } from "tailwindcss/defaultTheme"

export default {
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-sans)", ...fontFamily.sans],
        mono: ["var(--font-mono)", ...fontFamily.mono],
      },
    },
  },
}
```

---

## Theming Tips

1. **Always use semantic tokens** (`bg-primary`, not `bg-blue-600`) so dark mode just works.
2. **`hsl(var(--primary) / 0.5)`** — add opacity with the `/` syntax in newer CSS.
3. **Preview themes** at [ui.shadcn.com/themes](https://ui.shadcn.com/themes) before building.
4. **Component-level overrides**: pass `className` to any shadcn component to override individual styles — shadcn uses `cn()` which handles merging safely.
