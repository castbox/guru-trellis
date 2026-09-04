# #332 Release current-fact alignment Design contribution

## Authority lifecycle

- `D332-AUTH-01`：task worktree 只负责本 contribution；RDT 与 Architecture promotion
  owner 串行写 shared current，两个 owner 不并行修改同一 current 文件。
- `D332-AUTH-02`：RDT 与 Architecture 使用同一 source/expected current `.43`、successor
  `.44` 和 release mapping `.5/.40/CLI 0.6.15`，保持单一 current identity。
- `D332-AUTH-03`：promotion 先由 Architecture owner 激活统一 `.44` baseline，再由 RDT
  owner 建立并继承 `.44` Requirements/Design/Test authority；任一 owner 发现 live current
  已不再是 `.43` 时返回 `sync_required`，不得覆盖新 authority。
- `D332-AUTH-04`：promotion 只投影适用 current release facts、navigation、history 与
  traceability；`.43` 正文只接受 lifecycle status 与 predecessor/successor 收敛，不原地改写
  为 `.44`。
- `D332-AUTH-05`：promotion-created shared-current diff 是新的 reviewed content，必须重新
  执行 Phase 2、task commit 与独立 committed full-diff Branch Review，不能复用 contribution
  review 或旧 task commit。

## Preserved contracts

- 三个发布版本轴保持独立：`v0.6.15-guru.5`、`0.6.15-guru.40`、Trellis CLI `0.6.15`。
- #311、#333、#339、#358、#361 的实现、runtime graph、Publication/Finalizer/Issue recovery
  contract 与 public I/O 不在本 authority contribution 中重定义。
- design constitution、project change contract、Architecture owner、GAP 与 compatibility
  exit 不变；本次属于 `target_native` authority-fact convergence，不创建 ADR。
- Issue ledger 不扩张；PR 与 Release Gate 的动态证据由对应 owner 在其阶段即时产生。
