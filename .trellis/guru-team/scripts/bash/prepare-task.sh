#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-create-task-workspace/runtime/prepare.py" ]]; then
  PREPARE="$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-create-task-workspace/runtime/prepare.py"
else
  PREPARE="$SCRIPT_DIR/../../skills/packages/guru-create-task-workspace/runtime/prepare.py"
fi
python3 "$PREPARE" "$@"
