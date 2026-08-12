#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-select-workflow-mode/scripts/check-env.sh" ]]; then
  TARGET="$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-select-workflow-mode/scripts/check-env.sh"
else
  TARGET="$SCRIPT_DIR/../../skills/packages/guru-select-workflow-mode/scripts/check-env.sh"
fi
exec "$TARGET" "$@"
