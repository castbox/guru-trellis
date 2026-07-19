# Official Trellis Extension Contracts

核对日期：2026-07-19。

## 来源

- Custom workflow：https://docs.trytrellis.app/advanced/custom-workflow.md
- Custom skills：https://docs.trytrellis.app/advanced/custom-skills.md
- Architecture：https://docs.trytrellis.app/reference/architecture.md
- Custom spec template marketplace：https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md

## 对 #130 的约束

1. Team workflow行为通过 marketplace workflow Markdown定义；global workflow负责phase与route，不修改Trellis上游源码或全局npm安装。
2. Guru-specific semantic check必须使用additive custom Skill package；official `trellis-check` worker保持未修改，只提供review evidence。
3. Project specs保存可复用工程合同；active task state、planning artifacts和运行证据保持task-local，不进入spec template marketplace。
4. Package、workflow和preset必须通过canonical source、installer和installed copy验证，不能只在dogfood生成文件上打一次性patch。

## 规划结论

`guru-check-task`采用canonical Guru Skill package + thin workflow route + shared deterministic runtime + registry-driven preset distribution。任务不新增或修改任何upstream-owned `trellis-check` overlay。
