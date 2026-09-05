# 实施计划

1. 修改 canonical Merge eval corpus，删除 `no_github_write` assertion。
2. 运行 Merge package tests，确认 route coverage 和
   `mutation.assert_not_called()` 仍通过。
3. 运行 eval schema/source package 定向验证。
4. 执行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 同步 dogfood 与平台投影，
   检查并处理 `.new`/`.bak`。
5. 运行 installed package validator、平台 byte equality、preset reapply 和
   `check-dogfood-overlay-drift.sh`。
6. 运行 `git diff --check` 和 task validation，确认变更只包含 task artifact 与受管理的
   Merge eval corpus 投影。
7. 完成 Phase 2 check、task commit、Branch Review、Publication、Finalizer 和 PR merge。
8. 合并后 fresh fetch `origin/main`，冻结新 SHA/tree，并从零重跑 #332 Stage 2 Release Gate。

## 重点验证命令

```bash
python3 -m unittest trellis.skills.guru-team.packages.guru-merge-task-pr.tests.test_contract
python3 trellis/skills/guru-team/runtime/validate.py --help
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 ./.trellis/scripts/task.py validate 09-05-332-merge-eval-trace-contract
git diff --check
```

具体 validator argv 以当前脚本 `--help` 和 Release Skill 合同为准，不凭历史命令猜测。

