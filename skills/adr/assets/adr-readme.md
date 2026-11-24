# Architecture Decision Records

This directory contains durable records of significant architectural decisions.

## Naming

Use `ADR-YYYYMMDD-<english-kebab-decision>.md` unless the repository establishes a stronger
local convention.
The fallback uses the actual decision date when known, otherwise the recording date for filename
identity. The body keeps `Decision date` and `Recorded` separate; never invent a historical date.

## Lifecycle

Use `Proposed`, `Accepted`, `Deprecated`, and `Superseded` as decision states. Accepted ADRs are
append-only historical records: when reality changes, write a successor and link both records
instead of rewriting the old rationale.

## Required Content

One paragraph is sufficient when a future reader can understand the significant decision and its
reason. Preserve consequential trade-offs and the conditions that would warrant revisiting the
decision. Record only choices and reasons supported by their source.

## Placement

System-wide decisions live here. A repository may establish module-local or infrastructure ADR
directories when ownership is narrower; project instructions always override this fallback.
