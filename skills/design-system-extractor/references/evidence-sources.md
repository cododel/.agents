# Evidence Sources

Where to look and how to mine each layer. For small projects, be exhaustive. For large
repositories, state which product surfaces and shared primitives were sampled.

---

## Layer 1 — Implemented UI (the ground truth)

Facts (palette, type, shape, dimensions, layout, component states, assets, motion) MUST come
from implementation evidence. `collect_tokens.py` accelerates common text formats; it does not
replace stack-native inspection or visual validation.

### Files to find

- **Web CSS and Tailwind:** `tailwind.config.{js,cjs,mjs,ts}` → `theme` and `theme.extend`
  (colors, fontFamily, borderRadius, spacing, screens, boxShadow). JS configs are not fully
  regex-parseable; read the file directly when present.
- **Global CSS / theme:** `**/globals.css`, `**/global.css`, `app/**/*.css`, `styles/**/*.css`,
  `src/**/*.css`, plus `.scss/.sass/.less`. Look at `:root { ... }`, `@theme { ... }`
  (Tailwind v4), `[data-theme]`, `.dark { ... }` for light/dark token sets.
- **shadcn/ui:** `components.json` → `style`, `tailwind.baseColor`, `tailwind.cssVariables`,
  `aliases`. Confirms whether the project uses CSS-variable theming and which base palette.
- **Fonts:** `next/font/google` and `next/font/local` imports (e.g. `Geist`, `Geist_Mono`,
  `Inter`), `@font-face`, `<link>` to font CDNs, and `fontFamily` in the Tailwind config.
- **Components:** the most-used UI primitives — buttons, cards, inputs, nav/header/footer,
  layout shells, dialogs. Read these directly to capture **patterns and states** that tokens
  don't show: default vs hover vs focus vs active, wireframe-vs-fill, how borders behave, etc.
- **Apple platforms:** asset catalogs (`*.xcassets`), SwiftUI/UIKit/AppKit theme code,
  appearance proxies, custom fonts, shape styles, symbols, storyboards, and previews.
- **Android:** `res/values` colors/dimens/styles/themes, XML drawables/layouts, Material theme
  definitions, Compose `ColorScheme`/`Typography`/`Shapes`, and previews.
- **Flutter and cross-platform:** `ThemeData`, `ColorScheme`, text themes, component themes,
  asset declarations, shared design-token files, and platform-specific overrides.
- **Other desktop/native stacks:** theme/resource dictionaries, style sheets, widget catalogs,
  design-token JSON/YAML, icon sets, screenshots, snapshots, and preview/demo applications.
- **Rendered evidence:** Storybook, previews, screenshot tests, product screenshots, and a
  runnable UI when available. Use these to validate hierarchy and composition that raw tokens
  cannot prove.

### How to read it

- **Frequency is signal, not semantics.** A value used across the whole codebase may be a rule;
  confirm its role from definitions and representative usage before naming it as a token. A
  one-off value is normally an exception. For example, dominant `rounded-none` or
  `border-radius: 0` supports a "Zero Radius" rule only after component usage confirms it.
- **Capture the system, not the instance.** "Cards use a 1px grey border by default and an
  accent border on hover, with no background fill" is a system rule. Listing one card's exact
  classes is not.
- **Light/dark:** if two token sets exist, document both and which is default.
- Don't assert framework defaults or resource semantics from memory; verify with `find-docs` or
  current official documentation.

---

## Layer 2 — Intent docs (the "why")

Code rarely explains itself. Mine these for philosophy, rationale, and naming.

- **Existing design docs:** `DESIGN.md`, `DESIGN_SYSTEM.md`, `DESIGN*.md`, `STYLE*.md`, `BRAND*.md`,
  `docs/design*`, `docs/ui*`. If one exists, it is both evidence and (in update mode) the
  base to preserve.
- **Decision records:** `docs/decisions/`, `docs/adr/`, `**/adr/*.md`, `openspec/` — proposals
  and design.md files often state *why* a visual choice was made.
- **Agent/project docs:** `AGENTS.md`, `CLAUDE.md`, `ROADMAP.md`, `README*`, `CONTRIBUTING*`.
  These frequently encode design constraints and the project's "voice".
- **Storybook / component docs:** `*.stories.{ts,tsx,js,jsx,mdx}`, `*.mdx` — usage intent,
  variants, do/don't notes.
- **Code comments:** grep for design rationale near theme/token definitions
  (e.g. `rg -i "design|brand|theme|palette|aesthetic|do not|must"` in CSS/config/component dirs).
- **Git history:** recover decisions and their timing:

  ```bash
  git log --pretty=format:'%h %ad %s' --date=short \
    -i --grep='design\|ui\|ux\|style\|theme\|color\|colour\|font\|typograph\|layout\|brand\|spacing\|radius'
  ```

  Inspect the diffs of the most relevant commits (`git show <hash>`) for what actually changed
  and any rationale in the message body.
- **PR descriptions (if `gh` is available and authenticated):**
  `gh pr list --search "design OR ui OR theme" --state merged --limit 20` then `gh pr view <n>`.

---

## Layer 3 — Optional agent-session history (the evolution)

Use this layer only after explicit approval. The bundled helper currently supports Claude Code
transcripts; other clients need their own adapter. Read only short redacted snippets per
`session-history.md`. A correction can be useful evidence, but confirm it against
later code/docs because the snippet may describe an abandoned intermediate direction.

---

## Handling conflicts between layers

- **Facts:** code wins. If a doc claims the accent is `#3B82F6` but the code consistently uses
  `#2663EB`, document `#2663EB` and note the discrepancy.
- **Intent:** docs and approved session evidence inform the *why* and naming, but later accepted
  docs and implemented behavior outrank an isolated historical snippet.
- **Always report** unresolved conflicts in the provenance footer rather than papering over them.
  A surfaced conflict is useful to the user; a silent guess is not.
