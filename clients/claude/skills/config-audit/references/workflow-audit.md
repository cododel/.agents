# Phase 7 — End-to-end workflow audit (SDD + TDD loop)

Skills can be individually healthy while the pipeline leaks. Check the full
cycle:

**Reference loop:** Spec/ADR → Plan → RED (failing test) → GREEN (minimal
implementation) → REFACTOR → independent review → Commit.

- [ ] **Spec phase separated from implementation.** Large features start with an
      interview (`AskUserQuestion`) → `SPEC.md` → **fresh session** for
      execution. The spec is self-sufficient: files, interfaces, out-of-scope,
      an end-to-end check at the bottom
- [ ] **Plan mode used as intended:** multi-file/non-obvious changes go through
      a plan; one-line fixes go direct (a plan there is overhead)
- [ ] **TDD order is enforced, not declared.** Claude defaults to
      implementation-first; "write tests" in CLAUDE.md is not enough. A
      skill/workflow needs the explicit step "write a FAILING test, do not write
      implementation" + confirmation of the red run before implementing.
      *Deliberate deviation from the source, which mandates unconditional
      enforcement:* respect the config's own proportionality rules — if the
      operator's standards make TDD conditional (as this operator's CLAUDE.md
      §6/§7 do), audit *those conditions*, don't impose a blanket gate the
      operator explicitly rejected
- [ ] **Test writer and implementer separated by context** (subagents or two
      writer/reviewer sessions): in one window the implementation leaks into
      test logic, and tests start validating code instead of driving design
- [ ] **Every task has a check Claude can run itself:** test suite, build exit
      code, linter, screenshot diff. Without it "looks done" is the only stop
      signal, and *you* become the verification loop
- [ ] **A completion gate exists:** goal condition or Stop hook for unattended
      runs; "evidence, not assertions" — Claude shows test output, not success
      claims
- [ ] **Adversarial review is built in:** before "done", a fresh-context
      subagent reviews the diff against the plan/spec. The reviewer is told to
      report only correctness/requirements gaps — otherwise it generates
      findings for findings' sake and you over-engineer
- [ ] **Decisions crystallize:** significant architecture forks from sessions
      reach ADRs (a skill/habit exists for that), and session lessons ("Claude
      did X again") reach `.claude/` edits — otherwise every audit starts from
      zero
- [ ] **Session hygiene:** `/clear` between unrelated tasks; after two failed
      corrections — `/clear` + a better prompt instead of a third try; research
      goes to subagents, not the main context
