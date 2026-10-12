# ADR-023：先完成 scope 判断再由唯一 Author 写作

- 状态：`accepted`；来源：#292 design D9.1 与 ADR-292-SCOPE-READY-CANDIDATE，由[durable contribution](../contributions/292-unique-planning-author.md)承接。
- 继承：ADR-022 的唯一 writer、ADR-005 的 promotion 边界与既有 Clarify/context/execution owners。

## Decision

活动 Direct Source 变化时，原 Clarify active profile 先判断当前 scope/来源，private4.0 产生 scope_ready1.0。其 public output 仅为 exit_id、mode、task_ref、source_selection、revision_refs；revision refs 由 Clarify AI 根据实际修订选择。

原 clear-router 使用独立 consumer1.0：删除 exit_id、固定加入 active_task_scope_change，其余四字段直传 Author input1.0。Author 收敛受影响需求和候选，再沿原 Architecture candidate assessment、solution writing、Wording、final Architecture、Approval 与 execution resume 路径。Clarify 不写 planning，不携带规划 hash/旧 task action，不改变 lifecycle。

## Alternatives and consequences

旧 active clear 要求已更新三份 planning，而 Author 又要求先完成 Clarify；context refresh 无法消除该写作前置循环。Clarify 代写会制造第二 writer；Author 绕过 Clarify 会遗漏真实 scope 判断；给旧 clear 增字段会静默破坏 public API；新 router/owner 不必要。

private3.0、public clear3.0 与原 clear consumer2.0 保留 pinned 字节；旧 active 成功结果必须原 Clarify fresh 重入，不能转换旧 pass。非 current/mechanism-only clear 回原中断 consumer，source mutation 先 refresh_context，missing context 保留原四 profile 回程。in_progress 不重跑 initial activation。无新 executor、lifecycle、cache、授权存储或 GAP 生命周期变化。
