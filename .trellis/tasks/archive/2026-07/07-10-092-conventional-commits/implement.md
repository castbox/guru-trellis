# #92 实施计划

## 前置状态

- worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/092-conventional-commits`
- branch：`codex/092-conventional-commits`
- base：`main`，创建时已 fast-forward 到 `origin/main`
- source issue：`https://github.com/castbox/guru-trellis/issues/92`

## 执行步骤

1. 更新 durable workflow/spec/docs。
   - 修改 `trellis/workflows/guru-team/workflow.md`。
   - 同步 `.trellis/workflow.md`。
   - 修改 `trellis/workflows/guru-team/README.md`。
   - 修改 `trellis/presets/guru-team/README.md`。
   - 修改 `.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/workflow/quality-guidelines.md`。

2. 实现 companion 校验与格式化。
   - 修改 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
   - 新增 wrapper：`trellis/workflows/guru-team/scripts/bash/check-commit-messages.sh`。
   - 新增 wrapper：`trellis/workflows/guru-team/scripts/bash/format-merge-commit.sh`。
   - 更新 `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 的 `MANAGED_ASSET_PATHS`。

3. 接入 finish/publish。
   - `finish-work` metadata commit subject 使用 `chore(trellis): #92 固化任务收尾元数据` 形态。
   - `publish-pr` dry-run 输出 placeholder merge 指令。
   - `publish-pr` 正式路径在 PR URL 返回后输出带真实 PR number 的 merge 指令。

4. 补测试。
   - 在 `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 增加 issue #92 正反例。
   - 覆盖工作提交 body、metadata 空 body、merge body。
   - 覆盖 finish-work metadata subject 与 publish merge payload。

5. 同步 dogfood。
   - 执行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
   - 执行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
   - 检查并处理 `.new` / `.bak`。

6. Phase 2 check 与提交前验证。
   - `python3 -m json.tool trellis/index.json`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-10-092-conventional-commits`
   - `python3 ./.trellis/scripts/get_context.py --mode phase`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.4`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `git diff --check`

7. 开箱与 upgrade/update 验证。
   - 执行 `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`。
   - 验证 `trellis/index.json` 可解析。
   - 验证 `trellis workflow --marketplace ... --create-new` preview 路径。
   - 若当前分支 marketplace source 无法被 throwaway 安装读取，最终报告列为未覆盖风险。

8. Commit 与 review gate。
   - 运行提交规范校验器覆盖本分支新增提交。
   - 使用合规工作提交 message：

```text
chore(workflow): #92 强制中文 Conventional Commits 合同

背景：
issue #92 要求工作提交、metadata 提交和 merge commit 使用统一中文 Conventional Commits 规范，避免 git log、release、审计和 issue 追踪口径漂移。

变更：
- 固化 workflow、docs、spec 和 companion script 的提交规范合同。
- 增加 commit message 校验、merge commit 格式化和 finish/publish 接入。

边界：
不改写历史提交，不自动执行 GitHub PR merge，不把 AI review 充分性判断写入脚本。

验证：
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`

Refs #92
```

## Phase 2 检查重点

- 提交规范合同是否在 canonical workflow、dogfood workflow、README、spec、script、tests 中一致。
- Python / shell 是否只做 objective validator / formatter / executor。
- `Closes #92` 是否只保留在 PR body。
- `Refs #92` 是否出现在工作提交 body footer。
- metadata commit 是否不写 body。
- merge commit subject/body 是否由 publish payload 明确输出。

## 回滚点

- Durable docs 改动后若规划范围变化，回到 Phase 1 重审。
- Python helper 单测失败时，不进入 dogfood apply。
- dogfood drift 或 `.new` / `.bak` 未处理时，不提交。
- throwaway 安装失败时，最终报告必须列出失败命令和未覆盖门禁。
