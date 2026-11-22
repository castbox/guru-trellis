# 行为测试与因果验证方法的职责设计

Identity：RDT-DES-BEHAVIOR-VALIDATION；别名：D735/CON735。原语义 owner：guru-maintain-requirements-design-test-ssot。来源：Issue #735；状态 current。变更起点 main@b78edbbdc32e77392bc3775366473971050ccb4b；精确当前定义由包含本文件的 Git revision 绑定。晋升依据：原 candidate_checked 后，原 RDT owner 完成 final integration 写入与读回；不预填最终质量或交付结论。

## D735-01 / CON735-METHOD

承接R735-01/03。quality-guidelines Test And Validation Value 单写通用验证方法，Author planning-body 和 design/implement 原验证章节加载并应用；Phase2 派工、Check/Branch 原职责引用同一正文，避免复制第二套标准。确定性 runner 只运输事实和采集输入/工具/输出，AI 判断行为与证据边界。

## D735-02 / CON735-ADMISSION

承接R735-02。guru-qualify-root-cause 在原修复候选条款区分证据充分性与实验形式，并保留普通功能、诊断、缓解、修复、保护的原分类。没有新状态/字段；原阶段 owner 依据实际结果判断完成。共用 causal-completion-semantics 的证据维度不复制到本单元。

## D735-03 / CON735-ADOPTION

承接R735-03。沿现有 package/spec/preset 和 tools maintenance 分发完整 canonical/dogfood/installed 与实际声明平台。工具维护保留 Task/session；不手工覆盖受管副本。真实语义观察与结构、分发和正式交付证据分别报告。单一方法增量的维护成本为原正文/引用和定向评估，不引入固定重跑、时间限额、理由文件或兼容双读。来源行为、证据需要或原owner变更时重新判断影响。

## 关系

需求：docs/requirements/current/behavior-validation-method.md R735-01..03；测试：docs/test/current/behavior-validation-method.md T735-01..07。Architecture 当前 no impact 使用原独立结果，不制造贡献/ADR。quality/root/Author canonical 精确合同保持唯一来源。

## #868 本次整合与关系

原RDT owner在批准规划、实际实现及真实工程结果后，于固定前驱Git `b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec` 的Task隔离checkout完成final_integration和读回。状态为`integrated_pending_review`，尚待TaskCommit及独立committed Review；不产生质量或Completion通过。来源和替代范围见[#868追踪](../../requirements-design-test-contributions/868-issue-acceptance-boundary/traceability.md)。既有来源、完整条件及旧观察截止保持。

## D868-03 / CON868-VALIDATION：共用验证及实际观察

承接R868-04。quality-guidelines Test And Validation Value单写跨阶段边界、停止外推、去重、复用与每轮必要性；review-sufficiency在原覆盖职责中实际加载，不复制规则。现有native eval确定性公开方法投影补齐Skill必读正文及传递依赖，隔离预期和私有runtime；不扩flow状态机/命令/生产schema，不替代AI判断。维护事实case及transport测试；关键创建/修订由匹配原Skill真实会话另行观察。对应T868-02/03/04。

对应[R868-04](../../requirements/current/behavior-validation-method.md)、[T868-03及关联观察](../../test/current/behavior-validation-method.md)；Issue原入口D868-01/02见[Issue内容设计](issue-content.md)。

## D880-02 / CON880-ENVIRONMENT：跨阶段边界落点

承接 R880-02/03。`quality-guidelines.md#test-and-validation-value` 在原责任边界段区分服务版本部署、共享 test 部署、目标环境执行和业务发布配置，不复制 Issue 专属场景集合定义。`issue-content.md` 继续拥有 Issue 结果、证据、责任层和场景集合；review-sufficiency 只按原职责加载跨阶段方法，不新增环境 Gate、证明表或部署 owner。

## D747-D1-01 / CON747-JOURNEY

承接 R747-D1-01。Clarify 的 `references/contract.md` 在 Discover the actual choices 承接连续动作与可见结果。Author 的 `references/planning-body.md` 第 3 节承接阶段语义和资源交接。PRD 定义适用阶段与可见行为。Design 定义实际 writer、reader、交接前后保持的条件、动作顺序与失败归属。设计以候选的真实交接步骤为核对对象。原 Architecture 和 Approval 在既有职责内检查交接条件，按原修订路线处理缺口。

沿原 Markdown 和受管分发入口送达。去敏示例说明怎样从中性事实推导，期待结果由观察方单独持有。变更在原正文落地，保留简单任务按需裁剪。独立审核的读取方法见 [D747-D1-02](review-sufficiency.md)。测试见 [T747-D1-01](../../test/current/behavior-validation-method.md)。

## D747-D2-01 / CON747-JOURNEY-VALIDATION

承接 R747-D2-01。共用 quality-guidelines 的 Test And Validation Value 中，Behavior, evidence and experiment selection 是验证顺序的唯一方法正文。Author 实施模板引用此节。原 Phase 2 派工读取同一方法，实施负责人在已有 implement 正文安排可执行的验证顺序。计划写清当前承诺、可运行入口、依赖和要观察的结果。定向下层检查、依赖未就绪、单一入口足以观察和必要验收回归等条件沿共用方法判断。

## D747-D2-02 / CON747-EVIDENCE-BOUNDARY

承接 R747-D2-02。共用方法要求原审核者观察实际进入的路径和产生的结果，并把结论限制在实际触达范围。比较替身差异时，只追踪当前验收依赖的语义。样本覆盖按已接受范围和目标构建的实际能力判断。共用审核规范的独立推导、读取顺序和证据复用仍按原职责执行。Architecture 的职责连接见对应域。去敏示例扩展手势、异步、媒体样本和简单 API 裁剪，真实观察使用分开的中性材料。分发沿既有 managed-spec 和 Author package。

对应 [R747-D2-01 和 R747-D2-02](../../requirements/current/behavior-validation-method.md) 及 [T747-D2-01 至 T747-D2-03](../../test/current/behavior-validation-method.md)。

## D826-01 / CON826-METHOD

承接R826-01/02。唯一生产正文仍为quality-guidelines Test And Validation Value下项目验证与维护、真实Agent对照方法；Author/实施/Review按原职责消费，同源引用不复制标准。项目本地说明服从已有约定，真实执行和维护证明可用。实验host持标准和映射，执行者只读自然任务与对应方法，匿名评价先于揭示映射；工具只运输事实，原owner判断。复用原生入口/采集及受管分发，不新增Skill、runtime、DTO、总控或评分器。规则变化只重验实际受影响范围。关系：R826-01/02，T826-01..04。

本单元的826增量由原RDT owner在本Task实施与真实Sol medium案例验证后完成整合及回读；正式提交后独立Review与Delivery/Completion仍待各原owner，不从本文推定最终通过。
