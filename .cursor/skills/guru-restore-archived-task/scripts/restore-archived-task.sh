#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LAUNCHER="$SCRIPT_DIR/../../../runtime/launch.sh"
if [[ ! -f "$LAUNCHER" ]]; then
  LAUNCHER="$SCRIPT_DIR/../../../../runtime/launch.sh"
fi
if [[ ! -f "$LAUNCHER" ]]; then
  echo 'unsupported Skill package root for guru-restore-archived-task. Install the complete Guru Team runtime.' >&2
  exit 2
fi
source "$LAUNCHER" restore-archived-task "$@"
