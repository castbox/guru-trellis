# Implementation Plan

1. Read the installer, installed/source validators, package contract and
   quality guidance; identify the existing public-file and stale-removal helpers.
2. Add a canonical installed-package public projection helper and use it for
   installed package files, package tree hashes, managed source projections and
   manifest inventory.
3. Extend installed validation to reject package-private tests in installed
   package roots while keeping source validation and platform filtering intact.
4. Add focused installer/validator tests for fresh install, historical removal,
   local-edit conflict/sidecar, inventory parity, and source-versus-installed
   reporting.
5. Update package contract and preset workflow specs with the package-private
   boundary and validation ownership.
6. Reapply the preset in the dogfood checkout, verify no managed sidecars remain,
   and run source/package/installed targeted checks plus task validation.

## Expected files

- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/skills/guru-team/runtime/validate.py`
- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/python/test_preset_transaction_installer.py`
- relevant preset/workflow spec and generated dogfood manifest/projections

## Verification

- Canonical package tests and source package validator.
- Focused installer/transaction/installed validator tests.
- Temporary business-repository fresh install and reapply checks.
- `check-dogfood-overlay-drift.sh`, task validation, and `git diff --check`.
