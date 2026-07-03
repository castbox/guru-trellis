# #2 Align guru-team workflow with Trellis auto-bootstrap start model

## 目标

将 `guru-team` workflow、README、preset README 和平台入口 overlay 的用户心智模型，从“用户每次显式运行 `trellis-start`”调整为“用户日常直接描述任务，由 AI 依赖 Trellis auto-bootstrap / workflow-state / hook breadcrumb 自行判断是否进入 Trellis task 流程”。

本任务完成后，`trellis-start` 仍存在，但被定位为 fallback / explicit orientation / 无自动注入平台入口；`trellis-continue` 和 `trellis-finish-work` 仍作为用户常用显式入口保留。Guru Team 的 GitHub issue intake、duplicate search、base branch selection、worktree / branch preflight 不能被弱化。

## 背景与证据

- GitHub Issue: https://github.com/castbox/guru-trellis/issues/2
- Issue 无评论冲突，验收标准直接来自 issue body。
- 官方文档已转向 auto-bootstrap 心智模型：
  - `https://docs.trytrellis.app/start/install-and-first-task`
  - `https://docs.trytrellis.app/start/everyday-use`
  - `https://docs.trytrellis.app/start/how-it-works`
  - `https://docs.trytrellis.app/advanced/multi-platform`
  - `https://docs.trytrellis.app/advanced/appendix-b`
  - `https://docs.trytrellis.app/advanced/appendix-f`
- 当前仓库存在旧口径：
  - `README.md` 的“用户主流程”把 `trellis-start`、`trellis-continue`、`trellis-finish-work` 并列为三个必须记住的主入口。
  - `trellis/workflows/guru-team/README.md` 写明用户主流程仍然只有 `trellis-start`、`trellis-continue`、`trellis-finish-work`。
  - `trellis/presets/guru-team/README.md` 写明 user-facing entry points limited to start / continue / finish-work。
  - `trellis/workflows/guru-team/workflow.md` 的 no-task breadcrumb 已要求 intake/preflight，但未明确不需要用户显式 start；规则 5 仍把 `trellis-start` 列入 primary entry points。
  - `trellis/presets/guru-team/overlays/**/trellis-start*` 的描述仍是 “session entry / normal Trellis start entry point”。

## 需求

1. 日常入口说明必须改为：
   - 用户可以直接描述任务、贴 issue URL、说 “处理 issue #123”。
   - AI 在 repo 已安装 Trellis 的前提下，依据自动注入的 Trellis context、workflow-state、startup context、hook breadcrumb 或 skill matcher 判断是否进入 Trellis task 流程。
   - `trellis-continue` 和 `trellis-finish-work` 是保留的常用显式入口。
2. `trellis-start` 的定位必须改为：
   - fallback / explicit orientation / no-auto-injection 平台入口。
   - 适用于平台没有自动 session/startup 注入、hook 未启用或未审批、怀疑自动注入未运行、用户需要完整上下文报告或重新加载 Trellis 上下文。
   - 不应再被描述成每个任务都要用户记住或先手动执行的日常主入口。
3. `workflow-state:no_task` 必须明确：
   - no active task 时先分类用户自然语言请求。
   - 若请求包含 issue URL、issue number、明确开发任务或需要文件改动，先执行 Guru Team issue intake + base/worktree preflight。
   - 创建 GitHub issue、worktree、branch、Trellis task 等副作用前需要用户 consent，除非用户明确要求这些副作用。
4. Guru Team intake/preflight 规则必须保留并更清晰：
   - issue-backed 或 task-like 请求仍触发 `check-env.sh --json` 与 `prepare-task.sh --json`。
   - duplicate search、auto-create / bind issue、base branch selection、worktree / branch preflight 的门禁语义不变。
   - `.trellis/guru-team/handoff.json` 仍只是 intake provenance，最终 close/ref/followup 由 task-level `issue-scope-ledger.json` 负责。
5. 平台 overlay 必须按平台能力区分：
   - Codex：依赖 `AGENTS.md`、startup context、UserPromptSubmit breadcrumb / bootstrap reminder、skill matcher；缺失时使用 start fallback。
   - Claude/Cursor 等有显式 continue/finish overlay 的平台：不引入新的用户主入口；保留 continue/finish-work。
   - start overlay 文案应说明它是 fallback orientation，而非日常强制入口。
6. 公开 README、workflow README、preset README、workflow 主合同、overlay 文案必须保持一致。

## 非目标

- 不删除所有 `trellis-start` 文件或能力。
- 不削弱 issue intake、duplicate search、issue auto-create、base/worktree preflight。
- 不把 GitHub issue intake 改成 Trellis 流程之外的独立命令。
- 不修改 Trellis 上游源码、全局 npm 包、`node_modules`。
- 不把单个业务 repo 的私有规则写入通用 workflow。
- 不改变 Branch Review Gate、finish-work 后自动 publish PR 的流程。

## 验收标准

- [ ] 文档不再把 `trellis-start` 与 `trellis-continue` / `trellis-finish-work` 并列描述为用户必须记住的日常主入口。
- [ ] 文档明确用户日常可以直接描述任务，AI 根据 Trellis auto-bootstrap / workflow-state 自行判断是否进入 Trellis task 流程。
- [ ] `trellis-start` 被定位为 fallback / explicit orientation / no-auto-injection 平台入口。
- [ ] `workflow-state:no_task` 明确 task-like / issue-backed 请求会触发 Guru Team issue intake + base/worktree preflight。
- [ ] 贴 issue URL、说 issue number、或描述明确开发任务时，AI 会先执行 issue intake + base/worktree preflight，再请求创建 task/worktree/branch 的 consent。
- [ ] `trellis-continue` 和 `trellis-finish-work` 仍保留为用户常用显式入口。
- [ ] README、workflow、preset README、preset overlay 和平台入口文案保持一致。
- [ ] 不修改 Trellis 上游源码、全局 npm 包、`node_modules`，也不把业务 repo 私有规则写入通用 workflow。
- [ ] 验证命令通过：`python3 -m json.tool trellis/index.json`。
- [ ] 验证命令通过：`bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`。
- [ ] 验证命令通过：`python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`。
- [ ] 验证命令通过：`git diff --check`。

## 待确认问题

无阻塞问题。Issue 的目标与验收标准已经足够明确；实现中如发现 overlay 行为需要修改 installer 或脚本，将回到 Phase 1 更新设计后再继续。
