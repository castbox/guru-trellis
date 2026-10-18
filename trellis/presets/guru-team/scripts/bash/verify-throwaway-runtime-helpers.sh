#!/usr/bin/env bash

source_python() {
  "$SOURCE_RUNTIME_RESOLVER" "$REPO_ROOT" "$SOURCE_RUNTIME_ASSETS" "$@"
}

installed_python() {
  local installed_repo="$1"
  shift
  "$installed_repo/.trellis/guru-team/runtime/resolve-python.sh" \
    "$installed_repo" \
    "$installed_repo/.trellis/guru-team/runtime" \
    "$@"
}

assert_source_runtime_checkpoint() {
  local checkpoint_json="$1"
  local checkpoint_label="$2"
  local bootstrap_consumed="$3"
  source_python -c '
import json,re,sys
from pathlib import Path
payload=json.loads(sys.argv[1])
assert payload["status"] == "ok"
assert payload["checkpoint"] == sys.argv[2]
assert payload["repo"] == str(Path(sys.argv[4]).resolve())
assert payload["bootstrap_consumed"] is (sys.argv[3] == "true")
assert re.fullmatch(r"[0-9a-f]{24}", payload["runtime_id"])
assert re.fullmatch(r"[0-9a-f]{64}", payload["dependency_lock_sha256"])
assert payload["sys_executable_launch_path"] == payload["interpreter_launch_path"]
assert Path(payload["sys_executable"]).resolve() == Path(payload["interpreter"]).resolve()
assert payload["sys_executable_resolved"] == payload["interpreter_resolved"]
' "$checkpoint_json" "$checkpoint_label" "$bootstrap_consumed" "$REPO_ROOT"
}

assert_installed_runtime_checkpoint() {
  local checkpoint_repo="$1"
  local checkpoint_json="$2"
  local checkpoint_label="$3"
  installed_python "$checkpoint_repo" -c '
import json,re,sys
from pathlib import Path
payload=json.loads(sys.argv[1])
assert payload["status"] == "ok"
assert payload["checkpoint"] == sys.argv[2]
assert payload["repo"] == str(Path(sys.argv[3]).resolve())
assert payload["bootstrap_consumed"] is False
assert re.fullmatch(r"[0-9a-f]{24}", payload["runtime_id"])
assert re.fullmatch(r"[0-9a-f]{64}", payload["dependency_lock_sha256"])
assert payload["sys_executable_launch_path"] == payload["interpreter_launch_path"]
assert Path(payload["sys_executable"]).resolve() == Path(payload["interpreter"]).resolve()
assert payload["sys_executable_resolved"] == payload["interpreter_resolved"]
' "$checkpoint_json" "$checkpoint_label" "$checkpoint_repo"
}

assert_embedded_runtime_checkpoint() {
  local checkpoint_repo="$1"
  local outer_json="$2"
  local payload_json="$3"
  local embedded_label="$4"
  installed_python "$checkpoint_repo" -c '
import json,sys
outer=json.loads(sys.argv[1])
embedded=json.loads(sys.argv[2])["runtime_checkpoint"]
assert embedded["status"] == "ok"
assert embedded["checkpoint"] == sys.argv[3]
for key in (
    "runtime_id", "sys_executable", "sys_executable_launch_path",
    "sys_executable_resolved", "interpreter", "interpreter_launch_path",
    "interpreter_resolved", "dependency_lock_sha256",
):
    assert embedded[key] == outer[key], (key, embedded[key], outer[key])
' "$outer_json" "$payload_json" "$embedded_label"
}

workspace_tree_digest() {
  source_python - "$1" <<'PY'
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
digest = hashlib.sha256()
if root.is_dir():
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
print(digest.hexdigest())
PY
}

file_sha256() {
  source_python - "$1" <<'PY'
import hashlib
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.is_file():
    raise SystemExit(f"expected regular file: {path}")
print(hashlib.sha256(path.read_bytes()).hexdigest())
PY
}

assert_official_state_absent() {
  local root="$1"
  local label="$2"
  if [[ -e "$root/.trellis/.developer" || -e "$root/.trellis/workspace" ]]; then
    echo "Guru operation recreated official identity/workspace state during $label" >&2
    exit 2
  fi
}
