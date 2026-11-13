---
name: bug-report
description: "Prepare or review a bug report, including evidence for a fix PR. Use for requested report content or content review; not ordinary diagnosis, brief findings summaries, investigation, general PR authoring, or tracker lifecycle operations."
---

# Bug Report

Make the reported problem understandable and independently checkable. This skill owns report
content, not defect discovery, causal investigation, tracker selection, or publication authority.
Use the recipient's language and template; fill semantic gaps without duplicating fields or
imposing a second format. No separate template or report file is required.

## Establish the evidence

Use the supplied findings and available sources within the authorized task. Distinguish reported
observations from behavior personally reproduced. When verification needs design or interpretation,
use [testing-evidence](../testing-evidence/SKILL.md); diagnosis remains with the relevant investigation
workflow. Do not expand research merely to complete a report field.

Missing applicable facts are explicit gaps, not permission to invent steps, attempts, paths, code
locations, causes, remedies, or artifacts. Omit inapplicable details. If a gap violates agreed
readiness criteria, label the result an incomplete draft and identify the missing material. An
unknown cause or unavailable source code need not prevent a useful report of an observed defect.

## Report content

Adapt the structure to the recipient while preserving these applicable elements:

- **Problem and impact:** a specific title, observed failure, consequences, and affected scenario
  boundaries. Follow established priority/severity conventions; do not invent a ranking.
- **Environment:** version or build, relevant platform/configuration, prerequisites, and test data.
  Identify the tested artifact precisely enough to reproduce the observation.
- **Reproduction:** minimal steps, expected behavior with its requirement/documentation or other
  evidenced basis, and actual result. Give observed successful reproductions / attempts when
  measured; otherwise state the repeatability limit without inventing counts.
- **Evidence:** apply the shared [review evidence standard](../_shared/review-evidence.md). Include
  artifacts that establish the reported claim, distinguish helpful context from proof, and identify
  missing required evidence explicitly.
- **Code and mechanism:** when sources are accessible, identify relevant code at the affected
  revision with verified links or locators. Separate the symptom location, established causal chain,
  and hypotheses. Code access alone does not establish the cause; record unresolved attribution.
- **Repair and verification:** propose an evidence-backed fix direction, rationale, material limits,
  and a way to check the result when supported. Distinguish a proposal from an implemented or tested
  fix. If the cause is unknown, give a supported next distinguishing experiment instead of a
  speculative remedy; say when no such experiment is yet established.
- **Confirmation limits and context:** known workaround, related records, and material gaps when
  established. Claim platform exclusivity or regression only with comparative evidence; absence of
  comparison is a limit, not proof of either claim.

## Fix reports

For an implemented fix, distinguish evidence of the original problem from evidence of the result
after the change. Identify the relevant revisions, scenario and expected/observed outcome for each;
use comparable conditions or explain material differences. Reuse valid existing evidence without
requiring a new baseline run merely to populate the report. Original-failure artifacts do not prove
the fix. RED/GREEN tests establish their exercised boundary, not untested native UI behavior.
If an after-change outcome has not been checked, state that gap and keep any dependent readiness
claim incomplete. A proposed remedy is not an implemented or verified fix. No fixed headings or
additional investigation outside task authority are required.

## Review and delivery

Check that steps, expected result, evidence, code attribution, and proposed remedy support the same
scoped claim. Preserve uncertainty when editing another author's report. For a review-only request,
report missing or unsupported content without rewriting or publishing it unless requested.

Return the report or review through the requested channel within existing authority. Preparing a
report does not authorize publication, attachment uploads, local Issue creation, or further
investigation outside the agreed task. Reuse established permissions and the operator-selected
tracker workflow; report quality does not confer write authority or require renewed approval of an
already authorized action. Tracker state, duplicates, and lifecycle remain with that workflow.

## Optional review preview

When a rendered preview is requested, use [markdown-preview](../markdown-preview/SKILL.md) for the
canonical Issue or fix-PR drafts. Apply the fix-report evidence requirements above when preparing
content for a fix-PR preview.
