# ADR-019：独立 Architecture 评估与下游 eligibility

- 状态：`accepted`；来源：#404 `implementation-v2` contribution 与 task-owned ADR candidate。
- predecessor：ADR-005 的贡献/审查/promotion 生命周期继续有效；本条补充评估执行边界，不 supersede 其 owner 或公共合同。

## Decision

Architecture Skill 独占 step-local reviewer 方法；Planning、适用 implementation discovery、Phase2 与 committed Branch Review 的新结论由 fresh、未参与候选编写/实现、第一轮未暴露任务通过叙事的 generic subagent 执行。reviewer 先读取 current constitution、baseline、change contract、实际候选、受影响消费者和必要约束，形成独立判断后才核对解释；自行执行适用 project checks、author semantic result 并调用原 formal wrapper。

一个合规 fresh worker 可先完成 Architecture，再读取任务叙事执行整体 Check/Branch Review；两个 Skill 的判断和实际 DTO 分开。已参与实现或先读叙事的 worker 不能回溯声称首轮独立；no-impact 仍须判断，但不制造 contribution/ADR。合规执行不可用或结果未完成/不匹配时沿既有 blocked/re-entry，不退回主会话自评。

publication/acceptance_finish 继续由原 Architecture owner 消费仍适用的独立结论、当前 authority/candidate/committed review/promotion facts，执行 matching-stage eligibility；不因 caller 改变重复同质评估，不 relabel 上游 DTO。改变结论的新事实返回对应 fresh assessment，shared-current promotion 继续 expected-current-bound 单写，晋升 diff 必须重新 fresh Phase2/commit/完整 Branch Review。

## Alternatives and consequences

不新增 Skill、审批链、reviewer ledger、公共 reviewer 字段或脚本判断。平台入口只加载/调度，workflow 只 mandatory invocation 与跨 Skill route，原 2.0 I/O、四 profiles、七 exits、constitution、GAP lifecycle 和整体 gate owners 不变。必要局部收敛与无关历史债务依因果分开；发现不授权修复或扩大验收。

真实 native 行为与风险匹配验证由 [唯一 Test](../../requirements-design-test-contributions/404-independent-architecture-review/test.md)拥有；知识晋升不证明后续 gates、Delivery/Completion、完整矩阵、软件发布或生产部署。
