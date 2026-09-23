# Remote publication

1. Confirm the operator authorized this write to this destination. Identify the exact `owner/repo`,
   destination ref, local source ref and SHA, remote ref and SHA, and push method. Check for unrelated
   local work and unexpected remote advancement. A PR request alone may not authorize push under
   project rules.
2. Prefer the configured remote and ordinary Git transport. State the target and method before
   writing. Do not silently switch to a direct URL, another account, an API object-write path, or a
   different repository. Follow [transport failures](transport-failures.md) if normal access fails.
3. If a non-fast-forward update is needed, stop for specific authorization. After authorization,
   use `--force-with-lease` against the expected remote SHA; never use plain `--force` as a retry.
4. After push, compare `git rev-parse <local-ref>` with
   `git ls-remote <destination> refs/heads/<branch>`. Confirm that the queried destination is the
   one just written. A successful push to a direct URL may leave `origin/<branch>` stale.
5. If the direct URL corresponds to the configured `origin`, fetch its branch through `origin`
   when available, then check `origin/<branch>` against the verified remote SHA. If fetch cannot
   complete, report the tracking ref as stale; do not represent `[⇡]` as proof the push failed.

When a push result is ambiguous, query the destination ref before retrying. If the remote SHA
already equals the intended local SHA, treat delivery as complete and reconcile tracking state.
