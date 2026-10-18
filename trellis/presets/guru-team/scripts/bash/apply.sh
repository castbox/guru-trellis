#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
SELECTED_PYTHON=python3
ARGUMENTS=("$@")
while [[ $# -gt 0 ]]; do
  case "$1" in
    --python)
      if [[ $# -lt 2 || -z "$2" ]]; then
        printf '%s\n' '{"code":"interpreter_unavailable","field_path":"runtime","remediation":"Provide --python /path/to/python3 or put executable python3 on PATH."}' >&2
        exit 2
      fi
      SELECTED_PYTHON="$2"
      shift 2
      ;;
    --python=*) SELECTED_PYTHON="${1#--python=}"; shift ;;
    *) shift ;;
  esac
done
if ! command -v "$SELECTED_PYTHON" >/dev/null 2>&1 || [[ ! -x "$(command -v "$SELECTED_PYTHON")" ]]; then
  printf '%s\n' '{"code":"interpreter_unavailable","field_path":"runtime","remediation":"Make python3 executable on PATH or rerun apply.sh --repo . --python /path/to/python3."}' >&2
  exit 2
fi
if ! PYTHON_MAJOR="$("$SELECTED_PYTHON" -c 'import sys; print(sys.version_info[0])' 2>/dev/null)" || [[ "$PYTHON_MAJOR" != 3 ]]; then
  printf '%s\n' '{"code":"python3_required","field_path":"runtime","remediation":"Select Python 3: apply.sh --repo . --python /path/to/python3."}' >&2
  exit 2
fi
exec "$SELECTED_PYTHON" "$SCRIPT_DIR/../python/apply_guru_team_trellis_preset.py" "${ARGUMENTS[@]}"
