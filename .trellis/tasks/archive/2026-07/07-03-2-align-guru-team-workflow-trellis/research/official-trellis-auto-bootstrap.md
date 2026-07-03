# 官方 Trellis auto-bootstrap 文档摘录

## 目的

记录 issue #2 的外部依据：Trellis 官方文档当前推荐用户直接描述任务，由平台注入上下文与 AI 判断是否进入 Trellis 流程，而不是每个任务显式运行 `trellis-start`。

## 来源

- https://docs.trytrellis.app/start/install-and-first-task
- https://docs.trytrellis.app/start/everyday-use
- https://docs.trytrellis.app/start/how-it-works
- https://docs.trytrellis.app/advanced/multi-platform
- https://docs.trytrellis.app/advanced/appendix-b
- https://docs.trytrellis.app/advanced/appendix-f

## 结论

- 日常用户入口应强调自然语言任务、issue URL / issue number、continue、finish-work。
- `trellis-start` 应作为 fallback / explicit orientation / no-auto-injection 平台入口保留。
- Guru Team 自有的 issue intake 和 worktree preflight 必须挂在 no active task triage 之后，而不是绑定到用户显式 start 命令。

## 对本任务的影响

- README 与 workflow README 需要移除“用户必须记住三个主入口”的旧表述。
- `workflow-state:no_task` 需要明确自然语言分类、task-like 判断、intake/preflight 和 consent。
- start overlay 的文件仍保留，但 description 和正文要体现 fallback 定位。
