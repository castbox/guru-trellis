# Preset Installer

The managed Guru Team assets retain `schemas/closeout-plan.schema.json` only as
an immutable legacy compatibility asset. Current interfaces, runtime and archive
selection use `schemas/finalization-transaction.schema.json`. Fresh install,
workflow switch/update, and preset reapply must preserve the current transaction,
Draft-to-Ready handshake, `ready_for_merge` route and Merge entry across shared,
Codex, Claude, and Cursor. Recursive `.new`/`.bak` scans and canonical/dogfood
equality include both the current schema and explicit legacy asset.

## Boundary

`trellis/presets/guru-team/scripts/bash/apply.sh` is a Bash wrapper. The
installer logic lives in
`trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`.

The installer copies reusable assets from `trellis/workflows/guru-team/` into
the target repository's `.trellis/guru-team/` directory, installs active
`guru-*` packages into the selected discovery roots, and applies only the three
Guru-owned explicit finish entries from
`trellis/presets/guru-team/overlays/`. It never installs or managed-upgrades an
upstream-owned `trellis-*` path.

It also installs the managed finish-summary schema, materializes top-level
`session_auto_commit: false`, and adds `.trellis/workspace/` to the target root
`.gitignore`. It does not create, scan, translate, or rewrite workspace
journal/index files.

Before `install_assets()` creates the target `.trellis/guru-team/` directory or
performs any other target mutation, it must run the source ownership validator
defined in [upstream-ownership.md](./upstream-ownership.md). The validator is
read-only and source-repository scoped; it is not installed into business
repositories or exposed as a workflow/Skill runtime command. It validates the
current-only ownership schema 3.0, exactly 11 Guru-owned rules, nine managed
claims, three additive overlay files, and the live registry/package identities
before installer staging. A non-current ownership contract fails closed.

## Managed Assets

Before staging managed assets, preset apply prepares an immutable Python runtime
under the current OS user's Guru Team cache. It activates only after staged
source/installed validation succeeds. Activation writes a repository-private
default pointer below Git common-dir, not a checkout-local venv. New linked
worktrees inherit that default; an applied linked checkout writes a worktree-gitdir
override so different checkout contracts select their exact coexisting cache
entry. Runtime identity includes dependency-lock,
Python implementation/minor, OS, architecture, ABI/platform tag, runtime API and
layout. Existing checkout-local runtimes are preserved during migration and are
never deleted by normal apply/reapply. A failed cache candidate or staged
activation leaves the previous pointer unchanged.

The complete throwaway verifier has one narrower interpreter-routing contract.
Its canonical `bootstrap.py` invocation is the only shell-level call that may
resolve and execute PATH Python. The returned `source-managed-runtime.json` is
immediately consumed through the canonical source `resolve-python.sh`. Every
later Python subprocess uses either that source runner or the target checkout's
installed `.trellis/guru-team/runtime/resolve-python.sh`; target, linked-worktree,
closeout, update/reapply, and no-developer evidence must never use the source
interpreter as a substitute. Each checkpoint binds the normalized managed
`sys.executable` launch path while preserving the final `venv/bin/python`
symlink, its separately resolved physical interpreter identity, the active
pointer/runtime metadata identity, and the SHA-256 of the selected runtime's
dependency lock.

The eval adapter graph is part of that same routing boundary. Its shell adapter
enters `native_adapter.py` through the checkout-local resolver;
`native_adapter.py` then starts `guru-team-shared-eval` with the current managed
`sys.executable`, never by executable shebang dispatch. The shared evaluator has
no PATH shebang. Source owner staging likewise invokes the canonical Python
preset installer with that same `sys.executable`; it must not execute `apply.sh`
and reopen a PATH-Python second hop.

Verifier-executed workflow, preset, package, and platform shell wrappers are
part of the caller inventory before the checker decides whether they currently
enter Python. Package and platform rows bind the actual invocation path to the
canonical package wrapper, its fixed command in `commands.json`, the installed
`runtime/launch.sh`, and that launcher's exact `resolve-python.sh` hop. A wrapper
that enters Python must use the resolver matching its source or installed
layout. Installed `finish-work.sh`, compatibility `prepare-task.sh`, package
validators, and platform `invoke.sh` entries therefore cannot invoke PATH
Python before their package-local entry.

The inventory also scans every canonical
`trellis/skills/guru-team/packages/*/runtime/**/*.py` file as the installed
package-runtime closure. A package runtime may start another Python process
only with its current managed `sys.executable`. The checker recognizes the real
`run`, `run_stdout`, `subprocess.run`, and `owner.run` call shapes and explicitly
registers the current dynamic validation helper. Literal PATH Python and PATH
Python shebangs in those supported maintenance paths fail closed. Every accepted
package-runtime second hop remains an explicit inventory row.

The preset also maintains one bounded AI-first principles block in the target
root `AGENTS.md`, delimited by stable start/end markers. Missing `AGENTS.md` is
created; an existing file keeps every byte outside the block; repeated apply is
idempotent; and one well-formed older block is replaced in place. Duplicate,
unbalanced, embedded, or out-of-order markers fail closed before target
activation. The installer reports this operation as `agents_principles` in its
JSON result. `AGENTS.md` remains user-owned and is deliberately absent from
`install.managed_assets`; the bounded block is the only preset-owned region.

Public workflow skill packages are a separate managed-hash domain. The preset
validates `trellis/skills/guru-team/`, installs its registry/schema/active
packages under `.trellis/guru-team/skills/`, and distributes active package
bytes to `.agents/skills/<id>/` plus only the selected Codex/Cursor/Claude
roots. Planned ids and test fixtures are never installed.

The three additive platform entries use their own top-level `overlays`
provenance domain in `.trellis/guru-team/extension.json`. Its closed fields are
`schema_version`, `status`, `selected_platforms`, `files`, `removals`,
`conflicts`, and `sidecars`. `files[]` is the complete current selected-entry
inventory and records path, canonical source, managed hash, executable bit, and
install action. This domain, rather than the flat `install.managed_assets`
inventory or an entry marker/text match, is the current ownership authority.

Every existing installed manifest must contain the complete current `overlays`
domain. Missing, malformed, or incomplete provenance fails closed. The
installer does not infer overlay ownership from `install.managed_assets`, entry
markers, or content text, and platform shrink removes only a target whose bytes
match its recorded `previous_managed_sha256`.

Skill files use the exact previous hash recorded in
`.trellis/guru-team/extension.json`. Missing files install; canonical-equal
files stay unchanged; a known managed old version produces `.bak` before the
new canonical bytes replace it; an unknown edit or invalid/missing provenance
is preserved and receives `.new`. This path must not call
`looks_like_trellis_generated_entry()` or any content heuristic. Any conflict,
drift, invalid provenance, or unresolved sidecar blocks installed validation.
The only recoverable conflict provenance is a known managed upgrade with empty
`conflicts[]` and declared `.bak` sidecars adjacent to current managed
`files[]`. Reapply must preserve and continue reporting backups that still
exist; once the user removes all declared backups, the next reapply may promote
the manifest to `status=ok`. Unknown edits, `.new` sidecars, malformed paths,
and semantic conflicts remain invalid previous provenance.

Platform selection may shrink on reapply. A stale platform file whose bytes
equal its previous managed hash is removed and recorded in `removals[]`; empty
skill-owned directories may then be pruned without removing the platform skill
root. A stale unknown edit or invalid-provenance path is preserved, receives a
deterministic `.new` remediation sidecar when its parent is safe, is recorded in
`conflicts[]`, and forces `status=conflict`. `files[]` contains only current
successfully managed files, and installed validation derives the complete
expected inventory independently.

The same previous-manifest hash rule applies when the closed shared-kernel
inventory retires a file below `.trellis/guru-team/runtime/`. An exact managed
copy is removed and recorded; an unknown local edit is preserved with a `.new`
remediation sidecar and blocks activation.

Overlay conflicts participate in the same staged activation gate as package and
current ownership conflicts. Missing selected entries install, canonical-equal
entries remain unchanged, and only an exact previous managed hash may be
upgraded after writing `.bak`. Unknown/invalid provenance preserves the target
and writes `.new`. A transaction with overlay conflicts or unresolved sidecars
does not publish the staged repository; the installed validator independently
checks selected and unselected disk state, hash/mode provenance, removals, and
the exact `.new`/`.bak` inventory.

Before any public skill read/write/remove, validate lexical repo containment
and use `lstat` on every target component. Any target or ancestor symlink,
including dangling, internal, external, and multilevel chains, fails closed.

The atomic current package inventory includes the Interface 1.4 additive
`skill_input_authoring_seed` schema shape, thirteen target-owned authoring
examples, the production manifest bindings, the four finalization-family
bindings, and their validator/probe tests. Canonical, installed, shared, Codex,
Cursor, and Claude copies must carry byte-identical contracts; a graph that has
only part of those thirteen handoffs is a mixed package activation and must fail
before target mutation.

Installed package validation parses the installed workflow target declarations
as well as invoke/exit markers. Every `skill` consumer must resolve to an active
or planned installed registry id. Active consumers require their complete
installed package; planned consumers have no package and stop at the
missing-Skill gate until promoted. Planned invoke/exit markers are invalid.
Every `workflow` / `stop` consumer must resolve to one matching-kind
`guru-workflow-target` / `guru-stop-target` marker. Missing, unknown, multiple,
kind-mismatched, or dangling targets block installation/runtime use.

The production registry installs the active `guru-create-task-commit` package
to the audited runtime root and selected shared/Codex/Cursor/Claude discovery
roots. Its artifact schema,
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

The registry also installs active semantic `guru-discover-change-context` to
the audited runtime root and selected shared/Codex/Cursor/Claude discovery
roots. Its managed tree includes `SKILL.md`, interface, contract, the
active `guru-stage0-discover-change-context-input-pre-task-2.0` and
`guru-change-context-owner-result-3.0` schemas/examples, retained immutable
legacy input 1.0 / owner-result 2.0 assets, public schemas/examples, tests, and
executable dispatcher-only wrappers. Managed companion assets include
`preview-change-context-history.sh`, `record-context-discovery.sh`, and
`check-context-discovery.sh`; the extension manifest publishes the active id,
owner-result schema id, and all three runtime command ids. Installed validation
must prove exact bytes, executable modes, package/interface/tree digests and
selected-platform inventory before direct discovery may run.
Managed schema/runtime/tests must move together when duplicate candidate facts
gain canonical repo/number/identity/URL/open-state/update-time digest and live
freshness checks, or when the `blocked` exit/Gate state matrix changes; a mixed
old-schema/new-runtime installation is drift and fails installed validation.
The active graph supplies Discovery public input independently from actual Sync
`base_current`; no installer fixture may reconstruct or expose the Sync private
result or its facts digest.
Installed and throwaway checks cover stdin/stdout record/check/invoke, zero
repository writes, minimal public DTO projection, live stale restart, and lazy
same-owner recovery checkpoint consume-and-clean. Upgrade/reapply may not leave
an old owner schema/runtime/wrapper combination or any `.new`/`.bak` sidecar.

The registry also installs active semantic `guru-clarify-requirements` to the
same audited runtime and selected discovery roots. Its managed tree includes
`SKILL.md`, interface, contract, deidentified example,
active current-only `guru-requirements-clarification-2.0` schema, tests, and executable
dispatcher-only record/check wrappers. Companion managed assets are exactly
`record-requirements-clarification.sh` and
`check-requirements-clarification.sh`. No GitHub mutation or issue-creation
executor is installed for this Skill. The extension manifest publishes the
active id, artifact schema, and both runtime command ids as one compatible
versioned capability.

The registry additionally installs active semantic
`guru-review-change-request` and active consumer
`guru-create-task-workspace`. The readiness
managed tree includes Skill/interface/contract, deidentified
`issue-review.json` example, `guru-change-request-review-1.0` schema, tests, and
executable dispatcher-only record/check wrappers. Companion managed assets are
`record-change-request-review.sh` and `check-change-request-review.sh`; both are
stdout-only and install no task/workspace mutation executor. The workspace
package separately installs Skill/interface/contract, plan/result schemas,
deidentified examples, tests, and dispatcher-only wrappers for
`record-task-workspace-plan`, `create-task-workspace`, and
`check-task-workspace-result`. The extension manifest publishes both active
ids, artifact schema ids, stable artifact basename, and all runtime command
ids. Source/installed validation must prove readiness's five exit markers and
the workspace package's three exit markers and exact consumers. No planned
missing-package stop remains.

Guru preset apply, update, and reapply do not read, create, copy, initialize,
restore, or delete `.trellis/.developer` or `.trellis/workspace/**`. A clean
fixture begins from an initialized repository where those official paths are
absent and proves all Guru operations leave them absent. A preservation fixture
begins with existing official identity/journal bytes and proves Guru operations
leave them unchanged. Official Trellis may still create/use those paths outside
the Guru preset contract.

The installed workspace verification invokes the isolated official
`common.task_store.cmd_create` adapter in both fixture shapes. It proves the
reviewed assignee becomes both `task.json.assignee` and `task.json.creator`, the
call-scoped developer accessor does not consume existing identity, and existing
identity bytes remain exact.

Fresh install and update/reapply verification must exercise a selected-platform
standalone wrapper with the full preset runtime. Missing runtime, runtime drift,
or unresolved sidecars must block before fetch. A package-only copy must never
appear to work. The throwaway path also verifies workflow route markers,
stdout-only standalone resolution/result facts, the real workflow
`synced -> guru-discover-change-context -> context_ready ->
guru-clarify-requirements` chain and all six clarification exit consumers,
direct zero/candidate history preview, stdin/stdout record/check/invoke,
pre-task zero-write and exact minimal DTO projection, duplicate projection/digest
recomputation from one search result, live stale restart and base-stale
short-circuit, checkpoint-free active-task normal routing, dirty same-owner
active-task recovery plus consume-and-clean,
bidirectional blocked exit/Gate rejection, clarification workflow/standalone
precondition parity, question/scope/action invariants, zero persisted
authorization fields, stdout-only
pre-task behavior, active-task bindings, the query-only prepare path consuming
the current post-sync digest through the shared resolver/sync core, and the
workspace Skill's independent mutation-time freshness checks, `trellis update`,
workflow re-selection, preset reapply, and a final recursive zero-sidecar scan.

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

A fresh target may omit this file. Once present, only the complete current
installed-manifest schema 2.0 is accepted. Non-current schema versions,
missing/extra top-level fields, or malformed current provenance fail closed
before target mutation.

The business Finalizer may consume this current manifest only as immutable
extension-source provenance for its own pre-PR reprepare. It must validate a
canonical repository identity, full commit OID, `tree_state=clean`, and
`is_mutable_ref=false`, then obtain source in a separate detached checkout.
The manifest never makes the business target an extension source checkout and
never transfers standalone verifier ownership. Canonical apply bytes come from
the bound extension source; the apply target remains the business reviewed
checkout. Self-hosted source/target repository equality explicitly binds the
reviewed target commit instead of falling back to an older manifest commit.

When adding user-facing version fields, expose them through `check-env --json`
or `version.sh --json`; scripts may record and validate objective facts, but
must not decide whether an upgrade or rollback is semantically safe.

Stable install and upgrade docs must pin workflow marketplace sources to the
repo release tag that combines the target official Trellis CLI version and Guru
Team revision, for example `gh:castbox/guru-trellis/trellis#v0.6.5-guru.9`.
The preset source must use the same immutable release tag as the workflow
marketplace source; mixing a tag-pinned workflow with `main`, an unpinned source,
or another preset tag is not a stable install or upgrade.
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
the Guru Team Chinese documentation rule. Do not write those exact source
sentences into source-repo `.trellis/spec/**` guidance, because dogfood
installer apply intentionally scans specs for target-project normalization. It
must not scan ordinary historical task directories, rewrite unknown task
content, or translate business `docs/**`; durable docs language is an AI
workflow contract, not an installer rewrite job.

The CLI JSON success payload must expose a `language_guidance` result block with
checked paths, updated paths, replacement count, and the normalized rule. This
is deterministic install evidence only; the script must not judge whether an
unknown document should be translated.

## Current Ownership Gate

The overlay tree is a Guru-only extension surface. It contains exactly the
three `guru-finish-work` entries. The current schema 3.0 inventory contains
exactly 11 anchored Guru-owned rules and nine managed claims. Official
`trellis-*` paths are outside both the overlay tree and the managed inventory.

Before installing Guru-owned assets, the installer validates that exact
current inventory, the extension manifest claims, the three overlay paths, and
the live registry/package graph. A fresh target may have no installed manifest;
an existing target must provide the complete current installed-manifest schema
2.0. Any non-current ownership or installed manifest, unknown claim, broad
upstream namespace, unexpected overlay, malformed provenance, or sidecar fails
closed before target mutation. The installer consumes only the current closed
ownership fields.

Current managed assets still follow their current provenance: missing assets
install, canonical-equal assets remain unchanged, an exact previous managed
hash creates `.bak` before replacement, and an unknown local edit is preserved
with canonical bytes in `.new` when safe. These rules apply only to current
Guru-owned paths.

Do not overwrite unknown current Guru-owned edits. Throwaway verification must
validate the expected workflow preview `.new`, perform the initial switch, run
the selected version upgrade, run `trellis update --dry-run`, then execute
exactly one preserve-mode live update: `trellis update --migrate --skip-all`
when migration is required or `trellis update --skip-all` otherwise. It then
reapplies the marketplace workflow and preset. Successful completion requires
all current ownership conflicts and recursive `.new`/`.bak` sidecars to be
resolved.

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
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
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
  deterministic inventory derived from canonical Guru assets and exactly the
  selected Guru-owned Finish entries
- missing/existing `AGENTS.md` receives exactly one current AI-first marker
  block, preserves all user-owned bytes outside it, refreshes an older block,
  remains byte-identical on reapply, and fails closed on malformed/duplicate
  markers; root `AGENTS.md` never enters `install.managed_assets`
- managed companion assets update and produce `.bak`
- unknown Guru-owned entry edits produce `.new`
- ownership schema 3.0 has exactly 11 Guru-owned rules, nine managed claims,
  and three additive overlays; a non-current ownership or installed manifest
  fails current-contract validation before mutation
- scripts remain executable
- `.codex/prompts/guru-finish-work.md`,
  `.claude/commands/guru/finish-work.md`, and
  `.cursor/commands/guru-finish-work.md` are installed from canonical bytes,
  are the complete additive overlay set, and route only through the live
  workflow and three stable Finish Skill ids
- `language_guidance` reports checked/updated `.trellis/spec/**` and bootstrap
  paths without modifying business `docs/**` or `.trellis/workspace/**`
- throwaway validation fails if `.trellis/spec/**` or
  `00-bootstrap-guidelines` still contain known English documentation language
  requirements
- the already-installed `finish-work.sh` completes dry-run digest, formal draft
  binding, official archive, local/remote/PR HEAD equality, ready transition,
  and clean-tree assertions both before and after update/reapply; the verifier
  must not copy canonical workflow/scripts/schemas into the target fixture
- the installed `test_finish_family_integration.py` passes before and after
  update/reapply, including 13 Finish exits, six route groups, platform entry
  bytes, terminal eval execution, and private/public boundary assertions

## Common Mistakes

- Adding a new companion script but forgetting `MANAGED_ASSET_PATHS`.
- Updating overlays but not the preset README installed-file list.
- Treating `.new` as success without telling the user to review it.
- Copying assets from installed target directories instead of the canonical
  workflow source under `trellis/workflows/guru-team/`.

## Skill Evaluation Assets

Canonical eval schemas, adapter descriptors/wrappers, public command wrappers,
and the package-local kernel live under `trellis/`. The preset installs the
complete active package tree below `.trellis/guru-team/skills/packages/` and
the shared kernel below `.trellis/guru-team/runtime/`. Shared/Codex/Claude/
Cursor discovery roots receive only the public projection: `SKILL.md`,
interface, references, public schemas/examples/evals and the public invocation
wrapper. They never receive package `runtime/`, `tests/`, `errors/`, private
artifact schemas/examples, or recorder/checker/execute wrappers.

The shared kernel installation inventory is closed. Compatibility facts for
extension version/provenance, workflow environment, and planning-document
resolution install through their owning active packages and declared validator
wrappers; they are not shared-kernel commands. Source validation rejects a
workflow compatibility wrapper that points to an undeclared package wrapper,
and installer tests reject any extra kernel file.

Every installed adapter descriptor names an executable in the same
`adapters/eval/` directory. Apply and installed validation require that file to
be regular and executable; the runner may not bypass the managed executable
with a machine-local hidden environment override. The shared adapter runtime
and all four thin wrappers are therefore part of fresh-install and
update/reapply inventory, not documentation-only descriptors.
`skill-eval-native-trace.schema.json`, the adapter response schema, and the
shared native adapter runtime are one managed protocol version: canonical,
fixture, installed, dogfood, and selected-platform checks must reject a partial
update.
That runtime stages a repo/package-external public-only package projection and
keeps canonical adapter request, corpus locator, and private runtime outside
native execution. Fresh-install and update/reapply tests prove the projection
omits `evals/`/private runtime on all four adapters while exact Skill/wrapper
bytes and the public invocation boundary still execute.

Apply, installed validation, and throwaway update/reapply verify every managed
eval file digest/mode and reject missing, unexpected, drifted, symlink-backed,
or sidecar state. Normal install/update never moves eval corpus into workflow
prompt context or ordinary Skill invocation payloads.

## Current Intake Package Activation

The preset installs only the live six-package/23-exit Intake contract,
including optional `guru-sync-base.repo_root` / `route` scalar arguments. The
six production packages, five-stage transition family, call-local invocation
envelopes, current public and consumer schemas/examples, package wrappers,
shared runtime, registry, extension/activation manifests, eval corpora, and
selected platform copies are one versioned activation unit. Source staging
validates the complete unit before target mutation, and installed validation
runs immediately after apply. Failure preserves the prior complete graph and
reports conflicts or sidecars; it must not leave a partially updated or mixed
old/new Intake graph.

The installed normal route invokes only the `guru-sync-base` public wrapper for
authoritative synchronization, carries `base_current`, `context_current`,
`clarity_current`, `wording_current`, and `readiness_current` call-locally, and
has zero production references to repo-local owner/prerequisite locators.
Compatibility locator assets may be staged only when declared by the current
inventory and must not appear in workflow, production eval, or throwaway happy
path examples.

Published 1.0 Phase 0 schema/example paths remain immutable legacy inventory.
Current Interfaces select new versioned contracts where a required transition
or provenance field was added; staging validates both the selected current graph
and retained legacy bytes. Reapply never rewrites a legacy path into the new
shape, and no migration may synthesize missing current identity from live state.

The transaction includes the executable shared native evaluator and preserves
its mode. Interface 1.4 accepts explicit boolean scalar `required`; the staged
`guru-sync-base` package marks `repo_root`, `base_branch`, and `route` optional,
and fresh/current-update probes execute explicit and omitted paths through the
same resolver.

A fresh target or a complete current installed manifest is the only accepted
input. A non-current installed manifest fails closed before staging. Reapply
replaces the complete six-package activation unit. Fresh install, current update,
`trellis update`, and repeated preset apply all end with the same manifest,
registry, extension, package, corpus, and selected-platform bytes and modes.
The verifier scans recursively for `.new` and `.bak` after each transition.
Clean throwaway installation runs the actual-stdout six-Skill transcript; an
isolated package test or handwritten intermediate DTO does not prove activation.
Its Sync-to-Discovery edge invokes the real Sync public wrapper, applies the
declared projection, invokes Discovery with input 2.0 plus actual
`base_current`, and projects actual `context_ready` to Clarify. Product Python
checks use source/installed managed resolvers or those public wrappers; PATH
Python dependency imports are not product-runtime evidence.

## Production Skill Atomic Activation

`production-current-v4` is the sole current planning/check/commit/qualification
contract. The preset stages its schema, manifest, four complete package trees, consumer
schemas, registry, extension inventory, installed provenance, and selected
platform copies in one transaction. The transaction validates the complete
current package graph before publishing any destination; only the current
contract manifest and its declared assets are installed. Update/reapply accepts
only the complete current manifest and reproduces
identical canonical, installed, shared, Codex, Cursor, and Claude bytes and
executable modes without `.new` or `.bak` sidecars.

## Branch Review Package Activation

`guru-review-branch` is an additive active package installed in the same preset
transaction as registry, extension inventory, shared consumers, Interface
schema, runtime, workflow and selected platform copies. It extends the active
closure to ten Skills and 39 exits without changing the then-current legacy
production manifest's three-Skill/11-exit membership. The current v4 manifest
includes qualification and the current
committed consumer/projection binding and four authoring-seed edges.

The current installation includes both active packages and routes Branch Review
`passed` through the five continue entries to the active publication owner. The
finalizer package is directly discoverable, globally invoked after
publication `ready`, and reached through the five thin finish entries. Internal
verification and recovery exits are automatically consumed rather than exposed
as user continuation gates. The combined layer adds the canonical
`guru-finish-work` platform entries and installed integration regression without
changing any package-local public contract.

## Task Publication Package Activation

`guru-review-task-publication` is installed as an additive active Interface 1.4
package together with its registry row, active `guru-finalize-task` consumer
identity, consumer schemas, runtime commands, extension inventories, canonical
workflow markers, installed shared package, and selected Codex/Cursor/Claude copies.
Fresh install, update, and reapply require byte- and executable-mode identity
for the package's Skill, Interface, references, schemas, examples, wrapper,
tests, and canonical eval corpus.

The activation contributes to the current package closure of twenty-one active
Skills and 89 external exits.
`production-current-v4` remains exactly four Skills and 15 exits; #116 is an
additional complete active Interface 1.4 row outside that manifest. The current Branch Review
`passed` DTO feeds the target-owned `publication_review` authoring seed.

The preset transaction does not install any `trellis-continue` payload. Initial
PR payload authoring and the integrated `ready -> guru-finalize-task` route are
owned by the Publication package, marketplace workflow, and active public
package graph. The installed asset inventory contains no task-local body/index
template, reader, writer, fixture, or CLI compatibility flag. It distributes
the current readiness/ready/Finalizer input 4.0 schemas, transaction 1.0,
finish-summary 2.0, and explicit legacy closeout-plan 3.0 asset together.

Clean throwaway install and post-`trellis update` preset reapply both run
source/installed validation, workflow marker and consumer uniqueness checks,
real wrapper/eval smoke, selected-platform byte identity, upstream ownership,
dogfood drift, and recursive zero `.new`/`.bak` checks. Business finish-work has
no extension-verification gate.
Update/reapply tests also reject any retained retired publication asset and
prove legacy 3.0 DTOs fail closed rather than being silently upgraded.

Focused Finalizer recovery validation may project the current installed package
into an isolated clean Git fixture without running the complete marketplace,
official-update, preset-reapply, or tag-pinned release matrix. It must exercise
the installed package bytes for post-bind recovery and historical tracked-plan
retirement; it is scoped evidence and never substitutes for the cumulative
release verifier.

## Extension Installation Verification Package Activation

`guru-verify-extension-installation` remains the standalone-only active
package with Interface 1.5 and
`workflow_integration_state=standalone_only`. Its current inventory contains one
`source_repository_verification` input, `verified|blocked` outputs, ignored
source-session private state, a two-case corpus, thin wrappers, runtime commands,
and direct standalone stop consumers. It has no global workflow marker or
Finalizer projection.

The installed verifier package also carries execution facts schema 5.0 and the
matrix failure projection contract. Canonical, installed, shared, Codex,
Cursor, and Claude copies must agree on parser/schema/example bytes. Focused
tests may inject bounded failures, but preset activation must not claim the full
release matrix was executed.

The preset installs execute/record/check/invoke companion commands before the
package becomes discoverable. These commands are usable only after source
preflight proves canonical `castbox/guru-trellis` assets, credential-free
`origin`, requested ref resolution, current HEAD, and clean tree. Rejection must
happen before clone, tempdir creation, installer execution, artifact write, or
mutation. No target installed manifest, task path, business changed path, or
Finalizer plan can satisfy this entry contract.

Fresh install, upgrade, `trellis update`, and preset reapply validate canonical,
installed, shared, Codex, Cursor, and Claude package/corpus byte identity,
wrapper executable modes, the twenty-one-Skill/89-exit package closure, the
integrated business closure of 20 invokes, 87 exits, 33 workflow targets, and
21 stop targets, and current
ownership schema 3.0 with 11 rules, nine managed claims, and three overlays.
Unknown edits and sidecars retain the existing managed-hash remediation.

## Task Finalization Package Activation

`guru-finalize-task` is installed as an additive active Interface 1.4 package
with four current public input profiles, six output contracts, current gate
5.0, transaction 2.0, real-wrapper eval corpus, and deterministic runtime
wrappers. Canonical, installed shared, Codex, Cursor, and Claude package/corpus
bytes remain identical and wrappers retain executable mode. Legacy aggregate,
gate, transaction, verification re-entry, and closeout-plan assets remain
immutable but are absent from current inventories and routes.

Business content push proceeds directly to Draft PR, archive, Ready, and Merge.
Finalizer does not invoke verifier, emit `verification_required`, accept
verification re-entry, read owner state, or archive a task-local verifier result.
The current archive contains exactly six durable files. Publication retains its
own `return_to_task_work` route for actual content drift.

Installed Finalizer provenance reprepare resolves the manifest-bound canonical
extension repo/ref/commit into a separate exact-OID detached clean source
checkout, invokes its preset entry with the business reviewed checkout as
`--repo`, and commits only the binding-aware manifest tail in the business
lineage. Self-hosted targets use the same closed binding contract with source
commit equal to reviewed HEAD. This package-local behavior adds no installed
managed claim, public profile, exit, transaction state, or verifier route.

The complete source/installed package graph contains twenty-one active Skills and
89 exits. The global business workflow projection is 20 invokes, 87 exits,
33 workflow targets, and 21 stop targets. The preset additionally installs the three Guru-owned
`guru-finish-work` entries and combined integration suite; those entries route
only Publication, Finalizer, and Merge. Upstream `trellis-finish-work` assets
remain under official Trellis ownership.
