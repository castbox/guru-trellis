# 实施计划

## 前置核对

- [x] 读取 issue #8。
- [x] 核对 Trellis 官方 custom workflow / custom spec template marketplace 文档。
- [x] 读取 workflow / preset / shared guides。
- [x] 确认现有 preflight 不会自动更新 base branch。
- [x] 记录 durable docs SSOT：本仓库以 README、workflow README、preset README 和 `.trellis/spec/` 为长期说明。

## 实施步骤

1. 新增 artifact 通用工具
   - 复用现有 `load_review_report()` / hash 模式，提炼或新增 artifact digest helper。
   - 实现 task-local path 校验、sha256、size、modified_at、dirty paths。

2. 实现 planning approval gate
   - 新增 `record-planning-approval` / `check-planning-approval` Python subcommand。
   - 新增 bash wrapper。
   - 校验 `prd.md` 必须存在，复杂任务可通过 `--artifact design.md --artifact implement.md` 或默认存在即纳入。
   - 缺失、hash 变化、HEAD 变化、summary 空时 fail closed。

3. 实现 Phase 2 check report gate
   - 新增 `record-phase2-check` / `check-phase2-check` Python subcommand。
   - 新增 bash wrapper。
   - 支持 `--checked-artifact`、`--checked-spec`、`--coverage`、`--validation`、`--finding`。
   - P0/P1/P2 unresolved finding 或 HEAD/dirty stale 时 fail closed。

4. 实现 Branch Review Gate 独立审查来源
   - 为 `review-branch --pass` 新增 `--review-source independent-agent` 要求。
   - passed gate 拒绝空 reviewer、`*-main-session`、`self-review`。
   - `--review-report` 必须是 task-local `review.md`，拒绝 `prd.md` 等其他 artifact。
   - `review-gate.json` 写入 `verification_evidence.review_source`。
   - `validate_review_gate()` 拒绝缺 independent source 或 self-review 的旧/新 passed gate。
   - 单元测试覆盖缺来源、主会话 reviewer、合法独立 Agent 通过路径。

5. 实现 base freshness preflight
   - 在 `cmd_prepare()` / `prepare_workspace()` 前后加入 `git fetch` 与 base freshness evidence。
   - planner-only 输出风险，不创建 worktree、不写 handoff。
   - executor path 强制 fresh；优先使用 refreshed remote base 创建 worktree。
   - 更新 handoff schema 示例或保持 schema permissive，并在 README/workflow 中说明字段。

6. 更新 workflow / overlay / docs
   - `trellis/workflows/guru-team/workflow.md`
   - `.trellis/workflow.md`
   - `trellis/presets/guru-team/overlays/**/trellis-continue*`
   - `README.md`
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`
   - 必要时更新 `.trellis/spec/workflow/*`。

7. Preset 同步
   - 更新 installer `MANAGED_ASSET_PATHS`。
   - 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`。
   - 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
   - 处理 `.new` / `.bak`。

8. 验证
   - `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
   - `python3 -m json.tool trellis/index.json`
   - `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-8-auditable-evidence-planning-approval-trellis`
   - `python3 ./.trellis/scripts/get_context.py --mode phase`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.4`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.2`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.4`
   - `git diff --check`
   - 能力允许时运行 `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`；若完整 throwaway 因环境/网络限制无法完成，最终报告明确未验证项。

## Commit / Review / Publish 准备

- commit 前必须先写入并检查本任务自己的 `phase2-check.json`。
- commit 后执行完整 Branch Review Gate，范围为 `origin/main...HEAD`。
- PR body 必须中文、具体，`Closes #8` 只能在 ledger 验收证据和 Review Gate 覆盖后使用。

## 阻塞项

当前无阻塞项。进入实现前需要用户确认本规划 artifact 可作为 start 依据。
