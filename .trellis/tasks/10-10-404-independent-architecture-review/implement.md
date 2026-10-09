# #404 实施计划

## 顺序与写入边界
任务保持 planning；本文件不表示 activation 或代码已写。每次 task/planning/source/test/artifact 写入前执行 check-task-checkout-boundary.sh --json --task 对 exact task locator 检查，所有实现只在由 TaskId/generation/control state 解析的唯一 checkout。
1. 完成三规划文件，先建立task-owned Architecture contribution与draft ADR（九concern、before/after、owner、退出、descriptor与pending committed review/promotion），再完成两项 planning qualification、planning wording、fresh independent Architecture formal wrapper 和 Planning approval。当前计划展示后由 workflow 的 Phase1 pause 承接；只有接受完整计划后才调用 guru-activate-task。
2. 进入 Phase2，读 current specs 和原文件，按 delta_first 撰写 task-owned RDT 增量。
3. 直接演进 Architecture step-local independent reviewer entry/读取顺序/职责取证方法。构造 generic fresh dispatch，审查实际平台 prelude，保证不调用自动 task narrative 注入的官方角色作为第一轮 reviewer。
4. 同步受影响 Planning/qualification/实施协调/Check/Branch Review/Delivery/Completion consumer。workflow只 routing，platform只加载调度；保持现有 profiles/exits/schema/promotion。不复制 constitution/quality 文本，不新增 wrapper/ledger/授权存储。
5. 演进现有 native eval staging 与 execution 边界，删除同一 Agent 自填 Architecture/预载通过叙事作为独立证明的旧路径；fixture保持真实设计/source/default/consumer/约束。先运行 objective regression，再真实 native dispatch/semantic 行为验收。
6. 同步三 README、canonical workflow 与 preset managed copies。apply/reapply，逐个处理本次 .new/.bak，运行 source/installed/ownership/drift。保留未知本地修改，冲突走现有停止路径。
7. 独立 Architecture 判断决定必要 contribution/ADR；依既有 Architecture/RDT owner 完成 reviewed promotion，最终 Phase2 check 前完成 delta reconciliation。promotion 新 diff 重新 fresh Phase2/commit/full BranchReview。
8. Phase2 新 reviewer 先 Architecture formal wrapper，随后完整 guru-check-task；如共用 worker，只有专项完成后才允许读 task叙事。任何 out-of-plan 候选只报告事实/locator/reproduction hint，在扩展写入/测试/severity前运行既有 qualification。
9. 取得 passed 后按精确 commit write set 停止展示。确认后的 TaskCommit 结果进入新 fresh independent committed Architecture + 完整 BranchReview，发现修订返回 Phase2/commit/full review，不以旧 pass 延续。
10. Delivery readiness、push/PR、merge、whole-task Completion、Issue Closure、Finish/bookkeeping、Cleanup 依既有 owners 与各自副作用边界执行。Delivery/Finish PR只 Refs #404，Closure 单独处理 exact source，不让 PR merge 隐含完成或关闭。

## 验证执行与缺陷检测
- A404-01/02：去敏真实 source/full diff 与未改 caller 的 native reviewer 用例；观察实际读取与职责/default影响判断。破坏消费者取证或换成叙事 pass 时行为评测必须失败。
- A404-03：必要局部迁移/旧路径退出与无关历史债务对照；观察必要调整保留、无关 work停止和 hack拒绝。
- A404-04/05：红测因果与未归因、合法非默认配置/保护不变量/诊断缺失。观察有限调查与各现有回程，不靠 fixture固定值、全量绿或超时调整证明。
- A404-06/07：Planning/discovery/Phase2/committed四阶段真实 fresh dispatch；先 authority再真实候选/consumer/约束，独立判断后才读解释。无候选、task独有约束最小取证、普通主会话自填wrapper路径都有真实执行证据；后者不能算独立评估。
- A404-08：fresh worker先专项再整体，已叙事暴露/参与实现worker改派fresh，no-impact真正评估并无无谓artifact。观察各 formal results，不能只看worker id。
- A404-09：正常 missing/unfinished/mismatch/unavailable、stale/new candidate/current downstream/promotion。实际 caller消费真实 exits，验证唯一 consumer，不用手工篡改artifact/hash。
- A404-10：source/installed package checker、workflow graph、preset apply/reapply、dogfood drift、upstream ownership、recursive zero sidecar与descriptor-selected平台投影。真实 native执行的平台与只做投影的平台明确分开。

按实际编辑选择 affected package unittest/runtime eval tests，run-skill-evals 的目标 case 和 existing semantic grading；路径/参数先从 current --help/interface读取，不猜 wrapper input。Native不可用、缺必要约束或结果未通过时保留 evidence_pending/blocked，不能以mock/字符串/schema代替accepted行为。
最多一个确有必要的 representative clean throwaway，不运行完整累计 matrix；不更改官方全局/npm/node_modules、业务repo或生产。新发现的共享 owner/public I/O/compatibility需求回Planning qualification，不能自动扩写。
触及非generated源码超过3000行时先按现有合同机械拆分/小解耦，必要性由原owner审查，不借此全仓重构。

## 交付策略与文档归属
唯一 Delivery 覆盖全部 R404-01..08；不存在需 #382/#383/#464 先完成的隐藏 remaining work。native行为/必要投影证据缺失保持当前任务未完成。Release matrix、真实业务部署和未执行平台native不是本Task的验收扩张，但报告边界。
RDT贡献中的Test记录本次唯一验证结论并由其它文档引用；Architecture贡献只在独立评估实际要求时写入，promotion由既有owner。Gate/qualification保持最小current对话或owner-private短期结果，不写审计清单/任务叙事transcript/授权记录。
