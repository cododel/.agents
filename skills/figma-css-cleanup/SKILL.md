---
name: figma-css-cleanup
description: "Audit and simplify CSS exported from Figma or visual builders without changing rendered behavior. Use for `почисти generated/Figma CSS`, redundant declarations, or style-noise reduction while preserving layout, resets, responsive states, and variants."
---

## CSS Hygiene For Generated Designs

An audit is read-only. Remove or rewrite CSS only when the request authorizes cleanup. Find the
maintained source, its generated outputs, and all affected consumers before proposing or applying
changes; regenerate outputs through the owning process when required.

**Core Principles:**

1. **Prove redundancy** — Adjacent, exactly identical declarations in the same block (property,
   value, and priority) can be removed statically when no source/generator directive gives them a
   distinct purpose. For other removals, compare computed styles and layout with and without the
   declaration across affected consumers and relevant states. A browser default is not redundant
   when the declaration is an intentional reset.

2. **Verify inheritance** — Remove inherited-property declarations (`font-family`, `color`) only
   when behavior stays equivalent across all affected consumers, themes, variants, and states.
   Inheritance alone does not prove a declaration is redundant.

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
states used for verification. Keep uncertain candidates unchanged and identify unverified states
or consumers; one screenshot or unavailable browser evidence cannot establish preservation.
