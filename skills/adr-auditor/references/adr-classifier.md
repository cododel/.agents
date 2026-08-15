# ADR Classifier Method

Use this file as the complete task method for a generic read-only subagent launched by the
`adr-auditor` skill. The subagent's job is to read a batch of
ADRs, measure each against the quality criteria, cross-check it against the code and git
history, and return a structured findings table. You are **read-only**: no file writes, no
edits, no deletes, no moves. The orchestrator handles all mutations after operator approval.

## Input you will receive

The orchestrator passes:

1. **`candidates`** — a list of ADR file paths (absolute) to audit.
2. **`scope_context`** — text containing:
   - The confirmed ADR directories and each one's local convention (filename pattern,
     status taxonomy, routing rules) from its `README.md`.
   - The repo root, so you can grep the codebase and run `git log`.
   - Any user instruction narrowing the audit.
3. **`criteria_paths`** — absolute paths to `adr-writer/references/adr-spec.md` (the quality
   contract) and `adr-auditor/references/audit-criteria.md` (the review-time specifics).
   Read and apply both inside the subagent context. If either file is not found, return an
   error — without them you have no yardstick.

If any input is missing:

```json
{"error": "missing_input", "missing": ["criteria_paths.adr-spec"], "expected": "..."}
```

## What to do, per ADR

1. **Read the ADR in full.** Don't sample.
2. **Document-only checks** (`adr-spec.md` §3): one decision vs bundled; valid status
   value; real vs decorative/absent alternatives; concrete vs vague rejection reasons;
   honest vs all-upside consequences; self-sufficient vs references to ephemeral context;
   decision invariants captured vs missing.
3. **Drift check** (`audit-criteria.md`): extract the ADR's concrete anchors (paths in
   `Implementation:`, libraries, providers, services, config keys, invariant rules). Grep
   the codebase for each. Decision **holds** if anchors are present and used; **drifted**
   if the underlying choice is demonstrably gone or replaced. A missing `Implementation:` path
   is a strong signal to trace, not automatic drift: it may be a pure relocation.
   Distinguish drift (reality moved on → succession) from a violated-but-valid invariant
   (a code bug / coverage gap, not an ADR fault) — say which.
4. **Immutability check** (`audit-criteria.md`): for `Accepted`/`Superseded` ADRs, run
   `git log --follow -p <path>`, identify the commit where the ADR became accepted, and look
   for substantive rewrites of Context/Options/Decision after that point. Changes while the
   ADR was still `Proposed` are not violations. Append-only changes (Refresh notes, status flips,
   link back-fills) are legitimate and are **not** findings. A post-acceptance rewrite of
   the reasoning **is** a finding. If the file isn't in git, skip this check and say so.
5. **Status truth**: is the status not just valid but *true* given drift and the code?
   (`Accepted` but drifted → de-facto dead; `Proposed` but shipped → should be `Accepted`.)
6. **Current-contract ownership** (`audit-criteria.md`): discover declared living or
   executable contracts. If the ADR is the only normative owner of durable current behavior or
   architecture, record `adr-as-current-contract`; do not infer an owner from tests, schema,
   types, or README summaries.
7. **Record evidence.** Every finding quotes the actual signal — a code path that
   contradicts the ADR, a git commit hash that rewrote it, the verbatim vague line. Never
   assert a finding you can't show. When genuinely unsure, mark `ambiguous`.

You may read additional files for context (the successor ADR a `Superseded by:` points to,
the code an `Implementation:` link references). Don't exhaustively scan the repo for
corpus-level checks — supersession-chain integrity, reverse-coverage gaps, and conflicts
are computed by the orchestrator across the full set, not per file.

## Output format

A single JSON array, one object per candidate, in input order:

```json
[
  {
    "path": "/abs/docs/adr/ADR-20251101-auth-clerk.md",
    "title": "ADR: Use Clerk for authentication",
    "status": "Accepted",
    "relationships": {
      "supersedes": [],
      "superseded_by": [],
      "related": [],
      "current_contract": null
    },
    "anchors": [
      {"kind": "path", "value": "lib/clerk.ts", "state": "missing"},
      {"kind": "replacement", "value": "lib/session/", "state": "present"}
    ],
    "findings": [
      {"criterion": "drift", "severity": "high", "evidence": "Implementation: → lib/clerk.ts is gone; auth now in lib/session/*.ts (no clerk import anywhere in src/)"},
      {"criterion": "status-untrue", "severity": "high", "evidence": "Accepted but the decision it records is no longer how auth works"}
    ],
    "recommended_action": "write-successor",
    "immutability": "clean",
    "ambiguous": false
  },
  {
    "path": "/abs/docs/adr/ADR-20250903-db-choice.md",
    "title": "ADR: PostgreSQL as primary store",
    "status": "Accepted",
    "relationships": {
      "supersedes": [],
      "superseded_by": [],
      "related": [],
      "current_contract": null
    },
    "anchors": [],
    "findings": [
      {"criterion": "hollow-alternatives", "severity": "medium", "evidence": "Section 2 lists only PostgreSQL; no rejected options and no stated reason none existed"},
      {"criterion": "missing-decision-invariants", "severity": "low", "evidence": "no Decision Invariants/Constraints section despite a lasting condition on the recorded persistence choice"},
      {"criterion": "adr-as-current-contract", "severity": "medium", "evidence": "the Accepted ADR is the only normative owner found for current persistence behavior; no living or declared executable contract exists"}
    ],
    "recommended_action": "flag-hollow",
    "immutability": "clean",
    "ambiguous": false
  }
]
```

Field rules:

- `findings` — list of `{criterion, severity, evidence}`. `criterion` is a spec-derived
  tag: `drift`, `status-untrue`, `hollow-alternatives`, `missing-decision-invariants`,
  `adr-as-current-contract`,
  `vague-reasons`, `not-self-sufficient`, `bundled-decisions`, `dishonest-consequences`,
  `invalid-status`. `severity` is `high|medium|low`. `evidence` is one sentence quoting
  the real signal. **Required** for every finding.
- `relationships` — normalized ADR paths or identifiers copied from `Supersedes`,
  `Superseded by`, `Related`, and `Current contract` fields. Use empty arrays or null
  when absent.
- `anchors` — concrete implementation paths, libraries, providers, services, config keys,
  or invariant symbols extracted from the ADR, each with a `present`, `missing`, `replaced`,
  or `ambiguous` state. This lets the orchestrator perform corpus checks without rereading bodies.
- An ADR with no problems → empty `findings`, `recommended_action: "none"`.
- `recommended_action` — one label from `remediation.md`: `mark-superseded`,
  `mark-deprecated`, `write-successor`, `add-link`, `flip-status`, `flag-hollow`, `split`,
  `relocate`, `fill-coverage`, `establish-current-contract`, `normalize`, or `none`.
  Pick the primary one.
- `immutability` — `clean | violated | skipped-no-git`. If `violated`, include a finding
  with the offending commit hash in evidence.
- `ambiguous` — `true` when you can't confidently classify (e.g. drift vs code-bug); put
  the reason in a finding with `criterion: "ambiguous"`.

## Constraints

- **Read-only.** No writes, edits, deletes, moves. Not even fixing an obvious typo.
- **Don't fabricate findings.** A finding must quote a real signal. "Feels stale" is not a
  finding. No matched signal → empty findings or `ambiguous`, never an invented one.
- **Don't fabricate the fix either.** You recommend an action label; you never author the
  successor ADR or invent missing rationale. That's a hand-off the orchestrator surfaces.
- **One object per file.** Multiple findings on one ADR go in its `findings` array, not
  split rows.
- **Evidence is one sentence.** The operator reads the ADR themselves for detail.
- Honor scope narrowing in the brief ("only infra ADRs", "skip anything < 30 days old").

## Boundaries

- You are not the corpus pass. Chain integrity, coverage gaps, conflicts, and
  naming/placement across the set are the orchestrator's job — you provide the per-ADR
  rows it needs (status, links present, anchors), not the cross-file verdict.
- You are not the operator gate. Your output is the gate's input, not the gate.
- You do not mutate. Every `recommended_action` is a proposal the operator approves first.
