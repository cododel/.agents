# Phase 3 — Skills audit (the SDD core)

Run **every** skill through four axes. With more than ~5 skills, dispatch the
per-skill checks to Explore subagents (one for reference-integrity/freshness,
one for content quality) and work with their conclusions.

## 3.1 Frontmatter and triggering

`description` is the only auto-trigger mechanism — the body is invisible until
Claude decides to load it based on the description.

- [ ] Description answers both: **what it does** — one clause, no more — +
      **when to apply** (concrete phrases, contexts, file types)
- [ ] Description carries **no workflow summary**: no steps, no gates, no
      hand-offs, no "read-only until approval". Measured upstream
      (obra/superpowers `writing-skills`): an agent follows a process stated in
      the description *instead of* opening the body — a skill described as
      "code review between tasks" ran one review where its flowchart specified
      two, and obeyed the flowchart only after the description was cut back to
      triggering conditions. The body is the process; the description is only
      the door. A tail like «investigation is strictly read-only; patches after
      approval; hands off to X» belongs in the body
- [ ] Description is pushy enough: skills systematically *under*-trigger, so
      enumerate trigger contexts explicitly, including when the user doesn't
      name the skill
- [ ] Trigger phrases in all working languages (рус/англ) if the team is bilingual
- [ ] **Anti-triggers** ("Do NOT use for...") wherever a skill borders another
      thematically
- [ ] Side-effect skills (deploy, publish, broadcast, migrations) →
      `disable-model-invocation: true`. *Deliberate deviation from the source
      methodology, which makes this unconditional:* a skill whose every mutation
      already passes an explicit in-body confirmation gate may stay
      auto-invocable, since auto-triggering it still mutates nothing without the
      operator. This is how the house skills work (adr-writer, docs-cleanup et
      al. mutate, gate, and stay invocable). Judge case by case — but treat a
      *prose* gate skeptically: if the protection is advisory the source rule
      stands, because advice is not a guarantee (routing-table: guarantee → hook)
- [ ] Directory name = invocation command, meaningful, no collisions

## 3.2 Structure and progressive disclosure

```
skill-name/
├── SKILL.md          # <500 lines; workflow + routing to references
├── references/       # loaded on demand; >300 lines → add a TOC
├── scripts/          # deterministic work as code, not prose
└── assets/           # templates the output refers to
```

- [ ] SKILL.md < 500 lines; approaching the limit → extract a layer to
      `references/` with explicit "when to read what" pointers
- [ ] Multi-domain skill organized by variants (`references/django.md`,
      `references/laravel.md`) — Claude reads only the relevant one
- [ ] Repeated mechanics packaged in `scripts/`, not described in prose (if
      session transcripts show Claude writing the same helper three times —
      bundle the script into the skill)
- [ ] Dynamic injection (`` !`git diff HEAD` ``) where the skill needs live
      state, instead of "first look at the diff" instructions

## 3.3 Content

- [ ] Imperative voice, **why** explained instead of caps-MUSTs. ALL-CAPS and
      rigid constructions are a yellow flag: usually means the author didn't
      explain motivation, and the model will look for loopholes
- [ ] Input → Output examples for non-trivial formats
- [ ] No overfit to the specific case the skill was written for — instructions
      generalized
- [ ] No content duplication between skills or with CLAUDE.md — shared contracts
      live in a shared reference both skills point to
- [ ] Tone/style rules (voice preservation, anti-escalation) formulated as
      principles with examples, not prohibitions

## 3.4 Freshness — the most common rot

- [ ] No references to dead tools or renamed commands (e.g. Codex mentions,
      `/fork` → `/branch`, retired model names, platforms no longer in use)
- [ ] Library/API versions in references are current (verify via Context7/docs,
      not memory)
- [ ] Every path inside the skill exists; every cross-reference between skills
      is alive
- [ ] Skills unused for N weeks → candidate for deletion or
      `disable-model-invocation: true` (free storage instead of permanent
      context rent)
- [ ] Versions of related skills are in sync (one contract edit → check all
      consumers)

## 3.5 Collision matrix

For every pair of thematically close skills ask: *"which request could fire
both?"* The answer must be either "none" (descriptions are disjoint) or
explicitly pinned by an anti-trigger in one of them. Trigger collisions are the
top cause of "Claude picked the wrong skill".

Check **both directions**: skill A deferring to B in its body doesn't help if
B's description still claims A's territory. The hand-off must be symmetric —
an anti-trigger in the description (where routing happens), not only a boundary
note in the body (read after routing already went wrong).

Include plugin skills in the matrix: a local skill can collide with a
marketplace skill of similar purpose (e.g. a local troubleshooter vs a plugin's
troubleshooting skill). `skillOverrides` in settings mutes a plugin skill
without editing its files.
