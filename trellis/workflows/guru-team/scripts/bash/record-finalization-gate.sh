#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/run-package-command.sh" "guru-finalize-task" "scripts/record-finalization-gate.sh" "$@"
