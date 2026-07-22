#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/guru-review-contract-wording) REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-review-contract-wording}" ;;
  */.trellis/guru-team/skills/packages/guru-review-contract-wording) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-review-contract-wording}" ;;
  */.agents/skills/guru-review-contract-wording) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-review-contract-wording}" ;;
  */.codex/skills/guru-review-contract-wording) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-review-contract-wording}" ;;
  */.cursor/skills/guru-review-contract-wording) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-review-contract-wording}" ;;
  */.claude/skills/guru-review-contract-wording) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-review-contract-wording}" ;;
  *) REPO_ROOT="" ;;
esac
DISPATCHER="${GURU_TEAM_DISPATCHER:-${REPO_ROOT:?unsupported Skill package root for guru-review-contract-wording}/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator public_invocation -- "$@"
