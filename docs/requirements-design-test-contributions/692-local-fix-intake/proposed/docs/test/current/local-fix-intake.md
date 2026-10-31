# 局部修复 Intake 与一致性诊断测试策略

Identity：`RDT-TST-LOCAL-FIX-INTAKE`；T692/SC692；适用基线 `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`。完整 current 定义在原 final_integration 后生效；精确内容由 Git revision 与 locator 定位。要求：[R692/BEH692](../../requirements/current/local-fix-intake.md)；设计：[D692/CON692](../../design/current/local-fix-intake.md)。实际命令、首次失败及恢复唯一由 [#692 Test](../../requirements-design-test-contributions/692-local-fix-intake/test.md) 拥有，本文不预告通过。

| Identity 与关系 | 正常输入/原入口 | 必须观察与证明边界 |
| --- | --- | --- |
| T692-01 / SC692-ROUTE/REUSE；R692-01/02→D692-01 | 原 Check/独立 Review 读取 selector、Create Issue、Discovery、Clarify、Author 的真实完整差额及未改消费者 | 购买提示与支付核心按实际影响区分；触发、当前重读、仍适用调查事实、亲自重审及下一 consumer 明确。保留 fresh Sync/正式完整正文、正式 graph、全部原子能力和各 gate，具体减少重复广搜/访谈/装配。文案存在不能证明普遍 Agent 效果，不新增专项或计时。 |
| T692-02 / SC692-BINDING；R692-03→D692-02/03 | Discovery 现有 runtime/test_contract 和真实 record/check/invoke wrappers；workflow/standalone 由真实 recorder 分别产生合法结果后普通配错；中文结果逐块错误解码与完整解码对照 | 具体字段/evidence 诊断到当前 AI；失败仍拒绝，check 原字段保留，invoke stdout DTO 不变而 stderr 三字段可读。一致结果保正常成功；digest 差异不被宣称 UTF-8 根因，无正文/值/字节泄露。不得手改 hash/state 制造攻击用例。 |
| T692-03 / SC692-CHANGE；R692-03/04→D692-02/03 | 现有正常 base 前进、authority dirty、错误 branch 及 context_request 目标错配场景 | 原 classification、code/status、字段及直接错误形状保持；恢复说明指到原 Sync 或当前 Discovery/Clarify 支持入口。JSON 读取错误归原层，live body 无新增自动比较，未触及类别不假称通过。 |
| T692-04 / SC692-INSTALL；R692-04→D692-04 | 原 source/installed package validators、完整 apply/reapply、dogfood drift、实际声明平台投影 bytes/mode、递归 sidecar 和基础语法/JSON/Bash/Task/diff | 源码、实际 installed 与选择平台分开验证；继承基线 #706 投影不计 #692 新成果。保原 provenance/用户修改，失败沿原 owner 恢复，不手改 hash 或扩大矩阵。 |
| T692-05 / SC692-QUALITY；全部 R692→全部 D692 | 原 candidate/begin_check、独立 Architecture phase2、完整 candidate Check→原 RDT final_integration/readback→实际 after 重绑→final Check→独立 committed Review/readiness | candidate_ready/candidate_checked 不等最终通过；实际正文/关系/导航与未改 consumer 完整覆盖。后续 commit/publish/merge/Completion/Closure/Finish 各自保原责任；局部测试不代替整体终态。 |

定向现有测试、正常开发和原质量 owner 足以证明本批字段/consumer 与合同改动；不增加专项 replay、A/B、native eval、固定数量、耗时测量、额外 clean installation 或完整多平台矩阵。failed/SKIP/环境缺失分别记录。业务现场、当时安装/原会话、运行时根因、实际净节省时间、外部采用与完整 Release 边界保留未知/未验证。前驱策略为 [生命周期](task-delivery-lifecycle.md)、[JSON 载体](json-input-carriers.md)、[知识方法](knowledge-maintenance.md)，其原责任与历史结果不由本项重写。
