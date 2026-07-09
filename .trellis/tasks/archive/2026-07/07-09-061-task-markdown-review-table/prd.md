# #61 阶段回复必须提供 Markdown task 产物 review 表

## 目标

用户在任意 Guru Team 阶段收到 Agent 回复时，都能从最近一次回复打开当前 task 的关键 Markdown 产物进行 review，不需要翻找旧会话消息，也不需要把机器 JSON 证据当作常规入口。

## 背景与证据

- Live issue: https://github.com/castbox/guru-trellis/issues/61。
- Issue 明确非目标：不要求历史消息里的旧链接永久有效；不改变 `task.py archive` 的物理归档语义；不为旧路径创建 symlink、stub 或 pointer 目录；标准人类 review 表不默认列 JSON artifact。
- 官方 Trellis `custom-workflow` 文档说明 `.trellis/workflow.md` 是 workflow 行为集中定义，`[workflow-state:STATUS]` 由 hook 运行时解析；因此阶段输出规则应落在 workflow / skill / prompt Markdown，而不是 hook 或上游源码。
- 官方 spec template marketplace 文档说明 spec template 只放可复用工程约定、规则、checklist 和去敏例子，不放 active task state；本任务不修改 spec template marketplace 内容。
- 本仓库 spec 要求：canonical workflow 是 `trellis/workflows/guru-team/workflow.md`，dogfood active copy 是 `.trellis/workflow.md`；overlay 改动必须从 `trellis/presets/guru-team/overlays/` 同步到 dogfood 安装副本。

## 需求

1. 增加 deterministic Markdown artifact resolver，能根据当前 repo root 和 task 参数解析 active task 或 archive task 目录。
2. Resolver 的标准人类 review 产物只包含 Markdown 文件：
   - `prd.md`
   - `design.md`
   - `implement.md`
   - `review.md`
   - `pr-body.md`
3. Resolver 返回每个产物的 label、filename、用途、存在性、状态、repo-relative path 和 absolute path；不存在的产物不得产生可点击死链。
4. Resolver 只负责路径、archive 状态和存在性事实，不读取或展示 `planning-approval.json`、`phase2-check.json`、`review-gate.json`、`pr-readiness.json`、`issue-scope-ledger.json`、`agent-assignment.json` 等机器 JSON。
5. Guru Team workflow、`trellis-continue`、`trellis-finish-work` 及对应平台 prompt / command overlay 必须要求：每个阶段停止点或完成回复都调用 resolver，并输出“Markdown 产物 review 表”。
6. `finish-work` dry-run 后必须输出当前 active task 路径表；正式 `finish-work` archive 后必须重新 resolve，并在最终回复输出 archive 后路径表。
7. Branch Review Gate 后表格必须包含 `review.md`，用途说明为 AI/human review 报告；raw `reviews/*.md` 通过 `review.md` 链接进入，不进入默认表格。

## 非目标

- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 不把 AI 阶段判断写进 Python / shell；脚本只做 Executor / Validator / Recorder / deterministic resolver。
- 不改变 `task.py archive` 行为，不创建旧路径 symlink/stub。
- 不改变 PR publish、review gate、planning approval 的通过条件。
- 不在标准表格默认展示 JSON artifact；排障时可在额外“机器证据”段落单独列 JSON。
- 不把本 issue 的 task artifact 或业务私有规则放入 spec template marketplace。

## 验收标准

- Phase 1 planning 审查回复包含 `prd.md`、`design.md`、`implement.md` 的 Markdown 产物表。
- Phase 2 实现 / check 完成回复包含同一张表，并正确标记未生成的 `review.md` / `pr-body.md`。
- Branch Review Gate 通过或失败后回复包含 `review.md` 行，并说明它是 AI/human review 报告。
- `trellis-finish-work --dry-run` 预览后回复包含 active task 路径的 Markdown 产物表。
- 正式 `trellis-finish-work` 完成并 archive 后，最终回复重新 resolve，表格链接指向 `.trellis/tasks/archive/YYYY-MM/<task>/...`。
- 标准表格不列 `review-gate.json`、`phase2-check.json`、`pr-readiness.json`、`issue-scope-ledger.json`、`agent-assignment.json`。
- 新增 helper 在 active task、archived task、缺失 artifact 场景均有回归验证。
- 修改 workflow / preset / overlay 后完成 dogfood overlay 同步和 drift 检查；若不能跑完整 throwaway 安装，最终说明必须列明未覆盖风险。

## Docs SSOT 与知识门禁

- Durable docs 已存在：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`docs/requirements/README.md`。
- 本任务改变 Guru Team workflow / companion script 行为，需同步 canonical workflow、dogfood workflow、preset README installed files、公开 README 或 workflow README 中的日常入口说明。
- Middle-platform Knowledge Gate 不适用：本任务不涉及 `go-guru`、`proto-guru`、Unity、Flutter 或 Guru Team middle-platform SDK。

## 开放问题

无。Issue 对范围、非目标和验收标准已经足够明确。
