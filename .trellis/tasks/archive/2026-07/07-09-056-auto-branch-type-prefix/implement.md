# #56 Implementation Plan

## Ordered Steps

1. 更新 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`：
   - 增加合法 branch type 常量和 deterministic inference helper。
   - 让 `prepare_naming_payload()` 在 `--branch` 缺省时使用 `<type>/<unique_prefix>`。
   - 让 `naming_override_flags()` 使用推断类型生成 `--branch` 示例。
   - 保留显式 `--branch` 覆盖。
2. 更新配置与 durable docs：
   - `trellis/workflows/guru-team/config-template.yml`
   - `README.md`
   - `trellis/workflows/guru-team/README.md`
   - `trellis/workflows/guru-team/workflow.md`
   - `.trellis/workflow.md`
   - `docs/requirements/requirement-main.md`
3. 更新单测：
   - 覆盖所有 11 个 branch type 的推断。
   - 覆盖 unknown fallback 为 `chore`。
   - 覆盖显式 `--branch` 覆盖。
   - 更新旧的 `codex/...` 断言。
4. 如改动涉及 overlay 或 preset installer 文件，运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 并处理 `.new` / `.bak`；若未改 overlay，则记录不适用。
5. 执行验证命令并写入 Phase 2 check evidence。

## Validation Commands

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-056-auto-branch-type-prefix
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 0.4
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

## Review Gates

- Planning approval gate: 展示 `prd.md`、`design.md`、`implement.md` 后取得用户明确确认，再记录 `planning-approval.json` 并启动 task。
- Phase 2 check gate: 在 commit 前完成 full task scope check，并记录 `phase2-check.json`。
- Branch Review Gate: commit 后由 independent review agent 审查 `origin/main...HEAD` 完整 diff，再记录 `review.md` 与 `review-gate.json`。

## Rollback

如推断规则造成不可接受的分支类型，回滚脚本 helper 与测试改动，并保持文档回退到旧固定前缀说明。回滚不得删除 task artifact 或 Issue Scope Ledger。
