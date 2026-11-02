# 需求探索与确认追踪

适用基线 a4feadd99683e006580ef16b078c44e3ad3648a7，authority `guru-trellis-rdt`。proposed 镜像最终 repo-relative 位置，内部链接按最终位置解释。

| 整体要求与验收 | 需求/行为 | 设计/合同 | 测试/场景 |
| --- | --- | --- | --- |
| DEC-R1/R2；AC1/4 | R-DEC-01 / BEH-DEC-DISCOVERY | D-DEC-01 / CON-DEC-OWNERS | T-DEC-01 / SC-DEC-EVIDENCE |
| DEC-R3/R4；AC1/2 | R-DEC-02 / BEH-DEC-QUESTION | D-DEC-02 / CON-DEC-PRESENTATION | T-DEC-02 / SC-DEC-CHECKLIST |
| DEC-R5/R6；AC2/3 | R-DEC-03 / BEH-DEC-ANSWER | D-DEC-02/03 / CON-DEC-ANSWER/RETURN | T-DEC-02/03 / SC-DEC-PARTIAL/RESUME |
| DEC-R7/R8；AC5/6 | R-DEC-04 / BEH-DEC-EVIDENCE | D-DEC-04 / CON-DEC-VALIDATION | T-DEC-04 / SC-DEC-DISTRIBUTION |

现有 Task/Delivery、局部修复 Intake 和知识维护完整单元保持。既有逐项问题和部分回答规则继续有效；原单问题消息限制按本次明确需求调整为问题记录及用户呈现分离。精确执行方法归原 canonical Skill/shared spec，不复制第二份流程。

无 Issue 不产生外部关闭语义。Architecture entry/constitution 保持。该贡献不作为用户授权、独立审核通过或 Task 完成的记录；实际验证观察见 test.md，正式质量与交付事实由原公开结果承接。
