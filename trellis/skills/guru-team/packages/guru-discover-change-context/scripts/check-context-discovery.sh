#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT=""
case "$PACKAGE_ROOT" in
  */.trellis/guru-team/skills/packages/guru-discover-change-context) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-discover-change-context}" ;;
  */.agents/skills/guru-discover-change-context) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-discover-change-context}" ;;
  */.codex/skills/guru-discover-change-context) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-discover-change-context}" ;;
  */.cursor/skills/guru-discover-change-context) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-discover-change-context}" ;;
  */.claude/skills/guru-discover-change-context) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-discover-change-context}" ;;
esac
DISPATCHER="$REPO_ROOT/.trellis/guru-team/scripts/bash/run-skill-command.sh"
if [[ -z "$REPO_ROOT" || ! -x "$DISPATCHER" ]]; then
  echo "Guru Team Skill packages are not self-contained or portable. Install or upgrade the complete Guru Team preset, resolve every .new/.bak sidecar, run source and installed Skill package validation, then retry." >&2
  exit 2
fi
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator snapshot_validator -- "$@"
