# Architecture Baseline 使用规则

## Current identity

- locator：`docs/architecture/README.md`
- version：`current-main-0.6.17-guru.66`
- status：`active`
- source binding：reviewed #454 D436 contribution + inherited immutable `.65` authority；active registry 保持 32 Skills / 142 package exits / 102 commands 与六个 planned IDs，production workflow 保持 22 mandatory invokes / 98 exits；current 增量见 `ARCH-CUR-043` / `ARCH-DOM-028` / `ARCH-INT-031` / `ARCH-GAP-011` / `EVD-041`，fixed Fork source 为 `eb370008c7689d4e272ae626bd002190ecbb3296`。`.66` 继承 C2-C7/D443 并增加五个非激活 D436 terminal lifecycle canonical packages；E434 与 #434 production graph activation 尚未完成。五包、共享 lifecycle runtime 与 package integration 定向合跑 `226/226`；installed/platform 与完整 Release matrix 均未声明通过，promotion diff 须 fresh Phase 2/commit/完整 Branch Review。
- Finalizer recovery binding：既有 `REQ-048/DES-046/TST-032/SCN-044` 同时覆盖 same-base fresh-reviewed transaction reprepare；只消费合法 predecessor tail、selected-base lineage、current review/Publication/live HEAD equality、Open PR absence 与 transaction-owned remote endpoints，不把 terminal PR history、branch name、session 或 path 提升为 authority。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `current`
- project change contract：`docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`
- required concern set：`guru-trellis-architecture-change-concerns-v1`
- project check：`guru-trellis-architecture-convergence@1`

## 语义分区

FOUNDATION 是横向约束；CURRENT 必须有 code/config/test/release evidence；TARGET 是 accepted future state；GAP 是 explicit delta；PLAN 只记录依赖；ADR 是历史；EVIDENCE 支撑而不替代 judgment。`inferred` 与 `unverified` 不得晋升为 CURRENT。

## Task route

文件变更先走 `guru-maintain-architecture-baseline:task_impact_sync`。`sync_required` 进入 `promotion`；`baseline_incomplete` 回 Bootstrap/repair；`architecture_conflict`、`contract_incomplete`、`fitness_regression` 回对应 owner；`blocked` 停止。普通并行 task 使用隔离 contribution，不写同一 shared current。

## Freshness

每次 gate 重读 live baseline locator/version/status、design constitution、project change contract/check descriptor、RDT public identity、task delta 和 source binding。任一 locator 缺失、CURRENT/TARGET 串位、版本冲突或 projection stale 时 fail closed，并进入 `repair`；不得靠本页摘要继续。
