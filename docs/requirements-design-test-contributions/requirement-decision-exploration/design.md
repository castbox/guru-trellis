# 需求探索与确认设计差额

状态为 proposed，适用同一基线与 Architecture `guru-trellis-architecture / docs/architecture/README.md / active`。完整责任见 [D-DEC / CON-DEC](proposed/docs/design/current/requirement-decisions.md)。

共享 Interaction Budget 单写跨阶段原则。Clarify 单写问题发现、轻度清单组织与逐项回答处理；Author 在现有入口承接新歧义，不以技术细化替用户决定需求。现有 question_id、round、部分回答与公共出口保持，不增加 schema 或平行 Skill。对话测试驱动只收集执行事实，不充当语义评分器。

实际 candidate_assessment 与 final_plan 独立评估均返回 no_architecture_impact；实现仍需按实际内容评估，不复制旧 pass。完整 proposed 经候选 Check 后由原 RDT owner 在 final_integration 写入、读回，再重绑实际候选检查；无影响时不造空 Architecture contribution/ADR。
