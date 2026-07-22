# Repository Issues

This directory tracks bugs, incidents, regressions, technical debt, and operational follow-ups
as Markdown files close to the code they affect.

## Naming

Use `[STATUS]P<priority>-YYYY-MM-DD-<english-kebab-slug>.md`.

- Status: `ACTIVE`, `INVESTIGATING`, or `RESOLVED`.
- Priority: `P0` critical through `P3` low.
- Keep prose in the author's language; keep filenames in English kebab-case.

## Content

Each issue records evidence, affected scope, root cause when known, a recommended fix, and a
verification checklist. Unknown facts remain explicit `TODO:` items rather than guesses.

## Lifecycle

Status changes update both the body and filename. Resolved issues are not archived forever in
this directory: first extract durable architectural decisions to ADRs and operational knowledge
to runbooks or troubleshooting docs, then delete the source issue through an explicit per-path
gate. Git history provides recovery only for tracked, committed files.

Local project instructions and established examples override this fallback convention.
