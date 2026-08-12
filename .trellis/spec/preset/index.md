# Guru Team Preset Specs

Use these specs when changing:

- `trellis/presets/guru-team/scripts/`
- `trellis/presets/guru-team/overlays/`
- `trellis/presets/guru-team/README.md`
- installer behavior that copies `trellis/workflows/guru-team/` assets into a
  target repository

## Pre-Development Checklist

1. Read [installer.md](./installer.md).
2. Read [upstream-ownership.md](./upstream-ownership.md) before changing any
   overlay, public managed-path claim, or preset mutation entrypoint.
3. Read [overlay-guidelines.md](./overlay-guidelines.md) for platform command or skill changes.
4. Read `.trellis/spec/workflow/workflow-contract.md` when changing user-facing workflow steps.
5. Run the validation commands in `.trellis/spec/workflow/quality-guidelines.md`.

## Local Architecture

The preset does not run `trellis init` and does not install the marketplace
workflow. It installs companion assets and platform overlays into an already
initialized Trellis project.

Primary files:

- `trellis/presets/guru-team/scripts/bash/apply.sh`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/overlays/`
- `trellis/presets/guru-team/ownership/`
- `trellis/workflows/guru-team/`

## Expected Installer Behavior

The installer is idempotent:

- identical files are skipped
- missing managed files are installed
- changed managed companion assets are updated with `.bak` backups
- existing `.trellis/guru-team/config.yml` is preserved
- ownership inventory schema 3.0 contains exactly 11 current Guru rules, nine
  managed claims, and three additive overlays
- existing ownership or installed manifests must satisfy the current schema;
  non-current input fails current-contract validation before mutation
- the overlay tree contains only the three Guru-owned `guru-finish-work` entries
- unknown local edits receive `.new` copies instead of being overwritten
- the six-package/23-exit Phase 0 graph, five closed transition stages,
  call-local envelopes, package runtimes, minimal shared kernel, and activation manifest install as one
  versioned unit; mixed old/new activation fails closed
- clean install/update/reapply verifies the actual-stdout public graph, single
  authoritative sync, platform/dogfood parity, and recursive zero sidecars

The source ownership validator must pass before any preset mutation:

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
```
