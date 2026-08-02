---
name: design-system-extractor
description: "Extract or update an existing product's visual/UI language in DESIGN.md from code, UI assets, docs, and approved session evidence. Use when asked to document, reverse-engineer, audit, regenerate, or update a design system/style guide (`вытащи дизайн-систему`) for web, mobile, or desktop. Do not use to invent a new visual system."
---

# Design System Extractor

## What this does, and why it is different

Most "extract the design system" attempts produce a flat dump of colors and fonts. That
is the cheap, low-value version. The point of this skill is to reconstruct the design
system the way a careful designer would document it: the **mechanical tokens** (palette,
type scale, radii, spacing, component states) AND the **concept** behind them — the
manifesto, the non-negotiable rules, the intent. A good output reads like an intentional
design language, not a CSS audit.

To get there, gather evidence from these layers, in this order of trust:

1. **Implemented UI — the ground truth.** Code, theme resources, assets, rendered surfaces,
   component catalogs, and platform design tokens show what the UI actually is. Anchor every
   factual rule to implementation evidence.
2. **Intent docs — the "why".** Existing design docs, `docs/decisions/` (ADRs), `openspec/`,
   `AGENTS.md`, `ROADMAP.md`, README, comments, Storybook, and git history. This is where
   the philosophy and rationale live; code rarely explains itself.
3. **Optional agent-session history — the evolution.** It can recover debated or corrected
   intent, but may contain unrelated private context. Use it only after explicit approval and
   never make a valid extraction depend on its availability.

When layers disagree (a doc says one thing, the code does another), **code wins for facts**
and the conflict is reported, not silently resolved.

## When NOT to use this skill

- The user wants the **stack/architecture** documented (frameworks, DB, jobs, deploy) — that
  is a different document, not a visual design system. Decline this scope unless asked to add it.
- The user wants to **build new UI** from scratch — this skill documents what exists, it does
  not design.
- A single trivial token lookup ("what's the primary color") — just answer; no skill needed.

## Workflow

Default mode is **interactive**: gather evidence, infer the concept, *confirm the concept
with the user*, then write the full document. The manifesto and the "non-negotiable rules"
are the subjective part, and confirming them is the cheapest place to fix a wrong reading.
Fall back to a one-shot autonomous pass only if the user explicitly asks ("just generate it",
"no questions").

### Phase 1 — Gather evidence

Read `references/evidence-sources.md` first. Be exhaustive for a small project; for a large
repository, identify representative product surfaces and shared primitives, state the sampling
boundary, and avoid pretending a partial scan was complete. Then:

1. **Orient.** Identify the project root, product surfaces, and UI stack from the relevant
   manifests and resource trees: web manifests, iOS/macOS projects and asset catalogs,
   Android/Compose resources, Flutter packages, desktop UI frameworks, or other local evidence.
2. **Harvest token candidates.** Resolve the loaded skill's base directory and run the helper
   where its supported text formats apply:

   ```bash
   python <absolute-skill-dir>/scripts/collect_tokens.py <project_root>
   ```

   It emits candidate colors, variables, fonts, radii, and dimensions from web and common
   native text formats. Treat this as an inventory aid, not proof of semantic roles. For an
   unsupported stack, inspect its theme/resource system directly instead of forcing CSS terms.
3. **Optionally mine session history.** Ask first. If approved, run the currently available
   Claude Code adapter:

   ```bash
   python <absolute-skill-dir>/scripts/scan_sessions.py <project_root>
   ```

   It returns short, redacted, design-relevant snippets. Other clients may require another
   adapter. If history is unavailable or declined, proceed without treating that as a gap.
4. **Read intent docs (Layer 2).** Existing design docs, `docs/decisions/`, `AGENTS.md`,
   README; run `git log` filtered for design/ui/style/theme commits. Details in
   `references/evidence-sources.md`.
5. **Read representative surfaces and primitives.** Open shared controls, navigation, inputs,
   content containers, layout shells, and product-defining screens. Capture platform-relevant
   states such as hover/focus, pressed/selected, disabled/loading, validation, responsive or
   adaptive behavior, and accessibility variants.

### Phase 2 — Infer the concept

From the combined evidence, derive:

- **Manifesto** — one tight paragraph naming the design philosophy, plus a few keywords.
  Lean on Layer 3 and Layer 2 for the actual intent; do not invent a vibe the evidence
  doesn't support.
- **Core rules (non-negotiables)** — detected mainly from *consistency* in the code. E.g.
  `border-radius: 0` everywhere → "Zero Radius"; background always `#000000` → "True Black".
  A rule is something the codebase enforces, not a one-off.
- **Token system** — palette, typography, radii, spacing, all traced to code.

Mark each item as **observed** (from code) or **inferred** (philosophy/rationale). Keep the
distinction honest — it is what makes the document trustworthy.

### Phase 3 — Confirm with the user (default)

Present the draft concept compactly: the manifesto, the core rules, and the key tokens
(palette + fonts). Ask for corrections, missing rules, or renames. Do not write the full
document until the user confirms — unless they requested the autonomous one-shot.

### Phase 4 — Generate

Fill the structure in `references/output-template.md`. Write the result and append a short
provenance footer (which evidence layers were used, and any unresolved conflicts). See
**Output rules** below.

## Output rules

- **Default path:** `DESIGN.md` at the project root. Honor an explicit path/filename
  if the user gives one.
- **If a design doc already exists:** do not blindly overwrite. Read it, then produce an
  updated version that *preserves the human-written voice* (manifesto, intentional prose)
  while refreshing tokens/components/rules to match the current code. Summarize what changed
  and why; never silently drop sections a human wrote on purpose.
- **Never invent tokens.** Every color, font, radius, and spacing value must trace to the
  evidence. If you can't find something, say so rather than fabricating a plausible value.
- **Frequency-aware language.** Describe ubiquitous values as rules and rare values as
  exceptions; don't present a one-off accent as a system-wide token.
- **Provenance footer** is mandatory: list the evidence layers consulted (code / docs / git /
  sessions), and flag any code-vs-doc conflicts you found.

## Library specifics — do not guess

For framework-specific semantics, use the global `find-docs` workflow or official current
documentation rather than guessing. This applies equally to Tailwind/shadcn, Apple platform
APIs, Android/Compose, Flutter, and desktop UI frameworks.

## Reference files

- `references/evidence-sources.md` — exhaustive where-to-look and how-to-mine for all three
  layers, plus the conflict-handling rule. Read this at the start of Phase 1.
- `references/session-history.md` — optional Claude Code history adapter and privacy rules.
  Read only after the user approves session-history mining.
- `references/output-template.md` — the `DESIGN.md` section skeleton to fill, with
  per-section guidance. Read at Phase 4.

## Scripts

- `scripts/collect_tokens.py` — deterministic candidate harvest from common web/native text
  formats. Stdlib only; supplement it with stack-native resource inspection.
- `scripts/scan_sessions.py` — optional, redacted Claude Code session-history adapter. Stdlib
  only; it is not required for extraction.
