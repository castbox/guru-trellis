#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  printf '%s\n' '{"code":"invalid_arguments","field_path":"arguments","dependency":"python-runtime","runtime_identity":null,"remediation":"trellis/presets/guru-team/scripts/bash/apply.sh --repo ."}' >&2
  exit 2
fi
REPO_ROOT="$1"
RUNTIME_ASSETS="$2"
shift 2
ACTIVE="$REPO_ROOT/.trellis/.runtime/guru-team/python/active.json"
REMEDIATION="trellis/presets/guru-team/scripts/bash/apply.sh --repo ."

runtime_error() {
  local identity="${1:-null}"
  printf '{"code":"runtime_dependency_missing","field_path":"runtime","dependency":"jsonschema","runtime_identity":%s,"remediation":"%s"}\n' "$identity" "$REMEDIATION" >&2
  exit 2
}

[[ -f "$ACTIVE" && ! -L "$ACTIVE" ]] || runtime_error
ACTIVE_LINE="$(tr -d '\n\r' < "$ACTIVE")"
RUNTIME_ID="$(printf '%s' "$ACTIVE_LINE" | sed -n 's/.*"runtime_id":"\([0-9a-f]\{24\}\)".*/\1/p')"
INTERPRETER="$(printf '%s' "$ACTIVE_LINE" | sed -n 's/.*"interpreter":"\([^"]*\)".*/\1/p')"
case "$INTERPRETER" in
  "$RUNTIME_ID/venv/bin/python"|"$RUNTIME_ID/venv/Scripts/python.exe") ;;
  *) runtime_error ;;
esac
MANAGED_PYTHON="$REPO_ROOT/.trellis/.runtime/guru-team/python/$INTERPRETER"
[[ -f "$MANAGED_PYTHON" && -x "$MANAGED_PYTHON" ]] || runtime_error "\"$RUNTIME_ID\""
"$MANAGED_PYTHON" "$RUNTIME_ASSETS/bootstrap.py" --repo "$REPO_ROOT" --runtime-assets "$RUNTIME_ASSETS" --python "$MANAGED_PYTHON" --validate-active "$RUNTIME_ID" --json >/dev/null 2>&1 || runtime_error "\"$RUNTIME_ID\""
exec "$MANAGED_PYTHON" "$@"
