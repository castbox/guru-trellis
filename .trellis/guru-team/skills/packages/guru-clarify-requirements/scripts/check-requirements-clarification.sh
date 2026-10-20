#!/usr/bin/env bash
set -euo pipefail
PACKAGE_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../runtime/launch.sh"
if [[ ! -f "$LAUNCHER" ]]; then
  LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../../runtime/launch.sh"
fi
if [[ ! -f "$LAUNCHER" ]]; then echo 'Guru Team Skill packages are not self-contained or portable. Install or upgrade the complete Guru Team preset.' >&2; exit 2; fi
source "$LAUNCHER" check-requirements-clarification "$@"
