# Playbook: Next.js / TypeScript

Load only for a Next.js / React traceback. Where the framework manufactures bad state that
the component code doesn't show. Use with `discovery.md`.

## Reading the traceback

- Distinguish **server** from **client**: a stack in the terminal / function logs is SSR or a
  route handler; a stack in the browser console is client. The same component renders in both —
  the boundary is where assumptions diverge.
- `Hydration failed` / `Text content does not match server-rendered HTML` means the server and
  client rendered different trees — the bad state is a value that differs between the two
  environments (time, random, `window`, locale, `localStorage`), not a crash in one of them.
- `undefined is not a function` / `Cannot read properties of undefined` is the dominant
  shape — an optional prop, an unresolved `await`, or a value that only exists on one side.

## Where bad state is born (in likelihood order)

1. **Server/client boundary.** A Client Component reaching `window`/`document`/`localStorage`
   during SSR (undefined on the server); a Server Component passing a non-serializable prop
   (function, Date, class) to a Client Component; `'use client'` missing or misplaced.
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
5. **Env vars.** `process.env.X` is `undefined` on the client unless prefixed
   `NEXT_PUBLIC_`; a server-only secret read in a Client Component reads as undefined.
   `rg -n 'process\.env\.'`
6. **Module-load-time code.** Top-level code touching browser globals or env runs at import on
   the server and throws before any component renders.

## Masking mechanics to distrust

- `try { … } catch {}` in an async component or effect swallowing a rejected fetch.
- `as` casts and non-null assertions (`value!`) hiding a `null` the type system was told to
  ignore — the runtime didn't get the memo. `rg -n '\bas \w+|!\.'`
- `useEffect` running only on the client, papering over an SSR `undefined` so the bug only
  shows on first paint or in production SSR.

## A read-only repro is still a mutation

`next build`, `next dev`, and running the test suite spin up servers, hit APIs, and write the
`.next/` cache. Per the gate, propose the command for the user to run — don't start a server to
"just reproduce".
