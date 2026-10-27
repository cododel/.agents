# Task-needed worktree setup

Inspect project instructions and setup conventions before installing or copying anything. Prefer a
tracked setup script, then a suitable native facility, documented bootstrap, or the smallest manual
setup needed by the requested task. Read-only/offline work may need none.

Handle ignored files explicitly. Copy or generate only proven necessary files inside the worktree;
never broadly mirror the primary checkout, print secrets, or copy credentials into tracked files.
Share caches/dependency directories only when the project or harness convention establishes safe
concurrent use.

Install dependencies only when a task command needs them and they are absent or stale for the
resolved lockfile. Record setup failures without silently changing package managers or versions.
