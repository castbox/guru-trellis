#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$SCRIPT_DIR/../../../runtime/launch.sh"
[[ -f "$LAUNCHER" ]] || LAUNCHER="$SCRIPT_DIR/../../../../runtime/launch.sh"
source "$LAUNCHER" check-workflow-environment "$@"
