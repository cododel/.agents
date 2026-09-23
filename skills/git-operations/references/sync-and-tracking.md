# Synchronization and tracking

Keep these distinct:

- Local branch: `refs/heads/<branch>`.
- Remote branch: `refs/heads/<branch>` queried from the destination with `git ls-remote`.
- Remote-tracking ref: local cache such as `refs/remotes/origin/<branch>`.

Before fetch or pull, inspect branch, upstream, status, and the remote being used. Fetch updates
remote-tracking refs; pull also integrates changes into the checked-out branch and may need separate
authorization under project rules. Do not pull merely to remove a stale ahead marker.

After a direct-URL push, verify the destination branch SHA first. If that URL names the configured
`origin` repository, run `git fetch origin` when available and compare `origin/<branch>` with the
verified destination SHA and local SHA. If the comparison fails or fetch is unavailable, report the
three states separately. An ahead marker calculated from stale `origin/<branch>` is not evidence of
a failed push.

For a divergent branch, inspect the actual local and remote commits before deciding whether to
integrate, create a new branch, or request a history rewrite. Never infer the intended resolution
from the ahead/behind count alone.
