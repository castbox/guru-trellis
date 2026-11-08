# 正常完成与协调成本：需求差额

状态：proposed。来源为 [Task 整体需求](../../../.trellis/tasks/11-08-normal-completion-design/prd.md) NC-R1—R7；本批完整承担，未改变来源或范围。固定 B 为 `80fc24eed3d4deb2dd0fc63126c0affb9789d365`，原 authority identity 保持 `guru-trellis-rdt`。

完整拟写位于 `proposed/docs/requirements/current/knowledge-maintenance.md`，保留所有有效前驱、稳定身份和历史观察，只修改 R-MECH-01、02、04：

- R-MECH-01 承接 NC-R1—R4、R6：从最终可观察结果推导直接路径，额外协调默认不准入，作者和独立审核主动尝试简单替代；原方案最小时不虚构替代，功能正确与完成成本共同判断。
- R-MECH-02 承接 NC-R2、R4、R6：保留原保护提出方举证和必要保密/权限，明确资格不代替 Architecture 取舍。
- R-MECH-04 承接 NC-R5：必要性已证、缺陷已证与证据不足分别处理；已证问题有界整改，缺证不擅删、不扩大机制，无关工作继续。

R-MECH-03、05 的证据适用性和存量消费者规则继续有效。设计与测试由本贡献的对应文件及完整 proposed targets 承接；不复制通用方法全文，不新增阶段、接口、状态、固定问卷或性能矩阵。NC-R7 的验证与采用边界在 test.md 明确。

这是候选定义，不能作为 shared current 或正式质量结论。原维护 owner 在完整候选检查后按 final_integration 合并、实际写入与读回；安装采用及业务整改不由本贡献证明。
