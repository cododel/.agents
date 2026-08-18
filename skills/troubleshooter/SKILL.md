---
name: troubleshooter
description: "Auto-diagnose concrete tracebacks, crashes, logs, failing commands, and runtime failures; fix when requested. Require an evidence-backed root cause and focused regression or probe. Not for generic architecture review."
---

# Troubleshooter

Find the incorrect assumption that produces the observed failure, not merely the line that throws.
Diagnosis precedes the final fix, but an explicit fix request authorizes local reversible investigation,
reproduction, patching, and proportionate verification without an extra approval ceremony.

## Intent and authority

- **Explain/diagnose only:** remain read-only with respect to tracked product code. Focused local probes
  or existing tests are allowed when they are proven disposable and do not touch shared/persistent
  state; otherwise show the exact risky command and stop at that gate.
- **Fix/debug request:** investigate, reproduce when useful, apply the evidence-backed fix, improve
  directly touched code when it reduces defect risk, and verify it. Do not ask for permission for
  ordinary local reversible edits.
- **Material fork:** stop when plausible fixes encode different product behavior, stable contracts,
  architecture, migration semantics, or irreversible cost.

A fix request does not authorize unrelated cleanup, push/deploy, destructive operations, or
shared/persistent database mutation.

## Workflow

1. **Parse the failure artifact.** Extract error type/message, execution command/environment, and the
   first relevant application frame. Separate the symptom frame from the upstream source of invalid
   state. If the artifact or target is genuinely insufficient, ask only for the exact missing input.
2. **Reproduce or establish a falsifiable probe.** Prefer the smallest existing test/command that
   isolates the failure. For a legacy seam, a temporary test or script in task scratch is acceptable.
   Prove the probe fails for the intended reason, not setup noise.
3. **Trace origin to failure.** Follow `references/discovery.md`; load only the applicable stack
   playbook. Use an existing Graphify graph for cross-module/event-flow navigation when useful, then
   verify decisive edges in source. Use `$find-docs` for drift-prone framework/library semantics.
4. **Name the root cause.** State the violated assumption and the concrete state/data/control path
   from origin to failure. Distinguish proven cause from remaining hypotheses.
5. **Fix the best boundary.** Correct the origin or ownership boundary rather than adding a broad
   catch/suppression at the crash site. Local touched-area refactoring is allowed when it reduces the
   same failure class without widening merge-conflict or regression radius.
6. **Verify correctness and quality.** Make the focused repro/test pass, run relevant type/lint/static
   checks, inspect failure/unavailable paths, and check that the patch did not hide the symptom,
   weaken validation, introduce unsafe typing, or create a security/resource leak.
7. **Capture independent debt.** If the investigation proves a distinct, independently resumable
   problem outside the current affected radius, invoke `$issue-writer`, add a useful linked TODO at
   the local seam when appropriate, and return to the active failure.

## Investigation control

Do not impose a fixed file-count stop on a cross-layer failure. Instead use evidence checkpoints:

- begin narrow at the failing frame and widen by concrete data/control edges;
- after roughly three widening rounds or 10–15 substantive file reads, summarize the current causal
  chain and identify what next observation can falsify it;
- continue autonomously when that observation is repository-local and likely decisive;
- ask only when the remaining evidence requires unavailable input, shared/external mutation, or an
  operator decision;
- stop searching once one root cause explains the complete observed path and the focused probe can
  distinguish the proposed fix from alternatives.

Do not patch an unproven cause merely to see whether the error disappears. A disappearing symptom can
still be suppression, state leakage, or an incomplete fix.

## Handoff

For a fix, respond compactly with:

- root cause and violated assumption;
- semantic fix and why that boundary is correct;
- decisive failing-before/passing-after evidence;
- any material quality/completeness caveat or linked deferred Issue.

For diagnosis-only, omit implementation claims and state the next falsifying observation when the
cause remains uncertain. Do not force a five-section template when two precise paragraphs suffice.
