---
name: figma-css-cleanup
description: >
  Audit and simplify CSS exported from Figma or visual builders without changing rendered
  behavior. Use when the user asks to clean generated CSS, remove redundant declarations, or
  reduce style noise while preserving layout, browser resets, responsive states, and variants.
---

## CSS Hygiene For Generated Designs

**Core Principles:**

1. **Prove redundancy** — Remove a declaration only after comparing computed styles and relevant
   layout states with and without it. A browser default is not redundant when the declaration is
   an intentional reset.

2. **Leverage inheritance** — Don't redeclare inherited properties (`font-family`, `color`) unless overriding is intentional.

3. **Eliminate duplication** — Consolidate truly identical declarations when specificity,
   cascade order, media queries, themes, and component isolation remain unchanged. Matching
   `height` and `line-height` may be intentional sizing; verify before removing either.

4. **Preserve layout contracts** — Do not remove flex/grid alignment because one current child
   happens to render correctly. Verify different content lengths, empty states, wrapping,
   breakpoints, and directionality.

5. **Verify visual behavior** — Check default, hover, focus, active, disabled, validation,
   responsive, theme, and reduced-motion states that exist in the product. Prefer visual or
   computed-style regression evidence over eyeballing one screenshot.

6. **Keep design intent** — Preserve tokens, component boundaries, and deliberate Figma-derived
   geometry. Cleanup removes accidental noise, not the design language.

Report removed declarations, retained suspicious declarations and why they remain, and the
states used for verification.
