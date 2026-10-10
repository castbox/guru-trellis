# Guru Team Workflow

Normal revision and recovery follow the single continuation block in
`workflow.md`. Check execution-fact reuse and Delivery Review anchor recovery
are owned by their respective canonical Skill contracts, not this README.

The `guru-team` canonical workflow is the global AI routing contract. The
canonical source is `workflow.md`; an installed `.trellis/workflow.md` is a
managed projection, not a second owner. Read the active Skill's `SKILL.md` and
Interface before invoking its step. The workflow supplies mandatory invocation,
unique typed-exit consumers and fail-closed routing; package owners supply
judgment and deterministic command details.

New Architecture conclusions at Planning, applicable implementation discovery,
Phase 2 and committed Branch Review are produced by a fresh independent
subagent executing the existing
[Architecture Skill](../../skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md).
The [step-local contract](../../skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md)
owns reviewer method and input boundaries; this workflow routes the real result.
Delivery/Completion consume current conclusions and matching-stage eligibility.
Actual native and projection evidence is owned by [#404 Test](../../../docs/requirements-design-test-contributions/404-independent-architecture-review/test.md).

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

Current task identity is TaskId and lifecycle generation from current task
metadata, not a checkout path, session or branch name. Path-free session focus
selects the task; without a session context key, select an explicit TaskId.
Current branch authority is TaskBranchBinding in the Git common directory;
current execution location comes from live registered Git worktree facts.
Ignored runtime mapping and checkout paths are neither task identity nor
checkout-path authority. Missing binding enters
`guru-establish-task-branch-binding`. The public
`check-task-checkout-boundary.sh` validates the current task and checkout
before writes; it does not rebuild old task/workspace mappings. `guru-activate-task`
owns the status-only Planning activation; do not call the former `start-task.sh`
or upstream `task.py start` to perform that transition.

## Installation

本次 repository 正式发布目标为 `v0.7.0-guru.3`，extension 为 `0.7.0-guru.3`，固定 Fork CLI/core 为 `0.7.0-castbox.3`，package manager 为 `pnpm@10.32.1`；predecessor 是已发布的 `v0.7.0-guru.1`。版本轴独立，保持现有 extension，不发布中间 `.2`。Guru 目标仍为未发布候选，本准备文档不表示 candidate gate 或 Release 已通过。正式 Fork `.3` 已由 PR28 合并并通过 main CI，当前 lock 已固定；Guru 精确远端 `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的同源定向验收已完成，见 [唯一系列 Test](../../../docs/requirements-design-test-contributions/495-upgrade-version-families/test.md) / EVD-051。后继文档 HEAD 不代表重跑；Guru 软件发布、真实业务安装和完整累计矩阵仍未验证。
候选验证的 workflow marketplace source 与 preset 使用同一可寻址的完整 Guru
candidate SHA；只有目标发布且远端 tag 核验与最终 candidate 匹配后，才使用
同一 immutable `v0.7.0-guru.3`（marketplace `gh:castbox/guru-trellis/trellis#v0.7.0-guru.3`，
preset 来自该 tag 的 checkout）。Fork main CI 成功
不替代 Guru exact-candidate、installed/lifecycle 或发布门禁。

本次最终 candidate 门禁在准备交付与 Finish 合并后，从 fresh `origin/main` 重新冻结
exact commit/tree 执行；早期 `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的验收不能替代
本次候选验证。tag、tag-pinned smoke、GitHub Release 与 Release Issue closure 仍为后续独立动作。

历史已发布 `v0.7.0-guru.1` 所锁定 Fork 的 update 会在访问旧 `0.6.17` 项目数据前拒绝，原数据保持不变。
已发布 `v0.7.0-guru.1` 不支持旧安装原地升级；拒绝不代表升级成功。
本次 `.3` 目标（extension `0.7.0-guru.3` / Fork `0.7.0-castbox.3`）通过独立 standalone
`guru-upgrade-installation` 承接全部 `v0.6.x-guru.*` 与 `v0.7.0-guru.*` 正常安装；
显式升级请求从目标 source package 加载该 Skill，不先进入 business Intake。
见 [迁移说明](../../presets/guru-team/MIGRATION-495.md)；正式 Fork source/CI 已固定，Guru 分组验收及上述精确来源的同源远端验收已完成，普通 update/reapply 不替代迁移，普通 runtime 无兼容双读或自动迁移。
迁移保留业务定制、无关 dirty/untracked 与合法当前任务状态；legacy nonterminal 的 pinned-old/deferred 处置及 rollback 恢复实际升级前来源的边界保持 [迁移说明](../../presets/guru-team/MIGRATION-495.md) 合同。
当前 knowledge authority 为 `current-main-0.6.17-guru.76` / `active`，不是软件发布版本。

Use the source-locked Trellis Fork checkout (`castbox/Trellis@5c760463680ffc10a3f26957b330c57a4b0c3ff8`,
successful main CI `37735554354`)
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
adapter, dual reader, or mixed-graph mode. Archived tasks with retired
personnel fields are never Reactivate or Finish recovery candidates. Their
TaskIds remain reserved; exact source clues may only locate one for a read-only
rejection diagnostic. Archives conforming to the current task schema use the
current Reactivate contract.
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

## 根因候选资格

新增 semantic `guru-qualify-root-cause` 在现有十个 candidate profiles 中承接
normal-scenario、solution-mechanism 的实际合格结果。根因未知的有界诊断可以
继续；有独立效果、风险、owner 和退出依据的缓解保留 `mitigation_only`。
修复证据不足返回诊断，症状抑制只返回机制移除/替换。四出口为
`classified`、`mechanism_revision_required`、`diagnosis_required`、`blocked`。
同机制结论仍适用时由后续阶段消费；新/实质变化机制重新资格。阶段仍审当前
实现和证据，qualification 不等于完成，#383 拥有共同完成语义。

完整 preset 安装后使用 public discovery 和 stdin wrapper：

```bash
.trellis/guru-team/scripts/bash/discover-skill-contract.sh --root . --mode installed --skill guru-qualify-root-cause --json
# 先由 AI 读取 public contract/live facts 并完成 gate，再将 call-local envelope 送入：
.trellis/guru-team/skills/packages/guru-qualify-root-cause/scripts/invoke.sh --invocation -
```

三个 record/check/invoke 命令仅 stdin/stdout，无 qualification 文件、cache 或
授权持久化。安装与升级通过 canonical marketplace/preset，并重新应用 preset；
定向验证和代表性 clean/update/reapply 不代表完整多平台 Release 矩阵。
