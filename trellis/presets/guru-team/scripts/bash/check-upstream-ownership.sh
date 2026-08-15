#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
RUNTIME_ASSETS="$REPO_ROOT/trellis/skills/guru-team/runtime"

exec "$RUNTIME_ASSETS/resolve-python.sh" \
  "$REPO_ROOT" \
  "$RUNTIME_ASSETS" \
  "$SCRIPT_DIR/../python/validate_upstream_ownership.py" \
  "$@"
