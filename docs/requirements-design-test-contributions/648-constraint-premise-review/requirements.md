# #648：来源约束与关键前提的跨阶段审查增量

状态：`proposed`；固定适用源为 `cca65742bc485f8ab4e6399623b70dd5aebc25bd` 的 `docs/requirements/current/knowledge-maintenance.md`，authority identity 保持 `guru-trellis-rdt`。来源为 [#648](https://github.com/castbox/guru-trellis/issues/648) 完整正文与2026-10-21补充。完整拟写正文见 `proposed/docs/requirements/current/knowledge-maintenance.md`；其中链接按最终目标路径解析，当前尚未晋升。

R648-01..07 / BEH648-01..07 的完整定义由该拟写正文中“约束、前提与原 owner 修订”小节拥有。本文件只定位增量与继承关系：约束落点、原证据与合法例外、规划内冲突三分流、合同先于共同错误断言、gate/invariant适用范围、前提变化复核、真实当前版本对照。

保留 R331、R578、R600、R637、R638及原稳定REQ/BEH身份、完整条件、否定、例外与关系。#648不改变阶段成果状态或Completion证据一致性机制，不承接#649；不改变fresh reviewer载体，不承接#651。公共Skill/profile/exit/schema/runtime、职责与授权边界保持。业务政策、业务API/代码、版本发布和完整Release矩阵不在本增量。

原RDT owner在candidate Check前提供完整隔离目标；实际shared-current写入仍在原final_integration。当前文件存在不证明行为、安装或Task完成。设计与测试关系见[traceability](traceability.md)。
