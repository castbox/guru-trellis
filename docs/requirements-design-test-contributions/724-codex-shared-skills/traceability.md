# #724 RDT 关系与迁移边界

来源：https://github.com/castbox/guru-trellis/issues/724；适用source 42ffd32d70be3859a4493e084464738473c45dd6；authority guru-trellis-rdt；Architecture guru-trellis-architecture。

| 整体/场景 | Requirement/behavior | Design/contract | Test/scenario |
| --- | --- | --- | --- |
| AC1/S1 | R724-01/02、BEH724-DISCOVER/SELECT | D724-01、CON724-PROJECT | T724-01、SC724-INSTALL |
| AC2/S2/S3 | R724-03/04、BEH724-MIGRATE/CONFLICT | D724-02/03、CON724-RETIRE/MAINTAIN | T724-02/03、SC724-UPGRADE/CONFLICT |
| AC3/S5 | R724-05、BEH724-NATIVE | D724-04 | T724-05、SC724-NATIVE |
| AC4/S4 | R724-02/06、BEH724-SELECT | D724-01/03 | T724-04、SC724-SELECTION |
| AC5 | R724-01..06 | D724-01..04 | T724-01..05及定向分发/知识整合 |

本贡献的proposed/docs/{requirements,design,test}/current/codex-skill-distribution.md 提供完整 resulting definitions，proposed 中对应README仅增加新单元关系。原安装和公共资产的具体规范继续由其唯一canonical正文拥有，不复制脚本协议。

predecessor 为原Codex独立根的分发选择，定位 #452 design第3/5/7节及当前preset/skill-package规范；本项窄替代Codex物理根，保留exactselection、用户内容、公开集合和其它平台约束。Architecture精确替代由ARCH-INT-006/ARCH-DOM-020及必要ADR承接。历史不可变版本和其它当前单元不改义。

状态promoted；原candidate Check已完成，原RDT owner在final_integration比较固定B的实际target与完整后像后，写入并读回三层current正文及导航。未覆盖其它单元，authority identity保持guru-trellis-rdt。本贡献记录知识整合，不代替最终Check、完整Review或整体Completion。
