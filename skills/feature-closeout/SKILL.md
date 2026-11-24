---
name: feature-closeout
description: "Bring an implementation to an evidenced local handoff when closeout is requested or material completion uncertainty remains. Reconstruct behavior and architecture, resolve authorized defects, and explain the verified result to the operator."
---

# Feature Closeout

Establish what the task changed, whether it delivers the agreed result, and what the operator can rely on at this handoff. Scale the investigation to consequences, interactions, uncertainty and available evidence. A small change with decisive evidence needs only a compact answer.

1. **Set the boundary.** Recover the agreed outcome, constraints, decisions and checks due now from the operator, applicable project sources and active [task journal](../task-journal/SKILL.md). Establish the task baseline if available and identify the actual target, including relevant commits, staged, unstaged and untracked changes. Preserve other people's work. If the baseline is missing, assess the target against the agreement and identify which comparisons are unknown.
2. **Reconstruct and trace.** Group material changes by capability and responsibility, including correct changes, removals and justified decisions. Follow actual entry points through their consumers and effects. For substantial changes or uncertain interactions, use [change investigation](references/investigation.md) to account for the affected areas, changed relationships and gaps. Trace each material obligation to its enforcement and each material new behavior back to its authority.
3. **Challenge the result.** For each consequential guarantee, look for a reachable condition under which it breaks. Where a material outcome depends on a later actor, establish how that actor discovers the outstanding work and what happens to work its selection rules exclude. Verify suspected defects against reachable guards and contrary evidence. Verify a proposed simplification against the same contract. Use [testing-evidence](../testing-evidence/SKILL.md) for substantive verification, including check selection, execution, interpretation and reuse. Follow project gates and global authority, isolation and E2E limits. Use [adversarial-review](../adversarial-review/SKILL.md) when a particular guarantee warrants specialized investigation. Consume its evidence once.
4. **Resolve and recheck.** With implementation authority, repair confirmed unambiguous defects within the agreed task and its demonstrated affected radius. An explicit read-only assessment leaves the implementation untouched. For a material unresolved choice, present the evidence, alternatives, consequences and recommendation to the operator. Continue independent work. Update affected documentation, inventory and claims after repairs or target drift. Refresh missing or invalidated evidence and reuse demonstrably current results. If the same finding persists, investigate the missing causal link. Continue useful repair/recheck cycles until prepared or concretely blocked.
5. **Verify the handoff.** Inspect the final affected diff and compare the final state with every material criterion due now. Record results and remaining gaps in the active journal if present. Include significant original defects, their resolution and the decisive final checks. For substantial work deliver a [local visual report](references/report.md) from this investigation, including when the change is sound. For small work give the scoped outcome and evidence directly.

Choose independent read-only contexts when they add material evidence or when required by the operator, project or specialist procedure. Give them the task, constraints and raw target first, withholding builder conclusions and expected verdicts. Reconcile their returned evidence against the actual target. If required independence is unavailable, continue useful work and identify that blocker. Label same-context checks accurately.

## Completion boundary

- **PREPARED for [agreed handoff]** when evidence covers every material criterion due there and no confirmed in-scope correctness, quality or completeness blocker remains. Identify separately assigned later operator checks as pending.
- **BLOCKED for [agreed handoff]** when a specific unmet decision, required evidence, prerequisite, authority or agreed resource limit prevents further authorized progress. Name the affected obligation and what would resolve it. Preserve any confirmed defects alongside evidence gaps.

A completed read-only assessment can establish that the implementation is blocked. Preserve the agreed boundary even if runtime access is missing. Local preparation and operator acceptance or production rollout are separate decisions. Git, worktree, external actions and documentation ownership follow applicable instructions.

## Existing invocations

Legacy **Full** means ordinary closeout. A **Quick** or interim request checks only the requested slice, its due criteria and prerequisites of the next step. Correct clear authorized gaps within that scope and report deviations and missing proof. Future work stays pending. An interim check never certifies final handoff.

Only an explicit frozen final audit, legacy `--release` or “release closeout” invokes the [frozen audit](references/frozen-audit.md) after preparation. Explain that mapping for release aliases.
