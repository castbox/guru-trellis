# 需求探索与确认职责设计

Identity：`RDT-DES-DECISIONS`；定义 D-DEC-01..04 / CON-DEC。适用来源与基线同 [R-DEC](../../requirements/current/requirement-decisions.md)。精确接口与方法归原 packages/shared spec，本单元描述能力职责及其关系。

## D-DEC-01 / CON-DEC-OWNERS：原职责内探索

共享 Interaction Budget 拥有需求选择、实现细节及确认边界。Clarify 消费该规则，拥有意图、来源与范围判断，并从具体例子、受影响旧行为和适用边界发现问题；Discovery 提供事实与历史，不能替用户决定意图。Author 是唯一规划写作者；原 Wording、Architecture、Approval 和实施职责保持。

选择细化原方法而不是新增 Socratic Skill，可避免重复写作者、问题状态、审批及跨 owner 缓存。成本是原相邻提示和引用必须一致维护，并用对话验证防止“文件存在等于行为生效”的误判。若未来真实需求改变 owner/public 数据，回原流程审查，不预留接口。

## D-DEC-02 / CON-DEC-PRESENTATION / CON-DEC-ANSWER：呈现与生命周期分离

轻度独立问题可在同一消息展示推荐清单，但每项继续按原 question_id 及问题记录处理。真正不可分的产品选择才使用原 atomic_group。一次用户回答可解决多条问题，逐条记录实际答复范围，不虚构多次发言；未答不得补成 complete/refused。现有 partial 不关闭问题及 opened/closed 顺序约束不放宽。

重大或有依赖的选择逐步提出，说明可行选项和代价。普通自然语言确认与可用按钮仅为呈现通道，不创造接受状态或授权 schema。必要回答到来前不实施依赖行为，独立调查不受阻。

## D-DEC-03 / CON-DEC-RETURN：方案细化与决定承接

Author 自主研究既有要求内的实现，不向用户索取代码设计。方案展开暴露新的需求选择或重大取舍时，经已有 Clarify/Architecture 对应职责处理，不以技术命名掩盖产品含义。决定更新其所属需求、设计及验收；后续恢复复用有效决定而非重新访谈。无新出口、持久化或授权字段。

## D-DEC-04 / CON-DEC-VALIDATION：三类证据

原 recorder/checker 测试检查显式提供的逐项问题记录、内容绑定及 schema 的 partial 不关闭约束，不据此宣称自动推导全部问题生命周期；分发测试证明方法、consumer 和实际安装投影；隔离 native 对话证明其声明范围内的真实提问、选择及回答后变化。驱动只控制分轮输入和收集执行事实，后续答复及评分材料不提前暴露，语义由 AI 审核。不能用关键词命中或预写用户结论替代真实 Agent 执行。

canonical 经当前受管 preset 同步选定平台，保留用户内容与 sidecar 处理。普通 scoped 变动不自行扩张完整 Release 矩阵；已有项目升级是后续独立动作。策略与边界见 [T-DEC](../../test/current/requirement-decisions.md)，生命周期仍见 [Task/Delivery](task-delivery-lifecycle.md)。
