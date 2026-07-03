# Public Documentation

## Audience and Language

Top-level user-facing docs in this repository are primarily Chinese because
the install/upgrade prompts are intended for Guru Team users. Keep command
names, config keys, file paths, GitHub keywords, and Trellis template ids in
English.

Lower-level script comments and Python docstrings may stay English when they
document implementation mechanics.

## Install and Upgrade Prompts

Prompts in `README.md` are meant to be copied into an AI coding session in a
target business repository. They should tell the AI to:

- confirm the current `@mindfoldhq/trellis` latest version live
- detect conflicting SDD or agent harness frameworks before installing
- use the `guru-team` marketplace workflow source
- apply the preset installer from this public repository
- keep only selected platform entry directories
- run minimal validation
- check for secrets before commit
- do Git publishing preflight before pushing or opening a PR

Do not write prompts that assume direct push to protected branches.

## SSOT Rules

When workflow behavior changes, update the docs that users actually read:

- `README.md` for install/upgrade and daily operation
- `trellis/workflows/guru-team/README.md` for marketplace workflow behavior
- `trellis/presets/guru-team/README.md` for installer behavior and installed files

Do not let README instructions contradict the canonical workflow in
`trellis/workflows/guru-team/workflow.md`.

## Safety

Public docs must not include tokens, private repository URLs that reveal
secrets, signed URLs, `.env` contents, database URLs, or raw provider responses.

## Validation

For docs-only changes:

```bash
git diff --check
rg "publish-pr|review-branch|finish-work|trellis-start|trellis-continue" README.md trellis/workflows/guru-team/README.md trellis/presets/guru-team/README.md
```

When docs mention installed files, compare with the actual overlay and managed
asset lists:

```bash
find trellis/presets/guru-team/overlays -type f | sort
rg "MANAGED_ASSET_PATHS|Installed Files" trellis/presets/guru-team trellis/workflows/guru-team
```
