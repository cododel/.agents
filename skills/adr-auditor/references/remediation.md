# ADR remediation

Accepted ADR reasoning is immutable. Repair metadata and links directly only after an explicit
remediation request; changed decisions require real operator rationale and a successor.

| Action | Use when | Result |
|:--|:--|:--|
| `add-link` | missing inverse relationship or dead link with a proven target | append/fix relationship metadata |
| `flip-status` | lifecycle truth is established from decision evidence | update status only |
| `mark-superseded` | successor already exists and relationship is proven | status + bidirectional links |
| `mark-deprecated` | decision area is gone with no direct successor | status + concise append-only note |
| `normalize` | filename/date/placement violates proven local convention | move/rename and update inbound links |
| `write-successor` | operator made a new significant choice | hand off to `adr-writer`, then supersede old |
| `split` | ADR bundles independent decisions | operator-backed successor records; retire bundle |
| `flag-hollow` | rationale/options are missing or unsupported | request real author/operator evidence; never invent |
| `confirm-candidate` | code shows a consequential fork but no decision history | ask whether an ADR-worthy operator decision exists |
| `establish-current-contract` | ADR alone owns current normative behavior | hand off to `contract-writer` under its semantic gate |
| `fix-code-or-contract` | current implementation violates a still-valid invariant | implementation/contract workflow, not ADR rewrite |

Group an approval plan into append-only metadata, filesystem normalization, and reasoning-dependent
hand-offs. Never bundle source deletion. If evidence changes between diagnosis and remediation,
re-resolve the action rather than applying a stale plan.
