# 正常完成与协调成本：设计差额

状态：proposed。完整目标为 `proposed/docs/design/current/knowledge-maintenance.md` 的 D-MECH-01—03，保留其它正文、稳定身份和历史来源。

方法唯一正文仍为 [Adopted-mechanism review](../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md#adopted-mechanism-review)。它拥有直接最终完成路径、默认不准入额外协调、主动替代比较、完整完成成本及存量三分类。具体新增 I/O、共享争用、串行和等待的判断由该正文单写，RDT 仅承接行为和所属职责。

- D-MECH-01 承接 R-MECH-01/03/04：Author 先推导直接路径；Architecture/独立审核主动尝试并自行判断替代可行性。已最小方案说明依据，无需虚构替代；现有 Approval/Check/Review 消费同一方法。
- D-MECH-02 承接 R-MECH-02：Root Cause 的 Protection 保留原资格，明确其不自动批准 Architecture 选择。Author 和 Root Cause 在原消费点引用，不复制规则或改变出口。
- D-MECH-03 承接 R-MECH-03—05：保留文档优先及必要源码调查，分别承接必要机制、已证缺陷和缺证；由原 owner 有界修订并适配必要消费者，不建永久机制登记或迁移台账。

canonical 只修改 Architecture contract、Root Cause contract 和 Author authoring 三处；已有有效的 Approval、Check、Branch Review 和独立 Review 引用不改。公共 I/O、schema、runtime、installer、原则和生命周期保持。未修改 managed dogfood/installed，不把源码一致当作安装采用。

本贡献准备完整 proposed 内容供原维护 owner 及候选 Check 使用，不预写 shared current。候选通过后的实际整合、读回、同 B 的全部 after 重绑及最终质量链仍由原 owners 执行；本设计不提供其通过结论。
