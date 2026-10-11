# Full closeout

Apply the common review invariants in `../SKILL.md` to actual acceptance and integration risks.
Select only useful review vectors; use independent read-only contexts when they add meaningful
evidence or independence is required by the request or project.

If required independent contexts are unavailable, continue useful inline review and report `BLOCKED`;
self-review does not satisfy required independence. An optional additional reviewer is not a gate.

Allow at most **two** authorized repair/recheck rounds; after the limit, hand off remaining blockers
and evidence rather than continuing an open-ended audit/fix loop.

- `PREPARED`: no confirmed in-scope blocker remains and material acceptance within the agreed
  completion boundary has evidence. Explicitly separate later deployment/live checks remain
  pending/unverified; they do not prevent a prepared local handoff.
- `BLOCKED`: an unresolved operator fork, missing decisive evidence required at the current
  completion boundary, or confirmed in-scope defect remains. Identify the unmet current criterion;
  a separately agreed post-deploy check alone is not a blocker.

## Explicit frozen final audit

Run this procedure only when the user requests a frozen independent final audit or uses legacy
`--release` / "release closeout". It is part of Full, not a separate mode or an automatic next step.

First complete Full preparation and any applicable release evidence not already covered by current
results. If preparation is not `PREPARED`, report `NOT READY` for a confirmed blocker or `UNVERIFIED`
for missing required evidence; do not claim the final audit ran.

Freeze the final exact source fingerprint, then run **one independent read-only final review**. Use
`$contract-auditor` when living contracts materially govern the feature or contract/rollout compliance
is requested; otherwise use a bounded release reviewer. Its own audit constraints still apply.
If the required isolated reviewer is unavailable, return `UNVERIFIED`.

Once the frozen audit begins, neither reviewer nor primary may repair that snapshot. Any fix or
repeat requires leaving the audit, a new fingerprint and a new explicit invocation. Return the
terminal verdict without automatically repairing or restarting. This grants no deployment authority.

- `READY`: required local/review evidence supports the requested handoff.
- `NOT READY`: a confirmed blocker exists; also disclose coexisting verification gaps.
- `UNVERIFIED`: no confirmed blocker, but required evidence or independent review is unavailable
  or cannot be trusted.
