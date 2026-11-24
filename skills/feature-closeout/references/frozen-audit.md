# Explicit frozen final audit

Run this procedure only when the user requests a frozen independent final audit or uses legacy
`--release` / "release closeout". Explain that these aliases request preparation followed by a separate read-only audit.

First complete ordinary preparation within the granted authority and any applicable release evidence not already covered by current
results. If preparation is not `PREPARED`, report `NOT READY` for a confirmed blocker or `UNVERIFIED`
for missing required evidence; do not claim the final audit ran.

Freeze the final exact source fingerprint, then run **one independent read-only final review**. Use
`$contract-auditor` when living contracts materially govern the feature or contract/rollout compliance
is requested; otherwise use a bounded release reviewer. Its own audit constraints still apply.
If the required isolated reviewer is unavailable, return `UNVERIFIED`.

Once the frozen audit begins, neither reviewer nor primary may repair that snapshot. Any fix or
repeat leaves this invocation and requires authorization covering that action; reuse an existing
operator instruction when it covers the continuation. A later review resolves a new fingerprint.
Return the verdict before any separately authorized continuation. When using `$contract-auditor`,
preserve its verdict and stated boundary unchanged, including `READY WITH ACCEPTED RISKS`;
`NOT READY` for contract noncompliance does not by itself assert a rollout blocker.
The labels below apply to the other bounded release-review path.

- `READY`: required local/review evidence supports the requested handoff.
- `NOT READY`: a confirmed blocker exists; also disclose coexisting verification gaps.
- `UNVERIFIED`: no confirmed blocker, but required evidence or independent review is unavailable
  or cannot be trusted.
