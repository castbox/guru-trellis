# Guru Team Trellis Workflow Documentation

本目录提供 Guru Team Trellis 的架构说明和验收要求，不是运行时流程 SSOT，也不复制
Skill 内部步骤。

运行时必须以以下 canonical 文件为准：

- Global workflow：`trellis/workflows/guru-team/workflow.md`
- Step-local contracts：`trellis/skills/guru-team/packages/<skill>/`
- Deterministic runtime：`trellis/workflows/guru-team/scripts/`
- Preset / platform distribution：`trellis/presets/guru-team/`
- Dogfood contract specs：`.trellis/spec/workflow/`

## 文档

| 文档 | 用途 |
| --- | --- |
| [requirement-main.md](./requirement-main.md) | AI-first workflow 的稳定验收要求、兼容边界与非目标。 |
| [guru-team-trellis-flow.md](./guru-team-trellis-flow.md) | 面向维护者的简化流程、交互预算和证据生命周期。 |

历史 Issue / PR 只解释需求来源，不定义当前行为。Issue #161 / PR #162 的验收回归以
live GitHub、live `main`、当前 diff、当前测试和冻结的 #119 正常路径复现为证据；旧会话、
旧流程图、旧 task artifact 或已合并 PR 声明都不能替代 current acceptance。

公共 Skill id、exit id、schema id 和 script command 属于公共 API。发生实质变化时必须
提供新 id 或明确迁移合同，并通过 clean install、`trellis update`、preset reapply、
`.new/.bak`、drift 和平台副本一致性验证。
