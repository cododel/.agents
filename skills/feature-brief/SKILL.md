---
name: feature-brief
description: "Conduct operator-led feature discovery or create and revise a temporary feature brief contract. Use for `проведи брифинг`, `опроси меня по фиче`, `составь/обнови бриф`, `feature briefing`, or `feature brief`, including requests that combine the interview and document. Do not use for ordinary task summaries, implementation plans, deferred Issues, durable specifications, or ADRs."
---

# Feature Brief

## Purpose

Use one skill for two optional modes:

1. **Briefing** — inspect the current project, then interview the operator only for
   material information that repository evidence cannot supply. Do not create a document.
2. **Brief** — only on explicit request, create or revise a temporary, reviewable contract.

Do not create an Issue or ADR as a side effect. Project-local instructions and established
document conventions override this fallback workflow.

## Mode selector

| Intent | Mode | Read next |
|:--|:--|:--|
| Gather requirements through questions: `проведи брифинг`, `опроси меня по фиче`, `feature briefing` | briefing | `references/briefing.md` |
| Materialize or revise the agreement: `составь бриф`, `обнови бриф`, `feature brief` | brief | `references/brief.md` |
| Interview and then write the result | briefing, then brief | both references in order |

When wording is ambiguous between an ordinary discussion and a briefing, continue the
discussion without invoking this workflow. Do not turn every feature conversation into a brief.

## Shared grounding

Before either mode:

1. Resolve the repository root and read its instructions.
2. Inspect the relevant code, documentation, and existing project contracts before asking
   questions or drafting requirements.
3. Separate observed facts, operator decisions, assumptions, and open questions.
4. Identify contract impact as `unchanged`, `extend`, `conflict`, or `missing` for relevant
   product, UI, API, domain, persistence, architecture, or security contracts.

Do not treat chat, plans, Issues, or a brief as proof of current implementation state.

## Storage and authority

Use an established repository location only when it explicitly covers temporary briefs or
draft feature contracts. Otherwise write to:

```text
<repo-root>/.agents/briefs/YYYY-MM-DD-english-kebab-slug.md
```

Use `assets/brief-template.md`. Do not add the brief to a README or index, alter `.gitignore`,
stage it, commit it, or promote it to durable documentation without an explicit request.

- `Draft` records a proposal under review. It does not authorize implementation.
- `Agreed` requires an explicit operator confirmation of the document's current content.
- A material scope, behavior, constraint, or acceptance change returns an agreed brief to
  `Draft` until the operator confirms it again.
- Operator comments or edits are review input, not implicit agreement.

The operator must separately request implementation. A briefing may flow directly into explicitly
requested planning or implementation without a file. If a brief exists, work follows only its
current `Agreed` version and stops for material divergence.

## Completion

At implementation completion, compare the result with the agreed brief and current project
contracts. Route durable value through `../_shared/durable-documentation.md`. A temporary brief is
not an implementation spec and must not receive a durable ADR link.

Never delete a repository-local brief automatically. Present the exact path for the operator's
normal deletion gate after durable value has been extracted.

## Report back

- For a briefing, report the current fact/decision/question state and whether enough context
  exists to draft a brief.
- For a brief, report its path, `Draft` or `Agreed` status, unresolved questions, and contract
  impact. Do not repeat the whole document in chat.
