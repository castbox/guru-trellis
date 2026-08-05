# Upstream Ownership And Removed Overlay Tombstones

This document is the durable semantic source of truth for Trellis/Guru path
ownership. The machine-readable inventory records reviewed facts and historical
migration hashes; it does not replace AI scope or design judgment.

## Final Ownership Categories

Every preset overlay, public managed-path claim, canonical Guru package, and
installed discovery path has exactly one current owner:

- `upstream_owned`: Trellis creates and updates the path. Guru Team must not
  install, claim, patch, delete, or managed-upgrade it.
- `guru_owned`: the path is inside an anchored Guru namespace and is authored,
  distributed, and upgraded by this repository.

`transitional_legacy` and `unclassified` are not valid final states. The source
validator must report zero entries in either state before preset mutation.

## Frozen 43-Path History

`trellis/presets/guru-team/ownership/upstream-ownership.json` retains the exact
43 paths present at base commit
`291b57b6c02872320a4dce0626a2f718399b8f56`. The field name
`legacy_entries` is a compatibility name for this historical table; every row
is now a removal tombstone:

- `category: upstream_owned`;
- `migration_state: removed`;
- unchanged `path`, `baseline_sha256`, `generated_in_clean_init`, upstream
  producer, replacement owners, blocker/removal issue history, and migration
  notes;
- no `current_payload_sha256`;
- `dogfood_status: removed_with_audit_history`;
- `target_business_repo_status: no_longer_installed`.

The immutable historical identity remains the canonical SHA-256 of the 43
sorted `path + baseline_sha256` pairs. Removal must not change the count, path
set, baseline hashes, or immutable identity.

## Migration-Only Payload Provenance

Removing `current_payload_sha256` must not make existing installations
unmigratable. Each tombstone therefore owns a non-empty, unique
`migration_payload_sha256s` list containing every exact historical Guru payload
hash that the installer may recognize for that path, including the baseline
payload and any later reviewed payload when distinct.

This list is consumed only by preset migration and deterministic ownership
validation. It is not a current managed hash, public workflow authority,
authenticity boundary, anti-tamper mechanism, or permission to restore an
overlay. Git history, aggregate digests, content heuristics, and installed
copies are not substitutes for this explicit per-path provenance.

## Canonical Overlay Set

The canonical overlay tree contains exactly three `guru_owned` files:

- `.codex/prompts/guru-finish-work.md`;
- `.claude/commands/guru/finish-work.md`;
- `.cursor/commands/guru-finish-work.md`.

None of the 43 tombstone paths may exist below
`trellis/presets/guru-team/overlays/`. A new upstream namespace overlay is a
contract violation.

## Guru-Owned Namespaces

The exact public managed claims are:

- `.trellis/guru-team/`;
- `.trellis/guru-team/skills/`;
- `.agents/skills/guru-*/`;
- `.codex/skills/guru-*/`;
- `.cursor/skills/guru-*/`;
- `.claude/skills/guru-*/`;
- `.codex/prompts/guru-finish-work.md`;
- `.claude/commands/guru/finish-work.md`;
- `.cursor/commands/guru-finish-work.md`.

Rules are matched by complete anchored path components. They do not authorize a
broad prompt/command/skill directory or any `trellis-*` path.

Canonical `trellis/workflows/guru-team/**`,
`trellis/skills/guru-team/**`, and installed `.trellis/guru-team/**` assets are
Guru-owned source/runtime content even when not all are expressed as platform
managed-path claims.

## Installer Migration State Machine

Before any target mutation, the installer validates this source inventory and
classifies every removed tombstone path using `lstat`, official template
provenance, and `migration_payload_sha256s`:

| Target state | Required behavior |
| --- | --- |
| path missing | Do not create it; record already missing/unmanaged. |
| clean upstream | Preserve exact bytes and remove any old Guru ownership record. |
| upstream-generated path still equals a known Guru payload | Preserve the file and fail closed with official `trellis update`/version-upgrade remediation; the preset must not synthesize upstream bytes. |
| legacy-only path equals a known Guru payload | Remove that exact obsolete file and record the reviewed migration. |
| unknown or locally edited path | Preserve the original, materialize a deterministic `.new` remediation/conflict sidecar when safe, and block activation. |

`generated_in_clean_init=true` distinguishes upstream-generated paths from the
six historical legacy-only paths. The installer may not use
`looks_like_trellis_generated_entry()` or another content heuristic for this
migration.

Successful activation removes all 43 paths from the new installed extension
manifest's `install.managed_assets`. Unresolved `.new`/`.bak`, invalid
provenance, unsafe/symlink paths, or a recognized old Guru payload at an
upstream-generated path keeps the install blocked.

## Update And Upgrade

For an existing repository:

1. run official `trellis update` or the required Trellis version upgrade;
2. reselect the `guru-team` marketplace workflow;
3. reapply the Guru preset;
4. resolve all `.new`/`.bak` and local-edit conflicts;
5. rerun source/installed package validation, ownership validation, platform
   discovery checks, dogfood drift, and a recursive zero-sidecar scan.

Official Trellis owns the bytes of generated `trellis-*` files after update.
The preset restores only Guru-owned assets.

## Deterministic Validator Boundary

Maintainers run:

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
```

The validator is read-only. It may validate schema, 43-path immutable history,
tombstone state, migration payload hashes, overlay presence/absence, exact
Guru-owned claims, registry state, and objective counts/digests. It must not
judge design quality, route intent, finding severity, update safety, or Issue
closure.

Success reports at least:

- `frozen_count=43`, `active_count=0`, `removed_count=43`;
- `legacy_overlay_count=0`, `additive_overlay_count=3`;
- `transitional_legacy_count=0`, `unclassified_count=0`;
- immutable historical identity and migration-payload-set digests;
- exact managed claims and additive overlay identities.

Malformed data returns structured `code`, `path`, and `detail` errors without a
traceback. Any active transitional row, unclassified row, tombstone overlay,
unknown managed claim, missing additive entry, or changed immutable identity
fails closed before target mutation.

## Public Skill And Eval Assets

Guru public packages, consumer schemas, migrations, eval corpora, adapter
runtime, native trace contracts, companion scripts, and selected-platform
`guru-*` discovery copies remain additive Guru-owned assets. Current Interface
1.3 package semantics and contract identities are owned by their canonical
packages, not by overlay tombstones.
