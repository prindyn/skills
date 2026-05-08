#!/usr/bin/env bash
# Install one or more shadcn/ui components with dependency checks and helpful output.
#
# Usage:
#   bash scripts/add_components.sh button card input
#   bash scripts/add_components.sh --overwrite button dialog
#   bash scripts/add_components.sh --list
#   bash scripts/add_components.sh --bundle forms
#   bash scripts/add_components.sh --bundle dashboard

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $1"; }
info() { echo -e "${BLUE}ℹ${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }

OVERWRITE=""
BUNDLE=""
COMPONENTS=()

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --overwrite|-o) OVERWRITE="--overwrite"; shift ;;
    --list)
      echo ""
      echo "Available component bundles:"
      echo "  --bundle forms      : form input label button select checkbox textarea"
      echo "  --bundle nav        : tabs navigation-menu breadcrumb sidebar"
      echo "  --bundle overlays   : dialog sheet alert-dialog popover tooltip dropdown-menu"
      echo "  --bundle data       : table badge avatar card"
      echo "  --bundle feedback   : alert progress skeleton sonner"
      echo "  --bundle dashboard  : card badge avatar separator button sonner"
      echo "  --bundle auth       : card input label button form tabs"
      echo ""
      echo "Add all at once: npx shadcn@latest add --all"
      exit 0
      ;;
    --bundle|-b)
      BUNDLE="$2"
      shift 2
      ;;
    *) COMPONENTS+=("$1"); shift ;;
  esac
done

# Expand bundles
if [ -n "$BUNDLE" ]; then
  case "$BUNDLE" in
    forms)      COMPONENTS+=(form input label button select checkbox textarea switch slider) ;;
    nav)        COMPONENTS+=(tabs navigation-menu breadcrumb sidebar pagination menubar) ;;
    overlays)   COMPONENTS+=(dialog sheet alert-dialog popover tooltip dropdown-menu hover-card context-menu) ;;
    data)       COMPONENTS+=(table badge avatar card carousel accordion) ;;
    feedback)   COMPONENTS+=(alert progress skeleton sonner) ;;
    dashboard)  COMPONENTS+=(card badge avatar separator button sonner chart sidebar) ;;
    auth)       COMPONENTS+=(card input label button form tabs separator) ;;
    *)
      fail "Unknown bundle: $BUNDLE"
      echo "  Run with --list to see available bundles."
      exit 1
      ;;
  esac
fi

if [ ${#COMPONENTS[@]} -eq 0 ]; then
  echo "Usage: bash scripts/add_components.sh <component> [components...]"
  echo "       bash scripts/add_components.sh --bundle <bundle-name>"
  echo "       bash scripts/add_components.sh --list"
  exit 1
fi

# Check components.json exists
if [ ! -f "components.json" ]; then
  fail "components.json not found. Initialize shadcn first:"
  echo ""
  echo "  npx shadcn@latest init"
  echo ""
  exit 1
fi

# Check npx is available
if ! command -v npx &>/dev/null; then
  fail "npx not found. Please install Node.js 18+."
  exit 1
fi

echo ""
echo "Installing shadcn/ui components"
echo "================================"
info "Components: ${COMPONENTS[*]}"
if [ -n "$OVERWRITE" ]; then
  warn "Overwrite mode: existing component files will be replaced"
fi
echo ""

# Deduplicate
UNIQUE_COMPONENTS=($(echo "${COMPONENTS[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' '))

FAILED=()
for comp in "${UNIQUE_COMPONENTS[@]}"; do
  echo -n "  Adding $comp..."
  if npx shadcn@latest add "$comp" $OVERWRITE --yes 2>&1 | tail -1 | grep -qi "error\|not found\|invalid"; then
    echo ""
    warn "  '$comp' may have failed. Check output above."
    FAILED+=("$comp")
  else
    echo -e " ${GREEN}done${NC}"
  fi
done

echo ""
if [ ${#FAILED[@]} -eq 0 ]; then
  ok "All ${#UNIQUE_COMPONENTS[@]} component(s) installed successfully."
  echo ""
  info "Import from @/components/ui/<name>"
  echo "  Example: import { Button } from \"@/components/ui/button\""
else
  warn "${#FAILED[@]} component(s) may have issues: ${FAILED[*]}"
  echo "  Try running: npx shadcn@latest add ${FAILED[*]} --overwrite"
fi
echo ""
