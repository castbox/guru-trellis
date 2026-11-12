# Guru Team Preset

当前出口查询复用 `discover-skill-contract` 的 `--skill <id> --exit <id>`。
完整路由正文由 workflow 显式引用，preset 将 `references/routing.md` 和
`references/legacy.md` 安装到 `.trellis/guru-team/references/`。
查询返回原 consumer、入口及前置合同；AI 仍须显式加载并执行原 owner。
已有 checkout 通过 `guru-upgrade-tools` 完整更新匹配的 workflow、runtime、引用及受管投影，
保留 Task/session，并处理 `.new`/`.bak`。迁移和普通错误恢复见
[MIGRATION-792](MIGRATION-792.md)。源码分发不证明实际 Agent 已采用，也不代表完整安装/升级矩阵通过。

Codex 的 Guru Skill 使用共享 `.agents/skills/`；新安装/reapply 不再创建受管 `.codex/skills/guru-*/`。专属编排包及 `agents/openai.yaml` 仍由目标 exact platform selection 决定，保留显式调用与原生能力前置。旧安装经原维护 owner 在目标完整后退出旧受管文件，保留用户修改并处理冲突；详见 [MIGRATION-724](MIGRATION-724.md)。

只读 Intake 通过原 `guru-sync-base` 的 `operation=read` 采用明确 Git 来源，
再由 Discovery 读取固定 tree 和独立草案。实际同步继续使用 `operation=sync`
并保留原 clean/ff/identity 检查。公开版本、投影及旧安装边界见 [MIGRATION-718](MIGRATION-718.md)。

normal/solution资格确认的真实context循环按完整matching包、共享consumer、workflow/routing和声明平台投影采用。
Task确认对象与来源authority分别保留；原工具owner负责已有checkout受管更新和目标验证。
版本、旧在途恢复及证据边界见 [MIGRATION-811](MIGRATION-811.md)，各原Skill保语义门禁和内部行为。

跨 Issue 编排通过 Codex 显式调用 `guru-orchestrate-issue-dag` 或
`guru-orchestrate-issue-sequence`。当前源码将它们作为受管 `standalone_only` 包分发，
DAG 可处理跨仓显式或动议正式绑定依赖图；Sequence 保持单仓严格串行。
DAG 按仓核项目、基线及环境，保留旧单仓简写。默认协调器 heartbeat 为 2 分钟。
始终以完成 Issue 为目标；显式基线用于启动、PR 和完成证明，无关分支不要求同步。
入口边界、同源规范、个人副本迁移及验证范围见
[Issue 编排迁移说明](./MIGRATION-ISSUE-ORCHESTRATION.md)。

审核、审查、评审、复审和 review 先按对象与目的分流。代码、PR、测试覆盖和
需求实现情况的审核，再区分独立只读审核与正式阶段结果。无论有无
Task/Delivery，独立审核都显式调用 `guru-review-change`，由它保留指定范围并返回
用户报告，不创建 Task、推进生命周期或生成正式 Guru pass。
workflow 调用或用户要求正式阶段结果时，才按原前置与完整范围进入
提交后完整 Review 或 Completion。普通 review 关键词和 Task 存在本身
不选择正式门禁。专项选择方法唯一见
[Specialist Review Standards](./spec/workflow/quality-guidelines.md#specialist-review-standards)。
`guru-ai-guides` 的需求、概要设计、详细设计、Go-Guru 实现与集成测试计划审核
提供适用标准和方法；它们未被通用流程门禁替代，也不随本 preset 安装。
按项目技术栈、已采用标准和当前产物选择实际需要的 Skill 及同源标准包，
专项结果由原 Guru owner 在自己的职责内审查，不能替代正式阶段结论。

行为测试、因果验证、证据采用和实验停止的共同方法见
[Test And Validation Value](./spec/workflow/quality-guidelines.md#test-and-validation-value)。
Author、实施派工和提交后完整 Review 在原职责内采用该方法。

Issue 内容、需求本身和动议本身的审核不进入 `guru-review-change`；它们保留
现有 Issue、需求专项或项目动议/上游需求入口，Git 文件是否有改动不改变该边界。
“审核需求是否已被代码和测试实现”属于实现审核。仅有 review 动词时承接明确的
对话对象；对象不明时先澄清。完整入口选择以 workflow 为准。

完整 preset 分发 `guru-review-change` 的独立合同、共享审核方法和无状态只读命令。
它可审核未安装 Trellis 的 Git 仓库，输入选择工作区或已提交范围及可选路径。
`reviewed` 表示完成本次审核，可以包含 Findings；它不代表正式门禁通过。
共同覆盖与结束规则由 [审核充分性规范](./spec/workflow/review-sufficiency.md) 唯一维护，
安装到 provider 的 `.trellis/spec/workflow/review-sufficiency.md`，由各原审核 owner 加载。
提交后完整 Review 另读同源工程方法组合，并继续各自的正式流程。
组合读取 Architecture、current-knowledge 和专题 SSOT，不读取 Check/Branch 的私有阶段方法。
原 owner 仍须实际形成架构基线吻合度、基线规则适用性和需求实现覆盖结论。原 Architecture 独立读序、适用性与重审规则继续生效；无 Task
独立审核不调用或伪造正式 Task/Delivery 架构结果。
独立审核的不同角度由多个独立 subagent 实际执行，最终 owner 核对证据并汇总判断。
原正式阶段的 worker 政策保持在各自 owner 内。

已有安装需要更新匹配的 marketplace workflow 并完整 reapply preset，才能采用
本次共同规范、十二个审核消费者与工程方法迁移。专项 Skills 在其
原来源单独维护和安装；缺少当前必须的专项证据时明确受影响结论，不静默降级。
继续检查受管投影、drift 和 `.new`/`.bak`，保留用户修改。源码与分发检查不证明
真实 Agent 已采用，也不代表完整多平台 upgrade/update 或 Release 矩阵通过。

JSON 载体读取、Bind 双 stdin 冲突与完整正常调用见
[MIGRATION-695](MIGRATION-695.md)。共享 reader 保留原合法 inline、stdin 和普通文件；
各入口仍遵守自身准入，不支持进程替换。已有安装须采用完整匹配 preset。

局部修复的实际影响判断见原 [selector 合同](../../skills/guru-team/packages/guru-select-workflow-mode/references/contract.md)。
调查事实复用与 Discovery record/check/invoke 的字段诊断见原
[Discovery 合同](../../skills/guru-team/packages/guru-discover-change-context/references/contract.md#current-owner-mismatch-diagnostics)。
同批更新原 owners、runtime 和调用声明，再按受管机制 reapply 并检查 installed、
平台投影、drift 与 sidecar；不把源码或分发结果当作外部业务采用或耗时改善证明。

明确 Task/Delivery 的接收会话通过原 Identity/Ensure/Bind/Selection 补齐自身缺失事实，
再继续同对象原未完义务。Planning 首失败诊断、standalone producer 身份构造，以及
带实际 key 的 Human artifacts 展示须成套采用。具体诊断字段、Task-only/archive
分支、matching 安装和分层验证边界见 [MIGRATION-679](MIGRATION-679.md)。

当前正常流程的 repair 投影、归档 Review example、首次 before authority 缺失及
final promotion 的 Bootstrap 回程，采用三个原 owner 的匹配当前合同。
直接演进、旧合法输入及成套安装边界见 [MIGRATION-663](MIGRATION-663.md)。

活动Task续接通过当前身份、合法binding/checkout及实际阶段owner准入，原created只服务初始创建区间。Delivery created wire保持；原consumer重读公共phase，planning才进适用Author，其余沿唯一continuation。范围修订按pre-Author→根PRD Author→Clarify acceptance→post-Author两次承接，退役status/DTO不成为current前置。完整matching切换、在途恢复及证据边界见 [MIGRATION-657](MIGRATION-657.md)。源码修改不证明已有安装或实际Agent已采用。

当前知识读写的唯一共享正文位于原 RDT package 的
[current-knowledge.md](../../skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md)。
两维护 Skills 实际读取同一文件；原递归 package 安装分发，无新 runtime API。
完整单元、真实两层技术栈源、本仓库迁移与旧 Task 读取边界，以及完整匹配安装、
update/reapply 和项目投影责任见 [MIGRATION-331](MIGRATION-331.md)。分发一致、
真实 Agent 正确读写与成本改善、业务采用分别验证，不能互相代替。

Issue 创建与修订的共同内容正文由原 Clarify package 的
[Issue 内容编写规范](../../skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md)
唯一维护。四个原 Issue owners 实际读取同一安装正文及清晰写作规范，继续各自的
写作、审核与创建职责。原递归 package 分发安装正文及 `examples/issue-content/`
教学示例；示例和分发检查不代替实际 Agent 行为或创建、修订后的回读证据。
已有安装须完整采用匹配的 preset 与四个原 packages，再检查 reapply、投影、drift
及 sidecar；源码更新本身不证明旧安装已经采用。

原知识 owners 在工程自检后、提交前整合必要文档并读回；整合事实等待提交后独立审核。
原 `guru-review-branch` 在固定提交上一次完成 Check 与 Branch Review 的全部适用职责，
包括一次实现后独立 Architecture 判断，再由原 Delivery Review 记录 readiness。
普通晋升保留稳定 identity、single-writer 和实际 expected-current/readback；
当前与在途采用边界见 [MIGRATION-794](MIGRATION-794.md)，历史来源和原验证截止点保持。
源码变更不证明安装、实际 Agent 行为或外部采用。

并行知识采用稳定入口、限定目录及稳定 ID 查找完整正文；独立主题不在共享入口逐项登记。
共同方法、既有项目切换条件、未迁移范围、在途最终整合与旧写退出见
[MIGRATION-711](MIGRATION-711.md)。安装新规则与项目文档切换分别完成。

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

单 checkout 的 tools-only 升级由 `guru-upgrade-tools` 承接。调用方显式提供
`AGENTS.md` 的 custom 基底正文与原文件快照；Guru 在公共 prepare 前更新其中的
规则块，公共计划返回后保持不变。目标 Fork 须声明 `tools_custom_instruction`
能力；缺失能力或最终内容被 `update.skip` 保留为旧块时，准备阶段停止。
旧失败操作先由未变的原来源合法处置，再从修复来源重新准备；不转换旧 checkpoint。

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

Normal revision/recovery contracts live in `guru-review-branch` and
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
First assessments and later independent continuation follow that contract;
platform entries load and schedule the same owner. Install/update must reapply the matching complete
preset so canonical, installed and selected platform copies use the same method.
Projection checks and actual native behavior are separate evidence; current
#404 coverage and limitations live in its [unique Test](../../../docs/requirements-design-test-contributions/404-independent-architecture-review/test.md).

独立 Architecture `final_plan` 的完整显式对象由原 Skill 只读校验，不为一次性评审写 Task/Delivery 选择。普通执行恢复及相邻 Approval 保原选择合同。采用时更新同源 workflow 和完整 preset；见 [MIGRATION-694](MIGRATION-694.md)。源码与分发一致不代表现有业务安装或所有平台 Agent 已采用。

## 候选变化后的审核与验证

[唯一候选适用性合同](spec/workflow/workflow-contract.md#candidate-applicability-and-coverage) 由七个原 owner 在各自职责内读取。
首次完整独立审核继续执行；后继候选以可核验原覆盖、全部差额和受影响依赖形成
当前完整结论。finding 闭合后不再无条件更换 reviewer 或重复完整相同审核。
各阶段仍须实际判断并产生原正式结果；工程命令事实与语义结论分别处理。
matching 安装、`fresh_final_review` 的窄后继含义及同 Delivery 在途恢复见
[MIGRATION-637](MIGRATION-637.md)。源码修改不代表活跃 Task 已迁移，静态分发不证明实际
Agent 行为或耗时改善。#636 已有接口需命中组合验证，#638 未来接口明确未验证。

## 提交后一次独立完整审核

当前顺序是实现/工程自检、必要知识整合、本地提交、一次独立完整 Review，
然后原 Delivery Review/readiness 与 Publication。未独立通过前不新 push、不创建 PR。
原 TaskCommit 的待审提交和干净重入保留精确事务、hook 与同提交恢复。
早期 Draft 新发布路径退出；既有 PR/HEAD 和已执行动作由原 owner 准确恢复，
pending 新远端动作回当前审核/readiness。完整版本、退休入口和在途处置见
[MIGRATION-794](MIGRATION-794.md)；不把旧 pass 机械转换为新通过。

## 构建所选 Fork

新仓安装前，先将 `GURU_SOURCE` 设置为所选 Guru tag 或完整 candidate SHA 的
checkout，设置 `FORK_SOURCE` 为本机 Fork 源码目录。下列命令读取该 checkout
自身的 source lock，不使用本页历史正文中的 SHA。已有 Fork checkout 会复用；
尚未取得源码时才 clone。先安装 Fork `package.json` 要求的 Node.js，以及
source lock 声明的 package-manager 版本。

```bash
(
  set -e
  : "${GURU_SOURCE:?请设置所选 Guru 源码目录}"
  : "${FORK_SOURCE:?请设置 Fork 源码目录}"
  SOURCE_LOCK="$GURU_SOURCE/trellis/presets/guru-team/source/trellis-source.json"
  FORK_REPOSITORY="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["repository"])' "$SOURCE_LOCK")"
  FORK_COMMIT="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["commit"])' "$SOURCE_LOCK")"
  FORK_PACKAGE_MANAGER="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["package_manager"])' "$SOURCE_LOCK")"
  test "pnpm@$(pnpm --version)" = "$FORK_PACKAGE_MANAGER"
  if ! git -C "$FORK_SOURCE" rev-parse --git-dir >/dev/null 2>&1; then
    git clone "$FORK_REPOSITORY" "$FORK_SOURCE"
  fi
  FORK_STATUS="$(git -C "$FORK_SOURCE" status --porcelain)"
  test -z "$FORK_STATUS"
  git -C "$FORK_SOURCE" fetch "$FORK_REPOSITORY" "$FORK_COMMIT"
  git -C "$FORK_SOURCE" checkout --detach "$FORK_COMMIT"
  test "$(git -C "$FORK_SOURCE" rev-parse HEAD)" = "$FORK_COMMIT"
  cd "$FORK_SOURCE"
  pnpm install --frozen-lockfile
  pnpm build
  git rev-parse HEAD > packages/cli/dist/.guru-source-commit
  node packages/cli/bin/trellis.js --version
)
```

保留 Fork 的正常 ESM/workspace 依赖布局和模板 mode，不复制 dist 或重造 launcher。
任一步失败即停止，不把版本输出或旧 dist 当作匹配构建。
`.guru-source-commit` 记录成功构建的源码 HEAD，用于识别同版本 stale dist；
单独校验时不补写该标记。随后使用
`node "$FORK_SOURCE/packages/cli/bin/trellis.js"` 执行匹配版本的公共 CLI。

## Apply And Verify

已发布稳定版本为 `v0.7.0-guru.8`，peeled commit 为
`2ab135ed2d3908966785bb23ad42ada0790f0c81`。默认稳定安装使用同一 immutable `.8`
tag 的 workflow marketplace `gh:castbox/guru-trellis/trellis#v0.7.0-guru.8`
和 preset checkout，并读取该 checkout 自身的 Fork lock 构建。该 tag 锁定
Fork `ca0e8b931d19ccb87802d6866abd2113a6f707c0` / CLI-Core
`0.7.0-castbox.6`，不包含下述 current-peer 修复。

当前修复源码的 extension 与 maintenance target 仍为 `0.7.0-guru.8`，但其内容与
已发布 `.8` tag 分开识别。本次不重发 tag、Release 或同版本 npm 包。
Fork 的 repository、commit、tree、CI identity、CLI version 与 package manager
统一读取所选 Guru checkout 自身的 [source lock](source/trellis-source.json)。
本页不另存当前 SHA/CI 对照表；按[构建所选 Fork](#构建所选-fork)核验实际构建。
该来源包含 #40 维护能力、#43 旧原生 schema-1 会话元数据兼容修复、#47
Task/Delivery Git 对象读取优化、#50 公开 `GitCandidateContent` 不可变摘要能力及
#52 公开 `task_resume`，以及 #53 新进程 Python 选择与命令加参数执行修复。
本来源包含上游 #55 的正式 schema1 归档一次增代、固定操作恢复与无私有 receipt 的后继查询。
精简 known_legacy 正式归档能力已随上游 #64/PR #65 合入当前正式 lock。
Guru 消费公共家族/key 及目标 native 前驱关系；AI 仍审核原安装/Finish、历史范围及 PR/Git。
原档不改写，人员字段只保留为历史资料。实际 `source_locked` 安装、真实业务恢复和 Release 仍需分别验证。
上游 #56 修复已验证后继与 registered sibling 共享快照的误冲突：同一正式前驱的同代或较早快照可被只读核验，仍返回所选 root 的实际 key/ref。
本来源另包含上游 #58 的 AGENTS 自定义正文维护能力，以及 #59/#60 的已保留旧 Delivery profile 合法停止修复。
本来源另包含上游 #62/PR #63 的 parent gitlink 原子身份修复，以及 #64/PR #65 的精简 known_legacy 正式归档后继能力。
本来源新增上游 PR #66 的 current-schema Task peer 迁移：mixed Plan2 通过
`defer/source_task_schema=2.0` 保留合法副本，由原 binding 与 live checkout 选择唯一
authority。peer 原 bytes/modes 保留，不进入 lifecycle、session、Delivery 或私有转换。
匹配构建、目标安装和各专项验收须分别核验，source lock 更新不证明这些步骤通过。
CLI/Core 与 package-manager 版本采用同一 source lock 声明的值。
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
历史 `.3` 系列迁移能力（extension `0.7.0-guru.3` / Fork `0.7.0-castbox.3`）提供独立 semantic
`guru-upgrade-installation`，支持全部 `v0.6.x-guru.*` 与 `v0.7.0-guru.*` 正常安装，
按实际 receipt/ownership/core/task 差异分组；从固定目标 source package 加载，不先进入
business Intake，普通 apply 保持严格。
支持来源、固定依赖前置条件和验收状态见 [MIGRATION-495.md](./MIGRATION-495.md)。
历史 Guru `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的同源远端验收绑定原 Fork `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / CI `37647767799`，由 [唯一系列 Test](../../../docs/requirements-design-test-contributions/495-upgrade-version-families/test.md) / EVD-051 承接，不证明当前新来源；
普通 update/reapply 不替代迁移，普通 runtime 无兼容双读或自动迁移。
迁移保留业务定制、无关 dirty/untracked 与合法当前任务状态；legacy nonterminal 的 pinned-old/deferred 处置及 rollback 恢复实际升级前来源的边界保持 [迁移说明](./MIGRATION-495.md) 合同。
当前知识 authority 为 `guru-trellis-rdt` / `guru-trellis-architecture`，从
`docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md`
与 `docs/architecture/README.md` 读取完整适用单元及 Git revision，与软件版本分开。

For current-source validation, read the selected Guru checkout's own
[source lock](source/trellis-source.json), verify its source and CI identity,
and build that exact Fork commit. Use its CLI with that same reviewed Guru source.
Stable `.8` installation uses its original source pair described above. For the local workflow sample, compare the canonical `workflow.md`
with the target `.trellis/workflow.md` and preserve target edits before
applying it. For a target meeting the ordinary current-only installation
prerequisites, run:

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo <target>
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root <target> --mode installed --json
```

For tools-only updates in an existing checkout, including source-repository
dogfood synchronization, load the complete
[`guru-upgrade-tools` contract](../../skills/guru-team/packages/guru-upgrade-tools/references/contract.md).
The AI selects that owner from the requested scope and actual target state.
An ordinary apply blocked by old Tasks does not make historical migration part
of a tools-only request; preserve the records and follow the selected owner's
preconditions. Full installation/migration retains its original owner and gate.

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

当前 Git `pull_request` Delivery 的完整 Candidate 由原公开
`construct-delivery-candidate.sh` 入口构造。原 Author/implementation owner
选择 B、实际 HEAD 和 dirty paths；执行器复用原固定范围与内容算法，返回既有
Candidate，不写阶段或 gate。完整参数、输出、begin-check/rework、scope 与 stop
恢复见 [原步骤合同](../../skills/guru-team/packages/guru-author-task-plan/references/authoring.md#fixed-delivery-range)。
原上游 candidate 的 content_ref 输出及 git_free consumer 保持原边界，不增加
无 Git Delivery。新入口、nested runtime、workflow 和原 Skill 正文须随完整
matching preset/tools 更新采用；源码存在不证明目标安装或实际 Agent 验收通过。

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

完整采用与在途接续见 [MIGRATION-793](./MIGRATION-793.md)。
适用条件由各原包独占，README 不复制资格判据。

七类 Task/Delivery 资格输入现选 input 2.0 / aggregate 3.0，显式传递原完整
DeliveryKey，并复用原身份和当前选择校验。原 caller 持有本次调用对象并消费
原出口后继续当前阶段。旧发布输入保持历史字节；采用与在途恢复见
[MIGRATION-812](./MIGRATION-812.md)。已有 Task 的工具更新由原 `guru-upgrade-tools`
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
受管环境 patch 与 Homebrew 最新版本同步。日常 Skill 按实际工具需求验证并选择已有共享 cache；
无自动 pointer 的普通 worktree 也可发现匹配环境。有效 hint 或真实显式类别不因 Homebrew/PATH 更新
自动变化，也不退回全局 site-packages。旧 identity 不自动清理。

激活前必须完成 hash-locked 依赖安装、Draft 2020-12 probe、真实公开 schema wrapper
正/普通不完整输入检查，以及完整 staged source/installed 验证。wrapper 的隔离 capability
fixture 只证明传输/运行能力，不代表用户业务语义判断。安装或 runtime-check 失败时保留
原合法选择和原环境；同 identity repair 也在检查通过后才替换旧环境。
当前选择写入 checkout-private selection-v3.json，旧 active.json 原文保留给旧消费者。
仅当新载体不存在时一次迁移旧有效选择；日常缺环境不会隐式安装。独立公开入口为：

```bash
.trellis/guru-team/runtime/manage-python.sh . .trellis/guru-team/runtime --check --json
.trellis/guru-team/runtime/manage-python.sh . .trellis/guru-team/runtime --repair --python /path/to/python3 --json
```

从完整 matching source 恢复时，把实际目标 repo 和该来源 runtime assets 显式传给同一脚本。
格式、稳定选择、直接 consumer 和原维护回滚的完整边界见 [MIGRATION-718](MIGRATION-718.md)。

| 错误 code | 修复和重试 |
| --- | --- |
| `interpreter_unavailable` | 运行 `command -v python3` 和 `python3 --version`；检查可执行权限，或用上面的 `--python /path/to/python3` 明确选择。 |
| `python3_required` / `python_implementation_unsupported` | 选择可运行的 CPython 3；不修改框架 manifest 来添加 minor。 |
| `venv_bootstrap_failed` | 检查所选 Python 的 `-m venv` / ensurepip 支持，再使用同一环境 repair 命令。 |
| `dependency_install_failed` | 检查 PyPI 访问及锁定依赖对所选解释器的 wheel 可用性，再通过环境 repair 重试；可显式选另一 CPython 3，不改 lock 或系统 Python。 |
| `runtime_not_bootstrapped` / `managed_runtime_missing` / `explicit_runtime_unavailable` | 先运行独立 `--check`，再由原环境 owner 执行 `--repair`；显式类别失配不静默换环境。 |
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
#577 当时未修改正式 source lock，本地 matching candidate 只用于隔离开发。
当前正式来源以所选 Guru checkout 自身的 [source lock](source/trellis-source.json) 为准；历史兼容边界详见
[兼容与依赖边界](./MIGRATION-577.md)。

## 已有实现分支恢复（#669）

已有实现提交、本地差额及原 Draft PR 的正式归档恢复，进入原
`guru-reactivate-task` 的独立 `delivery_reactivate_existing_implementation`
profile。原 clean-base profile 保持；入口、同操作接续、matching 安装和验证边界见
[迁移合同](MIGRATION-669.md)。恢复身份后由原 Task/Delivery owners 审核当前工作。

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
旧省略字段的绝对路径输入、受影响 callers 和成套更新边界见 [MIGRATION-760](MIGRATION-760.md)。
源码修改不表示已有安装已采用；已有 checkout 通过 `guru-upgrade-tools` 更新完整 matching
工具投影并验证 drift/sidecar，保留 Task/session 和用户配置。完整多平台安装、升级及 Release
矩阵不属于本项验证范围。

当前完整 Review 对范围内规划修复传递真实 actions；原旧 Check rollback 仅通过显式恢复入口承接。
完整 matching 采用、已回退旧现场、缺来源 blocked 及验证边界见
[MIGRATION-775](MIGRATION-775.md)；恢复不生成 Planning 或 Check pass。
