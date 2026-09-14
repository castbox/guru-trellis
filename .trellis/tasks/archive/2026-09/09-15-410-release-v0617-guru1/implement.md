# #410 实施与验证计划

## 阶段边界

本文件是稳定的 Phase 1 执行计划，不是实现结果、gate 结果、授权记录或发布 checklist。任务在 `planning` 完成前不执行 `task.py start`；规划批准后仍按每个 owner 和每个外部副作用边界重新获取确认。

## 执行顺序

1. 完成 planning wording review、Architecture `task_impact_sync(stage=planning)`、RDT planning gate 和 `guru-approve-task-plan`；通过后才激活 task。
2. 在 task worktree 中按 Docs SSOT Plan 形成最小 pre-promotion contribution 和必要 canonical delivery change；同步受影响的 dogfood/平台 projection，但不修改无关内容。
3. 执行 fresh Phase 2 `guru-check-task`，由 `guru-create-task-commit` 独占首次 commit preview、当前确认和 commit mutation。
4. 对首次提交执行一次覆盖完整 `origin/main...HEAD` 的独立 Branch Review；无开放 P0-P3 finding 后才进入 Architecture 与 RDT 的串行 promotion。
5. promotion 后重新读取 authority 和 task diff，重复 Phase 2、task commit 和完整 Branch Review；不得复用首次 review 或首次 commit 证据。
6. 进入 Publication，生成中文 preparation PR title/body，使用 `Refs #410`；由 Finalizer 和 Merge owner 分别完成 push、PR、archive/Ready 和 merge，且每一项 mutation 独立确认。
7. 合并后 fresh-fetch `origin/main`，冻结 exact candidate commit/tree；重新执行前序 tag lineage、版本映射、source/installed validator、四平台 parity、ownership/preset/drift、focused install/update/reapply、secret scan 和 residue gate。
8. 由 AI 基于 live Issue、exact candidate diff 和当前验证独立审查 Release title/body；随后依次展示并确认 annotated tag、tag-pinned smoke、GitHub Release、Issue closure 和 cleanup。

## 目标交付面

实施前逐个从当前仓库事实确认是否需要变更：`trellis/guru-team-extension.json`、根/workflow/preset README、canonical workflow/preset/source lock、受影响的 Skill package/projection、Architecture/RDT contribution 与验证 fixture。不得为了发布创建 release notes、动态 checklist、发布状态文件或公共 API。

## 验证矩阵

| ID | 验证 | 通过条件 |
| --- | --- | --- |
| T410-01 | planning/Architecture/RDT/Publication identity | 当前 authority、task scope、promotion result 和 reviewed content identity 新鲜且可追溯 |
| T410-02 | candidate lineage | `HEAD`、前序 tag commit、ancestor check、full diff 和 name-status 均绑定 exact candidate |
| T410-03 | four-axis mapping | manifest、README、workflow/preset docs 和 Release text 对 tag、extension、CLI/core、source lock 的表达一致 |
| T410-04 | source/installed/package parity | source 与 installed validator 通过；Shared/Codex/Claude/Cursor 的目标 Skill 文件字节一致 |
| T410-05 | ownership/preset/reapply | ownership check、preset apply、dogfood drift 通过，未产生未解释 `.new/.bak` 或用户内容覆盖 |
| T410-06 | focused installation | 由已验证 Fork source 运行 focused clean install，并覆盖现有项目 update/reapply；不宣称累计 Release Gate matrix |
| T410-07 | release hygiene | changed-file secret scan、`git diff --check`、status 和 residue 检查无阻塞结果；缺 scanner 或结果不完整即 `SKIP`/阻塞 |
| T410-08 | live mutation proof | tag、smoke、GitHub Release、Issue state、PR/base/head 和 cleanup 结果逐项从 live GitHub/Git 事实核验 |

## 主要命令族

命令参数在执行前从当前 owner contract 和 `--help` fresh-read，不凭旧命令猜测。候选 gate 至少覆盖：

```bash
git rev-parse HEAD
git rev-parse "${predecessor_tag}^{commit}"
git merge-base --is-ancestor "${predecessor_tag}^{commit}" "${candidate_commit}^{commit}"
git diff --find-renames --find-copies "${predecessor_tag}^{commit}" "${candidate_commit}^{commit}" --
./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
./.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
./trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
./trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
git diff --check
git status --short
```

实际 focused install、secret scanner、tag/smoke/Release 命令以候选 checkout 中的当前合同为准，并把完整结果绑定到 candidate SHA；未执行或不可用结果必须显式报告。

## 风险与停止条件

- Issue、base、branch、worktree、authority、candidate 或版本轴发生变化：停止并 fresh-read 对应 owner。
- promotion、task commit、Branch Review、Publication 或 Finalizer 结果过期：回到其唯一 consumer，不用 metadata commit 修复。
- install/update/reapply 产生未知 sidecar、用户内容变化或平台漂移：保留差异，停止，不覆盖。
- secret scan 缺失/不完整、命令 `SKIP`、外部 GitHub 不可用或 smoke 未完成：不得继续 tag/Release。
- 任何真实 mutation 失败：只报告该边界失败，重试前重新读取 live authority；不把失败当作已授权重试。
