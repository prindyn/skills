/**
 * Dashboard Layout Template
 *
 * Install required components first:
 *   npx shadcn@latest add sidebar card badge avatar separator button sonner chart
 *   npm install lucide-react recharts
 *
 * Features:
 *   - Collapsible sidebar with navigation groups
 *   - Header with search, notifications, and user menu
 *   - Stats cards grid
 *   - Area chart (monthly revenue)
 *   - Recent activity feed
 *   - Responsive (sidebar collapses to icon rail on mobile)
 *
 * Usage (Next.js App Router):
 *   // app/dashboard/layout.tsx  ← use this component as a layout wrapper
 *   // app/dashboard/page.tsx    ← or render directly as a page
 */

"use client"

import * as React from "react"
import {
  AreaChart, Area, CartesianGrid, XAxis, ResponsiveContainer,
} from "recharts"
import {
  BarChart3, Bell, ChevronDown, Home, LayoutDashboard,
  LogOut, Settings, ShoppingCart, TrendingDown, TrendingUp,
  Users, Search, Package, FileText, HelpCircle, Moon, Sun,
} from "lucide-react"

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  ChartContainer, ChartTooltip, ChartTooltipContent,
} from "@/components/ui/chart"
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem,
  DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import {
  Sidebar, SidebarContent, SidebarFooter, SidebarGroup,
  SidebarGroupContent, SidebarGroupLabel, SidebarHeader,
  SidebarInset, SidebarMenu, SidebarMenuBadge, SidebarMenuButton,
  SidebarMenuItem, SidebarProvider, SidebarRail, SidebarTrigger,
} from "@/components/ui/sidebar"

// ─── Mock data ──────────────────────────────────────────────────────────────

const revenueData = [
  { month: "Jan", revenue: 18600 },
  { month: "Feb", revenue: 23050 },
  { month: "Mar", revenue: 19800 },
  { month: "Apr", revenue: 31200 },
  { month: "May", revenue: 28700 },
  { month: "Jun", revenue: 35400 },
  { month: "Jul", revenue: 42100 },
  { month: "Aug", revenue: 38600 },
]

const chartConfig = {
  revenue: { label: "Revenue", color: "hsl(var(--chart-1))" },
}

const stats = [
  { title: "Total Revenue", value: "$45,231", change: "+20.1%", trend: "up" as const, icon: BarChart3 },
  { title: "Active Users", value: "2,350", change: "+15.3%", trend: "up" as const, icon: Users },
  { title: "New Orders", value: "1,247", change: "-4.5%", trend: "down" as const, icon: ShoppingCart },
  { title: "Products", value: "573", change: "+8.2%", trend: "up" as const, icon: Package },
]

const recentActivity = [
  { user: "Alice Johnson", action: "placed an order", amount: "$124.00", time: "2 min ago", avatar: "AJ" },
  { user: "Bob Chen", action: "signed up", amount: null, time: "14 min ago", avatar: "BC" },
  { user: "Carol Smith", action: "upgraded to Pro", amount: "$49/mo", time: "1 hr ago", avatar: "CS" },
  { user: "David Kim", action: "submitted a refund", amount: "$89.00", time: "3 hr ago", avatar: "DK" },
  { user: "Eva Martinez", action: "placed an order", amount: "$342.00", time: "5 hr ago", avatar: "EM" },
]

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard", href: "/dashboard", badge: null },
  { icon: Users, label: "Users", href: "/users", badge: null },
  { icon: ShoppingCart, label: "Orders", href: "/orders", badge: "12" },
  { icon: Package, label: "Products", href: "/products", badge: null },
  { icon: FileText, label: "Reports", href: "/reports", badge: null },
]

const navSecondary = [
  { icon: Settings, label: "Settings", href: "/settings" },
  { icon: HelpCircle, label: "Help & Support", href: "/help" },
]

// ─── Sidebar Component ───────────────────────────────────────────────────────

function AppSidebar() {
  return (
    <Sidebar variant="inset">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="/dashboard">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                  <Home className="size-4" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-semibold">Acme Corp</span>
                  <span className="text-xs text-muted-foreground">Dashboard</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Main</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navItems.map((item) => (
                <SidebarMenuItem key={item.label}>
                  <SidebarMenuButton asChild tooltip={item.label}>
                    <a href={item.href}>
                      <item.icon />
                      <span>{item.label}</span>
                    </a>
                  </SidebarMenuButton>
                  {item.badge && (
                    <SidebarMenuBadge>{item.badge}</SidebarMenuBadge>
                  )}
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup className="mt-auto">
          <SidebarGroupContent>
            <SidebarMenu>
              {navSecondary.map((item) => (
                <SidebarMenuItem key={item.label}>
                  <SidebarMenuButton asChild tooltip={item.label}>
                    <a href={item.href}>
                      <item.icon />
                      <span>{item.label}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuButton size="lg">
                  <Avatar className="size-8">
                    <AvatarImage src="/avatars/user.jpg" alt="Jane Doe" />
                    <AvatarFallback>JD</AvatarFallback>
                  </Avatar>
                  <div className="flex flex-col gap-0.5 leading-none">
                    <span className="font-semibold">Jane Doe</span>
                    <span className="text-xs text-muted-foreground">jane@acme.com</span>
                  </div>
                  <ChevronDown className="ml-auto size-4" />
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent side="top" className="w-[--radix-popper-anchor-width]">
                <DropdownMenuLabel>My Account</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem><Settings className="mr-2 size-4" />Settings</DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="text-destructive">
                  <LogOut className="mr-2 size-4" />Log out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  )
}

// ─── Main Dashboard Page ─────────────────────────────────────────────────────

export default function DashboardPage() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        {/* Header */}
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />

          <div className="flex flex-1 items-center gap-2">
            <div className="relative flex-1 max-w-sm">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input placeholder="Search..." className="pl-8 bg-muted/50" />
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" className="relative">
              <Bell className="h-4 w-4" />
              <span className="absolute top-1.5 right-1.5 flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary" />
              </span>
            </Button>
          </div>
        </header>

        {/* Page content */}
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          <div className="pt-4">
            <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
            <p className="text-muted-foreground">Welcome back, Jane. Here's what's happening.</p>
          </div>

          {/* Stats grid */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {stats.map((stat) => (
              <Card key={stat.title}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">
                    {stat.title}
                  </CardTitle>
                  <stat.icon className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <div className="flex items-center gap-1 mt-1">
                    {stat.trend === "up" ? (
                      <TrendingUp className="h-3 w-3 text-emerald-500" />
                    ) : (
                      <TrendingDown className="h-3 w-3 text-red-500" />
                    )}
                    <p className={`text-xs ${stat.trend === "up" ? "text-emerald-600" : "text-red-600"}`}>
                      {stat.change} from last month
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Chart + Activity */}
          <div className="grid gap-4 lg:grid-cols-7">
            {/* Revenue chart */}
            <Card className="lg:col-span-4">
              <CardHeader>
                <CardTitle>Revenue</CardTitle>
                <CardDescription>Monthly revenue for the current year</CardDescription>
              </CardHeader>
              <CardContent>
                <ChartContainer config={chartConfig} className="h-[220px] w-full">
                  <AreaChart data={revenueData}>
                    <defs>
                      <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="var(--color-revenue)" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="var(--color-revenue)" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="month" tickLine={false} axisLine={false} tickMargin={8} />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <Area
                      type="monotone"
                      dataKey="revenue"
                      stroke="var(--color-revenue)"
                      strokeWidth={2}
                      fill="url(#colorRevenue)"
                    />
                  </AreaChart>
                </ChartContainer>
              </CardContent>
            </Card>

            {/* Recent activity */}
            <Card className="lg:col-span-3">
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
                <CardDescription>Latest events across your platform</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentActivity.map((item, i) => (
                    <div key={i} className="flex items-center gap-3">
                      <Avatar className="h-8 w-8">
                        <AvatarFallback className="text-xs">{item.avatar}</AvatarFallback>
                      </Avatar>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium leading-none truncate">
                          {item.user}
                        </p>
                        <p className="text-xs text-muted-foreground mt-0.5">
                          {item.action}
                          {item.amount && (
                            <span className="font-medium text-foreground"> · {item.amount}</span>
                          )}
                        </p>
                      </div>
                      <span className="text-xs text-muted-foreground whitespace-nowrap">
                        {item.time}
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}
