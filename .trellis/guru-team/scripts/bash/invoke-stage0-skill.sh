#!/usr/bin/env bash
set -euo pipefail
cat >&2 <<'EOF'
invoke-stage0-skill is package-owned after the package-local runtime migration. Invoke the selected Skill package's public scripts/invoke.sh wrapper so command ownership is explicit.
EOF
exit 2
