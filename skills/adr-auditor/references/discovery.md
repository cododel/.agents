# Discovery: locating the ADR directory

> **Note:** This file is duplicated from `adr-writer/references/` (and
> `issue-writer/`, `docs-cleanup/`). The duplication is intentional — the discovery
> technique is generic and each skill stays installable on its own. Keep the copies in
> sync when the technique itself changes. (The quality *criteria* are NOT duplicated —
> those are read from `../../adr-writer/references/adr-spec.md`.)

## Goal

Produce a confirmed list of the ADR directories to audit — **proven from repo evidence**,
not guessed from a similar name. Unlike the writer's discovery, the auditor never
*creates* a directory: if there's no ADR corpus, there's nothing to audit (skip to the
coverage check — a project with real architecture and zero ADRs is itself a finding).

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

In a monorepo, expect **several** ADR roots (root + per-app + infra). Audit them as one
corpus for cross-references but keep each directory's local convention separate — Step D3.

## Step D3 — Read each directory's own README

For every confirmed `adr/` directory, look inside for files that document the local
convention:

- `README.md`, `CONTRIBUTING.md`, `TEMPLATE.md`, `_template.md`

Read them in full. The local convention is the **yardstick the audit measures against** —
judge each ADR by its own project's rules, not by imposing the fallback template. Mature
ADR directories typically encode:

- **Filename pattern** (which may extend the generic with a status-percent prefix, scope
  tags, or a custom `XYZ-NNNN-` numbering)
- **Required header fields** (Scope / Component, Risk/Strictness Profile, Implementation,
  Status, relationship links, Refresh notes)
- **Status taxonomy** — the decision lifecycle (Proposed/Accepted/Deprecated/Superseded)
  and, separately, any implementation-completeness prefix (CLOSED-100%/IN-PROGRESS-X%/OPEN-X%)
- **Verification requirements** (what proof is needed before marking an ADR complete)
- **Project guardrails** (current architecture invariants the ADR body should respect)

Where a directory has **no** documented convention, the fallback is
`adr-writer/assets/adr-template.md` — but flag the missing convention as a corpus finding
(naming/placement consistency is one of the §6 criteria).

Also sample 2-3 existing ADR files to confirm the documented convention is the one people
actually follow — a README that no ADR obeys is itself a finding.

## Step D4 — Confirm scope before a large audit

If multiple ADR roots exist, confirm with the user which are in scope before reading
bodies. Auditing every ADR in a large monorepo without checking is the most common way to
burn a session. State what you found and let the user narrow it.

## Step D5 — Stop and ask, never guess

If the exact set of directories cannot be proven from repo files or explicit user input,
stop and ask. Similar names, nearby directories, or older conversations are not proof. The
cost of asking is one message.
