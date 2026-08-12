#!/usr/bin/env bash
set -euo pipefail

ROOT=""
JSON_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      ROOT="$2"
      shift 2
      ;;
    --json)
      JSON_ARGS=(--json)
      shift
      ;;
    -h|--help)
      cat <<'EOF'
Usage: version.sh [--root <repo>] [--json]

Show the installed Guru Team Trellis extension version and provenance.
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$ROOT" ]]; then
  ROOT="$(pwd)"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/runtime/utility.py" ]]; then
  RUNTIME_PARENT="$(cd "$SCRIPT_DIR/../../../../skills/guru-team" && pwd)"
elif [[ -f "$SCRIPT_DIR/../../runtime/utility.py" ]]; then
  RUNTIME_PARENT="$(cd "$SCRIPT_DIR/../.." && pwd)"
else
  echo "Guru Team shared runtime is missing: runtime/utility.py" >&2
  exit 2
fi
export PYTHONPATH="$RUNTIME_PARENT${PYTHONPATH:+:$PYTHONPATH}"
python3 -m runtime.utility version --root "$ROOT" "${JSON_ARGS[@]}"
