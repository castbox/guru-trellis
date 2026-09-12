#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ $# -lt 1 || "$1" == -* ]]; then
  echo "usage: start-task.sh <task-path> [task.py start options...]" >&2
  exit 2
fi

REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
TASK_PATH="$1"

# The official task.py remains upstream-owned. Guru's wrapper owns the
# workspace identity gate for the supported activation path.
"$SCRIPT_DIR/check-workspace-boundary.sh" --json --task "$TASK_PATH" >/dev/null
exec python3 "$REPO_ROOT/.trellis/scripts/task.py" start "$@"
