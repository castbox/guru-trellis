#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-approve-task-plan/scripts/resolve-human-artifacts.sh" ]]; then
  TARGET="$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-approve-task-plan/scripts/resolve-human-artifacts.sh"
else
  TARGET="$SCRIPT_DIR/../../skills/packages/guru-approve-task-plan/scripts/resolve-human-artifacts.sh"
fi
exec "$TARGET" "$@"
