# #521 设计职责

状态：reviewed_promoted；Architecture 由[任务贡献](../../architecture/contributions/521-checkout-isolation.md)拥有，change path `target_native`。各步骤的完整合同只在其 canonical owner 定义。

| Identity | 唯一职责与直接 consumer |
| --- | --- |
| D521-01 / CON521-PREWRITE | selector 只判 mode；execute-task-free-change 的 pre-write suitability 读取位置、差额和 binding，首次写入前确定 linked/non-base。location_required 回同 owner，不调用 Task acquisition。 |
| D521-02 / CON521-CALLER | Guru workflow caller 消费上游 no_current_task；fresh 范围/位置/绑定决定轻量接续。上游 stop 结束它自身步骤，实际 native 返回无法接续时单列依赖，不 patch 上游。 |
| D521-03 / CON521-C6 | C6 composition.prepare_creation_inputs 与 guru-create-task 的 create-only 约束拒绝新 Task primary acquisition；shared adopt/recover/resolution 和旧 Task result recovery 保留，clean invariant 不放宽。 |
| D521-04 / CON521-EVOLUTION | 原 execution owner 停止剩余 writes、完整保留差额；自动/显式回原 owner。无 Issue 标准接管由原 Review 的 standalone_request 输入保持 workflow mode，来源 profile 与执行 mode 独立，原 producer/owner mode equality 保留。dirty 候选不能直接 adoption，原 Intake 选择 clean linked 并在精确承接边界操作，不造空 Task或迁移账本。 |
| D521-05 / CON521-DISTRIBUTE | 原 preset/workflow owners 从 canonical 同步当前投影与文档；一个代表性 clean/current-update/reapply 检查 upstream bytes。业务安装和正式软件 Release 独立。 |

新聊天靠明确请求与 live facts，信息不足返回 location_required/有界 blocked。无 Task registry、mapping、wrapper、第二生命周期、双模式或 OS 权限机制。现 Task session/branch/resource 的权威不因隔离位置而转移。

旧 current-checkout 仅为 pinned 历史合同；current consumers 同步时退出其文案/示例。旧 primary Task 逐例由原 lifecycle owner 根据 live binding/control state迁移；不以全局 resolver 禁令代替，不预填迁移完成。

