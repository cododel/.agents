#!/usr/bin/env bash
# Re-copy official skills from redis/agent-skills into this folder.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
git clone -q --depth 1 https://github.com/redis/agent-skills "$tmp/src"
for d in "$here"/redis-*/; do
  name="$(basename "$d")"
  rm -rf "$d"; cp -rL "$tmp/src/skills/$name" "$here/$name"
done
cp "$tmp/src/LICENSE" "$here/LICENSE"
echo "redis/agent-skills $(git -C "$tmp/src" rev-parse HEAD)" > "$here/SOURCE"
