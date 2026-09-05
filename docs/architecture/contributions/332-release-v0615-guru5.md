# #332 Release current-fact alignment Architecture contribution

## Identity And Authority Boundary

- candidate identity：`architecture-contribution-332-release-v0615-guru5-v1`。
- source authority：live Issue #332 与 task `prd.md`。
- planning/behavior authority：task `design.md`、稳定 `implement.md` 与 RDT contribution。
- source/expected current：`docs/architecture/README.md` /
  `current-main-0.6.5-guru.43` / `active`。
- candidate successor：`current-main-0.6.5-guru.44`。
- promotion state：`reviewed_promoted`；successor `current-main-0.6.5-guru.44`。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`。
- change path：`target_native`；ADR required：`true`，仅接受 #240 已独立审查的
  `ADR-008-CANDIDATE`。

本 contribution 定义 `.43 -> .44` 的 release/current fact alignment，并串行消费已合入、已独立
审查的 #240/#348 contribution；这些 authority 已由 serialized owner 提升到 `.44`。它不记录 task
HEAD、动态 Gate 结果、finding closure、tag、smoke、Release、时间或用户授权；promotion state 只记录
shared current 的稳定 successor 关系，不替代 promotion-created diff 的 fresh downstream gates。

## Boundary And Decision

当前 `.43` Architecture/RDT authority 仍将 current release facts 指向历史
`v0.6.15-guru.3`、`0.6.15-guru.39` 与 #267，而 #332 的 accepted current target 已固定为
`v0.6.15-guru.5`、`0.6.15-guru.40`、Trellis CLI `0.6.15`。这造成 current authority 与
committed release-facing source 的事实冲突，阻断当前 task 进入 Publication。

目标边界建立 successor `.44`，把适用的 current release facts、navigation、history、
traceability 与 evidence 对齐到 #332，同时把 #240 的 solution-mechanism semantic owner 与
`ADR-008`、#348 的 archived-task Phase 2 recovery owner/RDT contract 提升为 current authority。
这些能力已存在于 latest `main`，promotion 不新增实现；它使 shared authority 与 live
23-Skill / 97-exit / 81-command graph 一致。`.43`、旧 release、旧 tag、#267 与历史 evidence 的
原始事实继续保留，Architecture promotion single-writer、GAP lifecycle 与 compatibility exit 不变。

## Required Concerns

| Concern | Applicability | #332 contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | 绑定 Architecture 2.0、active `.43`、Issue #332 与 change contract v1 |
| `constitution-binding` | `applicable` | 绑定 current constitution identity；仅命中语义完整、变化隔离与单向收敛 |
| `boundary-and-decision` | `applicable` | `target_native` 收敛 release facts，并接受 #240/#348 已合入 owner topology；不新增实现路径 |
| `owner-and-single-writer` | `applicable` | task 写 contribution；serialized promotion owner 单写 shared current |
| `compatibility-and-exit` | `applicable` | 不建立 adapter、双读或 legacy path；current authority 精确承接 #240/#348 已发布 public exits |
| `gap-and-deviation` | `applicable` | 收敛 current-fact conflict，不关闭或改变既有 Architecture GAP |
| `parallel-scope` | `applicable` | contribution 阶段禁止 shared-current edit，promotion 绑定 expected `.43` |
| `evidence-and-freshness` | `applicable` | 绑定 live #332、`.43` authority、task contribution 与后续 exact ranges |
| `review-and-promotion` | `applicable` | #240 PR #346、#348 PR #351 与 #332 contribution 均须有独立 Review，再由 expected-current owner 串行提升 |

## Before And After

- before：active `.43` 仍声明 `.3/.39/#267` current release facts，并遗漏已进入 `main` 的
  #240/#348 owner、typed exits、RDT 与 ADR authority；task candidate 已是 `.5/.40/#332` 和
  23-Skill / 97-exit / 81-command graph。
- after：successor `.44` 成为唯一 active authority，current release facts 与 #332 对齐；
  #240/#348 reviewed contributions 与 accepted `ADR-008` 成为 current；`.43` 作为 superseded history 保留。
- preserved：历史 tag/Release/authority 原始记录、实现 bytes、Architecture promotion owner、
  GAP/compatibility 与 Issue closure boundary。

## Project Check Contract

使用 `guru-trellis-architecture-convergence:repository:1` /
`guru-trellis-architecture-convergence@1`，绑定 `ARCH-GOV-006..008`、`ADR-005`、
`ARCH-GAP-006`，并在 promotion 后加入 accepted `ADR-008`。检查范围为 authority binding、
release fact alignment、#240/#348 contribution review provenance、owner topology、single-writer、
history preservation、RDT traceability 与 promotion freshness。实现和动态验证证据由
Phase 2、独立 committed full-diff Branch Review 及后续 promotion owner 即时读取；本文不保存
动态 Gate 结果。

## Explicit Boundaries

- 不发布 `v0.6.15-guru.5`，不创建、移动或删除 tag/GitHub Release。
- 不修改、关闭、归档或清理 #267、#311、#333、#339、#358、#361 或其他 Issue/task/worktree。
- 不修改 Trellis upstream、全局 npm、`node_modules`、业务仓库或完整 Release Gate 矩阵。
- 本 contribution 已由 Architecture/RDT owner 绑定 expected `.43` 串行提升到 `.44`；该稳定事实不证明
  promotion-created diff 已完成 fresh Phase 2、task commit 或独立 committed full-diff Branch Review。
