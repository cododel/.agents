# ADR classifier method

Use this method for a bounded, read-only ADR batch delegated by `$adr-auditor`. Read the supplied
quality specification and audit criteria before inspecting records. Return evidence, not rewritten
history.

## Required input

The primary agent supplies:

- `candidates`: exact ADR paths;
- `scope_context`: repository root, confirmed ADR convention, and any narrowed audit scope;
- `criteria_paths`: absolute paths to `adr-writer/references/adr-spec.md` and
  `adr-auditor/references/audit-criteria.md`.

If a required input or criterion file is missing, return a structured error instead of improvising a
yardstick.

## Per-record method

1. Read the ADR in full and identify its stated decision, status, alternatives, rationale,
   consequences, assumptions/invariants, relationships, and current-contract link.
2. Check whether it records a real operator decision rather than reconstructing history from code.
   Flag bundled decisions, unsupported rationale, decorative alternatives, vague rejection reasons,
   dishonest consequences, or an unresolved core `TODO:` in an Accepted record.
3. Extract concrete anchors: paths, symbols, dependencies, providers, services, configuration keys,
   data shapes, event guarantees, and decision invariants. Verify decisive anchors in current source
   or configuration.
4. Classify current-state evidence carefully:
   - `drift`: implementation demonstrably follows a different choice;
   - `stale-invariant/code-defect`: implementation violates a choice that may still be intended;
   - `area-removed`: the decision surface no longer exists;
   - `ambiguous`: evidence cannot distinguish these states.
   A missing path proves at most link drift until the underlying choice is traced.
5. When Git history is available, inspect `git log --follow -p <path>`. For Accepted/Superseded ADRs,
   substantive post-acceptance changes to Context, Options, Decision, or Consequences are
   immutability findings. Status/link metadata and append-only review notes are allowed.
6. Check lifecycle truth and relationships. Implemented code alone does not prove that a Proposed
   choice was operator-accepted. Supersession links must resolve in both directions.
7. Report `adr-as-current-contract` only when the ADR is the sole normative owner of current behavior
   that maintainers must preserve. Tests, schemas, types, and README summaries are not silently
   canonical unless project instructions declare them so.
8. Record the exact evidence for every finding. When evidence is insufficient, return ambiguity or no
   finding; never invent a historical choice or rationale.

The batch agent may read directly linked ADRs and decisive source/history evidence. Corpus-wide
conflict, density, naming, and chain checks remain with the primary auditor.

## Output schema

Return one JSON object per input path, in order:

```json
[
  {
    "path": "/abs/docs/adr/ADR-20260801-auth-boundary.md",
    "title": "Use service-owned sessions",
    "status": "Accepted",
    "relationships": {
      "supersedes": [],
      "superseded_by": [],
      "related": [],
      "current_contract": "docs/contracts/AUTH_CONTRACT.md"
    },
    "anchors": [
      {"kind": "symbol", "value": "SessionService", "state": "present"}
    ],
    "findings": [],
    "recommended_action": "none",
    "immutability": "clean",
    "ambiguous": false
  }
]
```

Field rules:

- `findings`: `{criterion, severity, evidence, uncertainty?}` entries. Use criteria such as
  `drift`, `stale-invariant/code-defect`, `area-removed`, `status-untrue`,
  `unsupported-rationale`, `hollow-alternatives`, `vague-reasons`, `bundled-decisions`,
  `dishonest-consequences`, `invalid-status`, `broken-relationship`,
  `immutability-violation`, `adr-as-current-contract`, or `ambiguous`.
- `severity`: `high | medium | low`. Every finding needs one concise evidence sentence with a stable
  source pointer or commit hash when relevant.
- `anchors`: each extracted anchor plus `present | missing | replaced | ambiguous`. Do not treat a
  missing anchor as automatic decision drift.
- `recommended_action`: one primary label from `remediation.md`:
  `add-link`, `flip-status`, `mark-superseded`, `mark-deprecated`, `normalize`,
  `write-successor`, `split`, `flag-hollow`, `confirm-candidate`,
  `establish-current-contract`, `fix-code-or-contract`, or `none`.
- `immutability`: `clean | violated | skipped-no-git`.
- `ambiguous`: `true` when the material classification cannot be supported confidently.

## Boundaries

- Read-only: no edits, moves, deletes, or generated ADRs.
- Do not treat every framework, database, provider, or cross-cutting implementation as a missing ADR.
  Code proves current state, not an operator decision or its rationale.
- Recommend a successor only when a changed operator decision is evidenced. Otherwise surface the
  need for operator history or route a violated invariant to implementation/contract review.
- Keep output compact. The primary agent owns corpus integration, operator gates, and any mutation.
