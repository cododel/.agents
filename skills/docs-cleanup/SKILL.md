---
name: docs-cleanup
description: "Audit and classify existing repository docs—issues, ADRs, decisions, temporary feature briefs, incidents, and runbooks—for broad cleanup. Use for stale/duplicate docs, explicit milestone or release documentation cleanup, `почисти доки`, `docs are a mess`, or read-only questions such as `which issues can we close`. Diagnose by default. Do not use for ADR-only audits (`adr-auditor`) or creating/updating/closing issue records (`issue-writer`)."
---

# Docs Cleanup

## Purpose

Classify documentation files (issues, ADRs, decision records, temporary feature briefs,
incident notes) by
long-term value, propose safe cleanup actions, and protect against false-positive
deletion. Deletion is destructive and irreversible — it always passes through an
explicit operator review gate.

This skill is the **orchestrator** for the audit. The actual reading of file bodies
happens in subagents to keep the orchestrator's context light: it works with a small
JSON table of verdicts rather than the contents of 20-40 files.

## Workflow

The full path: **discovery → enumerate → classify → gate (delete subset only) →
apply → report**.

### Step 1 — Discover the documentation set

Read `../_shared/repository-discovery.md` to locate the relevant docs directories
(`docs/issues/`, `docs/adr/`, monorepo equivalents, plus less-common locations like
`notes/`, `decisions/`, `runbooks/`). Confirm scope with the user when ambiguous —
auditing all of a monorepo's docs without checking is the most common way to waste a
session.

### Step 2 — Enumerate candidates

List every `.md` file under the confirmed scope, excluding `archive/` subdirectories
(those have already been processed). This is just a `find` — no body reading yet.

### Step 3 — Classify

The classification is the expensive step (every file body must be read). Two paths:

- **≤ 10 candidates** → classify inline. Read each file, apply
  `references/value-criteria.md`, produce the verdict table.
- **> 10 candidates** → launch generic read-only subagents using
  `references/classifier-method.md`. Each subagent reads its method, criteria, and file bodies
  in its own context and returns compact JSON. The orchestrator never reads the bodies — it
  works only with the tables. See "Subagent contracts" below.

### Step 4 — Compose with sibling skills

Before presenting the gate, scan the verdict table for items that belong in a
sibling skill's flow:

- `promote-to-adr` verdicts → recommend `adr-writer:from-issue` (which has the
  promote workflow with merge support; it also deletes the source issues after the
  ADR is saved, with explicit operator confirmation).
- Closed issues with no ADR-worthy content (verdict `delete` on `[CLOSED]` files
  in `docs/issues/`) → recommend `issue-writer:close` (which has the proper sweep
  workflow with mismatch detection and a mandatory pre-extraction check that catches
  any leftover documentation value).
- `close` verdicts (open or implementing issues that are actually fixed in the codebase) →
  after the operator renames them to `[CLOSED]` and updates the body, the next
  `issue-writer:close` sweep handles them.
- `stale` verdicts (open issues whose premises no longer match current evidence, but whose
  completion is unverified) → recommend updating `Last reviewed` and adding an evidence-based
  `Stale note`; keep `Status: Open`.
- Completed temporary feature briefs with durable behavior → keep the `repair` verdict, route that
  value to the existing living contract through `$contract-writer`, then use the normal delete
  gate. If the contract is `missing`, request separate operator approval before creating a file.
  Do not promote feature description to ADR without an independently significant architectural
  decision with alternatives and rationale.

Don't invoke these directly — surface as text recommendations in the report so the
user picks the order of operations.

### Step 5 — Delete review gate

For every `delete` verdict, launch a generic read-only subagent using
`references/pre-delete-method.md` on each candidate. It verifies:

- No incoming references from other docs, code comments, indexes
- Content is not unique (rationale, evidence, commands, logs not preserved elsewhere)
- A safer alternative (`repair` / `close` / `stale` / `merge` / `supersede` /
  `promote-to-adr`) doesn't fit better

Only after pre-checks come back does the orchestrator present the gate per
`references/delete-gate.md`. **Wait for explicit approval** before any deletion.

### Step 6 — Apply approved actions

Per `references/delete-gate.md` rules: only delete explicitly approved paths, never
globs or directories. For non-delete actions (repair, close, stale note, supersede,
merge headers),
apply them only with explicit operator instruction; the orchestrator's job by default
is to *recommend*, not to mutate.

### Step 7 — Report

Use the formats in `references/output-formats.md`. Always include counts by label,
hand-off recommendations to sibling skills, and any items skipped (with reason).

## Subagent contracts

Resolve absolute paths from the loaded skill directory and pass them to generic exploration or
read-only subagents. For classification, pass `references/classifier-method.md`,
`references/value-criteria.md`, candidate paths, repo root, and compact scope context. For a
delete check, pass `references/pre-delete-method.md`, one candidate path, repo root, and scope
context. Instruct subagents to read the method files themselves and return JSON only; do not
inline methods or document bodies into the orchestrator prompt. Use platform-level read-only
permissions when available. No registered agent name or vendor model alias is required.

### When to spawn

| Subagent             | When                                                            |
|----------------------|-----------------------------------------------------------------|
| Classifier method  | More than 10 candidates after enumeration.                       |
| Pre-delete method | Always, for every `delete` candidate, before the gate.           |

For audits with ≤ 10 candidates, classify inline — the subagent overhead doesn't
pay off. The pre-delete method still runs (per-candidate, in parallel if multiple),
because the gate's safety guarantee depends on it.

## Design notes

- Repository discovery and durable-value routing are shared across this coordinated skill set;
  classification and deletion gates remain local.
- Generic method-based subagents keep file bodies out of the orchestrator context and work
  across clients without registered Claude agents or model aliases.
- Boundary between this skill and its siblings is **textual recommendations**, not
  direct invocation. `docs-cleanup` writes "these 6 fit `issue-writer:close`",
  the user runs that next. Avoids tight coupling and lets the user reorder.
- Boundary with `adr-auditor`: that skill goes *deeper* on ADR semantics (drift
  against code, immutability violations, coverage gaps); this one goes *wider*
  across issues, runbooks, and notes with shallower per-type checks. When the user
  asks for the ADR corpus specifically, hand off to `adr-auditor`; ADRs swept up
  here get only the shallow value-classification, not the semantic audit.
- Delete gate is non-skippable, even when the user's request sounds categorical
  ("just clean it up", "they're definitely stale"). The cost of one round-trip is
  trivial compared to losing a unique evidence file by accident.
