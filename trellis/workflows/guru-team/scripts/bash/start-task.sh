#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  echo "usage: start-task.sh --mode initial|recovery <task-path> [task.py start options...]" >&2
}

if [[ $# -lt 3 || "$1" != "--mode" ]]; then
  usage
  exit 2
fi

MODE="$2"
shift 2
case "$MODE" in
  initial|recovery) ;;
  *)
    usage
    exit 2
    ;;
esac

if [[ $# -lt 1 || "$1" == -* ]]; then
  usage
  exit 2
fi

TASK_PATH="$1"
shift
if [[ "$MODE" == "recovery" && $# -ne 0 ]]; then
  echo "Error: recovery accepts no task.py start options" >&2
  exit 2
fi

REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
TASK_PY="$REPO_ROOT/.trellis/scripts/task.py"

"$SCRIPT_DIR/check-workspace-boundary.sh" --json --task "$TASK_PATH" >/dev/null

IDENTITY_JSON="$(python3 - "$REPO_ROOT" "$TASK_PATH" "$MODE" <<'PY'
import json
import subprocess
import sys
from pathlib import Path

repo_root = Path(sys.argv[1]).resolve()
task_input = Path(sys.argv[2])
mode = sys.argv[3]
task_dir = (task_input if task_input.is_absolute() else repo_root / task_input).resolve()
tasks_root = (repo_root / ".trellis/tasks").resolve()

try:
    task_dir.relative_to(tasks_root)
except ValueError:
    print("Error: task path must resolve below .trellis/tasks", file=sys.stderr)
    raise SystemExit(1)

task_file = task_dir / "task.json"
try:
    task = json.loads(task_file.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    print(f"Error: cannot read task identity from {task_file}: {exc}", file=sys.stderr)
    raise SystemExit(1)
if not isinstance(task, dict):
    print(f"Error: task identity must be a JSON object: {task_file}", file=sys.stderr)
    raise SystemExit(1)

task_id = task.get("id") or task.get("name")
recorded_worktree = task.get("worktree_path")
recorded_branch = task.get("branch")
status = task.get("status")
expected_status = "planning" if mode == "initial" else "in_progress"
if not isinstance(task_id, str) or not task_id.strip():
    print("Error: task.json id or name is required before task activation", file=sys.stderr)
    raise SystemExit(1)
if not isinstance(recorded_worktree, str) or not recorded_worktree.strip():
    print("Error: task.json worktree_path is required before task activation", file=sys.stderr)
    raise SystemExit(1)
if Path(recorded_worktree).expanduser().resolve() != repo_root:
    print("Error: task.json worktree_path does not match the current checkout", file=sys.stderr)
    print(f"Expected: {repo_root}", file=sys.stderr)
    print(f"Recorded: {recorded_worktree}", file=sys.stderr)
    raise SystemExit(1)
branch = subprocess.run(
    ["git", "branch", "--show-current"],
    cwd=repo_root,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=True,
).stdout.strip()
if not branch or not isinstance(recorded_branch, str) or recorded_branch != branch:
    print("Error: task.json branch does not match the current checkout", file=sys.stderr)
    print(f"Expected: {branch or '(detached)'}", file=sys.stderr)
    print(f"Recorded: {recorded_branch}", file=sys.stderr)
    raise SystemExit(1)
if status != expected_status:
    print(
        f"Error: --mode {mode} requires task status {expected_status}; found {status!r}",
        file=sys.stderr,
    )
    raise SystemExit(1)

print(json.dumps({
    "task_id": task_id,
    "task_ref": task_dir.relative_to(repo_root).as_posix(),
    "task_dir": str(task_dir),
    "workspace_root": str(repo_root),
    "branch": branch,
    "status": status,
}, ensure_ascii=False, sort_keys=True))
PY
)"

verify_current_identity() {
  local expected_status="$1"
  local current_json
  if ! current_json="$(python3 "$TASK_PY" current --json)"; then
    printf '%s\n' "$current_json" >&2
    echo "Error: current active-task identity is unavailable" >&2
    return 1
  fi
  python3 - "$IDENTITY_JSON" "$current_json" "$expected_status" <<'PY'
import json
import sys

identity = json.loads(sys.argv[1])
current = json.loads(sys.argv[2])
expected_status = sys.argv[3]
task = current.get("current_task")
errors = []
if not isinstance(task, dict):
    errors.append("current_task is missing")
if current.get("error"):
    errors.append("resolver returned an error")
if current.get("stale") is not False:
    errors.append("resolver identity is stale")
if current.get("source") in (None, "", "none"):
    errors.append("resolver source is not an active binding")
if current.get("task_workspace_root") != identity["workspace_root"]:
    errors.append("task workspace root does not match")
if current.get("resolved_task_path") != identity["task_dir"]:
    errors.append("resolved task path does not match")
if isinstance(task, dict):
    if task.get("id") != identity["task_id"]:
        errors.append("task id does not match")
    if task.get("status") != expected_status:
        errors.append("task status does not match")
    if task.get("branch") != identity["branch"]:
        errors.append("task branch does not match")
if errors:
    print("Error: current active-task identity mismatch: " + "; ".join(errors), file=sys.stderr)
    raise SystemExit(1)
PY
}

if [[ "$MODE" == "recovery" ]]; then
  verify_current_identity in_progress
fi

UPSTREAM_EXECUTED=false
if [[ "$MODE" == "initial" ]]; then
  stdout_file="$(mktemp)"
  stderr_file="$(mktemp)"
  trap 'rm -f "$stdout_file" "$stderr_file"' EXIT
  if ! python3 "$TASK_PY" start "$TASK_PATH" "$@" >"$stdout_file" 2>"$stderr_file"; then
    cat "$stdout_file"
    cat "$stderr_file" >&2
    exit 1
  fi
  UPSTREAM_EXECUTED=true
  "$SCRIPT_DIR/check-workspace-boundary.sh" --json --task "$TASK_PATH" >/dev/null
  verify_current_identity in_progress
fi

python3 - "$IDENTITY_JSON" "$MODE" "$UPSTREAM_EXECUTED" <<'PY'
import json
import sys

identity = json.loads(sys.argv[1])
mode = sys.argv[2]
upstream_executed = sys.argv[3] == "true"
print(json.dumps({
    "schema_version": "1.0",
    "operation": "task_activation",
    "exit_id": "activated",
    "mode": mode,
    "status": "ok",
    "task_ref": identity["task_ref"],
    "task_status": "in_progress",
    "upstream_start_executed": upstream_executed,
}, ensure_ascii=False, sort_keys=True))
PY
