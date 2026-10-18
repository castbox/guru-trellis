#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; LAUNCHER="$SCRIPT_DIR/../../../runtime/launch.sh"; [[ -f "$LAUNCHER" ]] || LAUNCHER="$SCRIPT_DIR/../../../../runtime/launch.sh"; [[ -f "$LAUNCHER" ]] || LAUNCHER="$SCRIPT_DIR/../../../../.trellis/guru-team/runtime/launch.sh"; [[ -f "$LAUNCHER" ]] || { echo 'Guru Team Skill packages are not self-contained or portable.' >&2; exit 2; }; source "$LAUNCHER" invoke-guru-bind-task-session "$@"
