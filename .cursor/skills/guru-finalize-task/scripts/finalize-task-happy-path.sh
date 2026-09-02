#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/guru-finalize-task) REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-finalize-task}" ;;
  */.trellis/guru-team/skills/packages/guru-finalize-task) REPO_ROOT="${PACKAGE_ROOT%/.trellis/guru-team/skills/packages/guru-finalize-task}" ;;
  */.agents/skills/guru-finalize-task) REPO_ROOT="${PACKAGE_ROOT%/.agents/skills/guru-finalize-task}" ;;
  */.codex/skills/guru-finalize-task) REPO_ROOT="${PACKAGE_ROOT%/.codex/skills/guru-finalize-task}" ;;
  */.cursor/skills/guru-finalize-task) REPO_ROOT="${PACKAGE_ROOT%/.cursor/skills/guru-finalize-task}" ;;
  */.claude/skills/guru-finalize-task) REPO_ROOT="${PACKAGE_ROOT%/.claude/skills/guru-finalize-task}" ;;
  *) REPO_ROOT="" ;;
esac
PACKAGE_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../runtime/launch.sh"
if [[ ! -f "$LAUNCHER" ]]; then
  LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../../runtime/launch.sh"
fi
if [[ ! -f "$LAUNCHER" ]]; then
  LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../../.trellis/guru-team/runtime/launch.sh"
fi
if [[ ! -f "$LAUNCHER" ]]; then echo 'unsupported Skill package root for guru-finalize-task. Guru Team Skill packages are not self-contained or portable. Install or upgrade the complete Guru Team preset.' >&2; exit 2; fi
source "$LAUNCHER" finalize-task-happy-path "$@"
