#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

WORK_DIR="${1:-}"
if [[ $# -gt 0 && "$1" != --* ]]; then shift; else WORK_DIR=""; fi
FORK_SOURCE="${TRELLIS_FORK_SOURCE:-}"
PREDECESSOR_SOURCE="${TRELLIS_PREDECESSOR_SOURCE:-}"
PREDECESSOR_COMMIT="${TRELLIS_PREDECESSOR_COMMIT:-}"
VERIFY_MODE="full"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --fork-source) FORK_SOURCE="${2:?--fork-source requires a checkout}"; shift 2 ;;
    --predecessor-source) PREDECESSOR_SOURCE="${2:?--predecessor-source requires a checkout}"; shift 2 ;;
    --predecessor-commit) PREDECESSOR_COMMIT="${2:?--predecessor-commit requires a SHA}"; shift 2 ;;
    --mode) VERIFY_MODE="${2:?--mode requires full or focused}"; shift 2 ;;
    *) echo "Unknown verifier option: $1" >&2; exit 2 ;;
  esac
done
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
WORKFLOW_SOURCE="${TRELLIS_WORKFLOW_SOURCE:-gh:castbox/guru-trellis/trellis#main}"
ALLOW_PUBLIC_SAMPLE="${TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE:-0}"
SEMANTIC_RETRIEVAL_GRADING="$REPO_ROOT/trellis/presets/guru-team/tests/semantic-retrieval-grading.json"
SOURCE_RUNTIME_ASSETS="$REPO_ROOT/trellis/skills/guru-team/runtime"
SOURCE_RUNTIME_RESOLVER="$SOURCE_RUNTIME_ASSETS/resolve-python.sh"
PYTHON_ROUTING_HELPER="$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_throwaway_python_routing.py"
COMPATIBILITY_MATRIX_HELPER="$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py"
PYTHON_CALLER_INVENTORY="$REPO_ROOT/trellis/presets/guru-team/tests/throwaway-python-callers.json"
ENGLISH_LANGUAGE_RULE_PATTERN='All documentation (must|should) be written in .*English'

if [[ -z "$WORK_DIR" ]]; then
  WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/guru-trellis-install.XXXXXX")"
  GURU_AUTO_WORK_DIR=1
else
  GURU_AUTO_WORK_DIR=0
fi

GURU_TEMP_FILES=()
cleanup_guru_temporary_objects() {
  local path
  if [[ "${#GURU_TEMP_FILES[@]}" -gt 0 ]]; then
    for path in "${GURU_TEMP_FILES[@]}"; do
      if [[ -n "$path" && -f "$path" ]]; then
        case "$(basename "$path")" in
          guru-task-commit-input.*|guru-phase2-input.*) rm -f -- "$path" ;;
        esac
      fi
    done
  fi
  if [[ "$GURU_AUTO_WORK_DIR" == 1 && -d "$WORK_DIR" && "$(basename "$WORK_DIR")" == guru-trellis-install.* ]]; then
    rm -rf -- "$WORK_DIR"
  fi
}
trap cleanup_guru_temporary_objects EXIT INT TERM

mkdir -p "$WORK_DIR"
TARGET="$WORK_DIR/project"

if [[ -e "$TARGET" ]]; then
  echo "Target already exists: $TARGET" >&2
  exit 2
fi

[[ -n "$FORK_SOURCE" ]] || { echo "--fork-source is required; no npm fallback" >&2; exit 2; }
[[ "$VERIFY_MODE" == full || "$VERIFY_MODE" == focused ]] || {
  echo "Unknown verifier mode: $VERIFY_MODE" >&2
  exit 2
}

command -v git >/dev/null 2>&1 || {
  echo "git not found on PATH" >&2
  exit 127
}

python3 "$REPO_ROOT/trellis/skills/guru-team/runtime/bootstrap.py" \
  --repo "$REPO_ROOT" \
  --runtime-assets "$REPO_ROOT/trellis/skills/guru-team/runtime" \
  --python "$(command -v python3)" \
  --json > "$WORK_DIR/source-managed-runtime.json"
if [[ -n "${GURU_TEAM_VERIFY_PATH_PYTHON_POISON_FILE:-}" ]]; then
  : >"$GURU_TEAM_VERIFY_PATH_PYTHON_POISON_FILE"
fi

PYTHON_BRIDGE_DIR="$WORK_DIR/source-managed-python-path"
mkdir -p "$PYTHON_BRIDGE_DIR"
cat >"$PYTHON_BRIDGE_DIR/python3" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec "$SOURCE_RUNTIME_RESOLVER" "$REPO_ROOT" "$SOURCE_RUNTIME_ASSETS" "\$@"
EOF
chmod +x "$PYTHON_BRIDGE_DIR/python3"
export PATH="$PYTHON_BRIDGE_DIR:$PATH"
export TRELLIS_PYTHON_CMD=python3

source "$SCRIPT_DIR/verify-throwaway-runtime-helpers.sh"

source_python "$COMPATIBILITY_MATRIX_HELPER" validate-source \
  --repo-root "$REPO_ROOT" --fork-source "$FORK_SOURCE" >"$WORK_DIR/trellis-source.json"


SOURCE_RUNTIME_CHECKPOINT="$(
  source_python "$PYTHON_ROUTING_HELPER" checkpoint \
    --repo "$REPO_ROOT" \
    --runtime-assets "$SOURCE_RUNTIME_ASSETS" \
    --label source-bootstrap \
    --bootstrap-json "$WORK_DIR/source-managed-runtime.json" \
    --json
)"
printf '%s\n' "$SOURCE_RUNTIME_CHECKPOINT"
assert_source_runtime_checkpoint \
  "$SOURCE_RUNTIME_CHECKPOINT" source-bootstrap true

source_python "$PYTHON_ROUTING_HELPER" check-inventory \
  --repo-root "$REPO_ROOT" \
  --inventory "$PYTHON_CALLER_INVENTORY" \
  --json

# Full preserves the standalone catalog; focused is an explicit bounded run.
if [[ "$VERIFY_MODE" == full || "$VERIFY_MODE" == focused ]]; then
  MATRIX_ARGS=(
    run
    --repo-root "$REPO_ROOT"
    --work-root "$WORK_DIR/matrix"
    --workflow-source "$WORKFLOW_SOURCE"
    --fork-source "$FORK_SOURCE"
    --mode "$VERIFY_MODE"
  )
  if [[ -n "$PREDECESSOR_SOURCE" ]]; then
    MATRIX_ARGS+=(--predecessor-source "$PREDECESSOR_SOURCE")
  fi
  if [[ -n "$PREDECESSOR_COMMIT" ]]; then
    MATRIX_ARGS+=(--predecessor-commit "$PREDECESSOR_COMMIT")
  fi
  if [[ "$ALLOW_PUBLIC_SAMPLE" == "1" ]]; then
    MATRIX_ARGS+=(--allow-local-sample)
  fi
  source_python "$COMPATIBILITY_MATRIX_HELPER" "${MATRIX_ARGS[@]}"
  exit 0
fi
