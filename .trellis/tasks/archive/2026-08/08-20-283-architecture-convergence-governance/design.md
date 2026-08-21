# #283 技术设计

## 1. Authority 模型

### 1.1 三层边界

1. `authority_kind=horizontal_baseline` 的独立横向基线拥有跨项目设计宪法正文与解释。
2. 项目 `docs/architecture/` 拥有该项目的 Architecture Baseline，并声明适用设计宪法的 locator/version/content identity、适用范围和最小原则投影；若设计宪法由项目基线自己拥有，其 locator 仍必须唯一。
3. `guru-maintain-architecture-baseline` 只读取 live authority、完成语义判断、投影最小结果并路由 contribution/review/promotion；不复制原则正文，也不成为第二 authority。

最小原则 projection 使用稳定 identity 与短名称：

| Identity | Short name |
| --- | --- |
| `mature-practice-applicability` | 成熟实践与适用性 |
| `concept-semantic-completeness` | 概念与语义完整性 |
| `cohesion-change-isolation` | 职责内聚与变化隔离 |
| `minimum-necessary-complexity` | 最小必要复杂度 |
| `debt-one-way-convergence` | 技术债务单向收敛 |

这些 identity 只用于引用与上下文注入；具体解释必须回到 authority locator。Task 只记录命中的冲突/权衡/例外，不为未命中原则填空。

## 2. Architecture Baseline 生命周期闭环

### 2.0 双维约束与交叉点

Guru Team 方法论维度拥有 mandatory invocation、stage order、semantic owner、freshness、fail-closed/re-entry 与 typed consumers；业务 repository 项目语义维度拥有 Architecture Baseline、Architecture change-contract authority、required concern set、字段适用性和项目检查入口。二者不互相复制正文，只在 task-local Architecture change contract 相交。缺少 Guru public identity 或项目 authority identity 的架构相关 task 均不能继续。

### 2.1 正常数据流

```text
current Architecture Baseline + design constitution
  -> Planning impact/change path
  -> implementation discovery re-entry when scope/risk evolves
  -> Phase 2 project checks + before/after satisfaction review
  -> task-isolated contribution + ADR only when decisions evolve
  -> committed full-diff Branch Review
  -> reviewed promotion updates shared current authority
  -> next task reads the promoted version/content identity
```

Architecture Baseline 是该数据流唯一的项目架构 SSOT。Guru Team 不在 task artifact、workflow 或公共 Skill 中建立平行架构正文；它只负责让每个阶段读取 current authority、形成最小判断结果并把需要长期保留的架构变化送回 promotion。

### 2.2 ADR 与 contribution 边界

- 新增或改变 architecture decision、设计宪法权衡/例外、GAP 生命周期、domain/integration owner、single-writer 或 compatibility exit condition 时，task contribution 必须携带对应 ADR candidate 与证据。
- 完全遵循现有 decision 且不改变上述状态的 task 只记录 current 满足性结果，不创建 ADR。
- Phase 2 首次判断 candidate 满足性；Branch Review 独立验证 committed diff 与 ADR/contribution 一致性；二者都不能直接激活 shared authority。
- `promotion` 是把 reviewed contribution/ADR 回补 current baseline、ADR history、GAP/owner 状态并生成下一 current identity 的唯一入口。

### 2.3 自我迭代不变量

每次 task 结束后，shared current 要么保持同一 identity，要么由 reviewed promotion 形成一个后继 identity。后继 identity 必须能追溯被消费的前序 baseline、reviewed task/contribution、ADR/decision/GAP 变化和项目检查 evidence，并成为下一 task Planning 的 current 输入。任何 task-local 结果、当前错误实现或未 review 草稿都不能反向改写该链。

## 3. Architecture package 2.0

### 3.1 Stable identity

保持 `guru-maintain-architecture-baseline`、`bootstrap_foundation`、`task_impact_sync`、`promotion`、`repair` 和现有七个 exit 不变。Interface 仍遵守当前 Skill Interface 1.4 容器合同，但 current public profile 明确选择 Architecture schema 2.0。

### 3.2 Public entry

2.0 input 是 caller route DTO，caller 不得预选 semantic result。公共字段只包含：

- `schema_version=2.0`、profile、source exit、mode、continuation；
- repository/task locator 与 stage intent；
- profile 所需的 current baseline 或 contribution identity/freshness；
- `task_impact_sync` 的 stage 为 `planning|implementation_discovery|phase2|branch_review|publication|acceptance_finish`。

Architecture owner 从 live baseline、task、diff、contribution 与项目检查结果重建语义。caller 不提交 pass/finding/route、原则评分、授权、完整扫描或 owner-private digest。

### 3.3 Task-local Architecture change contract

仅当 `impact_kind=architecture_impact` 时建立 current task-local Architecture change contract 和 task-owned contribution。合同同时绑定 Guru public contract 与项目 Architecture Baseline/change-contract identity，并包含：

- requirement/behavior authority、baseline locator/version/status 与设计宪法 authority/version-or-content identity；
- 一个互斥 change path；
- domain/integration/decision/GAP refs 与项目 required concern set；
- current/target owner，single-writer 与 compatibility exit condition；
- allowed/forbidden parallel scope；
- planned closed/retained/new deviation refs 与 legacy deletion conditions；
- applicable principle refs，以及 conflict/tradeoff/exception reason/evidence refs；
- overview/detailed design responsibilities；
- before plan、after candidate、required project architecture check refs、test/runtime/external evidence；
- contribution、必要 ADR、review、promotion 和 expected current baseline identity。

适用项目字段 missing/empty/stale、无法证明 `not_applicable`，或与 requirement/design/code/diff/evidence 不一致时返回 `contract_incomplete|architecture_conflict|sync_required`。`impact_kind=no_architecture_impact` 仍由 Architecture owner 生成，只携带 task、baseline、stage identity 与可审核理由，不创建 contribution，不要求 principle rows、GAP、owner 或检查结果。

### 3.4 Project architecture check protocol

项目 Baseline 声明检查 descriptor，项目命令产生闭合 result：

```text
check identity/version + applicable scope + rule/decision/GAP refs
  -> before/after counts or state + pass/fail/unverified
  -> evidence locator + unavailable reason + freshness identity
```

Guru runtime 只验证 descriptor/result shape、命令 identity、locator 与 freshness，不能根据数量自动判断架构充分性。Architecture semantic owner 结合设计宪法、decision、GAP 和 task scope 判断适用性与 route。`unverified` 对 mandatory applicable check fail closed；不适用检查不制造失败。

### 3.5 Typed outputs

- `baseline_current`：仅投影 consumer 必需的 task/stage、current baseline、设计宪法 identity，以及 `no_architecture_impact` 或 reviewed contribution locator/identity。
- `sync_required`：投影 stale authority 或 reviewed contribution 的最小 identity、sync kind 和 freshness，回到 `promotion|repair` authoring。
- `baseline_incomplete`：投影缺失 authority refs 到 Bootstrap/repair。
- `architecture_conflict`：投影当前 task、冲突 refs 和 planning route；不复制原则正文。
- `contract_incomplete`：投影缺失 contract/decision/constitution refs 和 planning/repair route。
- `fitness_regression`：投影 current task、regression refs 和 implementation/check route。
- `blocked`：只保留稳定 reason/remediation。

每个 output 使用独立闭合 schema 和唯一 consumer；完整语义结果、检查明细、review narrative 与 Git facts留在 owner-private gate 或 live authority。

## 4. 单向收敛算法与语义门禁

Planning 记录 before plan；Phase 2 对 worktree 完整候选首次计算 after；Branch Review 在 committed full diff 上独立重算并复核 Phase 2 evidence。语义比较必须完整覆盖以下七项：

- 新增违规数必须为零；已有违规的 scope/risk 不得扩大；
- closed GAP 不得重现；retained/new GAP 必须满足 owner/reason/dependency/closure condition；
- owner 切换符合计划且任何过渡期只有一个写入 owner；
- compatibility layer 有可验证退出条件；
- 设计宪法冲突/权衡/例外有 live authority 支持。

新增或恶化返回 `fitness_regression`。缺 decision/constitution/check contract 返回 `contract_incomplete`。方案或实现与 current principle/decision 冲突返回 `architecture_conflict`。baseline/constitution/contribution identity stale 返回 `sync_required`。

## 5. Workflow stage 集成

```text
Planning
  -> Architecture task_impact_sync(planning)
  -> guru-approve-task-plan consumes current impact

Implementation discovery expansion
  -> task_impact_sync(implementation_discovery)
  -> current resumes / conflict or incomplete returns planning

Phase 2
  -> project checks + convergence comparison
  -> guru-check-task consumes current or fitness route

Task commit
  -> task_impact_sync(branch_review) over complete committed diff
  -> independent guru-review-branch recomputes satisfaction

Publication
  -> current/no-impact or reviewed contribution only

Acceptance/Finish
  -> current no-change proof, or reviewed contribution -> serialized promotion
  -> promotion diff -> fresh Phase 2 -> new commit -> independent Branch Review
  -> final reviewed HEAD carries implementation + evidence + promoted baseline delta
  -> stale/unpromoted -> sync_required and return Architecture owner
```

Global workflow owns stage order和唯一 router。`guru-approve-task-plan`、`guru-check-task`、`guru-review-branch` 只增加设计宪法/impact 的语义消费说明，不复制 Architecture owner 内部步骤。Publication/Finalizer packages 不吸收 #261/#248 语义；它们只通过 workflow router 接收 current 结果。

## 6. Contribution、ADR 与 promotion

- Architecture contribution 位于项目 Architecture authority 约定的 task-isolated root；两个 task 的 locator 必须不同。只有架构决策或状态发生变化时才携带 ADR candidate。
- Planning/implementation 只能更新当前 task 自己的 contribution，不得写 shared current。
- Branch Review pass 证明 contribution 与完整 diff 一致，但不自动改变 authority。
- `promotion` 绑定 expected current baseline identity，由唯一 Architecture owner 串行执行，并重读 current baseline、reviewed task commit、contribution/ADR candidate、设计宪法和项目检查 evidence；live identity 已推进时返回 `sync_required`，禁止覆盖。
- promotion 产生 diff 后必须重新执行受影响的 Phase 2/Branch Review current-range gate，避免“review 后新增未审查 current 文件”。
- superseded identity 保留历史边界；old/new authority 过渡期间的写入 owner 必须恰好一个，并且必须有明确 removal condition。
- task A promotion 产生新 identity 后，仍绑定旧 identity 的 task B 必须重新执行 impact、满足性与并行边界判断；两个 task 不得竞争关闭同一 GAP、建立冲突 owner 或产生两个 current authority。

### 6.1 最终 reviewed HEAD

改变长期架构事实时，Publication 可消费的最终 HEAD 必须同时包含实现、测试/运行/外部 evidence、reviewed task-local contribution、必要 ADR、promotion 后的 CURRENT/GAP/decision/owner/history 增量，以及 promotion 后重新通过的 Phase 2 与 committed full-diff Branch Review。只通过实现测试、但 contribution/ADR/promotion 缺失的 HEAD 始终不可发布。没有 shared baseline 变化时，以 current、可审核 no-change proof 代替 promotion 增量。

## 7. 代表性业务仓库场景模型

公共 fixture 用项目中立的 `target boundary / legacy boundary / owner / state authority / persistence / external evidence` 抽象表达 10 个固定场景：`no-impact`、`target-native`、`legacy-boundary convergence`、`dedicated refactor slice`、`scope expansion`、`fitness regression`、`parallel stale`、`unpromoted contribution`、`next-task consumption`、`missing external evidence`。fixture 只验证公共合同能消费项目自己的两层 authority 与 change contract，不编码 Flutter、Afizzy、Controller、ViewModel 或具体业务规则。

## 8. 原子版本切换

- 删除现有 1.0 input/output schema、示例和 selector，不建立 legacy inventory、dual-read 或 migration adapter。
- 新增显式 `2.0` aggregate/profile/output/semantic-result/check-result/contribution schema 与 examples/evals。
- 在一个 reviewed change 中同步切换 canonical Interface/runtime、workflow consumers、dogfood installed package、Shared/Codex/Claude/Cursor 和 manifest inventory；任一表面仍引用旧 schema 都阻塞通过。
- runtime 只接受 2.0。缺少或使用旧 `schema_version` 的输入明确返回 schema mismatch，不被 normalize、upgrade 或路由为 current evidence。
- stable Skill/profile/exit/consumer ids 保持不变，因此公共图仍为 21 active Skills / 89 exits；测试锁定旧 schema 零库存、active 2.0 selector 和所有 consumer 的完全一致性。

## 9. Canonical 与 projection

唯一 package source 是 `trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/`。同步范围包括 registry/interface/runtime/tests/evals、canonical workflow 与 specs、preset/README/installed manifest、`.trellis/guru-team`、`.agents`、`.codex`、`.claude`、`.cursor`。通过 preset apply 生成 dogfood/platform copies，不手工建立第二 source。

## 10. Docs SSOT 与本仓 dogfood

#283 先写 RDT 与 Architecture 两个 task-owned contribution。当前仓库 Architecture contribution 将声明项目设计宪法 locator 仍由 `docs/architecture/` 自己拥有，并投影上述五个 identity；正文解释留在唯一 authority。独立 review 后，promotion 建立下一 current-main 版本并更新 README/history/traceability；`.trellis/spec` 只同步 locator、identity、消费和 freshness 规则。

## 11. 风险与回滚

- 风险：2.0 选择器遗漏 installed/platform copy。控制：registry-derived package/installed/platform parity 与代表性 clean install。
- 风险：把原则 projection 误写成 checklist。控制：schema 不出现五项 required verdict/score，no-impact eval 断言零额外 contribution。
- 风险：Branch Review 复用 Phase 2 结果。控制：review contract 要求 committed full-diff 独立计算并绑定自己的 freshness。
- 风险：promotion 后 diff 未复核。控制：promotion 后强制 current-range Phase 2/Branch Review re-entry。
- 回滚：整体回退 2.0 schema/runtime/workflow/projection 与 current docs promotion，不能局部恢复旧 consumer 或形成双合同；已创建 contribution 保留历史而不自动成为 authority。
