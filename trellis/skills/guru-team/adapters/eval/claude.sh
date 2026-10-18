#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
if [[ -x "$SCRIPT_DIR/../../runtime/resolve-python.sh" ]]; then
  RUNTIME_ASSETS="$(cd "$SCRIPT_DIR/../../runtime" && pwd)"
elif [[ -x "$SCRIPT_DIR/../../../runtime/resolve-python.sh" ]]; then
  RUNTIME_ASSETS="$(cd "$SCRIPT_DIR/../../../runtime" && pwd)"
else
  echo '{"code":"runtime_dependency_missing","field_path":"runtime","dependency":"python-runtime","runtime_identity":null,"remediation":"trellis/presets/guru-team/scripts/bash/apply.sh --repo ."}' >&2
  exit 2
fi
exec "$RUNTIME_ASSETS/resolve-python.sh" "$REPO_ROOT" "$RUNTIME_ASSETS" "$SCRIPT_DIR/native_adapter.py" --adapter claude "$@"
