# Quick checkpoint

Apply the common review invariants in `../SKILL.md` to the bounded changed radius.

Compare the completed slice and next step with current agreed behavior, decisions, constraints and
non-goals. Check criteria already due at this stage and prerequisites of the next step. Planned future
work is not a defect, but a claimed completed stage without evidence or a violated dependency is a gap.

Use proportional evidence under testing-evidence. Allow **one** clear authorized repair/recheck pass.
Do not fan out by default or broaden the review beyond the checkpoint. Continue authorized work;
stop the affected path for a material unresolved decision or unmet prerequisite.

Report the checked slice and one outcome; none certifies final acceptance:

- `DRIFT`: a confirmed deviation from agreed criteria remains, including an implementation defect
  or a next step that violates a required dependency. Report coexisting evidence gaps as well.
- `UNVERIFIED`: no confirmed deviation, but a material decision or evidence gap prevents assessment.
- `ALIGNED`: the checked slice and next-step prerequisites are supported; future criteria stay pending.
