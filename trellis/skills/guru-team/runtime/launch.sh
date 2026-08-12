#!/usr/bin/env bash
set -euo pipefail
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  if [[ $# -lt 2 ]]; then
    echo '{"code":"invalid_arguments","field_path":"arguments","remediation":"Invoke launch.sh PACKAGE_ROOT COMMAND_ID [arguments]."}'
    exit 2
  fi
  PACKAGE_ROOT="$(cd "$1" && pwd)"
  COMMAND_ID="$2"
  shift 2
else
  CALLER_SOURCE="${BASH_SOURCE[1]:-}"
  if [[ -z "$CALLER_SOURCE" || $# -lt 1 ]]; then
    echo '{"code":"invalid_arguments","field_path":"arguments","remediation":"Source launch.sh from a package wrapper with COMMAND_ID [arguments]."}'
    return 2
  fi
  PACKAGE_ROOT="$(cd "$(dirname "$CALLER_SOURCE")/.." && pwd)"
  COMMAND_ID="$1"
  shift
fi
case "$PACKAGE_ROOT" in
  */trellis/skills/guru-team/packages/*)
    REPO_ROOT="${PACKAGE_ROOT%%/trellis/skills/guru-team/packages/*}"
    SKILLS_ROOT="${PACKAGE_ROOT%%/packages/*}"
    ;;
  */.trellis/guru-team/skills/packages/*)
    REPO_ROOT="${PACKAGE_ROOT%%/.trellis/guru-team/skills/packages/*}"
    SKILLS_ROOT="$REPO_ROOT/.trellis/guru-team"
    ;;
  */.agents/skills/*|*/.codex/skills/*|*/.cursor/skills/*|*/.claude/skills/*)
    SKILL_ID="${PACKAGE_ROOT##*/}"
    case "$PACKAGE_ROOT" in
      */.agents/skills/*) REPO_ROOT="${PACKAGE_ROOT%%/.agents/skills/*}" ;;
      */.codex/skills/*) REPO_ROOT="${PACKAGE_ROOT%%/.codex/skills/*}" ;;
      */.cursor/skills/*) REPO_ROOT="${PACKAGE_ROOT%%/.cursor/skills/*}" ;;
      */.claude/skills/*) REPO_ROOT="${PACKAGE_ROOT%%/.claude/skills/*}" ;;
    esac
    SKILLS_ROOT="$REPO_ROOT/.trellis/guru-team"
    PACKAGE_ROOT="$SKILLS_ROOT/skills/packages/$SKILL_ID"
    ;;
  *)
    echo '{"code":"unsupported_package_root","field_path":"package_root","remediation":"Run the wrapper from a canonical, installed, or declared platform projection package."}'
    exit 2
    ;;
esac
if [[ ! -f "$SKILLS_ROOT/runtime/command.py" ]]; then
  echo '{"code":"runtime_dependency_missing","field_path":"runtime","remediation":"Install the complete compatible Guru Team preset runtime."}'
  exit 2
fi
export PYTHONPATH="$SKILLS_ROOT${PYTHONPATH:+:$PYTHONPATH}"
cd "$REPO_ROOT"
exec python3 -m runtime.command "$PACKAGE_ROOT" "$COMMAND_ID" "$@"
