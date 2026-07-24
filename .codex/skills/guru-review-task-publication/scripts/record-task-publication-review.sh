#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-review-task-publication}"
DISPATCHER="${GURU_TEAM_DISPATCHER:-$REPO_ROOT/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator publication_review_recorder -- "$@"
