# Architecture Baseline 使用规则

## Current identity

- locator：`docs/architecture/README.md`
- version：`current-main-0.6.17-guru.75`
- status：`active`
- source binding：reviewed #495 version-family exact-source acceptance contribution + immutable `.74` inheritance；35 active Skills/159 exits/106 commands，零 planned，migration standalone-only，business33/153。正式 Fork `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / CLI/core `0.7.0-castbox.3` / CI `37647767799`，Guru `0.7.0-guru.3` 为未发布目标；Architecture ARCH-CUR-049/ARCH-DOM-034/ARCH-INT-037/ADR-018/closed ARCH-GAP-012/EVD-051。全部正常 `v0.6.x-guru.*` 和 `v0.7.0-guru.*` 来源按实际差异分组；唯一结果见 `docs/requirements-design-test-contributions/495-upgrade-version-families/test.md`。EVD-051只绑定精确远端 `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的同源验收；EVD-050/.74 与 EVD-049/.73 保留为历史，首次失败与恢复不改写，不声明业务原始在途。晋升diff须freshPhase2/commit/独立完整BranchReview，后继文档HEAD不冒充同源重跑，merge/Completion/Closure/Finish/Release/真实业务安装/完整矩阵仍由各owner判断。knowledge identity 不是软件发布状态，#500 的最终候选须在准备与终态归档合并后从 fresh origin/main 独立验证。
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
