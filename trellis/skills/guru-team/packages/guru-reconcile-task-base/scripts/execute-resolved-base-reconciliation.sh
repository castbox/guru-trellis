#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
LAUNCHER="$SCRIPT_DIR/../../../../runtime/launch.sh"
[[ -f "$LAUNCHER" ]] || { echo "guru-reconcile-task-base is not self-contained or portable; install the complete Guru Team preset" >&2; exit 2; }
source "$LAUNCHER" execute-resolved-base-reconciliation "$@"
