# Architecture Baseline 规则

Guru Team 的 `guru-maintain-architecture-baseline` 是 Architecture Baseline
语义 owner。业务仓库的 `docs/architecture/` 持有 FOUNDATION、CURRENT、TARGET、
DOMAIN、INTEGRATION、GAP、GOVERNANCE、PLAN、ADR 与 EVIDENCE 正文；Trellis 只持有
可复用 contract、索引和最小 locator projection。

CURRENT 不等于 TARGET，TARGET 不等于实现，GAP 不自动进入 task scope，PLAN 不等于
完成，ADR draft 不等于 accepted authority。active baseline 缺失、冲突或过期时必须
fail closed。不同 task 只能写 task-owned contribution，active baseline 由 review
后的 promotion owner 投影；普通 stale/conflict 只阻塞当前 contribution。
