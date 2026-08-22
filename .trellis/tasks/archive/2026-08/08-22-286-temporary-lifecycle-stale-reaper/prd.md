# #286 临时对象生命周期与 stale 回收

## Goal

为 Guru Team 自身自动创建的临时目录和临时输入建立一份可复用、可审计的生命周期合同：正常成功、失败、SIGINT、SIGTERM 和支持的早期校验返回都执行精确清理；无法 trap 的残留在下一次运行按登记前缀和 closed stale 条件回收；本地删除策略拒绝实际删除时诚实报告 `deletion_unverified`。

用户价值是避免 Guru 自有运行残留长期累积，同时不误删调用方、其它应用、业务仓库或未登记对象，并让 #287/#293/#267 直接复用同一 ownership contract。

## Confirmed Facts

- Live Issue #286 是 open，标题/正文/`updatedAt` 已由 Phase 0 current readiness 绑定。
- #295/#296 已修复 Sync 到 Discovery 的 public handoff；该 Entry blocker 不属于本 Issue。
- 当前创建点分散在 preset staging、throwaway install、extension verification、task commit、Phase 2/installed verifier 所列脚本和 runtime 中。
- 现有实现使用 `TemporaryDirectory`、`mktemp` 和 caller `WORK_DIR`，没有统一 inventory、owner、controlled root、prefix、stale 判定和 cleanup disposition。
- #287 负责 staging strategy，#267 负责完整 exact-candidate 矩阵；本 Issue 不吸收两者。

## Requirements

1. 建立 canonical temporary inventory，逐项声明 owner/runtime command、object kind、controlled root resolver、exact prefix、auto-created/caller-provided、live/in-use 与 stale 条件、normal cleanup、next-run recovery、diagnostic/test owner。
2. 为 canonical auto-created 对象提供统一 cleanup/reaper API；cleanup failure 不覆盖 primary result，但必须返回可诊断 disposition。
3. stale reaper 只解析登记的 controlled roots，只匹配登记 prefixes，只处理 closed stale 且非 live/in-use 对象；不得 broad `guru*`、跨 root、follow unsafe target、扫描 `/private/tmp` 或 `/private/var/folders` 其它对象。
4. 显式 `WORK_DIR`、caller-owned、unknown、其它 application/user 对象和业务 repository 对象始终排除。
5. canonical source、dogfood、installed、Shared/Codex/Claude/Cursor 与 preset projection 保持一致；新增 prefix 缺少 inventory/test/consumer 时 fail closed。
6. 通过 targeted package/runtime/unit/integration coverage，覆盖 success/failure/signals/repeat/stale/explicit root/exclusion；执行 current preset apply、verify、reapply/drift 和一个代表性 isolated/clean fixture。
7. local deletion policy 拒绝真实删除时只能报告 `deletion_unverified` 或 CI/isolated route，绝不把未执行命令记为 PASS。

## Acceptance Criteria

- 自动创建对象在 success、ordinary failure、SIGINT、SIGTERM、supported early validation failure 后按合同清理。
- SIGKILL 及其它无法 trap 的异常残留在 next run 按 exact stale 条件回收；重复运行不永久累积。
- explicit `WORK_DIR`、caller-owned、unknown、non-stale/live/in-use 和其它应用对象都保留并给出原因。
- 每个 candidate 输出 owner/root/prefix/stale reason/delete result/retain reason；root resolution 错误 fail closed。
- cleanup failure 保留 primary result 并返回 exact disposition。
- canonical/dogfood/installed/Shared/Codex/Claude/Cursor/preset projection 一致，reapply/drift 无回退。
- #287/#293 可直接消费同一 inventory/root/cleanup/reaper 合同；不重建第二套 reaper。
- local deletion restriction 被明确记为 `deletion_unverified`；approved CI/isolated evidence 单独记录 actual deletion。
- fresh committed full-diff Branch Review 无 blocking finding；不创建 tag/Release。

## Out Of Scope

- #287 preset staging 物理复制架构、APFS CoW、managed-path transaction。
- #267 完整 multi-platform exact-candidate matrix。
- #293 的新 Finalizer input 实现，仅保留复用合同的直接测试边界。
- business repository worktree/branch/remote cleanup、caller/global garbage collection。
- Trellis upstream、global npm、`node_modules`、`.fseventsd`、service restart、锁/压力竞态、攻击模型和人为伪造 fixture。

## Planning Status

所有产品范围、兼容性和风险决定均已由 live Issue 与当前代码证据解决；没有阻塞性 open question。实现前仍需后续显式批准本 planning summary，并通过 planning wording、Architecture/RDT 与 Guru plan approval gates。
