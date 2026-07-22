# Discovery: locating the issues directory

> **Note:** This file is duplicated in `adr-writer/references/` and
> `docs-cleanup/references/` (with `issues` swapped for `adr` etc.). The duplication is
> intentional — each skill stays installable on its own. Keep the copies in sync when the
> discovery technique itself changes; do not introduce a shared root skill for this.

## Goal

Produce a single confirmed path to the issues directory for the current operation.
"Confirmed" means **proven from repo evidence**, not guessed from a similar name.

## Step D1 — Read repo instruction files first

If any of these exist in the repo root or any parent of the cwd, read them and let any
explicit instruction win over the `find` results below:

- `AGENTS.md`
- `CLAUDE.md`
- `.cursorrules`
- `docs/README.md`
- `README.md` (only if it has a docs/issues section)

Repo instructions are authoritative because they encode local workflow conventions the
file system can't express (e.g. "all issues live in `notes/issues/` for legacy reasons").

## Step D2 — One-shot directory scan

Run a single `find` from the repo root (or from the cwd if no clear repo root) with
explicit exclusions to keep it fast on large trees:

```bash
find . -type d -name issues \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/dist/*' \
  -not -path '*/.next/*' \
  -not -path '*/build/*' \
  -not -path '*/.venv/*' \
  -not -path '*/venv/*' \
  -not -path '*/target/*'
```

Why this list and not a "try docs/issues/, then apps/*/docs/issues/, then …" loop:

- A loop assumes the layout. `find` discovers it.
- Excluding build artifacts is the only thing that makes this fast on a real monorepo.
- One command, one output. The model reads the list and decides.

## Step D3 — Scope decision

Interpret the find output:

- **Single hit** → use it. Done.
- **No hits**:
  - For **create** mode with a clear repo root and no conflicting repo instruction: bootstrap
    `docs/issues/` at the root, or `<scope>/docs/issues/` when the request proves one module
    owns the issue. The explicit request to create a repository issue authorizes this standard
    structure; do not ask merely because the directory is absent.
  - Ask only when repo instructions conflict, the repository root is unclear, or monorepo scope
    has more than one plausible target.
  - For **close** mode: nothing to close. Report and stop.
- **Multiple hits (monorepo)**:
  - For **create** mode, scope rules:
    - Issue is local to one app/package → use `<scope>/docs/issues/`
    - Issue is shared, infra, cross-cutting, or scope is ambiguous → root `docs/issues/`
    - If the user named a scope explicitly, honor it.
  - For **close** mode: ask which directory to sweep. Don't sweep all by default —
    the user almost always means one specific app or the root.

## Step D4 — Read the directory's own conventions

Once the issues directory is known, **before** writing or moving anything, look inside it
for files that document the local convention:

- `README.md`, `CONTRIBUTING.md`, `ISSUE_TEMPLATE.md`, `TEMPLATE.md`, `_template.md`
- Any obvious "how we write issues here" file

Read them in full. They typically encode:

- Filename pattern (which may extend the generic one with percent-status, slice tags, etc.)
- Required header fields (Date, Status, Severity, Probe, Implementation, FSD Slice, …)
- Local guardrails the issue body should call out (DB conventions, deprecated services,
  forbidden APIs, …)
- Notes about automated tooling (e.g. "do NOT include `## Incidents` — bot appends it")

These local conventions **always win** over the generic fallback in
`assets/fallback-template.md`. The fallback is only the floor when nothing local exists.

Also sample 2-3 existing files in the directory to confirm the documented convention is
the convention people actually follow.

When Step D3 bootstraps a new directory, install `assets/issues-readme.md` as its `README.md`
and use `assets/fallback-template.md` for the first issue. This makes the portable workflow a
visible project convention rather than knowledge available only to the current agent.

## Step D5 — Stop and ask, never guess

If the exact target cannot be proven from repo files or explicit user input, **stop and
ask**. Similar names, nearby directories, previous plans, or older conversations are
NOT proof. The cost of asking is one message; the cost of writing or moving files in
the wrong place is much higher.
