# shadcn/ui Component Catalog

Complete list of all available components, organized by category. Install any component with:

```bash
npx shadcn@latest add <component-name>
```

---

## Forms & Inputs

| Component | Install Name | Description |
|---|---|---|
| **Button** | `button` | The primary action element. Supports variants: default, outline, secondary, ghost, destructive, link. Sizes: default, sm, lg, icon. |
| **Input** | `input` | Text input field. Pairs with Label and FormField. |
| **Textarea** | `textarea` | Multi-line text input. |
| **Label** | `label` | Accessible label for form controls. |
| **Checkbox** | `checkbox` | Controlled checkbox with indeterminate state. |
| **Radio Group** | `radio-group` | Group of mutually exclusive radio buttons. |
| **Select** | `select` | Dropdown select built on Radix Select. |
| **Switch** | `switch` | Toggle switch for boolean settings. |
| **Slider** | `slider` | Range slider with min/max/step. |
| **Form** | `form` | Form wrapper integrating react-hook-form. Provides FormField, FormItem, FormLabel, FormControl, FormDescription, FormMessage. |
| **Input OTP** | `input-otp` | One-time password input with segmented slots. |
| **Toggle** | `toggle` | Two-state button (pressed/unpressed). |
| **Toggle Group** | `toggle-group` | Group of Toggle buttons with single or multiple selection. |

### Form install bundle

```bash
npx shadcn@latest add form input label button
npm install react-hook-form zod @hookform/resolvers
```

---

## Layout & Structure

| Component | Install Name | Description |
|---|---|---|
| **Card** | `card` | Container with header, content, and footer sections. |
| **Separator** | `separator` | Horizontal or vertical dividing line. |
| **Aspect Ratio** | `aspect-ratio` | Maintains a consistent width-to-height ratio. |
| **Scroll Area** | `scroll-area` | Custom-styled scrollable region. |
| **Resizable** | `resizable` | Drag-to-resize panel layout (horizontal or vertical). |
| **Sidebar** | `sidebar` | Full-featured collapsible sidebar with groups and menus. |

### Card sub-components

```tsx
import {
  Card, CardHeader, CardTitle, CardDescription,
  CardContent, CardFooter
} from "@/components/ui/card"
```

### Sidebar sub-components

```tsx
import {
  Sidebar, SidebarContent, SidebarFooter, SidebarGroup,
  SidebarGroupContent, SidebarGroupLabel, SidebarHeader,
  SidebarInset, SidebarMenu, SidebarMenuBadge, SidebarMenuButton,
  SidebarMenuItem, SidebarMenuSub, SidebarMenuSubButton,
  SidebarMenuSubItem, SidebarProvider, SidebarRail, SidebarTrigger,
} from "@/components/ui/sidebar"
```

---

## Navigation

| Component | Install Name | Description |
|---|---|---|
| **Tabs** | `tabs` | Tabbed content panels. |
| **Navigation Menu** | `navigation-menu` | Full-featured navigation with dropdowns (for site headers). |
| **Breadcrumb** | `breadcrumb` | Breadcrumb trail navigation. |
| **Pagination** | `pagination` | Page number navigation with prev/next. |
| **Menubar** | `menubar` | Desktop-style application menu bar. |

### Tabs example

```tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

<Tabs defaultValue="account">
  <TabsList>
    <TabsTrigger value="account">Account</TabsTrigger>
    <TabsTrigger value="security">Security</TabsTrigger>
  </TabsList>
  <TabsContent value="account">Account settings</TabsContent>
  <TabsContent value="security">Security settings</TabsContent>
</Tabs>
```

---

## Overlays & Popovers

| Component | Install Name | Description |
|---|---|---|
| **Dialog** | `dialog` | Modal dialog with overlay. |
| **Alert Dialog** | `alert-dialog` | Confirmation dialog that interrupts the user. |
| **Sheet** | `sheet` | Slide-in panel from any edge (top, right, bottom, left). |
| **Drawer** | `drawer` | Mobile-friendly bottom drawer (built on Vaul). |
| **Popover** | `popover` | Floating non-modal panel anchored to a trigger. |
| **Hover Card** | `hover-card` | Rich tooltip shown on hover. |
| **Tooltip** | `tooltip` | Simple label shown on hover. |
| **Context Menu** | `context-menu` | Right-click context menu. |
| **Dropdown Menu** | `dropdown-menu` | Click-triggered dropdown menu. |
| **Command** | `command` | Command palette / combobox with search (use for ⌘K menus). |
| **Combobox** | — | Built from Command + Popover. See patterns.md. |

### Dialog example

```tsx
import {
  Dialog, DialogContent, DialogDescription,
  DialogFooter, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm Action</DialogTitle>
      <DialogDescription>This action cannot be undone.</DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button variant="destructive">Delete</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Dropdown Menu example

```tsx
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem,
  DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="outline">Options</Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuLabel>My Account</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuItem>Profile</DropdownMenuItem>
    <DropdownMenuItem>Settings</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem className="text-destructive">Log out</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

---

## Data Display

| Component | Install Name | Description |
|---|---|---|
| **Table** | `table` | Semantic HTML table with shadcn styling. |
| **Badge** | `badge` | Small label/tag. Variants: default, secondary, outline, destructive. |
| **Avatar** | `avatar` | User avatar with image and fallback initials. |
| **Calendar** | `calendar` | Date picker calendar (uses react-day-picker). |
| **Chart** | `chart` | Recharts wrapper with theming. Supports bar, line, area, pie, radar, radial. |
| **Carousel** | `carousel` | Embla-powered image/content carousel. |
| **Accordion** | `accordion` | Collapsible content sections. |
| **Collapsible** | `collapsible` | Single toggle show/hide section. |

### Badge example

```tsx
import { Badge } from "@/components/ui/badge"

<Badge>New</Badge>
<Badge variant="secondary">Beta</Badge>
<Badge variant="outline">Draft</Badge>
<Badge variant="destructive">Error</Badge>
```

### Avatar example

```tsx
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

<Avatar>
  <AvatarImage src="https://example.com/user.jpg" alt="Jane Doe" />
  <AvatarFallback>JD</AvatarFallback>
</Avatar>
```

### Chart example (bar chart)

```tsx
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { month: "Jan", sales: 186 },
  { month: "Feb", sales: 305 },
]
const config = {
  sales: { label: "Sales", color: "hsl(var(--chart-1))" },
}

<ChartContainer config={config} className="h-[200px]">
  <BarChart data={data}>
    <CartesianGrid vertical={false} />
    <XAxis dataKey="month" />
    <ChartTooltip content={<ChartTooltipContent />} />
    <Bar dataKey="sales" fill="var(--color-sales)" radius={4} />
  </BarChart>
</ChartContainer>
```

---

## Feedback & Status

| Component | Install Name | Description |
|---|---|---|
| **Alert** | `alert` | Inline status message. Variants: default, destructive. |
| **Progress** | `progress` | Linear progress bar (0–100). |
| **Skeleton** | `skeleton` | Loading placeholder. |
| **Sonner** | `sonner` | Toast notification system (replaces legacy Toast). |

### Alert example

```tsx
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Terminal } from "lucide-react"

<Alert>
  <Terminal className="h-4 w-4" />
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>You can customize your theme in settings.</AlertDescription>
</Alert>

<Alert variant="destructive">
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Your session has expired.</AlertDescription>
</Alert>
```

### Sonner toast setup

```tsx
// In root layout:
import { Toaster } from "@/components/ui/sonner"
<Toaster />

// Anywhere in your app:
import { toast } from "sonner"
toast("Event created!")
toast.success("Changes saved.")
toast.error("Something went wrong.")
toast.promise(saveData(), { loading: "Saving...", success: "Saved!", error: "Failed." })
```

---

## Typography

| Component | Install Name | Description |
|---|---|---|
| **Typography** | — | Not a component — shadcn ships prose styles you apply via className. |

### Prose typography classes

```tsx
<h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
  Page Title
</h1>
<h2 className="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0">
  Section
</h2>
<p className="leading-7 [&:not(:first-child)]:mt-6">Paragraph text.</p>
<p className="text-sm text-muted-foreground">Helper text</p>
<code className="relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm">code</code>
```

---

## Date Picker

Not a standalone component — compose from Calendar + Popover:

```bash
npx shadcn@latest add calendar popover button
npm install react-day-picker date-fns
```

```tsx
import * as React from "react"
import { format } from "date-fns"
import { CalendarIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { cn } from "@/lib/utils"

export function DatePicker() {
  const [date, setDate] = React.useState<Date>()
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline" className={cn("w-[240px] justify-start text-left font-normal", !date && "text-muted-foreground")}>
          <CalendarIcon className="mr-2 h-4 w-4" />
          {date ? format(date, "PPP") : <span>Pick a date</span>}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0">
        <Calendar mode="single" selected={date} onSelect={setDate} initialFocus />
      </PopoverContent>
    </Popover>
  )
}
```

---

## Icons

shadcn/ui uses **Lucide React** icons throughout:

```bash
npm install lucide-react
```

```tsx
import { Home, Settings, User, LogOut, ChevronRight, Search, Bell } from "lucide-react"

<Button size="icon" variant="ghost">
  <Bell className="h-4 w-4" />
</Button>
```

Browse icons at [lucide.dev](https://lucide.dev/icons/).
