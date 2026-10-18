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
NO_PYTHON_BIN="$TEMP_ROOT/no-python-bin"
TARGET="$TEMP_ROOT/repo"
SOURCE="$TEMP_ROOT/source"
mkdir -p "$PATH_BIN" "$NO_PYTHON_BIN" "$TARGET/.trellis" "$SOURCE/.trellis"
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
for command_name in bash dirname sed tr; do
  ln -s "$(command -v "$command_name")" "$NO_PYTHON_BIN/$command_name"
done
if PATH="$NO_PYTHON_BIN" command -v python3 >/dev/null 2>&1; then
  echo "focused runtime precondition failed: no-Python PATH resolves python3" >&2
  exit 2
fi

cp -R "$GURU_ROOT/trellis" "$SOURCE/trellis"
cp -R "$GURU_ROOT/.trellis/scripts" "$SOURCE/.trellis/scripts"
cp "$SOURCE/trellis/workflows/guru-team/workflow.md" "$SOURCE/.trellis/workflow.md"
git init -q -b main "$SOURCE"
git -C "$SOURCE" config user.email "managed-runtime@example.invalid"
git -C "$SOURCE" config user.name "Managed Runtime Fixture"
git -C "$SOURCE" add .
git -C "$SOURCE" commit -q -m "stage focused source checkout"
cp -R "$GURU_ROOT/.trellis/scripts" "$TARGET/.trellis/scripts"
cp "$GURU_ROOT/trellis/workflows/guru-team/workflow.md" "$TARGET/.trellis/workflow.md"
git init -q -b main "$TARGET"
PATH="$PATH_BIN:/usr/bin:/bin:/usr/sbin:/sbin" \
  "$SOURCE/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$SOURCE" --platform codex > "$TEMP_ROOT/source-apply.json"
PATH="$PATH_BIN:/usr/bin:/bin:/usr/sbin:/sbin" \
  "$SCRIPT_DIR/apply.sh" --repo "$TARGET" --platform codex > "$TEMP_ROOT/apply.json"

FOCUSED_PATH="$PATH_BIN:/usr/bin:/bin:/usr/sbin:/sbin"
SOURCE_RESOLVER="$SOURCE/trellis/skills/guru-team/runtime/resolve-python.sh"
SOURCE_POINTER="$(
  "$BOOTSTRAP_PYTHON" "$SOURCE/trellis/skills/guru-team/runtime/bootstrap.py" \
    --repo "$SOURCE" \
    --runtime-assets "$SOURCE/trellis/skills/guru-team/runtime" \
    --print-active-pointer
)"
TARGET_POINTER="$(
  "$BOOTSTRAP_PYTHON" "$TARGET/.trellis/guru-team/runtime/bootstrap.py" \
    --repo "$TARGET" \
    --runtime-assets "$TARGET/.trellis/guru-team/runtime" \
    --print-active-pointer
)"

expect_source_runtime_error() {
  local label="$1"
  local expected_code="$2"
  local expected_dependency="${3:-python-runtime}"
  local stderr_path="$TEMP_ROOT/runtime-error-$label.json"
  local status

  set +e
  PATH="$FOCUSED_PATH" \
    "$SOURCE_RESOLVER" "$SOURCE" "$SOURCE/trellis/skills/guru-team/runtime" \
    -c 'raise SystemExit("managed runtime unexpectedly executed")' \
    > "$TEMP_ROOT/runtime-error-$label.stdout" 2> "$stderr_path"
  status=$?
  set -e
  if [[ "$status" -ne 2 ]]; then
    echo "focused runtime $label expected exit 2, got $status" >&2
    exit 2
  fi
  "$BOOTSTRAP_PYTHON" - "$stderr_path" "$expected_code" "$expected_dependency" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
expected = sys.argv[2]
expected_dependency = sys.argv[3]
payload = json.loads(path.read_text(encoding="utf-8"))
assert payload["code"] == expected, payload
assert payload["field_path"] == "runtime", payload
assert payload["dependency"] == expected_dependency, payload
assert payload["remediation"] == "trellis/presets/guru-team/scripts/bash/apply.sh --repo .", payload
PY
}

mv "$SOURCE_POINTER" "$SOURCE_POINTER.saved"
expect_source_runtime_error missing-pointer runtime_not_bootstrapped
mv "$SOURCE_POINTER.saved" "$SOURCE_POINTER"

cp "$SOURCE_POINTER" "$SOURCE_POINTER.saved"
"$BOOTSTRAP_PYTHON" - "$SOURCE_POINTER" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
payload["runtime_id"] = "0" * 24
path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
PY
expect_source_runtime_error stale-pointer managed_runtime_missing
mv "$SOURCE_POINTER.saved" "$SOURCE_POINTER"

SOURCE_INTERPRETER="$("$BOOTSTRAP_PYTHON" -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["interpreter"])' "$SOURCE_POINTER")"
mv "$SOURCE_INTERPRETER" "$SOURCE_INTERPRETER.saved"
expect_source_runtime_error missing-interpreter managed_runtime_missing
mv "$SOURCE_INTERPRETER.saved" "$SOURCE_INTERPRETER"

SOURCE_LOCK="$SOURCE/trellis/skills/guru-team/runtime/requirements.lock"
cp "$SOURCE_LOCK" "$SOURCE_LOCK.saved"
printf '\n# focused dependency drift\n' >> "$SOURCE_LOCK"
expect_source_runtime_error dependency-lock-drift managed_runtime_missing
mv "$SOURCE_LOCK.saved" "$SOURCE_LOCK"

SOURCE_JSONSCHEMA="$("$SOURCE_INTERPRETER" -c 'import jsonschema, pathlib; print(pathlib.Path(jsonschema.__file__).parent)')"
mv "$SOURCE_JSONSCHEMA" "$SOURCE_JSONSCHEMA.saved"
expect_source_runtime_error missing-dependency runtime_dependency_missing jsonschema
mv "$SOURCE_JSONSCHEMA.saved" "$SOURCE_JSONSCHEMA"

PATH="$FOCUSED_PATH" \
  "$SOURCE/trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh" \
  --root "$SOURCE" --mode source --json > "$TEMP_ROOT/source-validation.json"
mv "$SOURCE_POINTER" "$SOURCE_POINTER.saved"
PATH="$FOCUSED_PATH" \
  "$TARGET/.trellis/guru-team/scripts/bash/check-skill-packages.sh" \
  --root "$SOURCE" --mode source --json > "$TEMP_ROOT/target-wrapper-source-validation.json"
mv "$SOURCE_POINTER.saved" "$SOURCE_POINTER"
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

printf '{' > "$TEMP_ROOT/invalid-adapter-request.json"
mv "$TARGET_POINTER" "$TARGET_POINTER.saved"
for adapter_id in shared codex claude cursor; do
  PATH="$NO_PYTHON_BIN" \
    "$SOURCE/trellis/skills/guru-team/adapters/eval/$adapter_id.sh" \
    --native-command unused \
    --request "$TEMP_ROOT/invalid-adapter-request.json" \
    > "$TEMP_ROOT/source-$adapter_id-no-path-python.json"
done
mv "$TARGET_POINTER.saved" "$TARGET_POINTER"
mv "$SOURCE_POINTER" "$SOURCE_POINTER.saved"
for adapter_id in shared codex claude cursor; do
  PATH="$NO_PYTHON_BIN" \
    "$TARGET/.trellis/guru-team/skills/adapters/eval/$adapter_id.sh" \
    --native-command unused \
    --request "$TEMP_ROOT/invalid-adapter-request.json" \
    > "$TEMP_ROOT/installed-$adapter_id-no-path-python.json"
done
mv "$SOURCE_POINTER.saved" "$SOURCE_POINTER"

"$BOOTSTRAP_PYTHON" - "$TEMP_ROOT" "$SOURCE" "$TARGET" "$SOURCE_POINTER" "$TARGET_POINTER" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
source_repo = pathlib.Path(sys.argv[2])
repo = pathlib.Path(sys.argv[3])
source_pointer = pathlib.Path(sys.argv[4])
target_pointer = pathlib.Path(sys.argv[5])

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
adapter_probes = {
    f"{mode}-{adapter}": load(f"{mode}-{adapter}-no-path-python.json")
    for mode in ("source", "installed")
    for adapter in ("shared", "codex", "claude", "cursor")
}
source_active = json.loads(source_pointer.read_text())
active = json.loads(target_pointer.read_text())
managed_python = pathlib.Path(apply["python_runtime"]["interpreter"])

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
assert all(
    payload["capability_status"] == "execution_error"
    and payload["public_stderr"] == "adapter request/context invalid"
    for payload in adapter_probes.values()
), adapter_probes
assert source_compat["guru_team_extension"]["version"] == installed_compat["guru_team_extension"]["version"]
assert managed_python.is_file()
result = {
    "status": "ok",
    "path_python_jsonschema": False,
    "path_python_pip": False,
    "path_without_python3": True,
    "preset_apply": apply["status"],
    "runtime_action": apply["python_runtime"]["action"],
    "runtime_identity": apply["python_runtime"]["runtime_identity"],
    "source_runtime_identity": source_active["runtime_id"],
    "managed_python_exists": managed_python.is_file(),
    "source_validation": source_validation["status"],
    "target_wrapper_source_validation": target_wrapper_source_validation["status"],
    "installed_validation": installed_validation["status"],
    "contract_discovery": source_contract["skill_id"],
    "eval_discovery": source_eval_discovery["skill_id"],
    "source_eval_execution": source_eval_run["status"],
    "installed_eval_execution": installed_eval_run["status"],
    "adapter_no_path_python_probes": sorted(adapter_probes),
    "compat_extension_version": source_compat["guru_team_extension"]["version"],
    "runtime_error_codes": {
        "missing_pointer": load("runtime-error-missing-pointer.json")["code"],
        "stale_pointer": load("runtime-error-stale-pointer.json")["code"],
        "missing_interpreter": load("runtime-error-missing-interpreter.json")["code"],
        "dependency_lock_drift": load("runtime-error-dependency-lock-drift.json")["code"],
        "missing_dependency": load("runtime-error-missing-dependency.json")["code"],
    },
}
print(json.dumps(result, sort_keys=True))
PY
