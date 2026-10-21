# #648：原 owner 方法与验证职责增量

状态：`proposed`；适用源与完整目标由[manifest](manifest.yaml)定位。完整设计定义位于 `proposed/docs/design/current/knowledge-maintenance.md` 的 D648 / CON648 小节。本增量保留独立Architecture、原单写、#637覆盖与工程事实复用，以及#638候选检查→最终整合→实际after重绑→最终质量链。

公共行为继续由原Author、Architecture、实施协调、Check、Branch Review及task-free owners判断；确定性代码只投影真实文件、运行原命令、落Agent实际写出字节、校验和记录客观结果。owner方法差额须根据变更前实际行为与完整来源核对确定；已经有充分证据的现行能力保留，不把两侧都检错记为新增收益。

原native Adapter扩充现有测试路径，测试私有事实和运输不成为公共Skill I/O。被测Agent必须自己读取来源、写作、作判断并调用原wrapper。多owner链消费实际前序stdout，在同一stateful fixture核对原公共转换；本地种子前置只证明测试起点，不算本轮真实前序审核。host期待与另一侧轨迹不进入被测上下文。

当前Architecture planning candidate/final原owner结果为no-impact；本候选不建空Architecture contribution或ADR。实际机制若扩owner、公共接口、持久状态、权限或兼容边界，停止该扩张并回原qualification/Architecture。原RDT最终整合后，implementation重新绑定全部实际写入，不能借用写前候选验证写后内容。
