# #532 增量需求

状态：reviewed_promoted；Direct Source：[Guru #532](https://github.com/castbox/guru-trellis/issues/532) 的目标与修复边界、验收，当前来源更新时间 2026-10-12T10:09:24Z。继承 current RDT .85 与 Architecture .84/active；行为步骤仍只由 canonical Check Skill 定义。

| Requirement / behavior | 必须行为 |
| --- | --- |
| R532-01 / BEH532-EMPTY | 完整真实 Check 无缺陷候选时，空 classifications 经原 recorder/checker/public initial_check 可达；受审文件和业务功能不是缺陷候选。 |
| R532-02 / BEH532-QUALIFY | 仅对实际候选调用适用 qualifier；保留三个 qualification Skill 非空合同。真实非空全 rejected 保留分类且无 findings。 |
| R532-03 / BEH532-GATES | 空集合不推导 passed；九维、Docs/Architecture、freshness、真实引用一致性、四 exits/consumer 和 execution checkpoint 生命周期保持。 |
| R532-04 / BEH532-PROFILES | 四 Check profiles 共用原 schema/validator；reconciliation 保留原私有结果与 target projection。 |
| R532-05 / BEH532-DISTRIBUTE | canonical/dogfood/一个代表 installed 的原入口、apply/reapply/drift 分别证明；分开报告单元/契约和真实公开链路。 |

本增量不接管 #292/#530/#531、不增加 Task/Delivery authority 或资格判断空集 API。完整 Release matrix、版本发布与业务部署独立。设计、验收实际结果与双向 trace 分别由本目录 [design](design.md)、[test](test.md)、[traceability](traceability.md)拥有。
