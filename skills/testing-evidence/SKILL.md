---
name: testing-evidence
description: "Use for substantive test design or review, test-failure diagnosis, uncertain verification boundaries or evidence reuse, and money/access/persistence/lifecycle risks. Routine established checks alone do not require this skill. Project profiles supply commands and required gates."
---

# Testing Evidence

Choose evidence for the claim: identify an independent expected result and the production boundary
that must perform the behavior. RED must expose the intended gap, not collection, fixture or
missing-service noise; reuse a trustworthy existing failure. General testing and authority policy
comes from AGENTS.md; project instructions supply commands, isolation and required gates.

Read the relevant procedure before making the corresponding evidence decision:

- [Test design](references/test-design.md): assertions and decisive setup/subject, independent
  expectations, doubles, failure phases, duplicate protection and scoped test-value review.
- [Execution evidence](references/execution-evidence.md): check selection, interpretation, incomplete
  stages, result identity, reuse/invalidation and final evidence.
- [Experiments](references/experiments.md): a temporary PoC/demo to resolve uncertainty, or a
  controlled comparison of resource use. This is an option, not a mandatory implementation stage.

Use [repository-test-audit](../repository-test-audit/SKILL.md) for a requested repository/suite audit
with inventory and global conclusions; an ordinary regression fix does not invoke that workflow.
