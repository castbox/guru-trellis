<!-- TRELLIS:START -->
# Trellis Instructions

These instructions are for AI assistants working in this project.

This project is managed by Trellis. The working knowledge you need lives under `.trellis/`:

- `.trellis/workflow.md` — development phases, when to create tasks, skill routing
- `.trellis/spec/` — package- and layer-scoped coding guidelines (read before writing code in a given layer)
- `.trellis/tasks/` — active and archived tasks (PRDs, research, jsonl context)

If a Trellis command is available on your platform (e.g. `/trellis:finish-work`, `/trellis:continue`), prefer it over manual steps. Not every platform exposes every command.

If you're using Codex or another agent-capable tool, additional project-scoped helpers may live in:
- `.agents/skills/` — reusable Trellis skills
- `.codex/agents/` — optional custom subagents

Managed by Trellis. Edits outside this block are preserved; edits inside may be overwritten by a future `trellis update`.

<!-- TRELLIS:END -->

<!-- guru-team-ai-first-principles:start -->
## Guru Team AI-first 原则

- **AI-first，不模拟人类审批流**：AI 直接读取 live authority、规划、diff、测试和前序最终结果完成语义判断，不制造 assignment、handoff、签字或审批链。
- **只保留不可重新推导且有直接 consumer 的最小结果**：活动 checkpoint 默认 owner-private、短生命周期，consumer 完成后即删除。
- **任何阶段都不持久化用户授权信息或授权过程**：授权只存在于当前对话，不进入 tracked、ignored-runtime、gate、handoff、checkpoint、archive、schema 或 public DTO。
- **Digest 不是 workflow authority**：digest 只服务一个局部确定性 consumer，不绑定用户授权、semantic approval、跨 Skill handoff 或全链 freshness。
- **交互只服务真实选择和副作用**：只有真实选择、scope/authority 变化或 Git/GitHub 副作用才询问；mapped exit、stale/re-entry/reprepare/recovery 自动承接。
- **语义门禁与持久化解耦**：AI 语义门禁仍然必需；recorder/checker 不得替代判断，也不得为留下证明制造 tracked dirty。
- **清晰技术写作**：首次生成实质文本前，完整读取 `.trellis/spec/workflow/clear-technical-writing.md` 并在原职责范围内执行。适用于无 Task、正式 Task、task-free、独立操作、恢复会话和子 Agent。读取成功前只输出短句进度或具体缺失诊断，说明当前动作或缺失项，不作未经验证的结论。文件缺失或读取失败时暂停实质文本；恢复后完整读取并继续原请求，不新增审批。子 Agent 不假设继承；完整且未截断的原生注入可直接使用，否则自行完整读取同一文件。
<!-- guru-team-ai-first-principles:end -->
