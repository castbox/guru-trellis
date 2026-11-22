# #880 完整设计提案

状态 `integrated_pending_review`；前驱 Git `76198a53b4da989b66d2e5f135ff4d2b703ca3cf`。独立 final_plan 为 `no_architecture_impact/no_change`；保留原 owner、公共 I/O、typed exits、恢复和事实执行边界，无 Architecture contribution 或 ADR。原 RDT owner 已在真实工程结果后写入六个 current 目标并 readback，尚待 TaskCommit 与独立 committed Review。

## D880-01 / CON880-ISSUE-CONTENT：唯一内容正文

承接 R880-01..07。在 Clarify-owned `issue-content.md` 原“验收切面与必要结果”段直接增加责任层组合、环境／部署／业务发布分离及场景集合独立风险规则。原结果／证据分类、边界内最外沿观察、原文完整审核与薄 owner 引用保持。`acceptance-boundary` 教学例增加目标环境正例、业务配置发布非服务部署和重复场景负例，不新增平行 SSOT、映射字段或裁剪执行器。

## D880-02 / CON880-VALIDATION：跨阶段最小边界

承接 R880-02/03/06。在 `quality-guidelines.md#test-and-validation-value` 原责任边界段补充服务版本部署、共享 test 部署、目标环境执行和业务发布配置的区别。有效需求或环境唯一性决定目标环境证据；最小验证不能删除明确承诺，部署通过不能替代未覆盖合同。Issue 专属场景集合规则仍由 D880-01 拥有，本节不复制。

## D880-03 / CON880-OWNERS：原门禁与单一消费者

承接 R880-05。Clarify、Readiness 和 Create Issue 继续沿现有薄引用和完整正文检查使用同一规则。Readiness 保留原十维与回程；Create Issue 保留首次 provider 写前核对和 `refresh_review`。不新增 Skill、profile、typed exit、schema、DTO、审批或独立 reviewer。

## D880-04 / CON880-EVIDENCE：现有 eval 与受管分发

承接 R880-06/07。扩展现有 `issue-acceptance-boundary-source.json` 和原 native eval case，使同一去敏 mixed scenario 包含组件、CLI、明确目标 runtime、业务配置发布及无依据环境／部署／重复场景建议。`test_issue_content_distribution.py` 将 `acceptance-boundary` 教学例纳入真实 writer/reapply 检查。受管 dogfood 与声明平台投影由原 `guru-upgrade-tools`／installer 同步，不手工覆盖。
