# Requirements 决策与 provenance

当前 .48 来源：`castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291` / CLI/core `0.6.16`；Guru manifest `0.6.16-guru.41`；repository release target `v0.6.16-guru.1`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.5-guru.48` / `active`。
继承段落中的旧版本映射、矩阵及历史 promotion 只绑定其原版本，不声明当前 Fork 的完整兼容或 Release；当前 #392 增量见本文件末节及同版本 traceability。


- `RDEC-001`（accepted）：current knowledge authority 使用 `current-main-0.6.5-guru.48`，明确区别于
  正式 predecessor `v0.6.15-guru.6` 与 current target `v0.6.16-guru.1` / extension
  `0.6.16-guru.41`；当前 Fork CLI 为 `0.6.16`。
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
- `RDEC-019`（accepted）：reviewed #332 original-entry contribution 绑定 expected `.44` promotion 为
  `.45`；四阶段原 wrapper/command 保持 public identity，Interface 成为 generic wrapper selection 唯一
  authority，23/97/77 为 current graph。该 promotion 不证明 release，也不复用旧 candidate evidence。
- `RDEC-020`（accepted）：reviewed #376 contribution 绑定 expected `.45` serialized promotion 为 `.46`；
  Reconcile 继续拥有 semantic classification 与唯一 local expected-head commit，Review Branch 只拥有 bounded
  continuity judgment，Publication 继续严格绑定 current reviewed-content identity。该 direct evolution 不新增
  public Skill/exit、compatibility branch、第二 writer、remote mutation、ADR 或 Release proof。

- `RDEC-021`（accepted）：#378 将 expected immutable `.46` 承接为唯一 current `.47`；R378 IDs 保持稳定，原来源入口直接迁移到固定 Fork，不保留长期双源 fallback。Guru manifest `0.6.15-guru.40`、Fork CLI `0.6.16` 与 Docs `.47` 是独立版本轴，均不证明 npm/tag/Release 已发布。

- `RDEC-022`（accepted）：#392 将 reviewed contribution
  `architecture-contribution-392-release-v0616-guru1-v2` 与五文件 RDT contribution 绑定 expected
  immutable `.47`，serialized promotion 为唯一 active `.48`。current mapping 收敛为
  `v0.6.16-guru.1` / extension `0.6.16-guru.41` / CLI `0.6.16` / fixed Fork full SHA；public graph
  保持 23/97/78。promotion 不授权 Publication、merge、tag、Release、full matrix、business smoke 或 Issue
  closure；promotion-created diff 必须重新进入 fresh Phase 2、task commit 与独立完整 Branch Review。
