# DAG 局部处置职责

Identity：`ARCH-DOM-DAG-LOCAL-DISPOSITIONS`。来源：[Issue #883](https://github.com/castbox/guru-trellis/issues/883)。本文件是拟晋升定义，实际采用由原 Architecture owner 整合并回读。决定来源为 [ADR-DAG-LOCAL-DISPOSITIONS](../adr/dag-local-dispositions.md)。

运行合同由 [共享编排方法](../../../trellis/presets/guru-team/spec/workflow/issue-orchestration.md) 唯一定义。DAG 入口消费现有会话授权并负责安排、观察和回读。动作受限时，DAG 调度仍根据原依赖与剩余工作维持观察。Sequence 只消费原共享职责，保留串行边界。

两项 DAG 局部处置的原执行职责不变：节点执行者拥有共享 Git 仓库的注册事实、限定清理与回读；原 Issue owner 拥有内容审核、精确写回和后继 Intake 刷新。协调者不取得 Git/GitHub 写入者职责，不替代真实范围决定。目标仓库的直接确认要求继续约束协调者。全部执行条件、限定范围和恢复行为在共享方法中维护，本文只约束职责归属。

作用域、原 owner、执行接口或权限来源发生实际变化时交原 Architecture owner 重评，不预设额外的调度或数据机制。
