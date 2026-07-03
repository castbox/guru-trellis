# #2 实施计划：Guru Team auto-bootstrap 入口心智模型对齐

## 执行清单

1. 范围搜索
   - 搜索 `trellis-start`、`start / continue`、`用户主流程`、`主入口`、`entry points`、`workflow-state:no_task`、`UserPromptSubmit`、`SessionStart`、`startup`、`bootstrap`。
   - 记录必须同步修改的 README、workflow、preset README、overlay 文件。
2. 更新 workflow 主合同
   - 更新 Request Triage 和 `workflow-state:no_task`。
   - 更新 Phase 0 / Rules 中与入口有关的旧表述。
   - 保留 issue intake、duplicate search、base/worktree preflight、consent、Issue Scope Ledger 规则。
3. 更新公开文档
   - `README.md`
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`
4. 更新平台 overlay
   - `.agents/skills/trellis-start/SKILL.md`
   - `.codex/prompts/trellis-start.md`
   - `.codex/skills/trellis-start/SKILL.md`
   - 如搜索发现其它平台 start overlay，按同一口径同步。
   - 检查 continue/finish-work 是否仍保持常用显式入口，不需要改动则不改。
5. 复查 `config-template.yml`
   - 只在注释会误导入口行为时修改。
6. 更新验收证据
   - 在 `issue-scope-ledger.json` 中补 close issue 的 acceptance evidence。
7. 运行验证命令
   - `python3 -m json.tool trellis/index.json`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `git diff --check`
   - 文案残留搜索。
8. Phase 2 check
   - inline 模式下主会话直接检查 task artifacts、spec、diff 与验收标准。
9. Phase 3
   - 判断是否需要 spec update。
   - 提交 task artifacts、文档和 overlay 变更。
   - 提交后运行 Branch Review Gate。
   - finish-work 自动 archive、journal、publish PR。

## 需要重点审查的文件

- `README.md`
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-start.md`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-start/SKILL.md`
- `trellis/workflows/guru-team/config-template.yml`（只读复查，必要时改）

## 回滚点

- 文档与 overlay 修改集中在 Markdown 文件；如发现口径错误，可按文件级 diff 回滚。
- 不改 installer 行为，降低运行时回归面。
- 不改脚本逻辑，验证失败时优先检查误改文件范围。

## 验证命令

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
git diff --check
rg -n "必须记住三个主入口|用户主流程仍然只有|start / continue /|trellis-start.*trellis-continue.*trellis-finish-work|entry points limited to start" README.md trellis
```

## 开始实现前门禁

- `prd.md`、`design.md`、`implement.md` 已完成中文规划。
- `issue-scope-ledger.json` 已从 handoff 种子复制。
- 用户确认可以从 planning 进入 implementation。

## 执行结果

- 已更新 README、workflow README、preset README，将日常入口改为自然语言任务 / issue URL / issue number / `trellis-continue` / `trellis-finish-work`。
- 已更新 `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`，在 Request Triage、`workflow-state:no_task` 和 Rules 中明确 auto-bootstrap、issue intake + worktree preflight、consent 规则。
- 已同步更新 preset overlay 与本仓库安装副本中的 `trellis-start`，将其定位为 fallback / explicit orientation。
- 验证通过：
  - `python3 -m json.tool trellis/index.json`
  - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
  - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
  - `git diff --check`
  - 旧口径残留搜索未命中。
- Spec 更新判断：不需要更新 `.trellis/spec/`。本任务未新增命令/API/配置合同，且现有 `.trellis/spec/guides/cross-layer-thinking-guide.md` 已覆盖 runtime-parsed template 和 cross-platform template consistency。
