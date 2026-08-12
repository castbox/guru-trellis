#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/runtime/utility.py" ]]; then
  RUNTIME="$SCRIPT_DIR/../../../../skills/guru-team/runtime"
else
  RUNTIME="$SCRIPT_DIR/../../runtime"
fi
python3 "$RUNTIME/utility.py" prepare "$@"
