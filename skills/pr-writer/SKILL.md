---
name: pr-writer
description: "Prepare, update or review pull request titles, descriptions and demonstrations for features, fixes and other changes. Includes review previews; not code implementation, a standalone bug report, Git synchronization, merge, or ongoing PR monitoring."
---

# Pull Request Writer

Explain the concrete problem or need and the behavior resulting from the actual change. Write for
a reviewer who has not read the conversation. Follow the recipient's language and PR template,
adapting detail to the change rather than imposing a second template or a fixed section count.

## Ground the description

Read the agreed task, relevant Issue when supplied, intended base and current diff. Resolve repository
facts from sources; ask only when missing intent or a material target boundary cannot be established.
Describe the final implementation, not an earlier plan or a list of commits/files. Rewrite stale titles
and descriptions when the change's scope evolves. Preserve unrelated operator-authored content.

Prepare only the requested content. A review-only request returns findings; it does not edit the draft
or remote PR. Authoring does not authorize implementation, push, PR creation, uploads, Issue lifecycle
changes, merge or deployment. Use existing permissions and the selected workflow for those actions,
without asking again about actions already covered by unchanged authority.

## Content by change

- **Feature:** state the need, resulting behavior and how it is used. Explain material implementation
  choices only when they help review the result. Do not invent a prior failure for new capability.
- **Known Issue fix:** link the Issue and summarize the relevant problem, change and result. Do not
  copy the full bug report; retain enough context to understand the PR and note material differences
  from the original report. References and completion claims must match actual scope and authority.
- **Fix without a sufficient report:** include the necessary problem/reproduction context using
  [bug-report](../bug-report/SKILL.md). Do not create a separate Issue merely to fill this role.
- **Refactor or maintenance:** explain the reason, intended preserved behavior and evidence of
  compatibility. For documentation/configuration/infrastructure, state the practical effect and
  relevant application conditions rather than forcing a product demo.

For all changes, include meaningful verification actually performed and its environment or revision
when material, plus remaining uncertainty. Mention compatibility, migration, configuration, operational
limits or reviewer instructions only when relevant. A small change can need only a short paragraph
and a verification note. Omit conversation history, generic checklists and unsupported readiness claims.

## Demonstration and verification

Use the shared [review evidence standard](../_shared/review-evidence.md) for selection, captions,
media and attachment handling. For a defect correction, apply [fix-report evidence](../bug-report/SKILL.md#fix-reports)
to distinguish the original problem from the after-change result without duplicating the full report.
Successful tests support their tested boundary; they do not establish unperformed GUI or production
acceptance. Report missing applicable evidence explicitly, keeping dependent readiness incomplete.

## Draft, preview and delivery

Maintain one canonical Markdown body and the actual proposed title. Save the body as `.md` when
preview or file delivery is needed; a simple response-only description needs no separate file.
Use the same body for later authorized publication rather than rewording a second copy.

For a PR containing media, or an explicit preview request, render through the existing
[review wrapper](../_shared/markdown-review/README.md) and open it in an available embedded browser
when ready. Use the manifest's title, target, stable ID and `kind: pr`; the body remains the actual
publication Markdown. Reuse the tab and bounded task-owned process, apply feedback to the Markdown,
and verify the refreshed render. Do not create a custom HTML duplicate. If preview is unavailable,
return the draft and the concrete preview limitation, without inventing a successful demonstration.

Deliver a simple text-only PR as text unless preview was requested. Neither route adds a new approval
gate: obey any established editorial review requirement and reuse existing publication authority.
After code changes, refresh affected description, demonstration and verification claims; do not rerun
unaffected checks merely because prose changed. State what is prepared, actually published, or still
unverified. PR creation does not start indefinite monitoring or authorize follow-up comments.
