# Discovery: locating the docs to audit

> **Note:** This file is duplicated in `issue-writer/references/` and
> `adr-writer/references/` (with `issues` / `adr` swapped in for the doc kind they care
> about). The duplication is intentional — each skill stays installable on its own.
> Keep the copies in sync when the discovery technique itself changes.

## Goal

Produce a confirmed list of documentation directories the audit will cover.
"Confirmed" means **proven from repo evidence**, not guessed from a similar name.

## Step D1 — Read repo instruction files first

If any of these exist in the repo root or any parent of the cwd, read them and let any
explicit instruction win over the `find` results below:

- `AGENTS.md`
- `CLAUDE.md`
- `.cursorrules`
- `docs/README.md`
- `README.md`

Repo instructions are authoritative because they encode local workflow conventions the
file system can't express (e.g. "issues live in `notes/`, ADRs in `decisions/`,
runbooks in `ops/playbooks/`").

## Step D2 — One-shot directory scan

Run a single `find` from the repo root with explicit exclusions. Cover all common
documentation locations in one command:

```bash
find . -type d \
  \( -name issues -o -name adr -o -name ADR -o -name decisions -o -name 'adr-*' \
     -o -name runbooks -o -name playbooks -o -name postmortems -o -name notes \) \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/dist/*' \
  -not -path '*/.next/*' \
  -not -path '*/build/*' \
  -not -path '*/.venv/*' \
  -not -path '*/venv/*' \
  -not -path '*/target/*' \
  -not -path '*/archive/*'
```

Why this command shape:

- Cleanup audits often span more kinds than just issues/ADRs — runbooks rot too.
- `archive/` is excluded at discovery time because already-archived docs aren't
  candidates for re-classification.
- A loop assumes the layout. `find` discovers it.

## Step D3 — Confirm scope with the user

For monorepos (multiple hits) or when the find returns surprises (a `notes/` directory
nobody mentioned), **stop and confirm** before reading any bodies.

The default expansion of "audit our docs" is wide and expensive — it can pull in
hundreds of files across an unfamiliar layout. Even a 30-second clarification ("you
mean root `docs/` only, or also the per-app dirs?") prevents a 10-minute audit of
something the user didn't actually want.

Frame the question concretely:

```
Found these docs locations:
  1. docs/issues/             (12 files)
  2. docs/adr/                (8 files)
  3. apps/api/docs/issues/    (5 files)
  4. apps/web/docs/issues/    (3 files)
  5. notes/                   (24 files — looks like a mix)

Audit scope?
  - all of the above
  - just root docs/ (1+2)
  - just one specific path
  - all *issues/ but skip adr/ and notes/
  - other (specify)
```

## Step D4 — Read each directory's own README

For each confirmed docs directory, look inside for files that document the local
convention:

- `README.md`, `CONTRIBUTING.md`, `TEMPLATE.md`, `_template.md`

Read them in full. They typically encode the same things `issue-writer` and
`adr-writer` need (filename pattern, status taxonomy, project guardrails) — but for
cleanup the most important signals are:

- Which status tags exist (`[ACTIVE]`, `[RESOLVED]`, `[CLOSED-100%]`, etc.) so you
  know what "resolved" looks like in this repo.
- Whether the directory has a documented archive convention (e.g. "files move to
  `archive/` after 90 days resolved").
- Project guardrails the body should respect (DB rules, deprecated services, etc.).

Pass these conventions to the classifier subagent as part of its task brief — the
classifier's verdicts are only as good as its understanding of the local rules.

## Step D5 — Stop and ask, never guess

If the exact targets cannot be proven from repo files or explicit user input, stop and
ask. For an audit, the cost of a wrong scope is reading the wrong files; for a
delete, it's losing them. Both are cheaper to prevent than to recover from.
