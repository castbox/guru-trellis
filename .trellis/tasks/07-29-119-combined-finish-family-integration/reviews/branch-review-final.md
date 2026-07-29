status: findings

### 审查范围

- Reviewer ID：`/root/branch_review_final`
- Reviewed HEAD：`b6e4d3ba5cb85ab7c10fea03fdb97a74dcffd699`
- Range：`origin/main...b6e4d3ba5cb85ab7c10fea03fdb97a74dcffd699`
- 独立覆盖 live #119 authority、61-path committed diff、批准规划、Phase 2 evidence、Issue Scope Ledger、Docs SSOT、thin workflow、13 Finish exits、Guru entries、public-only combined integration、#105 matrix、安装/update/reapply/四平台及 frozen legacy boundary。

### 资格判定

- `BR-FINAL-C1`：`normal_required_behavior`，`qualified_finding`。#119 FR-7、批准的 `ssot_first` 与 Branch Review 合同均要求 current durable Docs SSOT；不是非常规扩张。
- Exact remote branch-ref marketplace verification：`rejected_candidate`，属于 reviewed content push 后的 publication gate。
- 恶意伪造、竞态/锁/TOCTOU、额外 fault injection、跨 OS crash consistency 与 #132 cleanup：`out_of_scope`。
- 未重新审核 #116/#117/#118 Skill 内部行为，未发现 PR #160 task artifact 移植。

### 最终发现

Qualified findings: 1

- **P2 `BR-FINAL-F1`：ownership 数量合同仍有四处 stale Docs SSOT。** Committed inventory 实际为 43 legacy paths，其中 18 条带 `current_payload_sha256`、25 条使用 baseline；正确的新 installer SSOT 也写为 25/18。但 [README.md:96](/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/119-combined-finish-family-integration/README.md:96) 仍写 38/5，[overlay-guidelines.md:261](/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/119-combined-finish-family-integration/.trellis/spec/preset/overlay-guidelines.md:261)、[quality-guidelines.md:431](/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/119-combined-finish-family-integration/.trellis/spec/workflow/quality-guidelines.md:431) 和 [upstream-ownership.md:267](/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/119-combined-finish-family-integration/.trellis/spec/preset/upstream-ownership.md:267) 仍写 `exact thirteen`。这些文件属于本 task 的 durable/check scope；即使旧句源自 base，当前 #119 明确承诺 Docs SSOT current，因此会误导维护者理解 frozen/current binding 边界并阻止最终放行。

本轮只读，未修复或修改文件。

### 命令与结果

- Workspace boundary：`status=ok`；expected/actual worktree 一致，source checkout clean，无 suspicious artifact。
- HEAD/base/path count：`b6e4d3ba…` / `b034f466…` / 61。
- Mutable evidence 仅为 `agent-assignment.json`、`task-commit-plans/001.json` 和 task-local `reviews/`。
- `git diff --check origin/main...HEAD`：通过。
- Canonical/dogfood workflow、三个 canonical/dogfood Guru entries、三平台 entry bytes：全部一致。
- Finish markers：publication `3`、verification `4`、finalizer `6`，各一处 mandatory invocation。
- 三个 Finish package 内部路径无 committed diff；43 个 frozen legacy overlay 路径变更数为 `0`。
- Phase 2 的 59 个 reviewed-path digests 与 HEAD mismatch 数为 `0`；三份批准规划 digest 均 current。
- JSON parse、Python compile、throwaway shell syntax：通过。
- 已核对 current evidence：`184/184`、`640 passed / 13 skipped`、`48/48`、`12/12`，以及 initial/post-update 四 adapter `4/4`；本轮未重复执行耗时全量测试。

### Docs SSOT 结论

`ssot_first` 尚未完成最终一致性收敛。Guru entry、workflow、installer、requirements 和主要 README 路由语义已同步，但 ownership current-binding 数量仍存在上述四处冲突，因此 Docs SSOT Gate 不通过。

### 剩余门禁

当前必须返回 `implementation_required`：修正四处 durable wording，重新完成 `guru-check-task`、fresh task commit 和完整 Branch Review。之后仍需独立授权 push，并在 pushed reviewed HEAD 上完成 exact remote marketplace verification、publication review、PR、merge 与 #119/#115 closure；#132 仅保留 follow-up。
