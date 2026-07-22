# Phase 2 — CLAUDE.md audit

Target size: **up to ~200 lines**, less is better. Anthropic's own position: a
bloated CLAUDE.md makes Claude ignore your actual instructions.

Per-line test: *"If I remove this line, will Claude start making mistakes?"*
No → delete.

## Checklist

- [ ] **Nothing Claude derives from the code itself** — file structure, standard
      language conventions, "write clean code"
- [ ] **No procedures** — step-by-step workflows are extracted to skills
- [ ] **No dead commands** — every bash command in CLAUDE.md actually works:
      verify against `package.json` / `Makefile` / `pyproject.toml`
- [ ] **No rules that should be hooks** — anything phrased "always", "never",
      "must" is a hook candidate (advice → CLAUDE.md, guarantee → hook)
- [ ] **Imports are alive** — every `@path/to/file` points to an existing file;
      bare prose references to other files resolve too (qualify them with a path)
- [ ] **Hierarchy is meaningful** — monorepo: root CLAUDE.md = shared,
      `apps/<x>/CLAUDE.md` = module specifics; no duplication across levels
- [ ] **Behavioral check**: if Claude asks questions CLAUDE.md already answers —
      the wording is ambiguous; if it ignores a rule — the file is too long and
      the rule drowns

## Layered enforcement vs duplication

*Extends the source methodology, which frames an always/never rule purely as
something to convert into a hook.* The convert-it default still holds — but one
narrow case justifies keeping prose alongside the hook: when the prose carries
the **why** the deterministic gate cannot express (the rationale an agent needs
to apply judgment in the grey zone the hook doesn't cover). A bare "never X"
duplicated as both prose and a `permissions.ask`/hook entry is *not* that case —
delete the prose, the hook is the guarantee. The same instruction appearing in
CLAUDE.md *and* a rules file *and* a skill description is always triple-paid
context — collapse to one home per the routing table.

Treat CLAUDE.md as code: review on incidents, prune regularly, verify changes by
observing whether behavior actually changed.
