---
name: contract-writer
description: "Create or update lightweight living contracts for non-obvious stable behavior and ownership boundaries. Use when agreed guarantees change or a lasting obligation lacks a suitable owner; ask only when the contract would choose unresolved semantics."
---

# Contract Writer

Maintain one normative owner for established lasting guarantees. Discovery/impact requests are
read-only. An explicit authoring request or authorized behavior work covering confirmed guarantee
changes permits scoped owner edits; merely finding a gap does not.

## Modes

| Intent/state | Mode | Authority |
|:--|:--|:--|
| Locate the current normative owner | discovery | read-only |
| Classify proposed/implemented behavior | impact | read-only |
| Align an established owner with confirmed guarantees in authorized behavior/authoring work | update | scoped local reversible work |
| Establish a justified missing owner for confirmed guarantees in authorized work | create | scoped local reversible work |
| Contract would decide unresolved behavior/scope/ownership | decision gate | stop affected authoring for operator |

Read `references/contract-spec.md` before classifying/writing. It owns the unchanged four-value test,
normative ownership, content, language, and ADR relationship. Existing declared API/schema/docs may
suffice; absence of a Markdown file or conventional folder is not a gap.

Use `references/workflow.md` for discovery, `unchanged | extend | conflict | missing` classification,
authority, justified bootstrap, path/language, linking, and verification. Follow only the steps for the
requested mode: discovery/impact does not load an output template or perform authoring. Use
`../_shared/repository-discovery.md` when resolving documentation scope and
`assets/contract-template.md` only when authoring in the fallback format.

Confirmed guarantee changes update the existing owner without renewed confirmation. Pause affected
authoring only when the document would choose unresolved semantics, scope, ownership, language, or
canonical home. Never turn accidental implementation into a promise or rewrite Accepted ADR history.

Report classification, the semantic owner change, decisive evidence/checks, enforcement gaps, and any
real operator fork. Writing a contract does not prove implementation compliance.
