#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/guru-example-sync) REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-example-sync}" ;;
  */.trellis/guru-team/skills/packages/guru-example-sync) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-example-sync}" ;;
  */.agents/skills/guru-example-sync) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-example-sync}" ;;
  */.codex/skills/guru-example-sync) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-example-sync}" ;;
  */.cursor/skills/guru-example-sync) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-example-sync}" ;;
  */.claude/skills/guru-example-sync) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-example-sync}" ;;
  *) REPO_ROOT="" ;;
esac
DISPATCHER="${GURU_TEAM_DISPATCHER:-${REPO_ROOT:?unsupported Skill package root for guru-example-sync}/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator public_invocation -- "$@"
