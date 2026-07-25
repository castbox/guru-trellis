#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/guru-review-task-publication) REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-review-task-publication}" ;;
  */.trellis/guru-team/skills/packages/guru-review-task-publication) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-review-task-publication}" ;;
  */.agents/skills/guru-review-task-publication) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-review-task-publication}" ;;
  */.codex/skills/guru-review-task-publication) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-review-task-publication}" ;;
  */.cursor/skills/guru-review-task-publication) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-review-task-publication}" ;;
  */.claude/skills/guru-review-task-publication) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-review-task-publication}" ;;
  *) REPO_ROOT="" ;;
esac
DISPATCHER="${GURU_TEAM_DISPATCHER:-${REPO_ROOT:?unsupported Skill package root for guru-review-task-publication}/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator publication_review_checker -- "$@"
