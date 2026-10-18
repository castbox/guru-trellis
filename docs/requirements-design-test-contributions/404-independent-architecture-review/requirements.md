# #404 Requirements 增量

状态：RDT 合同已晋升至 `current-main-0.6.17-guru.78`，实际实现与后续 gates 只由唯一 [Test](./test.md)记录。Source：[Issue #404](https://github.com/castbox/guru-trellis/issues/404)，合同版本 `2026-10-09-r4`；晋升来源为 RDT `.77`；current RDT 与 Architecture 均为 `current-main-0.6.17-guru.78` / `active`。本增量承接任务中的 `R404-01..08`，不替代 live Issue、项目 Constitution 或 Architecture authority。

| Requirement | Source 接点与要求 |
| --- | --- |
| R404-01 | §4.2.1、§8：Planning、实际触发的 discovery、完整 tracked/untracked Phase2 和 exact committed Branch Review 的新架构结论由真实 fresh independent subagent 形成；no-impact 同样评估。 |
| R404-02 | §4.2、§4.3：先从 current authority、真实候选、实际消费者和必要约束形成判断，再核对解释；第一轮不预载任务完成叙事，仅取必要任务约束事实与来源。 |
| R404-03 | §4.1、§4.4、§5：依据实际职责、共享 default、状态装配和未修改的消费者分析因果；区分既有偏离与新增/恶化，承担必要局部收敛。 |
| R404-04 | §2、§6：扩展写入、测试、severity 或修复路由前分别判断问题成立、当前必要与机制合适；完整承担必要重构、调用方适配和旧路径退出，不自动接管独立债务。 |
| R404-05 | §7：红测有限归因；保持合法非默认配置和已有保护不变量，诊断缺失不新增业务拒绝；质量规范由原 authority 独占。 |
| R404-06 | §4.2.1–4.2.2：reviewer 自己执行 semantic authoring 与 formal wrapper；主会话消费真实结果。fresh worker 可先专项后整体，两项责任与结果分别成立。 |
| R404-07 | §8：missing/unfinished/mismatch/unavailable、stale、新候选及 promotion 走已有唯一 consumer；Delivery/Completion 消费 current 结论和 eligibility，Branch Review 独立重算。 |
| R404-08 | 行为验收、§9：canonical、dogfood、installed 与声明平台一致；实际派发、读取、判断、停止及接续的行为证据不能由静态校验代替。 |

一个 Delivery 完整覆盖上述增量。#382、#383、#464 的独立目标、#466/#477 的既有 authority、业务仓修复、生产写入与完整累计 Release 矩阵保持各自边界。结果只由 [Test](./test.md) 持有；双向关系见 [traceability](./traceability.md)。
