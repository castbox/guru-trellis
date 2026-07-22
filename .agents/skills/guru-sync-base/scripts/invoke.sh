#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/guru-sync-base) REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-sync-base}" ;;
  */.trellis/guru-team/skills/packages/guru-sync-base) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-sync-base}" ;;
  */.agents/skills/guru-sync-base) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-sync-base}" ;;
  */.codex/skills/guru-sync-base) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-sync-base}" ;;
  */.cursor/skills/guru-sync-base) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-sync-base}" ;;
  */.claude/skills/guru-sync-base) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-sync-base}" ;;
  *) REPO_ROOT="" ;;
esac
DISPATCHER="${GURU_TEAM_DISPATCHER:-${REPO_ROOT:?unsupported Skill package root for guru-sync-base}/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator public_invocation -- "$@"
