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

## Extension Version Manifest

`trellis/guru-team-extension.json` is the canonical source for the Guru Team
extension version. It is separate from the official Trellis CLI version,
`.trellis/.version`, and `trellis/index.json.version`, which is the marketplace
index schema version.

The preset installer must write `.trellis/guru-team/extension.json` into target
repositories on every apply. That installed manifest is an install provenance
record, not user configuration:

- overwrite it with the current deterministic install facts instead of writing
  `.new`;
- include extension id, SemVer version, workflow template id, source repo/ref,
  source commit when available, source tree state, selected platforms, and
  install timestamp;
- do not record tokens, GitHub auth details, `.env` contents, signed URLs, or
  unnecessary local-only source paths;
- tolerate source directories that are Git archives or lack `git` by recording
  `archive` / `unknown` provenance instead of failing the install.

When adding user-facing version fields, expose them through `check-env --json`
or `version.sh --json`; scripts may record and validate objective facts, but
must not decide whether an upgrade or rollback is semantically safe.

Stable install and upgrade docs must pin workflow marketplace sources to the
repo release tag that matches the canonical extension version, for example
`gh:castbox/guru-trellis/trellis#v0.6.5`. Keep `trellis/index.json.version` as
the marketplace index schema version; do not reuse it as the Guru Team
extension release number. If validation samples unpinned
`gh:castbox/guru-trellis/trellis`, report it as latest/canary sampling rather
than release-tag verification.

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

## Platform Overlay Selection

### 1. Scope / Trigger

Changing the preset installer platform flags changes the public install command
contract and the overlay files copied into target repositories.

### 2. Signatures

The supported installer platform flags are:

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo <repo> \
  [--platform codex] [--platform cursor] [--platform claude]

trellis/presets/guru-team/scripts/bash/apply.sh --repo <repo> --all-platforms
```

### 3. Contracts

- With no `--platform` and no `--all-platforms`, install shared `.agents/skills`
  overlays plus Codex and Cursor overlays.
- `--platform <name>` is repeatable and installs shared overlays plus exactly
  the selected platform overlay groups.
- `--all-platforms` installs shared overlays plus every known platform overlay.
- `--platform` and `--all-platforms` are mutually exclusive.
- Unknown platform names fail closed; do not silently ignore them.
- Shared `.agents/skills` overlays are always installed because Codex and some
  agentskills-compatible tools depend on the shared skill layer.

### 4. Validation & Error Matrix

| Condition | Expected behavior |
| --- | --- |
| no platform flags | install `.agents/`, `.codex/`, `.cursor/`; do not create `.claude/` |
| repeated `--platform codex --platform cursor` | install `.agents/`, `.codex/`, `.cursor/`; do not create `.claude/` |
| `--platform claude` | install `.agents/` and `.claude/`; do not create `.codex/` or `.cursor/` |
| `--all-platforms` | install `.agents/`, `.codex/`, `.cursor/`, `.claude/` |
| `--platform codex --all-platforms` | argparse exits non-zero |
| `--platform unknown` | argparse exits non-zero |

### 5. Good/Base/Bad Cases

- Good: README default install uses `trellis init --codex --cursor` and
  `apply.sh --platform codex --platform cursor`.
- Base: Maintainers use `apply.sh --repo . --all-platforms` only when dogfood
  overlay copies must include every canonical overlay.
- Bad: Installer recursively copies all platform overlays after a Codex +
  Cursor init and relies on an AI prompt to delete `.claude/` later.

### 6. Tests Required

- Unit tests for default platform selection, repeated platform flags,
  `--platform claude`, `--all-platforms`, mutual exclusion, and invalid
  platform names.
- Temporary repo behavior test or throwaway install validation that asserts the
  default Codex + Cursor path does not create `.claude/`.
- README/preset README command review whenever platform flags change.

### 7. Wrong vs Correct

#### Wrong

```bash
apply.sh --repo "$PWD"
# Then ask the AI to remove .claude/ if it was not selected.
```

#### Correct

```bash
apply.sh --repo "$PWD" --platform codex --platform cursor
```

## Validation

At minimum:

```bash
bash -n trellis/presets/guru-team/scripts/bash/apply.sh
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
```

For behavioral changes, run the installer against a temporary Trellis project
or disposable copy and verify:

- throwaway `trellis init` verifies the current branch's workflow marketplace
  source; if Trellis CLI cannot address the current branch as a marketplace
  source, the verification script must fail closed or the final report must
  explicitly say only the public remote marketplace was sampled
- existing-project `trellis workflow --marketplace ... --create-new` preview
  and forced switch paths can read the Guru Team workflow
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
