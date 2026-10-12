# #535 增量需求

Direct Source：[Guru #535](https://github.com/castbox/guru-trellis/issues/535)；source binding 见 [manifest](manifest.yaml)。继承 current RDT .86 与 Architecture .84/active。运行步骤由两个 canonical Review Skill 独占定义。

| Requirement / behavior | 必须行为 |
| --- | --- |
| R535-01 / BEH535-EMPTY | 完整语义 Review 无真实候选时使用 []，由原 recorder/checker/public invocation 承接；不捏造无缺陷占位候选。 |
| R535-02 / BEH535-QUALIFY | 仅对真实候选调用适用 qualification；实际非空全 rejected 保留分类，与真实零候选分开。 |
| R535-03 / BEH535-GATES | 空集不决定 passed/ready；原完整维度、Docs/Architecture、freshness、真实引用、route 与 checkpoint 生命周期保持。 |
| R535-04 / BEH535-PROFILES | Branch current initial/fresh-final、bounded continuity、archived read-only 与 Delivery 原五种路线保持各自合同；pinned Branch5/6不重写。 |
| R535-05 / BEH535-DISTRIBUTE | canonical、dogfood、一个完整代表性安装的原入口及 apply/reapply/drift 分层验证；不冒充完整 Release 矩阵。 |

不改变 Task/Delivery 生命周期、qualification 公共非空合同或公共 DTO，不接管 #292/#530/#531。设计、测试实际结果与 trace 分别由 [design](design.md)、[test](test.md)、[traceability](traceability.md)拥有。
