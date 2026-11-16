# #868 完整责任提案

状态integrated_pending_review；来源为[#868](https://github.com/castbox/guru-trellis/issues/868)当前完整正文。适用前驱Git b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec；保留当前完整单元的其他责任、原观察截止及稳定身份，只提出已变定义。

## R868-01 / BEH868-BOUNDARY：Issue结果与边界

原Clarify从有效来源确定目标、消费者、自身可独立交付及验证的边界，再在边界内最外沿有效切面表达必要结果。API、CLI、workflow、文档、代码、配置、协议或数据状态均为合法交付。候选分成结果、支撑证据和无依据扩张；能映射目标不证明有独立验收价值。删除后不影响必要承诺判断的条目合并或删除，不固定条数、一目标一条或多义务挤一条。必要失败、安全、兼容和规范性技术承诺仍保留。唯一内容方法由Clarify-owned issue-content承载，跨阶段验证只引用原quality-guidelines。对应D868-01、T868-01。

## R868-02 / BEH868-PREWRITE：所有创建入口首次写前

受支持Agent创建入口不因Task、阶段、Issue-only或草稿来源豁免。原Clarify、Readiness和Create Issue在各自门禁实际判断最终完整正文；上游通过、现成草稿与创建意图不能替代。未合理精简先沿原owner回程，修订通过前不创建，不先创建后补救。实质变化刷新直接受影响判断，执行器仍原文提交；成功后的输出丢失恢复原对象。对应D868-01/02、T868-01/02/04。

## R868-03 / BEH868-CONTINUING：每轮审核及正文写回

所有相关原写作/审核owner在本轮输出前按共同验证方法判断拟新增、恢复或强化义务；无依据或重复候选不能成为Finding、风险、返工、依赖、强制follow-up或gate，不改名或转移。每次写回前核完整postimage及受影响安排。模式、阶段、换Agent或恢复会话不豁免；真实原范围缺陷与失效证据仍定向修复，真正范围变化回Clarify。对应D868-02、T868-02。

## R868-04 / BEH868-EVIDENCE：共用最小充分证据

各原owner在accepted responsibility内选择最外沿有效观察，不沿调用链追到消费方接入、E2E、生产采用或联合验收。仅在有效需求包含联合交付，或自身承诺须经集成证明时保留最小相应验证，指出承诺与现有证据缺口。外沿充分证据已覆盖时不逐层复制单元/集成/E2E/联合验收；内部明确条件缺口只补定向证据。替身只隔离边界外依赖，不制造被测组件结果。对象/版本、条件、路径和结论仍适用的证据复用，阶段、reviewer或信心变化不要求重跑。原owner独立判断当前充分性。唯一跨阶段方法为quality-guidelines Test And Validation Value，共同review-sufficiency薄引用，不新建表/账本/阶段。对应D868-03、T868-02/03。
