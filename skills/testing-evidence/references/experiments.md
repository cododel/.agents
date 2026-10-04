# Temporary Experiments And Operator Demos

Use a temporary PoC or interactive operator demo when it resolves a material API/design/UX or
implementation uncertainty more cheaply than production integration. It is an evidence choice,
not an extra mandatory phase. Clear known work proceeds directly; choose the next action by what
uncertainty it removes rather than by a fixed implementation/refactor ceremony.

Identify the question, smallest experiment, observable answer and stop condition. This may be a
brief sentence, not a form. Work in a disclosed task-local temporary directory, using synthetic data
and minimal established dependencies. Existing global scope, service/credentials/spend/data safety
and process-cleanup boundaries apply; a demo does not authorize production access or publication.

Possible evidence: a minimal API interaction against a verified local fake/sandbox, an interactive
mock of two UX alternatives the operator can inspect, or a focused probe of a library behavior.
Do not build an entire framework or compulsory permanent tests for a disposable question. Stop once
the question is answered or the chosen boundary cannot safely resolve it; report that limit instead
of expanding the experiment silently. Operator feedback establishes a decision only when confirmed.

Before promotion, distinguish prototype observations from agreed product requirements. Implement
the chosen behavior with integration/consumer, error, lifecycle and relevant security/data checks.
A successful demo is not production acceptance. Independent expected results must come from the
agreed behavior/examples, not a copy of the exploratory implementation. Retain only reusable code or
permanent protection with demonstrated value; keep experimental artifacts out of product scope unless
requested. Preparatory behavior-preserving refactoring is allowed when the seam/testability/task needs
it; preserve existing guarantees. Cleanup after working behavior is proportional to touched risk,
while independent neighboring subsystem improvements remain separately scoped.
