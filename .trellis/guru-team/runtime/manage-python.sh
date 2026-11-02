#!/usr/bin/env bash
set -euo pipefail

# This seed runs only the current owner's standard-library resolver. The final
# command runs in the selected managed environment with the target's assets.
if [[ $# -lt 3 ]]; then
  printf '%s\n' '{"code":"invalid_arguments","field_path":"runtime","dependency":"python-runtime","runtime_identity":null,"remediation":"Use manage-python.sh REPO ASSETS --check, --resolve-active, or --repair [--python PYTHON]."}' >&2
  exit 2
fi
REPO_ROOT="$1"
RUNTIME_ASSETS="$2"
shift 2
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
unset PYTHONHOME
CACHE_ROOT="${GURU_TEAM_PYTHON_CACHE_ROOT:-}"
if [[ -z "$CACHE_ROOT" ]]; then
  case "${OSTYPE:-}" in
    darwin*) CACHE_ROOT="$HOME/Library/Caches/guru-team/python" ;;
    msys*|cygwin*|win*) CACHE_ROOT="${LOCALAPPDATA:-$HOME/AppData/Local}/GuruTeam/python" ;;
    *) CACHE_ROOT="${XDG_CACHE_HOME:-$HOME/.cache}/guru-team/python" ;;
  esac
fi
case "$CACHE_ROOT" in
  "~/"*) CACHE_ROOT="$HOME/${CACHE_ROOT#\~/}" ;;
esac
SEED=""
ARGUMENTS=("$@")
while [[ $# -gt 0 ]]; do
  case "$1" in
    --) break ;;
    --python) SEED="${2:-}"; break ;;
    --python=*) SEED="${1#--python=}"; break ;;
    *) shift ;;
  esac
done
set -- "${ARGUMENTS[@]}"
if [[ -n "$SEED" ]]; then
  if ! command -v "$SEED" >/dev/null 2>&1 || ! "$SEED" -S -c 'import sys; assert sys.version_info.major == 3' >/dev/null 2>&1; then
    printf '%s\n' '{"code":"interpreter_unavailable","field_path":"runtime","dependency":"python-runtime","runtime_identity":null,"remediation":"Provide an executable CPython3 with --python /path/to/python3."}' >&2
    exit 2
  fi
fi
for candidate in "$CACHE_ROOT"/[0-9a-f]*/venv/bin/python "$CACHE_ROOT"/[0-9a-f]*/venv/Scripts/python.exe; do
  if [[ -n "$SEED" ]]; then break; fi
  if [[ -f "$candidate" && -x "$candidate" ]] && "$candidate" -S -c 'import sys; assert sys.version_info.major == 3' >/dev/null 2>&1; then
    SEED="$candidate"
    break
  fi
done
if [[ -z "$SEED" ]] && command -v python3 >/dev/null 2>&1; then
  SEED="$(command -v python3)"
fi
if [[ -z "$SEED" ]]; then
  printf '%s\n' '{"code":"interpreter_unavailable","field_path":"runtime","dependency":"python-runtime","runtime_identity":null,"remediation":"Provide an executable CPython3 on PATH for manage-python.sh REPO ASSETS --repair --python /path/to/python3."}' >&2
  exit 2
fi
exec "$SEED" -S "$RUNTIME_ASSETS/bootstrap.py" --repo "$REPO_ROOT" --runtime-assets "$RUNTIME_ASSETS" "$@"
