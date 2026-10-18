# #283 Requirements contribution

本 contribution 绑定 Issue `#283`、task
`283-architecture-convergence-governance` 与 active Architecture Baseline
`current-main-0.6.5-guru.37`。它是 task-isolated candidate，不是 current authority；
只有独立 review 后的串行 promotion 才能更新 shared Requirements/Design/Test 或
Architecture Baseline。

- `REQ-027`：Architecture Baseline 必须成为标准 task 从 Planning、implementation
  discovery、Phase 2、Branch Review、Publication 到 Acceptance/Finish 的唯一项目架构
  SSOT。阶段只消费 current identity、task-local change contract 与 typed route；schema
  和 runtime 只支撑该生命周期，不成为架构判断 owner。
- `REQ-028`：每个标准 task 必须进入 Architecture semantic owner。Guru Team 方法论
  identity 与项目 Architecture Baseline/change-contract identity 必须在 task-local contract
  同时存在；任一缺失、过期或矛盾均 fail closed。scope、risk、owner、持久化、SDK、外部
  或架构边界扩大时，旧 Planning 结果 stale 并重新判断。
- `REQ-029`：项目 Architecture Baseline 必须唯一声明设计宪法 authority locator 及
  version 或 content identity。Guru Team 只消费以下五个 identity/short name，不拥有原则
  正文、解释、评分或逐项 verdict：`mature-practice-applicability`（成熟实践与适用性）、
  `concept-semantic-completeness`（概念与语义完整性）、
  `cohesion-change-isolation`（职责内聚与变化隔离）、
  `minimum-necessary-complexity`（最小必要复杂度）、
  `debt-one-way-convergence`（技术债务单向收敛）。
- `REQ-030`：`architecture_impact` 必须恰好选择 `target_native`、
  `legacy_boundary_convergence` 或 `dedicated_refactor_slice`；
  `no_architecture_impact` 是独立快速结果。本 task 选择 `target_native`，只建立新 2.0
  架构治理合同，不清理无关历史债务、不新增 legacy authority，也不实现业务仓库重构。
- `REQ-031`：architecture change contract 必须绑定 requirement/behavior authority、
  baseline/constitution、domain/integration/decision/GAP、required concerns、current/target
  owner、single-writer、compatibility exit、parallel scope、deviation/deletion conditions、
  design responsibility、before/after、项目检查、evidence、contribution/ADR/review/promotion
  与 expected current identity。适用字段 missing/empty/stale 或无法证明
  `not_applicable` 时不得继续。
- `REQ-032`：Phase 2 必须首次判断 candidate before/after 满足性，Branch Review 必须在
  committed full diff 上独立重算。项目检查结果至少包含 identity/version、applicable
  scope、rule/decision/GAP refs、before/after、`pass|fail|unverified`、evidence 或
  unavailable reason、freshness，以及 AI 根据 applicability 与任务真实依赖判断的
  `blocking`；新增或恶化偏移稳定返回 `fitness_regression`。
- `REQ-033`：普通 task 只写自己的 RDT/Architecture contribution。只有新增或改变
  architecture decision、原则权衡/例外、GAP 生命周期、owner/single-writer 或
  compatibility exit 才要求 ADR candidate。shared current 只能由唯一 Architecture owner
  在独立 review 后按 expected current identity 串行 promotion；本 task 因改变长期治理
  decision 与 promotion/single-writer 合同而需要 ADR candidate。
- `REQ-034`：并行 task 可各自维护不同 task-owned contribution，但不得在 review 前写
  shared current、竞争关闭同一 GAP、建立冲突 owner、形成双写或产生两个 current
  authority。任一 promotion 推进 current identity 后，仍绑定旧 identity 的 task 必须返回
  `sync_required` 并重新执行 impact、满足性与 parallel-scope 判断。
- `REQ-035`：2.0 schema/runtime、canonical/dogfood/installed/platform projection 与
  project-neutral fixture 必须原子承接上述生命周期，但不复制业务规则。#283 不启动
  #267，不声明 stable tag、Release、exact-candidate 全平台矩阵或生产结果，也不实施任何
  business-repository refactor；外部 evidence 不可得时保持 `evidence_gap|unverified`。

本 candidate 不包含 promotion 结论，不把后续 successor version 称为 current，也不修改
`docs/requirements/`、`docs/design/`、`docs/test/` 或 shared `docs/architecture/` 正文。
