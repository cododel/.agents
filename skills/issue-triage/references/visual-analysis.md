# Visual analysis for triage

Choose by the operator's analytical question and the available evidence. The operator controls
meaning and priority criteria; the agent chooses the smallest effective representation. Begin with
overview, allow selection/filtering, then expose member issues and evidence. Do not build a dashboard
merely because there are many records or require every view below.

## View selection

| Question | Useful view | Evidence requirement / limit |
|:--|:--|:--|
| What is in this collection? | Horizontal bars by work type, component, or source, with a linked issue list | State whether counting records or distinct problems; show unknown/unclassified and incomplete coverage |
| Where do categories concentrate? | Count-labeled heatmap: component by problem type, or environment by source status | Use compatible categories; overlapping membership is not additive; color is not priority |
| Which consequential cases lack evidence? | Categorical matrix of impact assessment by evidence sufficiency | Mark estimated impact as such; preserve unknown impact; do not manufacture numeric confidence |
| What is aging or stuck? | Age distribution or elapsed-time dots grouped by state | Distinguish creation age, last observation, last review, and time in state; current status cannot reconstruct transitions |
| What is worsening or recurring? | Time series for selected groups, optionally annotated with releases | Comparable intervals, traffic denominators when available, and collection coverage; coincidence is not causation |
| What blocks what, or belongs to one incident? | Small graph of the selected related cluster | Label edges as dependency, duplicate candidate, or causal link, with evidence/confidence; avoid a whole-backlog hairball |
| What changed since the last review? | Before/after comparison with a list of changed members | Comparable snapshots; separate additions/removals and changed criteria from actual state changes |
| Which candidates trade impact for cost? | Scatterplot or categorical matrix on operator-selected axes | Supported comparable estimates; show omitted/unknown values; axes and quadrants do not silently select a policy |

For a large first overview, a coverage note, one useful composition view, and a linked issue list
usually suffice. Add another view only for a distinct question. Workflow-flow charts require actual
transition history and a question about throughput or bottlenecks; a current backlog snapshot is
insufficient. Keep quantitative uncertainty categorical or ranged when exact values are unsupported.

## Preferred backlog views

For a categorical backlog overview, prefer a count-labeled matrix of area/component by work type
with a linked issue list; use area by source priority when that answers the question or type data
is unavailable. Separate totals by area and type cannot reconstruct their intersections: require
record-level membership or an actual cross-tab. Preserve unknown/unclassified values.

When comparing a priority across areas, use separate bars from a common zero baseline, optionally
selected by a priority control. Stacked bars suit composition but make interior segments harder to
compare. Do not let a large low-priority group visually erase a rare high-priority record: retain
explicit counts and labels. Volume and chart order do not establish an execution priority.

For deciding which work needs more evidence, offer a matrix of source priority by audit/evidence
status when those fields exist. Explain the status definitions: a confirmed unmet criterion does
not establish root cause, readiness to fix, or current production impact. Keep this distinct from
an impact-by-evidence view; neither silently chooses the operator's priority policy.

Use one view per decision, with a compact switcher when alternative views are useful, rather than
a long stack of overlapping charts. For a small set of views or priorities, prefer visible,
keyboard-accessible buttons with a clear selected state. Preserve selection and keyboard focus
when switching. Native dropdowns remain suitable for larger option sets if their expanded options
are readable in the active theme.

## Interaction and integrity

- With record-level data, every bar, cell, point, or node maps back to source/member IDs and evidence.
  An aggregate-only screenshot can support a labeled comparison prototype, but not invented IDs,
  cross-tabs, or a working issue drill-down. Disclose that limit. Preserve the filtered
  subset size and the broader population, including excluded, unassessed, and unavailable records.
- Filter by relevant fields and reveal selected issues. Presentation filtering is not approval,
  prioritization, assignment, or a tracker write. Comparing criteria does not adopt a new criterion.
- When handing a selection back for investigation, include explicit selected IDs and filters in the
  follow-up; do not rely on hidden visual state reaching the next turn.
- Disclose the snapshot time, period, units, aggregation, and material missing data. Do not imply a
  live connection. Do not sum records/problems/events/users or sum overlapping groups as unique totals.
- Keep comparable scales and grouping meanings stable across views; mark changes. A failed source
  read is unavailable data, not a zero. Do not infer recovery from declining telemetry alone.
- Keep missing values visible rather than silently removing hard-to-assess cases. Use ordinal
  categories for ordinal evidence, not invented decimal scores, scatter positions, or effort.
- Label meaningful colors and connections; use readable labels and keyboard-accessible interaction.
  Provide a textual/tabular equivalent and direct evidence links. Essential details cannot depend
  on hover or color alone.
- Use theme-aware foreground/background pairs. Check rendered light and dark appearances, narrow
  layout, selected/focused controls, and view/filter switching. If using dropdowns, check expanded
  options as well as the closed control; a dark field does not prove a readable native menu. Report
  any unverified rendering/interaction boundary rather than claiming a text design is a tested UI.

Dense all-issue graphs, many-slice pies, and word clouds seldom answer a triage decision. Prefer a
selected cluster, comparable bars, or a matrix. A table is often the right visual. A causal diagram
can help with three issues; three hundred issues need not imply three hundred plotted nodes.

## Design sources

These sources motivate the choices; they are not mandatory live dependencies on each run.

- [Shneiderman: The Eyes Have It](https://www.cs.umd.edu/users/ben/papers/Shneiderman1996eyes.pdf): overview, filtering, and details on demand.
- [Tableau: Choose the Right Chart Type](https://help.tableau.com/current/pro/desktop/en-us/what_chart_example.htm): match the analytical question to data and representation.
- [Datawrapper: Area chart considerations](https://www.datawrapper.de/academy/what-to-consider-when-creating-area-charts): shared baselines improve cross-category comparisons.
- [Linear Triage](https://linear.app/docs/triage): disposition and reconsideration of deferred work.
- [Sentry Issue Status](https://docs.sentry.io/product/issues/states-triage/): recurring and escalating observations.
- [Google SRE Incident Response](https://sre.google/workbook/incident-response/): mitigation and RCA have different immediate purposes.
