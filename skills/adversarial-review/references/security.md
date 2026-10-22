# Security profile

Use for authorized vulnerability research in owned systems. Source access helps explain a weakness;
it does not grant the simulated attacker internal privileges or authorize attacks on dependencies.

## Establish the threat and execution boundaries

Identify protected assets/properties, actual trust boundaries, and relevant actors: anonymous caller,
ordinary user, another tenant, limited operator or a specifically scoped compromised component.
Record what each actor can control and which credentials, entrypoints and prerequisites they possess.
Ownership/access rules and explicit security requirements can establish a protected property even
without a dedicated contract. Cite that basis; ask about genuinely ambiguous intended authority.

Resolve the authorized execution targets and actions, including external providers and shared
environments. Distinguish local code research from remote testing. Use synthetic identities/data and
owned disposable targets for active probes under project rules. Configure containment before runtime
imports or commands that could use ambient credentials, dispatch effects or reach live systems.
Stop on unexpected external contact, target-identity mismatch or uncontrolled resource growth;
report what happened and reconcile owned effects before resuming.

## Generate reachable abuse cases

Inventory relevant exposed inputs and alternate entrypoints from actual routing, consumers and
configuration. Trace untrusted influence toward protected decisions or sensitive effects. Select
applicable attack families from that surface; do not require a universal vulnerability checklist.

For business logic, try skipping/reordering steps, replay, identifier/owner substitution, concurrent
use and combinations of individually allowed actions that violate a protected property. For other
surfaces, select appropriate authorization/session, injection, file/URL handling, secret exposure or
resource-exhaustion checks. Consult current primary references when a technique or dependency claim
requires verification; a scanner alert is a candidate, not a confirmed exploit.

Separate three claims: the code contains a weakness; an actor can reach it under stated conditions;
the resulting action violates the protected property. A direct internal call or fabricated privileged
state may establish only the first. Preserve conditional findings when deployment reachability is
unknown rather than asserting remote exploitability or discarding the weakness.

## Prove impact with minimal effects

Use testing-evidence for the reproduction, controls and causal claim. Prefer a synthetic victim,
canary or local receiver sufficient to demonstrate the unauthorized effect. Do not collect real
secrets, move real funds, establish persistence, or extend a compromise beyond the authorized proof.
Bound load/resource probes and stop once sufficient impact evidence exists. If safe reproduction is
unavailable, report the strongest source evidence and the missing confirmation explicitly.

Assess chains when they materially change reachability or impact, retaining each prerequisite and
cause. Rank by demonstrated consequence and actor capability, not the most alarming hypothetical
outcome. Record relevant attack preconditions alongside shared finding fields.

## Remediation and limits

Under existing repair authority, close the responsible trust/decision boundary and verify both the
original attack and legitimate operations. Blocking all inputs can stop a probe while breaking the
product. Check alternate affected entrypoints and variants justified by the same cause, without
turning every fix into another full security assessment.

Distinguish proven local exploitability from configuration-dependent exposure, provider guarantees,
and untested deployment controls. Report the assessed assets, actors and surface, remaining blockers
and required evidence. No findings means no confirmed vulnerability within those limits, not that
the system is secure against every attacker.
