# #283 Architecture contribution and ADR candidate

## Candidate identity and authority boundary

- Issue：`https://github.com/castbox/guru-trellis/issues/283`。
- task：`283-architecture-convergence-governance`；locator：
  `.trellis/tasks/08-20-283-architecture-convergence-governance`。
- profile：`guru-maintain-architecture-baseline:task_impact_sync`。
- impact/path：`architecture_impact` / `target_native`。
- live authority binding：`docs/architecture/README.md` /
  `current-main-0.6.5-guru.37` / `active`。
- expected current identity at promotion：`current-main-0.6.5-guru.37`；successor identity
  只能由 reviewed promotion 分配。
- contribution state：`phase2_reviewed_candidate_pending_independent_full_diff_review`；
  promotion state：`required_not_started`；本文件不构成 CURRENT、accepted ADR 或 promotion
  证明。

本 contribution 只提出让 Architecture Baseline 在完整 task 生命周期中单向收敛的长期
治理增量。Architecture schema 2.0、runtime 和项目检查协议是 supporting infrastructure，
不成为项目架构语义 owner。

## Proposed baseline identities

- `ARCH-FND-006`：项目 Architecture Baseline 必须唯一声明设计宪法 authority locator
  与 version/content identity；Guru Team 只消费稳定 identity/short name，不拥有原则正文、
  解释、评分或逐项 verdict。
- `ARCH-GOV-006`：每个标准 task mandatory 进入 Architecture semantic owner，并按
  Planning -> implementation discovery re-entry -> Phase 2 -> committed full-diff Branch
  Review -> Publication -> Acceptance/Finish 消费 current authority 与稳定 typed route。
- `ARCH-GOV-007`：Guru Team 方法论维度和项目 Architecture 语义维度只在 task-local
  Architecture change contract 相交。架构相关 task 缺任一 public/project identity、适用
  concern、fresh evidence 或一致性证明时 fail closed。
- `ARCH-GOV-008`：普通 task 只写 task-owned contribution；shared current 由唯一
  Architecture owner 在 independent review 后按 expected current identity 串行 promotion。
  live current 推进使旧 task 返回 `sync_required`，不得覆盖或形成双 current authority。
- `ARCH-DOM-008`：Architecture lifecycle governance 由
  `guru-maintain-architecture-baseline` semantic owner 持有；项目 baseline/change contract
  持有具体 decision、GAP、owner、concern 和 check semantics；global workflow 只拥有阶段顺序
  与唯一 router。
- `ARCH-INT-007`：项目可声明 architecture check descriptor/result；公共合同只统一
  identity/version、applicability、rule/decision/GAP refs、before/after、
  `pass|fail|unverified`、evidence/unavailable reason 与 freshness，AI 判断语义 route。
- `ARCH-GAP-006`：`.37` current 尚未持有设计宪法 locator/identity、双维 task-local
  change contract、全阶段 before/after/project-check consumption 与 promotion 后 next-task
  consumption 合同。owner 为 #283 Architecture promotion；closure condition 是 reviewed
  implementation/evidence/contribution/necessary ADR 一并 promotion 到 successor current，
  并在 promotion 后重新通过 Phase 2 与独立 Branch Review。

这些 identity 在本文件中均是 proposed candidate。独立 review/promotion 前，current
`ARCH-FND-001..005`、`ARCH-GOV-001..005`、`ARCH-DOM-001..007`、
`ARCH-INT-001..006` 与 `ARCH-GAP-001..005` 保持唯一 active authority。

## Design constitution projection candidate

- authority owner：项目 `docs/architecture/`。
- candidate locator：`docs/architecture/00-foundation/design-constitution.md`。
- identity kind/version：`version` / `guru-trellis-design-constitution-v1`；当前状态为
  `pending-reviewed-promotion`，只有 promotion owner 验证并写入 shared authority 后才可
  标为 active。
- minimal projection：

  | Identity | Short name |
  | --- | --- |
  | `mature-practice-applicability` | 成熟实践与适用性 |
  | `concept-semantic-completeness` | 概念与语义完整性 |
  | `cohesion-change-isolation` | 职责内聚与变化隔离 |
  | `minimum-necessary-complexity` | 最小必要复杂度 |
  | `debt-one-way-convergence` | 技术债务单向收敛 |

本表只建立可验证引用，不定义原则正文或解释。Task 只在真实冲突、权衡、例外或 baseline
不足时引用命中的 principle 和 evidence；no-impact/current-conforming task 不创建空白行、
contribution 或 ADR。

## Task-local Architecture change contract

### Authority, path, and boundaries

- Guru public identity：`guru-maintain-architecture-baseline:2.0` candidate。
- project baseline identity：`docs/architecture/README.md` /
  `current-main-0.6.5-guru.37` / `active`。
- project change-contract identity：`guru-trellis-architecture-change-contract-v1`
  candidate；required concern set：`guru-trellis-architecture-change-concerns-v1`
  candidate。
- requirement/behavior authority：Issue #283 与本 task RDT contribution；task planning
  artifact 只提供 approved delta，不替代 durable authority。
- current boundary：`.37` Architecture owner/profile 与已有 FOUNDATION/GOVERNANCE rules。
- target boundary：完整 task lifecycle 的 mandatory current reading、satisfaction checks、
  necessary contribution/ADR、reviewed promotion 与 next-task consumption。
- change path：`target_native`。不清理无关历史债务，不增加 legacy authority，不引入
  dual-read 或 migration adapter。

### Required concerns

| Concern | Applicability for #283 | Candidate evidence/route |
| --- | --- | --- |
| `authority-binding` | applicable | Guru 2.0 candidate + project `.37`; stale -> `sync_required` |
| `constitution-binding` | applicable | candidate locator + pending identity; missing at promotion -> `contract_incomplete` |
| `boundary-and-decision` | applicable | proposed identities + `ADR-283-CANDIDATE` |
| `owner-and-single-writer` | applicable | Architecture owner is sole shared-current promotion writer |
| `compatibility-and-exit` | applicable | no dual-read; exit when all producers/consumers/projections accept only 2.0 |
| `gap-and-deviation` | applicable | open `ARCH-GAP-006`; no release GAP closes |
| `parallel-scope` | applicable | isolated locators allowed; shared current/GAP/owner competition forbidden |
| `evidence-and-freshness` | applicable | Phase 2 + independent committed-diff review + promotion reread required |
| `review-and-promotion` | applicable | candidate pending; no current claim before both complete |

### Owner and single-writer

- current semantic owner：`guru-maintain-architecture-baseline`。
- target semantic owner：unchanged。
- task writer：只写
  `docs/architecture/contributions/283-architecture-convergence-governance.md` 与对应 RDT
  contribution。
- shared-current single-writer：独立 review 后进入 `promotion` 的 Architecture owner；
  review 前 writer count 为零。
- compatibility owner：Architecture owner；本 task 不保留 compatibility layer。删除/退出
  条件是 canonical、dogfood、installed、声明平台、consumer 与 fixture 对旧 schema 零引用且
  代表性 installed verification 通过。

### Parallel scope

- allowed：不同 task-owned locator、独立 decision/GAP/owner scope、只读同一 expected
  current `.37` 的并行 implementation 与 review preparation。
- forbidden：直接编辑 shared current；两个 promotion writer；竞争关闭 `ARCH-GAP-006`
  或其他同一 GAP；建立冲突 semantic owner/single-writer；旧/新 authority 双写；把未 review
  successor 称为 current。
- stale rule：任一 reviewed promotion 推进 live identity 后，仍绑定 `.37` 的 task 必须
  `sync_required`，重做 impact、before/after satisfaction 与 allowed/forbidden 判断。

### Before, after, checks, and evidence

- before plan：`.37` 有 Architecture profile 与 task contribution/promotion 基础规则，但
  缺设计宪法 identity、双维 change contract、全阶段 before/after/project-check 与
  next-task consumption 的闭合合同。
- after candidate：2.0 package/workflow/projection 与 project authority candidate 形成同一
  lifecycle；schema/runtime 仅验证结构与 freshness；semantic owner 仍判断适用性、冲突、
  regression、review 与 promotion。
- planned closed deviation：`ARCH-GAP-006`，仅在 reviewed promotion 与 promotion 后 fresh
  gates 完成时关闭。
- retained deviations：`ARCH-GAP-001..005`，原因、owner 和 closure condition 保持 current；
  #283 不改变 #267 release ownership。
- new deviation：none planned；legacy deletion condition 是 1.0 schema/example/selector/
  compatibility input 零库存且全部 current consumer 原子切换到 2.0。
- project check：`guru-trellis-architecture-convergence@1`，覆盖 authority/path/
  concerns/before-after/single-writer/parallel stale/review/promotion freshness；本次 Phase 2
  对完整 worktree candidate 的当前结果为 `pass`、`blocking=true`。证据 locator 为 RDT
  contribution 的 `test.md` 当前验证摘要；`guru-check-task` schema 5.0 已完成九维语义检查并
  返回 `passed`。完整 worktree content identity 只保留在 owner-private checkpoint，本文件
  状态同步后由 live content fresh 重录，不复制 token。其他 task 的 AI owner 仍必须结合
  applicability 与 task real dependency 独立判断 `blocking`；runtime 不代替该判断。
- evidence：Architecture source/installed contract `22/22`、source/installed graph、
  source/installed fixed 10-scenario eval、三个阶段 consumer、RDT/package/finish/semantic
  closure、preset ownership/apply/reapply/upgrade、dogfood drift、JSON/Python/Bash/task/diff
  静态门禁均已对当前 candidate fresh 通过；详见 RDT `test.md`。当前 dirty candidate 还在无
  `.git` 的隔离目标完成了 Trellis `0.6.15` 代表性 clean installation：公开 marketplace
  初始化后明确覆盖当前 canonical workflow，应用当前 all-platform preset，并通过 installed
  validation、Architecture `22/22`、installed/shared 十场景、Phase 2 context smoke、四平台
  parity、reapply 与 zero-sidecar。该 targeted 证据不证明未发布 branch marketplace ref。
  正式 `guru-verify-extension-installation` 要求 clean source 与解析到当前 HEAD 的 requested
  ref；当前 dirty/unpublished 状态不具备合法 executor entry，也没有形成 `verified` typed
  exit。Phase 2 的三个修复候选已在 current supported path 上重新判定为
  `rejected_not_reproduced`，open finding 为零；原 committed-diff review finding closure 仍须
  新 task commit 与 distinct fresh-final Branch Review 证明。serialized promotion、promotion
  后 fresh gates 与新 exact-commit verification 仍为 pending，本 contribution 不把它们声明
  为已完成。

## ADR-283-CANDIDATE

- status：`candidate_pending_independent_review`；不是 accepted ADR。
- trigger：#283 改变长期 architecture governance decision、设计宪法 authority projection、
  GAP lifecycle、shared-current single-writer/promotion 与 project-check consumption，因此满足
  necessary ADR trigger。它不因单纯 schema shape 变化而触发。
- candidate decision：采用“双维 authority + task-local change contract”的端到端 lifecycle；
  普通 task 只形成 isolated contribution/necessary ADR，shared current 只经 expected-identity
  bound serialized promotion 更新，并强制 promotion 后重新检查与 next-task consumption。
- rejected direction：schema/runtime 独自决定架构充分性；task 直接写 shared current；保留
  1.0 dual-read/adapter；把五项原则变成逐项评分；由公共 fixture 写入业务规则。
- consequence：Architecture owner 和项目 authority 各自保持单一职责；适用 evidence 缺失
  会 fail closed；并行 task 在 current 推进后必须 re-entry；文档成本只发生在真实
  architecture impact 或 necessary ADR 场景。
- acceptance condition：完整 #283 implementation/evidence、RDT/Architecture contribution、
  independent Branch Review 与 serialized promotion 位于最终 reviewed HEAD，promotion 后
  Phase 2/Branch Review 重新通过，successor identity 被 next-task Planning smoke 读取。

## Explicit boundaries

- #267 独占 stable tag、GitHub Release、exact-candidate 全平台矩阵与 immutable smoke；#283
  只允许 targeted package/runtime/projection 和一个代表性 clean installation 证据。
- 本 contribution 不声明 release、production、store、SDK/backend live outcome，不关闭
  `ARCH-GAP-001..005`，也不启动 #267。
- 本 task 不实施任何 business-repository refactor，不硬编码 Afizzy、Flutter、Controller、
  ViewModel 或业务阈值；项目具体 checker/semantics 仍由各业务仓 Architecture Baseline 拥有。
- #247/#249/#250/#261/#248/#252 与 #108 的 owner/scope 不由本 candidate 吸收。
- review 前禁止修改 `docs/architecture/` shared current、设计宪法 current identity 或
  RDT current authority，也不得把 `.trellis/spec` 当作项目 Architecture authority。
  #283 的 canonical preset spec 可按 approved scope 生成字节一致的 dogfood
  `.trellis/spec` locator/identity/消费/freshness 投影；该投影不构成 promotion 或 shared
  current。本文件只能被后续 review/promotion 消费，不能自行宣称 promotion/current。
