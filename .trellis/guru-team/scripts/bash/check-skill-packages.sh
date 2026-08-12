#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAYOUT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
if [[ -d "$LAYOUT_ROOT/skills/guru-team/runtime" ]]; then
  RUNTIME_ROOT="$LAYOUT_ROOT/skills/guru-team"
elif [[ -d "$LAYOUT_ROOT/.trellis/guru-team/runtime" ]]; then
  RUNTIME_ROOT="$LAYOUT_ROOT/.trellis/guru-team"
else
  echo "Guru Team package-local validator runtime is missing." >&2
  exit 2
fi
export PYTHONPATH="$RUNTIME_ROOT${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m runtime.validate "$@"
