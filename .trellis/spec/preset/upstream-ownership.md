# Current Guru Ownership Contract

This document is the durable semantic source of truth for current Guru-owned
paths. The machine-readable contract is:

- `trellis/presets/guru-team/ownership/upstream-ownership.json`;
- `trellis/presets/guru-team/ownership/upstream-ownership.schema.json`.

Both use current-only schema 3.0. They describe the assets this extension owns
now, and every field has a current validator or installer consumer.

## Ownership Boundary

Official Trellis owns every `trellis-*` Skill, command, prompt, hook, agent,
runtime agent, bundled reference, and meta entry. Guru Team must not install,
claim, patch, delete, or managed-upgrade those paths.

Guru Team owns only paths inside an anchored Guru namespace. Current ownership
contains exactly 11 rules:

1. installed runtime under `.trellis/guru-team/`;
2. canonical workflow under `trellis/workflows/guru-team/`;
3. canonical Skill packages under `trellis/skills/guru-team/`;
4. stable Skill ids with the `guru-` prefix;
5. shared discovery packages under `.agents/skills/guru-*/**`;
6. Codex discovery packages under `.codex/skills/guru-*/**`;
7. Cursor discovery packages under `.cursor/skills/guru-*/**`;
8. Claude discovery packages under `.claude/skills/guru-*/**`;
9. the Codex `guru-finish-work` entry;
10. the Claude `guru-finish-work` entry;
11. the Cursor `guru-finish-work` entry.

Rules are matched by complete anchored path components. They never authorize a
broad prompt, command, Skill, hook, agent, or platform directory.

## Managed Claims

The extension manifest and ownership contract expose exactly nine current
managed claims:

- `.trellis/guru-team/`;
- `.trellis/guru-team/skills/`;
- `.agents/skills/guru-*/`;
- `.codex/skills/guru-*/`;
- `.cursor/skills/guru-*/`;
- `.claude/skills/guru-*/`;
- `.codex/prompts/guru-finish-work.md`;
- `.claude/commands/guru/finish-work.md`;
- `.cursor/commands/guru-finish-work.md`.

Canonical `trellis/workflows/guru-team/**` and
`trellis/skills/guru-team/**` remain Guru-owned source content. They are not
additional installed managed-path claims.

## Additive Overlay Set

The canonical overlay tree contains exactly three files:

- `.codex/prompts/guru-finish-work.md`;
- `.claude/commands/guru/finish-work.md`;
- `.cursor/commands/guru-finish-work.md`.

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

The validator is read-only. It verifies schema 3.0, the exact 11 rules, nine
managed claims, three additive overlays, anchored namespace matching, current
registry/package identities, and objective counts/digests derived from current
assets. It must not judge design quality, route intent, finding severity,
update safety, or Issue closure.

Malformed data returns structured `code`, `path`, and `detail` errors without a
traceback. Any non-current schema, unknown rule or claim, missing or unexpected
overlay, broad upstream namespace claim, manifest mismatch, or sidecar fails
closed before target mutation.

## Update And Reapply

For a current installation:

1. run official `trellis update` or the selected Trellis version update;
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
copies are additive Guru-owned assets. Their current Interface 1.3 identities
come from the live registry and package contracts.

Schema migrations inside those existing Guru namespaces do not expand path
ownership or managed claims. Publication/Finalizer 4.0, closeout plan 3.0, and
finish-summary 2.0 replace current managed bytes in place; retired task-local
publication artifacts are not installed or claimed, and no compatibility asset
may be added outside the declared inventories.
