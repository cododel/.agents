# Brief workflow

Use this mode to create or revise the temporary feature contract.

## 1. Establish sufficient context

Read the complete relevant conversation, repository evidence, current living project contracts, and an
existing brief when updating one. If a missing answer would materially change the feature, conduct
the briefing workflow first. Keep unresolved non-blocking questions explicit rather than inventing
answers.

## 2. Resolve the path

Prefer a proven repository convention specifically for temporary briefs or draft feature
contracts. Otherwise use:

```text
<repo-root>/.agents/briefs/YYYY-MM-DD-english-kebab-slug.md
```

Keep the original date and path when revising a brief. Never add the fallback directory to an
index or `.gitignore`, and never stage or commit the brief without an explicit request.

## 3. Draft the contract

Copy `assets/brief-template.md` and preserve the operator's language. Write testable behavior,
not implementation choreography. Separate:

- repository-observed facts;
- decisions explicitly made by the operator;
- assumptions that remain falsifiable;
- open questions that prevent or constrain agreement.

Classify `Contract Impact` as exactly one or more of:

- `unchanged` — existing durable contracts already allow the feature;
- `extend` — identified contracts need additions;
- `conflict` — the proposal contradicts an existing contract and needs an operator decision;
- `missing` — durable behavior may need a new contract, subject to the anti-bureaucratic value test.

Name proven contract paths for `extend` or `conflict`. Do not fabricate a target for `missing`.

## 4. Review and agreement

Create or update the document as `Draft` and hand back its resolved path. Incorporate operator
comments as another revision. Change status to `Agreed` only after the operator explicitly confirms
the current document.

Do not mark a brief `Agreed` while a `conflict` or another implementation-invalidating question
remains. If an agreed brief changes materially, set it back to `Draft` before editing the affected
scope, behavior, constraint, or acceptance criterion.

Brief creation and agreement do not themselves authorize implementation. Follow the operator's
separate implementation request and normal mutation gates.

## 5. Completion handoff

When implementation finishes:

1. verify observable behavior against `Acceptance Criteria`;
2. synchronize `extend` changes with the existing living contract via `$contract-writer`;
3. stop and resolve `conflict`; for `missing`, request separate operator confirmation before
   `$contract-writer` creates a new file;
4. use an ADR only for a significant architectural choice with real alternatives and rationale;
5. offer the exact temporary brief path for operator-approved deletion after extraction.
