# #692 设计差额

贡献编写时状态：proposed；适用同一基线及公开 Architecture `guru-trellis-architecture / docs/architecture/README.md / active`。完整责任由 [D692/CON692](proposed/docs/design/current/local-fix-intake.md) 拥有。

直接细化 selector、Create Issue、Discovery、Clarify、Author 的现有合同。Discovery 只拆已有比较、保留原错误诊断到当前 AI consumer，不新增 provider、Skill、公共 DTO 或持久化。选择本地 additive 诊断可保留原拒绝和调用图，避免跨 owner 缓存与恢复层的维护成本。Planning 的 no-impact 不代替实际实现的独立 Architecture 判断。

隔离完整 proposed 先经 candidate Check；原 RDT owner 随后在 final_integration 固定真实目标、写入并读回。原实施 owner 重绑实际候选，最终 Check 与独立 committed Review 覆盖真实正文和导航。无 Architecture 变化时不创建空 contribution/ADR。
