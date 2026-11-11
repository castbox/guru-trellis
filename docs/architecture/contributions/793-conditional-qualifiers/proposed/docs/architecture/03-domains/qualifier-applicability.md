# qualifier 适用条件与原 owner

Identity：ARCH-DOM-QUALIFIER-APPLICABILITY；aliases：conditional qualification、#793。
原 owner：guru-maintain-architecture-baseline。状态 proposed，来源为 Issue #793 及
固定 before Git e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e。原 final_integration
晋升前不是 shared current。决定为 [ADR-CONDITIONAL-QUALIFICATION](../adr/conditional-qualification.md)。

## 完整职责

normal、solution、root 分别独占场景准入、业务 authority 承载与因果候选准入。
各原包 `references/applicability.md` 独占可先读取的触发、采用、刷新和加载条件；
完整资格算法仍在原 Skill/contract。caller先判断是否需要该owner，不在短条件层
给qualified/rejected或因果充分性verdict。原stage仍判断其scope、规划、实现、
证据、severity、readiness与完成，qualifier不会替代这些职责。

十类lifecycle及已有Author profile在各自候选提升边界分别读取三条件。触发且无
适用结论时显式load原stable Skill，以实际适用非空集合执行原闭环；未触发不
load全文、装配空输入或制造classified/skipped结果。solution检查真实机制承载的
业务决定、证明、拒绝或执行资格，不把普通计算或OS关键词当完整判据。root按
真实诊断、缓解、修复、保护行为进入，普通feature名称不能遮蔽实际机制。

root入口使用caller当前场景/authority-placement判断，消费真正触发的上游结果；
正确未触发的normal/solution没有结果前置。非通过先回各原唯一consumer，未变
机制采用仍适用结论；实质authority、机制、支持路径、条件或证据变化刷新依赖项。
丢失必要结论回原producer。新invocation仍校当前facts，采用不重放旧envelope。

runtime只校schema、facts、coverage、aggregation和consumer，不决定是否触发或
语义pass；没有新Skill、wrapper、classifier、DTO、资格数据库或授权持久化。

## 选择、成本与采用

仅删global mandatory不能消除原caller/root前置；统一wrapper/固定问卷会复制
三个owner。选择各原owner短reference和原caller落点，减少不适用全文与装配，
保必要判断和原出口。新增reference有现有caller直接消费；不为未来预留状态。
本设计没有费用比例或业务效果结论。

[MIGRATION-793](../../../trellis/presets/guru-team/MIGRATION-793.md)定义成套采用；
旧完整安装采用前保原合同，同Task/gen/key/root按实际义务续接。原tools owner
保Task/session同步受管投影，原Architecture/RDT在candidate检查后分别晋升完整
定义并readback，actual after再绑定和最终质量链。不存在兼容双reader或新审批链。

本单元窄替代原固定调用、root两上游普遍前置和无材料变化的重复要求，保
ADR-008/020的其余职责和#383完成语义。方法变更、真实authority/consumer变化时
回原owner重审。R/D/T关系为 `REQ-793` → `DES-793` → `TST-793`，完整定义位于
各层 `current/qualifier-applicability.md`；实际观察由配对Test单写。
