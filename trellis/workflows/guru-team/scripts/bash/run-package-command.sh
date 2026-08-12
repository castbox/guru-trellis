#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: run-package-command.sh SKILL_ID PACKAGE_WRAPPER [arguments]" >&2
  exit 2
fi

SKILL_ID="$1"
PACKAGE_WRAPPER="$2"
shift 2
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAYOUT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

if [[ -d "$LAYOUT_ROOT/skills/guru-team/packages/$SKILL_ID" ]]; then
  PACKAGE_ROOT="$LAYOUT_ROOT/skills/guru-team/packages/$SKILL_ID"
elif [[ -d "$LAYOUT_ROOT/.trellis/guru-team/skills/packages/$SKILL_ID" ]]; then
  PACKAGE_ROOT="$LAYOUT_ROOT/.trellis/guru-team/skills/packages/$SKILL_ID"
else
  echo "Guru Team package runtime is missing for $SKILL_ID." >&2
  exit 2
fi

TARGET="$PACKAGE_ROOT/$PACKAGE_WRAPPER"
if [[ ! -x "$TARGET" ]]; then
  echo "Guru Team package command is missing or not executable: $SKILL_ID/$PACKAGE_WRAPPER" >&2
  exit 2
fi
exec "$TARGET" "$@"
