# #247 Issue Scope Ledger retirement Architecture contribution

## Identity And Authority Boundary

- contribution identity：`architecture-contribution-247-remove-issue-scope-ledger-v1` / `reviewed_promoted`。
- requirement authority：live Issue #247 `2026-09-13-r19`、task `prd.md` 与 #247 RDT contribution。
- behavior authority：task `design.md`、`implement.md` 与 #247 RDT contribution。
- promotion input：`docs/architecture/README.md` / expected `current-main-0.6.5-guru.49`。
- promoted successor：`current-main-0.6.5-guru.50` / `active`；`.49` 为 immutable superseded predecessor。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`。
- change path：`target_native`；promotion state：`reviewed_promoted`；ADR required：`true`；
  ADR locator：`docs/architecture/adr/009-issue-reference-closure-ownership.md`。

本 contribution 只定义 current ledger authority 的局部收敛，不恢复 #305 target 大重构，
不迁移旧 task，不改变 Skill id、owner、typed route 或四阶段顺序。

## Boundary And Decision

before：current Workspace、Planning/qualification、Commit/Review、Publication/Finalizer/Merge、
Finish/Restore 及 installed validation仍通过 task-local ledger 或其 Issue arrays交换跨阶段 authority。
`ARCH-INT-016` 也把 issue ledger列入 current task resolution。

after candidate：ledger writer、reader、schema registration、aggregate DTO 与 ledger-only assets全部退出
current graph。task identity来自 official task/Git/worktree/mapping；requirement/source reference由 current
authority拥有；PR reference/closure decision由 Publication 唯一 fresh判断，Issue-backed completed默认关闭；
Finalizer只绑定发布事务，Merge不重判关闭决定，GitHub通过进入默认分支的closing keyword自动执行关闭，
Merge再以live facts验证结果。
legacy ledger path不进入 managed inventory，preset/update不主动触碰，active runtime不打开；旧 task无迁移。

选择 `target_native`，因为本变更有意改变 closure-intent authority、默认关闭规则、非默认分支效果和
public DTO compatibility boundary，并直接删除旧 ledger 路径。它不是 `dedicated_refactor_slice`，因为
该路径要求行为/API/规则不变；也不是 `legacy_boundary_convergence`，因为没有 remaining compatibility
layer、reader 或退出期。该 target-native decision 仍局限于 #247，不恢复 #305 architecture rewrite。

## Required Concerns

| Concern | Applicability | #247 candidate contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | 绑定 Architecture 2.0、active `.49`、Issue #247 r19、RDT candidate与project contract v1。 |
| `constitution-binding` | `applicable` | 命中概念完整、职责隔离、最小复杂度、技术债单向收敛；constitution identity不变。 |
| `boundary-and-decision` | `applicable` | `target_native` 建立 reference、closure intent、GitHub action 与 live result 的独立 owner boundary。 |
| `owner-and-single-writer` | `applicable` | 各semantic owner单写自己的current result；task只写delivery/contributions；serialized owner单写shared current。 |
| `compatibility-and-exit` | `applicable` | current consumer同步迁移并删除旧资产；无旧task migration、adapter、fallback、dual-read/write。 |
| `gap-and-deviation` | `applicable` | accepted `ADR-009` 与 closed `ARCH-GAP-008` 承接 ledger authority debt 的关闭；不重开其它 closed GAP，不新增 owner、router 或替代 aggregate。 |
| `parallel-scope` | `applicable` | #247只写自己的worktree与contributions；promotion前不修改`.49` shared current或其它task。 |
| `evidence-and-freshness` | `applicable` | active-zero inventory、三路closure、legacy inert、package/eval/install/platform与full diff各绑定current candidate。 |
| `review-and-promotion` | `applicable` | contribution 与 `ADR-009` 已接受 independent committed review；serialized promotion 绑定 expected `.49` 并建立 `.50`，其 diff 重新过 gate。 |

## Owners And Single Writers

- task/workspace identity：official Trellis task metadata、live Git/worktree 与 ignored mappings。
- requirement/scope/source reference：Phase 0与Planning semantic owners。
- PR payload/closure decision：Publication semantic owner；Issue-backed completed默认关闭，remain-open必须有current-authority原因。
- publication transaction：Finalizer owner只绑定并执行已审查PR payload。
- merge execution：Merge semantic owner负责readiness、expected-head与本次确认，不重判关闭决定。
- Issue closure action/result：GitHub closing-keyword自动行为执行；Merge以live GitHub facts验证。
- task completion/recovery/cleanup：各现有 Finish/Restore/Cleanup owner。
- task writer：`247-remove-issue-scope-ledger` worktree。
- shared current writer：serialized Architecture/RDT promotion owners。

跨 owner只传唯一 consumer所需的最小 typed projection，不传 Issue classification aggregate。

## Project Check Contract And Stage Results

- descriptor：`guru-trellis-architecture-convergence:repository:1` /
  `guru-trellis-architecture-convergence@1`。
- refs：`ARCH-GOV-006..009`、`ADR-005`、`ADR-009`、`ARCH-GAP-006`、`ARCH-GAP-008`。
- Planning evidence：live Issue #247 r19、task planning、active `.49` Architecture/RDT、fresh
  ledger consumer inventory、#247 RDT candidate与本 contribution。
- Revised Planning result（2026-09-13）：`pass / blocking=true`；Architecture typed exit 为
  `baseline_current`。方案只有一个 target-native direct-deletion path、现有 owner与一个
  serialized promotion writer；无 compatibility layer、old-task migration、替代 aggregate、owner expansion
  或新增/恶化 deviation；Planning 当时的 `ADR-009-CANDIDATE` 完整承接 closure authority、GAP
  lifecycle 与 compatibility exit，现已随 `.50` promotion 成为 accepted `ADR-009`。

Phase 2与Branch Review必须分别基于完整 current candidate和exact committed range执行；Planning
re-entry后的 fresh Phase 2 已完成，但仍不替代提交后的 independent Branch Review。

Fresh Phase 2 result（2026-09-13）：Architecture 官方 invoke 返回
`baseline_current / architecture_impact / target_native / reviewed_candidate`，`ADR required=true`；九项
required concerns和 blocking project check均为pass。normal-scenario与solution-mechanism qualifier均将
`issue247-target-native-ledger-retirement`判定为`qualified_current`，`guru-check-task`返回`passed`：

- before 的 ledger跨 owner aggregate、writer/reader/schema/DTO/compatibility path已从 current active graph退出；
  未新增替代 aggregate、dual-read/write、migration或第二 authority owner。
- Publication唯一 fresh判断 Issue reference/closure intent；Finalizer只绑定该 payload；Merge读取live PR
  body、执行expected-head merge并验证 GitHub closing-keyword效果，不调用 Issue-close API或重判关闭意图。
- 本次相关 package/runtime/integration 共 `392` tests通过；active ledger writer、reader、precondition、
  schema registration与aggregate DTO consumer为零，upstream ownership与dogfood overlay drift均为
  `status=ok`，canonical/installed/platform projection保持一致。
- 此前完整 preset Python suite `203 tests / OK (skipped=1)`、parallel finish `2/2`、installed closeout
  `3/3` 与routing `42/42`仍是同一实现候选的较早完整回归事实，但不是本次fresh Phase 2的唯一gate，
  也不替代新的Architecture、qualification、freshness checker或public wrapper结果。
- code subtraction与Docs SSOT subtraction均通过：增长仅来自 current behavior测试、managed projection和
  task-owned RDT/Architecture contribution；不存在为 ledger兼容保留的 production/test/schema/docs资产。

Fresh Phase 2 Architecture route：`baseline_current`；impact kind：`architecture_impact`；change path：
`target_native`；promotion state：`reviewed_candidate`；ADR required：`true`。完整多平台 exact-candidate
Release matrix、tag、GitHub Release和生产业务仓验证不属于本 project check，保持明确 deferred。

## Review And Promotion Boundary

- Phase 2 review：`passed`；已绑定2026-09-13完整current candidate与fresh Architecture/task-check结果。
- independent Branch Review：`passed`；绑定 exact range
  `origin/main@ec016827fac81d33faeacb307b0db76d5259dc28...9c3c00908446ac0fa86974cb9886f37917ac40ca`。
- promotion：`reviewed_promoted`；expected input `current-main-0.6.5-guru.49`，current successor
  `current-main-0.6.5-guru.50`。
- ADR：`required=true`；accepted `ADR-009` 记录 closure authority、GitHub action/result 和无兼容退出的长期 decision。
- promotion-created diff 必须重新进入 fresh Phase 2、Task Commit 与 independent Branch Review，之后才可由
  Publication/Acceptance消费 current `.50`。
- live current advance、scope/owner扩张、兼容机制、project-check failure或stale contribution必须返回对应owner。

## Explicit Boundaries

- 不迁移、解析、转换或保证旧 task/DTO/schema/invocation继续运行。
- 不删除或回写历史 archive、ADR、superseded/released RDT与release evidence。
- 不新增 public Skill、graph router、authority graph、shared cache/journal或第二 task context。
- 不修改 Trellis upstream、global npm、`node_modules`、业务仓库、tag、GitHub Release或完整Release matrix。
