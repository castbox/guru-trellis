# Implementation Plan: GitHub CLI-only platform operations

## Phase 1: Inventory And Durable Contract

- [ ] 枚举 current canonical、runtime、public Skill、preset/platform 与 README 中所有 GitHub reads/writes、repo binding、fallback wording 和 error mapping。
- [ ] 在 workflow/companion/quality specs 写入 GitHub CLI-only SSOT、failure taxonomy、semantic boundary 与 validation contract。
- [ ] 增加 current-surface static guard fixture，排除 `.trellis/tasks/archive/**` 等历史证据。

## Phase 2: Shared Runtime

- [ ] 收敛统一 CLI availability/auth/repo-access preflight、repo normalization、JSON parsing 与 required-field validation。
- [ ] 将 Issue/PR/comment/check/review/mergeability/run/status operations 迁移到显式 repo-bound `gh`/`gh api` path。
- [ ] 将 CLI/auth/access/permission/API/incomplete-response 映射为精确 deterministic error facts；移除 adapter fallback 与泛化 `verification_required`。
- [ ] 保持 `git` fetch/push/ls-remote/worktree/revision logic 不变。

## Phase 3: Skill And Platform Consumers

- [ ] 更新所有受影响 `guru-*` contracts 引用 durable SSOT，删除 connector/App/MCP/UI fallback wording，不复制通道政策。
- [ ] 更新 Codex/Claude/Cursor Guru-owned entries 与 preset overlays，保证入口不覆盖 workflow 的 CLI-only 合同。
- [ ] 若 schema/fixtures 需要 additive migration，同步 registry、interface consumer projections、examples 与 evals。

## Phase 4: Tests And Distribution

- [ ] 为 high-level command、`gh api` fallback、explicit repo endpoint、expected SHA、missing CLI/auth/access/permission/API/field failures增加 deterministic fixtures。
- [ ] 覆盖 forbidden channel/fallback wording、implicit repo context、semantic gate ownership 与 `git` transport boundary。
- [ ] 运行 preset apply，同步 dogfood/discovery copies，逐个处理 `.new/.bak`。
- [ ] 更新 README 与 workflow/preset docs。

## Phase 5: Validation

- [ ] focused runtime/package/static tests。
- [ ] 完整 Python runtime 与 Skill package test suites。
- [ ] source/installed Skill validation、ownership、overlay drift、bash syntax、Python compile、JSON/schema、task validate 与 `git diff --check`。
- [ ] clean throwaway marketplace init、preview/switch、preset initial/reapply、official update/upgrade 与 Codex/Claude/Cursor consistency。
- [ ] `guru-check-task` current-scope semantic pass；不创建 `implementation-handoff.md`。

## Validation Commands

```bash
python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis
python3 -m unittest discover -s trellis/skills/guru-team -p 'test*.py'
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-09-181-gh-cli-only-github-operations
git diff --check
```

实际测试模块名以 live repository discovery 为准；不存在的示例命令必须替换为仓库当前真实入口，不得将跳过项报告为通过。
