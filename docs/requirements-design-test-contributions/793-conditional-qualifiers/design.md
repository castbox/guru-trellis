# #793 设计贡献

原 owner：guru-maintain-requirements-design-test-ssot；状态为已晋升来源；实际 current 定义位于对应完整目标。
完整拟写为 [qualifier-applicability](proposed/docs/design/current/qualifier-applicability.md)，
对应本批唯一 Delivery design 的第4—7节。原 Architecture 决定与九 concerns
仍归该 Delivery 的真实 contribution/ADR 及原独立评估，RDT 不复制其判断。

本轮直接修改原包、原 caller 和 workflow；保三独立 owner、固定 profile、
nonempty 输入、全部原出口/consumer。短 reference 承担加载前条件，caller
判断是否触发；正式资格只在原 Skill 执行。无新 schema、wrapper、classifier、
ledger 或兼容双reader。现行 DES-382-01..05 的算法/路由/持久化边界保留，
仅将两上游结果前置收敛为当前 caller 判断与适用的真实结果。

完整 matching 采用、在途恢复与原 tools owner 的分发由
[MIGRATION-793](../../../trellis/presets/guru-team/MIGRATION-793.md) 定义；源码、
dogfood、目标项目采用和业务效果分别报告。原 candidate Check 后才进行
final_integration/readback，随后实际 after 重绑并完成最终质量链。
