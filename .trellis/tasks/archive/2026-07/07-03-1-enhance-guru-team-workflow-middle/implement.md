# 实施计划

## 实现前知识核对

- 已核对官方 Trellis 文档：`workflow.md` 是 workflow 主控制面，config 缺省 key 走默认，hooks 不适合承载核心阻塞门禁，日常入口是 skill-first / continue / finish-work。
- 已检索 `guru-knowledge-center` middle-platform，trace id：`6218cc88-6450-427f-8b4f-79be47d49944`。
- 本任务不需要引入具体 go-guru 代码规范，只需要在 reusable workflow 中要求相关任务自行检索并持久化 citation。

## 文件修改顺序

1. 修改 `trellis/workflows/guru-team/workflow.md`
   - Phase 1 增加中台知识门禁和 docs SSOT discovery。
   - Phase 2 增加实现前知识核对。
   - Phase 3 增加 docs SSOT reconciliation。
   - Branch Review Gate evidence 增加 docs SSOT reconciliation 覆盖要求。
   - Rules 增加配置默认、MCP runtime detection、docs SSOT 规则。
2. 修改 `trellis/workflows/guru-team/config-template.yml`
   - 增加 `middle_platform_knowledge.mode: optional_warn` 和 allowed values 注释。
3. 修改 `trellis/workflows/guru-team/README.md` 与 `trellis/presets/guru-team/README.md`
   - 说明新增门禁、默认兼容行为和 installer preserve 语义。
4. 修改 platform overlays
   - `.agents` / `.codex` skill entries。
   - `.codex/prompts`。
   - `.claude/commands` 与 `.cursor/commands`。
   - 只放短提醒，详细规则指向 `.trellis/workflow.md`。
5. 根据实际变更决定是否需要修改 preset installer；当前设计预计不修改 installer。

## 验证命令

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
git diff --check
```

如果 platform overlay 或 installer 行为实际改变，再用临时 Trellis project 运行 preset installer，验证未知本地改动写 `.new` 而非覆盖。

## 回滚点

- 文档和 overlay 修改可按文件回滚。
- 若 validation 显示 shell / Python 文件未变但命令失败，先确认文件是否存在及 glob 展开，再修正验证命令或实际脚本问题。

## 完成判定

- 所有 AC 在 PRD 中可映射到具体文件变更。
- `issue-scope-ledger.json` 的 `close_issues` 只有 #1。
- 验证命令通过，并在 review gate 中记录 docs SSOT / deployment impact judgment。

## 执行记录

- 已同步 `trellis/workflows/guru-team/workflow.md` 与 dogfood 运行时 `.trellis/workflow.md`，`get_context.py --mode phase --step 1.1/2.1/3.5` 能读取新增门禁内容。
- 已更新 `trellis/workflows/guru-team/config-template.yml`，新增 `middle_platform_knowledge.mode: optional_warn`，并在 workflow/README 中声明缺失 key 的兼容默认。
- 已更新 workflow README、preset README、根 README 和 `trellis/index.json`，说明 Middle-platform Knowledge Gate 与 Repo Docs SSOT reconciliation。
- 已同步 `.agents`、`.codex`、`.claude`、`.cursor` 的 start / continue / finish-work overlay 提醒；详细规则仍以 `.trellis/workflow.md` 为 SSOT。
- preset installer 逻辑未改；用临时 Trellis-like repo 验证已有 `.trellis/guru-team/config.yml` 保留、未知本地 `.codex/skills/trellis-continue/SKILL.md` 生成 `.new`。

## Docs SSOT reconciliation

- 本仓库没有 `docs/` 目录；长期文档 SSOT 是 marketplace workflow、workflow/preset README、根 README 和 platform overlays。
- 本任务改变的是 reusable workflow 行为与安装说明，已更新对应 durable docs：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- task artifact 中的 issue intake、官方文档核对和中台知识检索记录只作为本任务归档证据，不另建长期 `docs/`。
- 不需要新增 `.trellis/spec/`：本次可复用规则已经进入 workflow 主合同与 README，未新增代码签名、API、数据库、环境变量或脚本行为合同。

## 验证结果

- `python3 -m json.tool trellis/index.json`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：通过。
- `git diff --check`：通过。
- `python3 ./.trellis/scripts/task.py validate 07-03-1-enhance-guru-team-workflow-middle`：通过。
- 临时 preset installer preserve / `.new` 验证：通过。
