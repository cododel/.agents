---
name: troubleshooter
description: "Auto-diagnose concrete tracebacks, crashes, logs, failing commands, and runtime failures; fix when requested. Verify the cause and preserve a focused regression test when useful. Not for generic architecture review."
---

# Troubleshooter

Prove the violated assumption and its path to the observed failure. The throwing application frame
anchors a symptom; it does not establish which producer or ownership boundary caused it.

## Authority and local reproduction

Explain/diagnose/debug requests permit investigation, not tracked product edits. An explicit fix
request permits evidence-backed local repairs and proportionate verification. Stop for a material
product, architecture, contract, migration, or irreversible-cost fork. Unrelated cleanup,
push/deploy, destructive actions, and shared/persistent mutations remain gated.

Builds, focused tests, and development servers are permitted in a verified local development copy.
First resolve actual database, cache, queue, API, and delivery targets; a local path proves no service
is local. Data-changing checks require isolated disposable targets. Task-local generated files and
caches are ordinary side effects; stop task-owned processes before handoff. An unresolved service
blocks only its dependent command, while independent investigation continues.

## Focused workflow

Use [testing-evidence](../testing-evidence/SKILL.md) for regression design, meaningful RED and check
interpretation; the project profile supplies execution commands. Diagnosis owns the causal chain.

1. Extract error/message, command/environment, relevant application frame, and the unexpected state.
   Resolve missing evidence from supplied artifacts, source, logs, or safe probes before asking.
2. Choose the distinguishing test/probe by the uncertainty it removes. For fixes, prefer a useful regression at the
   behavior boundary and run it before patching; confirm the failure is the bug rather than setup
   noise. Reuse an existing failure. Diagnosis-only, brittle, or disproportionate seams may use
   disposable scratch probes with their limits stated.
3. Trace concrete producer, transformation, boundary, consumer, and lifecycle edges in source.
   Connect origin → control/data path → violated assumption → distinguishing probe. Label uncertain
   links as hypotheses; do not patch a guess merely to make the symptom disappear.
4. When authorized, fix the origin or ownership boundary. Improve directly touched code only when
   it reduces the same failure risk without widening scope. Make the focused probe pass and inspect
   relevant static/type checks, failure paths, validation, typing, security, and resource cleanup.
   Retain a useful regression, or explain why a durable test was unsuitable.

## Load only relevant detail

Read [references/discovery.md](references/discovery.md) when the origin is unclear or upstream,
cross-module, event, or lifecycle tracing needs more guidance. Load framework playbooks only when
repository dependencies and runtime/project structure prove that framework on the causal path:

- Django/DRF: [references/playbooks/django.md](references/playbooks/django.md).
- Next.js: [references/playbooks/nextjs.md](references/playbooks/nextjs.md).
- Laravel: [references/playbooks/laravel.md](references/playbooks/laravel.md).

Generic language projects use discovery without a framework playbook. A proven cross-stack path may
need several; use `$find-docs` only for unverified version-sensitive external semantics.

## Handoff

Report cause versus hypotheses, the semantic fix when authorized, decisive before/after evidence,
and material gaps. Diagnosis-only reports must omit implementation claims and identify the next
falsifying observation when uncertain. Briefly report independent debt; record it through
`$issue-writer` only on a request to record/defer it.
