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
python3 - "$REPO_ROOT" "$TASK_PATH" <<'PY'
import json
import sys
from pathlib import Path

repo_root = Path(sys.argv[1]).resolve()
task_input = Path(sys.argv[2])
task_dir = task_input if task_input.is_absolute() else repo_root / task_input
task_file = task_dir.resolve() / "task.json"

try:
    task = json.loads(task_file.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    print(f"Error: cannot read task identity from {task_file}: {exc}", file=sys.stderr)
    raise SystemExit(1)

recorded_worktree = task.get("worktree_path") if isinstance(task, dict) else None
if not isinstance(recorded_worktree, str) or not recorded_worktree.strip():
    print("Error: task.json worktree_path is required before starting a task", file=sys.stderr)
    raise SystemExit(1)

if Path(recorded_worktree).expanduser().resolve() != repo_root:
    print("Error: task.json worktree_path does not match the current checkout", file=sys.stderr)
    print(f"Expected: {repo_root}", file=sys.stderr)
    print(f"Recorded: {recorded_worktree}", file=sys.stderr)
    raise SystemExit(1)
PY
exec python3 "$REPO_ROOT/.trellis/scripts/task.py" start "$@"
