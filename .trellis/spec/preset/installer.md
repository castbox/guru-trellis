# Preset Installer

## Boundary

`trellis/presets/guru-team/scripts/bash/apply.sh` is a Bash wrapper. The
installer logic lives in
`trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`.

The installer copies reusable assets from `trellis/workflows/guru-team/` into
the target repository's `.trellis/guru-team/` directory, then applies platform
overlays from `trellis/presets/guru-team/overlays/`.

## Managed Assets

`MANAGED_ASSET_PATHS` is the authoritative list of companion assets copied from
the workflow source. When adding a companion script, schema, or managed config
template:

1. Add the file under `trellis/workflows/guru-team/`.
2. Add the relative path to `MANAGED_ASSET_PATHS`.
3. Add executable permission handling if it is a script.
4. Update `trellis/presets/guru-team/README.md` installed-file list.
5. Validate a temporary install or upgrade path.

## Config Preservation

`config-template.yml` is managed and may be upgraded with a `.bak`. Existing
target `.trellis/guru-team/config.yml` must not be overwritten. This allows
business repositories to keep local repo names, workspace mode, branch
preferences, labels, and other configuration.

Do not add installer behavior that silently merges unknown local config values
unless the merge is deterministic, covered by tests or validation, and safe for
older configs.

## Overlay Conflict Handling

Use `copy_overlay()` behavior:

- install missing overlay files
- skip identical files
- replace known Trellis-generated entries detected by
  `looks_like_trellis_generated_entry()`
- write `.new` for unknown local edits

Do not overwrite unknown platform command, prompt, or skill edits. The target
repo owner must inspect `.new` when local customization exists.

## Validation

At minimum:

```bash
bash -n trellis/presets/guru-team/scripts/bash/apply.sh
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
```

For behavioral changes, run the installer against a temporary Trellis project
or disposable copy and verify:

- existing `.trellis/guru-team/config.yml` remains unchanged
- managed companion assets update and produce `.bak`
- unknown overlay edits produce `.new`
- known upstream Trellis-generated entries are replaced
- scripts remain executable

## Common Mistakes

- Adding a new companion script but forgetting `MANAGED_ASSET_PATHS`.
- Updating overlays but not the preset README installed-file list.
- Treating `.new` as success without telling the user to review it.
- Copying assets from installed target directories instead of the canonical
  workflow source under `trellis/workflows/guru-team/`.
