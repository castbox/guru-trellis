# Research: #154 真实 Codex Planning 验证执行路径

- Query: 为已批准 I5 找到 V1–V7 的最小合法真实 Agent 执行路径；宿主不预写最终正文、pass 或公共 lifecycle 事实。
- Scope: mixed
- Date: 2026-10-18

## Findings

### 当前可执行子集与判断边界

V1、V3、V4、V6 的正常本地 Planning 可以不写 GitHub；V2 已核实真实 OPEN 候选 #331，仍待原 Discovery/Clarify 判断当前差额和必要选择。它们仍需要主会话确认的本地资源：一个匹配安装目标、原 owner 创建的必要 Task/Delivery、branch/checkout association，以及实际 Codex 会话。去敏来源快照只能按其真实角色使用，不能冒充 V1/V2 的 live Direct Source，也不能由宿主预填最终 PRD 或用户回答。V2/V4 的真实选择若尚未回答，必须保留对应缺口。V3 使用原 no_issue/standard Intake，不制造 GitHub Issue。

V7 可以无 GitHub 写入完成，但不能保证首次生成一定出现遗漏。使用实际 Agent 初稿或原入口支持的未完成规划；原 reviewer 必须满足其原前置条件。只有 reviewer 实际指出具体缺口、原 Author 实际修订并重审，才有该场景证据。不能为了取得 V7 强制 writer 返回不真实的 plan_ready，也不能删除已接受正文或重放宿主预填的 revision/pass。若本轮没有合格草稿或原 reviewer 前置不足，记录 provider/场景缺口，不能把自检或 wrapper pass 改称原审核闭环。

V5 的历史数据恢复路径缺少前置事实。后续核对确认了另一条原合同支持的候选：同一隔离仓库以 scratch base 承接一个真实 no_issue fixture Task，partial D1 经实际 PR 交付，原 Completion/Creation 进入 D2 Planning。见文末最新执行方案。本研究未实际运行该链，不计行为通过。

### 真实平台入口

已运行只读 `codex --version`、`codex exec --help`，当前 `/opt/homebrew/bin/codex` 为 `codex-cli 0.162.1`。CLI 支持 `exec -C <target> -s workspace-write --json -o <final> -`，prompt 可从 stdin 输入。使用配置默认模型，无需新指定模型。

建议每个实际 writer/reviewer 使用原 installed Skill，并保留 stdout JSONL、stderr 和最终文字。CLI 是现有真实 Agent provider；不新增公共 harness、owner 或 DTO。独立 Architecture assessment 仍遵守其 fresh generic subagent/read-order，不能用已经读过 PRD 的 writer 冒充独立 owner。

V6 启动第二次普通 `codex exec`，以新的 `thread.started` UUID 证明新原生会话；不用第二次普通 exec 冒充 native resume。另需恢复同一原会话时才用 `codex exec resume <exact UUID> --json <prompt>`。V6 不使用 `--ephemeral`，不使用 `--last`。避免继承主会话的 `TRELLIS_CONTEXT_ID`；先由新 Agent 实际检查其工具环境与 `get_context.py` 结果，再调用原 Bind。`.trellis/scripts/common/active_task.py:518` 优先读 TRELLIS_CONTEXT_ID，其后才从实际平台环境解析；源码第72行说明 Codex 实际变量为 CODEX_THREAD_ID。

新会话的原 owner 顺序为：`guru-bind-task-session:delivery_rebind_missing_session` → 明确 `guru-create-delivery:delivery_selection` → `get_context.py --mode continuation` → 原 affected owner。Bind public-input schema 的必要字段是 profile、mode、task_id、lifecycle_generation、continuation_id；新 Task binding 不自动带入 selected Delivery。`guru-bind-task-session/SKILL.md:24` 至第50行规定这一区分。缺少原 context key 时只能 explicit_task_mode，不能算新会话恢复已经通过。

### 原 Planning 链与实际调用

`.trellis/workflow.md:1003` 明确：Author task_scope_requirements → 原 Clarify scope acceptance → Creation → Author delivery_initial_review → candidate Architecture → Author delivery_solution_planning → Wording → final Architecture → Approval。Activation 是后续独立接受边界；I5 不能靠文件存在跳过任何 semantic owner。

`guru-author-task-plan/references/authoring.md:22` 定义 root PRD 唯一 writer；第60行起定义八个 Delivery profiles；第106行起要求 partial/staged 的剩余工作及整体 Completion；第139行承认 seed/PRD-only/design-only/partial/stale 为正常可收敛状态。对应实际 wrapper 为 installed `skills/packages/guru-author-task-plan/scripts/invoke.sh --root <target> --input <AI-authored input> --owner-result <AI-authored current result>`。AI 先调查、写正文、自检，再构造本轮 call-local result，宿主不能填它。

`guru-author-task-plan/runtime/invoke.py:26` 核对 Task 的实际 C4 binding/ledger/唯一 checkout；第90行起要求当前 Delivery phase=planning、当前 generation、当前 accepted_scope 与 selection。不能通过复制 task.json 或只补 DeliveryKey 绕过该事实关系。

Approval 的合法 writer 回程为 `revision_required` → Author delivery_approval_revision → 刷新受影响 gates → Approval delivery_revision_reentry。参见 `guru-approve-task-plan/SKILL.md` 的 Source design and Author revision boundary，以及 references/contract.md:231。Approval 只做语义审核，不直接写业务规划。

### 现有 eval 与 fixtures 的局限

`trellis/skills/guru-team/adapters/eval/owner_staging.py:69` 的 semantic_authoring 仅显式接受 standard_intake、guru-check-task 和 Architecture；第81行对其他 Skill 报 `semantic authoring fixture is not declared for this Skill`。现有 runner 不能直接成为 Author V1–V7 suite。post_owner 阶段消费已有 owner result，只能提供 transport/runtime evidence。

`adapters/eval/fixture_io.py:255` 的 stage_clean_installed_owner_repo 复制官方 scripts/workflow 后实际 apply preset，可参考完整安装方法；它不是公开 Task history import owner。`tests/test_delivery_family_integration.py:47` 起从 example 构造 projection 并对 schema，只证明 DTO 边，不证明真实写作和审核。

`runtime/eval_runner.py:288` 的 qualification production identity 固定 codex-cli 0.147.0；本机当前 0.162.1 不满足该专属入口。不要为 #154 改 qualification provider、固定模型或扩展其沙箱/攻击测试。

### 当前可用 CLI/Core 与 clean 安装方法

当前候选 source lock 为 `trellis/presets/guru-team/source/trellis-source.json`：CLI/Core `0.7.0-castbox.4`、Fork commit `7bcbeaad31380e7a29c97898cb947c6120a61775`。

本机确认存在匹配版本安装：

- CLI：`/private/tmp/guru-589-d7-paired-package/node_modules/@mindfoldhq/trellis/bin/trellis.js`。真实 `node <path> --version` 返回 `0.7.0-castbox.4`。
- Core：同一 node_modules 下 `@mindfoldhq/trellis-core/package.json`，声明 `0.7.0-castbox.4`。
- 可供既有 focused verifier 使用的 source root：`/private/tmp/guru575-fork-7bc-source`。其 `packages/cli/dist/.guru-source-commit` 真实内容为同一 `7bcbeaad…`。本研究未再次运行该 source 的完整 validate-source/CI gate，执行前仍需其原校验。

#599 旧代表安装仍存在：`/var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/guru-599-writing-kezezay1/project`，但实际 `.version` 和安装 lock 都是 `.3` / `c7bd746…`。不能直接当 #154 的完整匹配环境。旧日志在 `/private/tmp/guru599-behavior/`；只参考方法，不复用为本轮行为通过证据。

最小复用既有 clean/focused 入口如下；这是待主会话确认资源后执行的具体命令，本研究未执行：

```bash
TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#main \
TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 \
bash trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh \
  <主会话选定的全新空目录> \
  --fork-source /private/tmp/guru575-fork-7bc-source \
  --mode focused --platform codex
```

该命令必须从本 #154 source cwd 执行，指定显式目录以保留结果；默认临时目录会被 trap 删除。目标实际为 `<目录>/matrix/codex/project`，不是外层预留的 `<目录>/project`。`verify-throwaway-install.sh:127` 若省略 platform 会默认三平台，故明确 codex。`verify_trellis_compatibility_matrix.py:2460` 的 focused 是一次当前 source clean init 和同候选 update/reapply，不是完整 Release 矩阵。`_install_workflow:1554` 在未发布 workflow 上使用官方 native init 再应用本地 canonical 样本；这是原 local-sample 路径，不声称 exact remote candidate 已发布。其 init uses `init -y --codex --workflow native`。必须如实保留 unpublished/local-sample 边界；平台 projection check 不等于真实 Agent 已加载。

如果 focused source validator 不可用，匹配 installed pair 可真实运行 CLI init；但不能把绕开原 validator 的手工安装宣称既有 focused verifier 通过。由主会话决定是否使用原已支持的 local-sample/init+完整preset方法，不新造验证脚本。

### V5 最小合法方案与尚缺证明

当前真实归档 `.trellis/tasks/archive/2026-10/10-17-589-git-object-performance/task.json` 有八批 delivered，来自 PR593/594/595/596/597/598/604/606。该 archive 已有 Completion/Closure，正常 Reactivate 会增加 generation。`guru-maintain-legacy-task/references/contract.md:31` 明确 normally finished current archive 不能走 archive_resume，而归原 Reactivate。不能把归档目录复制到 active 后宣称原 lifecycle 已恢复。

本研究只读 GitHub contents 核实真实历史 commit `c422692bca2d385a264da4db0030612b1b306fe1`：原 active Task schema2/gen0、没有 Completion；D1 `3f225649-2810-435d-baf4-4d2e36c287e5` 已 delivered，D2 `ec0712d3-2dcc-49f7-b557-262022bfcf3d` 为 reviewing。只读 live PR593/594 确认均 MERGED，D1 head=`924f293821e1e3031b7efdbfc3b0868ef9d02011`、merge=`faef781870c69e3657fcbafeb1ce24d0474e6969`，D2 head=`c422692…`、merge=`5baff654d2c7ac7a069cea181852d4831c2e65bd`。

可选最小方案是原样使用该实际 Git snapshot 作为明确历史数据集，在同一个隔离仓库建立本地 caller-owned checkout，运行原 C4 binding/Ensure/Bind/Selection，再让当前阶段原 reviewer 判断真实规划差额，通过其合法 rework 返回同一 D2 Author。新模板、所有正文与 owner result 都须当前 Agent 实际读取/生成；历史结果只当历史事实。`guru-establish-task-branch-binding/SKILL.md:19` 支持当前 active Task 的 missing binding 恢复；`runtime/task_lifecycle/checkout_acquisition.py:126` 支持 adopt_invocation_checkout。它们不是一般 history import API。

这里尚有两个实际 provider 门槛，不能预写成功：一是 clean 环境装载该真实历史 checkout 后，C4/current resolver 与安装维护是否正常接受；二是 D2 reviewing 的原 reviewer 是否有真实问题和完整前置，可合法回 planning。不能直接对 reviewing D2 调 Author。`delivery_operations.py:252` 要求 rework 来自当前 semantic owner；`guru-review-task-delivery/SKILL.md:18` 还要求当前完整 Branch Review，不允许拿历史 reviewing 状态代替 fresh upstream output。

若上述门槛不能在既有入口满足，则 V5 保留精确 provider gap。另一正常方案是全新 partial D1 经原 PR Delivery owners 真实交付后创建 D2，但那会新增 GitHub push/PR/merge 边界，不能由 I5 本地验证自动授权。Guru workflow `.trellis/workflow.md:715` 只声明 pull_request；`guru-create-delivery/runtime/invoke.py:58` 检查声明，不能换成上游 schema 支持但 Guru 未声明的 local_commit。

### 资源副作用最小集合

建议一个 Codex clean installed 仓库，共用 source/preset与可调查的小型工程 fixture；原 owner 创建独立场景确实需要的最少 Task/Delivery，避免为每个 V 新建仓库；至少两个真实 native sessions 完成 V6；Architecture 使用原合同所要求的独立 generic Agent。主会话保存实际平台日志 locator，唯一 Test 保存最小 evidence 引用。无须新 Issue、push、PR、merge、公共 API、公共 DTO、额外 harness 或完整 Release 矩阵。V5 历史 checkout 若需额外 branch/目录/本地 refs，应先纳入主会话的精确资源边界，不执行清理或修改原 #589 状态。

新 Task 的资源还必须满足 `guru-create-task/SKILL.md:29`–43：不能 adopt primary checkout，即使 primary 已在非base branch；必须使用干净、注册的 linked non-base checkout，或由原 owner provision_linked_worktree。因此一个 clean primary repo 之外，至少需要原 owner 创建的 linked worktree/branch。既有 Task 的 C4恢复可以使用 primary，不得把这个例外套用于新建 Task。

### V2 真实简略来源补充核实

本轮只查一个已知历史候选 `castbox/guru-trellis#56`。live body 是分支类型自动判断及一个类型表，确属相对简略工程来源；live state 为 CLOSED、updatedAt=`2026-07-09T17:16:50Z`。它不能作为无需 mutation 的 V2 正常 Intake Direct Source。`guru-clarify-requirements/references/contract.md:201`–207 明确 `reopen_closed_issue` 需要实际 GitHub reopen mutation，且 closed Issue 不能返回 clear；`create_followup_draft` 只保留它为related/reference。`guru-create-task/SKILL.md:19`–26 只消费 ready 的 existing_issue 或 standalone_request，并保持真实 source.kind 与 accepted scope。不能通过 reference_only 偷渡 closed Issue 到 clear，也不能用 no_issue fixture 同时冒充 V2 与 V3。

这不是新 requirement 或 finding。#56 不满足无需 mutation 的来源条件；不新建或重开 Issue，也不宽搜其他历史。Task整体scope由其真正来源和原Clarify决定，切片的缩小仅由原Delivery Creation/Policy负责；不能为测试只选Issue部分正文却声称全部承接。

### 后续只读核实：真实 OPEN #331 可作 V2 候选

本轮根据主会话给出的唯一新线索，live 读取 `castbox/guru-trellis#331`。state=`OPEN`，updatedAt=`2026-09-02T03:38:52Z`，title 为“对文档SSOT的结构做出针对Agent友好的结构性调整，从 SDD 转型为 KDD”。正文说明 RDT 检索/修订与编号维护痛点、两层 Architecture Baseline 的检索和增补能力、Guru 接管两套 SSOT 生命周期，以及向 KDD 转变的目标；Obsidian 是参考建议。没有完整场景、可观察验收、实际执行机制和迁移安排。

该输入符合 V2 的“真实但不充分的工程 Issue”类型，不是空 Issue，也不与 V3 的 no_issue 混用。它的业务范围较复杂，适合检查调查和设计深度；若还要检查简单工程裁剪，可由 V3 承担。原 owners 必须保留上述全部明确目标和两层基线约束；不能把它缩成一个模板字段调整后声称承接完整 #331，也不能把 Obsidian 建议升级为强制工具选择。没有完整来源实现设计不表示没有规范约束，design 必须区分这两者。

实际可执行顺序是：原 Discovery 调查当前 RDT/Architecture 与历史实现差额 → 原 Clarify 处理真实未决范围 → source.kind=issue、repo_ref=castbox/guru-trellis、number=331 的原 Intake/Task Creation → Author whole Task PRD → 实际切片与 Planning。OPEN 只解决 closed-source 限制，不等于 ready 或必然还有可独立交付差额。真实用户选择未回答时，不编造答案。当前未运行这些 owners，因此仍是候选方法，不是 V2 通过。

### 后续只读核实：#589 没有找到更早 D2 planning 公共 Git 快照

通过 GitHub commits API 读取 main 可达的真实 active `task.json` 历史，返回11个内容变更提交；另查 D2 `prd.md` 路径历史，其首次加入为 `c422692bca2d385a264da4db0030612b1b306fe1`。这些查询未创建本地 refs/目录或修改 Git。结果如下：

| 原始提交 | Task 状态事实 | 可否直接续写 D2 |
| --- | --- | --- |
| `924f293821e1e3031b7efdbfc3b0868ef9d02011`，PR593 head | gen0、无Completion；只有D1，phase=reviewing。 | 无D2。 |
| `faef781870c69e3657fcbafeb1ce24d0474e6969`，PR593真实merge | gen0、无Completion；仍只有D1，phase=reviewing。 | 无D2。 |
| `c422692bca2d385a264da4db0030612b1b306fe1`，PR594 head及D2首次提交 | gen0、无Completion；D1 delivered，D2 reviewing。 | D2不是planning。 |
| `5baff654d2c7ac7a069cea181852d4831c2e65bd`，PR594真实merge | gen0、无Completion；D1 delivered，D2 reviewing。 | D2不是planning。 |

此结论范围是已核对的公共 main 可达文件历史及以上确切提交，不声称本机所有旧 reflog 或不可达对象均不存在。当前没有可给出的“D1 delivered + D2 planning + 未Completion”真实已提交快照。原 C4 可以恢复已有 active schema2 Task 的 branch/ownership；`branch_resolution.py:146` 从真实 branch HEAD 的 Task artifact 核对 TaskId/generation/active 状态，第230行起核对唯一registered checkout及归属。因此原样历史 snapshot 在明确隔离数据集内可以成为待验证的已有Task候选；C4不提供stage重置、history import或新Authority，也不允许宿主改 phase。工具更新只能由原 `guru-upgrade-tools` 完整匹配维护，保留Task/planning/session/control，并单列 local_candidate 边界。

### 更小路径核实：PR593 已合并但原快照缺 Publication

主会话提出：从真实 PR593 merge snapshot 开始，原 Merge `delivery_merged_recovery` 读取 live MERGED 事实补 D1 delivered，再由原 Creation 真正创建后续切片。这条路径不需要新远程 merge，但当前确切输入在原前置处阻塞。

对 `faef781…` 的原样 Task JSON 本轮实际读取结果：D1 `publication_result=null`、`delivery_result=null`、`full_review=null`、`readiness=null`；planning/check 有历史结果，candidate.head_ref=`3676b9ee65834ef3720f2ff5cc0d8330afcea6ed`。这些是历史提交本身，不是 live PR状态。

Merge `references/contract.md:5`–15 明确要求实际现存公共 Publication；`runtime/manual_recovery.py:24`–40 精确查 selected Task 所有Delivery的public Publication，缺少时返回 `manual_merge_missing_publication`；第178行先执行这项检查，再读远程 terminal facts。真实 PR593 的 MERGED/head/merge 两parent只能验证已有关系，不能创建该关系。public input schema `public-delivery-merged-recovery-input-1.0.schema.json` 只有profile、mode、task_ref、DeliveryKey、repo_ref、pr_number，没有Publication导入字段。

Publish `references/contract.md:39`–57 的正常恢复以原 private transaction reference 为键；fresh publication 需要实际 readiness_result_id。旧 Git snapshot 两者均未提供，也不能由live PR重新构造门禁或原事务。原 Merge history query2 明确只读取/验证已有事实，不导入。不能从后续 Task JSON 复制 Publication 到较早 snapshot，也不能把它包装为新的 schema/API 输入。

这里的精确 provider gap 是：“缺少已存在 public Publication 或其原生产者恢复事务，无法从PR593的已提交快照合法补 Delivery fact”。C4/Bind不能补这一事实；source #589 当前 CLOSED 并不是该 Merge profile 的直接检查条件，Merge源码没有要求reopen source。Creation也不主动重开Issue；但初始Intake仍遵守Closed不能clear的合同，不得因此将#589重新当新任务来源。当前研究不构造任何新的历史scope权威。

因此该历史恢复方案没有可确认的更小 V5 资源路径。若未来提供真实未改写的 public Publication 原始数据集或原事务locator，可沿原 owners再次判断；否则保留该历史方案的 provider gap。此缺口不要求新增import API/harness，也不升级为新finding。新的真实 scratch PR 路径另见下节，不依赖导入历史。

### 最新方案：scratch base 上真实 partial D1 → 同 Task D2 Planning

合同层面可用原正常路径，不需要新增公共 provider。隔离验证仓库的 origin 保持 `castbox/guru-trellis`，唯一发布目标为 `codex/154-validation-base`；fixture Task 的真实 source 为 `{kind:no_issue}`。#154 是这次验证的用途，不成为 fixture Task 的伪造 Direct Source。该路径必须真实经过原 Planning、实现、Check、Commit、独立 Branch Review、Delivery Review、Publish、Merge、Completion 和下一 Creation；宿主只提供请求与仓库事实，不写最终规划或Gate结果。

#### 最小资源和 base 前置

1. 使用父会话正在恢复的同一 clean root。官方 init 应采用匹配 CLI 的 `native-delivery-v1`，以便 public Task schema2/API1.0 可用。既有 focused helper 以 legacy native 引发的 schema1/bootstrap失败保留为首次失败事实；它不是本轮需要修的生产 verifier。本研究不改 helper，也不把新的实际正常安装当旧focused已通过。
2. 在该root形成一个实际干净初始commit，保留完整匹配工具和真实fixture输入。主会话将该隔离仓库的 primary checkout 绑定为 scratch base，并使远程 `refs/heads/codex/154-validation-base` 与它实际相同。所有 GitHub 操作显式repo/branch，不推main。实际写入和命令由执行owner选择；此处不预写commit/HEAD。
3. `guru-sync-base` 的 invocation public_input 指定 `mode=workflow`、`route=repo_change`、`repo_root=<clean root>`、`base_branch=codex/154-validation-base`。实际 public wrapper 为 installed `guru-sync-base/scripts/invoke.sh --invocation -`。`runtime/invoke.py:24` 将明确base传给内部执行器；`references/contract.md:27`–50 要求该branch有唯一干净registered checkout。必须实际满足local base、remote-tracking与authority HEAD相同；不要让默认候选main取代scratch。
4. 新fixture Task另由原Creation owner provision一个linked non-base、non-delivery worktree/branch。建议角色路径是 `<clean root>` 保留scratch authority、`<同一验证临时根>/task-v5` 作为linked Task checkout，head branch可由执行owner选 `codex/154-validation-v5`。这些是建议的资源角色，不是已创建事实。最小为一个repo common-dir、两个checkouts、两个local branch和后续同名remote refs，无需第二个clean安装或GitHub Issue。

#### Fixture 请求与真实 source

可以给原Agent一个清晰的no_issue工程请求：在验证fixture中实现一个本地CLI；D1实现 `hello NAME` 并提供准确输出/退出码；D2实现独立的 `goodbye NAME`，保留D1接口。原Agent应调查已有fixture文件，自行细化可观察行为、参数和设计，并说明工程裁剪。两个能力只是去敏行为验证输入，不写进#154生产实现。也可使用父会话已有更合适的双能力fixture，避免重复搭建。

整体Task PRD必须从开始就保留两个能力；D1的partial Policy说明独立交付目标、D2剩余责任和整体Completion条件。不要让Task先只接受D1，再临时增加D2来制造“原剩余责任”。D1交付后D2实际Planning读取D1真实结果、当前代码、整体PRD与原必要引用。原Writer决定实现细节，宿主不预写最终四正文。

原 Intake 应保留 `standalone_request`；`guru-create-task/SKILL.md:19`–26、`examples/public-create-input.json`、`runtime/task_lifecycle/source.py:34` 支持 `reviewed_source={kind:no_issue}`。Create input 的关键绑定如下，具体scope identity/HEAD/事务值由原owners产生：

```json
{
  "source_profile": "standalone_request",
  "reviewed_source": {"kind": "no_issue"},
  "delivery_target": {
    "repo_ref": "castbox/guru-trellis",
    "branch_ref": "codex/154-validation-base"
  },
  "selected_base_ref": "codex/154-validation-base"
}
```

这只是 `creation` 中字段的说明，不是可直接伪填执行的完整input。`prepare_creation_inputs`（composition.py:196）要求actual local selected-base HEAD等于reviewed_base_head、acquisition.decision_head相同、同一common-dir、generation0、Task artifact此前absent。Task head branch不能等于selected base或delivery target；新Task不能adopt primary。`guru-create-task/runtime/invoke.py:83` 将selected_base写成官方Task `base_branch`，不在task.json新增delivery_target。TaskRef使用执行当日Asia/Shanghai日期。

#### 基础 Docs / Architecture 不能省略

匹配安装本身不证明新fixture有可用项目authority。原 Planning Architecture/Approval仍需适用的Baseline、constitution和change-contract。若这些在clean fixture中缺失，沿 `guru-bootstrap-repository-ssot:new_repository`，实际调用上游spec-bootstrap、原RDT `bootstrap_foundation` 和原Architecture `bootstrap_foundation`，由实际Agent写最小且真实的authority并完成cross-SSOT判断。该owner的SKILL:21–43定义此顺序；不得由宿主制造baseline_current或no-impact pass。

最省重复的安排是在冻结scratch初始base之前由原owners完成这套fixture基础authority，再commit/push scratch seed并Sync；若Planning首先发现缺失，则沿其原bootstrap回程完成，更新的真实diff纳入本批。每批仍由Architecture判断是否有实际差额；真实no_architecture_impact结果可避免无必要contribution/ADR，不能预选该结论。未发生产品变更时不凭模板创建额外ledger。

#### 实际 native Agent 的顺序

1. **Intake与Task创建。** 新native Agent在实际installed目标完整读clear-writing/AGENTS、当前workflow，再沿selector的standard route、明确scratch Sync、Discovery、Clarify、Wording、Change Request Review到 `guru-create-task`。只使用真实producer outputs。切到返回的linked checkout，核对C4/C5/Ensure与本会话binding。缺失的source_selection回原Clarify，不能从PRD补造。
2. **整体scope与D1 Planning。** 唯一Author task_scope_requirements写完整两个能力的root PRD；原Clarify task_scope_requirements_acceptance实际accept_scope。原Creation创建 `pull_request` D1并选择它。D1 scope_ref的authority等于实际整体accepted_scope，anchors只承接本批能力；UUID由原Creation分配。
3. **D1真实写作/审核。** Author delivery_initial_review实际读Task/Delivery模板并写本批需求 → 原candidate Architecture → Author delivery_solution_planning写design/implement/官方context → 原Wording → final_plan Architecture → Approval → 原Activation。implement唯一Policy为partial，并保留D2。实际适用Docs差额走原RDT/Architecture owners；当前语义结果由本轮Agent生成。
4. **D1实现与完整质量链。** 实现仅本批能力并运行真实定向验证；原phase2 Architecture与 `guru-check-task` 完整Check，必要Docs reconciliation/promotion须在final Check前完成。原TaskCommit精确提交候选；独立fresh generic reviewer先按Architecture read order评committed candidate，再做完整Branch Review。不要把fixture简单等同于免除这些owner，也不为它运行#154整仓Release矩阵。
5. **D1真实发布。** 原publication Architecture → Delivery Review，确认独立D1范围、partial剩余责任、真实验证和中文PR payload。no_issue PR不含Issue引用或closing keyword。原Publish实际push head、创建Draft PR、converge metadata/Ready，再投影真实Publication；base必须是scratch。
6. **D1真实Merge。** 原Merge使用实际ready_for_merge handoff及独立本轮语义review，执行其expected-head `--merge --match-head-commit`，实际两parent merge与五个schema2 trailers必须相符。Merge原owner通过公共 `record_delivery` 写真实fact并release D1 selection。宿主不手写delivered、Publication或PR号。
7. **整体Completion给出下一批。** 实际acceptance_finish Architecture → 原 `guru-review-task-completion:delivery_completion`。它读整体两个能力、D1事实和未交付D2；只有它实际判断 `additional_delivery_required`，workflow `task-delivery-planning-router`（workflow.md:528）才将实际TaskKey seed交原Creation。普通remaining_work另有consumer，不把它改标additional_delivery_required。
8. **D2真实Creation与Planning。** Creation读取剩余scope和历史D1，分配新UUID/新的planning_root，仍同TaskId/gen0/原accepted_scope。原Author delivery_initial_review → candidate Architecture → solution → Wording → final Architecture → Approval，实际生成D2三正文并读D1结果/代码/必要引用。此处即可审查V5所需的两批正文、起点差额、剩余责任和Completion关系；不必为#154的V5证明额外完成D2第二次PR。

只要同Task head branch保持D1 head的后继，D2可在原Task linked checkout/branch继续，通常无须新worktree/rebind。原 `DeliveryProjection.content_base`（adapter.py:254–286）优先同Delivery既有candidate，否则取同generation中祖先关系成立的唯一最大已delivered head；因此D2内容base通常取D1实际reviewed_head，不能再次采用root scratch起点重复D1。scratch PR目标的merge commit和内容base是不同事实，不混为一个B。

#### 非默认base、无Issue和收尾边界

Publish `runtime/owner.py:169`、347从Task读base_branch，PR create（491）显式 `--base` 该值。Merge `runtime/owner.py:209`只要求非空base，随后核对实际PR/base与Publication，并读该base的远端ref；没有要求default branch或main。Review `runtime/common.py:340`按source.kind=issue才要求Refs；对应references/contract.md明确no external Issue不生成Issue reference。所有PR禁用closing关键词，中文正文如实标明这是#154独立scratch行为验证，不宣称生产交付或软件发布。

D1后停在D2 Planning时，fixture Task仍active，不能声称whole Task completed/archived，也没有正常Cleanup seal。原Cleanup SKILL:67–70明确current binding会阻止删除。若最终要移除全部resources，由父会话选择真实剩余责任处置：继续完成必要fixture交付/Finish，或通过原Clarify/当前stage withdrawal处理测试目标结束，再由相应owner正常收尾；如果选择外部手工保全/销毁，则如实记为manual disposition，不能伪造完成或绕过绑定。此条只说明原合同，不扩大V5验收为强制第二次PR或Release矩阵。

本节是只读合同可行性结论。scratch refs、初始commit、linked checkout、Task/Delivery、PR和merge均未在本研究创建。实际平台若在原前置处遇到问题，应保留精确typed gap并由原owner处理，不补宿主fact或另造provider。

### Related specs and references

已读取本 Task D1 prd/design/implement、当前 AGENTS、完整 clear-technical-writing、trellis-before-dev、workflow/guides indexes、semantic-retrieval、相关 quality/skill I/O/subtraction/ownership合同，以及上述原 owners 与实际 runtime。官方 Trellis custom workflow/marketplace URL 为 AGENTS 指定参考；本研究不修改扩展，也未重新在线核对官网，因此不提供新的官方兼容性结论。CLI flags/version 为本轮 live help/version；GitHub historical contents 与 PR 状态为本轮只读查询。

## Caveats / Not Found

本研究没有执行 Agent 写作、clean install、Task/branch/repo/session creation/binding、Git/GitHub mutation，也没有修改实现、测试、门禁或公共事实。唯一写入是本研究文件。V1–V7 当前都不能据此计通过。现有 eval 明确缺 Author semantic-authoring provider，直接 native CLI 是可用平台候选；V5 的历史接续及 V7 的原 reviewer 前置仍须实际执行证明。不得把这些执行缺口转为新 scope、finding severity 或新 public harness。

### 最新V2选择：经原CreateIssue链创建真实简略fixture Issue

#331 的 native 场景已遇到下述 Wording 分类边界。V2合同要求真实简略Issue，不要求事先存在；因此另一条保持现有#154机制的路径是由原CreateIssue链创建一个真实、简略、仅描述隔离fixture期望行为的Issue，随后以其live identity执行V2。输入不是最终PRD/design，不携带预填pass；fixture的范围、预期行为与未决事实由原Agent调查和澄清。

原入口顺序必须完整：proposed_draft的原Sync/Discovery/Clarify/Wording/Change Request Review → 实际ready且target.kind=proposed_draft → `guru-create-issue:issue_creation` → 实际created(repo/number/url) → 明确scratch Sync及fresh Intake → live existing_issue ready → Task Creation/Author。不能 `gh issue create` 直接替代原owner，不能created后直入Task，也不能把新Issue作为#154的替代Direct Source。依据为 `guru-create-issue/SKILL.md:26`–32、39–78，及其 `schemas/public-input.schema.json`。

CreateIssue的public input仍使用现有profile/action、实际reviewed_target、实际reviewed_label_identity_sha256、draft与reviewed_at；当前draft.duplicate_disposition必须是create_new。所有identity/time由本轮实际review产生，不能从示例复制。创建后采用返回的真实OPEN Issue；新V2与V3 no_issue继续分别报告。

这个替代路径可以避免为本轮V2修改#331或Wording协议，不是修复#331 advisory分类。#331的原试验保留为未通过的场景provider边界；新V2不能被表述为已经证明#331或所有advisory表述可通过。R4/V4对来源角色的真实验证责任仍在，不因换V2输入而消失。此处不新增severity、实现或测试任务。

### #331 advisory候选：当前owner支持范围

只读证据：Wording `references/contract.md:59`–71要求change_request固定包含完整title/body；第142–165行九分类没有一般advisory_non_contract。quoted_source_non_contract只适用于已经明确标记的外部引文，historical_record_non_contract只适用于非规范历史事实；deterministic_option是封闭产品选择，deterministic_reference针对明确可核对引用，均不能凭理由文本改义为任意建议。

`runtime/record.py:22`–27要求每个当前hit恰好一个分类，未分类或contract_violation不能pass；`schemas/contract-wording-review.schema.json:546`的enum同样只有这九类。#331 live body的“可以参考obsidian等业界著名的知识库……”是来源作者的方案探索建议，单因Clarify的source_selection.authority_kind=advisory，不会从扫描范围排除该句。source_kind=issue的当前read/check仍绑定真实正文与updated_at。

在保持#331 live正文不变的条件下，本次没有找到能诚实承接这类一般建议的现有非阻塞分类。将该句直接归quoted_source_non_contract、historical、closed option、literal等会改变这些分类含义。按子段重新生成draft或只扫描规范部分会改变来源身份/固定scope，不是合法解法。必要的等义语言修订属于原Wording能力，但对live Issue必须真实修改、重读和rescan，不能只在内存改scope后声明原Issue通过；当前选择不采用该live修改路径。

这份记录只保留候选事实，不定severity：candidate_ref=`wording-live-advisory-classification-gap`；observed_behavior=合法advisory正文的控制词命中没有适用非阻塞分类；locators=上述contract/schema/recorder及真实#331；minimal_reproduction_hint=原change_request扫描完整#331，保留原advisory角色后逐hit尝试当前九分类，不改live正文或owner语义。

### 若未来确需同scope机制返工：原入口与限制

当前优先换用真实简略fixture Issue，因此无需因这一个V2输入立即修改#154规划或runtime。若后续证明Task自身必须修改Wording机制，原Implementation owner先按workflow.md:1170的implementation_discovery资格链审当前候选，再决定原范围内机制修订；不默认变成scope变化，也不由研究Agent分类或定级。

从implementing存在的确定性公共回程是 `.trellis/scripts/delivery.py rework --task <actual task_ref> --input <complete operation JSON>`。原 `guru-phase2-implementation-coordinator` 必须先真实判断回程，operation携带：api_version=1.0、operation=rework、同一DeliveryKey、owner_role=implementation、owner_id为当前workflow声明的implementation owner、expected_phase=implementing、target_role=planning、真实reason AuthorityRef，以及affected_results=[planning,check,full_review,readiness]。同scope机制返工不传新scope_ref，不执行accept_scope，不改TaskId/generation/DeliveryKey或历史PR事实。`.trellis/scripts/common/delivery_operations.py:252`–272检查current semantic owner、回程方向并清理受影响gate；`runtime/delivery_projection/gates.py:24`是同一公共operation薄projection。此CLI不支持把 `--input -` 当stdin，其input接受内联JSON或UTF-8文件（delivery.py:52）。

公共rework只改变阶段，不能制造Author的上游producer结果。Author delivery_approval_revision的语义前置是实际Approval revision_actions；不能因schema能接数组便由宿主冒充Approval。若采用直接implementation rework，仍须回原规划审核producer获得合法当前revision出口，再进入对应Author profile；没有实际producer证据时停在其原回程，不发明新handoff。

另一个合同完整的既有路径是实际候选进入Check：原implementation公开begin_check绑定当前真实candidate；原 `guru-check-task` 完整语义round若确实选择planning_stale/reapprove_plan，则其 `runtime/delivery.py:87`–92实际按check owner rework到planning并清理四gate，workflow.md:521的原router以实际current actions进入Author delivery_approval_revision。该Check入口要求实际Planning acceptance、当前candidate/C4/适用gate等，不能只为改phase而填Check结果；其schema仍要求真实proposal_refs，不能虚构scope_decision以填满字段。若这些前置尚未满足，不能把此路径当作已经可立即执行的捷径。

Author机制/设计改动需要返回requirements_ready→candidate Architecture→solution→Wording→final Architecture→Approval→Activation；只刷新实际受影响依赖。整体需求和#154 accepted_scope仍相同时，不默认先重写root PRD或重做Clarify scope publication。真正改变已接受义务时才进入原scope owner。

### 若新增advisory分类：实际I/O与兼容迁移边界

先区分owner-private证据和public Skill输出。Wording `interface.json:493`将contract-wording-review.schema注册为 `stdout_only_owner_private` 的gate_evidence；`runtime/invoke.py:18`–48最终public出口仅投影现有route/identity/change_refs等。分类数组和classification_version不进入public typed DTO。public pass的source_selection.authority_kind早已允许advisory（public-pass-output-2.0.schema.json），缺口是独立的lexical classification。因此不能未经盘点就断言“加一分类必然新增public DTO字段”。

新增分类仍会实质改变当前分类协议、private result schema/record/check语义及安装投影，超出本批原来纯Markdown机制假设。旧checker遇到新enum值会拒绝，新producer/旧consumer不能只靠相同文件路径混用。若未来选择实现，须由原Author明确合同变化、classification_version/相关schema是否新版本、受影响producer/checker/invoke/Interface private artifact引用、示例、文档及全部安装投影。保持既有九类语义，不把v1名称静默改成一般建议分类。

只有实际public input/output/consumer不兼容时，才按AGENTS 3.5与skill-package-contract.md:329–343走独立public I/O迁移、新schema/id或明确迁移合同，并保持legacy validation资产、明确新current选择及cross-version失败/重入原producer。若最终仅owner-private短生命周期证据扩展，不能为形式完整新增public DTO、dual reader、历史artifact导入或长期兼容adapter。当前stdout-only证据可以失效后由原owner当前全文rescan/review/record/check重做，不需要虚构持久化迁移账本。任何长期兼容仍适用subtraction-first的真实consumer/退出条件要求。

本节没有提出具体新enum字面值，没有修改public/private schema、runtime、测试、Issue或Task状态。优先的真实新V2 Issue方案保持上述迁移问题为未采用的候选边界。
