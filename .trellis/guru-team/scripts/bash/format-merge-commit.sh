#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-merge-task-pr/runtime/legacy.py" ]]; then
  RUNTIME="$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-merge-task-pr/runtime"
else
  RUNTIME="$SCRIPT_DIR/../../skills/packages/guru-merge-task-pr/runtime"
fi
PYTHONPATH="$RUNTIME${PYTHONPATH:+:$PYTHONPATH}" python3 "$RUNTIME/legacy.py" "$@"
