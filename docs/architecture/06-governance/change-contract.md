# 验证样本维护协议

Identity: sample-change-contract。状态: current。Concern set: sample-concerns。

当前样本只维护完整文档；没有网络、数据库、部署或外部服务。查询和导出定义各自归一个单元，不共享业务状态；共享入口单元必须完整保留历史条件和缺来源 repair。两条 consumer 只引用完整单元，不复制业务定义。

Task 选择 fixed Git B 中的 authority。首次独立 Architecture 读完整候选和未改 consumer，再由原 Check 完成候选检查。候选成功仍不是晋升。原维护 owner 最终读取真实 target、保留已晋升条件并组合，独立 reviewer 补审实际差额后才写 shared current。写后读回、重新绑定候选并完成最终 Check。没有真实冲突或依赖阻塞时不需要 Git 整合。

本样本 project check 是 AI 语义协议：descriptor_identity=sample-knowledge-boundary:1，check_id=sample-knowledge-boundary，check_version=1；entrypoint=docs/architecture/06-governance/change-contract.md；scope=[complete-units,condition-preservation,unchanged-consumers]；rule_refs=[SAMPLE-RULE-OWNER]；decision_refs=[]；gap_refs=[]；result_contract_identity=guru-project-architecture-check-result-2.0。检查 before/after 单元完整性、命中范围、有效条件、两条未改 consumer 和真实写入时机。没有未关闭的项目 GAP。
