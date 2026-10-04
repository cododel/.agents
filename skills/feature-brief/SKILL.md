---
name: feature-brief
description: "Resolve material feature requirements or architecture forks through repository-grounded discussion, using a structured planning surface when available; optionally record the agreed task. Not for an ordinary implementation plan or a clear request, regardless of size."
---

# Feature Brief

Resolve material product or architecture ambiguity into an actionable agreed task. A clear request,
regardless of size, needs no interview. An implementation plan describes execution; the agreed task
preserves the intended result.

## Ground the forks

Before asking, resolve the repository, affected surface, instructions, current behavior, nearby
schemas/tests, and established contracts. Research repository-discoverable facts and objective
implementation choices; use `$find-docs` for unverified external semantics. Ask only about alternatives
that materially change behavior, stable boundaries, scope, risk, migration, or acceptance.

For an interview, read [references/briefing.md](references/briefing.md). Use an exposed planning/question
surface within its actual limits and current collaboration mode. If unavailable or disallowed, use
focused plain-chat questions where applicable instructions permit them. Do not start another app or
create a second plan file solely for this skill.

A recommended default, recorded assumption, or unanswered question is not agreement. Planning or
briefing intent authorizes investigation and the requested plan; product implementation and external
writes require their own authorization.

## Record and continue

When requirements, decisions, or handoffs become hard to retain, or a record is requested, use
[$task-journal](../task-journal/SKILL.md) directly. It owns the shared `task.md`, templates, storage,
confirmed changes, and separate execution state. No separate default brief is needed; a requested
export is a deliverable rather than another maintained task owner.

When choosing acceptance evidence, use [testing-evidence](../testing-evidence/SKILL.md) and the
project testing profile; agreed behavior stays the source of acceptance, not the latest green tests.
A temporary PoC/operator demo may answer an API/design/UX fork before production integration; use
[experiments](../testing-evidence/references/experiments.md) for its bounded evidence procedure.

Once material forks are resolved, continue the explicitly requested planning or implementation.
Update existing normative owners when agreed guarantees change; use `$contract-writer` for a new
owner only under its value test. Use `$adr-writer` only on a request to record a significant decision
the operator actually made. Stop the affected work for an unresolved contract or architecture fork.

Report the confirmed target, remaining material questions, and whether task memory was created.
