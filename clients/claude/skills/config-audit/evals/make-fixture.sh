#!/usr/bin/env bash
# Materialize the config-audit functional-eval fixture: a fake project .claude/
# with 12 planted configuration defects (see answer-key.md). Written to a temp
# dir, NOT under ~/.claude/skills (real SKILL.md files there would pollute the
# skill namespace and inventory.sh). Prints the fixture path on stdout.
#
# Usage: make-fixture.sh [target-dir]   (default: a fresh mktemp dir)
set -euo pipefail

DEST="${1:-$(mktemp -d "${TMPDIR:-/tmp}/config-audit-fixture.XXXXXX")}/proj"
mkdir -p "$DEST/.claude/commands" \
         "$DEST/.claude/skills/api-docs" \
         "$DEST/.claude/skills/docs-helper" \
         "$DEST/src"

cat > "$DEST/package.json" <<'EOF'
{ "name": "shop-api", "scripts": { "test": "vitest run" } }
EOF

# k1 dead command (lint:all absent from package.json); k2 always-rule that should
# be a hook; k3 inline 15-step procedure (workflow → skill); k4 broken @import;
# k5 facts derivable from code.
cat > "$DEST/.claude/CLAUDE.md" <<'EOF'
# shop-api conventions

We use TypeScript. Source files live in src/.

Run `npm run lint:all` before committing.

ALWAYS run prettier on every file you edit. NEVER skip formatting.

@docs/conventions.md

## Release procedure
1. Bump version in package.json
2. Run npm run test
3. Update CHANGELOG.md
4. Tag the release vX.Y.Z
5. Push the tag
6. Wait for CI
7. Run the smoke suite against staging
8. Announce in #releases
9. Merge back into develop
10. Close the milestone
11. Create next milestone
12. Update the roadmap doc
13. Notify support team
14. Verify sentry release created
15. Done
EOF

# k6 legacy command (should migrate to a skill)
cat > "$DEST/.claude/commands/deploy.md" <<'EOF'
Deploy the app: run ./scripts/deploy.sh $ARGUMENTS and report the URL.
EOF

# k7 description lacks triggering conditions
cat > "$DEST/.claude/skills/api-docs/SKILL.md" <<'EOF'
---
name: api-docs
description: Helps with API documentation.
---
# API Docs
Write OpenAPI specs for endpoints. Document request/response shapes.
EOF

# k8 trigger collision with api-docs (no anti-trigger); k9 dead path; k10 stale command
cat > "$DEST/.claude/skills/docs-helper/SKILL.md" <<'EOF'
---
name: docs-helper
description: Use when the user asks to document APIs, write docs, or clean up documentation.
---
# Docs Helper
For API documentation requests, generate markdown docs.
If the session gets messy, /fork the session and continue there.
Detailed style rules are in references/missing.md — read them first.
EOF

# k11 overly broad permission
cat > "$DEST/.claude/settings.json" <<'EOF'
{ "permissions": { "allow": ["Bash(*)"] } }
EOF

# k12 unused MCP server (context tax)
cat > "$DEST/.mcp.json" <<'EOF'
{ "mcpServers": { "weather": { "command": "npx", "args": ["weather-mcp"] } } }
EOF

cat > "$DEST/src/index.ts" <<'EOF'
export const ping = () => "pong";
EOF

echo "$DEST"
