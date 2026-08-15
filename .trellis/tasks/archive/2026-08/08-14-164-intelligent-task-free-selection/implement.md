# #164 实施计划

## Phase A：Canonical contract

- [x] 更新 `trellis/workflows/guru-team/workflow.md` 的 no-task selector 与
      `guru-task-free-current-checkout` target behavior。
- [x] 更新 canonical `guru-select-workflow-mode` Skill/contract，写明 explicit、automatic、
      one-question、standard Intake 和 same-scope reuse 规则。
- [x] 保持 public schema/interface/exit 集合最小；仅在现行 schema 无法校验最终选择时修改结构。
- [x] 新增 semantic closed-loop Skill `guru-execute-task-free-change`，独占 checkout suitability、
      bounded edit、交互与 scope/risk re-entry，不新增 runtime risk classifier。
- [x] 将 selector `task_free` 最小输出通过 target-owned authoring seed 投影到新 Skill；
      workflow 只保留 mandatory invocation、typed exits 与唯一 consumers。
- [x] 为新 Skill 增加 package-local recorder/checker/invoker；脚本只校验 AI 已完成的结果。

## Phase B：Evals and tests

- [x] 重构现有 implicit/ordinary eval，使其匹配三分语义判断。
- [x] 增加 high-confidence、insufficient-evidence、complex request 三类无明确意图用例。
- [x] 增加 simple / insufficient / complex Issue 用例。
- [x] 将活动 task、scope expansion、unrelated worktree、dirty overlap、position evidence、
      risk evolution 用例迁移到新 Skill，并真实执行其 public wrapper。
- [x] 增加 completed、location self-reentry、explicit choice self-reentry 与 blocked 用例。
- [x] 为自动/显式 post-write expansion 增加真实 tracked partial edit、风险扩大、停止后续写入
      与剩余目标未改证据。
- [x] 将 completed workflow DTO 收敛为 edited paths、validation summary 与
      unverified boundaries，并保持 review narrative/transcript private。
- [x] 更新 package contract tests、preset tests 与 installed transcript assertions。

## Phase C：Docs and entry points

- [x] 更新 `README.md`、workflow README、preset README。
- [x] 所有用户入口公开 `这次走 task-free`，并说明 task-free 不授权生命周期或发布动作。
- [x] 同步 canonical workflow 与 dogfood workflow。
- [x] 同步 selector 与新 Skill 的 Shared/Codex/Claude/Cursor projections，验证 byte identity。

## Phase D：Install/update compatibility

- [x] 运行 preset apply 同步 dogfood；逐个处理 `.new` / `.bak`。
- [x] 运行 dogfood overlay drift 与 source/installed validation。
- [x] 运行 fresh throwaway public marketplace discovery、本地未发布 workflow sample 与 preset install；
      当前 branch ref 发布后仍需用该远端 ref 重验 marketplace workflow 安装。
- [x] 在 throwaway 中运行 `trellis update`，重新应用 preset，再验证 workflow、Skill、平台入口、
      eval 和 sidecar 状态。

## Validation Commands

```bash
python3 trellis/skills/guru-team/packages/guru-select-workflow-mode/tests/test_contract.py
python3 trellis/skills/guru-team/packages/guru-execute-task-free-change/tests/test_contract.py
python3 trellis/skills/guru-team/packages/guru-execute-task-free-change/tests/test_runtime.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
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

- [x] `prd.md`、`design.md`、`implement.md` 完整且无重复 SSOT。
- [x] Planning wording review 无 unchecked normative hit。
- [x] `guru-approve-task-plan` 返回 `approved`。
- [x] 用户确认批准规划并激活任务后才运行 task activation；activation 仅写入任务状态，不授权开始实现。
