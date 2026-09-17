# Recording the agreed task

Use a written record when requirements, decisions, or handoffs are hard to retain, including medium
work, or when the operator requests one. Briefing itself does not require a file.

## Reuse task memory

Use `$task-journal` for storage and lifecycle: the current checkout's
`.tmp/tasks/<task-id>/task.md` is the same task record used by implementation and closeout.
Do not create a separate default brief or duplicate the target in the working-state file.
Read `../assets/brief-template.md` for the content boundary and use the task-journal template.
An explicitly requested export is a deliverable, not a second independently maintained task owner.

## Record agreement accurately

Capture the current agreed motivation, observable behavior, constraints, non-goals, and acceptance.
Separate unresolved proposals from confirmed content. Agreement may already exist in the request or
conversation; recording it needs no additional approval ceremony.

When a material requirement changes, retain unchanged agreement, record the confirmed replacement and
its decision source, and invalidate affected evidence/assignments in state. Do not reset the whole
task to Draft or preserve a superseded first request as the acceptance target. A proposed default or
implementation choice does not establish agreement.

## Handoff

Continue authorized implementation once material questions are resolved. Keep execution details and
verification in state, referring to task criteria rather than copying them. At completion compare the
result to the current agreed task. Update existing durable owners when their guarantees change;
create a new contract only under the contract-writer value test. Report unrelated debt; record an
Issue/TODO only on request. Do not automatically delete or promote the working records.
