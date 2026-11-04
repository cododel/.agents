---
name: skill-evolution
description: "Create or update a skill with a built-in evolution mechanism: learning signals, evidence, scoped patches, checks and promotion boundaries. Use when the operator asks for an evolving, living or self-improving skill, including «добавь механизм эволюции». Not ordinary skill authoring or permission to evolve every skill encountered."
---

# Skill Evolution

Make experience improve future execution without silently changing the operator's intent.
This is an authoring workflow: embed the resulting evolution instructions in the target package
so they work when this meta-skill is absent. Preserve the target's existing authoring conventions.

## Establish the target

Read the target entrypoint, affected resources and applicable rules. Identify the maintained source,
ownership, existing evolution policy, task acceptance and permitted writes. Patch the source rather
than an installed cache or vendor package. If only a protected/read-only copy is available, prepare
a candidate in the authorized task workspace and identify the missing promotion path.

Use an existing evidence store, examples and checks where they fit. Do not introduce a database,
cron, event ledger, dependency or general self-modification system merely to make a skill living.
Adding evolution does not itself authorize capturing conversations, using secrets, external writes,
commits or publication. Reuse established authority without asking again.

## Define learning and promotion

Distinguish a one-off correction, a reusable procedural defect, a preference, a new scope and a
policy change. A successful output or the agent's own reflection alone is insufficient evidence
for a persistent rule. Operator corrections establish intended meaning within their stated scope;
silence and an unaccepted draft do not establish acceptance.

Choose the narrowest applicable lane for each change, rather than one lane for the entire skill:

| Change | Evidence and permitted promotion |
| --- | --- |
| Objective procedural repair, such as a verified command workaround | Reproduce the relevant failure, verify the repair and affected existing behavior; apply a narrow local patch when existing authority covers that target and change. Otherwise prepare a candidate. |
| Terminology, authorial voice, domain interpretation or new scope | Preserve the correction's scope; prepare a candidate with a counterexample, a new transfer case and relevant regression cases. Promote only with operator approval covering the change; an explicit instruction to persist that exact rule can supply it. |
| Evolution policy, trusted evidence, write permissions or approval rules | Require an explicit external decision covering this boundary. The learning loop cannot grant itself authority or weaken its own checks. |

Do not infer permission for automatic edits merely from the word “evolving”. If no automatic-write
scope is established, embed candidate-only promotion. Clarify a material unresolved boundary only
when necessary for the requested behavior; continue independent authoring work meanwhile.

## Embed the runtime loop

Read [Runtime clause](references/runtime-clause.md) and adapt it to the actual domain. Put the
essential trigger, evidence threshold, write boundary and disclosure rule in the target entrypoint.
Put conditional detail in target-owned references with explicit routing. The finished package must
not require this meta-skill, private wiki access or an unavailable harness to perform the loop.

The target must tell the executing agent:

1. **Observe:** notice direct corrections, reproducible failures, confirmed workarounds and requests
   that expose a real scope gap. Finish or repair the current authorized task first; do not delay
   useful delivery for speculative learning.
2. **Explain:** identify the mechanism, evidence, applicability and a counterexample. Preserve only
   the minimum necessary source/confirmation, reproduction or fixture reference. Label hypotheses.
3. **Patch:** update the current procedure or add a concise trap where the mistake would occur:
   plausible wrong move → observed mechanism and evidence → correct move. Avoid a run diary.
4. **Check:** replay the original gap and a new relevant case, then check affected prior guarantees.
   Subjective improvements need external assessment; mechanical checks alone cannot certify them.
5. **Promote:** apply only within the established lane and writable surface. Otherwise retain an
   explicit candidate outside active instructions, stating what decision or evidence is missing.
6. **Disclose:** say what was learned, its scope, what changed or remains proposed, verification
   limits and how the exact change can be rejected or reverted without losing unrelated work.

Store reusable mechanisms rather than easily rediscovered facts, whole conversations, secrets,
unaccepted outputs or transient run totals. Scope measurements to dated snapshots when needed;
prefer relational checks over pinning live totals. Encode knowledge as an executable check when
that meaningfully catches recurrence using the existing tools.

Keep one owner for each rule. Revise superseded guidance rather than appending conflicting rules.
Parameterize genuinely shared procedures when an authorized scope expands; do not clone nearly
identical skills. Preserve discovery and callers when changing names or descriptions. Revisit stale
evidence when contradicted or when its dependencies change; propose removals or apply them only
within existing authority. Do not impose a fixed audit schedule or monotonic file growth.

## Validate the authored result

Check realistic requests at both boundaries: authoring must embed a complete loop, and later
execution must obey it without this meta-skill. Include a confirmed technical repair, an ambiguous
preference, an unsupported hypothesis and an attempted change to the evolution gate. Preserve the
target's existing purpose, behavior and protected cases; do not fabricate prior failures or evidence.

Use the target's established structural checks. Where behavioral confidence matters, run isolated
forward trials with realistic inputs and inspect resulting artifacts, not promises. An independent
agent may perform these trials with writes restricted to disposable fixtures. Grade against criteria
set before the trial. Record failures and untested boundaries honestly; do not claim that a valid
Markdown package guarantees improvement or an enforceable security boundary.

Report the target, embedded lanes, actual validation and remaining limits. Leave unrelated skills
and global policy unchanged.
