# Quick checkpoint

Apply the common completion invariants in `../SKILL.md` to the bounded changed radius.

Compare the completed slice and next step with current agreed behavior, decisions, constraints and
non-goals. Check criteria already due at this stage and prerequisites of the next step. Planned future
work is not a defect, but a claimed completed stage without evidence or a violated dependency is a gap.

Use proportional evidence under testing-evidence. Fix clear authorized in-scope gaps and recheck
affected criteria while making verified progress; there is no fixed repair-round limit. Keep the
checkpoint bounded: do not fan out by default or broaden it; return larger work to ordinary
implementation. Continue independent work and clarify material choices. Stop the affected path when
a concrete unresolved decision, unmet prerequisite, stalled progress or agreed resource limit
prevents progress; identify the blocker rather than repeating an unchanged check.

Report the checked slice and one outcome; none certifies final acceptance:

- `DRIFT`: a confirmed deviation from agreed criteria remains, including an implementation defect
  or a next step that violates a required dependency. Report coexisting evidence gaps as well.
- `UNVERIFIED`: no confirmed deviation, but a material decision or evidence gap prevents assessment.
- `ALIGNED`: the checked slice and next-step prerequisites are supported; future criteria stay pending.
