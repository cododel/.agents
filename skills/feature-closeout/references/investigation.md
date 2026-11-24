# Investigating a material change

## Compare the right states

Prefer the agreed task-start snapshot or actual integration base. A last commit or branch name alone rarely identifies a whole task. In a dirty checkout distinguish included commits, index, working files and new paths from unrelated work. Include deletions, configuration, schema, dependency and consumer changes where relevant. Equal HEADs can hold different reviewed bytes. Preserve enough identity to detect changes to conclusions or checks. Only a frozen audit requires a separate exact source fingerprint.

Partition a large change by scenario or subsystem. For each material area tie the before/after, source of intent, consequence and coverage to a locator on the reviewed state. Group mechanical edits. Identify exclusions and unexamined areas that could affect readiness. Without a reliable baseline, describe established current behavior and limit historical or causal claims. Reconcile the target again at handoff.

## Follow responsibilities in both directions

For each material requirement follow the supported route through the component that enforces it to the observable result. Account separately for met, partial, violated and unverified obligations. Keep the source of each consequential requirement or amendment. Tests, code and author explanations supply evidence about implementation.

Then walk the inventory in reverse. Which behavior implements the agreement, exercises delegated engineering discretion, or changes a material policy or architecture choice? Identify the actor affected by a new default, write, access rule, dependency or failure path. Silence alone cannot establish a prohibition. Keep justified engineering decisions in the inventory. Present a genuine unresolved tradeoff to its owner.

Follow meaningful edges on both sides: who triggers the operation, owns the decision or data, reads or writes state, relies on the output, and recovers when it fails? Compare added, removed and repeated calls, contracts, state transitions, configuration, operational controls and side effects. Include compatibility, rollback, lifecycle and observability where changed. When a new route carries sensitive data or access to a private resource, follow that value to its recipients on success, error and retry, including diagnostic or persistent sinks in reused consumers. Check what each recipient may retain or expose. A source-supported route establishes possibility. A count, timing or successful execution needs appropriate observed evidence.

## Test a consequential conclusion

Start with the claim on which acceptance depends. Trace a concrete combination of states or events that could falsify it, across components when relevant. Inspect failure handling and its side effects. Choose cases from the actual path and consequences. For difficult interactions use the specialized investigation referenced by the entrypoint.

When responsibility passes between components, distinguish the first stage's completion from the outcome still owed. Take a concrete state the first stage can leave behind and walk it through the next actor's actual discovery and selection rules, including reused code. Which inputs to those rules can change independently after the work was accepted? Try a reachable combination that would exclude the item. Trace who can then observe it and finish, resume or otherwise resolve it under the agreement. A handler or retry protects the item only if its own entry conditions admit it. Give credit to an independently reachable recovery path or an agreed pause. If the supplied evidence ends before the next owner, identify the gap. Surface a confirmed loss of a consequential outcome in the operator summary.

When a producer declares a result ready, compare the exact predicate that releases it with what its next consumer must actually be able to do. Construct the smallest incomplete, stale or wrong result that passes that predicate. Trace whether it can become the final user-visible outcome, including when recovery trusts an already recorded success. Check the real guards on that path. If a positive claim survives only for the happy-path example, narrow it or retain the concrete finding and its evidence limits.

For a candidate finding establish the triggering condition, responsible boundary and consequence. Search for enforcement elsewhere, alternate paths, version differences and contrary results. Separate introduced or worsened behavior from unrelated pre-existing debt. Distinguish confirmed, refuted and unresolved claims. A failed tool, a vote or a green unrelated test cannot settle them. Keep consequential unresolved risks visible.

For suspected unnecessary work, name a simpler available mechanism and compare it on the same inputs and contract. Check who is authoritative, freshness, security, consistency, compatibility, error handling and lifecycle as applicable. Show the actual extra dependency or coordination and what the alternative preserves. A deliberate cache, request or layer may supply a necessary guarantee. Record justified costs, verified avoidable burdens, unresolved choices and evidence gaps according to what the comparison supports.

[Methodological sources](sources.md) document the origin of these techniques.
