#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
REPO_ROOT="$DEFAULT_REPO_ROOT"

usage() {
  cat <<'USAGE'
Usage: check-dogfood-overlay-drift.sh [--repo <path>]

Validate the current Guru-owned claims and managed asset/package closure, then
compare the canonical Guru Team workflow and finish overlays with installed
dogfood copies in this repository, and verify the managed semantic retrieval
spec exists. These checks provide normal version/drift binding, not an
authenticity boundary. The command is read-only and exits non-zero on ownership
failure or when any managed copy is missing or different.
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
OWNERSHIP_CHECK="$REPO_ROOT/trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh"

if [[ ! -x "$OWNERSHIP_CHECK" ]]; then
  echo "Missing executable ownership validator: $OWNERSHIP_CHECK" >&2
  exit 2
fi

"$OWNERSHIP_CHECK" --repo "$REPO_ROOT" --json

if [[ ! -d "$OVERLAY_ROOT" ]]; then
  echo "Missing overlay root: $OVERLAY_ROOT" >&2
  exit 2
fi

missing=0
changed=0

workflow_source="$REPO_ROOT/trellis/workflows/guru-team/workflow.md"
workflow="$REPO_ROOT/.trellis/workflow.md"
if [[ ! -f "$workflow_source" || ! -f "$workflow" ]]; then
  printf 'MISSING %s\n' ".trellis/workflow.md"
  missing=$((missing + 1))
elif ! cmp -s "$workflow_source" "$workflow"; then
  printf 'CHANGED %s\n' ".trellis/workflow.md"
  changed=$((changed + 1))
fi

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

semantic_spec_source="$REPO_ROOT/trellis/presets/guru-team/spec/workflow/semantic-retrieval.md"
semantic_spec="$REPO_ROOT/.trellis/spec/workflow/semantic-retrieval.md"
if [[ ! -f "$semantic_spec_source" || ! -f "$semantic_spec" ]]; then
  printf 'MISSING %s\n' ".trellis/spec/workflow/semantic-retrieval.md"
  missing=$((missing + 1))
elif ! cmp -s "$semantic_spec_source" "$semantic_spec"; then
  printf 'CHANGED %s\n' ".trellis/spec/workflow/semantic-retrieval.md"
  changed=$((changed + 1))
fi

if [[ "$missing" -gt 0 || "$changed" -gt 0 ]]; then
  printf 'Dogfood workflow/overlay drift detected: %s missing, %s changed\n' "$missing" "$changed" >&2
  printf 'Review the current Guru-owned overlay drift, then run trellis/presets/guru-team/scripts/bash/apply.sh --repo %q and inspect any .new/.bak files.\n' "$REPO_ROOT" >&2
  exit 1
fi

echo "Dogfood workflow and overlay copies match canonical Guru Team sources."
