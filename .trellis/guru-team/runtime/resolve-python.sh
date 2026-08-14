#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  printf '%s\n' '{"code":"invalid_arguments","field_path":"arguments","dependency":"python-runtime","runtime_identity":null,"remediation":"trellis/presets/guru-team/scripts/bash/apply.sh --repo ."}' >&2
  exit 2
fi
REPO_ROOT="$1"
RUNTIME_ASSETS="$2"
shift 2
REMEDIATION="trellis/presets/guru-team/scripts/bash/apply.sh --repo ."

runtime_error() {
  local code="$1"
  local dependency="$2"
  local identity="${3:-null}"
  printf '{"code":"%s","field_path":"runtime","dependency":"%s","runtime_identity":%s,"remediation":"%s"}\n' \
    "$code" "$dependency" "$identity" "$REMEDIATION" >&2
  exit 2
}

STATE_ROOT="$REPO_ROOT/.trellis/.runtime/guru-team/python"
if [[ -d "$REPO_ROOT/.git" ]]; then
  GIT_DIR="$(cd "$REPO_ROOT/.git" && pwd -P)"
  COMMON_DIR="$GIT_DIR"
  STATE_ROOT="$COMMON_DIR/guru-team/python"
elif [[ -f "$REPO_ROOT/.git" && ! -L "$REPO_ROOT/.git" ]]; then
  GIT_DIR_RAW="$(sed -n 's/^gitdir: //p' "$REPO_ROOT/.git")"
  case "$GIT_DIR_RAW" in
    /*|[A-Za-z]:/*) GIT_DIR="$GIT_DIR_RAW" ;;
    *) GIT_DIR="$REPO_ROOT/$GIT_DIR_RAW" ;;
  esac
  GIT_DIR="$(cd "$GIT_DIR" && pwd -P)"
  COMMON_DIR="$GIT_DIR"
  if [[ -f "$GIT_DIR/commondir" && ! -L "$GIT_DIR/commondir" ]]; then
    COMMON_RAW="$(tr -d '\n\r' < "$GIT_DIR/commondir")"
    case "$COMMON_RAW" in
      /*|[A-Za-z]:/*) COMMON_DIR="$COMMON_RAW" ;;
      *) COMMON_DIR="$GIT_DIR/$COMMON_RAW" ;;
    esac
    COMMON_DIR="$(cd "$COMMON_DIR" && pwd -P)"
  fi
  COMMON_STATE_ROOT="$COMMON_DIR/guru-team/python"
  WORKTREE_STATE_ROOT="$GIT_DIR/guru-team/python"
  if [[ -f "$WORKTREE_STATE_ROOT/active.json" && ! -L "$WORKTREE_STATE_ROOT/active.json" ]]; then
    STATE_ROOT="$WORKTREE_STATE_ROOT"
  else
    STATE_ROOT="$COMMON_STATE_ROOT"
  fi
fi

ACTIVE="$STATE_ROOT/active.json"
[[ -f "$ACTIVE" && ! -L "$ACTIVE" ]] || runtime_error runtime_not_bootstrapped python-runtime
ACTIVE_LINE="$(tr -d '\n\r' < "$ACTIVE")"
RUNTIME_ID="$(printf '%s' "$ACTIVE_LINE" | sed -n 's/.*"runtime_id":"\([0-9a-f]\{24\}\)".*/\1/p')"
INTERPRETER="$(printf '%s' "$ACTIVE_LINE" | sed -n 's/.*"interpreter":"\([^"]*\)".*/\1/p')"
case "$INTERPRETER" in
  */"$RUNTIME_ID"/venv/bin/python|*/"$RUNTIME_ID"/venv/Scripts/python.exe) ;;
  *) runtime_error managed_runtime_missing python-runtime "\"$RUNTIME_ID\"" ;;
esac
[[ -f "$INTERPRETER" && -x "$INTERPRETER" ]] || runtime_error managed_runtime_missing python-runtime "\"$RUNTIME_ID\""
if ! VALIDATION_ERROR="$(
  "$INTERPRETER" "$RUNTIME_ASSETS/bootstrap.py" \
    --repo "$REPO_ROOT" \
    --runtime-assets "$RUNTIME_ASSETS" \
    --validate-active "$RUNTIME_ID" --json 2>&1 >/dev/null
)"; then
  if [[ -n "$VALIDATION_ERROR" ]]; then
    printf '%s\n' "$VALIDATION_ERROR" >&2
    exit 2
  fi
  runtime_error runtime_dependency_missing python-runtime "\"$RUNTIME_ID\""
fi
exec "$INTERPRETER" "$@"
