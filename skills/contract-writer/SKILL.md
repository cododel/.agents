---
name: contract-writer
description: "Inspect, classify, create, or update living project contracts for current product, UI, API, domain, persistence, security, and architecture behavior. Use for `write/update the contract`, `опиши/обнови контракт`, contract-impact checks, or work that must synchronize established behavioral or architectural contracts. Do not use for implementation-compliance or rollout-readiness reviews (`contract-auditor`), decision history (`adr-writer`), temporary feature agreements (`feature-brief`), plans, or broad cleanup (`docs-cleanup`)."
---

# Contract Writer

## Purpose

Maintain the normative current-state documentation that implementations must satisfy. Keep decision
history in ADRs and temporary scope agreements in briefs.

Route requests to review whether implementation satisfies existing contracts, including final or
production-readiness reviews, to `$contract-auditor`. This skill owns the documents, not the
read-only compliance verdict.

## Modes

| Intent | Mode | Mutation |
|:--|:--|:--|
| Locate the governing contract and language | discovery | Read-only |
| Classify a proposed change against that owner | impact assessment | Read-only |
| Change an established contract with approved behavior work | update | Covered by that work |
| Create a missing durable contract | create | Requires explicit operator approval for scope and path |

Read `references/contract-spec.md` before classifying or writing. Read
`references/workflow.md` for discovery, language, path, linking, and verification steps. Use
`assets/contract-template.md` only when no stronger local format exists.

## Grounding

1. Resolve the repository boundary and read applicable instructions and documentation indexes.
2. Use `../_shared/repository-discovery.md` to prove contract scope; a familiar filename is not
   proof.
3. Inspect current code, tests, schemas, and relevant ADRs as evidence, but do not promote them to a
   living contract unless the project explicitly assigns that role.
4. Classify impact as `unchanged`, `extend`, `conflict`, or `missing`.

Project-local conventions override every fallback in this skill. Preserve one normative owner per
rule and use links instead of copying requirements across contracts, indexes, ADRs, or runbooks.

## Authority gates

- Update an established contract when an explicitly requested behavior or interface change extends
  it.
- Stop on `conflict` for an operator decision.
- On `missing`, propose the contract scope and exact path, then wait for explicit approval before
  creating it. An implementation request alone does not open this gate.
- Never create translations or update translated siblings unless the applicable project
  `AGENTS.md` explicitly requires multilingual documentation.
- Never rewrite an Accepted ADR body. Relationship backfills and status changes follow the ADR
  workflow; changed decisions require a successor ADR.

## Report

State the proven contract owner and language, impact classification, files created or updated,
verification performed, and any open operator gate. Do not claim that an ADR or regression test is
itself the missing living contract.
