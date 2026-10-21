# #648 来源、目标与追踪

固定B：`cca65742bc485f8ab4e6399623b70dd5aebc25bd`。RDT authority identity保持`guru-trellis-rdt`，Architecture保持`guru-trellis-architecture`。完整目标在proposed镜像，由原RDT owner最终整合后才成为共享正文。未命中knowledge单元及导航、旧版本、其他Task贡献与归档均不改。

| Requirement / behavior | Design / contract | Test / scenario | 来源与完整目标 |
| --- | --- | --- | --- |
| R648-01 / BEH648-01 | D648-01 / CON648-SOURCE | T648-01 / V648-01 | #648目标1；requirements/design/test各knowledge-maintenance完整拟写中的648小节 |
| R648-02 / BEH648-02 | D648-02 / CON648-PREMISE | T648-02 / V648-02 | #648目标2/3，独立性、before_authority及合法例外 |
| R648-03 / BEH648-03 | D648-03 / CON648-REENTRY | T648-03 / V648-03 | #648目标4及原owner三分流、受影响恢复条件 |
| R648-04 / BEH648-04 | D648-04 / CON648-EXPECTATION | T648-04 / V648-04 | #648目标5；有效合同、共同错误断言与未改consumer |
| R648-05 / BEH648-05 | D648-05 / CON648-APPLICABILITY | T648-05 / V648-06 | #648目标6及10/21补充；同域gate/invariant A-B |
| R648-06 / BEH648-06 | D648-06 / CON648-COVERAGE | T648-06 / V648-05 | #648目标7；前提变化刷新与合法事实复用 |
| R648-07 / BEH648-07 | D648-07 / CON648-VALIDATION | T648-07 / V648-07/08及横切01..06 | #648验收与边界；当前匹配对照、原入口和分发/行为分层 |

本增量补充原owner方法与验证，保留R331/R578/R600/R637/R638的适用性、single-writer、当前语义判断、工程事实与最终整合条件。没有旧public API退役或兼容扩张，不改基线或五原则，不新增ledger、通用审批、公共数据或runtime状态。

所有实际结果只由[test.md](test.md)拥有；完整目标的Test正文只定义场景、策略与结果定位。raw语料/脚本和wrapper结构通过不能替代AI对实际记录的语义判断。
