# Guru Trellis Current Capability Inventory

版本：`current-main-0.6.5-guru.40-to-evolution-draft-2026-08-24`；状态：
`requirements_trace_draft`。

本文件是 Evolution Requirements 的 current-to-target 能力保留与差集台账。它回答“当前
已经具备哪些可观察能力、目标版本如何承接、哪些只是旧合同形态、哪些是本轮新增目标”，
不定义 target 行为，也不取代任何 current authority。

## 1. Authority 与一致性关系

- 上一版本 [`Current Capability Inventory`](../../design/versions/current-main-0.6.5-guru.40/capability-inventory.md)
  继续是 `.40` current Design SSOT，拥有 active Skill/interface/external-exit inventory 及其
  source identity。本文件逐项建立 successor/classification，不复制 interface 或 exit 正文。
- current 产品能力与非功能边界以
  [`current-main-0.6.5-guru.40/requirement-main.md`](../versions/current-main-0.6.5-guru.40/requirement-main.md)、
  [`requirement-non-functional.md`](../versions/current-main-0.6.5-guru.40/requirement-non-functional.md)
  和 [`decisions.md`](../versions/current-main-0.6.5-guru.40/decisions.md) 为 authority。
- current 实现责任与验收证据分别由 `.40`
  [`design-main.md`](../../design/versions/current-main-0.6.5-guru.40/design-main.md)、
  [`traceability.md`](../../design/versions/current-main-0.6.5-guru.40/traceability.md)、
  [`test-strategy.md`](../../test/versions/current-main-0.6.5-guru.40/test-strategy.md) 和
  [`Test Traceability`](../../test/versions/current-main-0.6.5-guru.40/traceability.md) 证明。
- current Architecture 能力由 [`Architecture Baseline`](../../architecture/README.md)、
  current design constitution 与 project change contract 证明；canonical registry/interfaces
  只补充 `code_recovered` 的 active package/route 事实。
- target 行为的唯一主定义仍是 [`requirement-main.md`](./requirement-main.md) 中对应的
  `EVO-REQ-*` 和 [`requirement-non-functional.md`](./requirement-non-functional.md) 中对应的
  `EVO-NFR-*`。本文件中的摘要不得被实现或 Design 当作并行主定义。

`.40` inventory 当前记录 21 个 active Skill 与 89 个 external exit。这些数量、Skill id、
schema/exit shape 和文件布局仅用于核对 current source coverage，不是 target API、验收常量或
必须保留的拆分。

## 2. Classification

| Classification | 含义 |
| --- | --- |
| `preserved_current` | current 可观察结果与正常场景必须在 target 保持，允许内部 owner 或合同形态变化 |
| `replaced_contract_shape` | 能力结果必须保留，但 current Skill/schema/exit/handoff/文件拆分明确由单一新合同替换 |
| `new_target` | 本轮新增或显著加强的目标；不得冒充 `.40` 已有能力 |
| `intentionally_not_retained` | 经产品决定不保留的旧合同、冗余过程或实现形态；不得作为 capability loss 阻塞迁移 |

一项能力可以同时是 `preserved_current + replaced_contract_shape`：前者约束用户结果，后者
明确旧 API/owner/handoff 不具有兼容权利。

## 3. Current 可观察能力总表

| Stable capability id | Current 可观察能力 | Classification | Current authority / evidence | 上一版 inventory 对应 | Target successor | Acceptance fixtures | 保留与 loss 边界 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CUR-CAP-001` | 通过官方 Trellis workflow/spec marketplace、Markdown workflow、Skill、preset/overlay 和 deterministic companion runtime 扩展，不修改上游源码或 npm 安装 | `preserved_current + replaced_contract_shape` | `REQ-002,006,013`; `BEH-009`; `NFR-001` | Registry/package/platform closure | `EVO-REQ-051..055` | `EVO-FIX-PROJECTION`, `EVO-FIX-MIGRATION` | 保留官方扩展面与 canonical source；不保留 current package/API layout |
| `CUR-CAP-002` | global workflow 与 step-local semantic owner 分层，AI 判断与 deterministic executor/validator 分层，typed route 未映射时 fail closed | `preserved_current + replaced_contract_shape` | `REQ-003..004,008`; `NFR-002..003`; `CASE-001..002` | 全部 active interfaces 的 consumer closure | `EVO-REQ-010,024..025,034,051`; `EVO-NFR-007,014..015` | `EVO-FIX-TASK-FREE`, `EVO-FIX-FRESH-SCOPE`, `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-RDT-LIFECYCLE` | 保留唯一 semantic owner、唯一 consumer/stop 与脚本边界；不保留 current Skill/exit/schema id |
| `CUR-CAP-003` | 标准请求完成 mode selection、current change context、需求澄清、duplicate/prerequisite/scope readiness，再进入资源准备 | `preserved_current + replaced_contract_shape` | `REQ-001,005,012,044..045`; `BEH-001,006`; `SCN-001,004` | `guru-select-workflow-mode`, `guru-discover-change-context`, `guru-clarify-requirements`, `guru-review-change-request` | `EVO-REQ-002..010,059` | `EVO-FIX-INTAKE-CLEAR`, `EVO-FIX-INTAKE-REVIEWED-DESIGN`, `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-CHANGE-REQUEST` | 保留 clear/unclear/duplicate/prerequisite/recovery 结果；不保留 current Phase 0 顺序、aggregate 或 private result |
| `CUR-CAP-004` | selected base 按明确 precedence 绑定 exact authority checkout；detached invocation 可读取/同步 authority，unsafe/ambiguous/dirty/mismatch fail closed | `preserved_current + replaced_contract_shape` | `REQ-036..045`; `SCN-034..040`; `TST-027..030` | `guru-sync-base`, `guru-discover-change-context` | `EVO-REQ-009,060`; `EVO-NFR-010` | `EVO-FIX-DETACHED-READ`, `EVO-FIX-BASE-REFRESH` | 保留 selection/binding/safe refresh 与 downstream freshness；不保留 Sync/Discovery producer-private payload |
| `CUR-CAP-005` | requirement 信息不足时交互澄清，明确 contract wording 与 change readiness 可执行有界 semantic review | `preserved_current + replaced_contract_shape` | `REQ-001,003..005`; `BEH-001`; canonical active interfaces | `guru-clarify-requirements`, `guru-review-contract-wording`, `guru-review-change-request` | `EVO-REQ-003..008,057,059` | `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-CHANGE-REQUEST` | 保留交互式澄清和显式 specialist review；wording review 不再是 normal Planning mandatory gate |
| `CUR-CAP-006` | 在精确副作用确认后创建或复用语义命名的 task/worktree/branch，并隔离并行资源 | `preserved_current + replaced_contract_shape` | `REQ-005,011..012,020,042`; `BEH-001`; `SCN-001,007` | `guru-create-task-workspace` | `EVO-REQ-011,033,059`; `EVO-NFR-011,017` | `EVO-FIX-NO-ISSUE`, `EVO-FIX-PARALLEL`, `EVO-FIX-FULL-NORMAL` | 保留精确确认、identity、复用与隔离；不保留 preparation/task creation 的 current coupling |
| `CUR-CAP-007` | 标准 task 形成 `prd.md`、`design.md`、`implement.md`，可交互澄清并接受一次完整 semantic plan approval | `preserved_current + replaced_contract_shape` | `BEH-002`; `SCN-002`; current workflow 与 planning package | `guru-clarify-requirements`, `guru-approve-task-plan`，以及 upstream planning authoring | `EVO-REQ-012..026,064` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-FRESH-EQUIVALENT`, `EVO-FIX-FRESH-SCOPE`, `EVO-FIX-TECH-REVISION`, `EVO-FIX-RDT-LIFECYCLE` | 保留 task planning 的 current intent/delta、finding/revision 和一次 approval；authoring 改为 Guru-owned RDT-first 单闭环，三份 task 文件降为 repository RDT 的引用/projection/contribution mapping，不保留 upstream `trellis-brainstorm`、wrapper author 或 task-planning-as-project-authority |
| `CUR-CAP-008` | caller 明确需要时，可独立审核 contract wording 或判断受支持 normal scenario | `preserved_current + replaced_contract_shape` | canonical active interfaces；current package semantic contracts | `guru-review-contract-wording`, `guru-qualify-normal-scenario` | `EVO-REQ-023,057..058` | `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-QUALIFY-EXPLICIT` | 保留 standalone specialist 能力；普通直接派生验收不例行调用，也不产生第二 planning owner |
| `CUR-CAP-009` | 标准 task 在全生命周期消费 Architecture Baseline/constitution/change contract，区分 no-impact、change path、conflict、contribution/ADR、fitness、freshness 与 serialized promotion | `preserved_current + replaced_contract_shape` | `REQ-027..035`; `BEH-007`; `TST-018..026`; Architecture 2.0 authority | `guru-maintain-architecture-baseline` | `EVO-REQ-013..020,026..031,033,035,040,061,063`; `EVO-NFR-011,015` | `EVO-FIX-ARCH-NO-IMPACT`, `EVO-FIX-ARCH-ALIGNED`, `EVO-FIX-ARCH-CONFLICT`, `EVO-FIX-ARCH-INCOMPLETE`, `EVO-FIX-ARCH-NEW-DECISION`, `EVO-FIX-ARCH-REVISION`, `EVO-FIX-ARCH-NO-ADR`, `EVO-FIX-FRESH-EQUIVALENT`, `EVO-FIX-FRESH-SCOPE`, `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-PARALLEL` | 保留 Architecture 方法论、从 Planning 到 Publication/Acceptance/Finish 的 current binding、task-local contribution 与 shared-current promotion；不保留 2.0 profile/schema/exit shape |
| `CUR-CAP-010` | 有界 task-free change 可在 current checkout 执行、检查、恢复或升级为标准 route | `preserved_current + replaced_contract_shape` | canonical `guru-execute-task-free-change` interface；current mode/ownership requirements | `guru-select-workflow-mode`, `guru-execute-task-free-change` | `EVO-REQ-010,034,051`; `EVO-NFR-007,009..010` | `EVO-FIX-TASK-FREE` | 保留有界执行、适用 check、scope evolution 与 concise terminal result；不生成 standard planning/archive 只是 target 收窄，不声称 current 已完全满足 |
| `CUR-CAP-011` | Implementation 消费 approved scope，Phase 2 对 task scope/实现/测试/文档/Architecture 完成 semantic finding loop，并执行 scope-relevant 最小可靠验证 | `preserved_current + replaced_contract_shape` | `REQ-003..004,032`; `BEH-003`; `NFR-004`; `TST-003..004,018` | `guru-check-task` | `EVO-REQ-027..029,065`; `EVO-NFR-014..015` | `EVO-FIX-FULL-NORMAL`, `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS` | 保留完整 semantic check 与 targeted validation ownership；新增 current RDT binding/contribution 的下游消费和中间回写，不保留 aggregate/handoff/private checkpoint |
| `CUR-CAP-012` | 精确 staging/commit，base movement impact reconciliation，exact committed full-diff independent Branch Review 与 finding closure | `preserved_current + replaced_contract_shape` | `REQ-005,012,032`; `BEH-004,006`; `SCN-002,004` | `guru-create-task-commit`, `guru-reconcile-task-base`, `guru-review-branch` | `EVO-REQ-029..034` | `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-BASE-EVOLUTION`, `EVO-FIX-FULL-NORMAL` | 保留 commit identity、fresh review 与最早受影响点 re-entry；不保留 current wrapper/transition shape |
| `CUR-CAP-013` | 从 current plan、committed diff、验证与 live GitHub facts 判断 publication readiness，并支持 `github_pr`/`none` 与 provider recovery | `preserved_current + replaced_contract_shape` | `REQ-009,012,020`; `BEH-005..006`; `TST-008,011,017` | `guru-review-task-publication`, `guru-finalize-task` 的 provider route | `EVO-REQ-035..041` | `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-PROVIDER-RECOVERY` | 保留 PR truthfulness、expected-head、两种 provider 与 forward recovery；不保留 Issue Scope Ledger/close-related-followup aggregate |
| `CUR-CAP-014` | Acceptance、Finalize、Merge、Issue closure 与 terminal projection 使用 exact task/head/archive/live provider facts，stale/mismatch fail closed | `preserved_current + replaced_contract_shape` | `REQ-011,014,020`; `BEH-005,008,010`; `TST-010,012,017` | `guru-finalize-task`, `guru-merge-task-pr` | `EVO-REQ-038,040..043`; `EVO-NFR-009..010` | `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-HISTORY-RESUME` | 保留 terminal correctness、merge/closure verification 和 forward recovery；不保留 placeholder/retired-locator/current owner 切法 |
| `CUR-CAP-015` | task index/archive/finish-summary 可查询；Finish/cleanup 只处理 exact owned resource 并保护 retained ref/history | `preserved_current + replaced_contract_shape` | `REQ-005,011..012,014,020`; `BEH-006,008,010`; `TST-009..012` | `guru-finalize-task`, `guru-merge-task-pr` 及 task history runtime | `EVO-REQ-039..043,046..047`; `EVO-NFR-009..011` | `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-LATEST-INTENT`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE` | 保留可发现历史、partial recovery、owned cleanup、latest-intent continuation 与 reachability；不保留 workspace journal、完整 stdout、授权或长摘要 |
| `CUR-CAP-016` | Requirements/Design/Test 与 Architecture 各有 shared current SSOT；新/残缺仓库可 bootstrap/repair，task 通过 isolated contribution 与 reviewed serialized promotion 演进 | `preserved_current + replaced_contract_shape` | `REQ-007,019,027..035`; `BEH-007`; `TST-006,016,018..024` | `guru-maintain-requirements-design-test-ssot`, `guru-maintain-architecture-baseline`, `guru-bootstrap-repository-ssot` | `EVO-REQ-018..020,031,033,061..065`; `EVO-NFR-011,015` | `EVO-FIX-SSOT-BOOTSTRAP`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-PARALLEL` | 保留唯一 shared current、traceability、bootstrap/repair、contribution/promotion；target 将 RDT 提升为所有 standard task 的前置与下游 current authority，task planning 不再是平行 SSOT；不保留 current profile/public DTO/recorder layout |
| `CUR-CAP-017` | canonical/dogfood/installed/Shared/Codex/Claude/Cursor、preset managed assets、mode、sidecar 与 official install/update/upgrade 可做一致性验证 | `preserved_current + replaced_contract_shape` | `REQ-002,006,013,016..019,035,043,046`; `BEH-009,011`; `TST-005,014..016,025..030` | 全 registry packages；`guru-verify-extension-installation` 为 standalone owner | `EVO-REQ-051..056`; `EVO-NFR-012..015` | `EVO-FIX-PROJECTION`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE` | 保留跨平台/安装/升级 capability equality；target 只投影新合同，不保留旧 route/schema/artifact consumer |
| `CUR-CAP-018` | verifier 从 live registry/interfaces 派生 active package/command/complete capability inventory，不依赖固定 magic count | `preserved_current + replaced_contract_shape` | `REQ-015,018`; `TST-013,015`; `SCN-010,013` | `.40` inventory 全 21 active Skill/89 exits | `EVO-REQ-053,055..056`; `EVO-NFR-012` | `EVO-FIX-PROJECTION`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE` | 保留 live derivation 和 before/after loss detection；21/89 只作为 `.40` source identity |
| `CUR-CAP-019` | static/package/semantic/integration/distribution/live/release evidence 分层；普通 change 只运行 accepted scope 所需最小可靠集合，专项 owner 才声明完整矩阵或 Release | `preserved_current` | `REQ-009`; `NFR-004..005`; `TST-001..009` 与 Test “选择规则” | inventory 的 #260/#283 boundary 说明 | `EVO-REQ-028,035,051,056`; `EVO-NFR-010,014,016` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-RELEASE` | 保留 proof boundary、SKIP/unverified honesty 与最小 validation ownership；流程精简不得把它删除 |
| `CUR-CAP-020` | 两个正常并行 task 的 workspace/provider/archive/Finish/cleanup 隔离，`github_pr` 与 `none` 都可完成，shared current 单写 | `preserved_current + replaced_contract_shape` | `REQ-020,034`; `BEH-011`; `TST-009,017,024`; `SCN-007,015..016,030` | delivery、finalize、merge、SSOT packages 的组合能力 | `EVO-REQ-033,037..043`; `EVO-NFR-011` | `EVO-FIX-PARALLEL`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE` | 保留隔离、两种 provider、merge order/recovery/reachability；不保留 current metadata/handoff 切分 |

## 4. 上一版 active Skill coverage index

本表是与 `.40` Design inventory 的逐行一致性检查。每个 previous Skill 都至少映射到一个
`CUR-CAP-*`；target 是否继续使用同名 Skill 由后续 Design 决定。

| Previous `.40` Skill id | Current capability successor | Target requirement successor | 结论 |
| --- | --- | --- | --- |
| `guru-select-workflow-mode` | `CUR-CAP-003,010` | `EVO-REQ-010` | 可观察 mode/task-free 分流保留，Skill id/exit 可替换 |
| `guru-sync-base` | `CUR-CAP-004` | `EVO-REQ-009,060` | exact base authority 能力保留，private result shape 不保留 |
| `guru-discover-change-context` | `CUR-CAP-003,004` | `EVO-REQ-002,059..060` | fresh context 能力保留，不允许 consumer 读取 producer-private result |
| `guru-clarify-requirements` | `CUR-CAP-003,005,007` | `EVO-REQ-002..008,012` | 逐问澄清和 requirement readiness 保留，normal authoring owner 重构 |
| `guru-review-contract-wording` | `CUR-CAP-005,008` | `EVO-REQ-025,057` | 显式 specialist 能力保留，normal Planning 调用为 0 |
| `guru-review-change-request` | `CUR-CAP-003,005` | `EVO-REQ-059` | duplicate/prerequisite/independent-unit readiness 保留且不重复 authoring |
| `guru-create-task-workspace` | `CUR-CAP-006` | `EVO-REQ-011,059` | exact resource preparation 保留，owner coupling 可替换 |
| `guru-approve-task-plan` | `CUR-CAP-007` | `EVO-REQ-024..026` | 一次完整 planning approval 保留 |
| `guru-qualify-normal-scenario` | `CUR-CAP-008` | `EVO-REQ-023,058` | 仅 explicit current caller 需要时保留 |
| `guru-execute-task-free-change` | `CUR-CAP-010` | `EVO-REQ-010,034,051` | 有界 task-free 闭环保留并收窄长期 artifact；不借用 standard approved-plan/Phase 2 合同 |
| `guru-check-task` | `CUR-CAP-011` | `EVO-REQ-027..029` | Phase 2 semantic finding loop 保留 |
| `guru-create-task-commit` | `CUR-CAP-012` | `EVO-REQ-029..031` | exact commit 与 fresh candidate binding 保留 |
| `guru-reconcile-task-base` | `CUR-CAP-012,015` | `EVO-REQ-026,032` | base evolution impact/recovery 保留，不重建 task |
| `guru-review-branch` | `CUR-CAP-012` | `EVO-REQ-029..031` | committed full-diff independent review 保留 |
| `guru-review-task-publication` | `CUR-CAP-013` | `EVO-REQ-035..036` | truthful publication readiness 保留 |
| `guru-finalize-task` | `CUR-CAP-013..015,020` | `EVO-REQ-037..043` | provider/finalization/history/terminal 结果保留，owner/placeholder shape 可替换 |
| `guru-merge-task-pr` | `CUR-CAP-014,020` | `EVO-REQ-037,040..042` | expected-head merge 与 closure verification 保留 |
| `guru-verify-extension-installation` | `CUR-CAP-017..019` | `EVO-REQ-052..056` | standalone installation/capability verification 保留，target inventory live-derived |
| `guru-maintain-requirements-design-test-ssot` | `CUR-CAP-016` | `EVO-REQ-061..062` | RDT shared-current lifecycle 保留 |
| `guru-maintain-architecture-baseline` | `CUR-CAP-009,016` | `EVO-REQ-013..020,026..031,033,035,040,061,063` | Architecture lifecycle 与 downstream current binding 保留，2.0 API shape 不保留 |
| `guru-bootstrap-repository-ssot` | `CUR-CAP-016` | `EVO-REQ-061` | new/partial/stale/conflicting authority bootstrap/repair 保留 |

差集结论：上一版 Design inventory 的 21 个 active Skill 均有 successor，孤儿项为 0。该结论
只证明 Requirements coverage，不证明 target Design 已完成或 target runtime 已实现。

## 5. Current authority coverage closure

| Current authority set | Inventory coverage | 结论 |
| --- | --- | --- |
| `REQ-001..020` | `CUR-CAP-001..003,005..008,011..020` | 全部有 successor |
| `REQ-027..035` | `CUR-CAP-009,011..012,016,020` | 全部有 successor |
| `REQ-036..046` | `CUR-CAP-003..004,017` | 全部有 successor |
| `BEH-001..011` | `CUR-CAP-001..017,020` | 全部有 successor |
| `NFR-001..005` | `CUR-CAP-001..004,011,017..019` | 全部有 successor |
| `.40 TST-001..030`, `SCN-001..016,024..040`, `CASE-001..002` | 各行 current evidence 与 target fixtures | 无 current test capability 被静默删除；具体 target test design 尚未开始 |

`.40` Requirements 未定义 `REQ-021..026`，编号从 `REQ-020` 跳到 `REQ-027` 是 current
authority 的既有事实，不是本 inventory 的 coverage 缺口。

## 6. New target deltas

以下结果不能写成 `preserved_current`，也不能用 `.40` inventory 证明已存在。`Target core capability`
只记录该 delta 主要服务的顶层产品难点，不替代 `EVO-REQ-*` 与 fixture 的验收主定义：

| Delta id | New target | Target core capability | Target authority | Acceptance |
| --- | --- | --- | --- | --- |
| `TARGET-DELTA-001` | Guru-owned 单一 authoring 闭环完全替代 upstream `trellis-brainstorm`，并保留逐个最高价值问题的交互式澄清 | `EVO-CAP-001,EVO-CAP-002` | `EVO-REQ-004,012,024..025` | `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-PLAN-NORMAL` |
| `TARGET-DELTA-002` | `design.md` 首次实质写作前实际消费 current baseline、constitution、change contract，并 reconciliation Issue 中已审阅设计 | `EVO-CAP-003` | `EVO-REQ-013,015..017,021..022` | `EVO-FIX-INTAKE-REVIEWED-DESIGN`, `EVO-FIX-ARCH-ALIGNED`, `EVO-FIX-ARCH-CONFLICT` |
| `TARGET-DELTA-003` | normal Planning 去掉 mandatory wording/qualification wrapper，只保留一次 authoring 和一次 approval | `EVO-CAP-001,EVO-CAP-004` | `EVO-REQ-023..025,057..058` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-QUALIFY-EXPLICIT` |
| `TARGET-DELTA-004` | normal workflow 消除无 consumer 交接、重复 unchanged 正文/累计输出注入、不必要脚本/gate/验证和内部过程噪声，并在阶段后卸载无用 private evidence；不设置相对性能数值门槛 | `EVO-CAP-004` | `EVO-REQ-044..050`; `EVO-NFR-001..008` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-LONG-OUTPUT` |
| `TARGET-DELTA-005` | wait/compression/resume 后按到达顺序优先消费最新 override/additive 用户意图 | `EVO-CAP-001,EVO-CAP-004` | `EVO-REQ-046..048`; `EVO-NFR-009` | `EVO-FIX-LATEST-INTENT`, `EVO-FIX-HISTORY-RESUME` |
| `TARGET-DELTA-006` | task-free route 不生成正式 planning、task/archive history 或 standard cleanup resource | `EVO-CAP-001,EVO-CAP-004` | `EVO-REQ-010` | `EVO-FIX-TASK-FREE` |
| `TARGET-DELTA-007` | 最终 candidate 只含新合同；existing repository 通过一次迁移进入新路径，不提供旧合同 fallback | `EVO-CAP-001..004` | `EVO-REQ-052..056`; `EVO-NFR-012..015` | `EVO-FIX-PROJECTION`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE` |
| `TARGET-DELTA-008` | repository RDT 成为 standard task 的上位文档中心：Planning 前置回读/impact，task 三件套只承载引用与 task-local delta/contribution mapping，实施与审查持续回写并验证 current RDT lifecycle | `EVO-CAP-002` | `EVO-REQ-002,012,021,024,027..030,035,061..065` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`, `EVO-FIX-FULL-NORMAL` |
| `TARGET-DELTA-009` | parent repository task 默认完全排除 Git submodule 的 authority、RDT、代码、状态、副作用与验证；显式 submodule change 进入独立 repository workflow | `EVO-CAP-001,EVO-CAP-002` | `EVO-REQ-002,010..011,061,066`; `EVO-NFR-018` | `EVO-FIX-SUBMODULE-BOUNDARY`, `EVO-FIX-FULL-NORMAL` |

## 7. Intentionally not retained

| Removed shape/process | Current relation | 不保留理由 | 仍须证明的 successor |
| --- | --- | --- | --- |
| 21 active Skill、89 exits 及其具体 Skill/exit/schema id | `.40` inventory source identity | 固化数量会把 target 耦合 current graph | `CUR-CAP-001..020` 的 observable result 全量通过 |
| upstream `trellis-brainstorm` 作为 planning author | current workflow authoring mechanism | 用户已决定 Guru Team 完全替代 | `TARGET-DELTA-001..002` |
| task `prd.md`/`design.md`/`implement.md` 作为 repository Requirements/Design/Test 的替代或平行 authority | upstream/current task-centric planning model | 会允许 task planning 冒充或绕过 shared RDT，破坏项目长期文档中心与跨 task 连续性 | `TARGET-DELTA-008`：RDT-first 回读、task-local projection/contribution、serialized promotion 与 downstream freshness |
| parent task 默认递归处理 Git submodule | current/历史 repository discovery 与 validation 行为 | 无关 nested repository 状态会扩大 scope、制造副作用和阻塞，且不能成为 parent RDT/code authority | `TARGET-DELTA-009`：默认排除；显式 submodule change 使用独立 repository workflow |
| Issue Scope Ledger 与 `close_issues/related_issues/followup_issues` aggregate | current/历史 closeout shape | shared aggregate 不是 live closure authority | `CUR-CAP-013..015` 从 current Issue/diff/live provider 形成真实结果 |
| normal-path mandatory wording review / normal-scenario qualification | current specialist Skill 可用 | 重复 semantic owner、增加正常路径成本 | specialist standalone 保留，normal 调用为 0 |
| producer-private result、digest、完整 scan/stdout、授权、长篇 handoff summary、无 consumer gate artifact | current runtime/process shape | 可重建或无直接 consumer，扩大上下文并制造耦合 | 最小 public result、必要 private evidence 生命周期与 durable history |
| Architecture 2.0 的具体 profile/schema/exit id | current public contract shape | 保留方法论，不保留旧 API | `CUR-CAP-009,016` 的全生命周期 Architecture 结果 |
| 每个普通 change 都执行完整平台/Release matrix | 从来不是 current ownership 要求 | 会违背最小可靠验证 ownership | `CUR-CAP-019`：普通 scope-targeted，专项 owner 执行 exact matrix |
| legacy route、dual-read/write、wrapper、fallback 或只为旧 artifact 存活的 adapter | target migration 候选 | 用户明确要求只保留新合同 | existing migration 后全投影只含新合同 |

## 8. Inventory completion contract

进入 Evolution Design 前，本 inventory 必须满足：

1. `.40` Design capability inventory 的每个 active Skill 都有且只有明确的 current capability
   successor/classification；当前差集为 0。
2. `.40` `REQ-*`、`BEH-*`、`NFR-*` 与具有产品意义的 Test capability 不得出现未分类孤儿；
   当前差集为 0。
3. 每个 `preserved_current` / `replaced_contract_shape` 项都能到达 target `EVO-REQ-*` 与至少
   一个 acceptance fixture；无法到达时必须补需求或显式改为 `intentionally_not_retained`。
4. `new_target` 不得引用 `.40` PASS 冒充已实现；只能在 target Design/Test 建立 successor
   evidence 后成为 candidate capability。
5. Design 若改变本表的 capability 边界或发现 current omission，必须先回到 Requirements
   修订本 inventory 和对应 target requirement，不能在 Design 中静默补能力。
6. `EVO-CAP-001..004` 每项至少有一个 `TARGET-DELTA-*` 归属和一个可达 acceptance fixture；
   当前四项均已覆盖，Design 必须逐项承接，不能再把 RDT lifecycle 吞并回泛化 authority continuity。
