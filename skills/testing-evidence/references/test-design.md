# Test Design And Boundaries

## Oracle and value

Name the realistic defect/refactor the assertion detects, its observable result, expected-result
source and responsible production path. Prior incident history is not required. Expectations may
come from agreed behavior, independent arithmetic/examples, protocol/schema, a meaningful invariant,
or independently observed output. Calling the production algorithm to compute its own expected result
is not independent. Preserve legitimate metamorphic/round-trip contracts when the transform and
identity obligation are actually exercised; they do not prove all business meaning of the input.

Find the existing guarantee before adding tests. Expand an existing case/parameterization when the
same boundary is being protected. Separate tests are justified by distinct failures, consumers,
oracles, lifecycle/error phases or platforms. Similar names/shared fixtures do not prove duplication.
Retain permanent protection when its regression value justifies maintenance; temporary probes can
be stronger evidence at a difficult seam without becoming a new permanent framework.

## Doubles and realistic failures

- Payment callback: mock supplies provider input; production must perform the PAID transition.
  A callback fake that sets PAID itself cannot prove that transition.
- DB fencing/uniqueness/rollback: fake selection can test application handling of outcomes; it cannot
  certify DB eligibility, locking or durability if the fake always supplies the correct outcome.
  Use verified disposable integration evidence for those guarantees, or narrow the claim.
- Deferred autoflush failure: raising at method entry bypasses the transaction phase under test.
  Trigger the relevant flush/commit boundary; distinguish a commit from acknowledgement loss.
- Negative side effect: a raising stub is insufficient if production catches its exception. Observe
  zero calls/awaits, and use an allowed-input control when needed to rule out an inert handler.
- Concurrency: reaching a barrier before SQL is not proof of lock overlap. Observe the responsible
  contention/scheduling boundary where the guarantee depends on it.
- Rendering/media: mocked request arguments do not prove resulting pixels/alpha. Verify actual output
  at a suitable boundary; no need to test the whole live provider for a local adapter contract.

Controlled clocks/barriers/transport failures and mocks are legitimate when they preserve the causal
semantics. Avoid building a second DB/business engine in a fake merely to manufacture proof.

## Contracts versus incidental pins

Exact literals can be independent money/policy/wire expectations. Structural checks can enforce a
single migration head, forbidden imports or packaged-source integrity. Mocked DDL/send calls can
verify fail-before-action or required command construction. Retain that narrow obligation; separately
verify real schema/query/network state when the claim requires it. Source text or token order alone
does not establish runtime behavior. Snapshot updates need an agreed behavior change or demonstrated
check defect, not a failing implementation's convenience.

Examples: independent 60→69 protects a 15% rule even if a neighboring assertion imports the same
constant; an incidental release-version pin differs from recomputing bytes against a source hash.
A no-network source-order check can survive removal of early return; execute the handler with
observable zero calls and a positive control. A JSON-pool test with only existing files preserves
acceptance but can miss validation being removed: add a missing second path, not a second happy path.

## Safe scoped legacy decisions

Retain a meaningful narrow guarantee; strengthen a concrete oracle/boundary gap; consolidate only
verified equivalent protection with unique cases retained. For a live guarantee, retirement needs
verified surviving/replacement protection. For a legitimately obsolete requirement, establish its
cancellation and absence of dependent consumers or remaining obligations; no meaningless replacement
is needed. Investigate names missing contract/cancellation/consumer/helper/selection/replacement
evidence and how it changes the decision. Unknown is not permission to remove.

No numerical quality threshold, mock/source smell, green frequency, coverage total or no-incident
history authorizes deletion. Authorization for remediation is separate from an audit verdict.

## Avoid artificial protection

Choose evidence for the risk and claim, not because a particular file changed. Prose documentation
usually needs content/reference/example review, not tests pinning phrases. A skill's effectiveness
needs observed agent decisions; static links/frontmatter prove structure only. Grafana JSON snapshots
or field-presence checks need a meaningful datasource/query/units/consumer contract to justify them;
otherwise review the content and verify the actual relevant behavior. Real schemas, source-integrity
and architecture/API contracts remain legitimate. Purpose may be clear in group code/name; no
mandatory justification form or checklist for every assertion.
