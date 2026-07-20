#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$PACKAGE_ROOT/../../../../../.." && pwd)"
DISPATCHER="${GURU_TEAM_DISPATCHER:-$REPO_ROOT/.trellis/guru-team/scripts/bash/run-skill-command.sh}"
exec "$DISPATCHER" --package-root "$PACKAGE_ROOT" --validator public_invocation -- "$@"
