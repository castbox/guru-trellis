# #396 draft Intake 调用构造与同范围恢复

## Authority 与目标
Direct Source：[castbox/guru-trellis#396](https://github.com/castbox/guru-trellis/issues/396)，合同 2026-10-10-r1。实施前与每个语义门禁重读 live source；历史 main 3e4e91c 仅解释旧失败，不是实施基线。
本 task 从 main 00d844198009bd2f858b12b71841f2f4b5db3fc2 开始，只交付 #396。#453 已合入的 receipt/正式出口能力是复用基础；#250、#292、#521 不进入本 task。
目标是让正常 proposed_draft 经实际 Discovery、Clarification、Wording、Readiness record/check/invoke 到达实际 ready，并使 Agent 对同范围构造错误自动重建消费者输入。

## 现状、根因与证据边界
历史失败属于 Agent 消费者 authoring/recovery：自造 draft_id、混入 standalone 字段、正文 SHA 误作 authority digest、自包含 linkage、旧完整 result 局部补算，以及改写 producer transition。
最新 canonical runtime 已有 draft authority normalization、固定五字段 linkage、Gate 三项派生、identity/freshness 校验。现有 ReadinessAdapterTests.test_draft_and_standalone_source_profiles 经 managed runner 已通过；这是客观链路基线，不证明 Agent 行为或当前最小示例完整。
当前 public-proposed-draft-input.json 的 #145 与 change-request.json 的 draft 名不一致；现有 fixture 仍借助 private normalization。上述事实支持修正消费者指导与定向回放；没有证据要求改 runtime。

## Accepted requirements
| Identity | 必须观察的结果 |
| --- | --- |
| R396-01 | 真实生产 wrapper 完成 draft 链，逐步消费实际 public stdout/transition，最终实际 ready；record/check receipt 不当成正式出口。 |
| R396-02 | 未修订草案以实际 producer target_locator 作为 source.draft_id、target.draft_id、public_input.target_locator；恢复前后 producer transition 相等。 |
| R396-03 | 最小 authoring 使用完整 draft authority projection 的 canonical digest；Gate 仅写 status/reviewer/summary，省略三项 recorder 派生值；实际 record.result 替换 owner_result、实际 check.result.validation_receipt 进入 invoke。 |
| R396-04 | 回放五类误用：standalone 字段混入、body SHA、另造 draft_id、自包含 linkage、旧完整 result 局部补算；区分归一化忽略的多余字段与错误身份/摘要。 |
| R396-05 | 错误身份/摘要保持拒绝；从同一真实 source/transition 重建最小 consumer authoring 后 ready，校验不放宽。 |
| R396-06 | 正文正常修订经声明上游刷新形成新 authority；允许真实新 locator，旧摘要不能代替新内容。缺真实前序时停止或返回声明的前序恢复出口，不能制造 pass/receipt。 |
| R396-07 | 真实 Agent 运行证明同范围、无副作用纠正无需重复确认，并完成当前语义 review、实际 record/check/invoke；Python replay 单独报告。 |
| R396-08 | canonical、dogfood、installed 及声明平台一致，定向 apply/reapply、drift/hash/mode/sidecar 验证通过；测试资源隔离并清理。 |
| R396-09 | 报告历史错误、既有能力、剩余缺口与变更原因；runtime 只有独立合法输入缺陷复现后修改。 |
| R396-10 | 完整 Task gate、Delivery、Completion、Closure、Finish/Cleanup 按当前 owner 结束；真实 source Issue 完成不能由测试或 PR merge 代替。 |

## 范围与排除
修改已有 readiness Skill/contract/examples 与现有 Stage0 fixture/native replay 接续；公共 ids、schemas、profiles、typed exits、atomic capabilities 和十维 AI 判断保持。
不修 gitlink/index_tree_digest、不改业务 W2/Process Analytics/依赖/子模块、不新增 wrapper Skill、长期输入缓存、授权记录、审批链或第二 owner。
不引入恶意输入、故意伪造、并发压力、TOCTOU、锁、crash hardening；历史正常误调用的回放不是攻击模型。
完整多平台 Release matrix、软件发布、业务安装/部署与后续 Issue 均是独立未验证边界。

## Docs SSOT Plan
strategy：ssot_first。步骤内部合同只在 trellis/skills/guru-team/packages/guru-review-change-request/references/contract.md 定义；SKILL.md 提供入口/加载，examples 给出可运行 shape 与 producer 字段消费。workflow 与平台入口不复制局部恢复算法。
通过 guru-maintain-requirements-design-test-ssot:task_impact_sync 判断 #396 isolated contribution 与现有 authority 的关系；新增增量使用 docs/requirements-design-test-contributions/396-draft-intake-recovery/，R396 -> D396 -> T396，真实结果只由 test.md 拥有，其他 docs 引用它，不复制 transcript。
shared current 的任何晋升由既有 owner 串行执行，晋升 diff 重跑 Phase2、Task Commit 与完整 Branch Review。Architecture contribution/ADR 由独立 Architecture owner 判定；no impact 不产生形式化 contribution。
现有合同里正确的 derivation/normalization 不重新认领；不回写历史 archive 或前驱版本。没有 public I/O 迁移需求，不新增兼容双读。

## Delivery policy
一个完整 Delivery 覆盖 R396-01..09：指导、可执行示例、五误用/刷新/缺前序回放、真实 Agent 恢复及 distribution 证据共同交付，不拆出只改文案的完成声明。
remaining work：该 Delivery 之外无隐藏实现；R396-10 由当前 Task 的生命周期 owners 承接。交付前完成自身客观与 Agent 验收；merge 后仍由 Completion 审查全 scope，再 Closure/Finish/Cleanup。
当前 planning 不声明实施、Agent 验收、Phase2、Branch Review、Delivery 或 Closure 已通过。
