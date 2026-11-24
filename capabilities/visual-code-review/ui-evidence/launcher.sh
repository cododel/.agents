#!/bin/sh
ui_evidence_dir=$(dirname "$0")
export PLAYWRIGHT_BROWSERS_PATH="$ui_evidence_dir/browsers"
exec "$ui_evidence_dir/node_modules/.bin/ui-evidence" "$@"
