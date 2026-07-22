# Discovery: locating the ADR directory

> **Note:** This file is duplicated in `issue-writer/references/` and
> `docs-cleanup/references/` (with `adr` swapped for `issues` etc.). The duplication is
> intentional — each skill stays installable on its own. Keep the copies in sync when
> the discovery technique itself changes.

## Goal

Produce a single confirmed path to the ADR directory (or the right path to *create* one
if the project doesn't have it yet). "Confirmed" means **proven from repo evidence**,
not guessed from a similar name.

## Step D1 — Read repo instruction files first

If any of these exist in the repo root or any parent of the cwd, read them and let any
explicit instruction win over the `find` results below:

- `AGENTS.md`
- `CLAUDE.md`
- `.cursorrules`
- `docs/README.md`
- `README.md` (only if it has a docs/adr section)

Repo instructions are authoritative because they encode local workflow conventions the
file system can't express (e.g. "ADRs go in `notes/decisions/` for legacy reasons").

## Step D2 — One-shot directory scan

Run a single `find` from the repo root (or from the cwd if no clear repo root) with
explicit exclusions to keep it fast on large trees:

```bash
find . -type d \( -name adr -o -name ADR -o -name decisions -o -name 'adr-*' \) \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/dist/*' \
  -not -path '*/.next/*' \
  -not -path '*/build/*' \
  -not -path '*/.venv/*' \
  -not -path '*/venv/*' \
  -not -path '*/target/*'
```

Why this command shape:

- A loop assumes the layout. `find` discovers it.
- `decisions` and `adr-*` cover common variants (`adr-infra`, `architecture-decisions`).
- Excluding build artifacts is the only thing that makes this fast on a real monorepo.
- One command, one output. The model reads the list and decides.

## Step D3 — Read the directory's own README

Once an `adr/` directory is confirmed, look inside for files that document the local
convention:

- `README.md`, `CONTRIBUTING.md`, `TEMPLATE.md`, `_template.md`

Read them in full. Mature ADR directories typically encode:

- **Filename pattern** (which may extend the generic with status-percent prefix, slice
  tags, or a custom `XYZ-NNNN-` numbering)
- **Required header fields** (Scope / Component, Risk/Strictness Profile, Implementation,
  Status, relationship links, Refresh notes)
- **Status taxonomy** — the decision lifecycle (Proposed/Accepted/Deprecated/Superseded)
  and, separately, any implementation-completeness prefix (CLOSED-100%/IN-PROGRESS-X%/OPEN-X%).
  A local README may define its own; its convention wins over the fallback template.
- **Verification requirements** (what proof is needed before marking an ADR complete)
- **Project guardrails** (current architecture invariants the ADR body should respect
  or call out)

The local README **always wins** over `assets/adr-template.md`. The template is the
floor when nothing local exists; the README is the ceiling when it does.

Also sample 2-3 existing ADR files in the directory to confirm the documented
convention is the convention people actually follow.

## Step D4 — Bootstrap when missing

If no `adr/` directory exists:

- For **from-chat** mode: pick the right path per `path-resolution.md` and create it
  in the same change as writing the first ADR. No prompt needed — creating the directory
  is implied by the user's "create ADR" request. Install `assets/adr-readme.md` as
  `README.md` so the convention remains visible inside the project.
- For **from-issue** mode: **stop and ask** before creating a new doc location. The
  user is in batch-promote mode, and bootstrapping a new directory is a separate
  decision that deserves explicit confirmation. If approved, create the directory and install
  the same fallback README before writing promoted ADRs.

## Step D5 — Stop and ask, never guess

If the exact target cannot be proven from repo files or explicit user input, stop and
ask. Similar names, nearby directories, previous plans, or older conversations are NOT
proof. The cost of asking is one message; the cost of writing in the wrong place is much
higher (and ADR misplacement is especially bad — they're meant to be discoverable).
