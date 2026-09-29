# Guru Team Workflow

The `guru-team` canonical workflow is the global AI routing contract. The
canonical source is `workflow.md`; an installed `.trellis/workflow.md` is a
managed projection, not a second owner. Read the active Skill's `SKILL.md` and
Interface before invoking its step. The workflow supplies mandatory invocation,
unique typed-exit consumers and fail-closed routing; package owners supply
judgment and deterministic command details.

## Current Lifecycle

```text
Intake -> task creation -> Planning -> task activation -> Phase 2
  -> Task Commit -> Branch Review
  -> Delivery Review -> Publish Delivery -> Merge Delivery
  -> Completion -> (remaining work / another Delivery / Closure)
  -> Finish -> Cleanup
```

Each business Delivery PR uses `Refs` and leaves the task active. Completion
alone decides whether the accepted task scope is complete; Closure alone
decides source Issue disposition. Finish archives only after Closure and a
verified bookkeeping persistence result. Cleanup consumes the current Finish
seal, never a historical receipt. The Finish bookkeeping PR is not a business
Delivery. Reactivate starts from a normally finished archived TaskId and a
current base, preserving the identity and incrementing its lifecycle generation.

Task identity is `task.json.id`, not a checkout path, session or branch name.
Current branch authority is TaskBranchBinding in the Git common directory;
current execution location comes from live Git checkout resolution. Missing
binding enters `guru-establish-task-branch-binding`. The public
`check-task-checkout-boundary.sh` validates the current task and checkout
before writes; it does not rebuild old task/workspace mappings. `guru-activate-task`
owns the status-only Planning activation; do not call the former `start-task.sh`
or upstream `task.py start` to perform that transition.

## Installation

Use the source-locked Trellis Fork checkout (`castbox/Trellis@8336e78b8fafe2a4bc4ea3d01815a61cf4f08983`,
successful main push CI `36519692082`)
and a matching reviewed Guru
source. For a local installation, compare the canonical `workflow.md` with
the target `.trellis/workflow.md` and preserve target edits before applying
it. Apply the Guru preset using
`trellis/presets/guru-team/scripts/bash/apply.sh --repo <target>` and validate
the installed graph. The repository root README and source lock identify the
exact CLI build. Remote marketplace installation is not a #434 gate.

## Migration Boundary

The old complete Publication -> Finalizer -> Merge -> Restore graph belongs
only to a pinned compatible old version. The current graph has no old DTO
adapter, dual reader, or mixed-graph mode. Old archived tasks discovered by
source Issue require committed task source, unique TaskId and terminal Git
archive identity before Reactivate; the old finish summary/index is only a
candidate hint.
Old Finalizer residue or a closed Issue alone is not a normally finished archive.
An in-flight old task, including a terminal PR or divergent remote/local head,
needs exact-case old-version completion or explicit manual disposition; do not
reuse a merged PR or mutate the business repository during graph migration.

Retired public ids are not aliases: `guru-create-task-workspace` becomes the
independent `guru-create-issue` and `guru-create-task` route;
`check-workspace-boundary` becomes `check-task-checkout-boundary`; the old
Publication, Finalizer, PR Merge and Restore ids are retired in favor of the
Delivery, Completion, Closure, Finish, Cleanup and Reactivate owners. The
exact public-ID disposition table is in
`trellis/presets/guru-team/MIGRATION-434.md`; the active package Interfaces
define each new contract. `README.pre-434.md` is historical evidence, not
current guidance.

## Validation Boundary

Verify source and installed package/interface/manifest closure, all unique
workflow exits/targets, Shared/Codex/Claude/Cursor actual loading, preset
reapply without sidecars, and source/dogfood byte parity. A representative
clean install belongs to this activation gate. The full multi-platform
upgrade/release matrix belongs to its dedicated Release Gate Issue.
