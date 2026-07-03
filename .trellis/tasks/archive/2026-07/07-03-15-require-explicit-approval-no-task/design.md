# Issue 15 技术设计

## 设计原则

1. **Markdown 控制判断流程**：direct-edit override 是 AI/human 判断门禁，应写入 `workflow.md`、platform overlay 和 spec checklist。
2. **脚本只做事实检查**：如果增加 validator，只检查是否存在 evidence，不判断 scope 是否合理、不替代 handoff review。
3. **canonical 先行，dogfood 同步**：长期源头是 `trellis/workflows/guru-team/workflow.md` 与 `trellis/presets/guru-team/overlays/`；本仓库 `.trellis/workflow.md` 和 `.agents/.codex` 安装副本必须同步。
4. **不扩大用户授权**：direct-edit override 只允许本轮当前 checkout 修改，不包含 commit、push、PR，也不延伸到后续 turns。

## 目标行为

当没有 active task 时，AI 收到用户请求后按以下分支处理：

1. 纯解释 / 查询 / 不改文件：可直接回答，必要时询问是否创建 task。
2. issue URL、issue number、明确开发任务或任何 file-changing request：默认运行 Phase 0 intake/preflight。
3. 用户明确要求跳过 GitHub issue、Trellis task、worktree、branch，并批准 current-checkout direct edit：允许在当前 checkout 改文件，但必须先说明副作用、changed-file scope、dirty state，并记录 override evidence。

override evidence 可以是对话中的明确用户消息、task artifact 中记录的批准，或等价 review report。缺少 evidence 时，AI 不应静默编辑当前 checkout。

## 文件边界

### Workflow

- `trellis/workflows/guru-team/workflow.md`：canonical workflow contract。
- `.trellis/workflow.md`：本仓库 dogfood active copy，由 `get_context.py` / per-turn breadcrumb 读取。

需要同步以下区域：

- Core Principles：补充 direct-edit override 原则。
- Guru Team Gate / Request Triage：明确默认 Phase 0 与 override 例外。
- `[workflow-state:no_task]`：短提示加入“不要静默 direct edit”。
- Phase 0 / Handoff review：补充 direct-edit override 展示内容。
- Rules：补充 override 不等于 commit/push。

### Overlay

canonical overlays：

- `trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-start.md`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-start/SKILL.md`

dogfood 安装副本：

- `.agents/skills/trellis-start/SKILL.md`
- `.codex/prompts/trellis-start.md`
- `.codex/skills/trellis-start/SKILL.md`

修改 canonical overlay 后必须运行：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

### Specs / Checklist

- `.trellis/spec/workflow/workflow-contract.md`：加入 no_task direct-edit override 合同。
- `.trellis/spec/workflow/quality-guidelines.md`：加入 review/checklist 项，要求 Branch Review / PR readiness 检查是否有 Phase 0 evidence 或 explicit override evidence。

### Docs

- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

只在现有“日常入口 / workflow guardrails”段落补充 direct-edit override 说明，不新增大段重复流程。

## Validator 取舍

Issue 提到 optional hard gate / validator。本次优先落地 Markdown 合同与 review checklist；如实现脚本 gate，风险是需要定义“无 active task + 非 metadata 改动”如何跨平台可靠检测、证据存放在哪里，以及如何避免脚本把 AI 判断伪装为通过结论。

本设计选择不新增 validator，原因：

- issue 验收写的是“如实现 validator”，不是必做。
- 当前缺口首先是 AI 判断合同缺失；Markdown workflow / overlay 是官方推荐控制面。
- 如果没有清晰 evidence artifact schema，仓促脚本 gate 可能制造新的假通过路径。

若后续仍出现漏执行，应单独开 issue 设计 evidence artifact 与 validator。

## 兼容性与升级

- 不改 `trellis/index.json` 的 workflow id / path / type。
- 不改 preset installer 复制逻辑或 managed asset list。
- overlay canonical 改动通过 preset apply 同步到 dogfood copy，保证已安装副本可升级。
- workflow canonical 改动需要手动同步 `.trellis/workflow.md`，并通过 `get_context.py --mode phase` 验证 breadcrumb 解析。

## 安全

本次不涉及 secret、token、`.env`、客户数据或外部服务凭证。验证和 PR body 不应包含敏感本机路径之外的私密内容；本机 worktree path 可作为任务 evidence 使用。
