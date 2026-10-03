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
4. After push, query `git ls-remote <destination> <exact-destination-ref>` and compare the result
   for that exact ref with the intended source SHA. Verify the local source ref's current SHA too;
   if it moved, distinguish that new state from the SHA just published. Confirm the queried
   repository is the one written. Do not substitute `refs/heads/<branch>` when the write targeted
   a tag or another ref namespace. A direct-URL push may leave a local remote-tracking ref stale.
5. For a branch destination only, if the direct URL corresponds to the configured `origin`, fetch
   that branch through `origin` when available, then compare `origin/<branch>` with the verified
   destination SHA. If fetch cannot complete, report the tracking ref as stale; `[⇡]` does not prove
   the push failed. Tags and other destination refs do not imply branch upstream configuration.

When a push result is ambiguous, query the exact destination ref before retrying. If its remote SHA
already equals the intended local SHA, treat delivery as complete and reconcile tracking state.
