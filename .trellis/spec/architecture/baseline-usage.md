# Architecture Baseline 使用规则

## Current identity

- locator：`docs/architecture/README.md`
- version：`current-main-0.6.17-guru.72`
- status：`active`
- source binding：reviewed #495 migration candidate contribution + explicit immutable `.71` inheritance；active registry 为 35 Skills / 159 package exits / 106 commands，零 planned IDs；migration standalone-only，business workflow 保持 33 mandatory invokes / 153 exits。current 增量见 `ARCH-CUR-049` / `ARCH-DOM-034` / `ARCH-INT-037` / accepted `ADR-017` / open `ARCH-GAP-012` / `EVD-048`，fixed Fork source 为 `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`，CLI/core `0.7.0-castbox.2`，Guru `0.7.0-guru.2` 是未发布候选。`.71` 的 #490 与更早有效合同保持 inherited authority；promotion-created diff 须 fresh Phase 2/commit/不同 reviewer 完整 Branch Review。本地候选知识不证明 same-remote-HEAD `source_locked`/marketplace/preset provider、完整 `MIG-495-06`、merge/Completion、软件发布、真实业务安装或完整多平台 Release matrix；全部 `MIG-495-01..09` 最终验收仍属于同一任务，迁移 GAP 保持 open。
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
