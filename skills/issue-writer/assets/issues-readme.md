# Repository Issues

This directory tracks deferred, independently resumable work as Markdown files close to the
code it affects. Incidental observations and work being completed now do not need Issue files.

## Naming

Use `[STATUS]-YYYY-MM-DD-<english-kebab-slug>.md`.

- Status: `OPEN`, `IMPLEMENTING`, or `CLOSED`.
- Priority: `Critical`, `High`, `Medium`, or `Low` for urgency and sequencing.
- Severity: `Critical`, `High`, `Medium`, or `Low` for impact or harm.
- Keep prose in the author's language; keep filenames in English kebab-case.

## Content

Each issue records evidence, affected scope, root cause when known, a recommended fix, and a
verification checklist. Unknown facts remain explicit `TODO:` items rather than guesses.
Deferred work also records the known context, why it was deferred, and concrete conditions for
resuming it.

## Lifecycle

Status changes update both the body and filename. Priority and severity stay in the body and do
not require a rename. Closed issues are not archived forever in this directory: first extract
durable architectural decisions to ADRs and operational knowledge
to runbooks or troubleshooting docs, then delete the source issue through an explicit per-path
gate. Git history provides recovery only for tracked, committed files.

Local project instructions and established examples override this fallback convention.
