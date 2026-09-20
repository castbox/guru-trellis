#!/usr/bin/env bash
set -euo pipefail
PACKAGE_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../runtime/launch.sh"
[[ -f "$LAUNCHER" ]] || LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../../runtime/launch.sh"
[[ -f "$LAUNCHER" ]] || LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../../.trellis/guru-team/runtime/launch.sh"
[[ -f "$LAUNCHER" ]] || { echo 'Guru Team Skill packages are not self-contained or portable. Install or upgrade the complete Guru Team preset.' >&2; exit 2; }
source "$LAUNCHER" invoke-guru-reconcile-task-base "$@"
