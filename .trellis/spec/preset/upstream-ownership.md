# Current Guru Ownership Contract

This document is the durable semantic source of truth for current Guru-owned
paths. The machine-readable contract is:

- `trellis/presets/guru-team/ownership/upstream-ownership.json`;
- `trellis/presets/guru-team/ownership/upstream-ownership.schema.json`.

Both use current-only schema 4.0. They describe the assets this extension owns
now, and every field has a current validator or installer consumer.
Ownership does not define the platform inventory. Ownership does not define dogfood selection;
it projects the pinned upstream inventory and validates the target
manifest's exact selection.

## Ownership Boundary

Official Trellis owns every `trellis-*` Skill, command, prompt, hook, agent,
runtime agent, bundled reference, and meta entry. Guru Team must not install,
claim, patch, delete, or managed-upgrade those paths.

This includes the continuation extractor/loading protocol, `trellis-start`,
`trellis-continue`, SessionStart/UserPromptSubmit hooks, generated platform
entries, and `trellis-meta`. Guru owns the continuation semantics only inside
its marketplace workflow. Preset apply/reapply must preserve upstream-owned
entry bytes and must not modify the active `.trellis/workflow.md`, whether the
selected workflow is native or Guru Team.

Retired historical roots `.trellis/.developer`, `.trellis/workspace/**`, and
`.trellis/agent-traces/**` are outside the active ownership graph. Installer,
update, reapply, context, task-owner, and recovery paths preserve their bytes
without reading, indexing, copying, migrating, restoring, deleting, or claiming
them. Upstream `0.6.17` retired command stubs remain upstream-owned migration
messages, not supported Guru runtime entries.

Guru Team owns only paths inside anchored Guru namespaces. Schema 4.0 binds
the shared runtime/source claims and one projection descriptor for every pinned
upstream platform. Each descriptor declares the upstream id, public `cliFlag`,
template/config identity, Skill root, finish entry path/kind, and actual-load
policy.

Rules are matched by complete anchored path components. They never authorize a
broad prompt, command, Skill, hook, agent, or platform directory.

## Managed Claims

The extension manifest and ownership contract derive 43 current managed claims:
the installed runtime roots, shared Skill projection, and each descriptor's
deduplicated Skill-root and finish-entry claim.

Canonical `trellis/workflows/guru-team/**` and
`trellis/skills/guru-team/**` remain Guru-owned source content. They are not
additional installed managed-path claims.

## Additive Overlay Set

The canonical overlay tree contains exactly the 22 entry paths declared by the
pinned platform descriptors.

They are additive Guru entries. They do not replace an official Trellis file.
Any other file below `trellis/presets/guru-team/overlays/` is a current contract
violation.

## Current Manifest Boundary

A fresh target may begin without an installed Guru manifest. Once an installed
manifest exists, every installer and validator path accepts only the complete
current schema and current ownership contract. Missing required fields,
non-current schema versions, unknown claims, unexpected overlays, or malformed
provenance fail closed before target mutation.

The installer evaluates only paths declared by the current inventory. Current
managed assets use their previous-managed hash provenance:

| Current target state | Required behavior |
| --- | --- |
| missing | Install canonical bytes and record current provenance. |
| equals canonical | Preserve bytes and refresh deterministic provenance. |
| equals the current manifest's previous managed hash | Write `.bak`, then install current canonical bytes. |
| unknown local edit or invalid current provenance | Preserve the target, write canonical bytes to `.new` when safe, and block activation. |

Only current Guru-owned paths participate in this table.

## Deterministic Validator Boundary

Maintainers run:

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
```

The validator is read-only. It verifies schema 4.0, all 22 descriptors, 43
derived managed claims, 22 additive overlays, anchored namespace matching, current
registry/package identities, and objective counts/digests derived from current
assets. It must not judge design quality, route intent, finding severity,
update safety, or Issue closure.

Malformed data returns structured `code`, `path`, and `detail` errors without a
traceback. Any non-current schema, unknown rule or claim, missing or unexpected
overlay, broad upstream namespace claim, manifest mismatch, or sidecar fails
closed before target mutation.

## Update And Reapply

For a current installation:

1. run the selected Trellis version update, then `trellis update --dry-run` and
   exactly one preserve-mode live update: `trellis update --migrate --skip-all`
   when migration is required or `trellis update --skip-all` otherwise;
2. reselect the `guru-team` marketplace workflow;
3. reapply the current Guru preset;
4. resolve current managed-asset `.new`/`.bak` conflicts;
5. rerun source/installed package validation, ownership validation, platform
   discovery checks, dogfood drift, and a recursive zero-sidecar scan.

A non-current installed or ownership manifest is invalid input and stops this
flow. Continuing requires a fresh target or a complete current manifest; the
validator has no schema-version-specific branch.

## Public Skill And Eval Assets

Guru public packages, consumer schemas, eval corpora, adapter runtime, native
trace contracts, companion scripts, and selected-platform `guru-*` discovery
copies are additive Guru-owned assets. Their current Interface 1.4 identities
come from the live registry and package contracts.

The Phase 0 five-stage transition family, call-local invocation envelopes,
shared runtime, and activation manifest live inside those existing anchored
Guru namespaces. They activate atomically with the six current Intake packages
and do not add an ownership rule, managed claim, or overlay. A mixed graph,
unknown asset, manifest mismatch, or any `.new`/`.bak` sidecar remains a
current-contract failure before activation.

Schema migrations inside those existing Guru namespaces do not expand path
ownership or managed claims. Publication/Finalizer 4.0 and finish-summary 2.0
replace current managed bytes in place; retired closeout-plan, Issue scope
classification aggregate and other task-local publication artifacts are not installed or claimed,
and no compatibility asset may be added outside the declared inventories.
