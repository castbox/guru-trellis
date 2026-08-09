#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/guru-merge-task-pr) REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-merge-task-pr}" ;;
  */.trellis/guru-team/skills/packages/guru-merge-task-pr) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-merge-task-pr}" ;;
  */.agents/skills/guru-merge-task-pr) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-merge-task-pr}" ;;
  */.codex/skills/guru-merge-task-pr) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-merge-task-pr}" ;;
  */.cursor/skills/guru-merge-task-pr) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-merge-task-pr}" ;;
  */.claude/skills/guru-merge-task-pr) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-merge-task-pr}" ;;
  *) REPO_ROOT="" ;;
esac
DISPATCHER="${GURU_TEAM_DISPATCHER:-${REPO_ROOT:?unsupported Skill package root for guru-merge-task-pr}/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator merge_recorder -- "$@"
