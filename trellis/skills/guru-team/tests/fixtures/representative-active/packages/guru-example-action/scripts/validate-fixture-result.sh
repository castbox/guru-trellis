#!/usr/bin/env bash
set -euo pipefail

test -f "${1:?fixture result path is required}"
