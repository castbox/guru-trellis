#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-verify-extension-installation/scripts/version.sh" ]]; then
  TARGET="$SCRIPT_DIR/../../../../skills/guru-team/packages/guru-verify-extension-installation/scripts/version.sh"
else
  TARGET="$SCRIPT_DIR/../../skills/packages/guru-verify-extension-installation/scripts/version.sh"
fi
exec "$TARGET" "$@"
