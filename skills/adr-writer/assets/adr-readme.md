# Architecture Decision Records

This directory contains durable records of significant architectural decisions.

## Naming

Use `ADR-YYYYMMDD-<english-kebab-decision>.md` unless the repository establishes a stronger
local convention.

## Lifecycle

Use `Proposed`, `Accepted`, `Deprecated`, and `Superseded` as decision states. Accepted ADRs are
append-only historical records: when reality changes, write a successor and link both records
instead of rewriting the old rationale.

## Required Content

An ADR captures one significant decision, its context, considered alternatives, concrete
rejection reasons, the chosen outcome, consequences, and material assumptions/invariants. A
description of implementation without a consequential operator choice is not an ADR. An Accepted
record must contain its load-bearing rationale; missing history is a candidate for operator input,
never invented best-practice prose.

## Placement

System-wide decisions live here. A repository may establish module-local or infrastructure ADR
directories when ownership is narrower; project instructions always override this fallback.
