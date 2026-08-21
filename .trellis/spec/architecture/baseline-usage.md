# Architecture Baseline 使用规则

## Current identity

- locator：`docs/architecture/README.md`
- version：`current-main-0.6.5-guru.39`
- status：`active`
- source binding：task head `d4165f268d36e19139266d28519148c290f773a4` + #290 serialized promotion delta（精确 revision 为当前 Git HEAD）
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
