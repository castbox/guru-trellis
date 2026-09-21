# Overlay Guidelines

## Final Overlay Boundary

The preset overlay tree contains exactly one descriptor-bound Guru finish entry
for each platform in the pinned upstream `AI_TOOLS` inventory. The current
inventory contains 22 entries. This canonical capability set is distinct from
the target repository's exact installed selection.

They are additive platform launchers, not replacements for Trellis upstream
files. The current ownership inventory describes only Guru-owned rules, claims,
and additive overlays.

Do not add or restore overlays for `trellis-start`, `trellis-continue`,
`trellis-finish-work`, bundled skills, hooks, sub-agents, channel runtime agents,
or `trellis-meta` references. Official Trellis init/update/upgrade owns those
paths and bytes.

Do not add an overlay for `[trellis-continuation]` extraction, start/continue
loading, workflow switch behavior, or any native route. The Guru continuation
body belongs only to the canonical Guru marketplace workflow; preset reapply
does not rewrite `.trellis/workflow.md` and cannot use an overlay to repair a
missing or invalid continuation contract.

## Entry Contract

Each descriptor-bound entry must:

- carry the `<!-- guru-team-overlay: v1 -->` marker;
- read live task/Git context and `.trellis/workflow.md`;
- load the mandatory stable Guru Skills through the workflow graph;
- enter publication/finalization only through the current typed exits;
- automatically consume verification, stale, resume, and reprepare routes;
- ask only for a real material choice, new authority, or the finalizer's exact
  bounded side-effect set;
- return the declared terminal result or fail closed.

For Phase 0, launchers invoke the stable `guru-sync-base` public Skill once and
route only its checked output and the workflow-owned five-stage transition.
They must not expose low-level resolve/execute/check as normal steps, persist an
owner/prerequisite locator, invoke compatibility `prepare-task` as a workflow
hop, or reconstruct transition fields from runtime source.

The marker is an entry-format and drift check only. The installer must never
use the marker, the words `Guru Team`, or any other content-shape heuristic as
evidence that an existing target is preset-managed. Ownership comes only from
exact installed-manifest provenance.

They must not copy step-local input fields, semantic dimensions, findings,
confirmation rules, recorder/checker commands, artifact lifecycles, recovery
mechanics, deterministic closeout flags, or private runtime facts. They must not
call `finish-work.sh` directly.

Publication payload projection is package/workflow behavior, not an overlay
concern. Platform launchers route through current typed exits and must not
author `pr-body.md`, `finish-summary-index.json`, adapt legacy 3.0 DTOs, or
reconstruct title/body for Finalizer.

Each launcher uses the native entry path and entry kind declared by its
projection descriptor. OpenCode remains an ordinary explicit platform
capability; it is not part of this repository's dogfood selection.

## Public Skill Discovery

Canonical package semantics live only under `trellis/skills/guru-team/`.
Preset apply installs byte-identical active package copies to:

- Shared: `.agents/skills/guru-*/**`;
- Codex: `.codex/skills/guru-*/**`;
- Claude: `.claude/skills/guru-*/**`;
- Cursor: `.cursor/skills/guru-*/**`.
- every other selected upstream platform: the descriptor's `skill_root`.

These package projections are managed-hash installation, not overlay files.
Selected platforms may differ only in discovery root or native adapter
protocol; public Interface, exits, projections, eval corpus, and behavior remain
identical.

The six Phase 0 packages, transition/envelope schemas, package runtimes, minimal shared kernel, and
activation manifest are distributed as one versioned package unit. A selected
platform may never discover a new package copy against an old transition or
runtime inventory.

Mandatory invocation is guaranteed by the active workflow's stable markers,
not by frontmatter auto-match or patched upstream entries.

## Installer Selection

Shared `guru-*` package discovery is always installed. Platform flags select
only the corresponding platform package root and explicit Guru finish entry:

- default: Shared + Claude, Codex, and Cursor;
- `--platform <name>`: Shared + exactly the selected platforms;
- unknown platforms: fail closed before writes.

Shrinking platform selection removes only old files whose bytes match their
previous Guru managed hashes. Unknown local edits are preserved and receive a
`.new` conflict; they are never silently deleted.

## Overlay Provenance Domain

`.trellis/guru-team/extension.json` owns overlay state independently under the
closed top-level `overlays` object:

- `schema_version` and `status` identify the current provenance contract;
- `selected_platforms` is the exact requested platform set;
- `files[]` is the complete currently managed selected-entry inventory;
- `removals[]` records only safe previous-hash removal;
- `conflicts[]` records preserved unknown/invalid paths and remediation;
- `sidecars[]` exactly matches adjacent `.new`/`.bak` files on disk.

Selected entries follow four cases only: missing installs, canonical-equal stays
unchanged, exact previous managed hash upgrades after `.bak`, and unknown or
invalid provenance is preserved with `.new`. Unselected prior entries are
deleted only when their current bytes equal the recorded previous managed hash.
Missing or malformed `overlays` provenance fails closed. No
`install.managed_assets`, marker, or text fallback may infer overlay ownership.

Any conflict or unresolved sidecar blocks staged activation. Installed
validation reconstructs the selected inventory from canonical platform mapping
and independently checks hashes, modes, removals, unselected disk state, and
recursive sidecars; it does not trust the producer's flat managed-assets list.

## Update, Reapply, And Dogfood

Official `trellis update`/version upgrade may refresh upstream-owned files and
the default workflow. The supported recovery order is:

1. update/upgrade Trellis;
2. reselect the marketplace `guru-team` workflow;
3. reapply the Guru preset;
4. resolve `.new`/`.bak` and local-edit conflicts;
5. validate source/installed packages, ownership, platform identity, dogfood
   drift, executable modes, and recursive zero sidecars.

After canonical overlay edits, synchronize this dogfood repository with:

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . \
  --platform claude --platform codex --platform cursor --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

The drift checker compares only managed Guru assets and the entries selected by
the dogfood manifest. It never compares, replaces, or deletes upstream-owned files.
It also never treats the active workflow as a preset-managed overlay. Workflow
selection and continuation bytes are verified by the marketplace/workflow gate;
preset reapply must leave them unchanged.

## Validation

```bash
find trellis/presets/guru-team/overlays -type f | sort
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

Success requires exactly 22 canonical overlay files, exactly three dogfood
entries, no unexpected installed overlay path, exact canonical/dogfood bytes,
correct executable modes for managed scripts,
and no unresolved `.new`/`.bak` anywhere in the installed extension surface.
Phase 0 validation also proves public-sync-only launcher wording and byte parity
for the complete atomic package unit across dogfood and every selected platform.

## Anti-Patterns

- Adding any `trellis-*` launcher to the Guru overlay inventory.
- Broadly claiming a prompt, command, skill, hook, or agent directory.
- Copying workflow or Skill internals into platform launchers.
- Treating a package discovery copy as a self-contained extension.
- Treating `.new` or `.bak` creation as successful activation.
