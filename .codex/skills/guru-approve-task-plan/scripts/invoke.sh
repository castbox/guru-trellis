#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/guru-approve-task-plan) REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-approve-task-plan}" ;;
  */.trellis/guru-team/skills/packages/guru-approve-task-plan) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-approve-task-plan}" ;;
  */.agents/skills/guru-approve-task-plan) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-approve-task-plan}" ;;
  */.codex/skills/guru-approve-task-plan) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-approve-task-plan}" ;;
  */.cursor/skills/guru-approve-task-plan) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-approve-task-plan}" ;;
  */.claude/skills/guru-approve-task-plan) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-approve-task-plan}" ;;
  *) REPO_ROOT="" ;;
esac
DISPATCHER="${GURU_TEAM_DISPATCHER:-${REPO_ROOT:?unsupported Skill package root for guru-approve-task-plan}/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator public_invocation -- "$@"
