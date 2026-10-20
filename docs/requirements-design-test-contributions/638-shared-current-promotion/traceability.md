# 来源、完整目标与替代追踪

固定B=`9cec623833b61814f1175f31acde4fa81334cdb0`；RDT前驱`.114`，Architecture前驱`.105`。本贡献未晋升。proposed/镜像路径保存完整目标文件；其中相对链接按最终目标路径解析，不能把隔离目录当current。原promotion owner在真实目标合成后才写共享正文。

| Requirement/behavior | Design/contract | Test/scenario | 完整目标和来源处置 |
| --- | --- | --- | --- |
| R638-01/05；保留R331-01/02/05、BEH331及REQ/BEH稳定ID | D638-01/CON638-IDENTITY；保留D331-01/02/05 | T638-01/02/04 | 三层knowledge-maintenance完整单元与三根README；替换全局递增/总入口必写义务，保留条件/关系/历史/Git/API版本 |
| R638-02/03；承接R600、R531-04 | D638-02/CON638-CANDIDATE | T638-03 | knowledge与lifecycle最终质量小节；替换首次完整检查前实际晋升，新增原Check候选出口，保留独立Architecture和完整检查 |
| R638-04/06；保留R567/R578/R637 | D638-03/CON638-INTEGRATION | T638-02/03/05 | 原owners固定真实目标合成及实际写入；implementation重绑actual after；保留原覆盖+差额+未改consumers、普通mismatch/partial/output-loss |
| R638-06/07 | D638-04/05 | T638-04/06/07 | MIGRATION-638与原packages/consumer；当前旧入口退出、三类在途、matching分发、#636/#637组合；旧版本/Git保持原义 |

Architecture完整proposed命中ARCH-CUR-070、ARCH-DOM-053、ARCH-INT-056、ARCH-GOV-008/012及change-contract。新语义ADR为ADR-KNOWLEDGE-FINAL-INTEGRATION，最终locator=docs/architecture/adr/knowledge-final-integration.md。保留九concerns、constitution、descriptor/result2.0与GAP状态；不宣称关闭ARCH-GAP-006/008。根入口改稳定identity与必要关系，删除逐Issue摘要堆积；已有历史精确Git导航保留。

未命中范围：completion-closure、native-compatibility等完整单元和其current导航不改；未迁移legacy身份仍由原导航/完整来源拥有，不声称全语料重迁。历史版本页、ADR、其他Task contribution及归档不回填。源B中的有效例外/否定、single-writer、最终质量、Refs-only/Closure与整体Completion分工保持。旧Task普通读在finish、合法reactivate改选或真实依赖变化后退出；历史永久可读，不成为旧current持续维护路径。

执行结果只在[test.md](test.md)。规划验证表定义预期，目录/链接/schema与脚本成功不证明真实Agent、current晋升、Ready或Task完成。
