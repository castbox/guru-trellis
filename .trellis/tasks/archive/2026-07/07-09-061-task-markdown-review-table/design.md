# #61 详细设计

## 设计原则

本任务遵循“Markdown 定义流程，脚本执行事实”的仓库边界：

- AI 判断：哪些阶段算完成、表格是否足够、PR readiness 是否真实充分，仍由 workflow / skill / prompt Markdown 约束 AI 执行。
- Deterministic script：只解析 task 目录、archive 状态、Markdown 文件存在性和路径，返回可审计事实。
- 不修改 hook parser，不修改 Trellis upstream，不依赖历史会话消息。

## Resolver 合同

新增 companion subcommand 和 Bash wrapper：

```bash
.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task <task-path-or-name>
```

Python 子命令：

```text
guru_team_trellis.py resolve-human-artifacts
```

输入：

- `--root` 可选，默认当前 repo root。
- `--task` 可选，缺省时使用当前 task 或 handoff task。
- `--json` 输出 JSON。默认 stdout 仍是 JSON，保持 companion script 风格。

输出字段：

```json
{
  "status": "ok",
  "task_dir": "<absolute task dir>",
  "task_dir_relative": ".trellis/tasks/<task> 或 .trellis/tasks/archive/YYYY-MM/<task>",
  "archived": false,
  "markdown_artifacts": [
    {
      "label": "PRD",
      "filename": "prd.md",
      "purpose": "需求、范围、验收标准",
      "exists": true,
      "status": "已生成",
      "path": ".trellis/tasks/<task>/prd.md",
      "absolute_path": "<absolute path>",
      "link": "<absolute path or empty string>"
    }
  ]
}
```

默认五个 Markdown artifact：

| label | filename | missing status | purpose |
| --- | --- | --- | --- |
| PRD | `prd.md` | `未生成` | 需求、范围、验收标准 |
| Design | `design.md` | `未生成` | 技术设计与取舍 |
| Implement Plan | `implement.md` | `未生成` | 执行计划与验证计划 |
| Review Report | `review.md` | `未执行` | AI/human review 报告 |
| PR Body | `pr-body.md` | `未生成` | 给 GitHub reviewer 的 PR 说明 |

存在时状态统一为 `已生成`。是否 `不适用` 由 AI 根据阶段语义在回复中调整；resolver 不做阶段判断。

## 路径解析

复用现有 `resolve_existing_task_dir()`：

1. 接受 absolute path、repo-relative path、task name。
2. 优先 active task。
3. active task 不存在时查找 `.trellis/tasks/archive/YYYY-MM/<task>/`，按月份倒序。
4. 只接受包含 `task.json` 的目录。

归档识别：

- `task_dir_relative` 以 `.trellis/tasks/archive/` 开头时 `archived=true`。
- active task 为 `archived=false`。

## Workflow / overlay 输出合同

在 canonical workflow 和 overlay 中加入统一规则：

- 阶段停止点或阶段完成回复必须先运行 resolver。
- AI 按 resolver 结果渲染表格。
- 表格只列 resolver 返回的五个 Markdown 文件。
- `exists=false` 行不得输出 Markdown 链接。
- `finish-work` 正式 archive 后必须重新运行 resolver，再输出 archive 后路径表。

覆盖入口：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-finish-work/SKILL.md`
- `.agents/skills/trellis-continue/SKILL.md`
- `.agents/skills/trellis-finish-work/SKILL.md`
- `.codex/prompts/trellis-continue.md`
- `.codex/prompts/trellis-finish-work.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.codex/skills/trellis-finish-work/SKILL.md`
- Claude / Cursor continue 和 finish-work overlay。

## Installer / upgrade 合同

新增 wrapper 属于 managed companion asset：

- canonical source: `trellis/workflows/guru-team/scripts/bash/resolve-human-artifacts.sh`
- installed target: `.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh`
- installer `MANAGED_ASSET_PATHS` 必须新增该文件。
- preset README installed files 必须新增该文件。
- `trellis/guru-team-extension.json` 和 installed `.trellis/guru-team/extension.json` 可增加 capability / script 记录，保持 additive。

改 overlay 后必须运行：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

若产生 `.new` / `.bak`，逐个检查处理。

## 测试设计

新增 Python unit test 覆盖 resolver：

- active task：只返回 Markdown artifacts，存在文件给 path/link。
- archived task：同名 active 不存在时解析 archive 路径。
- missing artifact：状态为 `未生成` 或 `未执行`，`link` 为空。
- JSON artifact exclusion：输出不包含 `review-gate.json`、`phase2-check.json`、`pr-readiness.json` 等。

补充 grep / context 验证：

- `get_context.py --mode phase --step 1.4`
- `get_context.py --mode phase --step 2.2`
- `get_context.py --mode phase --step 3.5`
- `get_context.py --mode phase --step 3.6`
- overlay drift check。

## 风险与回滚

- 风险：只改 workflow 不改平台 overlay，导致某些平台仍不输出表格。缓解：搜索并同步 all overlay copies，再跑 dogfood drift。
- 风险：helper 输出死链。缓解：不存在时 `link=""`，AI 不渲染链接。
- 风险：脚本越界做 AI 判断。缓解：resolver 不读阶段状态、不读 JSON gate、不判断充分性。
- 回滚：删除新增 wrapper/subcommand，并回退 workflow / overlay 文案；不影响 task.py archive 或现有 gate artifact。
