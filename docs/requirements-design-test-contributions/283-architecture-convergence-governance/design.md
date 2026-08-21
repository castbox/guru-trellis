# #283 Design contribution

## Candidate authority binding

- Issue/task：`#283` / `283-architecture-convergence-governance`。
- source 与 expected current：`docs/architecture/README.md` /
  `current-main-0.6.5-guru.37` / `active`。
- profile：RDT 与 Architecture 均为 `task_impact_sync`；Architecture impact 为
  `architecture_impact`，唯一 change path 为 `target_native`。
- candidate contract：`guru-maintain-architecture-baseline:2.0`；它只有 reviewed
  promotion 后才能成为 shared current contract。

## Design responsibilities

- `DES-026`：双维 architecture contract 以 task-local change contract 为唯一交叉点。
  Guru Team 维度拥有 mandatory stage invocation、semantic route 与 freshness；项目维度
  拥有 baseline、constitution、required concerns、项目检查及具体正确答案。两边都不复制
  对方正文。
- `DES-027`：生命周期顺序固定为 current baseline/constitution -> Planning impact/path ->
  implementation discovery expansion re-entry -> Phase 2 project checks + first before/after ->
  task contribution/necessary ADR -> committed full-diff Branch Review -> serialized promotion ->
  successor identity consumed by the next task。Publication/Finish 只消费 fresh
  `baseline_current`、reviewed+promoted contribution 或明确 no-change。
- `DES-028`：设计宪法 candidate authority locator 为
  `docs/architecture/00-foundation/design-constitution.md`，由项目 Architecture authority
  唯一拥有。公共最小 projection 只含五个 identity/short name：

  | Identity | Short name |
  | --- | --- |
  | `mature-practice-applicability` | 成熟实践与适用性 |
  | `concept-semantic-completeness` | 概念与语义完整性 |
  | `cohesion-change-isolation` | 职责内聚与变化隔离 |
  | `minimum-necessary-complexity` | 最小必要复杂度 |
  | `debt-one-way-convergence` | 技术债务单向收敛 |

  candidate version identity 为 `guru-trellis-design-constitution-v1`；只有 promotion owner
  在建立并验证 shared authority 后才能将其标为 active。本 contribution 不拥有原则正文，
  不为未命中的原则创建 checklist rows。
- `DES-029`：本 task 的 `target_native` contract 绑定 `ARCH-FND-001..005`、
  `ARCH-GOV-001..005`、`ARCH-DOM-003`、`ARCH-DOM-006`、`ARCH-INT-004` 与
  `ARCH-GAP-004`，并提出 `ARCH-FND-006`、`ARCH-GOV-006..008`、
  `ARCH-DOM-008`、`ARCH-INT-007`、`ARCH-GAP-006` candidate。它不关闭 release GAP，
  不扩大 legacy owner，不引入 compatibility layer。
- `DES-030`：required concern set identity 为
  `guru-trellis-architecture-change-concerns-v1`，至少包含
  `authority-binding`、`constitution-binding`、`boundary-and-decision`、
  `owner-and-single-writer`、`compatibility-and-exit`、`gap-and-deviation`、
  `parallel-scope`、`evidence-and-freshness`、`review-and-promotion`。每项显式标记
  `applicable|not_applicable` 并给出依据；architecture impact 不得用空值代替判断。
- `DES-031`：project-check descriptor candidate 为
  `guru-trellis-architecture-convergence@1`，scope 覆盖 stage invocation、authority
  binding、path exclusivity、required concern completeness、before/after regression、
  single-writer、parallel stale、contribution/ADR review state 与 promotion freshness。
  语义 owner 依据 applicability 与 task real dependency 给出 `blocking` 并决定 route；
  通用 runtime 只校验 shape/locator/freshness 与 blocking-route consistency。
- `DES-032`：稳定 route 保持唯一 consumer：缺适用 contract/constitution/check facts 为
  `contract_incomplete`；方案与 current authority 冲突为 `architecture_conflict`；新增或
  恶化偏移、owner 扩张、双写或 closed GAP 重现为 `fitness_regression`；baseline、
  constitution、contribution 或 expected-current stale 为 `sync_required`。Publication 不得
  把任一路由补写为通过。
- `DES-033`：Architecture owner 是 architecture semantics 与 promotion 的唯一 owner；
  task writer 只写 task-owned contribution，shared-current single-writer 仅在 reviewed
  promotion 窗口内写入。compatibility layer 对本 `target_native` task 为
  `not_applicable`，理由是 2.0 全消费者原子切换且不保留 dual-read/adapter；退出条件是
  canonical、dogfood、installed、声明平台及 consumer 全部只接受 2.0。
- `DES-034`：public schema/runtime 是 supporting infrastructure。固定项目中立 fixture
  覆盖 10 个 approved scenario；targeted package/runtime/projection 与一个代表性 clean
  installation 证明 #283，完整多平台 exact-candidate、tag/Release 与 immutable smoke
  保留给 #267，business repository 的具体 checker、阈值与重构不进入公共包。

## Parallel and promotion contract

- allowed：绑定同一 expected current `.37`、写不同 task-owned locator、且不竞争相同
  decision/GAP/owner 的独立 task。
- forbidden：review 前写 shared current；两个 shared-current writer；并行关闭同一 GAP；
  冲突 owner/single-writer；未 promotion 即声明 successor/current。
- stale handling：task A promotion 推进 identity 后，task B 的 `.37` binding 只可返回
  `sync_required`，重读 live authority 后重新判断，不得覆盖。
- review state：`candidate_pending_review`；promotion state：`required_not_started`；candidate
  successor identity：`assigned-by-reviewed-promotion`。
