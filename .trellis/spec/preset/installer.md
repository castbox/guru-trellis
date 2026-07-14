# Preset Installer

The managed Guru Team assets include `schemas/closeout-plan.schema.json`.
Fresh install, workflow switch/update, and preset reapply must preserve the
same finish-work state order, expected-digest flag, draft handshake, and
single-entry recovery text across shared, Codex, Claude, and Cursor entries.
Recursive `.new`/`.bak` scans and canonical/dogfood equality include the new
schema and finish entry content.

## Boundary

`trellis/presets/guru-team/scripts/bash/apply.sh` is a Bash wrapper. The
installer logic lives in
`trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`.

The installer copies reusable assets from `trellis/workflows/guru-team/` into
the target repository's `.trellis/guru-team/` directory, then applies platform
overlays from `trellis/presets/guru-team/overlays/`.

It also installs the managed finish-summary schema, materializes top-level
`session_auto_commit: false`, and adds `.trellis/workspace/` to the target root
`.gitignore`. It does not create, scan, translate, or rewrite workspace
journal/index files.

## Managed Assets

Public workflow skill packages are a separate managed-hash domain. The preset
validates `trellis/skills/guru-team/`, installs its registry/schema/active
packages under `.trellis/guru-team/skills/`, and distributes active package
bytes to `.agents/skills/<id>/` plus only the selected Codex/Cursor/Claude
roots. Reserved ids and test fixtures are never installed.

Skill files use the exact previous hash recorded in
`.trellis/guru-team/extension.json`. Missing files install; canonical-equal
files stay unchanged; a known managed old version produces `.bak` before the
new canonical bytes replace it; an unknown edit or invalid/missing provenance
is preserved and receives `.new`. This path must not call
`looks_like_trellis_generated_entry()` or any content heuristic. Any conflict,
drift, invalid provenance, or unresolved sidecar blocks installed validation.

Platform selection may shrink on reapply. A stale platform file whose bytes
equal its previous managed hash is removed and recorded in `removals[]`; empty
skill-owned directories may then be pruned without removing the platform skill
root. A stale unknown edit or invalid-provenance path is preserved, receives a
deterministic `.new` remediation sidecar when its parent is safe, is recorded in
`conflicts[]`, and forces `status=conflict`. `files[]` contains only current
successfully managed files, and installed validation derives the complete
expected inventory independently.

Before any public skill read/write/remove, validate lexical repo containment
and use `lstat` on every target component. Any target or ancestor symlink,
including dangling, internal, external, and multilevel chains, fails closed.

The production registry keeps `guru-create-work-commit` reserved and installs
the active `guru-create-task-commit` package to the audited runtime root and
selected shared/Codex/Cursor/Claude discovery roots. Its artifact schema,
package thin wrappers and package tests are part of the managed tree. The
companion `scripts/bash/create-task-commit.sh` is a managed executable asset;
source/installed validation and the manifest inventory must prove its bytes and
mode.

The production registry also installs active `guru-sync-base` to the audited
runtime root and selected shared/Codex/Cursor/Claude discovery roots. Managed
inventory includes its `SKILL.md`, interface, contract, example, result schema,
tests, and executable thin wrappers. Companion managed assets include
executable `sync-base.sh` and `check-base-sync.sh`; the extension manifest
publishes active id `guru-sync-base`, schema id
`guru-base-sync-result-1.0`, and runtime command ids `sync-base` and
`check-base-sync`.

Fresh install and update/reapply verification must exercise a selected-platform
standalone wrapper with the full preset runtime. Missing runtime, runtime drift,
or unresolved sidecars must block before fetch. A package-only copy must never
appear to work. The throwaway path also verifies workflow route markers,
standalone cleanup, the real workflow `synced -> prepare-task` planner/mutation
guard chain using one resolution raw-byte/digest lease, terminal release with
zero result/resolution residue, `trellis update`, workflow re-selection, preset
reapply, and a final recursive zero-sidecar scan.

The shared `scripts/bash/run-skill-command.sh` dispatcher is also a managed
executable asset and stable companion script id. The canonical extension
manifest publishes `public_api.skill_runtime` with the runtime API version,
dispatcher id, and installed manifest path. Preset apply must install the
dispatcher before package discovery copies are usable, include it in
`MANAGED_ASSET_PATHS`, executable handling and the installed managed-asset
inventory, and preserve the exact capability metadata in
`.trellis/guru-team/extension.json`.

Generated Python `__pycache__` directories and `.pyc` / `.pyo` bytecode are not
public package assets. Package source validation, tree digests, installer
inventory and installed validation exclude them; reapply removes an older
managed cache entry by its recorded previous hash instead of redistributing it.

`MANAGED_ASSET_PATHS` is the authoritative list of companion assets copied from
the workflow source. When adding a companion script, schema, or managed config
template:

1. Add the file under `trellis/workflows/guru-team/`.
2. Add the relative path to `MANAGED_ASSET_PATHS`.
3. Add executable permission handling if it is a script.
4. Update `trellis/presets/guru-team/README.md` installed-file list.
5. Validate a temporary install or upgrade path.

For public Skill runtime changes, the temporary path must invoke a wrapper from
the selected shared discovery root after full preset installation, then repeat
the probe after `trellis update`, workflow re-selection, and preset reapply. A
package-only copy, missing dispatcher/manifest, incompatible API, command drift,
or managed-copy drift must fail before the target companion command with the
documented full-preset install/upgrade remediation.

`scripts/bash/backfill-finish-summary.sh` is a managed executable asset. Fresh
install and preset reapply/update validation must prove that the wrapper and
canonical Python subcommand are both present, the wrapper is executable, and
an empty archive can run `--json --dry-run` successfully. Reapply must restore
the managed wrapper without changing user-owned `.trellis/guru-team/config.yml`.

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
  target Trellis CLI, source commit when available, source tree state, selected
  platforms, and install timestamp;
- do not record tokens, GitHub auth details, `.env` contents, signed URLs, or
  unnecessary local-only source paths;
- tolerate source directories that are Git archives or lack `git` by recording
  `archive` / `unknown` provenance instead of failing the install.

When adding user-facing version fields, expose them through `check-env --json`
or `version.sh --json`; scripts may record and validate objective facts, but
must not decide whether an upgrade or rollback is semantically safe.

Stable install and upgrade docs must pin workflow marketplace sources to the
repo release tag that combines the target official Trellis CLI version and Guru
Team revision, for example `gh:castbox/guru-trellis/trellis#v0.6.5-guru.2`.
Keep `trellis/index.json.version` as the marketplace index schema version; do
not reuse it as the Guru Team extension release number. If validation samples unpinned
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

## Language Guidance Normalization

The preset installer may perform deterministic language-rule normalization for
target business repositories after managed assets and overlays are applied. The
allowed scope is limited to:

- `.trellis/spec/**/*.md`
- `.trellis/tasks/00-bootstrap-guidelines/**/*.md`

It must only replace the known Trellis-generated English language-rule
sentences enumerated in the installer's `ENGLISH_LANGUAGE_RULES` constant with
the Guru Team Chinese documentation rule. Do not write those exact legacy
sentences into source-repo `.trellis/spec/**` guidance, because dogfood
installer apply intentionally scans specs for target-project normalization. It
must not scan ordinary historical task directories, rewrite unknown task
content, or translate business `docs/**`; durable docs language is an AI
workflow contract, not an installer rewrite job.

The CLI JSON success payload must expose a `language_guidance` result block with
checked paths, updated paths, replacement count, and the normalized rule. This
is deterministic install evidence only; the script must not judge whether an
unknown document should be translated.

## Overlay Conflict Handling

Use `copy_overlay()` behavior:

- install missing overlay files
- skip identical files
- replace known Trellis-generated entries detected by
  `looks_like_trellis_generated_entry()`
- write `.new` for unknown local edits

Known Trellis-generated entries include Guru Team command/skill overlays and
the shipped `trellis-implement`, `trellis-check`, `trellis-research`,
`implement`, and `check` agent definitions when their content still carries
standard Trellis prelude, JSONL, research, or channel-runtime signals. They
also include generated Codex / Cursor SessionStart hooks, Cursor sub-agent
context injection hooks, bundled `trellis-brainstorm`, `trellis-check`, and
`trellis-before-dev` skills, and Trellis meta planning references such as
`task-system.md`, `context-injection.md`, `change-workflow.md`,
`change-context-loading.md`, and `platform-files/agents.md` when those files
still carry standard Trellis task context signals. Guru Team
replaces those generated surfaces so new installs do not keep stale `PRD-only`,
lightweight-PRD-only, or optional design/implement planning hints after the
canonical workflow has a stricter post-planning approval gate.

Do not overwrite unknown platform command, prompt, skill, or agent edits. The
target repo owner must inspect `.new` when local customization exists.
Throwaway verification must remove the expected workflow preview `.new` after
content validation, run the initial switch, execute `trellis update --force`,
then reapply the marketplace workflow before preset reapply. The second workflow
switch is required because official update may restore the upstream default
workflow. Successful completion requires a final recursive `.new`/`.bak` scan
with no remaining sidecars.

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
- `config-template.yml` remains managed while user-owned `config.yml` is not
  listed in `install.managed_assets`; fresh and repeated apply report the same
  deterministic managed asset set
- managed companion assets update and produce `.bak`
- unknown overlay edits produce `.new`
- known upstream Trellis-generated entries are replaced
- scripts remain executable
- `language_guidance` reports checked/updated `.trellis/spec/**` and bootstrap
  paths without modifying business `docs/**` or `.trellis/workspace/**`
- throwaway validation fails if `.trellis/spec/**` or
  `00-bootstrap-guidelines` still contain known English documentation language
  requirements
- the already-installed `finish-work.sh` completes dry-run digest, formal draft
  binding, official archive, local/remote/PR HEAD equality, ready transition,
  and clean-tree assertions both before and after update/reapply; the verifier
  must not copy canonical workflow/scripts/schemas into the target fixture

## Common Mistakes

- Adding a new companion script but forgetting `MANAGED_ASSET_PATHS`.
- Updating overlays but not the preset README installed-file list.
- Treating `.new` as success without telling the user to review it.
- Copying assets from installed target directories instead of the canonical
  workflow source under `trellis/workflows/guru-team/`.
