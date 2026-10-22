# Assessment rubric

These are provisional decision aids, not validated psychometric scales. Keep design judgments
separate from observed effectiveness. Unknown is not zero. Do not sum or average the scores below,
calculate a bureaucracy percentage, or treat more documented functions as automatically better.

## Countable units

An obligation is a distinct required action or constraint with an application condition, actor and
observable result or boundary. Record missing elements as uncertainty, not as invented requirements.
Distinguish mandatory, conditional and optional provisions.

Count semantic obligations, not sentences, bullets, words such as "must", documents or tool calls.
Split independently satisfiable duties; do not split requesting and awaiting the same approval into
two approvals. Deduplicate references to the same duty. Separate genuinely different decisions even
when written in one sentence. A prohibition does not imply a recurring inspection unless prescribed.

Useful counts for a scoped scenario include:

- unique obligations and applicable executions of each obligation;
- approval decisions, serial blocking gates and responsibility handoffs;
- manually maintained representations of the same information;
- checks with distinct claims, recurrence triggers and loop exit conditions;
- obligations whose actor, result, trigger or completion boundary cannot be resolved.

These categories overlap: an approval may also be a gate and a handoff. Do not add category totals
as if they were disjoint work. Alternative branches are not simultaneous executions. Separate setup
from recurring work. Unknown recurrence remains unknown; use explicit scenarios or ranges when useful.
A high count is descriptive, not evidence of excess.
Separate action executions from applicable constraints and permissions. Reusing an existing approval
does not itself imply another operation; report the counts separately rather than treating every
applicable obligation as work. State the counting boundary and preserve it across comparisons.

With evidence, estimate cost as setup cost plus the sum of execution frequency times per-execution
cost. Keep human effort, agent/computation cost and elapsed waiting distinct. Do not sum parallel
waits into project delay or infer active work time from message timestamps. Label estimates and
include consequential maintenance or rework costs when supported. Text alone rarely establishes cost.

## Useful functions and marginal contribution

Identify functions needed for this task: direction and shared intent; authority and accountability;
coordination; error prevention or detection; recovery; retained decisions; observable completion.
These are prompts, not a mandatory list of artifacts or universal requirements.

For an obligation, ask what would be lost if it were removed while other mechanisms remained.
Name its beneficiary, result and mechanism. Distinguish a stated purpose, a plausible design and
observed effectiveness. Unknown purpose is not proven absence of purpose. Consider operator and
user interests, not only agent convenience.

Evaluate complementary controls together when their value depends on the combination. Checks of
the same risk can provide independent protection; shared purpose alone does not establish duplication.
Do not credit every copy of information with the full benefit of the original source. Missing
necessary controls cannot be compensated by high scores on unrelated controls.

## Load justification: J0-J4

Score a specific obligation or coupled set within a stated scenario. For rules alone, label the score
"design assessment"; for execution, state which costs and benefits are actually observed.
Name the assessed unit before scoring; do not change its boundaries to obtain a different score.

| Score | Anchor |
| --- | --- |
| J0 | Burden exists and evidence establishes no needed function, or a conflict with the agreed objective. |
| J1 | A useful function exists, but most of the examined obligation is redundant or does not support it. |
| J2 | Useful contribution with a specific excess in frequency, scope, approvals or representation. |
| J3 | A credible mechanism and appropriate application support a needed function; no clear excess is established in the examined options. |
| J4 | Comparison supports this design over considered alternatives: it preserves needed functions with less burden, or adds material benefit at an acceptable cost. |

Use "undetermined" when evidence cannot distinguish the anchors. State what supports the selected
level and any decisive uncertainty. J4 is not a global optimum; a lack of examined alternatives does
not earn it. A high-stakes label alone does not establish an effective control. Do not obtain a lower
cost by silently changing acceptance, permissions or tolerated risk.

## Necessary function coverage: G0-G2

First establish which functions are needed in the scoped task. Then rate each applicable function:

- G0: no mechanism covers the necessary function in the examined process.
- G1: partial coverage; a material gap or ambiguity remains.
- G2: the process design covers the function under the stated conditions.
- Undetermined: the available sources do not establish coverage.

G2 is design coverage, not proof of operating effectiveness. Existing platform mechanisms, direct
instructions or shared conventions may provide coverage without another document. Do not average
away a critical gap. Where rules are incomplete, distinguish missing documentation from absent
practice. Process overhead can be excessive while essential functions remain uncovered.

## Consequence and reach

Describe actual extra actions, effort, waiting, rework or blocked outcomes when known. Mark reach
separately: isolated episode, recurring mechanism or process-wide requirement. Do not maintain a
second mandatory numerical severity score; justification, coverage and concrete consequences suffice.

## Calibration cases

During skill development, compare judgments on meaningful contrasts: risky migration versus trivial
edit; renewed approval after target change versus unchanged authority; rerun after shared-core change
versus unchanged evidence; independent checks versus duplicate records; high-level adequate process
versus detailed but unowned workflow; fresh data revealing a defect versus unsolicited new scope.

Also test a process with few rituals but lost decisions or no completion boundary. For evaluator
robustness, vary irrelevant formatting, author labels and comparison order while preserving substance.
Preserve temporal order in execution histories. Compare with human-reviewed cases; evaluator agreement
alone is not validity. These are development checks, not required steps in each audit.
