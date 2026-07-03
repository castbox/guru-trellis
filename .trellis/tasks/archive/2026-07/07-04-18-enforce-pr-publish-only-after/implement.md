# #18 实现计划

## 前置状态

- Issue: https://github.com/castbox/guru-trellis/issues/18
- Branch: `codex/18-enforce-pr-publish-only-after`
- Worktree: `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/18-enforce-pr-publish-only-after`
- Base branch: `main`
- Middle-platform Knowledge Gate: 不适用。
- Docs SSOT: 无传统 `docs/`，本任务需同步 README、workflow README、preset README、workflow contract/spec 相关长期文件。

## 实现步骤

### 1. 现状搜索 `[completed]`

- 搜索 `publish-pr`、`finish-work`、`trellis-continue`、`push`、`PR`。
- 确认 canonical workflow、dogfood workflow、overlay、README、script 的所有触点。

### 2. 脚本门禁 `[completed]`

- 在 `guru_team_trellis.py` 中为 `publish-pr` 增加：
  - Python 内部 `from_finish_work` marker；
  - `--recovery-after-finish-work` 显式恢复 flag；
  - `validate_publish_invocation()`。
- 在 `cmd_publish_pr()` 最前面调用校验，确保失败发生在任何 push/PR 前。
- 在 `cmd_finish_work()` 内部调用 publish 时传 `from_finish_work=True`。
- 在 `guru_team_trellis.py` 中为 `finish-work` 增加：
  - `--from-trellis-finish-work` 显式 intent marker；
  - `validate_finish_work_invocation()`；
  - 校验放在 `cmd_finish_work()` 最前面，确保裸调失败发生在 repo/gate/archive/journal/push/PR 前。
- 同步 canonical `.trellis/guru-team/scripts/python/guru_team_trellis.py` 安装副本。

### 3. 测试 `[completed]`

- 阅读现有测试结构；如已有 `test_guru_team_trellis.py`，扩展；如没有，创建 focused unit tests。
- 覆盖：
  - direct `publish-pr` 默认失败；
  - direct `finish-work` 未带 intent marker 默认失败；
  - recovery dry-run 可通过；
  - finish-work 内部 publish dry-run 可通过或至少 helper 参数构造路径可验证。

### 4. Markdown 合同更新 `[completed]`

- 更新 `trellis/workflows/guru-team/workflow.md`。
- 同步 `.trellis/workflow.md`。
- 更新 preset overlays：
  - `.agents/skills/trellis-continue/SKILL.md`
  - `.agents/skills/trellis-finish-work/SKILL.md`
  - `.codex/prompts/trellis-continue.md`
  - `.codex/prompts/trellis-finish-work.md`
  - `.codex/skills/*`
  - `.claude/commands/trellis/*`
  - `.cursor/commands/*`
- 运行 preset apply 同步 dogfood 安装副本。

### 5. README / spec `[completed]`

- 更新 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` 中 publish 边界。
- 更新 `.trellis/spec/workflow/workflow-contract.md` 或 `companion-scripts.md`，固化可复用规则。

### 6. 验证 `[completed]`

运行：

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-18-enforce-pr-publish-only-after
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

新增测试命令按实际文件执行，例如：

```bash
python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis
```

如 Python package path 不适合 module import，则直接运行测试脚本。

实际验证结果：

- `python3 -m json.tool trellis/index.json` 通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh` 通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过。
- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过，9 个测试。
- `.trellis/guru-team/scripts/bash/publish-pr.sh --json --dry-run` 按预期失败，返回 `blocked_step=publish-pr` 和 `recovery_flag=--recovery-after-finish-work`。
- `.trellis/guru-team/scripts/bash/finish-work.sh --json --dry-run` 未带 intent marker 时按预期失败，返回 `blocked_step=finish-work` 和 `intent_flag=--from-trellis-finish-work`。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-18-enforce-pr-publish-only-after` 通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1`、`--step 3.5`、`--step 3.7` 通过，3.7 输出包含 direct publish block 规则。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 通过，并验证新安装仓库 direct `finish-work --dry-run` 与 direct `publish-pr --dry-run` 均被拒绝。
- `git diff --check` 通过，无 `.new` / `.bak` / `__pycache__` 残留。

### 7. Branch Review Gate 和 finish-work `[pending]`

- 完成实现和验证后，更新 `issue-scope-ledger.json` 的 acceptance evidence。
- 提交本任务变更。
- 以 code-review stance 检查 `origin/main...HEAD` 完整 diff。
- 记录 Branch Review Gate。
- 最后运行 `trellis-finish-work`，由 finish-work 自动 publish PR。

## 回滚策略

- 如果脚本门禁导致 finish-work publish 失败，优先修正内部 flag 传递。
- 如果 recovery 路径过宽，收紧 flag help 和校验位置。
- 如 overlay 同步产生 `.new` / `.bak`，逐个检查，不提交未处理冲突文件。
