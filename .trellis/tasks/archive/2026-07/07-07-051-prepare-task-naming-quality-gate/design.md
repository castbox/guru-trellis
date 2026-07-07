# #51 设计：prepare-task 命名质量门禁

## 背景与边界

本任务修改 Guru Team workflow companion script，不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。长期源头必须在 canonical marketplace / preset 文件中：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `README.md`

改动 canonical 后同步 dogfood 安装副本：

- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/schemas/intake-handoff.schema.json`
- `.trellis/workflow.md`

## 命名合同

新增 `naming_quality` 为 prepare payload 的一等字段：

```json
{
  "ok": false,
  "reason": "slug is low-information; provide semantic English naming overrides",
  "requires_semantic_name": true,
  "current_slug": "52-issue-52",
  "suggested_override_flags": [
    "--short-name 052-resume-detail-inline-attachment-preview",
    "--workspace-slug 052-resume-detail-inline-attachment-preview",
    "--task-slug 052-resume-detail-inline-attachment-preview",
    "--branch codex/052-resume-detail-inline-attachment-preview"
  ]
}
```

`current_slug` 使用最终用于 workspace/task 的核心 slug；当 `task_slug` / `workspace_slug` 不一致时，`reason` 应指出 create 路径会检查所有命名 surface。

## 质量判定

实现纯标准库 helper：

- `normalize_slug_candidate(value)`：去掉 branch prefix 后按 slug token 解析，不做中文转换。
- `slug_business_tokens(value)`：只认 ASCII 字母数字 token，过滤 issue 编号和通用词。
- `evaluate_slug_quality(...)`：返回稳定 dict，识别低信息模式。
- `ensure_naming_quality_for_create(payload)`：executor 路径 fail closed。

判定规则：

- `issue-<n>`、`<n>-issue-<n>`、纯编号直接失败。
- token 全部是通用词或编号时失败。
- 少于两个业务 token 时失败；语义判断必须通过 `--short-name` 接入，`--branch`、`--task-slug`、`--workspace-slug` 与 `--short-name` 保持同一业务语义，不能只覆盖三面名称而留下低信息 handoff `slug`。
- source issue title / requirement 含非 ASCII 且自动名未通过时，`requires_semantic_name=true`，提示 agent 传入英文语义名。
- 不引入 transliteration，也不把中文转拼音。

## Executor 阻断点

`cmd_prepare()` 当前先计算命名，再进入 `prepare_workspace()` / `create_task()`。新的门禁放在所有副作用之前：

1. 计算 `issue_slug`、`task_slug`、`workspace_slug`、`branch_name`。
2. 计算 `naming_quality` 并写入 payload。
3. 当 `args.create_worktree` 或 `args.create_task` 为真且 `naming_quality.ok=false` 时抛出 `WorkflowError(exit_code=2)`。
4. 错误 payload 带上 `naming_quality` 和 recommended override flags。

这样只读 planner 保持可用，create 路径阻断低信息命名。

## 显式覆盖

显式覆盖是 agent 把语义判断传给确定性脚本的接口：

- `--short-name`
- `--workspace-slug`
- `--branch`
- `--task-slug`

覆盖优先于自动生成，但覆盖值同样进入质量检查。`--branch codex/foo` 检查去掉 `codex/` 后的 `foo`。

## 文档与安装副本

文档更新点：

- Phase 0 handoff review 增加 `naming_quality` 和语义 short-name 说明。
- README / preset README 的 prepare-task 章节说明中文标题不走拼音默认命名。
- workflow README 说明推荐格式和 create 路径阻断语义。

同步策略：

1. 先修改 canonical。
2. 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 同步 dogfood overlay。
3. 如 `apply.sh` 产生 `.bak` / `.new`，逐个处理。
4. 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。

## 测试设计

在 `test_guru_team_trellis.py` 增加 prepare 命名测试：

- 英文 issue title 自动生成业务 slug 且 `naming_quality.ok=true`。
- 中文 issue title 未覆盖时只读 planner 输出 `ok=false`、`requires_semantic_name=true`，并保持无副作用。
- 中文 issue title 未覆盖时 `create_worktree` 抛 `WorkflowError(exit_code=2)`，不调用 workspace 副作用。
- 显式 `--short-name 052-resume-detail-inline-attachment-preview` 通过，并生成 `task_slug` / `workspace_slug` / `branch_name`。
- 低信息显式 `--short-name issue-52` create 路径阻断。

最小 CLI 验证额外覆盖实际命令输出 JSON。

## 风险与兼容

- 新字段 additive，schema 使用 `additionalProperties: true`，老消费者可忽略。
- 对英文短标题可能更严格。为降低误伤，planner 不阻断，只在 create 路径阻断，并给出覆盖参数。
- 已安装旧仓库需要通过 preset apply/update 同步脚本；本任务验证 dogfood overlay drift，但完整 throwaway install 如时间不足需在最终说明中标明。
