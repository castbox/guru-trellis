#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-finalize-task/runtime/legacy.py" ]]; then
  RUNTIME="$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-finalize-task/runtime"
  GURU_ROOT="$SCRIPT_DIR/../../../../skills/guru-team"
else
  RUNTIME="$SCRIPT_DIR/../../skills/packages/guru-finalize-task/runtime"
  GURU_ROOT="$SCRIPT_DIR/../.."
fi
PYTHONPATH="$RUNTIME:$GURU_ROOT${PYTHONPATH:+:$PYTHONPATH}" python3 "$RUNTIME/legacy.py" check-workspace-boundary "$@"
