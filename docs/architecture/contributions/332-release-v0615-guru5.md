# #332 Release current-fact alignment Architecture contribution

## Identity And Authority Boundary

- candidate identity：`architecture-contribution-332-release-v0615-guru5-v1`。
- source authority：live Issue #332 与 task `prd.md`。
- planning/behavior authority：task `design.md`、稳定 `implement.md` 与 RDT contribution。
- source/expected current：`docs/architecture/README.md` /
  `current-main-0.6.5-guru.43` / `active`。
- candidate successor：`current-main-0.6.5-guru.44`。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`。
- change path：`target_native`；ADR required：`false`。

本 contribution 只定义 `.43 -> .44` 的 release/current fact alignment 候选。它不记录 task
HEAD、执行阶段、Gate 结果、finding closure、tag、smoke、Release、时间或用户授权，也不自行
声明 review、promotion 或 current 状态。

## Boundary And Decision

当前 `.43` Architecture/RDT authority 仍将 current release facts 指向历史
`v0.6.15-guru.3`、`0.6.15-guru.39` 与 #267，而 #332 的 accepted current target 已固定为
`v0.6.15-guru.5`、`0.6.15-guru.40`、Trellis CLI `0.6.15`。这造成 current authority 与
committed release-facing source 的事实冲突，阻断当前 task 进入 Publication。

目标边界建立 successor `.44`，把适用的 current release facts、navigation、history、
traceability 与 evidence 对齐到 #332，同时保留 `.43`、旧 release、旧 tag、#267 与历史
evidence 的原始事实。它不改变 runtime、公共 API、owner topology、single-writer、GAP
lifecycle、compatibility exit 或已合入 #311/#333/#339/#358/#361 的实现，因此不创建 ADR。

## Required Concerns

| Concern | Applicability | #332 contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | 绑定 Architecture 2.0、active `.43`、Issue #332 与 change contract v1 |
| `constitution-binding` | `applicable` | 绑定 current constitution identity；仅命中语义完整、变化隔离与单向收敛 |
| `boundary-and-decision` | `applicable` | `target_native` 只收敛 current release facts，不新增运行时路径 |
| `owner-and-single-writer` | `applicable` | task 写 contribution；serialized promotion owner 单写 shared current |
| `compatibility-and-exit` | `applicable` | 不建立 adapter、双读或新 legacy path，既有 exit 保持不变 |
| `gap-and-deviation` | `applicable` | 收敛 current-fact conflict，不关闭或改变既有 Architecture GAP |
| `parallel-scope` | `applicable` | contribution 阶段禁止 shared-current edit，promotion 绑定 expected `.43` |
| `evidence-and-freshness` | `applicable` | 绑定 live #332、`.43` authority、task contribution 与后续 exact ranges |
| `review-and-promotion` | `applicable` | contribution 先独立 Review，再由 expected-current promotion owner 串行提升 |

## Before And After

- before：active `.43` 仍声明 `.3/.39/#267` current release facts；task candidate 已是
  `.5/.40/#332`。
- after：successor `.44` 成为唯一 active authority，current release facts 与 #332 对齐；
  `.43` 作为 superseded history 保留。
- preserved：历史 tag/Release/authority 原始记录、运行时与公共合同、Architecture decision、
  owner/GAP/compatibility 与 Issue closure boundary。

## Project Check Contract

使用 `guru-trellis-architecture-convergence:repository:1` /
`guru-trellis-architecture-convergence@1`，绑定 `ARCH-GOV-006..008`、`ADR-005`、
`ARCH-GAP-006`。检查范围为 authority binding、release fact alignment、single-writer、
history preservation、RDT traceability 与 promotion freshness。实现和动态验证证据由
Phase 2、独立 committed full-diff Branch Review 及后续 promotion owner 即时读取；本文不保存
动态 Gate 结果。

## Explicit Boundaries

- 不发布 `v0.6.15-guru.5`，不创建、移动或删除 tag/GitHub Release。
- 不修改、关闭、归档或清理 #267、#311、#333、#339、#358、#361 或其他 Issue/task/worktree。
- 不修改 Trellis upstream、全局 npm、`node_modules`、业务仓库或完整 Release Gate 矩阵。
- 不把本 contribution 提升为 shared current；是否 promotion 由现有 Architecture/RDT owner
  绑定 expected `.43` 串行判断。
