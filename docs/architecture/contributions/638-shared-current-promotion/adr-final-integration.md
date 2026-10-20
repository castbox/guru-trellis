# ADR-KNOWLEDGE-FINAL-INTEGRATION：稳定身份与最终整合晋升

状态：proposed；来源：castbox/guru-trellis#638。本文是Task-owned必要ADR候选，尚未进入共享ADR/current authority。

## 决策与窄替代

知识单元使用稳定identity，完整Git revision与locator定位精确正文。取消普通Task晋升强制递增总入口identity及写总入口；真实public API/schema版本和历史引用意义保留。根导航仅在定位关系或状态真实变化时修改。

Task隔离贡献与完整拟写正文先由原独立Architecture及原Check完成候选检查。原Check的candidate_checked不写最终public Check gate。实际shared-current写入收敛到同Delivery最终整合边界：原Architecture/RDT owners读真实命中目标并合成、补审真实差额/消费者、写入读回，再由原最终Check、commit和独立完整Review覆盖实际内容，Ready/Merge前具备真实promoted状态。

只替代ADR-030和命中项目正文中的“首次检查前必须实际晋升”及普通全局successor写入义务。保留独立评估、single-writer、写前真实目标、完整定义/条件/关系、普通mismatch与恢复、最终质量覆盖。ADR-028固定适用来源及ADR-034覆盖适用性继续有效。

## 取舍与退出

原owners和最小consumer DTO足以实现本要求，不新增Skill、队列、锁、审批、第二current或证据账本。新旧public/runtime合同通过MIGRATION-638成套切换；旧安装固定，当前受控consumer直接迁移，不以旧pass补字段生成新通过。旧Git快照保留历史可读性，不作为持续双写路径。

同单元真实语义冲突仍由原owner合成；Git自动合入不能替代判断。无关目标前进不替换固定候选，无实际阻塞不要求merge/rebase或追赶最新SHA。正文改变行为、接口或验证义务时回原质量owner。no-change不制造空贡献或晋升。

## 结果边界

当前只有候选方向独立评估；final_plan、实现、安装和实际样本尚未完成。原Architecture owner在最终整合时将受审必要决定写入`docs/architecture/adr/knowledge-final-integration.md`及命中的完整current正文。贡献、规划或schema成功都不代表交付或整体完成。
