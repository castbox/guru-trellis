#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$SCRIPT_DIR/../../../runtime/launch.sh"
[[ -f "$LAUNCHER" ]] || LAUNCHER="$SCRIPT_DIR/../../../../runtime/launch.sh"
[[ -f "$LAUNCHER" ]] || { echo "Load the complete Guru Team source." >&2; exit 2; }
source "$LAUNCHER" legacy-maintenance-guru-finish-task "$@"
