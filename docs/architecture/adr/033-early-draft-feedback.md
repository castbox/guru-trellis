# ADR-033：由原 owners 提前提供 Draft 反馈

状态：accepted。来源：[Issue #636](https://github.com/castbox/guru-trellis/issues/636)；predecessor authority：`current-main-0.7.0-guru.103`。

## 决策与替代范围

由原TaskCommit提供独立闭合的有界早期提交输入/出口，保留精确staging、敏感检查、真实hook事务和同提交恢复；完整Check只保留为最终提交profile前置。原Publication在同PR内区分Draft反馈与最终Ready，未审新HEAD push前先确保Draft，实际PR/HEAD/payload/state支持原同操作读回恢复。Draft不写最终PublicationFact、不产生新公共phase、gate或整体完成。

Draft后独立固定B/H完整内容分析与风险验证并行，target前进不打断审核；HEAD H与组合T/M验证分开。早期分析不写或自动复用为full_review。最终仍在真实Check predecessor下fresh独立判断，完整最终质量和Merge资格保持。

本决定窄替代ADR-024/current生命周期中全部提交/PR动作统一置于完整Check/readiness之后的时机片段；保留其上游Task/Delivery身份、阶段ownership、Refs-only/Closure及公共gate chain。ARCH-GOV-008的未晋升禁止指最终readiness/Ready发布和Finish，早期Draft仅反馈；ADR-030最终Check前晋升顺序不变。ADR-028固定内容/阶段适用性、输出恢复、终态owners继续适用。

## 取舍、迁移与证据

直接演进原owners和受控consumers，不采用独立Draft发布器、第二账本、上游phase扩展或跨阶段review cache。公共profile/schema、私有事务和matching工作流/平台按MIGRATION-636成套切换；原owner先恢复实际旧动作，一次性迁移不合成pass/remote mutation，旧current入口退出而无双读。

实际源码、matching安装、Agent/GitHub反馈和未验证边界分别由 [唯一Test](../../requirements-design-test-contributions/636-early-draft-pr/test.md)拥有。知识接受、实现验证、Task完成与软件Release分开；不包含#637/#638、BackendCI/队列或完整Release矩阵。
