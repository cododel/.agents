# Phase 6 — Functional evals: TDD for skills, part 2

Triggering converged — now verify the skill **improves the outcome**, not just
fires. Costs real tokens; confirm with the operator before running.

## 1. Baseline comparison (RED-GREEN)

The core discipline: watch the agent fail *without* the skill before crediting
the skill.

- Build a fixture with **planted defects** and a written answer key (e.g. a fake
  project `.claude/` with a dead command, a broken import, a trigger collision,
  an always-rule that should be a hook — 10–12 items).
- RED: a subagent gets the bare user-shaped request, no skill. Score its output
  against the key with a judge subagent. The misses are what the skill must fix.
- GREEN: same prompt + the skill. Score again. The skill earns its place only if
  GREEN finds what RED missed.
- If there's no difference — the skill doesn't pull its context price; fix or
  delete it.
- When auditing an *edit* rather than the skill's existence, run the baseline
  against the skill's **previous version** instead of against nothing — that
  turns this into a regression test for the change.

A shipped fixture lives in `evals/`: `make-fixture.sh` materializes a
planted-defect project, `answer-key.md` lists the 12 defects and this skill's
own recorded RED/GREEN. Use it as the template for a fixture of the skill under
audit.

## 2. Assertions

For skills with objectively checkable output, write assertions and check them
with a script, not eyes: "test file created before implementation file", "ADR
has a rejected-alternatives section", "the test command appears in the output".

## 3. Pressure tests for process skills

Skills that impose discipline (TDD skill, review gates, approval checkpoints)
are tested under pressure: give the agent a deadline scenario, sunk cost,
"client is waiting" — and watch where it rationalizes bypassing the rule. A
found loophole → reword (explain *why* the rule exists) → re-run. That's
RED-GREEN-REFACTOR applied to the skill's text.

## 4. Read transcripts, not just results

If the skill makes the model burn turns on unproductive actions — cut those
parts and compare again.

## 5. Generalize, don't overfit

Iterating on 3 examples is how you move fast, but fixes must be general
principles, not patches for the specific test.
