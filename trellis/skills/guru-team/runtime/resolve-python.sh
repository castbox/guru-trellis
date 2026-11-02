#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ $# -lt 3 ]]; then
  printf '%s\n' '{"code":"invalid_arguments","field_path":"arguments","dependency":"python-runtime","runtime_identity":null,"remediation":"Use resolve-python.sh REPO ASSETS COMMAND [ARGUMENTS]."}' >&2
  exit 2
fi
REPO_ROOT="$1"
RUNTIME_ASSETS="$2"
shift 2
exec "$SCRIPT_DIR/manage-python.sh" "$REPO_ROOT" "$RUNTIME_ASSETS" --exec-active -- "$@"
