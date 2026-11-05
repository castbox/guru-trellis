# 行为测试与因果验证方法能力

Identity：RDT-REQ-BEHAVIOR-VALIDATION；别名：R735/BEH735。原语义 owner：guru-maintain-requirements-design-test-ssot。来源：https://github.com/castbox/guru-trellis/issues/735 行为要求1–4和验收1–7。状态：current。变更起点 main@b78edbbdc32e77392bc3775366473971050ccb4b；精确当前定义由包含本文件的 Git revision 绑定。晋升依据：原 candidate Check 的 candidate_checked 与原 RDT owner final integration 实际整合和读回；最终 Check、Review 和交付仍由原 owner 判断。

## R735-01 / BEH735-CONTRACT

Author、实现者和审核者从当前需求、设计或已确认缺陷取得正确预期，在原验证章节连接条件、动作、结果与独立断言。唯一通用方法正文为 [Test And Validation Value](../../../trellis/presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value)，本单元不另立测试标准。方法适用于合同要求的API、Biz、工具、运行与资源行为，依据实际风险、证据缺口、环境和成本选择足够观察层级与执行顺序。红绿过程不是交付条件。

## R735-02 / BEH735-CAUSAL

原根因资格在进入实现前判断当前因果依据、候选机制和验证计划，完成 owner 再判断修后证据。反事实依据可来自适用既有观察、因果分析或有界对照。已有日志本身不证明新回归有效；实际触达仍有疑问时先查入口、分支和观察，仍影响有效性才补旧实现对照或等效检出验证。保留必要因果依据，不禁止合法对照。

## R735-03 / BEH735-STOP

追加当前已选验证集以外的诊断或反事实实验，须回答现有证据不能回答且影响修复选择或验收的具体问题，说明要观察什么及其决策作用；必要验收和受影响回归保持原合同。有效既有证据可采用，充分后结束该项，不因阶段/执行者更换重做。长期回归与临时诊断目的分开，重复覆盖须有独立检出价值。设施反复失败时重评复现方式；未触达产品路径的编译、依赖、fixture/装配失败或预期异常未出现不能冒充目标产品缺陷RED，正常预期错误测试可有效通过。未解决验收保持缺口，不弱化业务断言。

## 归属与关系

不新增 Skill、阶段、公共I/O、证据账本或审批。原 Author、root qualification、实施协调、Check、Branch Review 保持自己的判断与出口；脚本仅执行和校验事实。设计 D735/CON735 位于 docs/design/current/behavior-validation-method.md；测试 T735/SC735 位于 docs/test/current/behavior-validation-method.md。现有工程事实适用性和审核充分性沿各自唯一源；本项不改生产完成语义或 #734预算范围。
