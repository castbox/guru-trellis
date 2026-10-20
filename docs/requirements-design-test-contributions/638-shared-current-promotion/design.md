# 最终整合与稳定身份设计贡献

状态：proposed。完整组合正文在[knowledge](proposed/docs/design/current/knowledge-maintenance.md)、[lifecycle](proposed/docs/design/current/task-delivery-lifecycle.md)及三层根README；不是另一current。

D638-01/CON638-IDENTITY由原maintenance owners保留单元身份、精确Git定位与必要关系。RDT根切换为guru-trellis-rdt，Architecture为guru-trellis-architecture；只在关系/身份/状态变化时修改根入口。公共API/schema独立版本化，bootstrap、历史Git和未命中能力不改义。

D638-02/CON638-CANDIDATE由原implementation与Check承接：candidate/begin_check把完整B..HEAD及dirty绑定公共candidate，独立Architecture和Check审完整拟写后，Check原rework只失效readiness回implementing，再发candidate_checked。候选结果仅交最终整合router，无check_result_id，不进入TaskCommit。

D638-03/CON638-INTEGRATION由原Architecture/RDT在固定真实目标合成、补审、写入及读回。只处理命中单元及必要导航/关系；同单元保留双方仍有效条件，不以Git自动合入替代语义。当前候选适用合同单写原覆盖、全差额和受影响未改consumers；义务/前提变化回原owner。实际after重新candidate/begin_check，再最终Check/committed Review，Ready只no_change或reviewed_promoted。没有知识变化走合法回程而不写空文件。

D638-04/05保持既有Skill/API/phase与single-writer。Arch5/Delivery3、RDT2、Check6和直接consumer按[MIGRATION-638](../../../trellis/presets/guru-team/MIGRATION-638.md)直接演进，Planning3/Delivery1与bootstrap/repair保持。三类在途和输出丢失由原producer实际重读，不从phase或旧pass补造结果，不跨读private状态。canonical经原matching安装分发；当前实现分支的source编辑不代表开发Task运行副本已采用。

原Architecture contribution/必要ADR由其原owner维护；其完整proposed位于[Architecture proposed](../../architecture/contributions/638-shared-current-promotion/proposed/docs/architecture/)。本RDT只继承公开locator/version/status，不复制constitution或project-check语义。唯一实际验证由[test.md](test.md)拥有。
