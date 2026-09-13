# #247 Issue Scope Ledger retirement Architecture contribution

## Identity And Authority Boundary

- contribution identity：`architecture-contribution-247-remove-issue-scope-ledger-v1`。
- requirement authority：live Issue #247 `2026-09-13-r19`、task `prd.md` 与 #247 RDT contribution。
- behavior authority：task `design.md`、`implement.md` 与 #247 RDT contribution。
- current/expected baseline：`docs/architecture/README.md` /
  `current-main-0.6.5-guru.49` / `active`。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`。
- change path：`dedicated_refactor_slice`；promotion state：`reviewed_candidate`；ADR required：`false`。

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

选择 `dedicated_refactor_slice`，因为本变更保持业务 lifecycle 与 owner拓扑不变，只收敛一个跨 owner
legacy aggregate boundary。它不是 `legacy_boundary_convergence`：没有 remaining compatibility layer、
reader或退出期；也不是 `target_native` 新能力或 #305 architecture rewrite。

## Required Concerns

| Concern | Applicability | #247 candidate contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | 绑定 Architecture 2.0、active `.49`、Issue #247 r19、RDT candidate与project contract v1。 |
| `constitution-binding` | `applicable` | 命中概念完整、职责隔离、最小复杂度、技术债单向收敛；constitution identity不变。 |
| `boundary-and-decision` | `applicable` | dedicated slice移除ledger aggregate并保留现有owner-native lifecycle。 |
| `owner-and-single-writer` | `applicable` | 各semantic owner单写自己的current result；task只写delivery/contributions；serialized owner单写shared current。 |
| `compatibility-and-exit` | `applicable` | current consumer同步迁移并删除旧资产；无旧task migration、adapter、fallback、dual-read/write。 |
| `gap-and-deviation` | `applicable` | 关闭ledger跨owner authority debt；不重开closed GAP，不新增owner、router或替代aggregate。 |
| `parallel-scope` | `applicable` | #247只写自己的worktree与contributions；promotion前不修改`.49` shared current或其它task。 |
| `evidence-and-freshness` | `applicable` | active-zero inventory、三路closure、legacy inert、package/eval/install/platform与full diff各绑定current candidate。 |
| `review-and-promotion` | `applicable` | contribution随delivery接受independent committed review；serialized promotion绑定expected `.49`，其diff重新过gate。 |

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
- refs：`ARCH-GOV-006..008`、`ADR-005`、`ARCH-GAP-006`。
- Planning evidence：live Issue #247 r19、task planning、active `.49` Architecture/RDT、fresh
  ledger consumer inventory、#247 RDT candidate与本 contribution。
- Planning result：`pass / blocking=true`。方案只有一个 direct-deletion path、现有 owner与一个
  serialized promotion writer；无 compatibility layer、old-task migration、替代 aggregate、owner expansion
  或新增/恶化 deviation。

Phase 2与Branch Review必须分别基于完整 current candidate和exact committed range重新执行；本结果不替代。

Phase 2 result（2026-09-13）：`pass / blocking=true`。完整 current candidate 已重新检查 before/after：

- before 的 ledger跨 owner aggregate、writer/reader/schema/DTO/compatibility path已从 current active graph退出；
  未新增替代 aggregate、dual-read/write、migration或第二 authority owner。
- Publication唯一 fresh判断 Issue reference/closure intent；Finalizer只绑定该 payload；Merge读取live PR
  body、执行expected-head merge并验证 GitHub closing-keyword效果，不调用 Issue-close API或重判关闭意图。
- project check `guru-trellis-architecture-convergence:repository:1` 结果为 `pass`：`ARCH-GOV-006..008`、
  `ADR-005` 与 `ARCH-GAP-006` 的 owner、single-writer、compatibility exit和debt convergence均未回归。
- 证据包括完整 preset Python suite `203 tests / OK (skipped=1)`、parallel finish `2/2`、workspace
  invocation `1/1`、installed closeout `3/3`、routing `42/42`、live inventory `status=ok`，以及
  canonical reapply/source-installed/dogfood/sidecar/static hygiene通过。
- code subtraction与Docs SSOT subtraction均通过：增长仅来自 current behavior测试、managed projection和
  task-owned RDT/Architecture contribution；不存在为 ledger兼容保留的 production/test/schema/docs资产。

Phase 2 Architecture route：`baseline_current`；impact kind：`architecture_impact`；change path：
`dedicated_refactor_slice`；promotion state：`reviewed_candidate`；ADR required：`false`。完整多平台
exact-candidate Release matrix、tag、GitHub Release和生产业务仓验证不属于本 project check，保持明确 deferred。
Branch Review仍必须从未来 exact committed `origin/main...HEAD` 独立重算，不能复用本结果。

## Review And Promotion Boundary

- Phase 2 review：`reviewed_candidate`；完整未提交 worktree candidate已审查通过。
- independent Branch Review：`pending`；exact committed range尚未形成。
- expected current：`current-main-0.6.5-guru.49`。
- promotion：`required`，但本 contribution不授权 shared current write。
- ADR：`required=false`；本 task执行现有constitution的局部债务收敛，没有新增长期architecture decision。
- live current advance、scope/owner扩张、兼容机制、project-check failure或stale contribution必须返回对应owner。

## Explicit Boundaries

- 不迁移、解析、转换或保证旧 task/DTO/schema/invocation继续运行。
- 不删除或回写历史 archive、ADR、superseded/released RDT与release evidence。
- 不新增 public Skill、graph router、authority graph、shared cache/journal或第二 task context。
- 不修改 Trellis upstream、global npm、`node_modules`、业务仓库、tag、GitHub Release或完整Release matrix。
