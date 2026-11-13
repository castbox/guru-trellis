# Guru Team Workflow

## 当前出口查询与按步骤加载

正常会话先通过原 `get_context.py --mode phase` 或唯一 continuation 定位当前步骤，
再用 `--mode phase --step <step>` 读取该步骤。取得原 Skill 的一个正式出口后，
通过既有查询命令取得唯一 consumer、必要入口及其前置合同：

```bash
bash .trellis/guru-team/scripts/bash/discover-skill-contract.sh \
  --root . --mode installed --skill guru-author-task-plan --exit plan_ready --json
```

源仓库验证使用 `trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh`
和 `--mode source`。输入是实际 producer Skill id 和该次出口；不能用 phase、
文件存在或自行编造的结果代替。查询前需要完整 matching workflow、references、
packages、runtime 及受管投影。省略 `--exit` 时，仍执行原 Skill public contract discovery。

查询结果交当前 AI 消费：按返回的 producer output、consumer input 和 projection
准备原参数。producer 合同的相对 schema 路径以其 `contract_root` 解释；JSON schema
consumer 直接读取 repo-relative `consumer_schema_locator`，不拼到 producer package。
原 `consumer_input` 和 producer `contract_root` 保持。随后显式加载返回的 Skill
入口或执行原 workflow target。条件 router 的
完整分支仍由 AI 判断，入口前置是否充分仍归原 owner；查询成功不是下游 pass。
unknown、multiple、unmapped、缺引用或 graph/Interface mismatch 返回非零并停止。
修正普通输入后重试；matching/分发缺口由原 tools owner 修复；正文/Interface 差错
由其原 owner 修复。查询不改变 Task、Delivery、selection 或 gate。

完整标记和 router/stop 正文只在一份 [routing reference](references/routing.md) 中。
当前正常 runtime 只接受明确 reference，不保留旧 inline 图的 fallback。
原生 phase/step/continuation 提取不改 upstream；正常入口不要求读取全表。
实际选中 legacy 维护时才加载 [legacy reference](references/legacy.md) 和原维护
package 的完整合同，保留旧家族、转换、控制退役、历史来源及原支持边界。

已有安装按 [MIGRATION-792](../../presets/guru-team/MIGRATION-792.md) 成套采用，
由原工具维护 owner 保留 Task/session 与用户内容并处理 sidecar。只更新源码或
workflow 预览不能证明 installed 或实际 AI 加载已通过；完整多平台升级及 Release
矩阵仍由专门 Issue 承担。

Codex 的 Guru Skill 通过 `.agents/skills/` 公共投影发现，专属包仍仅在选择 `codex` 时分发。目录收敛不改变 workflow、Skill id 或出口；已有安装沿原维护 owner 保留用户修改并退出旧受管投影。采用和 native 验证边界见 [MIGRATION-724](../../presets/guru-team/MIGRATION-724.md)。

只读 Intake 通过原 `guru-sync-base` 的 `operation=read` 采用明确 Git 来源，
再由 Discovery 读取固定 tree 和独立草案。实际同步继续使用 `operation=sync`
并保留原 clean/ff/identity 检查。公开版本、投影及旧安装边界见 [MIGRATION-718](../../presets/guru-team/MIGRATION-718.md)。

normal/solution资格确认沿原Clarify、Discovery和Sync read取得或刷新真实context，再由正式clear返回原caller。
Task确认目标与来源Issue authority分开，原Task/Delivery及continuation保持。
两个确认profile、公共I/O和consumer须成套采用；具体边界见
[MIGRATION-811](../../presets/guru-team/MIGRATION-811.md)。各原Skill拥有内部行为，不从旧transition或record/check制造正式出口。

审核、审查、评审、复审和 review 先按对象与目的分流。代码、分支/PR、测试覆盖和
需求实现情况的审核，再区分独立只读审核与正式阶段结果。上述独立审核
无论有无 Task/Delivery，都显式调用 `guru-review-change`，由它完成指定范围的
只读审核和用户报告，不创建 Task、推进生命周期或生成正式 Guru pass。
workflow 调用或用户要求正式阶段结果时，才按原前置与完整范围进入
提交后完整 Review 或 Completion。普通 review 关键词和 Task 存在本身
不选择正式门禁。显式需求、概要设计、详细设计和测试计划文档审核按当前对象
选择专项方法。选择方法唯一见
[Specialist Review Standards](../../presets/guru-team/spec/workflow/quality-guidelines.md#specialist-review-standards)。

行为测试、因果验证、证据采用和实验停止的共同方法见
[Test And Validation Value](../../presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value)。
Author、实施派工和提交后完整 Review 在原职责内采用该方法。

Issue 内容、需求本身和动议本身不属于 `guru-review-change`，即使它们是改动文件。
它们保留现有 Issue、需求专项或项目动议/上游需求审核入口。需求用于判断实现覆盖时，
可作为本 skill 的来源；判断需求本身是否完整合理时，使用其上游 owner。
短句承接对话中明确的对象；对象不明时先澄清。完整入口选择以 workflow 为准。

独立审核的完整步骤归 [guru-review-change](../../skills/guru-team/packages/guru-review-change/SKILL.md)；
workflow 只负责显式调用和消费终端出口。`reviewed`、`blocked` 分别停止在该 owner
声明的用户响应消费者，不进入正式交付阶段。共同覆盖与结束规则由
[审核充分性规范](../../presets/guru-team/spec/workflow/review-sufficiency.md) 唯一维护。
各原审核 owner 在原职责内读取；提交后完整 Review 另读
[工程方法组合](../../skills/guru-team/packages/guru-review-change/references/review-method.md)。
该组合读取 Architecture、current-knowledge 和专题 SSOT，不读取 Check/Branch 的私有阶段方法。独立审核实际执行架构基线及其技术规则适用性判断、业务需求实现覆盖判断，
报告依据和缺口。正式阶段的独立评估、重审适用性及公共结果仍遵守各自原合同。
独立 owner 还必须按其本地合同使用不同 subagent 完成不同角度的审核，并核对
原始证据作最终判断。正式完整 Review 不继承该独立只读 owner 的本地调度要求。

Guru Team 拥有流程、完整范围和正式结论；`guru-ai-guides` 的专项 Skills 与同源
标准包提供项目实际采用的需求/设计/Go-Guru 实现/集成测试计划方法。通用流程
尚未替代这些专项能力。本 workflow/preset 不安装该外部目录，适用时实际加载，
不向其他技术栈强加 Go-Guru 规则或完整文档套件。专项 pass 不替代原 owner 的
当前判断，测试计划审核也不证明测试实现有效或实际执行成功。

原 Author/implementation owner 从
[固定范围与公开操作合同](../../skills/guru-team/packages/guru-author-task-plan/references/authoring.md#fixed-delivery-range)
取得完整 Candidate 构造、begin-check/rework 和 scope/stop 恢复说明。当前 Git
`pull_request` 调用使用受管 `construct-delivery-candidate.sh`，复用原范围和摘要
算法；workflow 只编排原步骤与出口，不要求业务 Agent 导入私有 Python。
原上游 git_free consumer 保持独立边界。完整 matching 安装及实际 Agent 行为
分别验证，不从文档或静态投影推定通过。

已有安装须采用匹配的 workflow、原 Guru packages 和 managed quality spec，再
完整 reapply preset 并检查 discovery、drift 及 `.new`/`.bak`；专项来源另行更新。
源码或投影一致不能证明实际 Agent 采用；完整平台升级与 Release 矩阵保留原职责。

JSON 载体读取与 Bind 双输入调用保持原 Skill owner 和流程。载体限制、错误变化及
匹配安装见 [MIGRATION-695](../../presets/guru-team/MIGRATION-695.md)；完整调用由
[Bind 文档](../../skills/guru-team/packages/guru-bind-task-session/references/json-inputs.md) 定义。

局部修复的实际影响判断见原 [selector 合同](../../skills/guru-team/packages/guru-select-workflow-mode/references/contract.md)。
草稿转正式 Issue 后的调查事实适用性与当前字段诊断见原
[Discovery 合同](../../skills/guru-team/packages/guru-discover-change-context/references/contract.md#current-owner-mismatch-diagnostics)；
Clarify 和 Author 继续各自的当前判断。已有安装采用完整匹配 preset 后检查
installed、平台投影、drift 和 sidecar；源码说明不证明业务安装或实际耗时改善。

明确 Task/Delivery 的接收会话通过原 Identity/Ensure/Bind/Selection 补齐自身缺失事实，
再继续同对象原未完义务。Planning 首失败诊断、standalone producer 身份构造，以及
带实际 key 的 Human artifacts 展示须成套采用。具体诊断字段、Task-only/archive
分支、matching 安装和分层验证边界见 [MIGRATION-679](../../presets/guru-team/MIGRATION-679.md)。

当前正常流程的 repair 投影、归档 Review example、首次 before authority 缺失及
final promotion 的 Bootstrap 回程，采用三个原 owner 的匹配当前合同。
直接演进、旧合法输入及成套安装边界见 [MIGRATION-663](../../presets/guru-team/MIGRATION-663.md)。

活动Task续接通过当前身份、合法binding/checkout及实际阶段owner准入，原created只服务初始创建区间。Delivery created wire保持；原consumer重读公共phase，planning才进适用Author，其余沿唯一continuation。范围修订按pre-Author→根PRD Author→Clarify acceptance→post-Author两次承接，退役status/DTO不成为current前置。完整matching切换、在途恢复及证据边界见 [MIGRATION-657](../../presets/guru-team/MIGRATION-657.md)。源码修改不证明已有安装或实际Agent已采用。

当前知识读写由原 RDT 与 Architecture 维护 Skills 执行。它们共同读取
[完整单元合同](../../skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md)，
workflow 仅调用原 owners；规划、实施、提交后完整 Review 和晋升消费适用正文。
本仓库实际迁移单元、未迁移范围、旧 Task 读取退出及 matching update/reapply 见
[MIGRATION-331](../../presets/guru-team/MIGRATION-331.md)。原公共 I/O 保持不变。
源码修改不代表既有安装已采用，也不证明真实 Agent 行为或成本改善。

Issue 创建与修订共用原 Clarify package 的
[Issue 内容编写规范](../../skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md)。
四个原 Issue owners 在各自职责内实际读取同一正文及清晰写作规范；workflow
保持原编排，不复制内容规则。原 preset 分发正文与去敏教学示例，已有项目须
采用完整匹配安装。示例、投影一致或检查通过不证明实际写作与外部回读完成。

原知识 owners 在工程自检后、提交前整合必要文档并读回；整合事实等待提交后独立审核。
原 `guru-review-branch` 在固定提交上一次完成 Check 与 Branch Review 的全部适用职责，
包括一次实现后独立 Architecture 判断，再由原 Delivery Review 记录 readiness。
普通晋升保留稳定 identity、single-writer 和实际 expected-current/readback；
当前与在途采用边界见 [MIGRATION-794](../../presets/guru-team/MIGRATION-794.md)，历史来源和原验证截止点保持。
源码变更不证明安装、实际 Agent 行为或外部采用。

并行知识采用稳定入口、限定目录及稳定 ID 查找完整正文；独立主题不在共享入口逐项登记。
共同方法、既有项目切换条件、未迁移范围、在途最终整合与旧写退出见
[MIGRATION-711](../../presets/guru-team/MIGRATION-711.md)。安装新规则与项目文档切换分别完成。

规划正文的唯一 writer 是原 `guru-author-task-plan`。其
[正文合同](../../skills/guru-team/packages/guru-author-task-plan/references/planning-body.md)
与同 package 的 `templates/` 定义整体 Task PRD 和 Delivery 三正文；原 Clarify、
Wording、Approval、实施、完整 Review、Delivery Review 与 Completion 在各自职责内实际
读取同源合同和必要引用。workflow 只编排和定位，不复制正文规则或改变公共 I/O。
`examples/planning-body/` 是带来源与修订过程的去敏教学材料，不是实际 V1–V7
执行证据。验收分别报告真实 Agent 写作/审核、确定性检查和安装投影；一个代表平台
的行为结果不能推定其他平台通过，模板或示例齐全也不能代替实际行为验证。

采用该正文能力时，须同步完整匹配的 marketplace workflow、preset、Author 及原
consumers。原递归 package 分发安装合同、模板和示例；已有业务安装不会自动更新。
继续使用原 apply/reapply、受管哈希与 sidecar 冲突路径，保留用户内容；历史归档
不追溯改写。完整多平台升级与 Release 矩阵仍由专门 Issue 负责。

[清晰技术写作规范](../../presets/guru-team/spec/workflow/clear-technical-writing.md) 是唯一 canonical 正文；preset 将它安装到
`.trellis/spec/workflow/clear-technical-writing.md`。AGENTS 有界区块、workflow
Phase Index/continuation、公共 Guru Skills 和各平台 Guru finish 入口引用同一正文。
加载要求覆盖无 Task、Task、task-free、独立操作、恢复和子 Agent；写作 owner 自检，
审核 owner 保持原范围。源码和投影检查不证明实际平台加载与输出行为。

单 checkout 的 tools-only 升级由 `guru-upgrade-tools` 承接。调用方显式提供
`AGENTS.md` 的 custom 基底正文与原文件快照；Guru 在公共 prepare 前更新其中的
规则块，公共计划返回后保持不变。目标 Fork 须声明 `tools_custom_instruction`
能力；缺失能力或最终内容被 `update.skip` 保留为旧块时，准备阶段停止。
旧失败操作先由未变的原来源合法处置，再从修复来源重新准备；不转换旧 checkpoint。

已有安装须更新匹配的 workflow 并完整 reapply preset。Trellis update/upgrade 后，
先按官方 marketplace `--create-new` 预览，再显式 `--force` 应用 workflow，最后
reapply preset。现有受管哈希与 `.new`/`.bak` 机制保留用户修改；AGENTS 用户区块
保持原样。源码更新不会自动更新旧安装；完整升级与 Release 矩阵仍由专门 Issue 承担。

跨独立审查者的工程执行事实采用与完整安装边界见 [MIGRATION-578](../../presets/guru-team/MIGRATION-578.md)；当前完整语义判断和结果绑定继续由原 owner 拥有。

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
Activation; engineering preparation follows implementation. Actual resolved Git
integration and the complete committed review remain with their original owners.

The `guru-team` canonical workflow is the global AI routing contract. The
canonical source is `workflow.md`; an installed `.trellis/workflow.md` is a
managed projection, not a second owner. Read the active Skill's `SKILL.md` and
Interface before invoking its step. The workflow supplies mandatory invocation,
unique typed-exit consumers and fail-closed routing; package owners supply
judgment and deterministic command details.

The first independent Architecture assessment and later independent
continuation use the existing
[Architecture Skill](../../skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md).
The [step-local contract](../../skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md)
owns reviewer method and input boundaries; this workflow routes the real result.
Delivery/Completion consume current conclusions and matching-stage eligibility.
Actual native and projection evidence is owned by [#404 Test](../../../docs/requirements-design-test-contributions/404-independent-architecture-review/test.md).

独立 Architecture `final_plan` 的完整显式对象由原 Skill 只读校验，不为一次性评审写 Task/Delivery 选择。普通执行恢复及相邻 Approval 保原选择合同。采用时更新同源 workflow 和完整 preset；见 [MIGRATION-694](../../presets/guru-team/MIGRATION-694.md)。源码与分发一致不代表现有业务安装或所有平台 Agent 已采用。

## 候选变化后的审核与验证

[唯一候选适用性合同](../../presets/guru-team/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage) 由七个原 owner 在各自职责内读取。
首次完整独立审核继续执行；后继候选以可核验原覆盖、全部差额和受影响依赖形成
当前完整结论。finding 闭合后不再无条件更换 reviewer 或重复完整相同审核。
各阶段仍须实际判断并产生原正式结果；工程命令事实与语义结论分别处理。
matching 安装、`fresh_final_review` 的窄后继含义及同 Delivery 在途恢复见
[MIGRATION-637](../../presets/guru-team/MIGRATION-637.md)。源码修改不代表活跃 Task 已迁移，静态分发不证明实际
Agent 行为或耗时改善。#636 已有接口需命中组合验证，#638 未来接口明确未验证。

## 提交后一次独立完整审核

当前顺序是实现/工程自检、必要知识整合、本地提交、一次独立完整 Review，
然后原 Delivery Review/readiness 与 Publication。未独立通过前不新 push、不创建 PR。
原 TaskCommit 的待审提交和干净重入保留精确事务、hook 与同提交恢复。
早期 Draft 新发布路径退出；既有 PR/HEAD 和已执行动作由原 owner 准确恢复，
pending 新远端动作回当前审核/readiness。完整版本、退休入口和在途处置见
[MIGRATION-794](../../presets/guru-team/MIGRATION-794.md)；不把旧 pass 机械转换为新通过。

## Current Lifecycle

```text
Intake -> task identity/scope -> Delivery creation -> Delivery Planning -> implementation
  -> engineering self-check / knowledge integration -> local Task Commit
  -> one independent complete committed Review
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

当前源码支持 Codex 独立显式调用受管的 `guru-orchestrate-issue-dag` 和
`guru-orchestrate-issue-sequence`，协调器 heartbeat 默认为 2 分钟。
两个入口默认静默执行；通知条件与原生静默输出方式见共享规范的
[Quiet Notifications](../../presets/guru-team/spec/workflow/issue-orchestration.md#quiet-notifications)。
DAG 支持跨仓节点及各仓项目、基线和环境恢复，保留单仓简写；Sequence 仍单仓严格串行。
它们协调多个 Issue，不加入本 workflow 的单 Issue mandatory phase。
完整完成 Issue 是目标；显式选定基线贯穿启动、PR 和完成证明，无关分支不要求同步。
分发、执行终点和个人安装迁移见
[Issue 编排迁移说明](../../presets/guru-team/MIGRATION-ISSUE-ORCHESTRATION.md)。

已发布稳定版本为 `v0.7.0-guru.8`，peeled commit 为
`2ab135ed2d3908966785bb23ad42ada0790f0c81`。默认稳定安装使用同一 immutable `.8`
tag 的 workflow marketplace `gh:castbox/guru-trellis/trellis#v0.7.0-guru.8`
和 preset checkout，并读取该 checkout 自身的 Fork lock 构建。该 tag 锁定
Fork `ca0e8b931d19ccb87802d6866abd2113a6f707c0` / CLI-Core
`0.7.0-castbox.6`，不包含下述 current-peer 修复。

当前修复源码的 extension 与 maintenance target 仍为 `0.7.0-guru.8`，但其内容与
已发布 `.8` tag 分开识别。本次不重发 tag、Release 或同版本 npm 包。
正式 Fork lock 固定到 `b4f1665143bd4ecf3a290d426ad62293fc13ea42`，
tree `9ba2f6c8a32f63fe9a6ca36ccc90f12b50d9cb67`，成功 main CI `42440325190`。
该来源包含 #40 维护能力、#43 旧原生 schema-1 会话元数据兼容修复、#47
Task/Delivery Git 对象读取优化、#50 公开 `GitCandidateContent` 不可变摘要能力及
#52 公开 `task_resume`，以及 #53 新进程 Python 选择与命令加参数执行修复。
本来源包含上游 #55 的正式 schema1 归档一次增代、固定操作恢复与无私有 receipt 的后继查询。
上游 #56 修复已验证后继与 registered sibling 共享快照的误冲突：同一正式前驱的同代或较早快照可被只读核验，仍返回所选 root 的实际 key/ref。
本来源另包含上游 #58 的 AGENTS 自定义正文维护能力，以及 #59/#60 的已保留旧 Delivery profile 合法停止修复。
本来源另包含上游 #62/PR #63 的 parent gitlink 原子身份修复，以及 #64/PR #65 的精简 known_legacy 正式归档后继能力。
本来源新增上游 PR #66 的 current-schema Task peer 迁移：mixed Plan2 通过
`defer/source_task_schema=2.0` 保留合法副本，由原 binding 与 live checkout 选择唯一
authority。peer 原 bytes/modes 保留，不进入 lifecycle、session、Delivery 或私有转换。
匹配构建、目标安装和各专项验收须分别核验，source lock 更新不证明这些步骤通过。
CLI/Core 为 `0.7.0-castbox.6`，package manager 为 `pnpm@10.32.1`。
这些来源身份不替代实际目标安装、Guru 集成或各专项验收。
已有 Fork `.4` tarball `castbox-v0.7.0-castbox.4` 属于历史配对来源，
不证明当前 lock 的匹配构建。使用干净 source workspace 的正常 CLI/Core 依赖布局，
保留模板原 mode；不以相同版本号选择另一构建或放宽 `source_locked`。

源码试用的 workflow marketplace 与 preset 必须使用同一个真实、远端可寻址的完整
Guru candidate SHA，再从该 SHA 的 lock 构建。已发布 `.8` tag 不包含本次修复，
不能用该 tag 或相同 extension/CLI 版本号代替所选修复 SHA。
当前源码、投影及代表性安装各保留其真实来源和验证边界，不证明新 Release 通过。
未来正式发布仍由独立 Release owner 冻结 exact commit/tree，执行所需安装与
predecessor 验证，再分别完成新 tag、tag-pinned smoke、Release 和对应 Issue closure。
历史验收不替代新候选门禁；完整多平台矩阵与真实业务、生产验证保持独立。

已发布 `.8` 的准备集合由 `v0.7.0-guru.7` 到该 Release candidate 的完整 diff 确定。
该准备差额包括 #687 的固定 Fork `.6` 采用，#690/#694/#697 的 Architecture 出口、
显式对象与机制采用审核，#692/#695 的 Intake 和 JSON 输入诊断，以及 #693 的合同承接
与验证证据方法。#706/#717 收敛独立多视角审核与审核充分性；#709/#731 完善 Issue 编排
和协调者解阻；#710/#713 收敛 Phase 2 authoring 与公共执行合同。#711 隔离知识导航写入，
#718 解耦共享环境与运行位置，#724 将 Codex 公共 Skill 迁入共享根，#735 完善行为测试
与因果验证，#739 修复父仓 gitlink 原子候选与 resolved 合并承接。上述源码和合同变化的
具体交付范围由完整 diff 与原专项证据确定；它们不替代本次候选安装或发布验证。

以下前序能力保留原验证来源和层次：

- [#630 Test](../../../docs/requirements-design-test-contributions/630-native-compatibility/test.md)
  记录三系统 Python runtime、安装、维护脚本和公开 wrapper；Windows 实际 Agent
  会话仍未完成，其超时和早期失败保持原结果，该会话不属于 #630 当前脚本验收范围。
- [#649 Test](../../../docs/requirements-design-test-contributions/649-stage-result-convergence/test.md)
  保留独立对照、受控连续 Delivery 样本、合法路线差异、false/no-grade 及历史失败。
  已完成该 Issue 不表示每个样本通过，也不证明正式来源维护、业务采用或生产 E2E。
- [#669 Test](../../../docs/requirements-design-test-contributions/669-existing-implementation-reactivation/test.md)
  的受控原生 Task2 恢复样本、真实 SDK 回归及 local_candidate 维护各有独立边界；
  它们不证明 source_locked 维护、真实 GitHub/backend #802 或业务生产恢复。

这些结果不代替本次 exact-candidate、tag-pinned smoke 或完整多平台 Release 矩阵。
原 Test 的历史观察不因准备版本更新而回写。

历史已发布 `v0.7.0-guru.1` 所锁定 Fork 的 update 会在访问旧 `0.6.17` 项目数据前拒绝，原数据保持不变。
已发布 `v0.7.0-guru.1` 不支持旧安装原地升级；拒绝不代表升级成功。
历史 `.3` 系列迁移能力（extension `0.7.0-guru.3` / Fork `0.7.0-castbox.3`）通过独立 standalone
`guru-upgrade-installation` 承接全部 `v0.6.x-guru.*` 与 `v0.7.0-guru.*` 正常安装；
显式升级请求从目标 source package 加载该 Skill，不先进入 business Intake。
见 [迁移说明](../../presets/guru-team/MIGRATION-495.md)；历史 Guru `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的同源远端验收绑定原 Fork `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / CI `37647767799`，由 [唯一系列 Test](../../../docs/requirements-design-test-contributions/495-upgrade-version-families/test.md) / EVD-051 承接，不证明当前新来源，普通 update/reapply 不替代迁移，普通 runtime 无兼容双读或自动迁移。
迁移保留业务定制、无关 dirty/untracked 与合法当前任务状态；legacy nonterminal 的 pinned-old/deferred 处置及 rollback 恢复实际升级前来源的边界保持 [迁移说明](../../presets/guru-team/MIGRATION-495.md) 合同。
当前知识 authority 为 `guru-trellis-rdt` / `guru-trellis-architecture`，从
`docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md`
与 `docs/architecture/README.md` 读取完整适用单元及 Git revision，与软件版本分开。

For current-source validation, use the source-locked Trellis Fork checkout
(`castbox/Trellis@b4f1665143bd4ecf3a290d426ad62293fc13ea42`, successful main CI
`42440325190`) and that same reviewed Guru source. Stable `.8` installation
uses its original source pair described above. For a local installation, compare the canonical `workflow.md` with
the target `.trellis/workflow.md` and preserve target edits before applying
it. For a target meeting the ordinary current-only installation prerequisites,
apply the Guru preset using
`trellis/presets/guru-team/scripts/bash/apply.sh --repo <target>` and validate
the installed graph. For tools-only updates in an existing checkout, including
dogfood synchronization with Task/session preservation, load the complete
[`guru-upgrade-tools` contract](../../skills/guru-team/packages/guru-upgrade-tools/references/contract.md).
The AI chooses the owner from the actual request and target state; an old-Task
apply diagnostic does not expand a tools-only request into historical migration.
Full installation/migration keeps its original owner and gate. The repository
root README and source lock identify the exact CLI build. Remote marketplace
installation is not a #434 gate.

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

三个原 qualifier 各自拥有 `references/applicability.md`；原 caller 在加载全文前
读取条件，独立判断是否触发。触发且无仍适用结论时显式调用原 stable Skill；
未触发不作空判定。十类 lifecycle profiles 及已有 Author profile 保留原 consumer。
`guru-qualify-root-cause` 承接 caller 当前场景、authority-placement 判断与实际
触发的上游结果，不要求正确未触发的 qualifier 产生结果。根因未知的有界诊断可以
继续；有独立效果、风险、owner 和退出依据的缓解保留 `mitigation_only`。
修复证据不足返回诊断，症状抑制只返回机制移除/替换。四出口为
`classified`、`mechanism_revision_required`、`diagnosis_required`、`blocked`。
同机制结论仍适用时由后续阶段消费；新/实质变化机制重新资格。阶段仍审当前
实现和证据，qualification 不等于完成，#383 拥有共同完成语义。

完整采用与在途接续见 [MIGRATION-793](../../presets/guru-team/MIGRATION-793.md)。
适用条件由各原包独占，README 不复制资格判据。

七类 Task/Delivery 资格输入现选 input 2.0 / aggregate 3.0，显式传递原完整
DeliveryKey，并复用原身份和当前选择校验。原 caller 持有本次调用对象并消费
原出口后继续当前阶段。旧发布输入保持历史字节；采用与在途恢复见
[MIGRATION-812](../../presets/guru-team/MIGRATION-812.md)。已有 Task 的工具更新由原 `guru-upgrade-tools`
执行，保留 Task/session；安装投影一致不代替实际 caller 验收。

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

`guru-upgrade-tools` 与 `guru-maintain-legacy-task` 从完整匹配来源加载，分别处理工具更新、所选Task转换、人工旧归档恢复或仅历史保留；目标旧parser和Reconcile不成为维护启动前置。原完整Plan2保持独立。只更新显式目标，省略时先按既有配置与dev/develop/main/master/远端默认分支选分支，再绑定唯一checkout。

当前正式 source lock 已包含上游 #40 与 #43。`source_locked` 仍要求完整匹配、已提交且干净的 Guru 来源及成功的匹配 Fork 构建；来源锁变化不等于目标已升级。历史 `local_candidate` 仅为隔离开发证据，不证明正式来源维护、业务恢复或发布。入口、最小I/O成套切换、原owner核验/退役、native验证和兼容回退边界见 [MIGRATION-566.md](../../presets/guru-team/MIGRATION-566.md)。

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
#577 当时未修改正式 source lock，本地 matching candidate 只用于隔离开发。
当前正式来源以本页来源记录为准；历史兼容边界详见
[兼容与依赖边界](../../presets/guru-team/MIGRATION-577.md)。

## 已有实现分支恢复（#669）

已有实现提交、本地差额及原 Draft PR 的正式归档恢复，进入原
`guru-reactivate-task` 的独立 `delivery_reactivate_existing_implementation`
profile。原 clean-base profile 保持；入口、同操作接续、matching 安装和验证边界见
[迁移合同](../../presets/guru-team/MIGRATION-669.md)。恢复身份后由原 Task/Delivery owners 审核当前工作。

## 配置生成的 worktree 路径（#760）

AI 自行新建 linked worktree 时，先读取 live Git topology 与确证 primary 的
`.trellis/guru-team/config.yml`。空 `worktree_root` 使用
`<primary-parent>/<primary-name>-worktrees`；相对值相对 primary 根解析，绝对值直接采用。
从 primary、linked 或 detached 调用均使用同一项目锚点。不能以调用 cwd、common-dir
父目录或 porcelain 首行代替确证；锚点不可确证或配置冲突时按诊断修正，不自动覆盖配置。

公开 `guru-select-workflow-mode/scripts/check-env.sh --root <checkout> --json`
返回解析后的绝对 `worktree_root`。传 `--worktree-name <name>` 生成目标，再传
`--checkout-root <absolute-plan>` 可在创建前核对计划。正式 Task 的 AI 生成计划使用
`acquisition.path_source=configured`、单目录 `worktree_name` 和该绝对路径，原 executor
在任何创建副作用前再次核对。task-free 由原 owner 消费预检目标，继续普通 Git 创建并读回实际目录与注册。

真实显式新位置仍可在生成 root 外；AI 自填绝对值不代表调用方指定位置。已有 checkout
采用与原 Task 恢复保留原位置和身份检查，配置变化不触发搬移。
旧省略字段的绝对路径输入、受影响 callers 和成套更新边界见 [MIGRATION-760](../../presets/guru-team/MIGRATION-760.md)。
源码修改不表示已有安装已采用；已有 checkout 通过 `guru-upgrade-tools` 更新完整 matching
工具投影并验证 drift/sidecar，保留 Task/session 和用户配置。完整多平台安装、升级及 Release
矩阵不属于本项验证范围。

当前完整 Review 对范围内规划修复传递真实 actions；原旧 Check rollback 仅通过显式恢复入口承接。
完整 matching 采用、已回退旧现场、缺来源 blocked 及验证边界见
[MIGRATION-775](../../presets/guru-team/MIGRATION-775.md)；恢复不生成 Planning 或 Check pass。
