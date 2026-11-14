# 局部修复 Intake 与一致性诊断测试策略

#819由原RDT owner在完整实施和真实工程结果后完成final_integration并读回；状态为integrated_pending_review，尚待TaskCommit及独立committed Review。固定before=4f2adef1f7b099f78bb8429e8b8facd66dce3bfc，来源与替代边界见[#819追踪](../../requirements-design-test-contributions/819-issue-review-intake/traceability.md)。以下旧观察保其原截止；本轮实际结果由[#819 Test](../../requirements-design-test-contributions/819-issue-review-intake/test.md)拥有。

导航别名：`局部修复 Intake 与诊断`。原知识状态：`current`（继承上述旧入口的原 current 条目，不表示实现通过）。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/test/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-TST-LOCAL-FIX-INTAKE`；T692/SC692；适用基线 `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`。完整 current 定义在原 final_integration 后生效；精确内容由 Git revision 与 locator 定位。要求：[R692/BEH692](../../requirements/current/local-fix-intake.md)；设计：[D692/CON692](../../design/current/local-fix-intake.md)。实际命令、首次失败及恢复唯一由 [#692 Test](../../requirements-design-test-contributions/692-local-fix-intake/test.md) 拥有，本文不预告通过。

| Identity 与关系 | 正常输入/原入口 | 必须观察与证明边界 |
| --- | --- | --- |
| T692-01 / SC692-ROUTE/REUSE；R692-01/02→D692-01 | 原 Check/独立 Review 读取 selector、Create Issue、Discovery、Clarify、Author 的真实完整差额及未改消费者 | 购买提示与支付核心按实际影响区分；触发、当前重读、仍适用调查事实、亲自重审及下一 consumer 明确。保真实Sync来源、正式完整正文、声明graph及原owner门禁；#819已有Issue可先行复核和按缺口返回，必要完整链仍核真实前序，具体减少重复广搜/访谈/装配。文案存在不能证明普遍 Agent 效果，不新增专项或计时。 |
| T692-02 / SC692-BINDING；R692-03→D692-02/03 | Discovery 现有 runtime/test_contract 和真实 record/check/invoke wrappers；workflow/standalone 由真实 recorder 分别产生合法结果后普通配错；中文结果逐块错误解码与完整解码对照 | 具体字段/evidence 诊断到当前 AI；失败仍拒绝，check 原字段保留，invoke stdout DTO 不变而 stderr 三字段可读。一致结果保正常成功；digest 差异不被宣称 UTF-8 根因，无正文/值/字节泄露。不得手改 hash/state 制造攻击用例。 |
| T692-03 / SC692-CHANGE；R692-03/04→D692-02/03 | 现有正常 base 前进、authority dirty、错误 branch 及 context_request 目标错配场景 | 原 classification、code/status、字段及直接错误形状保持；恢复说明指到原 Sync 或当前 Discovery/Clarify 支持入口。JSON 读取错误归原层，live body 无新增自动比较，未触及类别不假称通过。 |
| T692-04 / SC692-INSTALL；R692-04→D692-04 | 原 source/installed package validators、完整 apply/reapply、dogfood drift、实际声明平台投影 bytes/mode、递归 sidecar 和基础语法/JSON/Bash/Task/diff | 源码、实际 installed 与选择平台分开验证；继承基线 #706 投影不计 #692 新成果。保原 provenance/用户修改，失败沿原 owner 恢复，不手改 hash 或扩大矩阵。 |
| T692-05 / SC692-QUALITY；全部 R692→全部 D692 | 原 candidate/begin_check、独立 Architecture phase2、完整 candidate Check→原 RDT final_integration/readback→实际 after 重绑→final Check→独立 committed Review/readiness | candidate_ready/candidate_checked 不等最终通过；实际正文/关系/导航与未改 consumer 完整覆盖。后续 commit/publish/merge/Completion/Closure/Finish 各自保原责任；局部测试不代替整体终态。 |

原#692定向测试及观察只证明其当时字段/consumer。#819当前新增入口/评论行为由T819策略另行验证；不从旧测试推断新路径通过。不增加固定数量、耗时或完整多平台矩阵，实际Agent观察不扩为新评测系统。failed/SKIP/环境缺失分别记录。业务现场、当时安装/原会话、运行时根因、实际净节省时间、外部采用与完整 Release 边界保留未知/未验证。前驱策略为 [生命周期](task-delivery-lifecycle.md)、[JSON 载体](json-input-carriers.md)、[知识方法](knowledge-maintenance.md)，其原责任与历史结果不由本项重写。

## #811 确认目标与来源关系

原T692-03的target mismatch观察继续适用于其原对象。新增两确认的Task/authority分离、snapshot与mutation返回由TST-811验证；T692-05的原#692阶段顺序保历史来源，当前#811的执行前提由TST-811-06及原lifecycle合同承接，不恢复退休Check。

完整定义见[TST-811](qualifier-applicability.md)；本项由原 RDT owner 在 #811 final_integration 整合并读回，状态为 integrated_pending_review；独立 committed Review 尚待执行。其他R692/D692/T692行为、历史证据与未验证边界保持。

## T819-03 / SC819-ROUTE：实际分流与终点

从原已有Issue→Sync→Readiness入口，观察直接ready、事实/需求/措辞局部补审、必要完整链、真实阻塞/恢复及多缺口最早依赖。局部实际producer必须返回同次Readiness；事实不变不自动补Clarify/Wording，需求变化只补失效措辞。另观察讨论/草稿/只创建/创建并开工及原no_issue边界。实际AI判断和完整答复单独验证，机械出口或文案存在不代替它。对应R819-02/03/04、D819-02/03/04。

## T819-04 / SC819-SOURCE：真实producer到当前Creation

生产Sync read/sync输出经本项新入口、局部/Clarify事实/刷新往返及ready进入当前Create Task2.0/creation3.0。观察完整来源三字段、独立集成目标、精确commit/acquisition及原同步/恢复条件；固定对象不因local main后来前进误判。必要完整链保实际transition；fixture只建立测试边界外的合法先决，不修被测producer结果或直接造supplemented。复用#813仍适用内部覆盖，补实际新桥接。对应R819-03/04、D819-03/04。

## T819-05 / SC819-DISTRIBUTION：matching采用

按真实受影响package/runtime、public graph/例子、原tools更新、installed/native、reapply、声明平台、drift、mode、sidecar及Task/session/用户保持提供证据。源码、目标采用、实际AI和GitHub外部效果分别报告；不扩完整多平台Release矩阵。对应R819-04、D819-04；评论分发关系见issue-content的T819-01/02。

本次真实结果唯一由[#819 Test](../../requirements-design-test-contributions/819-issue-review-intake/test.md)维护；当前提案不预填实现、工程、Agent、GitHub或安装通过。#692/#811的历史观察不改写，当前执行时机仍读原质量合同。
