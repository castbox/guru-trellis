#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/runtime/lifecycle_helpers.py" ]]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
  RUNTIME_ASSETS="$REPO_ROOT/trellis/skills/guru-team/runtime"
  RUNTIME="$SCRIPT_DIR/../../../../skills/guru-team/runtime"
  GURU_ROOT="$SCRIPT_DIR/../../../../skills/guru-team"
else
  REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
  RUNTIME_ASSETS="$REPO_ROOT/.trellis/guru-team/runtime"
  RUNTIME="$SCRIPT_DIR/../../runtime"
  GURU_ROOT="$SCRIPT_DIR/../.."
fi
if [[ ! -x "$RUNTIME_ASSETS/resolve-python.sh" ]]; then
  echo "Error: Guru Team managed Python runtime is unavailable" >&2
  exit 2
fi
export PYTHONPATH="$RUNTIME:$GURU_ROOT${PYTHONPATH:+:$PYTHONPATH}"
exec "$RUNTIME_ASSETS/resolve-python.sh" \
  "$REPO_ROOT" "$RUNTIME_ASSETS" \
  "$RUNTIME/lifecycle_helpers.py" check-agent-recovery "$@"
