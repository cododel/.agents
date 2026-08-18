# From-chat workflow

Create an ADR from a decision established in the current conversation.

## Step F0 — Verify authority and significance

Confirm the operator actually chose (or explicitly wants to record as `Proposed`) a significant path.
Apply `adr-spec.md` §§2–3. If the chat contains only implementation shape, agent recommendation, or an
obvious/reversible detail, explain briefly why no ADR is warranted and stop.

## Step F1 — Extract the decision evidence

Read the complete relevant conversation and extract without inventing:

- the motivating problem and decision forces;
- every real option actually considered;
- the concrete reason each option was selected/rejected;
- the operator's chosen outcome and status;
- consequences, constraints, assumptions/invariants, and revisit evidence that were discussed;
- related contracts, Issues, research, and prior ADRs.

If plausible alternatives existed but were never discussed, ask the operator rather than fabricating
them. A genuinely mandated single-option choice must name the hard constraint. Split independent forks
into separate ADRs with `Related` links.

## Step F2 — Resolve path, status, and depth

Read the local convention and `../assets/adr-template.md`.

- Match established naming and fields when they are coherent.
- Otherwise use `ADR-YYYYMMDD-<slug>.md` and the compact fallback.
- A settled operator choice is `Accepted`; an explicitly pending record is `Proposed`.
- If replacing a recorded decision, create the successor and backfill bidirectional links without
  rewriting the old body.
- Add optional depth only when the conversation contains decision-specific value. For high reversal
  cost, ensure assumptions, consequences, and validation/revisit triggers are explicit.

## Step F3 — Write the ADR

Write one self-sufficient decision record. Preserve the operator's actual nuance but do not paste the
conversation. The title names the decision, not merely the topic. Alternatives and rejection reasons
are load-bearing. Consequences include costs, not only benefits.

Decision invariants state when the historical choice remains valid; they do not replace the current
living contract.

## Step F3.5 — Link the current contract

Discover an existing stable-boundary contract. When it owns behavior shaped by this decision, add
`Current contract` to the ADR and `Decision provenance` to the contract. Keep normative rules in the
contract.

When no owner exists, apply `$contract-writer`'s value and decision gates. It may create a concise
contract if behavior/scope are already explicit; otherwise report the material fork. A temporary brief
is not a current contract.

## Step F4 — Save and confirm

Create the proven path/directories, verify links and `git diff --check`, and respond only with a short
repository-relative path confirmation. Do not echo the ADR body or add a celebratory status message.
