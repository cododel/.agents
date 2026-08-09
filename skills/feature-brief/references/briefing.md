# Briefing workflow

Use this mode to elicit operator intent, not to draft a document.

## 1. Ground the discussion

Inspect the actual feature surface and relevant project contracts. Build a private inventory of:

- observed current behavior and constraints;
- the operator's already-stated goals and preferences;
- material unknowns that cannot be answered from the repository;
- plausible choices whose differences affect scope, behavior, risk, or acceptance.

Do not ask the operator to repeat facts already present in the conversation or project.

## 2. Interview the operator

Ask a small coherent batch of high-impact questions at a time. Prefer structured choices when
the alternatives are real and mutually exclusive; use a direct question when the answer must be
free-form. Explain a recommended default without treating it as chosen.

After each answer:

1. update the distinction between fact, decision, assumption, and open question;
2. inspect more repository evidence when the answer exposes a discoverable unknown;
3. ask the next question only when its answer can still change the feature contract.

Do not ask implementation-detail questions that can safely remain for planning.

## 3. Close the briefing

Stop when the goal, audience, primary scenarios, scope, non-goals, constraints, contract impact,
and acceptance boundary are clear enough to review as one coherent agreement.

Summarize:

- established facts;
- operator decisions;
- explicit assumptions;
- remaining open questions, or `None`;
- contract impact classification.

If the request included creating a brief, continue with `references/brief.md`. Otherwise stop
without creating or modifying files. If planning or implementation was also explicitly requested,
continue to that work from the chat summary; do not insert a brief-file prerequisite.
