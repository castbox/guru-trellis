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
- `D332-AUTH-06`：`.44` 的 promotion source 组合 #332 release-fact contribution、#240
  solution-mechanism Architecture/ADR contribution、#348 archived-task recovery RDT/Architecture
  contribution与 inherited `.43` authority；#332 作为 serialized promotion owner 一次性建立
  与 latest `main` 一致的 successor，而不创建第二个 current authority。
- `D332-AUTH-07`：#240/#348 原 contribution 保留历史 candidate identity，并更新为
  `reviewed_promoted` 指向 `.44`；current Requirements/Design/Test/Architecture 只引用其稳定合同和
  live merge/review evidence，不复制动态 gate 或用户授权。

Architecture owner 已先激活 `.44` baseline，RDT owner 随后建立继承该 baseline 的完整 `.44`
Requirements/Design/Test authority；serialized promotion 已完成，下一唯一 route 是 fresh Phase 2。

## Preserved contracts

- 三个发布版本轴保持独立：`v0.6.15-guru.5`、`0.6.15-guru.40`、Trellis CLI `0.6.15`。
- #240/#348 的实现与 public I/O 不由本 authority contribution 重定义；`.44` 只消费其已审查
  contribution 并将 live inventory/owner topology 投影为 current。
- #311、#333、#339、#358、#361 的实现、runtime graph、Publication/Finalizer/Issue recovery
  contract 与 public I/O 不在本 authority contribution 中重定义。
- design constitution、project change contract、Architecture promotion owner、GAP 与 compatibility
  exit 不变；本次属于 `target_native` convergence，并正式接受 #240 的 `ADR-008`，#348 不新增 ADR。
- Issue ledger 不扩张；PR 与 Release Gate 的动态证据由对应 owner 在其阶段即时产生。
