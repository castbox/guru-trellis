# #2 设计：Guru Team auto-bootstrap 入口心智模型对齐

## 设计原则

1. **入口心智模型统一**：公开 README、workflow README、preset README、workflow 主合同和 overlay 不能互相冲突。
2. **Trellis 原生优先**：依赖 workflow-state、startup context、hook breadcrumb、skill matcher 和 overlay，不增加独立业务命令。
3. **start 保留但降级定位**：`trellis-start` 是 fallback / explicit orientation，不是每个任务的强制起手式。
4. **intake/preflight 不降级**：auto-bootstrap 只改变触发心智模型，不改变 Guru Team issue intake 与 Git preflight 的门禁强度。
5. **跨平台一致**：相同 overlay 内容在 `.agents`、`.codex/prompts`、`.codex/skills` 中保持同步；continue/finish-work 入口不被改弱。

## 修改边界

### 需要修改

- `README.md`
  - 将“用户主流程”改成“日常入口与 fallback”。
  - 明确直接描述任务 / issue URL 是日常入口。
  - 明确 `trellis-continue`、`trellis-finish-work` 仍是常用显式入口。
- `trellis/workflows/guru-team/workflow.md`
  - 更新 Request Triage 与 `workflow-state:no_task`，强调自然语言分类和 auto-bootstrap。
  - 更新 Phase 0 描述，确保 task-like / issue-backed 请求仍触发 intake/preflight。
  - 更新 Rules 中的 primary entry point 表述。
- `trellis/workflows/guru-team/README.md`
  - 更新用户入口说明，不再把 start/continue/finish-work 并列为三个主流程。
- `trellis/presets/guru-team/README.md`
  - 更新 installed files 后的 entry point 说明，解释 start overlay 的 fallback 定位。
- `trellis/presets/guru-team/overlays/**/trellis-start*`
  - 将 description 和正文改为 fallback orientation。
  - 保留实际执行步骤：读取 `get_context.py` 与 phase context；无 active task 且 durable work 需要时执行 Phase 0 intake/preflight。
- 如搜索发现其它同义旧口径，按相同原则更新。

### 只在必要时修改

- `trellis/workflows/guru-team/config-template.yml`
  - 当前配置主要是 issue/preflight/publish 参数，没有直接入口心智模型配置。除非实现中发现注释会误导入口行为，否则不改。
- preset installer 脚本
  - 当前 installer 已可替换 known upstream-generated entry files；本任务预期只改 overlay 内容，不改 installer 行为。

### 不修改

- Trellis npm 上游、`node_modules`、全局 CLI。
- `.trellis/scripts/` 上游生成脚本。
- Branch Review Gate、finish-work、publish PR 的核心行为。

## 文案合同

统一使用下面的概念：

- **日常入口**：
  - 直接描述任务。
  - 贴 GitHub issue URL。
  - 说 “处理 issue #123”。
  - `trellis-continue`。
  - `trellis-finish-work`。
- **AI 责任**：
  - 无 active task 时先分类自然语言请求。
  - issue-backed / task-like / file-change 请求先走 Guru Team intake + base/worktree preflight。
  - 副作用前请求 consent。
- **start fallback**：
  - 平台无自动注入。
  - hook 未启用、未审批或疑似未运行。
  - 用户要求完整上下文报告或重新加载上下文。
  - 异常恢复或平台特殊入口。

## 数据流 / 运行流

```text
用户自然语言任务 / issue URL / issue number
  -> 平台注入 Trellis startup context / workflow-state / bootstrap reminder
  -> AI 判断 no active task 且请求需要 durable task
  -> check-env.sh --json
  -> prepare-task.sh --json "<request>"
  -> 汇报 source issue、duplicate、base branch、branch、workspace、current checkout、create command
  -> 用户 consent
  -> 创建 worktree / branch / Trellis task
  -> planning artifacts
  -> 用户 review 后 task.py start
```

显式 `trellis-start` fallback 进入时，流程从“读取上下文并判断 no active task”开始，后续 Phase 0 规则完全一致。

## 兼容性

- 已安装旧 overlay 的业务 repo 通过重新应用 preset 获得新文案。
- `trellis update` 仍由 marketplace workflow 和 preset installer 负责；本任务不改变 update 语义。
- start 文件路径和名称不变，避免破坏无自动注入平台或用户已有调用习惯。
- continue/finish-work 文件路径和语义不变。

## 风险与回滚

- 风险：只改部分文档导致 README 与 overlay 口径继续冲突。
  - 控制：对 `trellis-start`、`主入口`、`entry points`、`no_task`、`startup`、`bootstrap` 做全仓搜索。
- 风险：start 被误读为废弃，导致无自动注入平台失去入口。
  - 控制：所有 start 文案都明确 “保留为 fallback / explicit orientation”。
- 风险：auto-bootstrap 口径被误读为可以跳过 issue intake/preflight。
  - 控制：workflow-state:no_task 和 Phase 0 均明确 task-like 请求仍必须先 intake/preflight，再创建 task/worktree/branch。

## 验证策略

- 静态格式与脚本语法：
  - `python3 -m json.tool trellis/index.json`
  - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
  - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
  - `git diff --check`
- 文案一致性：
  - `rg -n "trellis-start|start / continue|用户主流程|主入口|entry points|workflow-state:no_task|no_task|UserPromptSubmit|SessionStart|startup|bootstrap" README.md trellis .trellis/tasks/07-03-2-align-guru-team-workflow-trellis`
  - 确认没有 “必须记住三个主入口” 或 start/continue/finish-work 并列为日常主入口的残留。

## Spec 更新判断

本任务可能暴露“runtime-parsed workflow template 和跨平台 overlay 文案必须同步”的重复规则。当前 `.trellis/spec/guides/cross-layer-thinking-guide.md` 已有 runtime template 与 cross-platform template consistency 规则，预期无需新增 spec；实现后如果发现缺口，再在 Phase 3.3 记录或更新。
