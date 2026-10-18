#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
RUNTIME_ASSETS="$REPO_ROOT/trellis/skills/guru-team/runtime"
RESOLVER="$RUNTIME_ASSETS/resolve-python.sh"
TEMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/guru-throwaway-python-matrix.XXXXXX")"

cleanup() {
  case "$TEMP_ROOT" in
    "${TMPDIR:-/tmp}"/guru-throwaway-python-matrix.*)
      rm -rf -- "$TEMP_ROOT"
      ;;
    *)
      echo "Refusing to clean unexpected matrix path: $TEMP_ROOT" >&2
      ;;
  esac
}
trap cleanup EXIT

SOURCE_PYTHON="$(
  "$RESOLVER" "$REPO_ROOT" "$RUNTIME_ASSETS" \
    -c 'import sys; print(sys.executable)'
)"

NO_DEPENDENCY_VENV="$TEMP_ROOT/no-dependency-python"
"$RESOLVER" "$REPO_ROOT" "$RUNTIME_ASSETS" \
  -m venv --without-pip "$NO_DEPENDENCY_VENV"
NO_DEPENDENCY_PYTHON="$NO_DEPENDENCY_VENV/bin/python"
if [[ ! -x "$NO_DEPENDENCY_PYTHON" ]]; then
  NO_DEPENDENCY_PYTHON="$NO_DEPENDENCY_VENV/Scripts/python.exe"
fi
test -x "$NO_DEPENDENCY_PYTHON"

NO_DEPENDENCY_BIN="$TEMP_ROOT/no-dependency-bin"
WITH_DEPENDENCY_BIN="$TEMP_ROOT/with-dependency-bin"
mkdir -p "$NO_DEPENDENCY_BIN" "$WITH_DEPENDENCY_BIN"

cat >"$NO_DEPENDENCY_BIN/python3" <<EOF
#!/usr/bin/env bash
exec "$NO_DEPENDENCY_PYTHON" "\$@"
EOF
chmod +x "$NO_DEPENDENCY_BIN/python3"

POISON_FILE="$TEMP_ROOT/path-python.poison"
POISON_LOG="$TEMP_ROOT/path-python-after-seed.log"
cat >"$WITH_DEPENDENCY_BIN/python3" <<EOF
#!/usr/bin/env bash
set -euo pipefail
if [[ -e "$POISON_FILE" ]]; then
  printf '%s\n' "\$*" >>"$POISON_LOG"
  echo "PATH Python was invoked after the bootstrap seed" >&2
  exit 97
fi
exec "$SOURCE_PYTHON" "\$@"
EOF
chmod +x "$WITH_DEPENDENCY_BIN/python3"
cp "$WITH_DEPENDENCY_BIN/python3" "$WITH_DEPENDENCY_BIN/python"
chmod +x "$WITH_DEPENDENCY_BIN/python"

if "$NO_DEPENDENCY_BIN/python3" -m pip --version >/dev/null 2>&1; then
  echo "No-dependency PATH Python unexpectedly has pip" >&2
  exit 2
fi
if "$NO_DEPENDENCY_BIN/python3" -c 'import jsonschema' >/dev/null 2>&1; then
  echo "No-dependency PATH Python unexpectedly imports jsonschema" >&2
  exit 2
fi
"$WITH_DEPENDENCY_BIN/python3" -c 'import jsonschema' >/dev/null

(
  cd "$REPO_ROOT"
  export PATH="$NO_DEPENDENCY_BIN:$PATH"
  export TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1
  unset GURU_TEAM_VERIFY_PATH_PYTHON_POISON_FILE
  ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
)

rm -f "$POISON_FILE" "$POISON_LOG"
(
  cd "$REPO_ROOT"
  export PATH="$WITH_DEPENDENCY_BIN:$PATH"
  export TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1
  export GURU_TEAM_VERIFY_PATH_PYTHON_POISON_FILE="$POISON_FILE"
  export TRELLIS_PYTHON_CMD=python
  ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
)

test -f "$POISON_FILE"
if [[ -s "$POISON_LOG" ]]; then
  echo "PATH Python poison caught post-bootstrap calls:" >&2
  cat "$POISON_LOG" >&2
  exit 2
fi

echo "Verified README raw throwaway command with and without PATH jsonschema."
