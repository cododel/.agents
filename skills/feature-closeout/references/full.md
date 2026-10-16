# Full closeout

Apply the common completion invariants in `../SKILL.md` to actual acceptance and integration risks.
Select only useful review vectors; use independent read-only contexts when they add meaningful
evidence or independence is required by the request or project.

If required independent contexts are unavailable, continue useful inline review and report `BLOCKED`;
self-review does not satisfy required independence. An optional additional reviewer is not a gate.

Continue independent work while a decision is pending. There is no fixed repair-round limit.

If the same finding recurs without new decisive evidence, diagnose the missing link rather than
blindly repeating. Report the concrete blocker when a missing decision, prerequisite, required
evidence, authority or agreed resource limit prevents further progress; resume when it is resolved.

- `PREPARED`: no confirmed in-scope blocker remains and material acceptance within the agreed
  completion boundary has evidence. Separately assigned later operator checks remain
  pending/unverified; they do not prevent a prepared local handoff.
- `BLOCKED`: an unresolved operator fork, missing decisive evidence required at the current
  completion boundary, or another concrete barrier prevents further authorized progress on an
  in-scope defect. Identify the unmet criterion and required decision, prerequisite, authority or
  agreed resource limit. An obvious repairable defect triggers the next repair/recheck cycle;
  a separately assigned later operator check alone is not a blocker.

## Explicit frozen final audit

Run this procedure only when the user requests a frozen independent final audit or uses legacy
`--release` / "release closeout". It is documented here for invocation compatibility, but is a separate
read-only audit after preparation, outside the closeout repair loop; never infer it from ordinary Full.

First complete Full preparation and any applicable release evidence not already covered by current
results. If preparation is not `PREPARED`, report `NOT READY` for a confirmed blocker or `UNVERIFIED`
for missing required evidence; do not claim the final audit ran.

Freeze the final exact source fingerprint, then run **one independent read-only final review**. Use
`$contract-auditor` when living contracts materially govern the feature or contract/rollout compliance
is requested; otherwise use a bounded release reviewer. Its own audit constraints still apply.
If the required isolated reviewer is unavailable, return `UNVERIFIED`.

Once the frozen audit begins, neither reviewer nor primary may repair that snapshot. Any fix or
repeat requires leaving the audit, a new fingerprint and a new explicit invocation. Return the
terminal verdict without automatically repairing or restarting.

- `READY`: required local/review evidence supports the requested handoff.
- `NOT READY`: a confirmed blocker exists; also disclose coexisting verification gaps.
- `UNVERIFIED`: no confirmed blocker, but required evidence or independent review is unavailable
  or cannot be trusted.
