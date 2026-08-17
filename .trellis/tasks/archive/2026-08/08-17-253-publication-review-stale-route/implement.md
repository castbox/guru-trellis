# #253 实施计划

## 实施顺序

1. 在 canonical Finalizer contract 与 companion-script SSOT 中补充 planless stale owner-fact 规则。
2. 在 canonical `owner.py` 将 `publication_review_stale.branch_review_commit` 绑定到 Publication owner context。
3. 加强 stale-specific exact validation，同时保持其他 route 的 plan-bound 分支不变。
4. 增加原生 planless stale fixture 和 production recorder/checker/public invocation 正例。
5. 增加错误 task、commit、reason、current Publication 与 adjacent plan-backed route 负例。
6. 运行 canonical package tests 和静态校验。
7. 运行 preset apply，同步 dogfood、installed 与平台 managed copies。
8. 运行 projection equality、overlay drift、零 `.new/.bak` 和 focused clean installed-package smoke。
9. 执行 `guru-check-task` 完整 Phase 2 semantic check；发现问题后修复并完整重跑。

## 文件计划

### 必改 canonical

- `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py`
- `trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py`
- `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`
- `trellis/presets/guru-team/spec/workflow/companion-scripts.md`

### 由 installer 同步

- `.trellis/guru-team/skills/packages/guru-finalize-task/**`
- `.agents/skills/guru-finalize-task/**`
- `.codex/skills/guru-finalize-task/**`
- `.claude/skills/guru-finalize-task/**`
- `.cursor/skills/guru-finalize-task/**`
- `.trellis/spec/workflow/companion-scripts.md`

### Task-local

- `.trellis/tasks/08-17-253-publication-review-stale-route/{task.json,issue-scope-ledger.json,prd.md,design.md,implement.md}`

## 验证计划

### Targeted correctness

- Finalizer canonical contract tests。
- 真实 production preview/record/check/invoke stale chain。
- 四类 stale negative cases 与一个 adjacent plan-backed protection case。
- Python compile、JSON/schema/source package validation、`git diff --check`。

### Projection and drift

- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
- canonical/dogfood/Codex/Claude/Cursor package equality。
- 扫描 `.new` / `.bak`，期望为零。

### Focused installed-package smoke

- 使用 clean temporary repo 和 current canonical preset projection。
- 只安装/投影本次 managed package 所需资产并运行 stale re-entry production wrappers。
- 证明 installed Finalizer 无历史 patch 即可接受 owner-bound planless stale output。

### 明确跳过

- `verify-throwaway-install.sh`。
- 完整 clean initial install。
- existing-repo workflow preview/switch。
- official Trellis update 与 preset reapply matrix。
- Shared/Codex/Claude/Cursor 全语义矩阵。
- 双 PATH managed interpreter、linked worktree closeout 与 tag-pinned smoke。

上述完整门禁属于 Issue #254；本任务最终报告必须将其标记为未执行，不能据 focused evidence 宣称 release ready。

## 执行分工

- 主会话：维护规划、合同边界、Phase 路由、结果整合与后续 commit/finish 决策。
- Implementation worker：只负责本计划列出的 canonical/runtime/test/contract 与 installer projection 改动，不触碰 #251/#254 范围。
- Check worker：独立执行当前完整 diff 的 Phase 2 semantic check 和 targeted/focused validation，不复用 implementation worker 的结论。

## 风险与控制

- 风险：把所有 commit 校验改成 owner context，削弱 plan-backed routes。
  - 控制：只对 `publication_review_stale` 选择 owner commit，并保留相邻负例。
- 风险：测试只调用内部函数，未覆盖 production wrapper。
  - 控制：正例必须穿过 recorder、checker 与 public invocation。
- 风险：只改 canonical，installed/platform copies 继续旧行为。
  - 控制：apply 后逐面 equality 和 focused installed smoke。
- 风险：focused smoke 被误报为完整安装/发布证明。
  - 控制：固定跳过清单，并把累计 Release Gate 明确留给 #254。

## 完成条件

- Issue #253 Acceptance 全部有代码或验证证据。
- Phase 2 semantic check 无未关闭 finding。
- focused installed projection 通过，完整 throwaway/release gates 明确未执行。
- 工作区只包含本任务授权范围内的文件，不 push、不创建 PR、不合并、不发布。
