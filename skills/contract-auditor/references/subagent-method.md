# Contract audit subagent method

Use this method for one bounded, read-only review vector. Do not modify any file or external state.

## Required input

The orchestrator supplies:

- `vector_id` and its exact concern;
- repository root, worktree, target HEAD, base revision, and change inventory;
- snapshot fingerprint for the immutable audit target;
- contract inventory with paths, scopes, and stable rule IDs;
- named risks and scope exclusions;
- absolute paths to this method, `evidence-and-verdicts.md`, and
  `../../contract-writer/references/contract-spec.md` resolved by the orchestrator.

Return `missing_input` when any required item is absent. Read the referenced methods and every
contract assigned to the vector. Do not trust summaries when the source artifact is available.

## Review procedure

1. Inspect only the assigned vector across the full affected call-site and configuration radius.
2. Map each applicable contract rule to exact implementation evidence.
3. Locate existing tests or declared executable evidence and run focused checks when authorized.
4. Inspect negative paths appropriate to the vector; do not infer cleanup, rollback, or retry
   safety from a happy-path test.
5. Reverse-check changed durable behavior for missing ownership.
6. Record only evidence-backed findings. Check reachability and existing mitigations before
   proposing a blocker. Mark ambiguity as a gap, not a defect.
7. Do not assign the overall rollout verdict; return inputs for the orchestrator to decide it.

## JSON output

Return one JSON object only:

```json
{
  "vector_id": "contract-traceability",
  "target": {"head": "<sha>", "base": "<sha>", "snapshot_fingerprint": "<hash>"},
  "coverage": ["<surface>"],
  "rule_results": [
    {
      "rule_id": "docs/UI_CONTRACT.md#loading:1",
      "contract_path": "docs/UI_CONTRACT.md",
      "statement": "<normative rule>",
      "code_evidence": ["src/ui/view.ts:42"],
      "verification_evidence": ["test: command -> result"],
      "verdict": "compliant",
      "evidence_level": "executed"
    }
  ],
  "named_risks": [
    {
      "risk_id": "server-leak",
      "dimensions": {
        "lifecycle": "compliant",
        "cleanup": "compliant",
        "concurrency": "unverified",
        "detection": "partial",
        "runtime": "unverified"
      },
      "evidence": ["<path, command, or timestamped observation>"]
    }
  ],
  "findings": [
    {
      "finding_id": "<stable per-run id>",
      "class": "verification-gap",
      "severity": "high",
      "readiness_effect": "risk",
      "confidence": 0.72,
      "proof_kind": "observed|executed|derived|none",
      "cascade": {
        "classification": "root|confirmed-consequence|cascade-candidate|independent",
        "root_finding_id": "<stable finding id or null>",
        "causal_parent": "<finding id or null>",
        "causal_edge": "<control/data/persistence/ownership/resource edge or null>",
        "missing_proof": "<required evidence for a cascade-candidate or null>",
        "depth": 0
      },
      "blocker_gate": {
        "rule_or_named_risk": false,
        "production_reachable": false,
        "trace_complete": false,
        "mitigations_insufficient": false,
        "impact_high_or_blocker": false,
        "proof_sufficient": false
      },
      "rule_or_risk_id": "server-leak",
      "root_cause": "No concurrent shutdown exercise",
      "affected_surface": "worker lifecycle",
      "reachability": "<production entry to harmful result, or unverified>",
      "mitigations_checked": ["<guard or fallback checked>"],
      "reproduction": "<exact command/result, or unavailable reason>",
      "evidence": "Only single-worker cleanup is tested",
      "recommendation": "Run the bounded concurrent lifecycle probe"
    }
  ],
  "gaps": ["<unavailable evidence and why>"],
  "commands": ["<exact read-only command and result>"],
  "errors": []
}
```

Allowed rule verdicts are `compliant`, `partial`, `violated`, and `unverified`. Allowed finding
classes and evidence levels come from `evidence-and-verdicts.md`. Use repository-relative paths in
evidence. Never return secrets, private customer data, or irrelevant raw logs.
