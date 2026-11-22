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

## #868 本次整合与关系

原RDT owner在批准规划、实际实现及真实工程结果后，于固定前驱Git `b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec` 的Task隔离checkout完成final_integration和读回。状态为`integrated_pending_review`，尚待TaskCommit及独立committed Review；不产生质量或Completion通过。来源和替代范围见[#868追踪](../../requirements-design-test-contributions/868-issue-acceptance-boundary/traceability.md)。既有来源、完整条件及旧观察截止保持。

## R868-04 / BEH868-EVIDENCE：共用最小充分证据

各原owner在accepted responsibility内选择最外沿有效观察，不沿调用链追到消费方接入、E2E、生产采用或联合验收。仅在有效需求包含联合交付，或自身承诺须经集成证明时保留最小相应验证，指出承诺与现有证据缺口。外沿充分证据已覆盖时不逐层复制单元/集成/E2E/联合验收；内部明确条件缺口只补定向证据。替身只隔离边界外依赖，不制造被测组件结果。对象/版本、条件、路径和结论仍适用的证据复用，阶段、reviewer或信心变化不要求重跑。原owner独立判断当前充分性。唯一跨阶段方法为quality-guidelines Test And Validation Value，共同review-sufficiency薄引用，不新建表/账本/阶段。对应D868-03、T868-02/03。

对应[设计D868-03](../../design/current/behavior-validation-method.md)、[测试T868-03及关联T868-02/04](../../test/current/behavior-validation-method.md)；Issue-specific R868-01..03由[Issue内容单元](issue-content.md)拥有。

## R880-02/03 / BEH880-ENVIRONMENT：环境、部署与业务发布边界

服务版本部署、共享 test 环境部署、目标环境执行和业务发布配置操作是不同责任。普通工作不默认逐变更部署共享 test 环境；只有有效需求明确承诺，或只有该环境才能建立所需合同时，才要求目标或共享环境证据，并保留准确环境与未验证边界。业务操作名称包含 publish、config 或 sync 不自动产生服务部署义务。反之，最小验证不能删除明确目标环境承诺，部署成功也不能替代部署未实际覆盖的组件合同。

## R747-D1-01 / BEH747-JOURNEY

在涉及正常连续操作的需求中，Clarify 从当前来源、真实入口和实际调用方推导起点、阶段、允许动作及等待期间的正常再次操作。按任务实际分支，写清成功、失败、放弃和恢复后的可见结果。无交互任务使用真实调用方。既有行为只提供调查事实。原需求入口处理未决产品选择，新增场景沿原资格规则进入接受范围。

Author 在所属 PRD 和设计正文区分实际存在的局部确认、后台任务完成、可靠保留与最终提交。对受影响的状态或资源交接，写清须跨阶段保持的业务条件、动作顺序、实际 writer 和 reader，以及失败后的归属。原 Architecture 与 Approval 在各自职责内判断条件能否成立。技术缺口交回技术 owner。这一方法不要求额外状态、通用锁或异常 crash 协议。

来源为 #747 JQ-R1、R2 和本批适用的 R6。由 [设计 D747-D1-01](../../design/current/behavior-validation-method.md) 和 [测试 T747-D1-01](../../test/current/behavior-validation-method.md) 承接。

## R747-D2-01 / BEH747-JOURNEY-VALIDATION

当连续操作属于本次交付承诺，且入口可运行、所需依赖已就绪时，Author 在现有实施验证计划中优先安排交付范围内的一条最小完整正常旅程。实施负责人先取得该旅程的反馈，再补有独立价值的参数覆盖。如果一个函数、API 或 CLI 入口足以观察交付结果，就采用该层级。高风险下层行为可以先定向验证。测试和实现的先后按实际风险、成本和条件决定。设备或全链验证仅在交付承诺需要时采用。依赖缺失时，推进独立工作并说明哪些结论仍待验证。旅程通过后继续完成必要验收和受影响回归。

## R747-D2-02 / BEH747-EVIDENCE-BOUNDARY

原审核负责人核对证据实际经过的入口、动作和可观察结果。直接调用仅证明它实际执行的层级。替身保留当前结论依赖的真实适配器语义，包括适用的对象身份、异步完成、恢复、地址更新、缓存或解码就绪。按实际接受范围和目标交付组件选择样本。容器名、开发机能力或单一样本不能证明整个支持范围。未知能力由原负责人核实。

原独立审核负责人先按既有读取顺序从其适用来源推导问题，再核对候选和实施说明。沿用正常场景资格与证据复用规则。把验证顺序写入所属实施计划。结果只记实际覆盖、受影响需补验、失败和未执行的必要范围。保留历史观察。

来源为 #747 JQ-R3、R4 和本批适用的 R5、R6。对应 [D747-D2-01 和 D747-D2-02](../../design/current/behavior-validation-method.md) 及 [T747-D2-01 至 T747-D2-03](../../test/current/behavior-validation-method.md)。

## R826-01 / BEH826-PROJECT

来源 #826 R1/R2。原实施者从真实启动方式、入口和已有设施复用或补项目本地验证方法，说明启动、可用就绪、真实操作、可观察结果、证据及清理。只清理本轮实例和临时数据，清理后证据可读。实际跑通一条正常旅程，声明直接方法、替身及真实入口的证据层级。无UI使用真实CLI/API/库调用方；行为或入口变化后定位、更新和重跑受影响验证，不建立重复功能账本。

## R826-02 / BEH826-COMPARE

来源 #826 R3/R4/R5。原owner比较方法时事前固定问题、同任务材料和评价标准；执行Agent不接收标准、答案、优劣标签或另一侧结果。独立评价先读匿名实际输出和工具记录，原owner综合判读改善、退化和未证边界。复用既有原生入口和采集，保留最小可复核事实及首次失败，不持久化授权或敏感信息。区分环境/未执行/行为失败；充分后停止，小样本不推断普遍改善。两项方法沿原职责与分发，无新门禁。关系：D826-01/CON826-METHOD、T826-01..04。

本单元的826增量由原RDT owner在本Task实施与真实Sol medium案例验证后完成整合及回读；正式提交后独立Review与Delivery/Completion仍待各原owner，不从本文推定最终通过。
