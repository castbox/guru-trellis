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

## JQ-R1..4 / BEH-JQ-JOURNEY：正常旅程与交接

来源为 Task `user-journey-quality` generation 0 的整体 PRD JQ-R1..4；相关公开说明为 Issue #747。此增量为当前方法定义。既有 R735 条款与观察边界保持。本次 JQ 定义由该 Delivery 的实际 candidate_checked 后，原 RDT owner 在 final integration 整合并读回；当前定义由包含本文件的精确 Git revision 绑定。方法实现、有限行为观察与受管采用分别判断，最终 Check、Review、Delivery 和 Completion 仍由原 owner 的实际结果建立。

Clarify 从当前有效来源、真实入口及必要消费者推导正常连续操作，区分起点、适用阶段、等待期间正常再次操作，以及完成、失败或放弃后的可见结果。已有行为是调查事实，未明确的产品选择仍由原 Clarify 确认；实现细节归 Author/Architecture。场景沿原正常场景资格规则进入，不用经验扩大范围。

Author 在原 PRD/design 中区分本任务实际存在的局部确认、后台任务完成、可靠保留与最终提交。对当前状态或资源交接，说明业务条件、实际 writer/reader、动作先后及失败后归属。原 Architecture/Approval 在自己的职责内判断条件是否成立，不要求产品指定事务代码，不引入通用锁、压力并发或异常 crash 协议。

存在可运行入口且依赖就绪时，原 implement 验证计划优先取得一条最小完整正常旅程反馈，再扩展有独立检出价值的参数。高风险下层规则可先定向模块验证；简单函数/API-only 按足够层级验证。依赖缺失只阻塞相应声明，完整旅程通过不替代其余必要验收和回归。

真实交互入口、替身与真实适配器的必要语义、实际接受输入和交付构建能力共同限定证据。直接方法测试不证明手势菜单；内存同一实例不证明反序列化恢复；地址存在不证明解码就绪；同容器单样本不证明其它编码组合。具体方法由 Test And Validation Value 单写，不把所有测试升为全链或设备门禁。

关系：D-JQ-JOURNEY 位于 docs/design/current/behavior-validation-method.md；T-JQ-NATIVE 与 T-JQ-DISTRIBUTE 位于 docs/test/current/behavior-validation-method.md。本增量不宣称修复业务缺陷或证明统计改善。
