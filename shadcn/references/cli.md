# shadcn/ui CLI Reference

All commands use the latest shadcn CLI. Run via `npx` (no global install needed).

```bash
npx shadcn@latest <command>
```

---

## `init`

Initialize shadcn/ui in a project. Creates `components.json` and sets up CSS variables.

```bash
npx shadcn@latest init
```

### Options

| Flag | Description |
|---|---|
| `-y, --yes` | Skip confirmation prompts, use defaults |
| `-d, --defaults` | Use default config (no prompts) |
| `-f, --force` | Overwrite existing files |
| `--src-dir` | Use `src/` directory structure |
| `-c, --cwd <path>` | Set working directory (default: current directory) |

### Interactive prompts

1. **Which style?** → `default` or `new-york`
2. **Which color?** → `slate` | `gray` | `zinc` | `neutral` | `stone`
3. **Use CSS variables for theming?** → yes (recommended)

### What it creates

- `components.json` — project configuration
- Updates `globals.css` with CSS custom properties
- Creates `lib/utils.ts` with the `cn()` helper
- Updates `tailwind.config.ts` with content paths

---

## `add`

Add one or more components to your project.

```bash
npx shadcn@latest add <component> [components...]
```

### Examples

```bash
# Add a single component
npx shadcn@latest add button

# Add multiple components
npx shadcn@latest add card input label button

# Add all dependencies automatically (skip prompt)
npx shadcn@latest add dialog -y
```

### Options

| Flag | Description |
|---|---|
| `-y, --yes` | Skip confirmation, install all |
| `-o, --overwrite` | Overwrite existing component files |
| `-c, --cwd <path>` | Working directory |
| `-a, --all` | Add all available components |
| `-p, --path <path>` | Override destination directory |

### What it does

1. Downloads component source from the shadcn registry
2. Installs required npm dependencies
3. Writes component file(s) to your `components/ui/` directory
4. Installs peer dependencies (e.g., Radix UI primitives, class-variance-authority)

---

## `diff`

Check for upstream changes to components you've already added.

```bash
npx shadcn@latest diff
npx shadcn@latest diff button
```

Shows a diff between your local component and the current upstream version. Useful for staying up to date without losing customizations.

---

## `build` (Registry)

Build a custom component registry. For advanced users maintaining their own component distribution.

```bash
npx shadcn@latest build
```

---

## `components.json` Reference

This file lives at your project root and controls how components are installed.

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

### Field reference

| Field | Values | Description |
|---|---|---|
| `style` | `default` \| `new-york` | Visual style. `new-york` is more compact. |
| `rsc` | `true` \| `false` | Add `"use client"` directives for non-RSC components. |
| `tsx` | `true` \| `false` | Use TypeScript (`.tsx`) or JavaScript (`.jsx`). |
| `tailwind.config` | path | Path to Tailwind config file. |
| `tailwind.css` | path | Path to global CSS with CSS variables. |
| `tailwind.baseColor` | `zinc` \| `slate` \| `gray` \| `neutral` \| `stone` | Base color palette. |
| `tailwind.cssVariables` | `true` \| `false` | Use CSS variables (strongly recommended). |
| `tailwind.prefix` | string | Tailwind class prefix, e.g. `"tw-"`. |
| `aliases.ui` | path | Where component files go. |
| `aliases.utils` | path | Where `lib/utils.ts` lives. |
| `iconLibrary` | `lucide` \| `heroicons` | Icon library to use. |

---

## Framework-Specific Setup

### Next.js (App Router)

```bash
npx create-next-app@latest my-app --typescript --tailwind --app
cd my-app
npx shadcn@latest init
```

### Next.js (Pages Router)

Same as above but set `rsc: false` in `components.json` (or answer "no" to the RSC prompt).

### Vite + React

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npx shadcn@latest init
```

### Remix

```bash
npx create-remix@latest my-app
cd my-app
npx shadcn@latest init
```

### Astro

```bash
npm create astro@latest my-app
cd my-app
npx astro add tailwind
npx shadcn@latest init
```

---

## Path Alias Requirements

shadcn requires a `@/` path alias. Ensure your `tsconfig.json` includes:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

For Vite, also add to `vite.config.ts`:

```ts
import path from "path"
import { defineConfig } from "vite"

export default defineConfig({
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") },
  },
})
```

---

## Installed Dependencies

Components install these packages as needed:

| Package | Used by |
|---|---|
| `@radix-ui/react-*` | Most components (accessible primitives) |
| `class-variance-authority` | Variant props (`cva()`) |
| `clsx` | Conditional class merging |
| `tailwind-merge` | Tailwind class conflict resolution |
| `lucide-react` | Icons |
| `@tanstack/react-table` | Data Table |
| `react-hook-form` | Form |
| `zod` | Form validation |
| `@hookform/resolvers` | Form + Zod integration |
| `react-day-picker` | Calendar / Date Picker |
| `date-fns` | Date formatting |
| `sonner` | Toast (Sonner) |
| `vaul` | Drawer |
| `embla-carousel-react` | Carousel |
| `recharts` | Chart |
| `input-otp` | Input OTP |
| `cmdk` | Command |
