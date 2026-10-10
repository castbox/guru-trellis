# #250 设计

## 当前对象与约束

本轮从 live main 的 canonical workflow/registry/interface 与 installed contract 读取：初始链为 Sync → Discovery → Clarify → Wording → readiness → task-intake；Clarify 当前五 profiles 含 initial_change_request、active_task_scope_change、standalone_review 和两种 scope confirmation；Discovery 当前仅 pre_task，needs_context 固定回 initial_change_request，无法完整表达四类 caller return。#396 的 owner-memory record/check/invoke 与 #453 的正式 stdout transport 保持。

唯一 requirement authority 是 #250 r19；RDT/Architecture 从各 README 的 active locator fresh 取得。软件与 target Trellis 从声明及实际 target 读取，均不是固定实现 SHA 或版本前置。

## 方案与替代

保留初始 Sync → Discovery → Clarify。Discovery 判断检索证据覆盖和客观库存，不判断 requirement 意图、来源优先级、设计约束、Issue intent 或 task scope；这些唯一由 Clarify 判断。当现有证据无法回答本轮 load-bearing repo/context 问题时，四类 Clarify profile 均请求 Discovery，Discovery 返回同一 profile，Clarify fresh 重建输入并继续原闭环。

未采用 Clarify-first：它会同时改变 Sync consumer、标准 duplicate-snapshot 前置和初始闭环，当前需求允许保留顺序；把 Discovery 限定为 context owner 并修复 return graph 已能满足唯一 Intake owner。不上游 patch brainstorm；方法复用由 Guru 合同约束，真实 native 结果证明效果。

公共 API 采用直接演进和同步 consumer migration；无双 reader、alias、fallback 或旧 runtime 路径。旧 schema/example 若失去当前 consumer 则退役或明确 pinned-old-only；不得继续作为当前输入。stable Skill ids 不变，变更 schema id 和迁移表显式记录。该迁移只影响任务列明的公共边界，不顺带重写未相关 DTO。

## Public profile 与 return graph

| Clarify profile | input owner 与最小内容 | 正向/回程 |
| --- | --- | --- |
| standard_intake（新） | 当前初始路由；mode、当前 target/continuation、checked duplicate snapshot；current context transition 保持独立 envelope | clear → requirements-clear-router → current Wording/readiness |
| reviewed_plan_intake（新） | 同上，加明确选定的已有需求/设计来源定位；“reviewed”不替代 fresh source review | clear 同标准链；避免重新发明已约定设计 |
| active_task_scope_change（保留） | 当前 task/source、caller resume 与既有 scope-change input | accepted_current 回 Planning；其它分类回精确 interrupted owner |
| standalone_review（保留） | 显式 review target 与 caller consumer | clear 回声明 standalone consumer；不得默认进入 task creation |
| normal_scenario_scope_confirmation（保留） | 原 qualifier 最小 projection 与 original owner | 精确选择后回 normal qualifier 声明的 owner |
| solution_mechanism_scope_confirmation（保留） | 原 qualifier 最小 projection 与 original owner | 精确选择后回 solution qualifier 声明的 owner |

四个 context-capable profile 的 needs_context output 交给 Discovery 的明确 context_request profile：沿用客观 base/context identity，仅补充 return profile、原 target/continuation；active 分支再传 TaskId/generation，standalone 分支再传声明的 consumer。使用 discriminated profile-specific branches，不把任意 public input/private owner result 塞入 optional capsule。Discovery 不读取 Clarify private state。context_ready 唯一 consumer 仍是 Clarify，由 return profile 的薄 projection fresh 组装正确 input；原 active/standalone continuation 不变。需要的 repo clue 在现有可公开检索输入中传递，不复制用户原始对话或完整审查结果。

标准首次 Discovery 的 pre_task contract 显式迁移到能声明 standard/reviewed return 的新 schema；Sync synced consumer 仍是 Discovery。context_request 接受四类 caller，按其 source/task facts 重读。两类 qualification confirmation 不被 context loop 重解释，需要 authority/context repair 时返回原 qualification owner 的现有 re-entry。

所有 exits 保持唯一 owner：clear → requirements-clear-router；needs_context → Discovery；refresh_context/retarget_context → Sync；new_task → full-task-intake-chain；blocked → clarification stop。Sync/Discovery/Wording/readiness 的既有 blocked 与 refresh exits 不改成 clear。

## API 迁移边界

| 旧当前边界 | 直接替换后的边界与 consumer |
| --- | --- |
| Clarify initial_change_request input 2.0 | standard_intake/reviewed_plan_intake 的独立新 schema 与 examples；Discovery/readiness re-entry 和 initial routing 同步更新。旧 profile 不再当前接受，错误说明迁移到新入口。 |
| Discovery pre_task input 2.0、固定 initial_change_request context_ready 3.0 | 新 schema 显式标准/已规划 initial return，以及 context_request 的四类 return；所有 producer/consumer/interface/registry evidence 同轮同步。 |
| Clarify needs_context 1.0 固定 pre_task | 新 output schema 按调用 profile 提供最小 return identity；Discovery input projection 精确校验。 |
| Clarify clear 2.0 及 clear router | 新 output schema 按 profile 表达 minimal source selection；current Wording/readiness 保持其判断，薄 relay 仅传递下一 router/Planning 必需的来源定位和不可重新推导选择。 |
| upstream brainstorm 自动发现 | 保持上游 Skill；Guru workflow 和 Guru-owned entry 明确加载时的本轮 owner/stage/return 约束，不复制上游内部实现。 |

本轮 schema 迁移编号：Clarify aggregate 3.0、standard/reviewed input 各 1.0、clear 3.0、needs_context 2.0；Discovery pre_task input 3.0、context_request 1.0、context_ready 4.0。受影响 stage0 public relay schema 使用明确 successor identity；如 live base 已先推进同一编号，先按原 reconcile owner调整而非覆盖。旧已发布语义写入 migration contract，不静默改名。兼容策略为同步升级完整 Guru preset/current callers；在途旧 invocation 不被转换成新成功 DTO，按既有 source refresh/re-entry 获得当前合法输入，不新增长期兼容支持。跨仓调用方需完整 preset 与当前 interface，不能拿单个 package 自洽。

## 来源承接与 Planning 薄接缝

Clarify fresh 读 Direct Source、明确选定 comments、被引入需求/设计来源及必要 Related Work；区分规范性条款和建议。source selection 只包含 load-bearing source locator/section 及本轮不可重新推导的语义选择；不包含 retain/change/reject、全文、第二设计模型、review transcript 或授权。直接 consumer 是 clear router 及其最终当前 Planning author；Wording/readiness 仅按已声明薄 projection 传递，内容变化回最早 affected owner 重读。

Create Task 的 created DTO 保持 TaskId/TaskRef/generation，不把来源模型塞入 task.json。guru-task-created 从 live identity/binding/checkout 解析任务后，当前 Planning fresh 读 Direct Source 并消费相邻 current source selection；把来源定位写在 prd.md 的 authority，最终技术处置只写 design.md。选择结果若已丢失，恢复通过原 Clarify/context owner 重新收敛，不能猜测被选 comments 或增加 shared cache。未来 #292 接入时用同一最小来源 projection，#250 不注册未来必需 Author、task_created_attach 或新 consumer gate。

改变产品意图/accepted scope/明确设计约束进入现有 requirements/Architecture owner；普通技术细化在 design rationale。原 Issue intent none/create/reuse/reference_only 不改变 Source/Closure authority。

### 对 #250 r19 规范性来源的最终处置

| 来源章节 | 本设计处置与落点 |
| --- | --- |
| 唯一 semantic owner 与边界 / Requirement authority | retain：Clarify 独占 Intake 语义；来源定位与规范性/建议分类由其处理；最终设计只在当前 Planning。 |
| 路由与独立交付 / Discovery conditional loop | retain：六 profiles、四类条件请求、两类 qualifier；保留初始顺序并修复 caller return；不引入未来 #292 前置。 |
| Brainstorm 协作边界与实际入口行为 | retain：上游 discoverable，不 patch；Guru entries/workflow/Clarify 限定实际 owner 和回程，zero/one/partial 行为由 native 验证。 |
| Issue intent 与 mutation / Scope change、失效与恢复 | retain：使用原 GitHub mutation/Sync/source/task owners；依赖范围失效、#468 恢复和 no_issue 保持。 |
| 验证与完成标准 | retain：定向 package/distribution + 真实 Agent、新/已有安装；完整 Release matrix 明确未验证。 |

未 reject/change 任何 accepted 来源约束。没有以“新 Issue 更新”覆盖其它被明确引入 authority 的规则。

## Scope-change ingress 和失效

| Current producer/exit | consumer 与最早 affected owner |
| --- | --- |
| Planning/Approval clarify_scope | guru-task-plan-clarify-scope-router → Clarify active profile |
| Architecture architecture_conflict/contract_incomplete | architecture-planning-router → Planning/repair；真实 authority choice 再进入 Clarify |
| Reconcile Base scope_confirmation_required | guru-task-base-scope-router → Clarify |
| Check planning_stale | guru-task-check-planning-router → plan approval 或 Clarify，按真实 planning_action |
| Branch Review scope_confirmation_required | guru-branch-review-scope-router → Clarify |
| Delivery Review scope_confirmation_required | guru-task-delivery-scope-router → Clarify |
| Completion requirements_revision_required | task-requirements-revision-router → Clarify |
| task-free scope_change | guru-task-free-scope-change-router → exact bound active Clarify；非 active 走 standard intake |

以上由 live interface/router 消费，不新增 retired Publication/Acceptance owner。仅对 accepted scope/source/design/test/evidence 依赖受变化影响的 gate 重入；无关 Related Work 更新不作废整条链。active clear 之后 Planning、Wording、Architecture、Approval 和当前 activation consumer 仍按 #468 resume_execution 恢复；TaskId/generation/source/session/checkout 不重建。

## 状态、脚本与分发

Markdown 负责提问、authority、source/Issue intent、scope、readiness、route 和设计取舍。脚本只验证闭合 schema、profile/consumer projection、current identity/freshness、正常 stale/mismatch 与写入客观结果；不从关键词、Issue 内容、brainstorm 加载次数或字段存在推断 semantic pass。

canonical 来源为 trellis/workflows/guru-team、trellis/skills/guru-team 和 preset overlays/source；dogfood 为受管投影。同步 apply.sh 后运行 check-dogfood-overlay-drift.sh，逐个处理 .new/.bak，不覆盖用户修改。README/spec 只维护正确 owner/locator/migration，RDT 与 Architecture 通过原隔离 contribution/promotion 流程保持唯一 authority。

不新增 durable Intake artifact；已有 owner-private stdout/checkpoint 生命周期保持。授权只在当前对话。无额外 session slot、ledger、cache、机器路径状态。触及非生成代码超过 3000 行时仅做必要机械拆分，不借机扩大历史清理。

## Architecture change contract 与 Docs SSOT Plan

Planning 独立 Architecture owner 从真实设计与 affected consumers 判定 impact/path/贡献/ADR；该结论不能由本文件预填。项目合同：docs/architecture/06-governance/change-contract.md；constitution：docs/architecture/00-foundation/design-constitution.md。允许本 task 隔离 contribution，禁止同时改 shared current/GAP 或竞争 owner。贡献与需要的 ADR 先保持候选，完整独立 Branch Review 后再由原 owner expected-current promotion，随后重新执行必要 gates。

Docs 状态：现有 RDT/Architecture active 可读；usage projection .trellis/spec/architecture/baseline-usage.md 有旧版本摘要，不能当 authority。strategy 为隔离贡献 + 受影响文档定向同步；不在规划阶段批量修正历史版本正文。长期输出：
- docs/requirements-design-test-contributions/250-phase0-intake-owner/{manifest.yaml,requirements.md,design.md,test.md,traceability.md}：accepted delta 与唯一实际 Test locator。
- 由 Architecture owner 判定必需时，docs/architecture/contributions/250-phase0-intake-owner.md 及必要 ADR candidate；无 impact 则无需贡献。
- canonical workflow/Skill contracts 为行为 SSOT；README/spec 只描述当前入口、迁移与证据导航，不复制第二套 step-local 行为。
- promotion 前不修改 shared current；晋升由既有 RDT/Architecture owner 串行执行并验证 expected current，晋升 diff 再经 fresh Check/commit/独立完整 Branch Review。

affected docs：workflow 与 preset README、受影响 package contracts、workflow-contract.md 的 Phase 0/continuation、skill-package-contract.md 的 Public I/O migration，以及 semantic-retrieval.md/quality-guidelines.md 的受影响 owner references 和对应受管模板。checked no-update：Release matrix、软件版本轴、业务仓 PRD、upstream trellis-*、无关联历史 task/ADR，不宣称新验证。task artifacts 仅三文档与必要 JSONL context，不存 gate/授权/qualification 报告。Phase 2 执行该 Docs SSOT Plan 并检查重复/旧入口退役；Branch Review 只验证已完成 reconciliation。发现文档落点不足回原 Planning/SSOT owner，无新 ledger。

## 验证边界

验收场景位于 prd.md；具体执行步骤在 implement.md。真实 Agent 与正式 invocation 是语义/dispatch 证据，static/package 不能代替。完整多平台/Release、远端新 tag、额外业务安装和部署保持专门 owner 的未验证边界。实际 upstream 入口依赖缺失时报告最小 owner/prerequisite，不在本 task patch。
