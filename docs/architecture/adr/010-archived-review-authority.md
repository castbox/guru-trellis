# ADR-010: Archived Review Authority

状态：`accepted`。来源：[Issue #418](https://github.com/castbox/guru-trellis/issues/418) 的
`target_native` contribution；expected predecessor 为 `current-main-0.6.17-guru.52`，
knowledge successor 为 `current-main-0.6.17-guru.53`。提升前独立完整审查绑定
`78651e2068184e9e52a778fe33eda8b2bd7c8e0b...c30eadd6cf6fe4ba204c32c6e89f3f25f892e8f4`。
本 ADR 不表示 promotion-created diff 的后续 gates 或软件发布已经完成。

## Context

普通 Publication preparation 要求 active task；Finalizer 的归档连续性绑定归档前 review tip。
对 completed archive 直接重放普通 profiles，不能同时满足这些合同。映射遗留或真正缺少当前
复审结果需要明确恢复路径，但不能把正常 checkpoint 退休当作失败，也不能改写历史或绕过门禁。

## Decision

在原 Merge、Branch Review、Publication、Finalizer 四个 owner 内增加专用只读 profiles，
不新增 Skill、command、通用恢复状态机或第二 writer。具体 I/O 由各 canonical Interface 独占。

1. Finalizer 原 archive/exact recovery executor 在验证同一 task 的完整双端映射及 committed
   archive 后收敛 locator；reader 不修复未知、缺失或冲突映射。
2. Merge 的复审请求仅捕获现有 Ready PR 快照并交给 Branch Review，不批准或执行 merge。
3. Branch Review 独立审查当前 `B...A`；Publication 重新审查当前实际 title/body，快照只用于
   一致性，不是旧批准或新批准。B 与 payload 漂移必须由当前 consumer 拒绝。
4. Finalizer 从 committed summary 的 commit 集合按 ancestry 推导唯一原 tip H，复用原归档
   连续性验证；A 不替代 H。校验新 Publication payload 后仅返回原 `ready_for_merge`。
5. 三个新 success edges 前分别执行 fresh Architecture `branch_review`、`publication`、
   `acceptance_finish`。只读范围只能承接 current authority，或在缺证据/需写入时停止。
6. 普通 aggregate 4.0 的两个 profiles 与 gate 7.0 行为持续有效；aggregate 5.0 加入的
   `archived_review` 使用独立 `archived-1.0` gate，不升级旧私有 gate，也不放宽普通输入。

## Rejected Alternatives

- 放宽普通 Publication 的 task status：会将 active preparation 与 archived validation 混在一起。
- 用 A 代替 H：会丢失原归档历史约束。
- 为复审整体 restore task：引入不必要的业务状态及历史写入；真实 task-work 恢复仍归原 Restore owner。
- 只修正文案或手改旧 gate：无法建立当前独立审查和新的 Publication payload 判断。

## Consequences And Evidence

增加四个 profiles、三个 success exits，当前完整图为 23 Skills / 100 exits / 78 commands。
普通 mutation、Issue closure、ledger retirement 和 closed GAP 边界不变，不增加兼容 shim。
只读链不修改 task、archive、PR、Issue 或 refs；短期 gate 仍由原 owner 记录、校验并退休。

提升前证明见 [EVD-028](../evidence/current-evidence.md)：包含真实 installed wrappers、
schema/投影、ordinary/archived 分离与回归测试。Native 归档语义执行、原业务实例及完整 Release
矩阵仍未验证。共享 successor 必须经过 fresh Phase 2、新 task commit 和 distinct full Branch
Review 后，才能被 Publication/Acceptance 消费。
