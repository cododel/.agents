# Close workflow

Sweep closed issues by extracting any documentation value first, then deleting the
source files. The open list stays focused; no `archive/` subdirectory is used.

By the time you're reading this, you've loaded `discovery.md` and `conventions.md` from
`SKILL.md`'s shared steps.

## Why delete after extraction (not archive)

The old model moved closed issues into `archive/`. In practice the archive directory
is write-only: rarely read, adds noise to repo-wide greps, and duplicates what git
history already keeps. The current model is simpler:

- **If a closed issue has documentation value**, extract it into the proper home:
  - architectural decisions → ADR (via `adr-writer:from-issue`)
  - operational procedures → runbook / `DEVELOPMENT.md` / similar
  - unique repros, commands, diagnostics → troubleshooting doc / inline comment
- **Once the value is extracted (or there was none), delete the file.**

The ADR header's `Source issue:` field preserves provenance. Git history holds the body
if anyone ever needs to recover it. The issues directory only contains work
that are still open.

If the user wants to delete docs that are not closed issues, that's the `docs-cleanup`
skill's job (with its own safety gate).

## Step C1 — Confirm the directory to sweep

`discovery.md` should have produced a single confirmed issues directory. If `find`
returned multiple hits (monorepo with several `docs/issues/` directories), **ask which
one** to sweep. Do not sweep all by default — the user almost always means one specific
scope.

## Step C2 — Enumerate closed candidates

A file is a candidate for closing if **either**:

1. Its filename starts with `[CLOSED]`, OR
2. Its body header contains `**Status:** Closed` (case-insensitive)

For compatibility with an established local convention, also recognize legacy `[RESOLVED]`
or `[RESOLVED-100%]` filenames and `Status: Resolved`. Never rename or reinterpret a legacy
candidate silently; use its proven local convention in the mismatch check.

Run two separate scans to catch both — they're not equivalent in real repos, where
filename and body sometimes drift apart.

```bash
# By filename
find <issues-dir> -maxdepth 1 -type f \( -name '[[]CLOSED]*.md' -o -name '[[]RESOLVED*' \)

# By body status (case-insensitive, anchored to a status line)
grep -lEi '^\*\*Status:\*\*[[:space:]]+(Closed|Resolved)' <issues-dir>/*.md
```

Take the union of both lists.

## Step C3 — Detect filename / body mismatches

For each candidate, compare:

- Filename status tag (`[CLOSED]`, `[OPEN]`, `[IMPLEMENTING]`, or a proven legacy tag)
- Body status field (`**Status:** Closed | Open | Implementing`, or its proven legacy value)

If they disagree, classify the file as **ambiguous** — do not include it in the delete
plan. Surface ambiguous files in the report so the user can fix them manually before
re-running the sweep.

The reason to be strict here: a mismatch usually means someone forgot to update one of
the two. Auto-resolving in either direction risks deleting a file that's actually still
open.

## Step C4 — Pre-extraction check (mandatory, per candidate)

For each non-ambiguous candidate, read the body in full and scan for **extractable
documentation value**. Mark the candidate as `blocked` if any of these signals appear:

| Signal in body                                                                  | Suggested extraction target                         |
|---------------------------------------------------------------------------------|-----------------------------------------------------|
| Rejected options spelled out (2+ approaches compared, one chosen with rationale) | ADR via `adr-writer:from-issue`                     |
| Architectural invariant or system boundary stated ("X always goes through Y")    | ADR via `adr-writer:from-issue`                     |
| Choice of framework / library / language / package manager / data model         | ADR via `adr-writer:from-issue`                     |
| Cross-cutting policy (auth, errors, logging, deploy, security, observability)   | ADR via `adr-writer:from-issue`                     |
| "By design" rationale that explains why something stays as-is                   | ADR via `adr-writer:from-issue`                     |
| Unique repro steps, SQL, or commands not preserved elsewhere                    | Troubleshooting doc / runbook / inline comment      |
| Operational procedure (deploy steps, rotation playbook, incident response)      | Runbook / `DEVELOPMENT.md` / `OPERATIONS.md`        |
| Useful diagnostic technique that took time to develop                           | Troubleshooting doc / commit message in fix         |

For each `blocked` candidate, record:

- `path`
- `signal` — which row from the table matched, with a one-sentence quote from the body
- `suggested_target` — concrete extraction destination

Candidates with **no matching signal** are `safe-to-delete`. The body contained the
resolution but no durable documentation value beyond what the fix commit already
records.

The bias here is conservative: when uncertain whether a signal is "extractable enough",
treat the file as `blocked`. The operator can override in the gate. Silent deletion of
content the user later wishes they'd kept is the failure mode to avoid.

## Step C5 — Confirmation gate

Before deleting any file, present a plan and **wait for explicit per-decision
approval**. The gate has no silent default — the operator must respond per-item or with
an explicit bulk approval. Even if the user's request sounded categorical, this gate
stays.

Before rendering the gate, preflight each proposed deletion: resolve the canonical path,
require a regular non-symlink file inside the confirmed issues directory, record a content
fingerprint, and report whether Git tracks the current contents. Untracked or locally modified
files are `hold` by default and require an explicit exact-path override that acknowledges the
unrecoverable state.

Render the gate as plain markdown to the user (not wrapped in a code block — the
template below is for *your* reference, not for the literal output shape).

```
Close plan for <issues-dir>:

Decisions required from you:
  1. Approve the delete list (or hold specific items).
  2. For each `blocked` item: extract the value first (recommended), or `override` to
     force-delete (extraction explicitly waived).
  3. Ambiguous items are left in place — fix the status mismatch before next sweep.

--- Plan ---

=== To delete (N) — no extractable documentation value ===

  [CLOSED]-2026-04-12-readme-typo.md
    one-liner: README typo fix; no rationale to preserve.
    recovery: tracked and committed
    fingerprint: <hash>

  [CLOSED]-2026-03-08-restart-after-deploy.md
    one-liner: one-off service restart; ops note already mirrored in runbook.

=== Blocked — extract first (M) ===

  [CLOSED]-2026-02-15-bun-package-manager.md
    one-liner: choice of Bun over npm/pnpm/yarn with explicit rejections.
    signal: rejected options (npm/pnpm/yarn) + package-manager invariant.
    suggested: `adr-writer:from-issue` → then re-run close.

  [CLOSED]-2026-01-22-mysql-deadlock-repro.md
    one-liner: unique SQL repro for deadlock under concurrent writes.
    signal: unique repro + observed timing pattern.
    suggested: move into a troubleshooting doc → then re-run close.

=== Ambiguous — status mismatch, NOT in plan (K) ===

  [CLOSED]-2026-05-01-flaky-test.md
    reason: filename [CLOSED] but body says Status: Open.

Counts: delete=N, blocked=M, ambiguous=K

Reply with one or more:
  - `apply`                            — delete all in the `To delete` list
  - `apply except <paths>`             — delete the list except the named paths
  - `hold: <path>, <path>`             — keep these specific items in place
  - `override: <path>`                 — force-delete a `blocked` item (extraction waived)
  - `cancel`                           — abort
```

Accept `apply` / `proceed` / `go` / `да` as approval for the full `To delete` list.
Anything else means stop and clarify. Overrides must be explicit per path — no
`override all`.

## Step C6 — Apply the deletes

For each approved path (`To delete` minus `hold` plus any explicit `override`):

```bash
rm -- "$path"
```

- Immediately before deletion, re-resolve the path, re-read it, and recompute the fingerprint.
  If path type, location, or contents differ from the gated state, skip it and report the change.
- Do not `git rm` unless the operator asked for a commit in the same operation. The
  default is plain `rm`; the user stages it themselves.
- If a file disappeared between gate and apply (someone else committed a delete already),
  surface in the report and continue with the rest.

## Step C7 — Update indexes if present

If the issues directory has an unambiguous index (`README.md` with an "Open issues"
table, or an `index.md`), remove the deleted entries in the same change.

If the index format is **unclear** (free-form prose, mixed sections, no obvious table),
**don't edit it** — note in the report that the index may need manual updates. The cost
of mangling someone's hand-curated README is higher than the cost of asking.

## Step C8 — Report back

Final report includes:

- counts: deleted, blocked (per-extraction-target breakdown), ambiguous
- the full list of deleted paths
- per-blocked item: path, signal, suggested extraction target — so the user can decide
  the order in which to handle them
- ambiguous files with reason (filename/body disagreement)
- whether indexes were updated, and which
- next-step suggestions, e.g.:
  - "3 ambiguous files — fix the body status and re-run close"
  - "Blocked: 4 issues look ADR-worthy — run `adr-writer:from-issue` to promote them
    (it deletes the sources itself), or extract manually and re-run close"
