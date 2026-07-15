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
- only the 43 inventory-pinned transitional Trellis entries may be replaced by
  Guru Team overlays; the frozen set cannot expand
- unknown local edits receive `.new` copies instead of being overwritten

The source ownership validator must pass before any preset mutation:

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
```
