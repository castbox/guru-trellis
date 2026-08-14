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
SOURCE="$TEMP_ROOT/source"
mkdir -p "$PATH_BIN" "$TARGET/.trellis" "$SOURCE/.trellis"
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

cp -R "$GURU_ROOT/trellis" "$SOURCE/trellis"
cp -R "$GURU_ROOT/.trellis/scripts" "$SOURCE/.trellis/scripts"
cp "$SOURCE/trellis/workflows/guru-team/workflow.md" "$SOURCE/.trellis/workflow.md"
git init -q -b main "$SOURCE"
cp -R "$GURU_ROOT/.trellis/scripts" "$TARGET/.trellis/scripts"
cp "$GURU_ROOT/trellis/workflows/guru-team/workflow.md" "$TARGET/.trellis/workflow.md"
git init -q -b main "$TARGET"
PATH="$PATH_BIN:/usr/bin:/bin:/usr/sbin:/sbin" \
  "$SOURCE/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$SOURCE" --platform codex > "$TEMP_ROOT/source-apply.json"
PATH="$PATH_BIN:/usr/bin:/bin:/usr/sbin:/sbin" \
  "$SCRIPT_DIR/apply.sh" --repo "$TARGET" --platform codex > "$TEMP_ROOT/apply.json"

FOCUSED_PATH="$PATH_BIN:/usr/bin:/bin:/usr/sbin:/sbin"
PATH="$FOCUSED_PATH" \
  "$SOURCE/trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh" \
  --root "$SOURCE" --mode source --json > "$TEMP_ROOT/source-validation.json"
mv "$SOURCE/.trellis/.runtime/guru-team/python/active.json" \
  "$SOURCE/.trellis/.runtime/guru-team/python/active.saved"
PATH="$FOCUSED_PATH" \
  "$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" \
  --root "$SOURCE" --mode source --json > "$TEMP_ROOT/target-wrapper-source-validation.json"
mv "$SOURCE/.trellis/.runtime/guru-team/python/active.saved" \
  "$SOURCE/.trellis/.runtime/guru-team/python/active.json"
PATH="$FOCUSED_PATH" \
  "$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" \
  --root "$TARGET" --mode installed --json > "$TEMP_ROOT/installed-validation.json"
PATH="$FOCUSED_PATH" \
  "$SOURCE/trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh" \
  --root "$SOURCE" --mode source --skill guru-sync-base --json > "$TEMP_ROOT/source-contract.json"
PATH="$PATH_BIN:/usr/bin:/bin:/usr/sbin:/sbin" \
  "$TARGET/.trellis/guru-team/scripts/bash/discover-skill-contract.sh" \
  --root "$TARGET" --mode installed --skill guru-sync-base --json > "$TEMP_ROOT/installed-contract.json"
PATH="$FOCUSED_PATH" \
  "$SOURCE/trellis/workflows/guru-team/scripts/bash/discover-skill-evals.sh" \
  --root "$SOURCE" --mode source --skill guru-clarify-requirements --json > "$TEMP_ROOT/source-eval-discovery.json"
PATH="$FOCUSED_PATH" \
  "$TARGET/.trellis/guru-team/scripts/bash/discover-skill-evals.sh" \
  --root "$TARGET" --mode installed --skill guru-clarify-requirements --json > "$TEMP_ROOT/installed-eval-discovery.json"
PATH="$FOCUSED_PATH" \
  "$SOURCE/trellis/workflows/guru-team/scripts/bash/run-skill-command.sh" \
  --package-root "$SOURCE/trellis/skills/guru-team/packages/guru-verify-extension-installation" \
  --validator extension_version_projection -- --root "$SOURCE" > "$TEMP_ROOT/source-compat.json"
PATH="$FOCUSED_PATH" \
  "$TARGET/.trellis/guru-team/scripts/bash/run-skill-command.sh" \
  --package-root "$TARGET/.trellis/guru-team/skills/packages/guru-verify-extension-installation" \
  --validator extension_version_projection -- --root "$TARGET" > "$TEMP_ROOT/installed-compat.json"
PATH="$FOCUSED_PATH" \
  "$SOURCE/trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh" \
  --root "$SOURCE" --mode source --skill guru-clarify-requirements --adapter shared \
  --case clear-route \
  --run-root "$TEMP_ROOT/source-eval-run" \
  --semantic-grading "$SOURCE/trellis/presets/guru-team/tests/semantic-retrieval-grading.json" \
  --json > "$TEMP_ROOT/source-eval-run.json"
PATH="$FOCUSED_PATH" \
  "$TARGET/.trellis/guru-team/scripts/bash/run-skill-evals.sh" \
  --root "$TARGET" --mode installed --skill guru-clarify-requirements --adapter shared \
  --case clear-route \
  --run-root "$TEMP_ROOT/installed-eval-run" \
  --semantic-grading "$SOURCE/trellis/presets/guru-team/tests/semantic-retrieval-grading.json" \
  --json > "$TEMP_ROOT/installed-eval-run.json"

"$BOOTSTRAP_PYTHON" - "$TEMP_ROOT" "$TARGET" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
repo = pathlib.Path(sys.argv[2])

def load(name):
    return json.loads((root / name).read_text(encoding="utf-8"))

def transcript_errors(payload):
    return [
        json.loads(pathlib.Path(case["transcript_locator"]).read_text(encoding="utf-8")).get("error")
        for case in payload["cases"]
    ]

def first_transcript(payload):
    return json.loads(
        pathlib.Path(payload["cases"][0]["transcript_locator"]).read_text(encoding="utf-8")
    )

apply = load("apply.json")
source_apply = load("source-apply.json")
source_validation = load("source-validation.json")
target_wrapper_source_validation = load("target-wrapper-source-validation.json")
installed_validation = load("installed-validation.json")
source_contract = load("source-contract.json")
installed_contract = load("installed-contract.json")
source_eval_discovery = load("source-eval-discovery.json")
installed_eval_discovery = load("installed-eval-discovery.json")
source_compat = load("source-compat.json")
installed_compat = load("installed-compat.json")
source_eval_run = load("source-eval-run.json")
installed_eval_run = load("installed-eval-run.json")
active = json.loads((repo / ".trellis/.runtime/guru-team/python/active.json").read_text())
managed_python = repo / ".trellis/.runtime/guru-team/python" / active["interpreter"]

assert apply["status"] == "ok"
assert source_apply["status"] == "ok"
assert source_validation["status"] == target_wrapper_source_validation["status"] == installed_validation["status"] == "passed"
assert source_contract["skill_id"] == installed_contract["skill_id"] == "guru-sync-base"
assert source_eval_discovery["status"] == installed_eval_discovery["status"] == "ok"
assert source_eval_run["status"] == installed_eval_run["status"] == "passed", (
    source_eval_run["status"],
    installed_eval_run["status"],
    [case["status"] for case in source_eval_run["cases"]],
    [case["status"] for case in installed_eval_run["cases"]],
    transcript_errors(source_eval_run),
    transcript_errors(installed_eval_run),
    first_transcript(source_eval_run),
    first_transcript(installed_eval_run),
)
assert source_compat["guru_team_extension"]["version"] == installed_compat["guru_team_extension"]["version"]
assert managed_python.is_file()
result = {
    "status": "ok",
    "path_python_jsonschema": False,
    "path_python_pip": False,
    "preset_apply": apply["status"],
    "runtime_action": apply["python_runtime"]["action"],
    "runtime_identity": apply["python_runtime"]["runtime_identity"],
    "managed_python_exists": managed_python.is_file(),
    "source_validation": source_validation["status"],
    "target_wrapper_source_validation": target_wrapper_source_validation["status"],
    "installed_validation": installed_validation["status"],
    "contract_discovery": source_contract["skill_id"],
    "eval_discovery": source_eval_discovery["skill_id"],
    "eval_execution": source_eval_run["status"],
    "compat_extension_version": source_compat["guru_team_extension"]["version"],
}
print(json.dumps(result, sort_keys=True))
PY
