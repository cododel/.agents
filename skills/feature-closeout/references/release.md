# Release closeout

Release must be explicitly requested. First satisfy Full (`PREPARED`) using [full.md](full.md), then add the
project's actual release evidence:

- relevant suites, builds, migration and generated-artifact checks;
- upgrade/downgrade or mixed-version behavior where applicable;
- rollback/recovery and feature/action gates;
- observability, operator controls, cleanup ownership, and failure isolation;
- production-shaped evidence supplied locally or through authorized read-only tools;
- task-owned process termination and a final exact source fingerprint.

Run **one final independent read-only review** on that frozen fingerprint. Use `$contract-auditor`
when living contracts materially govern the feature or contract/rollout compliance is requested;
otherwise use a bounded release reviewer. The terminal reviewer cannot fix findings. Use an existing
isolated reviewer context; if none is available, return `UNVERIFIED` rather than simulated independence.

Any resulting fix requires leaving the frozen review, producing a new fingerprint, and an explicit
new Release review invocation. No deploy, push, merge, remote mutation, or shared/persistent database
action is implied.

- `READY`: required local/review evidence supports the handoff.
- `NOT READY`: a confirmed blocker exists.
- `UNVERIFIED`: required evidence is unavailable or cannot be trusted.
