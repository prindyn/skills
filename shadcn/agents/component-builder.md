# Custom shadcn-Compatible Component Builder

Use this guide when the user needs a component that doesn't exist in the shadcn/ui catalog but should integrate seamlessly with the existing design system.

---

## When to build a custom component

- The needed UI pattern isn't covered by any shadcn component
- You need domain-specific logic baked into the component (e.g., `StatusBadge`, `CurrencyInput`, `UserAvatar`)
- You're composing several shadcn primitives into a named, reusable unit
- You want variant-driven styling via `cva()`

---

## Pre-flight checklist

Before writing code, answer:

1. **Can I compose existing components?** A "delete confirmation button" is an `AlertDialog` with a `Button` trigger — no new file needed.
2. **Does Radix UI have the right primitive?** Check [radix-ui.com/primitives](https://www.radix-ui.com/primitives) for accessible building blocks (Toggle, Toolbar, Slider, etc.).
3. **What variants does this need?** Define them upfront so `cva()` handles the class logic cleanly.
4. **Does it need forwarded refs?** Use `React.forwardRef` for any component that wraps a DOM element so it's usable with `asChild` and refs.

---

## Standard patterns

### Pattern 1: Simple styled wrapper with `cn()`

For cases where you just need a consistently styled element:

```tsx
// components/ui/page-header.tsx
import * as React from "react"
import { cn } from "@/lib/utils"

interface PageHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  eyebrow?: string
}

function PageHeader({ className, eyebrow, children, ...props }: PageHeaderProps) {
  return (
    <div className={cn("space-y-1", className)} {...props}>
      {eyebrow && (
        <p className="text-sm font-medium text-primary">{eyebrow}</p>
      )}
      {children}
    </div>
  )
}

export { PageHeader }
```

### Pattern 2: Variant-driven component with `cva()`

For components that need multiple visual variants:

```tsx
// components/ui/status-badge.tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const statusBadgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium",
  {
    variants: {
      status: {
        active:    "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-200",
        inactive:  "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300",
        pending:   "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-200",
        error:     "bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-200",
        info:      "bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-200",
      },
    },
    defaultVariants: { status: "inactive" },
  }
)

const statusDot: Record<string, string> = {
  active:  "bg-emerald-500",
  inactive: "bg-gray-400",
  pending: "bg-amber-500 animate-pulse",
  error:   "bg-red-500",
  info:    "bg-blue-500",
}

interface StatusBadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof statusBadgeVariants> {
  showDot?: boolean
}

function StatusBadge({ className, status, showDot = true, children, ...props }: StatusBadgeProps) {
  return (
    <span className={cn(statusBadgeVariants({ status }), className)} {...props}>
      {showDot && (
        <span className={cn("h-1.5 w-1.5 rounded-full", statusDot[status ?? "inactive"])} />
      )}
      {children ?? status}
    </span>
  )
}

export { StatusBadge, statusBadgeVariants }
```

Usage:
```tsx
<StatusBadge status="active" />
<StatusBadge status="pending">Awaiting review</StatusBadge>
<StatusBadge status="error" showDot={false}>Failed</StatusBadge>
```

### Pattern 3: Composable component (forwardRef + asChild)

For interactive elements that need ref forwarding and polymorphism:

```tsx
// components/ui/stat-card.tsx
import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingDown, TrendingUp } from "lucide-react"

interface StatCardProps {
  title: string
  value: string | number
  change?: string
  trend?: "up" | "down" | "neutral"
  icon?: React.ComponentType<{ className?: string }>
  className?: string
}

function StatCard({ title, value, change, trend, icon: Icon, className }: StatCardProps) {
  return (
    <Card className={cn("", className)}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
        {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {change && (
          <div className="flex items-center gap-1 mt-1">
            {trend === "up" && <TrendingUp className="h-3 w-3 text-emerald-500" />}
            {trend === "down" && <TrendingDown className="h-3 w-3 text-red-500" />}
            <p className={cn(
              "text-xs",
              trend === "up" && "text-emerald-600 dark:text-emerald-400",
              trend === "down" && "text-red-600 dark:text-red-400",
              trend === "neutral" && "text-muted-foreground",
            )}>
              {change}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export { StatCard }
```

### Pattern 4: Radix UI primitive wrapper

When you need Radix behaviors (accessible keyboard nav, focus management, aria attributes):

```tsx
// components/ui/tag-input.tsx
// A multi-value tag input built on Radix primitives
import * as React from "react"
import { X } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"

interface TagInputProps {
  value: string[]
  onChange: (tags: string[]) => void
  placeholder?: string
  className?: string
  maxTags?: number
}

function TagInput({ value, onChange, placeholder = "Add tag...", className, maxTags }: TagInputProps) {
  const [inputValue, setInputValue] = React.useState("")
  const inputRef = React.useRef<HTMLInputElement>(null)

  function addTag(tag: string) {
    const trimmed = tag.trim().toLowerCase()
    if (!trimmed || value.includes(trimmed)) return
    if (maxTags && value.length >= maxTags) return
    onChange([...value, trimmed])
    setInputValue("")
  }

  function removeTag(tag: string) {
    onChange(value.filter((t) => t !== tag))
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault()
      addTag(inputValue)
    }
    if (e.key === "Backspace" && !inputValue && value.length > 0) {
      removeTag(value[value.length - 1])
    }
  }

  return (
    <div
      className={cn(
        "flex flex-wrap gap-1.5 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2",
        className,
      )}
      onClick={() => inputRef.current?.focus()}
    >
      {value.map((tag) => (
        <Badge key={tag} variant="secondary" className="gap-1 pr-1">
          {tag}
          <button
            type="button"
            onClick={(e) => { e.stopPropagation(); removeTag(tag) }}
            className="rounded-full hover:bg-muted p-0.5"
            aria-label={`Remove ${tag}`}
          >
            <X className="h-3 w-3" />
          </button>
        </Badge>
      ))}
      <input
        ref={inputRef}
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        onBlur={() => addTag(inputValue)}
        placeholder={value.length === 0 ? placeholder : ""}
        className="flex-1 min-w-[120px] bg-transparent outline-none placeholder:text-muted-foreground"
        aria-label="Tag input"
      />
    </div>
  )
}

export { TagInput }
```

---

## Naming conventions

| Rule | Example |
|---|---|
| Component file: `kebab-case.tsx` | `status-badge.tsx` |
| Component export: `PascalCase` | `StatusBadge` |
| Props interface: `ComponentNameProps` | `StatusBadgeProps` |
| Variant helper: `componentNameVariants` | `statusBadgeVariants` |
| Lives in: `components/ui/` | `components/ui/status-badge.tsx` |

---

## Required dependencies

Make sure these are installed (shadcn init creates them):

```bash
npm install class-variance-authority clsx tailwind-merge lucide-react
```

The `cn()` helper must exist at `@/lib/utils`:

```ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## Dark mode considerations

Always pair light and dark variants in the same `cva()` variant:

```ts
// Good — both light and dark in one variant entry
active: "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-200",

// Bad — only light colors
active: "bg-emerald-100 text-emerald-800",
```

Use semantic tokens (`bg-muted`, `text-foreground`) instead of raw Tailwind colors wherever possible — they switch automatically.

---

## Accessibility checklist

Before shipping a custom component:

- [ ] Interactive elements are focusable (`tabIndex`, `role`, or native element)
- [ ] Keyboard navigation works (Enter/Space to activate, Escape to dismiss)
- [ ] `aria-label` on icon-only buttons
- [ ] `aria-expanded`, `aria-controls` on toggles
- [ ] Color alone is not the only indicator (pair color with icon or text)
- [ ] Focus ring visible in both light and dark mode (`ring-ring`)
- [ ] Screen-reader-only text with `className="sr-only"` where needed

---

## Testing the component

Once built, verify it works with:

```bash
# Type-check
npx tsc --noEmit

# Lint
npx eslint components/ui/your-component.tsx

# Or run your test suite
npm test
```

Render the component in isolation (Storybook or a test route) to verify all variants and states.
