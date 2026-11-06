#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/runtime/delivery_projection/candidate_cli.py" ]]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
  GURU_ROOT="$REPO_ROOT/trellis/skills/guru-team"
else
  REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
  GURU_ROOT="$REPO_ROOT/.trellis/guru-team"
fi
RUNTIME_ASSETS="$GURU_ROOT/runtime"
if [[ ! -x "$RUNTIME_ASSETS/resolve-python.sh" ]]; then
  echo '{"code":"runtime_dependency_missing","field_path":"runtime","remediation":"Restore the complete matching Guru installation through the original installer/tools owner."}' >&2
  exit 2
fi
export PYTHONPATH="$GURU_ROOT"
export PYTHONDONTWRITEBYTECODE=1
exec "$RUNTIME_ASSETS/resolve-python.sh" "$REPO_ROOT" "$RUNTIME_ASSETS" \
  -m runtime.delivery_projection.candidate_cli "$@"
