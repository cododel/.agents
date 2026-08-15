---
name: adr-auditor
description: "Audit the quality, relevance, and code drift of an existing ADR corpus. Use for `audit our ADRs`, `проанализируй ADR`, `check ADR drift`, explicit milestone or release ADR review, or requests to tidy stale/dead ADRs. Diagnose by default. Do not use to create an ADR from a conversation or issue; use `adr-writer`."
---

# ADR Auditor

## Purpose

Run over a project's ADR corpus, measure it against the quality contract in
`../adr-writer/references/adr-spec.md`, and produce a **diagnosis plus a remediation
plan** — which ADRs drifted from the code, which are hollow, which supersession chains
are broken, which major decisions have no ADR at all, and where an ADR is incorrectly
serving as the only current-state contract.

This is the **review-time twin** of `adr-writer`. The writer *enforces* the spec when a
decision is captured; the auditor *measures* an existing corpus against the same spec.
One definition, two applications — they read the same `adr-spec.md` so "how we write" and
"how we audit" never drift apart.

The skill is an **orchestrator**. Reading ADR bodies and cross-checking them against code
happens in subagents (for larger corpora) to keep the orchestrator's context light: it
works with a compact table of findings, not the contents of 30 files. Every mutating fix
is a *recommendation* until the operator approves it at the gate — the auditor diagnoses
by default and mutates only on explicit instruction.

## Input and output

- **Input:** the ADR files (`docs/adr/` or its equivalents) **and the codebase**. Unlike
  `adr-writer:from-chat`, there is no conversation to draw on — the evidence is the
  documents and the code they claim to describe.
- **Output:** a diagnosis report (per-ADR findings + corpus findings) and a gated list of
  remediation actions. Nothing is mutated or deleted without explicit approval.

## Quality contract

The criteria live in `../adr-writer/references/adr-spec.md` — the same file `adr-writer`
uses. `references/audit-criteria.md` reads it and adds the **review-time specifics** that
only apply when auditing an existing corpus (drift-vs-code, immutability-via-git,
reverse-coverage). Read both before classifying. This skill is not standalone: it depends
on `adr-writer/` being installed alongside it for the spec.

## Workflow

The full path: **discover → enumerate → per-ADR audit → corpus audit → gate → remediate
→ report**.

### Step 1 — Discover the ADR set

Read `../_shared/repository-discovery.md` to locate the ADR directories (`docs/adr/`, monorepo
per-app equivalents, infra-specific ones). Read each directory's `README.md` to learn the
**local convention** — its status taxonomy, filename pattern, and routing rules win over
the fallback template, and the audit must judge ADRs against *their own* project's
convention, not impose one. Confirm scope with the user when several ADR roots exist.

### Step 2 — Enumerate

List every ADR file under the confirmed scope (a `find`, no body reading yet). Note the
filename-encoded status/percent prefixes — they're a cheap first signal of staleness.

### Step 3 — Per-ADR audit

The expensive step: each ADR body is read and checked against the per-ADR criteria
(`adr-spec.md` §3) plus the review-time specifics in `references/audit-criteria.md`. Two
paths:

- **≤ 10 ADRs** → audit inline. Read each, apply the criteria, build the findings table.
- **> 10 ADRs** → split candidates into bounded batches and launch generic read-only
  subagents using `references/adr-classifier.md` as their method. Each subagent reads ADR
  bodies and quality references in its own context, cross-checks against code, and returns
  compact JSON. Run independent batches in parallel when the client supports it. The
  orchestrator works only from the returned tables. See "Subagent contract" below.

Per-ADR checks include: one-decision, valid/true status, real alternatives,
**decision-still-holds (drift vs code)**, concrete reasons, **immutability respected (git
history)**, honest consequences, self-sufficiency, decision invariants captured, and
ADR-as-contract ownership leaks.

### Step 4 — Corpus audit

The cross-file checks (`adr-spec.md` §6), which no per-file pass can see:

- supersession chains intact (no orphaned `Superseded`/`Superseded by` links);
- **coverage / reverse audit** — major decisions visible in the code (DB, auth, deploy,
  framework, package manager) that have *no* ADR at all;
- duplicates / conflicts (two un-reconciled ADRs on the same area);
- placement vs the routing convention;
- naming/ID consistency and collisions;
- density/cadence and staleness distribution.

The reverse-coverage audit is the highest-value, least-obvious check — see
`references/audit-criteria.md`.

### Step 5 — Operator gate

Present the diagnosis per `references/output-formats.md`, then the remediation plan as a
**gate**. Mutating actions (status flips, adding links, moving files, splitting ADRs) and
especially any deletion require explicit approval. **Wait for it.** ADRs are append-only
memory — an accidental rewrite or delete loses history that can't be reconstructed.

### Step 6 — Remediate (only approved actions)

Apply per `references/remediation.md`, honoring ADR immutability: a drifted decision is
fixed by **issuing a successor** (hand off to `adr-writer`) and marking the old one
`Superseded`, never by rewriting its body. Only the append-only edits (status flip,
relationship link, refresh note, placement move) are applied directly.

### Step 7 — Report

Use `references/output-formats.md`: counts by finding, the remediation actions taken,
hand-offs to sibling skills, and anything skipped (with reason).

## Subagent contract

When **more than 10 ADRs** are in scope, resolve these paths from the loaded skill directory:

- `references/adr-classifier.md`
- `references/audit-criteria.md`
- `../adr-writer/references/adr-spec.md`

Launch a generic exploration/read-only subagent for each batch. Pass the absolute method path,
both absolute criteria paths, candidate paths, repo root, and compact local-convention text.
Instruct the subagent to read those files itself and return JSON only. Do **not** inline the
method, criteria, or ADR bodies into the task prompt: path-based loading is what keeps them out
of the orchestrator context. Use platform-level read-only permissions when available.

No registered custom-agent name or model alias is required. A cheaper capable model may be
selected by client configuration, but correctness must not depend on a vendor-specific model
field. For 10 or fewer ADRs, audit inline because delegation overhead does not
pay off.

## Composition with sibling skills

Boundary with siblings is **textual recommendation, not direct invocation** (the
repository convention) — surface hand-offs in the report and let the user order them:

- **`adr-writer`** — when an ADR has drifted (code moved on) or a major decision has no
  ADR, the fix is a *new* ADR. Recommend `adr-writer` (from-chat if the user can supply
  the reasoning, from-issue if it's buried in a resolved issue). The auditor itself only
  flips the old one to `Superseded`/`Deprecated` and wires links once the successor exists.
- **`contract-writer`** — when current behavior or architecture exists only in an ADR,
  report contract impact as `missing`; when a living contract exists but provenance is
  one-way, recommend a relationship-link backfill. Contract creation remains separately
  operator-approved.
- **`docs-cleanup`** — the broad, all-doc-types audit. `adr-auditor` goes *deeper* on ADR
  semantics (drift, immutability, coverage); `docs-cleanup` goes *wider* across issues,
  runbooks, and notes with shallower per-type checks. When the user wants the whole docs
  tree triaged, point them there; when they want the ADR corpus specifically diagnosed and
  repaired, this is the skill. Overlap on `supersede`/`repair`/`promote-to-adr` verdicts is
  intentional — the two reach the same conclusions from different depths.

## Design notes

- **Shared spec, not a copy.** The criteria are read from
  `../adr-writer/references/adr-spec.md` rather than duplicated here. This is the one place
  the autonomy-via-duplication convention is deliberately broken: the whole point of the
  spec is a *single* definition both skills obey. The cost is that `adr-auditor` is not
  standalone — it needs `adr-writer` installed beside it.
- Repository discovery is shared with the sibling lifecycle skills; audit criteria and
  remediation remain local.
- Generic read-only subagents keep bulk ADR bodies out of the orchestrator context. The method
  is a reference file rather than a registered agent, so the workflow works in both Claude Code
  and OpenCode.
- **Diagnose-by-default.** The auditor's job is to produce a report and a plan. It mutates
  only on explicit operator instruction, and it never rewrites an ADR body — drift is fixed
  by succession, per `adr-spec.md` §1.
