#!/usr/bin/env bash
# Checks whether shadcn/ui is initialized in the current project.
# Exits 0 if setup looks good, 1 if not.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
info() { echo -e "${BLUE}ℹ${NC} $1"; }

ISSUES=0

echo ""
echo "shadcn/ui project check"
echo "========================"
echo ""

# 1. Check components.json
if [ -f "components.json" ]; then
  ok "components.json found"

  # Extract style
  if command -v jq &>/dev/null; then
    STYLE=$(jq -r '.style // "unknown"' components.json)
    BASE_COLOR=$(jq -r '.tailwind.baseColor // "unknown"' components.json)
    CSS_VARS=$(jq -r '.tailwind.cssVariables // false' components.json)
    UI_ALIAS=$(jq -r '.aliases.ui // "@/components/ui"' components.json)
    info "  Style: $STYLE | Base color: $BASE_COLOR | CSS variables: $CSS_VARS"
    info "  Components install to: $UI_ALIAS"
  else
    warn "  Install jq for detailed config info: brew install jq"
  fi
else
  fail "components.json not found — shadcn is not initialized"
  echo ""
  echo "  Run: npx shadcn@latest init"
  echo ""
  ISSUES=$((ISSUES + 1))
fi

# 2. Check package.json exists
if [ -f "package.json" ]; then
  ok "package.json found"

  # Check for required dependencies
  if command -v node &>/dev/null; then
    node -e "
      const pkg = require('./package.json');
      const deps = { ...pkg.dependencies, ...pkg.devDependencies };
      const checks = [
        ['tailwindcss', 'Tailwind CSS'],
        ['react', 'React'],
      ];
      checks.forEach(([name, label]) => {
        if (deps[name]) {
          console.log('\x1b[32m✓\x1b[0m ' + label + ' (' + deps[name] + ')');
        } else {
          console.log('\x1b[33m⚠\x1b[0m  ' + label + ' not found in dependencies');
        }
      });
      // Check shadcn component dependencies
      const shadcnDeps = ['class-variance-authority', 'clsx', 'tailwind-merge'];
      const missing = shadcnDeps.filter(d => !deps[d]);
      if (missing.length === 0) {
        console.log('\x1b[32m✓\x1b[0m shadcn utility packages (cva, clsx, tailwind-merge)');
      } else {
        console.log('\x1b[33m⚠\x1b[0m  Missing: ' + missing.join(', '));
      }
    " 2>/dev/null || warn "  Could not parse package.json with Node"
  fi
else
  fail "package.json not found — not a Node.js project"
  ISSUES=$((ISSUES + 1))
fi

# 3. Check lib/utils.ts
UTILS_PATHS=("src/lib/utils.ts" "lib/utils.ts" "app/lib/utils.ts")
UTILS_FOUND=false
for p in "${UTILS_PATHS[@]}"; do
  if [ -f "$p" ]; then
    ok "Utils found at: $p"
    UTILS_FOUND=true
    break
  fi
done
if [ "$UTILS_FOUND" = false ]; then
  warn "lib/utils.ts not found (expected at src/lib/utils.ts or lib/utils.ts)"
  warn "  Run: npx shadcn@latest init to create it"
fi

# 4. Check components/ui directory
UI_PATHS=("src/components/ui" "components/ui" "app/components/ui")
UI_FOUND=false
for p in "${UI_PATHS[@]}"; do
  if [ -d "$p" ]; then
    COUNT=$(ls "$p" 2>/dev/null | wc -l | tr -d ' ')
    ok "UI components directory: $p ($COUNT files)"
    UI_FOUND=true
    break
  fi
done
if [ "$UI_FOUND" = false ]; then
  info "No components installed yet — run: npx shadcn@latest add button"
fi

# 5. Check Tailwind config
TAILWIND_CONFIGS=("tailwind.config.ts" "tailwind.config.js" "tailwind.config.mjs")
TW_FOUND=false
for p in "${TAILWIND_CONFIGS[@]}"; do
  if [ -f "$p" ]; then
    ok "Tailwind config: $p"
    TW_FOUND=true
    break
  fi
done
if [ "$TW_FOUND" = false ]; then
  fail "tailwind.config.ts not found"
  warn "  shadcn/ui requires Tailwind CSS. Install: npm install -D tailwindcss && npx tailwindcss init"
  ISSUES=$((ISSUES + 1))
fi

# 6. Check globals.css for CSS variables
CSS_PATHS=("app/globals.css" "src/app/globals.css" "src/styles/globals.css" "styles/globals.css" "src/index.css")
for p in "${CSS_PATHS[@]}"; do
  if [ -f "$p" ]; then
    if grep -q "\-\-background" "$p" 2>/dev/null; then
      ok "CSS variables found in: $p"
    else
      warn "CSS variables not found in $p — theming may not work"
      warn "  Run: npx shadcn@latest init to add them"
    fi
    break
  fi
done

# 7. Node version check
if command -v node &>/dev/null; then
  NODE_VER=$(node --version)
  NODE_MAJOR=$(echo "$NODE_VER" | sed 's/v\([0-9]*\).*/\1/')
  if [ "$NODE_MAJOR" -ge 18 ]; then
    ok "Node.js $NODE_VER (meets requirement ≥18)"
  else
    fail "Node.js $NODE_VER is too old. shadcn requires Node.js 18+"
    ISSUES=$((ISSUES + 1))
  fi
fi

echo ""
if [ "$ISSUES" -eq 0 ]; then
  echo -e "${GREEN}Project looks ready for shadcn/ui!${NC}"
  echo ""
  echo "Add components with: npx shadcn@latest add <component>"
  echo "Browse components:   https://ui.shadcn.com/docs/components"
  exit 0
else
  echo -e "${RED}Found $ISSUES issue(s). See above for details.${NC}"
  exit 1
fi
