#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAYOUT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
if [[ -x "$LAYOUT_ROOT/skills/guru-team/runtime/resolve-python.sh" ]]; then
  REPO_ROOT="$(cd "$LAYOUT_ROOT/.." && pwd)"
  RUNTIME_ROOT="$LAYOUT_ROOT/skills/guru-team"
elif [[ -x "$LAYOUT_ROOT/.trellis/guru-team/runtime/resolve-python.sh" ]]; then
  REPO_ROOT="$LAYOUT_ROOT"
  RUNTIME_ROOT="$LAYOUT_ROOT/.trellis/guru-team"
else
  echo '{"code":"runtime_dependency_missing","field_path":"runtime","dependency":"python-runtime","runtime_identity":null,"remediation":"trellis/presets/guru-team/scripts/bash/apply.sh --repo ."}' >&2
  exit 2
fi
export PYTHONPATH="$RUNTIME_ROOT"
cd "$REPO_ROOT"
exec "$RUNTIME_ROOT/runtime/resolve-python.sh" "$REPO_ROOT" "$RUNTIME_ROOT/runtime" -m runtime.eval_runner run-skill-evals "$@"
