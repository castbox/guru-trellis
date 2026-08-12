#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/run-package-command.sh" "guru-create-task-commit" "scripts/check-task-commit-plan.sh" "$@"
