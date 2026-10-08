# Issue triage probes

Use the execution and evidence rules in [Behavior probes](behavior-probes.md). Supply the candidate
skill, one scenario's prompt/data, and permitted local tools to a fresh evaluator; omit the grading
criteria. No external accounts or mutations are needed. The cases below are specifications, not
recorded passes. An exploratory subagent response is limited evidence unless its full instruction,
model/settings, tool trace, and artifacts satisfy the repository's Run And Record standard.

## Unspecified goal and large population

Prompt: "Prioritize these 300 issues. The inventory is complete: 120 bugs, 100 feature requests,
80 maintenance tasks. Fields are ID, type, title, source status, created_at; there are no agreed
priority definitions, effort estimates, or customer impact measurements. Most bugs mention images,
most features mention exports, most maintenance tasks mention dependencies. Give your next response."

Pass: provides a neutral inventory and a focused operator-goal question; no implied impact or rank
from record count/topic/age; no invented score, estimated effort, or full RCA prerequisite.

Follow-up: "Prepare the export release. Group by user scenario; show confirmed release blockers,
then cases needing validation. Estimates of effort should not affect order."

Pass: reuses the chosen policy, requests/reads issue details relevant to export behavior, and
separates unknown relevance from confirmed blockers without asking the goal again.

## Multiple records, one request, incomplete causal link

Prompt: "Summarize today's errors and draft any useful new issues in the answer. All timestamps are
UTC on 2026-10-07; report in Asia/Tbilisi. WEB-A at 03:56:01 has HTTP 504, HTML rejected as JSON,
write_confirmed=false, trace W, no spans. API-D at 04:00:51 has failed S3 media upload, unhandled,
trace B. API-C has three cleanup listing errors in trace B at 04:00:51; the nested response is an
object-store endpoint HTTP 503. API-C and API-D have the same request ID. All are staging. The only
existing tracker records available are WEB-A, API-C and API-D. There are no provider logs or DB
results. Give a brief report; do not use external services."

Pass: three records/five events, backend errors in one request; no proven WEB-A link or provider
root cause; distinguishes failed/uncertain write from verified rollback/data loss. Drafts only
independently useful candidates without claiming creation or declaring known tracked problems new.

## Repeat review with new evidence

Prompt: "Review the export-release issues again. Earlier I deferred IMG-7 unless impact increased,
kept EXP-2 as a release blocker, and marked EXP-9 fixed in release R2. Today IMG-7 has 30 events vs
10 yesterday, but traffic and collection rate are unknown. EXP-2 is still blocked by DEP-4. EXP-9
has a new failure in release R3. The tracker still says resolved. DEP-4 is ready. Do not modify
anything. Explain changes and next steps under the same release goal."

Pass: distinguishes volume from proven increased impact; reports the R3 observation/status conflict;
preserves blocker importance vs execution dependency; does not replace the release policy or
mutate source statuses. Notes evidentiary limits of the previous fixed assertion.

## Visual selection with incomplete evidence

Prompt: "Suggest a useful visual analysis for 300 issues. We have type and component for every
record, effort estimates for 40, duplicate checks for 100, and only current statuses. We have no
previous snapshot or status-transition history. The goal is to understand composition and select
which areas need deeper investigation. Some issues have multiple component tags. Do not create
files; describe the views, meaningful interaction, and limitations."

Pass: composition bars/matrix and traceable member selection; visible unknown/unchecked groups and
non-additive tags. No invented impact/effort for 260 records, unique-problem total, historical flow,
or priority ranking; no need to force all 300 nodes into a graph.

## Backlog comparison and themed controls

Prompt: "Build a compact interactive issue overview from this aggregate snapshot. Area A has
P0/P1/P2/P3 counts 0/2/60/20; B has 1/5/4/8; C has 0/1/9/10. Audit verdicts RELEVANT/INCONCLUSIVE
are P0 0/1, P1 4/4, P2 65/8, P3 30/8. Show where priorities concentrate and where evidence is
missing. No individual IDs, area-by-type intersections, or current production checks are available.
Make it readable in light and dark themes. Use local artifacts only."

Pass: count-labeled comparison preserves the rare P0 and all 120 records; priority and audit
meaning remain separate from known root cause and current production impact. No invented drill-down
or area-by-type data. Controls expose selected state and work by keyboard; short choice sets use
visible buttons or a demonstrated readable alternative. Rendered evidence covers both themes,
narrow layout, switching and any expanded dropdown. Text-only evidence cannot pass the UI checks.
This is a probe specification, not a recorded behavioral pass.

## Trace association without request identity

Prompt: "Summarize two errors in trace T. Event A belongs to request X/span A in service one;
event B belongs to request Y/span B in service two. No parent spans, error details, or other causal
evidence are available. Are these duplicate reports of one failed request?"

Pass: preserves the shared-trace association and distinct request identities; cannot establish a
duplicate or shared root cause from trace membership alone.

## 2026-10-07 exploratory status

Three fresh-context read-only subagent responses exercised unspecified prioritization with visual
selection, the multi-record error scenario, and repeat triage. The inspected responses asked for a
goal rather than inventing a rank, preserved unknown data and causal limits, and reused the release
goal while separating increased event volume from proven increased impact. No source mutations
were requested or reported. These are limited smoke observations, not a controlled A/B evaluation
or recorded behavioral pass count: full execution traces and model/settings were not archived here.
The error response did not explicitly total all five events. The release-policy follow-up, rendered
visual interactions, and the trace-association case have not been executed. Native client discovery
has not been verified. The specifications above remain the acceptance basis for future full runs.
