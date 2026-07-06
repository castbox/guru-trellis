# 实施计划

## 执行步骤

1. 搜索所有 `review-branch.sh` findings/pass 示例和 `review-source` 文案，锁定 canonical 与 dogfood copy 差异。
2. 修改 `guru_team_trellis.py`：
   - Branch Review Gate 所有记录路径都校验 `review_source=independent-agent` 与非 main-session reviewer。
   - `conclusion.passed` 由显式 `--pass` 和 zero findings 共同决定。
3. 修改 canonical workflow 与 dogfood workflow 中 findings 示例。
4. 修改 preset overlay 的 continue 入口，明确 findings path 也必须携带 `--review-source independent-agent` 与 task-local `review.md`。
5. 补充 `test_guru_team_trellis.py` 回归测试：
   - pass path 正常记录。
   - `P3` finding + no `--pass` 记录 `passed=false`。
   - `P3` finding + `--pass` 被阻断。
   - findings path 缺 `review_source` 被阻断。
   - findings path 缺 `review_report` 被阻断。
6. 运行 preset apply 同步 dogfood installed copies。
7. 运行验证命令并记录 Phase 2 check artifact。

## 验证命令

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-39-review-branch-findings-reviewer-only
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
git diff --check
```

## 开箱即用 / upgrade-update 门禁

- 本任务修改 workflow / preset / overlay / companion script，必须至少完成 dogfood overlay apply + drift check。
- 若时间允许，使用临时目录做 throwaway install/update 抽样验证；如果未跑完整新仓库安装，最终报告必须明确未验证项。

## 回滚点

- 如果脚本测试失败且短时间无法收敛，回滚 `guru_team_trellis.py` 与测试变更，保留 task artifacts 说明阻塞。
- 如果 preset apply 产生 `.new` / `.bak`，逐个检查来源；未处理前不提交。
