# #718 来源、稳定关系与完整拟写

状态：promoted；authority=`guru-trellis-rdt`；适用before为main `610a810d45bb30173906d55c77709389adf1cf31`。Task整体范围由根PRD拥有；D1为 `a12847c3-5f1e-4e72-9300-fca42bcf9e43`、generation=0，覆盖全部行为1—11与A1—A8。

完整来源为[Issue #718](https://github.com/castbox/guru-trellis/issues/718)、[D1设计](../../../.trellis/tasks/11-02-718-runtime-location-decoupling/deliveries/a12847c3-5f1e-4e72-9300-fca42bcf9e43/design.md)第3节原承诺处置、第4—8节方案及验证，以及原bootstrap、Sync/Discovery及其真实consumer。完整拟写与必要导航由manifest逐项定位；目标内相对引用按最终target解析。原RDT未迁移语料保留其原完整来源，不宣称整库迁移。

| Requirement / behavior | Design responsibility / contract | Test strategy / scenario | AC |
| --- | --- | --- | --- |
| R718-01 / BEH718-DISCOVER | D718-01/02 / CON718-ENV/SELECT | T718-01 / S718-ARBITRARY | A1 |
| R718-02 / BEH718-IDENTITY | D718-01/02 | T718-01/02 / S718-STABLE | A1/A3 |
| R718-03 / BEH718-CODE | D718-01/03 / CON718-REPAIR | T718-03/06 / S718-MAINTAIN | A6/A7 |
| R718-04 / BEH718-SELECTION | D718-02 / CON718-SELECT | T718-02 / S718-STABLE | A3 |
| R718-05 / BEH718-RECOVERY | D718-03 / CON718-REPAIR | T718-03 / S718-RECOVERY | A6 |
| R718-06 / BEH718-LIFECYCLE | D718-01/02/06 | T718-01/02 | A2 |
| R718-07 / BEH718-BASELINE | D718-04/05 / CON718-BASE/CONSUMER | T718-04 / S718-READ | A4 |
| R718-08 / BEH718-OPERATION | D718-04/05 | T718-05 / S718-REJECT | A5 |
| R718-09 / BEH718-DRAFT | D718-05 / CON718-CONSUMER | T718-04/08 / S718-READ/AGENT | A4 |
| R718-10 / BEH718-CONSUMER | D718-04/05 | T718-04/05/08 | A4/A5 |
| R718-11 / BEH718-MIGRATION | D718-06/07 / CON718-CUTOVER/BOUNDARY | T718-06/07 / S718-MAINTAIN/DISTRIBUTE | A7/A8 |

保留#219隔离环境和真实wrapper、#231完整identity共享、#556默认/显式规则和失败保护、#566单目标维护及公共Task/data兼容。窄替代pointer作为启动必要前置、只读Git对象继承Sync checkout/clean前置；旧active.json仅在新selection-v3.json不存在时一次迁移，旧消费者原文保持，新无效载体不回退丢约束。迁移API及具体schema由MIGRATION-718与原Interface单写。

原RDT task_impact_sync返回candidate_ready，独立Architecture和实际candidate Check审查了完整实现与proposed。取得candidate_checked后，原owners固定真实target并核对before/proposed/live差额；本RDT final_integration已整合六个目标并逐项readback。implementation随后须重绑全部after，再由原owners执行final Architecture/Check、commit和完整committed Review。历史贡献保留来源，普通当前查询读取完整current；实际工程观察仅由Test正文拥有。
