#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/guru-create-task-commit) REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-create-task-commit}" ;;
  */.trellis/guru-team/skills/packages/guru-create-task-commit) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-create-task-commit}" ;;
  */.agents/skills/guru-create-task-commit) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-create-task-commit}" ;;
  */.codex/skills/guru-create-task-commit) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-create-task-commit}" ;;
  */.cursor/skills/guru-create-task-commit) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-create-task-commit}" ;;
  */.claude/skills/guru-create-task-commit) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-create-task-commit}" ;;
  *) REPO_ROOT="" ;;
esac
DISPATCHER="${GURU_TEAM_DISPATCHER:-${REPO_ROOT:?unsupported Skill package root for guru-create-task-commit}/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator public_invocation -- "$@"
