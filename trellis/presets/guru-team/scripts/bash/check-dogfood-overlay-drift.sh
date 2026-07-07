#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
REPO_ROOT="$DEFAULT_REPO_ROOT"

usage() {
  cat <<'USAGE'
Usage: check-dogfood-overlay-drift.sh [--repo <path>]

Compare canonical Guru Team preset overlays with installed dogfood copies in
this repository. The command is read-only and exits non-zero when any overlay
copy is missing or different.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for --repo" >&2
        exit 2
      fi
      REPO_ROOT="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

REPO_ROOT="$(cd "$REPO_ROOT" && pwd)"
OVERLAY_ROOT="$REPO_ROOT/trellis/presets/guru-team/overlays"

if [[ ! -d "$OVERLAY_ROOT" ]]; then
  echo "Missing overlay root: $OVERLAY_ROOT" >&2
  exit 2
fi

missing=0
changed=0

while IFS= read -r source; do
  relative="${source#$OVERLAY_ROOT/}"
  target="$REPO_ROOT/$relative"
  if [[ ! -f "$target" ]]; then
    printf 'MISSING %s\n' "$relative"
    missing=$((missing + 1))
    continue
  fi
  if ! cmp -s "$source" "$target"; then
    printf 'CHANGED %s\n' "$relative"
    changed=$((changed + 1))
  fi
done < <(find "$OVERLAY_ROOT" -type f ! -path '*/__pycache__/*' ! -name '*.pyc' | sort)

if [[ "$missing" -gt 0 || "$changed" -gt 0 ]]; then
  printf 'Dogfood overlay drift detected: %s missing, %s changed\n' "$missing" "$changed" >&2
  printf 'Run trellis/presets/guru-team/scripts/bash/apply.sh --repo %q and inspect any .new/.bak files.\n' "$REPO_ROOT" >&2
  exit 1
fi

echo "Dogfood overlay copies match canonical Guru Team overlays."
