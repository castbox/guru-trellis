# 局部修复 Intake 的 owner 与诊断设计

#819由原RDT owner在完整实施和真实工程结果后完成final_integration并读回；状态为integrated_pending_review，尚待TaskCommit及独立committed Review。固定before=4f2adef1f7b099f78bb8429e8b8facd66dce3bfc，来源与替代边界见[#819追踪](../../requirements-design-test-contributions/819-issue-review-intake/traceability.md)。以下旧观察保其原截止；本轮实际结果由[#819 Test](../../requirements-design-test-contributions/819-issue-review-intake/test.md)拥有。

导航别名：`局部修复 Intake 与诊断`。原知识状态：`current`（继承上述旧入口的原 current 条目，不表示实现通过）。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/design/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-DES-LOCAL-FIX-INTAKE`；D692/CON692；适用基线 `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`。本完整单元在原 final_integration 后为 current；精确内容由 Git revision 与 locator 定位。需求：[R692/BEH692](../../requirements/current/local-fix-intake.md)；测试：[T692/SC692](../../test/current/local-fix-intake.md)。原 [生命周期](task-delivery-lifecycle.md)、[JSON 载体](json-input-carriers.md) 和 [知识方法](knowledge-maintenance.md) 的通用职责保持。

## D692-01 / CON692-OWNERS：保留调用图，在原 owner 内减少重复

selector依据实际行为影响选择原route。Create Issue完成D819-01正式内容/评论读回后，仅创建在created结束；还要开工则交原Sync，再由D819-02 Readiness先行。必要完整链中的Discovery仍核新身份、完整live正文、当前base及事实差额，并亲自完成适用duplicate/history和充分性；D819-03局部调查只补真实指明缺口并回同次Readiness。两者都不重复广搜仍适用完整内容，created不携带调查缓存。

普通完整链Clarify使用当前Discovery public output；局部Clarify采用D819-03真实缺口/返回合同。两者都读可核验完整来源，自行判断intent、role、disposition、scope，不借读producer私有结果，不重复询问证据已回答的问题。Author 依现有模板区分整体要求、本批要求、design 与 implement，复用已接受定义的必要引用，完成当前正文责任；来源处置仅在 design 唯一位置维护。Wording、独立 Architecture、Approval、展示接受与 Activation 顺序保持，各阶段仍作自己的判断。真实事实失效回原 producer/最早 owner；同源普通装配恢复不新增确认。

事实复用仍在原step-local Markdown完成，不新增恢复层、跨Skill capsule或统一缓存。#819已按其实际规划改变已有Issue入口、局部public I/O及评论恢复；这些新责任由D819单写，不能把原#692的固定调用图当作新profile的前置。其余调用图/接口变化仍回原规划及迁移合同。

## D692-02 / CON692-BINDING：拆分已有确定性比较

Discovery `runtime/common.py` 在现有等价判断中定位首个差异。mode、change_input、base_observation、history_preview 和 result_identity 分开检查；嵌套对象/数组指到实际差异键/位置，派生摘要只能指到其绑定字段。base observer 保持 `current/refresh_base/blocked` 及原错误 code/status，只细化 mode/repository/selected-base/branch/ref 的字段与原 Sync 恢复说明。

context_request 目标失配保持 `stale_identity` 和 `return_identity.target_locator`，回原 Discovery/Clarify 的当前目标入口。pre_task 不增加固定目标比较；live body 没有新 provider 自动校验。JSON 读取先由原 shared reader 完成，不把载体/语法错误改称身份失配。

## D692-03 / CON692-ERROR：把诊断交给当前调用者

record 保留原 CommandError。check 的失败 receipt 保留 status/typed_exit/reason，仅 additive 放入三字段 diagnostic。invoke 在原被收窄为 blocked 的分支将三字段写 stderr，stdout 保留原唯一 typed DTO；成功/refresh 和原直接参数/schema/目标错误均保原形状。直接 consumer 是当前 Discovery AI，无新 public DTO、独立状态、持久诊断或跨 owner authority。

字段/恢复文本只含固定位置和操作说明，不输出正文、expected/actual 值、bytes 或 exception。读取命令输出时捕获完整 bytes 后一次解码，或用保持边界的 streaming decoder；绑定失配不证明某一种根因。当前 owner 重读实际 public input、Sync transition、history 与完整输出后重建最小 authoring，再原 record→check→invoke；不补改派生 digest、producer 或旧 pass。

## D692-04 / CON692-DISTRIBUTION：受管传播与质量责任

现有 canonical packages、commands/errors、README 定位与实际 consumers 同批演进，通过原完整 preset 同步 dogfood/选定平台。apply/reapply、source/installed、drift、mode 与 sidecar 证明本 checkout 的实际采用，外部安装和完整升级/Release 矩阵分别保留边界。无业务 API/数据/支付迁移，无新安装要求；Architecture 无影响时不造空 ADR。

原#692的candidate Check时机保留为其历史观察。当前执行按项目现有质量合同：原RDT/Architecture owners在完整实施和工程结果后final_integration整合/readback，TaskCommit纳入全部after，固定B/H的同一次独立committed Review承担Architecture及完整Check/Review；本单元不恢复已退休提交前candidate Check。测试策略与实际结果保持各自单一来源。来源见 [追踪](../../requirements-design-test-contributions/692-local-fix-intake/traceability.md)，精确参数/接口仍由 [canonical packages](../../../trellis/skills/guru-team/packages) 独占。

## #811 确认目标与来源关系

原D692-02的直接target mismatch仍保原错误；新增资格确认分别校确认target与实际authority，按DES-811通过真实producer返回。原#692质量时序保其历史观察；当前#811采用工程完成后提交前整合/readback、TaskCommit后一次独立完整Review，不以旧candidate Check作为新前置。

完整定义见[DES-811](qualifier-applicability.md)；本项由原 RDT owner 在 #811 final_integration 整合并读回，状态为 integrated_pending_review；独立 committed Review 尚待执行。其他R692/D692/T692行为、历史证据与未验证边界保持。

## D819-02 / CON819-READINESS：原owner先行与逐出口

原workflow在Sync后薄路由：明确已有Issue进入原Readiness的existing_issue_intake，其他标准对象/原confirmation保原入口。Readiness拥有完整当前覆盖、变化影响、前置与路线的semantic判断；record/check/invoke只绑定原对象/来源/实际结论。ready仍只交原Task intake router；三个supplement、必要完整链、基线刷新和blocked各有唯一consumer。

新来源DTO保kind/selected_ref/commit。read复制真实git_object来源；实际sync将selected_base/decision_head归一为synced_branch，不从read或本地HEAD猜provenance。精确规格由canonical包及MIGRATION-819单写。对应R819-02和T819-03/04。

## D819-03 / CON819-SUPPLEMENT：原profile与同次回判

Discovery、Clarify、Wording分别拥有issue_readiness_supplement输入与真实结果。局部前置由仍适用审核和本轮事实满足，不用旧完整链transition替代。supplemented结果仅携必要对象、来源、continuation及该次结果/来源摘要，回Readiness的issue_review_return；来源kind和精确对象不丢失、不重解成集成branch。

Clarify需要上下文沿原needs_context/context_request/context_ready回原局部Clarify；结束才交Readiness。Wording保持完整标题/正文scan与保义方法，真实需求缺口回Readiness选择Clarify。各次Readiness重判必要后续，不让局部成功落入普通默认全链。缺必要真实结果回原producer，不建coverage缓存。对应R819-03和T819-03/04。

## D819-04 / CON819-BOUNDARY：消费、刷新与迁移

新ready向原Create Task当前profile2.0/共享creation3.0投影reviewed_base_source；Task集成selected_base_ref、未来delivery_target和原Issue disposition仍由原owner分别审定。精确来源commit与acquisition.decision_head等值；synced来源branch身份检查为新建/恢复共用，新建额外核local HEAD，已成功恢复不因后来ref前进失效。固定对象read不要求local main等于旧commit或primary clean。

必要全链继续消费真实Sync transition，不从最小三字段反拼摘要或前序。缺调用期结果恢复原读取/同步事实；真实基线失效由原Sync产生新事实后回判。讨论/草稿/只创建/创建并开工/no_issue保R819-04终点及全部Task后续门禁。

MIGRATION-819同步当前七包、workflow/graph、schema/Interface/consumer/examples和受管投影；原工具owner保Task/session、用户内容、mode和sidecar。旧Creation固定provider恢复沿MIGRATION-813，不转换旧pass、不重复对象、不新增长期dual-reader。对应R819-04和T819-04/05；原owner整合/readback后仍待TaskCommit及独立committed Review。
