# #164 实施计划

## Phase A：Canonical contract

- [ ] 更新 `trellis/workflows/guru-team/workflow.md` 的 no-task selector 与
      `guru-task-free-current-checkout` target behavior。
- [ ] 更新 canonical `guru-select-workflow-mode` Skill/contract，写明 explicit、automatic、
      one-question、standard Intake 和 same-scope reuse 规则。
- [ ] 保持 public schema/interface/exit 集合最小；仅在现行 schema 无法校验最终选择时修改结构。
- [ ] 明确定义 checkout suitability 与 scope/risk re-selection，不新增 runtime risk classifier。

## Phase B：Evals and tests

- [ ] 重构现有 implicit/ordinary eval，使其匹配三分语义判断。
- [ ] 增加 high-confidence、insufficient-evidence、complex request 三类无明确意图用例。
- [ ] 增加 simple / insufficient / complex Issue 用例。
- [ ] 增加 same file-count different-risk、活动 task、scope expansion、unrelated worktree、
      dirty overlap、no branch-protection lookup 用例。
- [ ] 更新 package contract tests、preset tests 与 installed transcript assertions。

## Phase C：Docs and entry points

- [ ] 更新 `README.md`、workflow README、preset README。
- [ ] 所有用户入口公开 `这次走 task-free`，并说明 task-free 不授权生命周期或发布动作。
- [ ] 同步 canonical workflow 与 dogfood workflow。
- [ ] 同步 Shared/Codex/Claude/Cursor Skill projections，验证 byte identity。

## Phase D：Install/update compatibility

- [ ] 运行 preset apply 同步 dogfood；逐个处理 `.new` / `.bak`。
- [ ] 运行 dogfood overlay drift 与 source/installed validation。
- [ ] 运行 fresh throwaway marketplace + preset install。
- [ ] 在 throwaway 中运行 `trellis update`，重新应用 preset，再验证 workflow、Skill、平台入口、
      eval 和 sidecar 状态。

## Validation Commands

```bash
python3 -m unittest trellis.skills.guru-team.packages.guru-select-workflow-mode.tests.test_contract
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-source-package.sh
trellis/presets/guru-team/scripts/bash/verify-installed-package.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
git diff --check
```

命令名称必须在实现开始前用当前仓库 wrappers 重新核实；不存在的 wrapper 不得以替代命令
冒充通过。完整 throwaway 因环境阻塞时，最终报告必须列出未验证边界和风险。

## Risky Files And Review Points

- `trellis/workflows/guru-team/workflow.md`：global graph 与 target behavior 必须保持闭合。
- selector contract/evals：AI semantic judgment 不得退化为关键词或文件数判断。
- preset installer/managed inventory：canonical、installed、platform projections 必须同源。
- throwaway script：验证必须覆盖 fresh install 与 update/reapply，不得只检查当前 dogfood。

## Pre-Activation Gate

- [ ] `prd.md`、`design.md`、`implement.md` 完整且无重复 SSOT。
- [ ] Planning wording review 无 unchecked normative hit。
- [ ] `guru-approve-task-plan` 返回 `approved`。
- [ ] 用户确认批准规划并激活任务后才运行 task activation；activation 仅写入任务状态，不授权开始实现。
