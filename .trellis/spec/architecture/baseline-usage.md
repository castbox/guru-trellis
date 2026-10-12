# Architecture Baseline 使用规则

## Current identity

- locator：`docs/architecture/README.md`
- version：`current-main-0.6.17-guru.84`
- status：`active`
- source binding：reviewed #521 committed contribution + immutable .83 inheritance + ARCH-CUR-057 / ARCH-DOM-040 / ARCH-INT-043 / ADR-021 / EVD-060；registry36/164/109、business34/158不变；actual results仅由docs/requirements-design-test-contributions/521-checkout-isolation/test.md拥有。software axes/GAP lifecycle不变；晋升差额须fresh gates，实际Task创建/承接、业务安装与Release未验证。
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

## Root-Cause Candidate Usage

Architecture retains independent responsibility and necessity judgment. New or materially changed incident mechanisms consume guru-qualify-root-cause after actual normal/solution outcomes; qualification does not promote Architecture or prove completion.
