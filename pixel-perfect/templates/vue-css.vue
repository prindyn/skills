<!--
  Pixel Perfect starter — Vue 3 SFC.

  Setup:
    1. Generate tokens.css from DESIGN.md:
         python scripts/extract_tokens.py DESIGN.md --format css > src/tokens.css
    2. Import once in main.ts: import './tokens.css';
    3. Use only var(--color-*), var(--space-*), var(--rounded-*) below.
    4. Run scripts/audit_pixels.py before shipping.
-->
<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}>();

const pressed = ref(false);
</script>

<template>
  <button
    class="btn"
    :class="[`btn--${variant ?? 'primary'}`]"
    :disabled="disabled"
    @mousedown="pressed = true"
    @mouseup="pressed = false"
    @mouseleave="pressed = false"
  >
    <slot />
  </button>
</template>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;                       /* 44pt touch target */
  padding: 12px var(--space-md);
  border: 0;
  border-radius: var(--rounded-sm);
  font: inherit;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 150ms cubic-bezier(0.2, 0, 0, 1);
}

.btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.btn:active {
  transform: translateY(1px);
}

.btn:disabled {
  cursor: not-allowed;
}

.btn--primary {
  background: var(--color-tertiary);
  color: #fff;
}
.btn--primary:hover { background: var(--color-primary); }
.btn--primary:disabled {
  background: var(--color-neutral);
  color: var(--color-secondary);
}

.btn--secondary {
  background: var(--color-neutral);
  color: var(--color-primary);
}
.btn--secondary:hover { background: color-mix(in srgb, var(--color-neutral), var(--color-primary) 8%); }
.btn--secondary:disabled { opacity: 0.5; }

@media (prefers-reduced-motion: reduce) {
  .btn { transition: none; }
  .btn:active { transform: none; }
}
</style>
