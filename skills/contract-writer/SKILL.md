---
name: contract-writer
description: "Create or update lightweight living contracts for non-obvious stable behavior and ownership boundaries. Use when agreed guarantees change or a lasting obligation lacks a suitable owner; ask only when the contract would choose unresolved semantics."
---

# Contract Writer

Maintain the smallest normative documentation layer that protects stable behavior and ownership seams
which code and tests cannot communicate reliably on their own.

A living contract answers **what this boundary guarantees and owns now**. It is not a full project
specification, implementation plan, test plan, or architecture history.

## When a contract has value

Update an established normative owner when agreed guarantees change. Create a new owner only when
all four conditions in `references/contract-spec.md` hold: established lasting obligation, material
consequence, insufficient expression in existing code/docs, and no suitable owner to update.
A feature, local change, or completed task does not by itself justify a new contract.
Existing normative API/schema/docs may suffice; do not duplicate them in a separate Markdown file.

## Modes

| Intent/state | Mode | Authority |
|:--|:--|:--|
| Locate the current normative owner | discovery | read-only |
| Classify proposed/implemented behavior | impact | read-only |
| Align an established owner with explicit behavior | update | local reversible work |
| Establish a missing owner for already-explicit stable behavior | create | local reversible work |
| Contract would decide unclear behavior/scope/ownership | decision gate | stop for operator |

Read `references/contract-spec.md` before classifying or writing and
`references/workflow.md` for discovery, path, language, linking, and verification. Use the fallback
template only when no stronger local convention exists.

## Classification

Classify relevant stable behavior as:

- `unchanged` — the current owner already permits and explains it;
- `extend` — an established owner needs a normative addition/narrowing;
- `conflict` — requested behavior contradicts an established owner and requires an operator decision;
- `missing` — all four value conditions hold and no suitable owner exists.

`missing` is not an automatic approval gate. Create the contract only after the value test passes
and behavior and ownership are unambiguous from established obligations plus implementation evidence.
Ask only when writing the document
would select among materially different semantics, boundaries, languages, or canonical homes.

## Grounding and anti-drift

1. Resolve repository/documentation scope through `../_shared/repository-discovery.md`.
2. Read the complete relevant contracts and representative local examples.
3. Inspect current code, tests, schemas, event flows, and relevant ADRs as evidence.
4. Separate normative behavior from implementation details and historical rationale.
5. Keep each rule in one canonical owner and link from tests, ADRs, indexes, and related contracts.

Verify the normative role of existing API/schema/docs from project declarations or established use.
Tests and incidental types alone do not establish adjacent product or architecture obligations.

## Decision boundary

Proceed autonomously when the contract merely records already-established behavior. Stop when it would:

- choose which module/service owns a responsibility;
- introduce a new invariant or compatibility promise;
- resolve contradictory code/docs/operator statements;
- select between co-equal documentation locations or languages;
- convert a temporary implementation detail into a stable public commitment.

An ADR remains operator-decision history. Never manufacture alternatives/rationale or rewrite an
Accepted ADR body.

## Handoff

Report the impact classification, semantic contract change, evidence used, verification, and any true
operator fork. Do not repeat the whole contract or present contract creation as proof that the
implementation is correct.
