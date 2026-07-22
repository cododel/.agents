# Discovery: tracing bad state from the failing line to its origin

## Goal

Get from the frame that crashed to the code that *created* the bad state, proven from the
repo — not guessed from a plausible-looking call site. The failing line may contain the defect,
but it is often where an upstream wrong assumption finally becomes visible. Discovery checks
the expression itself, then walks back to the source of its inputs.

This file is the language-agnostic "how". Framework-specific hiding spots live in
`playbooks/<stack>.md` and load only when that stack applies.

## Step D1 — Anchor on the failing frame

From the traceback, pin down four things before searching anything:

- The **exact symbol** that blew up (the variable that was `None`/`undefined`, the key that
  was missing, the type that was wrong, the index out of range).
- The **deepest relevant application frame** — skip vendored/framework frames and use this as
  the investigation starting point, not proof that this frame owns the defect.
- The **shape the code expected** vs. the shape it got. Name both. "Expected a non-empty
  list of `User`, got `None`" is the whole investigation in one line.
- Whether the failure is **deterministic or conditional** (always vs. only some inputs) — it
  tells you whether to look at construction (always) or a specific branch/edge (conditional).

If any of these can't be pinned from the artifact + repo files, **stop and ask** for the
missing traceback / log / path. A similar frame name is not proof.

## Step D2 — Search upstream for where the bad state is born

Don't read top-down from `main`. Search for the symbol's **origin** and **mutation points**,
then read only those.

Orientation greps (adapt the symbol; `rg` respects `.gitignore`):

```bash
# Where is the failing symbol assigned, constructed, or defaulted?
rg -n '\b<symbol>\s*[:=]' --type <lang>
rg -n '(def|fn|func|function)\s+<producer>' --type <lang>   # the function that returns it

# Who calls the failing function — what do they pass in?
rg -n '\b<failing_fn>\s*\(' --type <lang>

# Where does the value cross a boundary (the usual birthplace of bad state)?
rg -n 'json|loads|parse|deserialize|\.get\(|getenv|request\.|os\.environ' --type <lang>
```

The four usual birthplaces of bad state, in rough order of likelihood:

1. **A boundary**: deserialization, API/DB read, env var, file parse, user input — where an
   assumed shape was never actually guaranteed.
2. **A default or optional**: a `None`/`null`/`undefined`/zero-value that a happy-path test
   never exercised.
3. **A branch that skips initialization**: an early return, an `except`/`catch` that swallows,
   a conditional that leaves a field unset.
4. **A mutation after construction**: the value was fine when built, then something cleared or
   overwrote it.

Read the producer and the boundary first; that's where 80% of these resolve.

## Step D3 — Scope the search; don't read the whole repo

- Start in the **package/module of the failing frame**, then widen only along the data path
  you've actually traced — not breadth-first across the project.
- Use `git log -L`, `git blame`, or `git log -S '<symbol>'` to find *when* the assumption was
  introduced; a recent change near the failing line is a strong lead.
- Respect the investigation budget in `SKILL.md`: ~3 widening rounds / ~10–15 reads, then
  either land the root cause or surface the narrowed hypothesis and ask. Counting matters —
  it's the difference between diagnosis and a repo crawl.

## Step D4 — Load the stack playbook only if it applies

If the failure runs through framework machinery (request lifecycle, ORM, DI, serializers,
SSR/hydration, middleware), the bad state may be *manufactured by the framework*, not by
obvious project code. Detect the stack from the repo, then read the matching playbook:

| Repo tell                                                       | Playbook                       |
|----------------------------------------------------------------|--------------------------------|
| `manage.py` plus Django settings, or a manifest dependency on Django | `playbooks/django.md`      |
| `package.json` dependency on `next` plus `next.config.*`, `app/`, or `pages/` | `playbooks/nextjs.md` |
| `composer.json` dependency on `laravel/framework` plus `artisan` or `app/Http/` | `playbooks/laravel.md` |

Load **only** a playbook confirmed by framework-specific evidence. Generic Python, PHP, or
JavaScript projects use this discovery guide without a framework playbook.

## Step D5 — Confirm, don't assume

Before writing the root cause: can you point to the *specific line* that produced the bad
state and the *specific line* that consumed it on a wrong assumption? If there's a gap you're
filling with "probably", it's not proven yet — close the gap with one more targeted read, or
state it as a hypothesis in the report and say what would confirm it. Never present a guess as
a diagnosis.
