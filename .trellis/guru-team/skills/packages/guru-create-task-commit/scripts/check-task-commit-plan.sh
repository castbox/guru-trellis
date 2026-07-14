#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RUNTIME=""
for candidate in \
  "$PACKAGE_ROOT/../../../scripts/bash/check-commit-messages.sh" \
  "$PACKAGE_ROOT/../../../.trellis/guru-team/scripts/bash/check-commit-messages.sh"; do
  if [[ -x "$candidate" ]]; then
    RUNTIME="$candidate"
    break
  fi
done
if [[ -z "$RUNTIME" ]]; then
  echo "Installed check-commit-messages.sh runtime not found." >&2
  exit 2
fi
exec "$RUNTIME" "$@"
