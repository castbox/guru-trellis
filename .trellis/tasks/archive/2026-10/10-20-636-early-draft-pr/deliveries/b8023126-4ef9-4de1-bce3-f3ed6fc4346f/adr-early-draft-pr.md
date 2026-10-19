# ADR 候选：由原 owners 提前提供 Draft 反馈

状态：proposed，归属Task #636 / D1；不是当前共享ADR。编号和共享导航由原Architecture晋升owner在实际评估后分配。

## 背景与决策

现行所有TaskCommit依赖完整Check、Publication消费readiness并最终Ready，延后远端反馈。#636要求在最小自检后真实提交/发布Draft，并在最终审核前更新冲突解决或修订候选。选择直接演进TaskCommit/Publication，不增加第二commit/publish owner。

早期提交采用独立闭合input/exit和有界AI内容、精确staging、敏感检查、真实hook事务；不伪造Check。Publication在同事务内区分Draft与Ready，Ready修订先退Draft再push。Draft仅是反馈结果，不写最终PublicationFact。独立内容分析与风险验证在固定B/H并行；正式full_review仍以真实Check为predecessor，最终Ready/Merge不继承早期pass。

## 替代范围与保留

窄替代ADR-024及current生命周期中将全部提交/远端PR动作统一放在完整Check/readiness之后的时机片段。保留ADR-024的上游Task/Delivery身份、stage ownership、refs-only/Closure与public gate chain；保留ADR-028固定内容/阶段适用性和ADR-030晋升顺序。最终语义仍由原owner判断。未选择单独Draft发布器、第二账本、upstream phase扩展或跨阶段Review缓存。

## 影响与验证

同步public profile/schema/consumer、workflow、platform/preset与在途迁移；旧最终profiles语义保持。一次性迁移先恢复已执行事实，不制造pass或remote动作；matching成套切换后旧current输入退出，无双读。验收按design V636-01..07，真实远端/Agent结果与fixture分开。完整Release矩阵、#637/#638和BackendCI不在本决策范围。
