#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GURU_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
BOOTSTRAP_PYTHON="${GURU_MANAGED_RUNTIME_BOOTSTRAP_PYTHON:-$(command -v python3)}"
TEMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/guru-managed-python.XXXXXX")"

cleanup() {
  rm -rf -- "$TEMP_ROOT"
}
trap cleanup EXIT

PATH_VENV="$TEMP_ROOT/path-python"
PATH_BIN="$TEMP_ROOT/bin"
TARGET="$TEMP_ROOT/repo"
mkdir -p "$PATH_BIN" "$TARGET/.trellis"
"$BOOTSTRAP_PYTHON" -m venv --without-pip "$PATH_VENV"
cat > "$PATH_BIN/python3" <<EOF
#!/usr/bin/env bash
exec "$PATH_VENV/bin/python" "\$@"
EOF
chmod +x "$PATH_BIN/python3"

if "$PATH_BIN/python3" -c 'import jsonschema' >/dev/null 2>&1; then
  echo "focused runtime precondition failed: PATH Python imports jsonschema" >&2
  exit 2
fi
if "$PATH_BIN/python3" -m pip --version >/dev/null 2>&1; then
  echo "focused runtime precondition failed: PATH Python has pip" >&2
  exit 2
fi

cp "$GURU_ROOT/trellis/workflows/guru-team/workflow.md" "$TARGET/.trellis/workflow.md"
git init -q -b main "$TARGET"
PATH="$PATH_BIN:/usr/bin:/bin:/usr/sbin:/sbin" \
  "$SCRIPT_DIR/apply.sh" --repo "$TARGET" --platform codex > "$TEMP_ROOT/apply.json"
PATH="$PATH_BIN:/usr/bin:/bin:/usr/sbin:/sbin" \
  "$TARGET/.trellis/guru-team/scripts/bash/discover-skill-contract.sh" \
  --root "$TARGET" --mode installed --skill guru-sync-base --json > "$TEMP_ROOT/wrapper.json"

"$BOOTSTRAP_PYTHON" - "$TEMP_ROOT/apply.json" "$TEMP_ROOT/wrapper.json" "$TARGET" <<'PY'
import json
import pathlib
import sys

apply = json.load(open(sys.argv[1], encoding="utf-8"))
wrapper = json.load(open(sys.argv[2], encoding="utf-8"))
repo = pathlib.Path(sys.argv[3])
active = json.loads((repo / ".trellis/.runtime/guru-team/python/active.json").read_text())
managed_python = repo / ".trellis/.runtime/guru-team/python" / active["interpreter"]
result = {
    "status": "ok",
    "path_python_jsonschema": False,
    "path_python_pip": False,
    "preset_apply": apply["status"],
    "runtime_action": apply["python_runtime"]["action"],
    "runtime_identity": apply["python_runtime"]["runtime_identity"],
    "managed_python_exists": managed_python.is_file(),
    "public_wrapper_status": wrapper["status"],
    "public_wrapper_skill_id": wrapper["skill_id"],
}
if apply["status"] != "ok" or wrapper["status"] != "ok" or not managed_python.is_file():
    raise SystemExit(2)
print(json.dumps(result, sort_keys=True))
PY
