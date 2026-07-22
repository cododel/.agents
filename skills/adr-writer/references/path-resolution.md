# Path resolution: choosing the save path

This file picks the *target path* for a new ADR after `discovery.md` has confirmed which
`adr/` directories exist (or that none do).

## Decision matrix

| Scope            | When it applies                                                                                  | Path pattern                                                  |
|------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| **Global**       | Affects whole system, infra, DB, cross-cutting concerns (logging, middleware, auth, errors, i18n) | `docs/adr/<filename>.md`                                      |
| **Module-local** | Isolated to one existing app, package, or service                                                | `<module-path>/docs/adr/<filename>.md`                        |
| **Infra/DevOps** | Deployment, cron jobs, CI/CD, environment config, secrets management                             | `notes/adr-infra/<filename>.md` or repo-specific infra path   |

If the local repo's `docs/adr/README.md` defines a different layout (e.g. all ADRs under
`docs/decisions/<area>/`), that layout wins. Discovery should have surfaced this.

## Rules

- `<filename>` follows the local convention from `docs/adr/README.md` if present.
  Otherwise use the fallback: `ADR-YYYYMMDD-<slug>.md` (or
  `[STATUS-PERCENT%]-ADR-YYYYMMDD-<slug>.md` if the local repo uses percent-status —
  see `assets/adr-template.md`).
- `YYYYMMDD` = today's date.
- `<slug>` = short kebab-case title, English, 3-7 words, describes the *decision*
  (e.g. `payment-webhook-retry`, `bun-as-package-manager`, not just `payments`).
- **Do NOT invent parent folders that don't exist** in the project. If the user wants a
  module-local ADR but `<module>/docs/` doesn't exist, ask whether to create it or fall
  back to a global ADR.
- If scope is genuinely ambiguous after honest analysis, **default to global**
  (`docs/adr/`). It's more discoverable and easier to move down later than the reverse.

## Monorepo nuance

In a monorepo with multiple `docs/adr/` directories (root + per-app), the question
"which one?" is the same as the issue-writer scope question:

- Decision touches only one app/package → `<scope>/docs/adr/`
- Decision is shared, infra, or cross-cutting → root `docs/adr/`
- User explicitly named a scope → honor it

When in doubt, ask. ADR misplacement is especially costly because ADRs are meant to be
discoverable by future engineers reading just one app's tree.

## Bootstrap

If the chosen path's `adr/` directory doesn't exist:

- **from-chat mode**: create it as part of writing the ADR. Creating the directory is
  implied by the user's "create ADR" request; also install `assets/adr-readme.md` as the local
  `README.md` convention.
- **from-issue mode**: ask first. Bootstrapping a new doc location during a batch
  promote is a separate decision the user should sign off on. Once approved, create both the
  directory and its fallback README.
