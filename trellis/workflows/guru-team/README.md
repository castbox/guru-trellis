# Guru Team Workflow

原 Merge history owner 在一次固定远端截点内自动准备/核验历史，query1/query2
统一返回显式cutoff的result3.0。Completion/独立/恢复caller的直接消费与同步迁移见
[MIGRATION-569](../../presets/guru-team/MIGRATION-569.md)及原step-local合同。

已有正式 Delivery 经用户普通手动合并后，可按原 Merge 的
`delivery_merged_recovery` 恢复实际公共事实，再接原 Completion。
支持方式、实际内容/CI职责与完整安装采用见
[MIGRATION-557](../../presets/guru-team/MIGRATION-557.md)及 Merge step-local contract。

The [shared interaction contract](../../presets/guru-team/spec/workflow/workflow-contract.md#interaction-budget) is loaded at
`.trellis/spec/workflow/workflow-contract.md#interaction-budget` by the workflow,
interactive Skill owners and platform entries. Source/projection checks prove
contract distribution, not actual client interaction. Existing installations
receive it through a compatible complete migration; source edits do not update
an older installed runtime.

Intermediate command receipts are same-owner continuation material. The
[shared transport contract](../../presets/guru-team/spec/workflow/companion-scripts.md#intermediate-command-stdout-10)
and [migration](../../presets/guru-team/MIGRATION-453.md) govern CLI callers;
workflow routing consumes only the actual declared public invocation exit.

Causal evidence and disposition meanings live in the
[common spec](../../presets/guru-team/spec/workflow/causal-completion-semantics.md).
The existing qualification and stage Skills read its installed projection;
this workflow retains invocation/transition ownership and does not define
causal completion or infer it from a Delivery merge.

Normal revision and recovery follow the single continuation block in
`workflow.md`. Check execution-fact reuse and Delivery Review anchor recovery
are owned by their respective canonical Skill contracts, not this README.
The historical #531 development candidate consumes upstream Task schema 2.0 / Delivery API 1.0 and
requires the matching reviewed API source. The
[migration contract](../../presets/guru-team/spec/workflow/task-delivery-migration.md) owns the supported
D1 integration and D2 legacy-cutover boundary. A selected workflow does not
migrate existing Tasks or prove installation/joint acceptance.
Every Delivery has its own Planning and stable public identity before Author;
`guru-activate-delivery` is the Planning transition owner for D1 and successors.
The Task has overall scope/completion responsibility and no development-status router.

Before implementation, an approved plan's resolved document conflict is owned
by [Reconcile](../../skills/guru-team/packages/guru-reconcile-task-base/references/contract.md#pre-implementation-resolved-baseline).
Its baseline integration returns the same Task generation and Delivery to
Activation; business Check follows implementation. The post-implementation
resolved-Check/full-review path remains separately owned.

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
Intake -> task identity/scope -> Delivery creation -> Delivery Planning -> implementation
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
before writes; it does not rebuild old task/workspace mappings. Public Delivery
query/selection supplies execution identity; scope/Planning/phase writes use the
unique runtime declaration. Upstream `task.py start` binds a Task and does not
accept Delivery Planning or begin implementation.

## Installation

已发布稳定版本为 `v0.7.0-guru.3`，peeled commit 为
`7d20a930341dae3e7dd2d214660ce3b99e28d863`；其原 Fork lock 为
`5c760463680ffc10a3f26957b330c57a4b0c3ff8`，main CI `37735554354`。
默认稳定安装使用同一 immutable `.3` tag 的 workflow marketplace
`gh:castbox/guru-trellis/trellis#v0.7.0-guru.3` 和 preset checkout，按该 checkout
的原 lock 构建 Fork，不与当前新 Fork 混搭。

本次目标为尚未发布的 `v0.7.0-guru.4`。当前准备源码的 extension 与原 maintenance
target 为 `0.7.0-guru.4`；它不等于已发布的 immutable `.3` tag 内容。
当前正式 Fork lock 为 `2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0`，
tree `41ff285d857036324e480e1eb64d08fffd5956e1`，成功 main CI `38851816688`，
包含 #40 维护能力与 #43 的旧原生 schema-1 会话元数据兼容修复；CLI/Core
保持 `0.7.0-castbox.3`，package manager 为 `pnpm@10.32.1`。
源码试用的 workflow marketplace 与 preset 使用同一个真实、远端可寻址的完整 Guru
SHA；不预填未形成的 SHA，不使用尚不存在的 `.4` tag。来源记录和 Fork CI 不替代
实际构建、Guru exact-candidate、installed/lifecycle 或发布门禁。

当前基础工具采用保留其自身 receipt 对应的 `.3` installed graph 与原生 Task2/session3；
这不证明 `.4` installed parity。S2 先交付实际 clean committed `.4` 来源，S3 再经原
tools-only owner 执行新的 `.4` 操作，完成四平台投影、三平台 reapply/drift、正式 clean/
predecessor 维护及目标 native/下一实际 owner、恢复和回退定向验证。来源准备不声明
`.4` 正式安装、整体准备、完整多平台矩阵或业务/Release 通过。

本次最终 candidate 门禁在准备交付与 Finish 合并后，从 fresh `origin/main` 重新冻结
exact commit/tree 执行；早期 `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的验收不能替代
本次候选验证。tag、tag-pinned smoke、GitHub Release 与 Release Issue closure 仍为后续独立动作。

历史已发布 `v0.7.0-guru.1` 所锁定 Fork 的 update 会在访问旧 `0.6.17` 项目数据前拒绝，原数据保持不变。
已发布 `v0.7.0-guru.1` 不支持旧安装原地升级；拒绝不代表升级成功。
历史 `.3` 系列迁移能力（extension `0.7.0-guru.3` / Fork `0.7.0-castbox.3`）通过独立 standalone
`guru-upgrade-installation` 承接全部 `v0.6.x-guru.*` 与 `v0.7.0-guru.*` 正常安装；
显式升级请求从目标 source package 加载该 Skill，不先进入 business Intake。
见 [迁移说明](../../presets/guru-team/MIGRATION-495.md)；历史 Guru `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的同源远端验收绑定原 Fork `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / CI `37647767799`，由 [唯一系列 Test](../../../docs/requirements-design-test-contributions/495-upgrade-version-families/test.md) / EVD-051 承接，不证明当前新来源，普通 update/reapply 不替代迁移，普通 runtime 无兼容双读或自动迁移。
迁移保留业务定制、无关 dirty/untracked 与合法当前任务状态；legacy nonterminal 的 pinned-old/deferred 处置及 rollback 恢复实际升级前来源的边界保持 [迁移说明](../../presets/guru-team/MIGRATION-495.md) 合同。
当前知识 authority 由 `docs/requirements/README.md`、`docs/design/README.md`、
`docs/test/README.md` 与 `docs/architecture/README.md` 指定，与软件版本分开读取。

For current-source validation, use the source-locked Trellis Fork checkout
(`castbox/Trellis@2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0`, successful main CI
`38851816688`) and that same reviewed Guru source. Stable `.3` installation
uses its original source pair described above. For a local installation, compare the canonical `workflow.md` with
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

## Current Intake migration (#250)

The initial route remains Sync → Discovery → Clarify. Clarify owns six profiles
and selected requirement/design source authority; context requests preserve
the original caller. Install/reapply the complete current preset and controlled
callers together; see the canonical Clarify
[API migration](../../skills/guru-team/packages/guru-clarify-requirements/references/MIGRATION-250.md).
Upstream start/continue/brainstorm remain upstream-owned and discoverable; the
current workflow and Clarify contract constrain method reuse and resume.

## Current Planning migration (#292)

The sole task-plan business writer is `guru-author-task-plan`. The global
workflow invokes its requirements and solution exits around purpose-specific
Architecture planning 3.0, then current Wording, final Architecture and Approval.
Step-local behavior stays in the selected packages; upstream brainstorm/start/
continue and hooks remain upstream-owned. Install the matching complete preset
and marketplace workflow together using the [version and in-flight migration](../../presets/guru-team/MIGRATION-292.md).
Package closure, installed callability, actual native planning and Release are
separate conclusions; the migration document specifies their evidence boundary.

## Isolated task-free execution (#521)

Mode selection is independent of checkout location. The canonical
`guru-execute-task-free-change` contract owns linked non-base location selection
before the first write and its existing `location_required` interaction;
worktree/branch creation has its own exact operation boundary. Read-only work
creates no resources. No Task identity, Task-specific checkout API or
persistent location mapping is introduced for task-free execution. Formal new
Task creation also uses linked non-base execution through its existing owner;
old Task recovery and base Sync retain their original contracts.

The workflow's single continuation block is the Guru caller for start,
ordinary/same-chat, new-chat and explicit continuation. Actual upstream
`trellis-continue:no_current_task` ends that upstream step, then the caller
freshly resolves current request, binding and live candidate facts before the
existing no-task route. Valid bindings return to their Task owner; stale or
conflicting ones stop. Other-chat inventory never supplies this chat's identity.
Upstream start/continue/extractor/hooks remain unchanged. If the native entry
cannot hand the return to this caller, that path remains an upstream-owned
unverified dependency; installation or route tests do not prove it works.

Automatic partial-edit expansion returns to the selector; explicit expansion
returns to the execution owner's narrow-or-Intake choice. Preserve existing
candidates and unrelated dirty content, stop remaining writes, and retain
formal acquisition's clean invariant. Exact carryover, Task creation and each
Git/publication/install/cleanup action keep their own independent boundaries.
Install/update/reapply the canonical workflow and Skill projections together;
old current-checkout editing is directly replaced, not a fallback mode. Source
checks do not prove target installation or native Agent continuation.

## 受管 Python 的显式更新

初始化及显式 preset apply/reapply 默认选择执行时 PATH 的 `python3`，可用
`--python /path/to/python3` 覆盖；不传时直接运行 installer 也使用 PATH 选择。
从完整 Guru 源仓执行：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo /path/to/target-repository
trellis/presets/guru-team/scripts/bash/apply.sh --repo /path/to/target-repository --python /path/to/python3
```

CPython 3 不受 minor 白名单限制；相同有效 identity 复用，minor 变化选择对应 cache，
patch/path 本身不强制重建。依赖、真实公开 wrapper 的 Draft 2020-12 schema 检查和
staged 安装验证通过后才激活；失败保留原 active/环境。日常 Skill 继续使用 managed
venv，不自动跟随 Homebrew 或回退全局依赖，不自动清理旧 cache。
可执行 identity 命令、解释器优先级及失败修复见
[preset 使用与排障](../../presets/guru-team/README.md#显式更新受管-python)。

## 单 checkout 工具升级与独立旧任务维护（#566）

`guru-upgrade-tools` 与 `guru-maintain-legacy-task` 从完整匹配来源加载，分别处理工具更新、所选Task转换或仅历史保留；目标旧parser和Reconcile不成为维护启动前置。原完整Plan2保持独立。只更新显式目标，省略时先按既有配置与dev/develop/main/master/远端默认分支选分支，再绑定唯一checkout。

当前正式 source lock 已包含上游 #40 与 #43。`source_locked` 仍要求完整匹配、已提交且干净的 Guru 来源及成功的匹配 Fork 构建；来源锁变化不等于目标已升级。历史 `local_candidate` 仅为隔离开发证据，不证明正式来源维护、业务恢复或发布。入口、最小I/O成套切换、原owner核验/退役、native验证和兼容回退边界见 [MIGRATION-566.md](../../presets/guru-team/MIGRATION-566.md)。

## 固定开发基线

Task 开发基线、Delivery 完整内容范围与 PR target 分开承接。各阶段默认不追赶
最新 base；无实际阻塞可零 Reconcile 完成交付与收尾。真实冲突、必需检查集成
失败、Merge 已观察的既有服务端更新要求、明确依赖或主动同步，仍由原 owner
处理固定一次整合目标和必要差额。D2 消费真实已交付事实；Completion 核验全部
scope。合同退役与正常在途恢复见 preset 的 MIGRATION-567.md；不得单独更新
workflow/Skill 混入旧安装 graph。
