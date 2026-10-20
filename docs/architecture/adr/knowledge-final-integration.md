# ADR-KNOWLEDGE-FINAL-INTEGRATION：稳定身份与最终整合晋升

状态：accepted。来源：castbox/guru-trellis#638。前驱：ADR-030的首次检查前实际晋升义务；保留其最终Check前真实晋升、独立评估与质量覆盖。

## 决策

完整知识单元保持稳定identity，Architecture根authority为guru-trellis-architecture，RDT为guru-trellis-rdt。精确内容由完整Git revision和locator定位。普通promotion不要求global successor、总入口必写或每Issue业务摘要；导航只在定位、身份或状态变化时写入。真实public API/schema版本、bootstrap distinct successor与旧Git/版本引用原义保留。

同Delivery先在隔离贡献与完整proposed正文上完成独立Architecture和原Check完整候选判断。implementation先candidate/begin_check进入checking；候选通过后原Check用既有rework(target_role=implementation, affected_results=[readiness])回implementing，再输出candidate_checked，不写最终public Check。Planning与真实旧gate历史保留，但历史不自动成为当前结果。

candidate_checked唯一consumer进入原Architecture/RDT final_integration。原owners一次固定真实目标branch/commit，只读写命中单元及必要关系。相同单元合成保留原有效条件和双方改动，按唯一候选适用合同补独立审核全部实际差额、组合语义及受影响未改consumers；推翻前提或改变实现/接口/验证义务回最早原owner。原owners写完整组合、读回并判断适用性。

implementation以同B、实际HEAD和全部after差额重新candidate/begin_check。最终Architecture/Check使用新content_ref，最终public Check才进入reviewing，然后TaskCommit和独立完整committed Review覆盖真实内容。Ready/Publication/Completion/Finish只接受真实no_change或reviewed_promoted。no-change也走合法回程，无空贡献、ADR、文件或提交。

## 取舍与边界

原owners及最小DTO承接本能力，不新建Skill、Task phase、API操作、队列、锁、第二current或审计账本。实际目标不同于固定开发B；无关ref前进不要求merge/rebase或追赶。正常mismatch/partial/output-loss由原owner恢复同一明确intent，仅补pending；冲突或不唯一停止。候选输出丢失按实际phase/写入事实回原producer与implementation重绑，不从state制造pass。

ADR-028固定适用来源及ADR-034候选覆盖适用性继续有效。仅窄替代ADR-030及命中正文的首次完整检查前实际晋升、global successor/根入口必写义务。独立性、single-writer、完整条件/关系、真实写边界与最终质量保持。

## 迁移与验证责任

Arch非Planning5.0/Delivery3.0、RDT impact/promotion2.0、Check private6.0和直接consumers按MIGRATION-638完整matching切换。Planning3.0/Delivery1.0、bootstrap/repair保持。旧安装固定，当前runtime拒旧shape，不转换旧pass或双读；旧普通读consumer按Task完成/合法改选/真实依赖变化退出，历史永久可读。

本决定接受职责和行为，不证明实际实现、安装、Agent/GitHub或Release通过。唯一实际结果由[本Task Test](../../requirements-design-test-contributions/638-shared-current-promotion/test.md)拥有；完整多平台Release矩阵、Backend采用和生产部署不在本决定验证范围。
