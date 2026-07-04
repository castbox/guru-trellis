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
python3 "$SCRIPT_DIR/../python/guru_team_trellis.py" version --root "$ROOT" "${JSON_ARGS[@]}"
