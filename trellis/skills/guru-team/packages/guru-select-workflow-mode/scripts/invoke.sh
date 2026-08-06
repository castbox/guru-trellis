#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/guru-select-workflow-mode) REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-select-workflow-mode}" ;;
  */.trellis/guru-team/skills/packages/guru-select-workflow-mode) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-select-workflow-mode}" ;;
  */.agents/skills/guru-select-workflow-mode) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-select-workflow-mode}" ;;
  */.codex/skills/guru-select-workflow-mode) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-select-workflow-mode}" ;;
  */.cursor/skills/guru-select-workflow-mode) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-select-workflow-mode}" ;;
  */.claude/skills/guru-select-workflow-mode) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-select-workflow-mode}" ;;
  *) REPO_ROOT="" ;;
esac
DISPATCHER="${GURU_TEAM_DISPATCHER:-${REPO_ROOT:?unsupported Skill package root for guru-select-workflow-mode}/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator public_invocation -- "$@"
