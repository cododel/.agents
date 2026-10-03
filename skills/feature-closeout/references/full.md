# Full closeout

Apply the common review invariants in `../SKILL.md` to actual acceptance and integration risks.
Select only useful review vectors; use independent read-only contexts when they add meaningful
evidence or independence is explicitly requested. Size or compaction alone does not require fan-out.

Useful vectors are:

- frozen motivation, scenarios, decisions, invariants, non-goals, and acceptance coverage;
- callers/consumers, state/data/event flow, configuration, persistence, cleanup, and compatibility;
- quality, security, failure paths, concurrency, resource lifecycle, and migration risk where relevant;
- QA and test-evidence adequacy.

Give reviewers exact read-only targets and evidence requirements without builder conclusions when
independence matters. If required independent contexts are unavailable, continue useful inline review
and disclose the missing evidence rather than claiming independence.

Prefer focused behavior/regression tests or runtime probes. Retain permanent tests for critical
behavior, bug regressions, and business rules when their maintenance value justifies them; temporary
probes may provide stronger falsifiable evidence at difficult seams. Broaden suites only for affected
risk or project policy.

Allow at most **two** authorized repair/recheck rounds. Re-review only invalidated vectors; after the
limit, hand off remaining blockers and evidence rather than continuing an open-ended audit/fix loop.

- `PREPARED`: no confirmed in-scope blocker remains and material acceptance has evidence.
- `BLOCKED`: an unresolved operator fork, missing decisive evidence, or confirmed defect remains.
