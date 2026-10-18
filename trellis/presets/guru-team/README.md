# Guru Team Preset

Issue 创建与修订的共同内容正文由原 Clarify package 的
[Issue 内容编写规范](../../skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md)
唯一维护。四个原 Issue owners 实际读取同一安装正文及清晰写作规范，继续各自的
写作、审核与创建职责。原递归 package 分发安装正文及 `examples/issue-content/`
教学示例；示例和分发检查不代替实际 Agent 行为或创建、修订后的回读证据。
已有安装须完整采用匹配的 preset 与四个原 packages，再检查 reapply、投影、drift
及 sidecar；源码更新本身不证明旧安装已经采用。

Architecture 晋升在最终 Check 前完成；committed 独立判断和完整 Branch Review
覆盖实际晋升文件。公共入口与 consumer 必须成套更新，三类在途 Delivery、
partial/output-loss 恢复和窄引用/状态对齐见 [MIGRATION-600](MIGRATION-600.md)。
源码更新不证明已有安装或业务采用完成。

规划正文的唯一 writer 是原 `guru-author-task-plan`。其
[正文合同](../../skills/guru-team/packages/guru-author-task-plan/references/planning-body.md)
与同 package 的 `templates/` 定义整体 Task PRD 和 Delivery 三正文。原 consumers
在各自职责内实际读取这些文件及必要引用；preset 复用现有递归 package 分发，
不新增 loader、公共 DTO 或正文副本。`examples/planning-body/` 的去敏完整过程
示例用于教学，不能作为实际 V1–V7 写作/审核通过证据。

已有安装采用该能力时，须更新完整匹配的 marketplace workflow、preset、Author
和原 consumers；源码修改不会自动改变业务安装。apply/reapply 后检查 installed
和声明平台投影、drift、`.new/.bak` 及用户内容保留，按原冲突机制处理 sidecar。
真实 Agent 写作/审核、确定性检查和安装结果分别报告；静态分发不能代替行为
验收，一个代表平台结果也不证明其他平台实际行为。历史归档不追溯改写，完整
多平台升级及 Release 矩阵仍归专门 Issue。

[清晰技术写作规范](./spec/workflow/clear-technical-writing.md) 是唯一 canonical 正文；preset 将它安装到
`.trellis/spec/workflow/clear-technical-writing.md`。AGENTS 有界区块、workflow
Phase Index/continuation、公共 Guru Skills 和各平台 Guru finish 入口引用同一正文。
加载要求覆盖无 Task、Task、task-free、独立操作、恢复和子 Agent；写作 owner 自检，
审核 owner 保持原范围。源码和投影检查不证明实际平台加载与输出行为。

已有安装须更新匹配的 workflow 并完整 reapply preset。Trellis update/upgrade 后，
先按官方 marketplace `--create-new` 预览，再显式 `--force` 应用 workflow，最后
reapply preset。现有受管哈希与 `.new`/`.bak` 机制保留用户修改；AGENTS 用户区块
保持原样。源码更新不会自动更新旧安装；完整升级与 Release 矩阵仍由专门 Issue 承担。

跨独立审查者的工程执行事实采用与完整安装边界见 [MIGRATION-578](MIGRATION-578.md)；当前完整语义判断和结果绑定继续由原 owner 拥有。

历史查询由原 Merge owner 自动准备固定截点所需对象；query1/query2统一返回
含 `cutoff_commit` 的result3.0。实际临时Git写入、原consumer及完整成套采用见
[MIGRATION-569](MIGRATION-569.md)。源码变更不等于旧安装或开发Task已迁移。

已发布 Delivery 的普通手动合并由原 Merge 的 terminal-only profile 恢复，
随后原 Completion 审查真实内容与验证证据；采用边界见
[MIGRATION-557](MIGRATION-557.md)。仅 source 验证不证明旧安装已经切换。

The [shared interaction contract](./spec/workflow/workflow-contract.md#interaction-budget) is loaded at
`.trellis/spec/workflow/workflow-contract.md#interaction-budget` by the workflow,
interactive Skill owners and platform entries. Source/projection checks prove
contract distribution, not actual client interaction. Existing installations
receive it through a compatible complete migration; source edits do not update
an older installed runtime.

Intermediate command stdout follows the shared
[receipt contract](./spec/workflow/companion-scripts.md#intermediate-command-stdout-10).
Reapply the complete matching preset and migrate controlled callers as described
in [MIGRATION-453.md](./MIGRATION-453.md); public Skill exits retain their contracts.

The [common causal authority](./spec/workflow/causal-completion-semantics.md)
is installed at `.trellis/spec/workflow/causal-completion-semantics.md` through
the existing managed-spec installer. Qualification and stage packages read
that one source; apply/reapply distributes their stage-local contracts.

Normal revision/recovery contracts live in `guru-check-task` and
`guru-review-task-delivery`; apply/reapply projects those canonical packages
to installed and platform copies. Targeted validation proves those projections;
it does not replace the cumulative Upgrade/Release matrix.
The historical #531 development candidate uses the upstream Task schema 2.0 / Delivery API 1.0.
Read [MIGRATION-531.md](./spec/workflow/task-delivery-migration.md) before applying it.
That historical candidate binds product commit
`1e40014023de53ddfd9368b3fb4d0a7a31e92293`
and the matching CLI/Core tar identities recorded in that contract. PR #36
is merged and upstream #31 is completed; that does not establish Guru joint readiness.
The local source snapshot fingerprint is separate from the product commit and tar.
The previous `5181ab…` copy-collision result remains historical. PR #32 is merged;
its `ce36314b` predecessor is historical evidence, not the later #531 pair.
Those product/tar/snapshot results retain their historical scope; current-source
adoption uses the formal source lock below and does not relabel them as new evidence. Legacy targets require the upstream D2 migration
and Guru private migration before switching; refusal preserves the old install.

Every Delivery, including D1, owns its Planning. `guru-create-delivery` establishes
the public identity before the existing Author; `guru-activate-delivery` records
actual Planning after the current dialogue acceptance. Task identity/scope remains
separate. The old Task activation runtime is absent from this candidate. Reapply
never selects, migrates or advances a Task/Delivery, and the installed official
runtime owns the public model.

This preset installs the companion assets and current Skill packages for the
`guru-team` canonical workflow into an existing Trellis project. The
canonical package source is `trellis/skills/guru-team`; installed packages,
Shared/Codex/Claude/Cursor skills and finish entries are managed projections.
The installer never edits upstream Trellis source or a global npm package.

Architecture review uses the existing
[canonical Skill](../../skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md)
and its [step-local contract](../../skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md).
New conclusions use fresh independent subagents; platform entries load and
schedule that same contract. Install/update must reapply the matching complete
preset so canonical, installed and selected platform copies use the same method.
Projection checks and actual native behavior are separate evidence; current
#404 coverage and limitations live in its [unique Test](../../../docs/requirements-design-test-contributions/404-independent-architecture-review/test.md).

## Apply And Verify

已发布稳定版本为 `v0.7.0-guru.3`，peeled commit 为
`7d20a930341dae3e7dd2d214660ce3b99e28d863`；其原 Fork lock 为
`5c760463680ffc10a3f26957b330c57a4b0c3ff8`，main CI `37735554354`。
默认稳定安装使用同一 immutable `.3` tag 的 workflow marketplace
`gh:castbox/guru-trellis/trellis#v0.7.0-guru.3` 和 preset checkout，按该 checkout
的原 lock 构建 Fork，不与当前新 Fork 混搭。

本次目标为尚未发布的 `v0.7.0-guru.4`。当前准备源码的 extension 与原 maintenance
target 为 `0.7.0-guru.4`；它不等于已发布的 immutable `.3` tag 内容。
当前正式 Fork lock 为 `7bcbeaad31380e7a29c97898cb947c6120a61775`，
tree `c2129a4e600f37b40b08ecec7347fe16a5642d3a`，成功 main CI `39043542548`，
包含 #40 维护能力、#43 的旧原生 schema-1 会话元数据兼容修复与 #47 的
Task/Delivery Git 对象读取优化，以及 #50 的公开 `GitCandidateContent` 不可变摘要能力及 #52 的公开 `task_resume`。本次仅准备精确来源；目标工具安装、Guru PR 链与
性能验收仍须后续独立验证。CLI/Core
均为 `0.7.0-castbox.4`，package manager 为 `pnpm@10.32.1`。
已有 Fork `.4` tarball `castbox-v0.7.0-castbox.4` 属于历史配对来源，
不证明当前 lock 的匹配构建。当前来源使用干净 workspace 的正常 CLI/Core
依赖布局，保留模板原 mode；不重打上游包、不放宽 source_locked，
不代表 Guru `.4` 已发布或目标正式采用。
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
历史 `.3` 系列迁移能力（extension `0.7.0-guru.3` / Fork `0.7.0-castbox.3`）提供独立 semantic
`guru-upgrade-installation`，支持全部 `v0.6.x-guru.*` 与 `v0.7.0-guru.*` 正常安装，
按实际 receipt/ownership/core/task 差异分组；从固定目标 source package 加载，不先进入
business Intake，普通 apply 保持严格。
支持来源、固定依赖前置条件和验收状态见 [MIGRATION-495.md](./MIGRATION-495.md)。
历史 Guru `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的同源远端验收绑定原 Fork `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / CI `37647767799`，由 [唯一系列 Test](../../../docs/requirements-design-test-contributions/495-upgrade-version-families/test.md) / EVD-051 承接，不证明当前新来源；
普通 update/reapply 不替代迁移，普通 runtime 无兼容双读或自动迁移。
迁移保留业务定制、无关 dirty/untracked 与合法当前任务状态；legacy nonterminal 的 pinned-old/deferred 处置及 rollback 恢复实际升级前来源的边界保持 [迁移说明](./MIGRATION-495.md) 合同。
当前知识 authority 由 `docs/requirements/README.md`、`docs/design/README.md`、
`docs/test/README.md` 与 `docs/architecture/README.md` 指定，与软件版本分开读取。

For current-source validation, use the source-locked, built
`castbox/Trellis@7bcbeaad31380e7a29c97898cb947c6120a61775` CLI
(successful main CI `39043542548`) and that same reviewed Guru source.
Stable `.3` installation uses its original source pair described above. For the local workflow sample, compare the canonical `workflow.md`
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
including `runtime/task_lifecycle` and the stateless `runtime/delivery_projection`; platform projections do not contain
private runtime, tests or recovery state.

The workflow's current path is Task Commit -> Branch Review -> Delivery
Review/Publish/Merge (repeatable while active) -> Completion -> Closure ->
Finish -> Cleanup. `guru-activate-delivery` owns each Delivery Planning transition. The
current task identity is TaskId and lifecycle generation from current task
metadata. Path-free session focus selects the task; without a session context
key, select an explicit TaskId. The
`check-task-checkout-boundary.sh` command checks TaskId/generation, current
TaskBranchBinding and live Git checkout. It does not read `task.json.branch`,
`worktree_path`, old task/workspace mappings or a persisted checkout path.
The current checkout is resolved from TaskBranchBinding and live registered
Git worktree facts; ignored runtime mapping and checkout paths are neither
task identity nor checkout-path authority.

Old `prepare-task.sh`, `start-task.sh`, task-workspace, Publication,
Finalizer, PR-Merge and `finish-work.sh` companion entrypoints are not
installed as current public commands. They are not compatibility aliases.
The exact public-ID dispositions are in `MIGRATION-434.md`; a replacement ID
identifies a new contract, not an adapter for an old payload.
Historical tasks with retired personnel fields remain read-only. Their TaskIds
prevent reuse, while exact source clues may locate one solely to explain why
Reactivate and Finish recovery reject it. A normally finished archive that
conforms to the current upstream task schema remains eligible for the current
Reactivate contract.

## Source-Repository Official Projection Check

This source repository also dogfoods official Trellis scripts and bundled
Shared/Codex/Claude/Cursor entries. After refreshing those generated assets
from the built, source-locked Fork, verify the actual files separately from
Guru-managed overlay drift:

```bash
python3 trellis/presets/guru-team/scripts/python/verify_dogfood_upstream_projection.py \
  --repo-root . --fork-source <exact-built-fork-checkout> --json
python3 -m unittest discover -s trellis/presets/guru-team/scripts/python \
  -p test_verify_dogfood_upstream_projection.py
```

The read-only check uses official template collectors and hash functions. It
checks generated bytes, official hash entries, the generated `.version`, and
removal of the retired history reader; editable platform configuration and
Guru-owned files have separate owners. The behavior tests run the actual
dogfood task scripts without a supplied Fork replacement, covering Issue and
no-Issue creation, list/context, and rejection of retired personnel arguments.

Refreshing this source repository's generated projection is not an upgrade
path for old installations. The selected Fork rejects a mismatched installed
version before reading old project data; changing only `.version` cannot
establish a current projection. Historical task/workspace bytes remain outside
this check. Clean installation, old-install refusal, remote marketplace and
Release evidence must be reported separately.

Canonical source validation, installed graph/manifest verification, a
representative clean local workflow sample + preset install, current platform actual-load
and reapply/drift checks are part of #434 activation. The complete multi-platform
Release matrix is deferred to its dedicated gate. The pre-#434 long-form
contract is preserved in `README.pre-434.md` for historical diagnosis only.

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
and marketplace workflow together using the [version and in-flight migration](./MIGRATION-292.md).
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

## 显式更新受管 Python

初始化或显式 apply/reapply 在执行时默认选择 PATH 的 `python3`。在完整、
匹配当前 Guru/CLI 合同的目标上，从 Guru 源仓运行：

```bash
TARGET=/path/to/target-repository
# 默认使用当前 PATH python3；同一命令也是显式更新/reapply 入口。
trellis/presets/guru-team/scripts/bash/apply.sh --repo "$TARGET"
# 明确选择一个命令名或路径，优先于 PATH python3；失败不会回退。
trellis/presets/guru-team/scripts/bash/apply.sh --repo "$TARGET" --python /path/to/python3
# 可直接调用 Python installer；不传 --python 时仍按 PATH python3 选择目标解释器。
python3 trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py \
  --repo "$TARGET" --python /path/to/python3
# 只读查看默认/明确解释器 identity，不安装、不激活。
python3 trellis/skills/guru-team/runtime/bootstrap.py --repo "$TARGET" \
  --runtime-assets trellis/skills/guru-team/runtime --print-identity
python3 trellis/skills/guru-team/runtime/bootstrap.py --repo "$TARGET" \
  --runtime-assets trellis/skills/guru-team/runtime --python /path/to/python3 --print-identity
```

只要求 CPython 3，不维护 minor 白名单。identity 继续绑定 lock、runtime API/layout、
Python implementation/major/minor、OS、architecture、ABI/platform。相同有效 identity
复用；minor 变化选择对应 cache。patch 或解释器路径变化本身不要求重建，也不保证
受管环境 patch 与 Homebrew 最新版本同步。日常 Skill 只用已激活 managed venv，
Homebrew 更新不会触发自动更新或退回全局 site-packages。旧 identity 不自动清理。

激活前必须完成 hash-locked 依赖安装、Draft 2020-12 probe、真实公开 schema wrapper
正/普通不完整输入检查，以及完整 staged source/installed 验证。wrapper 的隔离 capability
fixture 只证明传输/运行能力，不代表用户业务语义判断。安装或 runtime-check 失败时保留
原 active pointer 和原环境；同 identity repair 也在检查通过后才替换旧环境。

| 错误 code | 修复和重试 |
| --- | --- |
| `interpreter_unavailable` | 运行 `command -v python3` 和 `python3 --version`；检查可执行权限，或用上面的 `--python /path/to/python3` 明确选择。 |
| `python3_required` / `python_implementation_unsupported` | 选择可运行的 CPython 3；不修改框架 manifest 来添加 minor。 |
| `venv_bootstrap_failed` | 检查所选 Python 的 `-m venv` / ensurepip 支持，再使用同一 apply 命令。 |
| `dependency_install_failed` | 检查 PyPI 访问及锁定依赖对所选解释器的 wheel 可用性，再重试；可显式选另一 CPython 3，不改 lock 或系统 Python。 |
| `managed_runtime_check_failed` | 从完整 matching Guru 源/preset 重试，检查公开 wrapper/runtime 资产；可显式选择解释器。原 active 和旧环境保留，不手动覆盖 cache。 |

未枚举 minor 的 identity admission 成功并不证明其 wheel/依赖兼容。这里的聚焦检查不替代
Python minor、多平台、Upgrade/Release 或业务仓升级验证；旧安装仍须遵守已有迁移边界。

## 单 checkout 工具升级与独立旧任务维护（#566）

`guru-upgrade-tools` 与 `guru-maintain-legacy-task` 从完整匹配来源加载，分别处理工具更新、所选Task转换、人工旧归档恢复或仅历史保留；目标旧parser和Reconcile不成为维护启动前置。原完整Plan2保持独立。只更新显式目标，省略时先按既有配置与dev/develop/main/master/远端默认分支选分支，再绑定唯一checkout。

当前正式 source lock 已包含上游 #40 与 #43。`source_locked` 仍要求完整匹配、已提交且干净的 Guru 来源及成功的匹配 Fork 构建；来源锁变化不等于目标已升级。历史 `local_candidate` 仅为隔离开发证据，不证明正式来源维护、业务恢复或发布。入口、最小I/O成套切换、原owner核验/退役、native验证和兼容回退边界见 [MIGRATION-566.md](MIGRATION-566.md)。

## 固定开发基线

Task 开发基线、Delivery 完整内容范围与 PR target 分开承接。各阶段默认不追赶
最新 base；无实际阻塞可零 Reconcile 完成交付与收尾。真实冲突、必需检查集成
失败、Merge 已观察的既有服务端更新要求、明确依赖或主动同步，仍由原 owner
处理固定一次整合目标和必要差额。D2 消费真实已交付事实；Completion 核验全部
scope。合同退役与正常在途恢复见 preset 的 MIGRATION-567.md；不得单独更新
workflow/Skill 混入旧安装 graph。

人工旧归档恢复使用原维护 owner 的 `archive_resume` profile。正式 Finish 归档
仍由 Reactivate 承接；未完成收尾返回原事务。恢复保留原归档并消费公共返回的
活动身份，目标 native 和下一实际 Guru owner 必须实际验证。
正式 source lock 不变，本地 matching candidate 只用于隔离开发；详见
[兼容与依赖边界](./MIGRATION-577.md)。
