# ADR-DAG-LOCAL-DISPOSITIONS：在原编排边界承接局部确认

状态为已整合，待独立提交审查。来源：[Issue #883](https://github.com/castbox/guru-trellis/issues/883)。前置：[Issue 审核 Intake 决定](issue-review-intake.md)、ARCH-FND-002、ARCH-FND-005。

## 决定

采用 `target_native`。在原共享编排 Markdown 中单写 DAG 的局部处置和观察交接。DAG 保留调度，再由原执行者完成限定清理或原 Issue 操作。协调者核证原权限和实际结果，不取得原 Task、Git、GitHub、Clarify 或 Readiness 的写入及审核职责。目标仓要求用户本人确认时，继续走原边界。Sequence 不获得 DAG 的局部例外。

## 取舍和代价

改用后台定时器会把同轮继续观察转为新的调度职责。由脚本从 Git 状态或标识不冲突推定授权，会移走原 Agent 的语义判断。保留现有消息、观察和原执行工具，代价限于共享合同、两处薄引用、隔离场景和定向分发核对。不引入持久授权、审批对象、兼容路径或新公共字段。

跨仓、资源范围或原执行 owner 真正变化时复查本决定；实际宿主能力不足沿原恢复报告。阅读 [共享运行合同](../../../trellis/presets/guru-team/spec/workflow/issue-orchestration.md) 核对执行条件。候选真实行为和安装采用由原检查证明，本文不声明它们已通过。
