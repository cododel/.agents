# Quick closeout

Apply the common review invariants in `../SKILL.md` to the bounded changed radius.

Use the smallest decisive evidence: source/docs review, config/parser validation, a focused probe,
existing tests, or reproduction when behavior requires it. Add relevant type/lint/static checks;
documentation/config changes need no artificial runtime reproduction.

Inspect obvious failure paths, unsafe typing, stale comments/docs, and scope drift. Allow **one**
clear authorized repair pass, then rerun affected checks. Do not fan out by default, force a full
suite, widen into a repository audit, or claim release readiness.

- `CLOSED`: target behavior and proportional evidence are supported.
- `BLOCKED`: a material decision/evidence gap or confirmed defect remains.
