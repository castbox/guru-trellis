#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -x "$SCRIPT_DIR/../../../../skills/guru-team/runtime/resolve-python.sh" ]]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
  RUNTIME_ASSETS="$REPO_ROOT/trellis/skills/guru-team/runtime"
  PREPARE="$REPO_ROOT/trellis/skills/guru-team/packages/guru-create-task-workspace/runtime/prepare.py"
else
  REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
  RUNTIME_ASSETS="$REPO_ROOT/.trellis/guru-team/runtime"
  PREPARE="$REPO_ROOT/.trellis/guru-team/skills/packages/guru-create-task-workspace/runtime/prepare.py"
fi
exec "$RUNTIME_ASSETS/resolve-python.sh" \
  "$REPO_ROOT" "$RUNTIME_ASSETS" \
  "$PREPARE" "$@"
