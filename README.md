# Guru Trellis

Guru Team Trellis marketplace and preset assets.

This repository is the public canonical source for the reusable `guru-team`
Trellis workflow. It contains:

- `trellis/index.json`: Trellis marketplace index.
- `trellis/workflows/guru-team/`: workflow, config template, schemas, and
  companion scripts.
- `trellis/presets/guru-team/`: installer for companion scripts and platform
  entry overlays.

## Install

For a new project:

```bash
trellis init -u <name> --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis
```

Then install Guru Team companion assets:

```bash
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project
```

For an existing Trellis project, preview before switching:

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis \
  --template guru-team \
  --create-new
```

After review, switch and reapply the preset:

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis \
  --template guru-team
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project
```

## Upgrade

Use Trellis upstream update and Guru Team updates separately:

```bash
trellis upgrade
trellis update --dry-run
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis \
  --template guru-team \
  --create-new
```

Review `.trellis/workflow.md.new`, switch when appropriate, then rerun the
preset installer. The preset is idempotent: identical files are skipped,
recognized upstream-generated entries are replaced by Guru Team overlays, and
unknown local changes are preserved as `.new` files.
