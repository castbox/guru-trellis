# #119 Branch Review

## 审查范围

- Base：`origin/main`
- Reviewed HEAD：`b6e4d3ba5cb85ab7c10fea03fdb97a74dcffd699`
- Range：`origin/main...b6e4d3ba5cb85ab7c10fea03fdb97a74dcffd699`
- 覆盖：Issue #119 acceptance、61-path committed diff、批准 planning、Phase 2、Docs SSOT、Issue Scope Ledger、部署与安全边界。

## 原始报告

- [Round 1 问题发现审查](reviews/branch-review-initial.md)：`/root/branch_review_initial`，0 findings。
- [Round 2 fresh 最终放行审查](reviews/branch-review-final.md)：`/root/branch_review_final`，1 finding。

## 资格判定

- `BR-FINAL-F1` 属于 `normal_required_behavior`。Issue #119 FR-7 与批准的 `ssot_first` 明确要求 durable Docs SSOT current；四处 ownership 数量描述与 committed inventory 冲突，不是范围扩张。
- Exact pushed-ref marketplace verification 属于后续 publication gate，不是当前 finding。
- 恶意 actor、竞态/锁/TOCTOU、额外 fault injection、跨 OS crash consistency 与 #132 cleanup 均不在当前范围。

## 审查发现

- `P2 BR-FINAL-F1`（open）：`README.md` 仍写 38 baseline / 5 current；`.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/workflow/quality-guidelines.md`、`.trellis/spec/preset/upstream-ownership.md` 仍写 `exact thirteen`。Committed inventory 与 installer SSOT 已是 25 baseline / 18 current，四处 durable wording 必须同步。

## 结论

`implementation_required`。修复上述四处 wording 后，必须重新执行完整 `guru-check-task`、fresh task commit 与完整 Branch Review；不得继续 publication。
