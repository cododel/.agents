# Playbook: Next.js

Load when dependencies and runtime/project structure prove Next.js on the causal path. Generic
JavaScript, TypeScript, or React projects use `discovery.md` without this Next.js playbook.

This is conditional diagnostic guidance, not a recommendation to select this framework. Project
contracts and installed-version evidence govern applicability. Candidate origins below are
non-exhaustive hypotheses; neither a framework name nor an error shape establishes a cause.

## Reading the traceback

- Distinguish **server** from **client**: terminal/function logs and browser-console traces are
  starting evidence, not proof of the originating execution context. Inspect the owning module
  and rendering boundary before assuming where it runs or whether it runs in both environments.
- For `Hydration failed` / `Text content does not match server-rendered HTML`, compare the actual
  server/client trees and inputs. Time, randomness, browser globals, locale and stored state are
  candidate differences to investigate, not an exhaustive explanation or an established cause.
- `undefined is not a function` / `Cannot read properties of undefined` may come from an
  optional prop, an unresolved `await`, or a value that only exists on one side; verify the actual path.

## Candidate origins to inspect

1. **Server/client boundary.** A Client Component reaching `window`/`document`/`localStorage`
   during SSR (undefined on the server); a Server Component passing an unsupported value
   such as an ordinary function or custom class instance to a Client Component;
   `'use client'` missing or misplaced. React RSC serialization supports `Date` and Server Functions;
   do not apply JSON-only restrictions to that boundary.
   `rg -n "'use client'|window\.|document\.|localStorage|typeof window"`
2. **Data fetching & caching.** `fetch` returning cached/stale data (`cache`/`next.revalidate`
   options); a `route handler` returning the wrong shape; `async` Server Component whose
   `await` rejected and got swallowed; `params`/`searchParams` awaited or shaped wrong in the
   App Router. `rg -n 'fetch\(|revalidate|generateStaticParams|route\.(ts|js)'`
3. **Hydration mismatch sources.** `Date.now()`, `Math.random()`, `new Date()`, locale/tz
   formatting, or `id` generated during render — different on server vs client.
   `rg -n 'Date\.now|Math\.random|new Date|toLocaleString|crypto\.randomUUID'`
4. **Props & optional chaining gaps.** A prop typed optional but read as required; an API
   response typed as `T` but actually `T | null`; `?.` that defers the crash to the next
   non-optional access. Check the type vs. the runtime shape at the boundary.
5. **Env vars.** Variables supplied through the environment or `.env` are not exposed to
   client code by default without `NEXT_PUBLIC_`. Check how the value is supplied: entries
   in `next.config.js` `env` are bundled even without that prefix. Inspect actual build/config
   behavior before attributing an undefined value or assuming a secret cannot reach the client.
   `rg -n 'process\.env\.'`
6. **Module-load-time code.** Top-level code touching browser globals or env runs at import on
   the server and throws before any component renders.

## Masking mechanics to distrust

Inspect the actual path before treating any of these patterns as causal masking:

- `try { … } catch {}` in an async component or effect swallowing a rejected fetch.
- `as` casts and non-null assertions (`value!`) hiding a `null` the type system was told to
  ignore — the runtime didn't get the memo. `rg -n '\bas \w+|!\.'`
- `useEffect` running only on the client, papering over an SSR `undefined` so the bug only
  shows on first paint or in production SSR.

## Local development reproduction

Run `next build`, focused tests, or `next dev` in a verified local development copy under the
[common authority rules](../../SKILL.md#authority-and-local-reproduction). Writing `.next/` is an ordinary local
side effect; resolve server-side API targets before reproduction and stop task-owned development
servers before handoff.

Serialization semantics: [React RSC serializable props](https://react.dev/reference/rsc/use-client#serializable-types-returned-by-server-components).
Resolve the installed React/Next.js versions before applying version-sensitive advice.
