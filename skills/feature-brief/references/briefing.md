# Briefing workflow

Use this workflow with a structured planning and question interface when the current execution
environment provides one. Its purpose is to improve the task contract, not to produce a long
questionnaire or implementation choreography.

## 1. Build a decision map

From repository evidence and the operator's existing statements, privately classify:

- **established facts** — current code/runtime/documented behavior;
- **operator decisions** — product or architecture choices already made;
- **objective choices** — implementation details the agent can resolve from evidence;
- **material forks** — plausible alternatives that change behavior, stable boundaries, risk, cost,
  migration, or acceptance;
- **assumptions** — falsifiable interpretations that remain after research.

Use current official documentation or a focused read-only probe before turning a discoverable fact
into a question. Preserve the operator's motivation; it is the reference point for later tradeoffs.

## 2. Ask by consequence, not by template

Ask one coherent batch of the highest-impact unresolved forks. Usually 2–5 questions is enough for a
round. For each question:

- explain the consequence of the alternatives in one compact sentence;
- offer a recommended default only when evidence supports it;
- use mutually exclusive options when they are real choices;
- allow free-form input when the operator's intent cannot be reduced safely;
- do not ask about internal naming, file layout, or implementation mechanics unless they encode a
  stable boundary or operator preference.

After an answer, update the decision map and inspect new repository evidence before asking the next
round. Do not ask everything foreseeable up front. A newly surfaced invariant may justify a later
question during implementation; ordinary local choices do not.

## 3. Challenge incompleteness selectively

Before closing, test the target contract against likely omissions:

- unhappy and unavailable paths;
- data lifecycle and compatibility;
- permissions/security boundaries;
- event ordering, retries, idempotency, and ownership where relevant;
- operator-visible controls and observability;
- explicit non-goals and acceptable shortcuts.

Raise only omissions that are material for this feature. Do not expand a normal feature into a generic
enterprise checklist.

## 4. Close into an actionable contract

Stop when the following are clear enough that remaining choices are reversible implementation details:

- motivation and intended outcome;
- primary scenarios and failure behavior;
- included scope and non-goals;
- confirmed invariants/decisions;
- affected stable contracts or known contract gaps;
- observable acceptance boundary;
- remaining material questions, if any.

Update the active plan and task journal. Create a brief file only when requested or justified by
cross-session/subagent review. If implementation was requested, proceed under the environment's normal
authorization boundary; do not insert another approval layer.
