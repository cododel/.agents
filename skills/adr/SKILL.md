---
name: adr
description: "Record significant agreed architecture decisions or audit existing ADRs for quality, drift, lifecycle and immutability. Select recording, audit or authorized remediation by intent; not ordinary task closure or implementation compliance auditing."
---

# Architecture Decision Records

Preserve evidenced operator decisions and assess their history without inventing agreement.
Read [the specification](references/adr-spec.md) for significance, lifecycle, immutable reasoning,
and relationships to current contracts. Load only the procedure selected by the request:

| Intent | Procedure | Authority boundary |
| --- | --- | --- |
| Record a significant established decision from discussion or an in-scope Issue | [Recording](references/write.md), then its selected from-chat/from-issue procedure | Authorized recording or implementation/documentation scope; planning alone does not authorize writes |
| Review ADR quality, drift, relationships or immutability | [Audit](references/audit.md) | Read-only; findings do not authorize recording or repair |
| Repair established metadata, links or placement after diagnosis | [Remediation](references/remediation.md) | Explicit remediation scope; reasoning changes require a real new decision and successor |

An implementation shape cannot establish historical agreement. Task closure does not require an ADR.
A mode transition preserves the actual request's authority; loading this skill grants none.
