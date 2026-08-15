# Repository documentation discovery

Use this reference when a living contract, Issue, ADR, brief, or broad documentation audit must
locate repository-local records. The goal is a proven scope, not a conventional-looking guess.

## 1. Establish the repository boundary

Resolve the repository root and read applicable instruction and documentation indexes first,
including `AGENTS.md`, `CLAUDE.md`, `README.md`, and `docs/README.md` when present. Explicit local
conventions override fallback names and layouts.

## 2. Discover candidate roots once

From the confirmed repository root, use `fd` or `rg --files` to identify directories or files named
or documented as contracts/specs, current architecture, Issues, ADRs/decisions, briefs,
runbooks/playbooks, incidents/postmortems, or notes.
Exclude `.git`, dependency, virtual-environment, build, cache, generated, and existing archive
trees. Do not search a parent repository or sibling checkout unless the operator included it.

Classify each hit by evidence:

- instruction or index explicitly declares its purpose;
- local README/template and representative files establish a convention;
- project documentation explicitly declares an executable schema/type surface canonical for a
  bounded interface;
- the operator supplied the exact root;
- otherwise it remains an unconfirmed candidate.

Do not create or relocate a documentation root merely because a common path is absent.

## 3. Resolve scope

- One confirmed root for the requested kind: use it.
- Several roots in a monorepo: select the named module when unambiguous; otherwise show the paths
  and ask which are in scope before reading bodies or writing files.
- Broad audit: report every confirmed root and surprising unconfirmed candidate before expensive
  classification.
- No confirmed root: follow the owning skill's bootstrap rule, if any; otherwise ask.

For each selected root, read its `README.md`, `CONTRIBUTING.md`, template, or index and sample the
minimum representative files needed to verify filename, status, placement, and language rules.

## 4. Preserve the evidence

In the result, state how the root and scope were proven. If exact targets remain ambiguous, stop
the affected branch. A similar name, a plan, or a prior conversation is not target evidence.
