# #548 Task 创建与原任务恢复验证

Direct Source：[Issue #548](https://github.com/castbox/guru-trellis/issues/548)，当前正文「目标与范围」「验收条件」「独立交付与非目标」；无评论。#547 独立，不是本 Task 前置。

## 目标

以当前固定 CLI/Core/Guru 组合验证正式创建 → 精确 Task/session 或 explicit-task 路由 → 首个 Delivery Planning → 激活/实施入口。只将支持的诚实正常流程中复现的缺口修入原 owner；现有实现满足时，交付必要联合回归和分层支持证据，明确无需产品修复。

当前源采用 Task schema2、session schema3、Delivery API1/Plan2；此仓主及开发 dogfood 仍是保留的完整旧安装。本 Task 的开发沿该安装正式流程；当前组合的行为验证使用成套隔离安装，不能半升级主仓或用旧运行副本替代当前组合。

受支持的无 context 正式链已实际复现：whole-scope Author/Clarify 成功，首次 Delivery 创建保留原 D1 后在 session selection 返回 `context_required`；后续 Planning consumers 也要求 session current。原 scope AC1/2 内修正原 projection 的显式 identity 读取与原 Creation 结果恢复。已有 context 时仍由官方 session 负责，不能把缺失、过期或冲突的 session 当成无 key 路径。

## 验收

| AC | 精确观察 |
| --- | --- |
| AC1 | 正式创建后，真实 Codex context 解析同一 TaskId/gen；缺 key 时正式 explicit-task owner 继续且不要求不适用的会话记录 |
| AC2 | 创建 → whole-scope Author/Clarify → D1 creation → Delivery Author/Wording/Architecture/Approval/Activation → implementing 保持同一 TaskId/gen，D1 只有一个 identity |
| AC3 | 创建实际成功后丢输出、attach 普通失败后的原结果恢复，不依赖缺失 current_task，不增加 Issue/Task/branch/worktree/Delivery |
| AC4 | 新 session rebind 同一 Task；其它合法 current route、stale generation、错误对象或冲突保持原记录并返回原 owner 的明确诊断 |
| AC5 | 隔离旧 nonterminal/untracked-only Task 缺 HEAD identity：实际公开 migration preview 给出支持的逐记录转换或 defer/manual 停止；旧字节、身份、规划和 Git 资源保留，停止不记为恢复通过 |
| AC6 | 恢复保留规划、历史、普通 dirty/untracked 和并行 Task/session；恢复不建立 Planning/Activation/Completion pass；native continuation 读取真实当前 owner |
| AC7 | package/runtime、代表性 installed/native、platform projection、reapply/drift、migration 各自报告范围；模拟 context 只证明测试层 |

## 范围和验证边界

复用原创建、C4/C5、绑定、Delivery 与升级 owners，不建立第二 writer、mapping 或恢复状态机。定向覆盖普通 stale/mismatch/conflict。只补与上述验收存在直接关系的联合测试，现有测试继续复用。

不升级/清理原业务仓库，不删除重建原 Task，不回退 start-task/workspace-mapping，不执行完整多平台/Release matrix，不加入攻击、锁、竞态压力或非常规 crash consistency。

真实平台样本只证明当前受控安装和本次 context；不声称原 CMS 会话已恢复。完整语义 Check、独立完整 committed Review、readiness、Delivery、whole-task Completion、Closure、Finish 和资源处置仍由正常流程各 owner 执行。
