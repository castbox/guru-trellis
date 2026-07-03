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
Usage: check-env.sh [--root <repo>] [--json]

Check local prerequisites for the Guru Team Trellis workflow.
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
python3 "$SCRIPT_DIR/../python/guru_team_trellis.py" check-env --root "$ROOT" "${JSON_ARGS[@]}"
