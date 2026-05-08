/**
 * Settings Page Template
 *
 * Install required components first:
 *   npx shadcn@latest add tabs card input label button switch select separator badge avatar
 *   npm install lucide-react react-hook-form zod @hookform/resolvers
 *
 * Features:
 *   - Tabbed layout: Profile, Account, Notifications, Appearance, Billing
 *   - Profile form with avatar upload area
 *   - Account security (password change, 2FA toggle, danger zone)
 *   - Notification preferences with granular switches
 *   - Appearance (theme, density, language)
 *   - Billing overview with plan badge
 *
 * Usage (Next.js App Router):
 *   // app/settings/page.tsx
 */

"use client"

import * as React from "react"
import { Bell, CreditCard, Moon, Palette, Shield, Sun, Upload, User } from "lucide-react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"

// ─── Schemas ─────────────────────────────────────────────────────────────────

const profileSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Enter a valid email"),
  username: z.string().min(3).max(20).regex(/^[a-z0-9_-]+$/, "Only lowercase letters, numbers, _ and -"),
  bio: z.string().max(160, "Bio must be under 160 characters").optional(),
  url: z.string().url("Enter a valid URL").optional().or(z.literal("")),
})

const passwordSchema = z.object({
  currentPassword: z.string().min(1, "Current password is required"),
  newPassword: z.string().min(8, "Password must be at least 8 characters"),
  confirmPassword: z.string(),
}).refine((d) => d.newPassword === d.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
})

type ProfileValues = z.infer<typeof profileSchema>
type PasswordValues = z.infer<typeof passwordSchema>

// ─── Profile Tab ─────────────────────────────────────────────────────────────

function ProfileTab() {
  const form = useForm<ProfileValues>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      name: "Jane Doe",
      email: "jane@example.com",
      username: "janedoe",
      bio: "Product designer & developer. Building things on the internet.",
      url: "https://janedoe.com",
    },
  })

  function onSubmit(values: ProfileValues) {
    // TODO: call your profile update API
    console.log("Profile update:", values)
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Profile</CardTitle>
          <CardDescription>This information will be displayed publicly.</CardDescription>
        </CardHeader>
        <CardContent>
          {/* Avatar */}
          <div className="flex items-center gap-4 mb-6">
            <Avatar className="h-16 w-16">
              <AvatarImage src="/avatars/jane.jpg" alt="Jane Doe" />
              <AvatarFallback className="text-lg">JD</AvatarFallback>
            </Avatar>
            <div className="space-y-1">
              <Button variant="outline" size="sm" className="gap-1">
                <Upload className="h-3.5 w-3.5" /> Change photo
              </Button>
              <p className="text-xs text-muted-foreground">JPG, GIF, PNG — max 2 MB</p>
            </div>
          </div>

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <FormField control={form.control} name="name" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Full Name</FormLabel>
                    <FormControl><Input {...field} /></FormControl>
                    <FormMessage />
                  </FormItem>
                )} />
                <FormField control={form.control} name="username" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Username</FormLabel>
                    <FormControl>
                      <div className="flex">
                        <span className="flex items-center px-3 border border-r-0 rounded-l-md bg-muted text-muted-foreground text-sm">@</span>
                        <Input className="rounded-l-none" {...field} />
                      </div>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )} />
              </div>

              <FormField control={form.control} name="email" render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl><Input type="email" {...field} /></FormControl>
                  <FormDescription>Used for notifications and sign-in.</FormDescription>
                  <FormMessage />
                </FormItem>
              )} />

              <FormField control={form.control} name="bio" render={({ field }) => (
                <FormItem>
                  <FormLabel>Bio</FormLabel>
                  <FormControl><Textarea rows={3} placeholder="Tell us a bit about yourself..." {...field} /></FormControl>
                  <FormDescription>{(field.value?.length ?? 0)}/160 characters</FormDescription>
                  <FormMessage />
                </FormItem>
              )} />

              <FormField control={form.control} name="url" render={({ field }) => (
                <FormItem>
                  <FormLabel>Website</FormLabel>
                  <FormControl><Input placeholder="https://example.com" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />

              <div className="flex justify-end">
                <Button type="submit">Save changes</Button>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  )
}

// ─── Account / Security Tab ───────────────────────────────────────────────────

function AccountTab() {
  const [twoFAEnabled, setTwoFAEnabled] = React.useState(false)
  const form = useForm<PasswordValues>({
    resolver: zodResolver(passwordSchema),
    defaultValues: { currentPassword: "", newPassword: "", confirmPassword: "" },
  })

  function onPasswordSubmit(values: PasswordValues) {
    // TODO: call password change API
    console.log("Password change:", values)
    form.reset()
  }

  return (
    <div className="space-y-6">
      {/* Password */}
      <Card>
        <CardHeader>
          <CardTitle>Change Password</CardTitle>
          <CardDescription>Choose a strong password you don't use elsewhere.</CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onPasswordSubmit)} className="space-y-4">
              <FormField control={form.control} name="currentPassword" render={({ field }) => (
                <FormItem>
                  <FormLabel>Current Password</FormLabel>
                  <FormControl><Input type="password" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />
              <FormField control={form.control} name="newPassword" render={({ field }) => (
                <FormItem>
                  <FormLabel>New Password</FormLabel>
                  <FormControl><Input type="password" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />
              <FormField control={form.control} name="confirmPassword" render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirm New Password</FormLabel>
                  <FormControl><Input type="password" {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />
              <div className="flex justify-end">
                <Button type="submit">Update password</Button>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>

      {/* Two-factor auth */}
      <Card>
        <CardHeader>
          <CardTitle>Two-Factor Authentication</CardTitle>
          <CardDescription>Add an extra layer of security to your account.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <Label>Authenticator App</Label>
              <p className="text-sm text-muted-foreground">
                Use an authenticator app to generate one-time codes.
              </p>
            </div>
            <Switch
              checked={twoFAEnabled}
              onCheckedChange={setTwoFAEnabled}
              aria-label="Enable two-factor authentication"
            />
          </div>
        </CardContent>
      </Card>

      {/* Danger zone */}
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="text-destructive">Danger Zone</CardTitle>
          <CardDescription>These actions are irreversible. Please proceed carefully.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between rounded-md border p-4">
            <div>
              <p className="font-medium text-sm">Delete Account</p>
              <p className="text-sm text-muted-foreground">Permanently delete your account and all data.</p>
            </div>
            <Button variant="destructive" size="sm">Delete</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// ─── Notifications Tab ────────────────────────────────────────────────────────

const notificationGroups = [
  {
    title: "Email Notifications",
    items: [
      { id: "email-marketing", label: "Product updates", description: "News, announcements and product updates." },
      { id: "email-orders", label: "Order activity", description: "Confirmations, receipts and updates on orders." },
      { id: "email-security", label: "Security alerts", description: "Sign-in from new devices, password changes." },
    ],
  },
  {
    title: "Push Notifications",
    items: [
      { id: "push-messages", label: "Direct messages", description: "Notify when someone sends you a message." },
      { id: "push-mentions", label: "Mentions", description: "Notify when someone mentions you." },
    ],
  },
]

function NotificationsTab() {
  const [prefs, setPrefs] = React.useState<Record<string, boolean>>({
    "email-marketing": true,
    "email-orders": true,
    "email-security": true,
    "push-messages": false,
    "push-mentions": true,
  })

  return (
    <div className="space-y-6">
      {notificationGroups.map((group) => (
        <Card key={group.title}>
          <CardHeader>
            <CardTitle className="text-base">{group.title}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {group.items.map((item, idx) => (
              <React.Fragment key={item.id}>
                {idx > 0 && <Separator />}
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor={item.id}>{item.label}</Label>
                    <p className="text-sm text-muted-foreground">{item.description}</p>
                  </div>
                  <Switch
                    id={item.id}
                    checked={prefs[item.id] ?? false}
                    onCheckedChange={(v) => setPrefs((p) => ({ ...p, [item.id]: v }))}
                  />
                </div>
              </React.Fragment>
            ))}
          </CardContent>
          <CardFooter className="justify-end">
            <Button variant="outline" size="sm">Save preferences</Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}

// ─── Appearance Tab ───────────────────────────────────────────────────────────

function AppearanceTab() {
  const [theme, setTheme] = React.useState<"light" | "dark" | "system">("system")
  const [density, setDensity] = React.useState("comfortable")
  const [language, setLanguage] = React.useState("en")

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Theme</CardTitle>
          <CardDescription>Select the color scheme for the interface.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-3">
            {(["light", "dark", "system"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTheme(t)}
                className={`flex flex-col items-center gap-2 rounded-lg border p-4 text-sm transition-colors hover:bg-accent ${
                  theme === t ? "border-primary bg-accent" : "border-border"
                }`}
              >
                {t === "light" && <Sun className="h-5 w-5" />}
                {t === "dark" && <Moon className="h-5 w-5" />}
                {t === "system" && <Palette className="h-5 w-5" />}
                <span className="capitalize">{t}</span>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Preferences</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-2">
            <Label>Interface density</Label>
            <Select value={density} onValueChange={setDensity}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="compact">Compact</SelectItem>
                <SelectItem value="comfortable">Comfortable</SelectItem>
                <SelectItem value="spacious">Spacious</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid gap-2">
            <Label>Language</Label>
            <Select value={language} onValueChange={setLanguage}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="en">English</SelectItem>
                <SelectItem value="es">Español</SelectItem>
                <SelectItem value="fr">Français</SelectItem>
                <SelectItem value="de">Deutsch</SelectItem>
                <SelectItem value="ja">日本語</SelectItem>
                <SelectItem value="zh">中文</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
        <CardFooter className="justify-end">
          <Button variant="outline" size="sm">Save preferences</Button>
        </CardFooter>
      </Card>
    </div>
  )
}

// ─── Billing Tab ──────────────────────────────────────────────────────────────

function BillingTab() {
  return (
    <div className="space-y-6">
      {/* Current plan */}
      <Card>
        <CardHeader className="flex flex-row items-start justify-between">
          <div>
            <CardTitle>Current Plan</CardTitle>
            <CardDescription>You are on the Pro plan.</CardDescription>
          </div>
          <Badge>Pro</Badge>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="rounded-md bg-muted p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Monthly cost</span>
              <span className="font-medium">$49/month</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Next billing date</span>
              <span className="font-medium">June 15, 2026</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Seats included</span>
              <span className="font-medium">10 seats</span>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">Manage Plan</Button>
            <Button variant="ghost" size="sm" className="text-destructive hover:text-destructive">Cancel Subscription</Button>
          </div>
        </CardContent>
      </Card>

      {/* Payment method */}
      <Card>
        <CardHeader>
          <CardTitle>Payment Method</CardTitle>
          <CardDescription>Update your billing details.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-3 rounded-md border p-4">
            <CreditCard className="h-5 w-5 text-muted-foreground" />
            <div>
              <p className="text-sm font-medium">Visa ending in 4242</p>
              <p className="text-xs text-muted-foreground">Expires 12/2027</p>
            </div>
            <Button variant="outline" size="sm" className="ml-auto">Update</Button>
          </div>
        </CardContent>
      </Card>

      {/* Invoices */}
      <Card>
        <CardHeader>
          <CardTitle>Billing History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {[
              { date: "May 15, 2026", amount: "$49.00", status: "Paid" },
              { date: "Apr 15, 2026", amount: "$49.00", status: "Paid" },
              { date: "Mar 15, 2026", amount: "$49.00", status: "Paid" },
            ].map((inv) => (
              <div key={inv.date} className="flex items-center justify-between text-sm py-2 border-b last:border-0">
                <span className="text-muted-foreground">{inv.date}</span>
                <span className="font-medium">{inv.amount}</span>
                <Badge variant="outline" className="text-emerald-600 border-emerald-200">{inv.status}</Badge>
                <Button variant="ghost" size="sm">Download</Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// ─── Page ────────────────────────────────────────────────────────────────────

export default function SettingsPage() {
  return (
    <div className="container mx-auto py-8 max-w-3xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">Manage your account settings and preferences.</p>
      </div>

      <Tabs defaultValue="profile">
        <TabsList className="mb-6 w-full sm:w-auto">
          <TabsTrigger value="profile" className="gap-1.5"><User className="h-4 w-4" />Profile</TabsTrigger>
          <TabsTrigger value="account" className="gap-1.5"><Shield className="h-4 w-4" />Account</TabsTrigger>
          <TabsTrigger value="notifications" className="gap-1.5"><Bell className="h-4 w-4" />Notifications</TabsTrigger>
          <TabsTrigger value="appearance" className="gap-1.5"><Palette className="h-4 w-4" />Appearance</TabsTrigger>
          <TabsTrigger value="billing" className="gap-1.5"><CreditCard className="h-4 w-4" />Billing</TabsTrigger>
        </TabsList>

        <TabsContent value="profile"><ProfileTab /></TabsContent>
        <TabsContent value="account"><AccountTab /></TabsContent>
        <TabsContent value="notifications"><NotificationsTab /></TabsContent>
        <TabsContent value="appearance"><AppearanceTab /></TabsContent>
        <TabsContent value="billing"><BillingTab /></TabsContent>
      </Tabs>
    </div>
  )
}
