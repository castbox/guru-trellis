# Architecture Baseline 使用规则

## Current identity

- locator：`docs/architecture/README.md`
- version：`current-main-0.6.17-guru.73`
- status：`active`
- source binding：reviewed #495 fixed-source acceptance contribution + immutable `.72` inheritance；35 active Skills/159 exits/106 commands，零 planned，migration standalone-only，business33/153。固定 Fork `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1` / CLI `0.7.0-castbox.2`，Guru `0.7.0-guru.2` 未发布候选；Architecture ARCH-CUR-049/ARCH-DOM-034/ARCH-INT-037/ADR-017/ARCH-GAP-012/EVD-049。固定远端 `6a563f5f` 的 source_locked/provider/actual installed、真实PR/merge与accepted旧正式writer构造在途分别取证；唯一结果见 `docs/requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/test.md`。首次失败与恢复保留，不声明单轮7/7或业务原始在途。晋升diff须freshPhase2/commit/独立完整BranchReview，后继文档HEAD不冒充fixed-source执行，merge/Completion/Release/真实业务安装/完整矩阵仍由各owner判断。
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
