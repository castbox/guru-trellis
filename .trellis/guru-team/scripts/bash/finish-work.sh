#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -x "$SCRIPT_DIR/../../../../skills/guru-team/runtime/resolve-python.sh" ]]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
  RUNTIME_ASSETS="$REPO_ROOT/trellis/skills/guru-team/runtime"
  RUNTIME="$REPO_ROOT/trellis/skills/guru-team/packages/guru-finalize-task/runtime"
else
  REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
  RUNTIME_ASSETS="$REPO_ROOT/.trellis/guru-team/runtime"
  RUNTIME="$REPO_ROOT/.trellis/guru-team/skills/packages/guru-finalize-task/runtime"
fi
exec "$RUNTIME_ASSETS/resolve-python.sh" \
  "$REPO_ROOT" "$RUNTIME_ASSETS" \
  "$RUNTIME/legacy.py" finish-work "$@"
