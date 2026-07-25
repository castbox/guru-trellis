#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/guru-verify-extension-installation) REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-verify-extension-installation}" ;;
  */.trellis/guru-team/skills/packages/guru-verify-extension-installation) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-verify-extension-installation}" ;;
  */.agents/skills/guru-verify-extension-installation) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-verify-extension-installation}" ;;
  */.codex/skills/guru-verify-extension-installation) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-verify-extension-installation}" ;;
  */.cursor/skills/guru-verify-extension-installation) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-verify-extension-installation}" ;;
  */.claude/skills/guru-verify-extension-installation) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-verify-extension-installation}" ;;
  *) REPO_ROOT="" ;;
esac
DISPATCHER="${GURU_TEAM_DISPATCHER:-${REPO_ROOT:?unsupported Skill package root for guru-verify-extension-installation}/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator public_invocation -- "$@"
