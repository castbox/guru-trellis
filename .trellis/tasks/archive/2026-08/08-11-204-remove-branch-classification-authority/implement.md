# Implementation Plan

## Phase 1: Contract Migration

- [ ] 更新 `guru-create-task-commit` Skill、contract 与 interface，删除 routine eligibility 语义并定义 dialogue-local exact commit authority。
- [ ] 将 candidate schema/example/runtime identity 升级为 5.0，写明 4.0 完整 reprepare 迁移。
- [ ] 更新 workflow/data/companion/quality/preset/public docs 中 Issue #180 的旧资格条款。

## Phase 2: Runtime Removal

- [ ] 删除 Branch Rules API 读取与仅服务分支/发布分类资格的 helper、常量、candidate builder/checker/executor 分支。
- [ ] 保留并复核 task、repo、remote、target ref、HEAD、Phase 2、snapshot、scope、message、index/tree 与 unrelated preservation 校验。
- [ ] 审计 push、Publication、Finalizer、PR readiness、Merge 和 companion scripts，移除发现的同类主动门禁。

## Phase 3: Tests And Evals

- [ ] 将旧分支分类矩阵测试替换为标准 task branch、任意目标 ref、Rules 403/不可用不被调用、identity mismatch 与真实 mutation rejection 测试。
- [ ] 更新 package contract tests、runtime tests、preset installer tests、installed closeout、throwaway verifier 和 native eval adapter。
- [ ] 加入 banned-term 断言，禁止旧字段、`routine_auto_commit_*` 与 `/rules/branches/` 回归 current surfaces。

## Phase 4: Distribution

- [ ] 运行 preset `apply.sh --repo .` 同步 dogfood 与 Codex/Claude/Cursor/agents copies。
- [ ] 处理所有 `.new` / `.bak` 并运行 overlay drift checker。
- [ ] 检查 extension manifest/package inventory 与 schema id 一致。

## Phase 5: Validation

- [ ] 运行 task-commit package tests 与 runtime targeted tests。
- [ ] 运行完整 Python/shell/schema/preset/eval 验证。
- [ ] 运行 clean throwaway workflow/preset install 与 upgrade/update 验证。
- [ ] 执行 `guru-check-task` 完整 Phase 2 semantic gate。
- [ ] 独立 current-HEAD branch review 达到零 P0-P3 finding。

## Expected Commands

```bash
python3 -m unittest trellis.skills.guru-team.packages.guru-create-task-commit.tests.test_contract
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
git diff --check
```

## Rollback Points

- Candidate schema/runtime/package docs 必须作为一个版本单元回滚。
- generated copies 只能由 canonical + apply 重新生成，不保留任何不完整同步结果。
