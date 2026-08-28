# #312 允许已合并的 active task 在原 worktree 中继续

## 1. Goal

修复 Guru Team workspace boundary 对同一 active task 已合并规划文件的误判：当 source checkout
中的同 task 文件由当前 base 跟踪且逐路径 clean 时，原 task worktree 继续后续阶段；真实
source-side 越界状态继续 fail closed。

Live authority：<https://github.com/castbox/guru-trellis/issues/312>。

## 2. Confirmed Facts

- 本 task 基于 `main@d907fcc5e17f23b6499648e5e9a208457f2d6f8b` 创建，branch 为
  `codex/312-workspace-boundary-merged-active-task`。
- `chengtuo-resume#252` 的规划文件已通过 PR #253 合并到其 `main`，task 仍按合同保持
  `in_progress`，原 worktree 继续同一 Issue 的 Phase 2。
- 2026-08-27 live 复现中，source checkout status 为空，但
  `task.json`、`prd.md`、`design.md`、`implement.md`、`implement.jsonl`、`check.jsonl` 与
  `issue-scope-ledger.json` 仅因存在便全部被归类为 `same_task_artifact`，checker 返回
  `blocked`。
- 根因位于两个 package-local owner 的同构实现：
  `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py:2326-2378` 与
  `trellis/skills/guru-team/packages/guru-review-task-publication/runtime/owner.py:2055-2107`。
  文件存在性扫描先无条件加入 blocker，后续才独立扫描 dirty path。
- `--allow-source-clean` 仅在无 blocker 时探测 clean source checkout 的 cwd mismatch；它
  不应成为 artifact blocker 的绕过开关。
- #60 建立 source-side task artifact fail-closed 边界；#195 迁移 package-local owner，但未改变
  分类语义。本任务保留两者的身份与所有权边界。
- `guru-finalize-task` 与 `guru-review-task-publication` 是当前重复 owner；canonical 与 dogfood
  installed copy 当前字节一致。
- Repository RDT authority 与 Architecture Baseline 均为
  `current-main-0.6.5-guru.40`。本任务与现有隔离目标一致，不新增公共能力或架构决策。

## 3. Requirements

### R1. 只豁免 current-base-tracked 且逐路径 clean 的普通 task 文件

- 对 `WORKSPACE_BOUNDARY_SUSPICIOUS_TASK_ARTIFACTS` 中非 review metadata 的文件，只有同时满足
  “source checkout 当前 `HEAD`/index 跟踪该路径”与“该路径相对 source checkout clean”时，才不
  进入 `suspicious_source_artifacts` blocker。
- 判定必须按路径执行；source checkout 或 task worktree 的无关 dirty 状态不得改变该文件的分类。
- 不以文件名、目录存在、全局 clean、自报字段或 `--allow-source-clean` 代替 Git 跟踪/clean 事实。

### R2. 真实 source-side 越界继续阻断

- untracked 同 task 文件继续进入 blocker。
- staged、unstaged、deleted、renamed 或其它 dirty 同 task 路径继续进入 blocker。
- `planning-approval.json`、`phase2-check.json`、`agent-assignment.json`、`review.md`、
  `review-gate.json`、`pr-readiness.json` 这些 review/check gate metadata 无论是否被 base 跟踪、是否
  clean，均继续阻断。
- `reviews/**` 目录继续阻断。
- 错误 cwd、缺失/错误 ignored runtime mapping、错误 worktree identity、缺失 `task.json`、
  task/branch/workspace 不一致和 task artifact locator 越界继续按现有合同阻断。

### R3. Owner 与公共合同保持不变

- 两个 package-local owner 使用一致的分类规则和测试矩阵，不形成一个放宽、另一个仍阻断的漂移。
- `blocking_suspicious_source_artifacts()`、workspace boundary public output、legacy CLI 参数、
  exit code、错误类别与 `--allow-source-clean` 职责不变。
- 不删除 source checkout 文件、不重写 ignored runtime mapping、不创建替代 task，也不跳过 checker。

### R4. Canonical、installed 与投影一致

- canonical package 是语义源；dogfood installed package 由 preset apply 同步，不手工反向维护。
- `.trellis/spec`、canonical preset spec、workflow/preset operator docs、extension manifests 与声明的
  Shared/Codex/Claude/Cursor projection 保持 installer 管理的一致性。
- 实施前若 `main` 或并行 #311 改变相同 owner/manifest/version bytes，先进入 base reconciliation，
  不覆盖并行工作。

### R5. 下游解除阻断必须使用真实安装结果证明

- Guru Trellis 修复经 current-HEAD review、PR merge 与所需的可安装候选发布后，更新
  `chengtuo-resume#252` 当前 worktree 所消费的 Guru Team preset。
- 在不删除 task、不创建替代 task、不清理 root-only evidence 的前提下，重新运行原
  `check-workspace-boundary.sh`；clean tracked merged task 文件不再阻断。
- Chengtuo #252 在该 checker 通过前不得进入 Phase 2 实现；#252 与 #312 在各自验收完成前保持
  OPEN，对应 worktree/branch 均保留。

## 4. Acceptance Criteria

- [ ] A1 / R1：真实 Git fixture 中，source checkout 当前 `HEAD` 跟踪且逐路径 clean 的
  `task.json/prd.md/design.md/implement.md/implement.jsonl/check.jsonl/issue-scope-ledger.json` 不进入
  `suspicious_source_artifacts`，workspace boundary 返回 `ok`。
- [ ] A2 / R2：同名文件分别处于 untracked、staged、unstaged、deleted/renamed 状态时继续
  `blocked`，错误包含可定位路径。
- [ ] A3 / R2：所有 review metadata 与 `reviews/**` 即使 tracked-clean 也继续 `blocked`。
- [ ] A4 / R2：wrong cwd、runtime/worktree/task identity、task locator 与 branch mismatch 的既有
  regression 不退化；`--allow-source-clean` 不能绕过 artifact blocker。
- [ ] A5 / R1-R3：source checkout 和 task worktree 的无关 dirty 状态不被误归类为当前 task
  artifact；两个 owner 对同一 fixture 输出一致分类。
- [ ] A6 / R4：canonical、dogfood installed、preset spec/docs、extension manifest 与平台投影的
  bytes/modes/managed inventory 检查通过，reapply/update 无 drift 或 sidecar。
- [ ] A7 / R5：安装修复候选后，`chengtuo-resume#252` 原 worktree 的 live checker 通过，且 source
  checkout 仍 clean、task/worktree/runtime identity 不变。
- [ ] A8：focused package tests、preset installer tests、throwaway install/update、task validation、
  Python compile 与 `git diff --check` 通过。
- [ ] A9：fresh committed `origin/main...HEAD` Branch Review 无 P0-P3 open finding；PR 只关闭 #312，
  不关闭或清理 Chengtuo #252。

## 5. Docs SSOT Plan

Strategy：`ssot_first`。

- RDT impact：`rdt_aligned`。绑定 current RDT `current-main-0.6.5-guru.40` 的 workspace isolation、
  fail-closed 和并行 task 隔离目标；本任务不改变产品 requirement，不创建 RDT contribution。
- Architecture impact：no-impact。owner、package boundary、runtime mapping、public DTO/exit 与
  publication/finalization route 均不变；不创建 Architecture contribution 或 ADR candidate。
- Phase 2 先更新 `.trellis/spec/workflow/companion-scripts.md` 与
  `.trellis/spec/workflow/quality-guidelines.md`，明确 tracked-clean 普通 task artifact 例外及必须保留
  的 blocker 矩阵，再修改 runtime/tests。
- preset apply 同步 canonical spec 到 `trellis/presets/guru-team/spec/workflow/**` 与 dogfood
  `.trellis/spec/**`，并同步 installed package、manifest 和声明平台投影。
- operator-visible wording 仅在当前 README 对“可疑同名 task artifact”描述不足时做最小同步；不
  扩大公共接口或另建第二份 SSOT。
- 若实现或 review 发现需要改变 public output、owner、typed exit、runtime mapping 或 RDT/Architecture
  事实，停止并回到 Phase 1 修订本计划。

## 6. Out Of Scope

- 不关闭、归档、重建或清理 Guru #312、Chengtuo #252 及其 task/worktree/branch/evidence。
- 不修改 Chengtuo 的简历解析、生产数据、错误文件或部署；这些工作在 #312 修复交付并安装后回到
  #252 原 worktree 继续。
- 不放宽任意 source checkout dirty 状态，禁止 source-side review/check metadata。
- 不重构 workspace mapping、Finalizer transaction、Publication readiness 或公共 Skill graph。
- 不增加 hostile actor、TOCTOU、锁、并发、crash consistency 或跨 OS 加固。
- 不执行与本修复无关的 release-wide compatibility matrix；若必须发布新 Guru 候选，仅执行交付该
  修复所需且另行授权的 release/install 范围。

## 7. Open Questions

无。Live Issue、current runtime、#60/#195 history、Chengtuo #252 复现和 current RDT/Architecture
authority 已确定产品、兼容、风险与验收边界。
