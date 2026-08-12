#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/runtime/discovery.py" ]]; then
  RUNTIME_PARENT="$(cd "$SCRIPT_DIR/../../../../skills/guru-team" && pwd)"
elif [[ -f "$SCRIPT_DIR/../../runtime/discovery.py" ]]; then
  RUNTIME_PARENT="$(cd "$SCRIPT_DIR/../.." && pwd)"
else
  echo "Guru Team shared runtime is missing: runtime/discovery.py" >&2
  exit 2
fi
export PYTHONPATH="$RUNTIME_PARENT${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m runtime.discovery "$@"
