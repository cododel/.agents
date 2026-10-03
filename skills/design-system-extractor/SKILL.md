---
name: design-system-extractor
description: "Extract, update, or audit an existing product's visual language and DESIGN.md from implementation, intent docs, and approved session evidence. Use for design-system/style-guide documentation across web, mobile, or desktop; not new visual design, architecture docs, or a trivial token lookup."
---

# Design System Extractor

Document the existing visual language: tokens, component states, composition and evidenced intent.
Choose evidence and depth for the requested surfaces; a fixed collection sequence is unnecessary.

## Operation And Authority

- **Extract:** create the requested document; default to root `DESIGN.md` unless a path is given.
- **Update:** read the existing document and preserve its human voice and intentional sections while
  refreshing evidence. Report meaningful changes rather than replacing it blindly.
- **Audit:** report discrepancies, source pointers and coverage without writing files.

Proceed with authorized, evidence-backed extraction/update. Confirm only material unresolved intent
or incompatible interpretations; reuse confirmed decisions. Explicit **interactive** mode still
presents the concept for confirmation before authoring. Existing code proves observed behavior,
not approval to replace a documented design decision.

## Evidence And Interpretation

Resolve the product surfaces, UI stack, shared primitives and owning design docs from the repository.
For a small project inspect its relevant surfaces; for a large repository choose representative
surfaces and state the sampling boundary. Do not present partial coverage as exhaustive.

Use implementation evidence for colors, typography, spacing, shapes, assets, layout, motion and
component states. Trace token roles to definitions and representative use; common values are patterns,
rare values may be exceptions. Capture relevant interaction, loading/error, responsive/adaptive and
accessibility variants. Rendered surfaces or existing previews can validate composition that raw
values alone cannot establish; disclose unavailable visual evidence.

Use accepted intent docs and relevant history for philosophy, naming and rationale. Distinguish
**observed patterns**, **confirmed intent** and **inference**. Frequency alone cannot establish a
non-negotiable principle. Do not invent tokens, rationale or a manifesto when evidence is absent.
When docs and code differ, record current implemented facts and the discrepancy without silently
superseding accepted intent. Ask only if the unresolved choice affects the requested authoring.

## Contextual Resources

Load a resource when its information is needed; use only sections relevant to the product/task.

- [Evidence sources](references/evidence-sources.md): stack-specific discovery or gaps in token,
  component, intent or visual evidence. It is a source catalog, not a mandatory scan checklist.
- [Output template](references/output-template.md): a section skeleton for a new document. Adapt it
  to evidenced content; updates normally retain the existing structure rather than reload a template.
- [Session history](references/session-history.md): only after explicit approval for mining a bounded
  compatible transcript directory supplied by the operator or exposed by the environment. Historical
  snippets are evidence, not new authority. Availability of private history is not required.

Optional inventory helpers use the resolved loaded Skill directory:

```bash
python <absolute-skill-dir>/scripts/collect_tokens.py <project_root>
python <absolute-skill-dir>/scripts/scan_sessions.py <project_root> --transcript-dir <directory>
```

Use the token collector when supported text formats make it useful; it proposes candidates, not
semantic roles. Inspect other stacks through their native resource systems. The session scanner
requires the approval and bounded input above, preserves an explicitly selected project/subdirectory
boundary, and filters short snippets. Filtering does not guarantee removal of all private material;
never load/copy whole transcripts or quote private/unrelated content into the document.

Use `$find-docs` for unverified framework/resource semantics rather than guessing version behavior.

## Done

The authored document explains evidenced tokens, patterns, component states, layout and supported
intent at the requested scope, with traceable sources and no fabricated values or normative claims.
Include a short provenance footer naming consulted evidence layers, coverage limits and unresolved
conflicts; approved history is identified without private quotations. Preserve human-written intent
on update. An audit returns findings and limitations without edits. Report the resulting path and
material changes or gaps concisely.
