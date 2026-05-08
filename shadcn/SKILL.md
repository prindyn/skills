---
name: shadcn
description: Create shadcn/ui compatible components, page templates, and layouts for React projects. Use this skill whenever the user wants to add UI components, build pages, scaffold layouts, configure theming, or work with design systems using shadcn/ui, Radix UI primitives, or Tailwind CSS. Trigger on phrases like: "add a shadcn component", "create a dashboard layout", "build a login page", "set up shadcn", "I need a data table", "create a settings page", "add a sidebar", "build a form", "use shadcn components", "card layout", "create a nav", "build a modal", "add a toast", "responsive layout with shadcn".
compatibility: Requires Node.js 18+, React 18+, Tailwind CSS v3/v4, and a supported framework (Next.js, Vite, Remix, Astro, Laravel).
metadata:
  version: "1.0"
  author: shadcn-skill
---

# shadcn Skill

Build production-ready UIs using [shadcn/ui](https://ui.shadcn.com/) — accessible, beautifully designed components built on Radix UI primitives and Tailwind CSS.

**Key concept**: shadcn/ui components are *copied into your project*, not installed as an npm dependency. You own the code and can customize every detail. Components live in `components/ui/` by default.

## Quick Links
- Full component list: `references/components.md`
- Theming guide: `references/theming.md`
- Common patterns: `references/patterns.md`
- CLI reference: `references/cli.md`
- Custom component guide: `agents/component-builder.md`
- Templates: `templates/`

---

## 1. Check / Initialize the Project

First, check whether shadcn is already set up:

```bash
bash scripts/check_setup.sh
```

If not initialized, run:

```bash
npx shadcn@latest init
```

Prompts you'll see:
- **Style**: `default` (rounded, softer) or `new-york` (compact, sharp — recommended for modern apps)
- **Base color**: `slate` | `gray` | `zinc` | `neutral` | `stone`
- **CSS variables**: `yes` (always choose yes for proper theming)

This creates `components.json` at the project root and sets up CSS variables in your global stylesheet. See `assets/components.json` for a reference config.

---

## 2. Adding Components

### Install via CLI (always preferred)

```bash
npx shadcn@latest add button
npx shadcn@latest add card dialog input label
```

### Batch install helper

```bash
bash scripts/add_components.sh button card input dialog sheet sonner
```

### Full component catalog

See `references/components.md` — components are organized by category (forms, layout, navigation, overlay, data display, feedback).

---

## 3. Using Components

Import from `@/components/ui/<name>`:

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
```

### Button variants

```tsx
<Button>Default</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="link">Link</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button disabled>Disabled</Button>
<Button asChild><a href="/login">Link button</a></Button>
```

### Card

```tsx
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Supporting text</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Main content area</p>
  </CardContent>
  <CardFooter className="flex justify-end gap-2">
    <Button variant="outline">Cancel</Button>
    <Button>Save</Button>
  </CardFooter>
</Card>
```

---

## 4. Templates

Ready-to-use page templates in `templates/`. Copy to your app and customize.

| Template | File | Required Components |
|---|---|---|
| Dashboard | `templates/dashboard-layout.tsx` | sidebar, card, badge, button, avatar, separator |
| Auth (Login/Signup) | `templates/auth-page.tsx` | card, input, label, button, tabs, form |
| Data Table | `templates/data-table-page.tsx` | table, button, input, badge, dropdown-menu |
| Settings | `templates/settings-page.tsx` | tabs, card, input, label, button, switch, select |

Each template file starts with the exact `npx shadcn@latest add ...` commands needed.

### Scaffold a new page

```bash
python scripts/scaffold.py --template dashboard --output src/app/dashboard/page.tsx
python scripts/scaffold.py --template auth --output src/app/login/page.tsx
python scripts/scaffold.py --template data-table --output src/app/users/page.tsx
python scripts/scaffold.py --template settings --output src/app/settings/page.tsx
```

---

## 5. Theming

shadcn/ui uses CSS custom properties (HSL values). The full theme lives in your `globals.css`.

Quick reference — variables you'll customize most often:

| Variable | Purpose |
|---|---|
| `--primary` | Brand color (buttons, links, focus rings) |
| `--background` | Page background |
| `--foreground` | Primary text color |
| `--muted` | Subtle backgrounds (inputs, cards) |
| `--accent` | Hover states |
| `--radius` | Border radius (affects all components) |

Full theming guide: `references/theming.md`

Default theme CSS: `assets/globals.css`

### Dark mode

Add `class="dark"` to `<html>`. All components respond automatically.

```tsx
// Next.js: use next-themes
import { ThemeProvider } from "next-themes"
// Wrap your app:
<ThemeProvider attribute="class" defaultTheme="system" enableSystem>
  {children}
</ThemeProvider>
```

---

## 6. Forms with Validation

shadcn Form component wraps **react-hook-form** + **zod**:

```bash
npx shadcn@latest add form input label button
npm install react-hook-form zod @hookform/resolvers
```

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: { email: "", password: "" },
  })

  function onSubmit(values: z.infer<typeof schema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input placeholder="you@example.com" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit" className="w-full">Sign in</Button>
      </form>
    </Form>
  )
}
```

---

## 7. Creating Custom Components

When you need a component that doesn't exist in shadcn's catalog, build it to match shadcn conventions so it integrates seamlessly.

See `agents/component-builder.md` for the complete guide.

Quick pattern:

```tsx
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const statusBadgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
  {
    variants: {
      status: {
        active: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100",
        inactive: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100",
        pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100",
        error: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-100",
      },
    },
    defaultVariants: { status: "active" },
  }
)

interface StatusBadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof statusBadgeVariants> {}

function StatusBadge({ className, status, ...props }: StatusBadgeProps) {
  return <span className={cn(statusBadgeVariants({ status }), className)} {...props} />
}

export { StatusBadge }
```

---

## 8. Common Patterns

For detailed, copy-paste implementations of these patterns, see `references/patterns.md`:

- **Data table** with sorting, filtering, and pagination (TanStack Table)
- **Multi-step form** with progress indicator
- **Sidebar navigation** with collapsible groups
- **Command palette** (⌘K) with search
- **Toast notifications** with Sonner
- **Confirmation dialogs**
- **Infinite scroll** with Scroll Area
- **Dashboard stat cards** grid

---

## Troubleshooting

**`Cannot find module '@/components/ui/...'`**
Run `npx shadcn@latest add <component>` — the component hasn't been added yet.

**Styles aren't applying**
Confirm Tailwind's `content` glob in `tailwind.config.ts` includes your file paths:
```ts
content: ["./src/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"]
```

**`cn is not defined` / missing `lib/utils.ts`**
Run `npx shadcn@latest init` to create `lib/utils.ts`. Or create it manually:
```ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```
Then `npm install clsx tailwind-merge`.

**TypeScript path alias errors**
Ensure `tsconfig.json` has:
```json
{ "compilerOptions": { "paths": { "@/*": ["./src/*"] } } }
```

**Component looks unstyled in production**
Tailwind may be purging classes. Ensure the component file paths are in `content` config.
