# Requirements 决策与 provenance

- `RDEC-001`（accepted）：current knowledge authority 使用 `current-main-0.6.5-guru.44`，明确区别于
  latest stable `v0.6.15-guru.4` / extension `0.6.15-guru.39`、current target
  `v0.6.15-guru.5` / extension `0.6.15-guru.40` 与 Trellis CLI `0.6.15`。
- `RDEC-002`（accepted）：旧 requirements 文件改为导航，避免双 current authority。
- `RDEC-003`（accepted）：从 current workflow/registry/interface 恢复的行为标为 `code_recovered`，不冒充原始产品 intent。
- `RDEC-004`（accepted）：#263/#264/#265 PR body 中的测试数字只作为 historical focused evidence，不自动转写为本次 PASS。
- `RDEC-005`（accepted historical boundary）：#260 建立 Trellis `0.6.15` compatibility；#267 当时独占
  `v0.6.15-guru.3` / extension `0.6.15-guru.39` 的 exact-candidate lifecycle。其历史 promotion/package
  evidence 不晋升为 #332 `.5/.40` Release Gate proof。
- `RDEC-006`（source_confirmed）：#262 以“当前无法复现、证据不足”关闭；其关闭评论记录 exact source targeted 10/10 与 suite 44/44 PASS，但没有 code fix，也不能证明 current main 或后续 release candidate。
- `RDEC-007`（accepted）：`.agents` 是每个声明平台 cell 的 shared public projection，不是第四个 Trellis CLI platform；package-private validator wrappers 不分发到 platform roots。
- `RDEC-008`（accepted）：A/B compatibility harness 只产生 #248/#252 可消费的事实，不新增 Acceptance、Finish 或 cleanup public owner。
- `RDEC-009`（accepted）：Architecture Baseline 是全 task lifecycle 的唯一项目架构 authority；双维 identity 只在 task-local change contract 相交，shared current 只经 independent review 后的 expected-current-bound serialized promotion 前进。
- `RDEC-010`（accepted）：设计宪法正文归项目 Architecture authority；公共合同只投影五个稳定 identity/short name，不建立 scorecard、逐项 verdict 或第二 authority。
- `RDEC-011`（accepted）：base selection 与 authority checkout binding 是两个顺序固定的确定性阶段；detached session 仅承载调用，selected-base authority checkout 独占同步、clean 与三向 equality，下游按 source 与完整 candidates 重新验证 provenance。
- `RDEC-012`（accepted）：installed Finalizer 将 extension source checkout 与 target reviewed
  checkout 分离，使用 closed `self_hosted|installed` binding；standalone verifier failure evidence
  保持独立 owner。该 knowledge promotion 不证明真实 fixture closeout、生产发布或错误文件重试。
- `RDEC-013`（accepted）：#267 reviewed contribution 先由 Architecture owner、后由 RDT owner 绑定
  expected `.41` 串行提升为 `.42`；`.42` 只更新 release/current facts、navigation、traceability 与
  evidence，不改变产品行为、公共 Skill API、Architecture decision、owner、GAP 或 compatibility exit。
- `RDEC-014`（accepted）：#335 将 `release-guru-trellis-version` 定义为仅属于本仓库的正式发布
  编排 Skill。它不进入 Guru Team 公共 registry、marketplace、preset 或业务仓库 installed projection，
  也不执行或替代任何发布 mutation owner。
- `RDEC-015`（accepted）：正式发布分为 preparation PR 与 post-merge exact candidate 两阶段；稳定
  delivery bytes 进入既有 Phase 2/commit/review/publication/finalization 生命周期，运行态 Gate 与外部
  副作用状态只由 live facts 或 owner-private checkpoint 承接，不写入 tracked authority。
- `RDEC-016`（source_confirmed + reviewed）：#332 以 latest stable `v0.6.15-guru.4` / extension
  `0.6.15-guru.39` 为 predecessor，将 `.5/.40/CLI 0.6.15` 固定为唯一 current target。#311 已完成的
  source/target provenance 前置由 #332 exact-candidate installed business-repository Release Gate fresh 消费；
  历史 package/Issue/PR evidence 不晋升 tag、Release、smoke 或 closeout 状态。
- `RDEC-017`（accepted）：#240 的场景/机制双 owner 与 OS primitive authority 禁止合同经 PR #346
  独立 Branch Review 后由 `.44` promotion 接受为 `ADR-008`；普通文件/目录例外保持。
- `RDEC-018`（accepted）：#348 的 Merge task-work re-entry 与 archived-task recovery 经 PR #351
  独立 Branch Review 后进入 `.44`；它复用既有 lifecycle recovery model，不新增 ADR。
