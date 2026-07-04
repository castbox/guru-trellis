# #17 实施计划

## 前置检查

- 已读取 issue #17、参考 PR #184/#95、官方 Trellis custom workflow / custom spec template marketplace 文档。
- 已读取 `.trellis/spec/workflow/`、`.trellis/spec/preset/`、`.trellis/spec/docs/` 和 shared guides。
- Middle-platform Knowledge Gate：不适用。
- Docs SSOT：无 `docs/` 目录，更新现有 README / workflow README / preset README / spec。

## 实施步骤

1. 补任务 artifact：
   - 完成 `prd.md`、`design.md`、`implement.md`。
   - 创建 `issue-scope-ledger.json`，默认 close #17，验收证据在实现验证后补齐。
   - 为 inline Codex 保留 `implement.jsonl` / `check.jsonl`，可填入相关 spec 作为上下文记录。
2. 修改 canonical workflow 与 dogfood workflow：
   - Phase 3 publish 增加 PR body readiness 标准。
   - 明确 AI 先审查/生成 body file，脚本只做结构校验和执行发布。
3. 修改 finish-work overlay：
   - `.agents`、`.codex`、`.claude`、`.cursor` 的 canonical overlay 入口增加 PR body readiness 要求和 `--body-file` 传递说明。
   - 运行 preset apply 同步 dogfood 副本。
4. 修改 companion script：
   - 增加 `--body-file` / 可选 `--body-artifact` 参数。
   - 实现 `load_pr_body`、`validate_pr_body_quality` 等标准库 helper。
   - fallback body 改成自解释结构，并让缺少具体 validation/影响范围时 fail closed。
5. 修改测试：
   - 单元测试低信息量 body 被拒绝。
   - 单元测试包含具体摘要/影响范围/验证/安全说明的 body 通过。
   - 单元测试 `--body-file` 优先于 fallback。
6. 更新文档与 spec：
   - README、workflow README、preset README 增加 PR body 质量标准。
   - `.trellis/spec/workflow/quality-guidelines.md` 或 `workflow-contract.md` 增加发布 body 检查项。
7. 验证：
   - `python3 -m json.tool trellis/index.json`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-17-improve-guru-team-pr-body`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.7`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `git diff --check`

## Review Gate 准备

提交前运行 `trellis-check` 语义检查并补 issue ledger 验收证据。提交后在 `trellis-continue` 内完成完整 Branch Review Gate，写 task-local `review.md`，再用 `review-branch.sh` 记录 `review-gate.json`。本入口不会 push、创建 PR 或调用 finish-work。

## 执行记录

- 已实现 `publish-pr --body-file` / `--body-artifact`，并在 `finish-work` 内部 publish 参数中透传。
- 已新增 PR body reviewer-readability 校验：必填 section、低信息量短语、具体内容、Issue Scope Ledger close/ref 语义。
- 已改写 fallback PR body，不再输出“当前 Trellis task / 已提交实现与文档更新”作为默认摘要。
- 已同步 canonical workflow、dogfood workflow、finish-work overlays、README、workflow README、preset README 与 workflow spec。
- 已运行 preset apply 同步 dogfood 副本，并处理 `.bak` 备份。

## Docs SSOT Reconciliation

- 本任务改变 Guru Team workflow / publish helper 的长期发布合同，已更新长期 SSOT：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/quality-guidelines.md`、`.trellis/spec/workflow/companion-scripts.md`。
- Task artifact 中的实现细节和验证命令保留为任务历史；长期规则已合并到 workflow、README 和 spec。
- 本仓库无独立 `docs/` 目录，本任务不新增 `docs/`。

## 验证记录

- `python3 -m json.tool trellis/index.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-17-improve-guru-team-pr-body`
- `git diff --check`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.7`
- 手工 dry-run：合格 `--body-file` 可通过 `publish-pr --recovery-after-finish-work --dry-run`；低信息量 `--body-file` 被 `Publish blocked because PR body is not reviewer-readable` 阻塞。
