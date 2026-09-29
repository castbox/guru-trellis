# Guru Team Preset

This preset installs the companion assets and current Skill packages for the
`guru-team` canonical workflow into an existing Trellis project. The
canonical package source is `trellis/skills/guru-team`; installed packages,
Shared/Codex/Claude/Cursor skills and finish entries are managed projections.
The installer never edits upstream Trellis source or a global npm package.

## Apply And Verify

当前目标仓库 tag 为 `v0.6.17-guru.2`，extension revision 为
`0.6.17-guru.43`；发布事实以 exact-candidate 验证、tag 和 GitHub Release
为准。官方 CLI/core 保持 `0.6.17`。

Use the source-locked, built `castbox/Trellis@8336e78b8fafe2a4bc4ea3d01815a61cf4f08983`
CLI (successful main push CI `36519692082`) and a matching reviewed Guru
source. For the local workflow sample, compare the canonical `workflow.md`
with the target `.trellis/workflow.md` and preserve target edits before
applying it. Then run:

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo <target>
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root <target> --mode installed --json
```

The installer uses managed-file provenance. Known managed updates may create
backups during the transaction; successful reapply must leave no unresolved
`.new` or `.bak`. User-modified files are preserved for review, not silently
overwritten. Current package wrappers load the installed shared runtime,
including `runtime/task_lifecycle`; platform projections do not contain
private runtime, tests or recovery state.

The workflow's current path is Task Commit -> Branch Review -> Delivery
Review/Publish/Merge (repeatable while active) -> Completion -> Closure ->
Finish -> Cleanup. `guru-activate-task` owns Planning activation. The
`check-task-checkout-boundary.sh` command checks TaskId/generation, current
TaskBranchBinding and live Git checkout. It does not read `task.json.branch`,
`worktree_path`, old task/workspace mappings or a persisted checkout path.

Old `prepare-task.sh`, `start-task.sh`, task-workspace, Publication,
Finalizer, PR-Merge and `finish-work.sh` companion entrypoints are not
installed as current public commands. They are not compatibility aliases.
The exact public-ID dispositions are in `MIGRATION-434.md`; a replacement ID
identifies a new contract, not an adapter for an old payload.
Historical old-chain tasks must finish on a pinned compatible old version or
receive exact-case manual disposition. A normally finished legacy archive may
enter current Reactivate only after source Issue, TaskId and terminal Git
identity validation; a partial Finalizer residue may not.

Canonical source validation, installed graph/manifest verification, a
representative clean local workflow sample + preset install, current platform actual-load
and reapply/drift checks are part of #434 activation. The complete multi-platform
Release matrix is deferred to its dedicated gate. The pre-#434 long-form
contract is preserved in `README.pre-434.md` for historical diagnosis only.
