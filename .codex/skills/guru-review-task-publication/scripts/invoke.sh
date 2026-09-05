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
PACKAGE_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../runtime/launch.sh"
if [[ ! -f "$LAUNCHER" ]]; then
  LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../../runtime/launch.sh"
fi
if [[ ! -f "$LAUNCHER" ]]; then
  LAUNCHER="$PACKAGE_SCRIPT_DIR/../../../../.trellis/guru-team/runtime/launch.sh"
fi
if [[ ! -f "$LAUNCHER" ]]; then echo 'unsupported Skill package root for guru-review-task-publication. Guru Team Skill packages are not self-contained or portable. Install or upgrade the complete Guru Team preset.' >&2; exit 2; fi
source "$LAUNCHER" invoke-guru-review-task-publication "$@"
