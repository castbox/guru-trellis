# 局部修复 Intake 与一致性诊断

#819由原RDT owner在完整实施和真实工程结果后完成final_integration并读回；状态为integrated_pending_review，尚待TaskCommit及独立committed Review。固定before=4f2adef1f7b099f78bb8429e8b8facd66dce3bfc，来源与替代边界见[#819追踪](../../requirements-design-test-contributions/819-issue-review-intake/traceability.md)。以下旧观察保其原截止；本轮实际结果由[#819 Test](../../requirements-design-test-contributions/819-issue-review-intake/test.md)拥有。

导航别名：`R692/BEH692`；`局部修复 Intake 与诊断`。原知识状态：`current`（继承上述旧入口的原 current 条目，不表示实现通过）。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/requirements/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-REQ-LOCAL-FIX-INTAKE`；定义 R692-01..04 / BEH692。来源：live [Issue #692](https://github.com/castbox/guru-trellis/issues/692)，适用基线 `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`。隔离 proposed 经原最终整合后成为此完整 current 定义；精确内容由完整 Git revision 与 locator 定位。前驱有效合同为 [Task/Delivery](task-delivery-lifecycle.md)、[JSON 载体](json-input-carriers.md) 和 [知识方法](knowledge-maintenance.md)，本单元仅新增下述具体行为。

## R692-01 / BEH692-ROUTE：实际影响选路

对尚无相关 formal Task 的局部修复，原 selector 依据当前范围、受影响消费者、风险和所需验证选择现有 route。购买引导的资格或展示不自动等同价格、扣费或支付协议变更；UI 表象也不独立证明低风险。已有 Task 回其当前生命周期。高置信度有界低风险仍可按原合同自动选路；证据不足时只提出真正必要的问题。真实范围/风险变化回原 owner，不以新身份或换 mode 绕过。

## R692-02 / BEH692-REUSE：事实适用性与当前判断

草稿创建成正式 Issue 后，Create Issue 按R819-01完成正式身份/内容和评论读回。只创建的请求在原created结束；还要求开工时经原Sync进入R819-02已有Issue复核。原完整链继续服务草稿、合法no_issue及Readiness明确判断必要的全审；这些路径的Discovery仍读取真实target、base及差额并完成自己的duplicate/history、证据充分性和Gate。已完整读过且当前内容仍可用的调查事实，经当前 owner 核 revision、base 差额和目标相关性后可继续使用；不因进入下一 owner 从零广搜同一事实。旧 target pass、producer 私有结果或摘要均不能替代当前结果。

普通完整链的Clarify消费当前Discovery output；R819-03局部profile则消费Readiness的真实缺口和仍适用依据。两者都读取完整来源，先用证据解决可回答的问题。已清楚的同范围事实不重复访谈或重装配 producer 结果；仍亲自判断当前 intent、source role、disposition 与 scope。Author 以当前整体来源写 Task 要求，以已接受整体定义展开 Delivery 的目标、边界、起点、行为与验收；不重复访谈、从零调查同一代码，也不省略各自正文和方案责任。

每个原 owner 明确触发、须重读的差额、仍适用事实、须亲自重做的判断与下一 consumer。缺失完整内容、真实 source/target/base/scope 变化回最早受影响原 owner。相同范围且无新副作用的 mapped 修复自动继续；真实选择和资源、commit、发布、merge 等独立边界保持。授权仅在当前对话，不持久化。

## R692-03 / BEH692-DIAGNOSTIC：原 Discovery 入口

JSON 成功读取后，原 record/check/invoke 对当前输入、base 观察、history 和结果绑定的不一致，在确定性可判定范围定位首个实际字段或 evidence 类别。诊断说明重读对象、原恢复 owner 和支持的重入入口。原observer定义的所选来源真实失效回原Sync；固定对象来源不因无关HEAD或同名ref后来前进而自动失效。dirty/错误branch/authority缺失仍按各原profile分类，context_request目标失配保原直接错误。普通 live Issue 正文仍由 AI 完整重读，本项不新增 provider 比较。

失败仍失败，公共 input、错误 code/status、typed exit 和成功 DTO 保持。check 失败保留原 status/typed_exit/reason，并 additive 提供 `diagnostic={code,field_path,remediation}` 给当前 Discovery AI；invoke 原收窄为 blocked 的错误在 stderr 给同一诊断，stdout 保持原 DTO。原参数/schema/直接目标错误保留原 error 形状。JSON 载体或解析失败继续由原读取层诊断。

payload/result digest 差异只证明绑定不一致，不能据此断定 UTF-8 根因。重新读取完整输出后由原 Discovery 重建其最小 authoring，再经原 record/check/invoke；不局部改 digest、producer 或旧 pass。诊断不回显 expected/actual 值、正文、原始 bytes 或 OS exception。

## R692-04 / BEH692-DISTRIBUTION：职责与证据边界

AI 拥有 scope、风险、充分性和恢复判断；脚本只验证事实。canonical 原 owner 是行为来源，匹配 preset 同步 dogfood 和实际选定声明平台。已有安装保留原 managed provenance、用户修改与 sidecar 规则；源码通过不证明外部采用。公共调用图与原子能力保持，无新 Skill、跨 Skill digest authority、通用审批链或长期审计缓存。

沿正常开发、Check、独立 Review/readiness 和适用 reapply 验证；失败/SKIP/环境阻塞不作通过。业务 #372 仅为脱敏历史案例，业务代码、测试、数据、Task/会话只读；当时安装、路线、根因和净节省时间保持未知。不开专项 replay/A-B/native eval、额外安装或完整矩阵，不新增恶意篡改与并发加固范围。

关系：[D692/CON692](../../design/current/local-fix-intake.md)、[T692/SC692](../../test/current/local-fix-intake.md)。精确 canonical 调用与数据定义由 [packages](../../../trellis/skills/guru-team/packages) 单写；来源/替代边界见 [追踪](../../requirements-design-test-contributions/692-local-fix-intake/traceability.md)。

## #811 确认目标与来源关系

原R692-03的context_request目标错配仍拒绝。#811新增确认profile的目标是原Task/候选对象，source authority是独立Issue/draft；二者不能互相替换。其真实context获取、mutation刷新和旧边界迁移由REQ-811完整定义；原诊断类别与live provider比较边界保持。

完整定义见[REQ-811](qualifier-applicability.md)；本项由原 RDT owner 在 #811 final_integration 整合并读回，状态为 integrated_pending_review；独立 committed Review 尚待执行。其他R692/D692/T692行为、历史证据与未验证边界保持。

## R819-02 / BEH819-READINESS：已有Issue先行复核

模式选择和原Sync后，已有Issue由原guru-review-change-request亲自复核完整live正文、有效讨论/审核评论、必要前置交付和影响原判断的代码差额。充分且仍适用并满足前置时ready，经原router进入原Task创建；评论存在不是自动通过，没有评论也不独立阻塞。历史清楚自然语言评论不因模板、label、身份资格或期限被排除。

只有事实缺口交原Discovery；需求、范围或独立交付单位问题交原Clarify；仅措辞问题交原Wording。原覆盖不足或影响不可界定时执行必要完整Discovery→Clarify→Wording→Readiness。确认必要前置未满足、真实选择未解或必要证据无法取得时按原blocked/等待说明恢复条件，不以重跑掩盖阻塞。对应D819-02、T819-03。

## R819-03 / BEH819-SUPPLEMENT：同次返回与最早必要依赖

三个原owner以真实局部profile、必要输入和逐出口consumer进入，不要求先取得本轮完整前序receipts，也不伪造前序pass。各owner完成其适用完整方法后，将实际结果交回同一Issue、来源及continuation的Readiness。Discovery不替Readiness判断开工；Clarify确需事实时沿原context往返，结束后回判；Wording发现真实需求变化也回原需求分支。

多缺口按事实→需求→措辞的依赖顺序处理最早必要项，每次补足后由Readiness再判断剩余缺口；事实不变可直接ready，需求变化只补受影响措辞，不能进入一个局部步骤就自动串完剩余全链。旧完整链仍须真实本轮结果。对应D819-03、T819-03/04。

## R819-04 / BEH819-BOUNDARY：来源、终点与后续门禁

局部返回保真实来源kind、selected_ref、commit；固定对象read不替owner选择Task集成branch，当前Create Task只接reviewed_base_source，selected_base_ref与delivery_target分别承担原职责。保同仓commit、acquisition等值、真实同步和原成功恢复条件，完整链不反拼旧transition。只有选定来源真实失效回原Sync；会话、Agent、时间或无关HEAD变化本身不使覆盖失效。

无Issue讨论仍经原标准调查/Clarify；只讨论或草稿在对应结果结束。需要创建须完整草稿Wording/Readiness后进入R819-01创建和评论读回；只创建至created结束，还要求开工则正式Issue经Sync→先行复核。合法standalone_request/no_issue保完整原审核和Task创建，不造空Issue或评论。Task身份、checkout、分支/资源、副作用和后续规划/交付门禁保持。

公共profiles、逐出口schema、consumers、例子及恢复通过本项matching迁移和原installer同步；AI判覆盖/路线，脚本执行/校验客观事实，不增独立复核Skill、长期ledger或digest authority。对应D819-04、T819-03/04/05。完整当前定义由原RDT owner沿#819 final_integration整合，真实观察由本次Test单写；实施及验收状态不能由本条存在推出。
