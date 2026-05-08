/**
 * Data Table Page Template
 *
 * Install required components first:
 *   npx shadcn@latest add table button input badge dropdown-menu select dialog form label
 *   npm install @tanstack/react-table lucide-react
 *
 * Features:
 *   - Full TanStack Table v8 integration
 *   - Column sorting (click headers)
 *   - Global search filter
 *   - Column visibility toggle
 *   - Row selection with bulk actions
 *   - Pagination with page size control
 *   - Status badge rendering
 *   - Row action dropdown
 *   - Empty state
 *
 * Usage:
 *   Replace the `User` type and `sampleData` with your actual data and types.
 *   Wire `onDelete`, `onEdit` to your mutation logic.
 */

"use client"

import * as React from "react"
import {
  ColumnDef, ColumnFiltersState, SortingState, VisibilityState,
  flexRender, getCoreRowModel, getFilteredRowModel,
  getPaginationRowModel, getSortedRowModel, useReactTable,
  Row,
} from "@tanstack/react-table"
import {
  ArrowUpDown, ChevronDown, ChevronLeft, ChevronRight,
  MoreHorizontal, Plus, Search, Trash2, UserCheck,
} from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  DropdownMenu, DropdownMenuCheckboxItem, DropdownMenuContent,
  DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from "@/components/ui/select"
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table"

// ─── Types ───────────────────────────────────────────────────────────────────

type UserStatus = "active" | "inactive" | "pending" | "suspended"

interface User {
  id: string
  name: string
  email: string
  role: string
  status: UserStatus
  joinedAt: string
  lastActive: string
}

// ─── Sample data ─────────────────────────────────────────────────────────────

const sampleData: User[] = [
  { id: "u1", name: "Alice Johnson", email: "alice@example.com", role: "Admin", status: "active", joinedAt: "2024-01-12", lastActive: "Today" },
  { id: "u2", name: "Bob Chen", email: "bob@example.com", role: "Developer", status: "active", joinedAt: "2024-02-03", lastActive: "2 days ago" },
  { id: "u3", name: "Carol Smith", email: "carol@example.com", role: "Designer", status: "inactive", joinedAt: "2024-03-15", lastActive: "1 week ago" },
  { id: "u4", name: "David Kim", email: "david@example.com", role: "Developer", status: "pending", joinedAt: "2024-04-28", lastActive: "Never" },
  { id: "u5", name: "Eva Martinez", email: "eva@example.com", role: "Manager", status: "active", joinedAt: "2023-11-05", lastActive: "Yesterday" },
  { id: "u6", name: "Frank Liu", email: "frank@example.com", role: "Developer", status: "suspended", joinedAt: "2023-09-20", lastActive: "3 months ago" },
  { id: "u7", name: "Grace Park", email: "grace@example.com", role: "Designer", status: "active", joinedAt: "2024-06-01", lastActive: "Today" },
  { id: "u8", name: "Henry Wang", email: "henry@example.com", role: "Developer", status: "active", joinedAt: "2024-05-14", lastActive: "Today" },
]

// ─── Status helpers ──────────────────────────────────────────────────────────

const statusVariant: Record<UserStatus, "default" | "secondary" | "outline" | "destructive"> = {
  active: "default",
  inactive: "secondary",
  pending: "outline",
  suspended: "destructive",
}

const statusLabel: Record<UserStatus, string> = {
  active: "Active",
  inactive: "Inactive",
  pending: "Pending",
  suspended: "Suspended",
}

// ─── Column definitions ──────────────────────────────────────────────────────

function buildColumns(
  onEdit: (user: User) => void,
  onDelete: (user: User) => void,
): ColumnDef<User>[] {
  return [
    {
      id: "select",
      header: ({ table }) => (
        <Checkbox
          checked={table.getIsAllPageRowsSelected() || (table.getIsSomePageRowsSelected() && "indeterminate")}
          onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
          aria-label="Select all"
        />
      ),
      cell: ({ row }) => (
        <Checkbox
          checked={row.getIsSelected()}
          onCheckedChange={(value) => row.toggleSelected(!!value)}
          aria-label="Select row"
        />
      ),
      enableSorting: false,
      enableHiding: false,
    },
    {
      accessorKey: "name",
      header: ({ column }) => (
        <Button variant="ghost" className="-ml-3" onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}>
          Name <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      ),
      cell: ({ row }) => (
        <div>
          <p className="font-medium leading-none">{row.getValue("name")}</p>
          <p className="text-xs text-muted-foreground mt-0.5">{row.original.email}</p>
        </div>
      ),
    },
    {
      accessorKey: "role",
      header: "Role",
      cell: ({ row }) => <span className="text-sm">{row.getValue("role")}</span>,
    },
    {
      accessorKey: "status",
      header: "Status",
      cell: ({ row }) => {
        const status = row.getValue("status") as UserStatus
        return (
          <Badge variant={statusVariant[status]}>
            {statusLabel[status]}
          </Badge>
        )
      },
      filterFn: (row, id, value) => value.includes(row.getValue(id)),
    },
    {
      accessorKey: "joinedAt",
      header: ({ column }) => (
        <Button variant="ghost" className="-ml-3" onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}>
          Joined <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      ),
    },
    {
      accessorKey: "lastActive",
      header: "Last Active",
      cell: ({ row }) => (
        <span className="text-sm text-muted-foreground">{row.getValue("lastActive")}</span>
      ),
    },
    {
      id: "actions",
      enableHiding: false,
      cell: ({ row }) => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon">
              <MoreHorizontal className="h-4 w-4" />
              <span className="sr-only">Row actions</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DropdownMenuItem onClick={() => navigator.clipboard.writeText(row.original.id)}>
              Copy user ID
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => onEdit(row.original)}>Edit user</DropdownMenuItem>
            <DropdownMenuItem
              className="text-destructive focus:text-destructive"
              onClick={() => onDelete(row.original)}
            >
              Delete user
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ]
}

// ─── Toolbar ─────────────────────────────────────────────────────────────────

interface ToolbarProps {
  table: ReturnType<typeof useReactTable<User>>
  selectedCount: number
  onBulkDelete: () => void
}

function Toolbar({ table, selectedCount, onBulkDelete }: ToolbarProps) {
  return (
    <div className="flex items-center gap-2">
      <div className="relative flex-1 max-w-sm">
        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search users..."
          value={(table.getColumn("name")?.getFilterValue() as string) ?? ""}
          onChange={(e) => table.getColumn("name")?.setFilterValue(e.target.value)}
          className="pl-8"
        />
      </div>

      {selectedCount > 0 && (
        <Button variant="destructive" size="sm" onClick={onBulkDelete} className="gap-1">
          <Trash2 className="h-3.5 w-3.5" />
          Delete ({selectedCount})
        </Button>
      )}

      <div className="ml-auto flex items-center gap-2">
        {/* Column visibility */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" size="sm" className="gap-1">
              Columns <ChevronDown className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {table.getAllColumns()
              .filter((col) => col.getCanHide())
              .map((col) => (
                <DropdownMenuCheckboxItem
                  key={col.id}
                  className="capitalize"
                  checked={col.getIsVisible()}
                  onCheckedChange={(value) => col.toggleVisibility(!!value)}
                >
                  {col.id}
                </DropdownMenuCheckboxItem>
              ))}
          </DropdownMenuContent>
        </DropdownMenu>

        <Button size="sm" className="gap-1">
          <Plus className="h-4 w-4" /> Invite User
        </Button>
      </div>
    </div>
  )
}

// ─── Pagination ──────────────────────────────────────────────────────────────

function Pagination({ table }: { table: ReturnType<typeof useReactTable<User>> }) {
  const { pageIndex, pageSize } = table.getState().pagination
  const totalRows = table.getFilteredRowModel().rows.length
  const from = pageIndex * pageSize + 1
  const to = Math.min((pageIndex + 1) * pageSize, totalRows)

  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <span>{table.getFilteredSelectedRowModel().rows.length} of {totalRows} row(s) selected</span>
        <span>·</span>
        <span>Showing {from}–{to} of {totalRows}</span>
      </div>

      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1">
          <span className="text-sm text-muted-foreground">Rows per page</span>
          <Select
            value={String(pageSize)}
            onValueChange={(v) => table.setPageSize(Number(v))}
          >
            <SelectTrigger className="h-8 w-[64px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {[10, 20, 50, 100].map((n) => (
                <SelectItem key={n} value={String(n)}>{n}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="flex gap-1">
          <Button variant="outline" size="icon" className="h-8 w-8" onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon" className="h-8 w-8" onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}

// ─── Page ────────────────────────────────────────────────────────────────────

export default function UsersPage() {
  const [data] = React.useState<User[]>(sampleData)
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = React.useState({})

  function handleEdit(user: User) {
    // TODO: open an edit sheet/dialog
    console.log("Edit:", user)
  }

  function handleDelete(user: User) {
    // TODO: show confirmation dialog, call delete mutation
    console.log("Delete:", user)
  }

  function handleBulkDelete() {
    const ids = table.getFilteredSelectedRowModel().rows.map((r) => r.original.id)
    // TODO: call bulk delete mutation
    console.log("Bulk delete:", ids)
    setRowSelection({})
  }

  const columns = React.useMemo(() => buildColumns(handleEdit, handleDelete), [])

  const table = useReactTable({
    data,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    state: { sorting, columnFilters, columnVisibility, rowSelection },
    initialState: { pagination: { pageSize: 10 } },
  })

  return (
    <div className="container mx-auto py-8 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Users</h1>
          <p className="text-muted-foreground">Manage your team members and their permissions.</p>
        </div>
        <Badge variant="secondary" className="gap-1">
          <UserCheck className="h-3 w-3" />
          {sampleData.filter((u) => u.status === "active").length} active
        </Badge>
      </div>

      <Toolbar
        table={table}
        selectedCount={table.getFilteredSelectedRowModel().rows.length}
        onBulkDelete={handleBulkDelete}
      />

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((hg) => (
              <TableRow key={hg.id}>
                {hg.headers.map((header) => (
                  <TableHead key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(header.column.columnDef.header, header.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id} data-state={row.getIsSelected() && "selected"}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className="h-32 text-center">
                  <div className="flex flex-col items-center gap-2 text-muted-foreground">
                    <UserCheck className="h-8 w-8 opacity-40" />
                    <p>No users found.</p>
                    <Button variant="outline" size="sm">
                      <Plus className="mr-1 h-4 w-4" /> Invite your first user
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      <Pagination table={table} />
    </div>
  )
}
