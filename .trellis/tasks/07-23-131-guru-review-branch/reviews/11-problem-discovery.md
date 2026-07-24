# Issue #131 Branch Review Round 11 问题发现原始报告

## 检查完成

### 审查身份与固定范围

- 逻辑角色：`问题发现审查代理`，round 11。
- Technical agent：`/root/issue_131_branch_review_final3`。
- 重入原因：主会话在 Round 10 fresh-final 之后首次执行真实 final recorder 时，
  暴露一个关于 post-commit Phase 2 planning projection 的候选问题。本轮只资格化
  该候选，不重新审查其它已关闭范围。
- Task：`.trellis/tasks/07-23-131-guru-review-branch`。
- Base：`origin/main`。
- Reviewed HEAD：
  `c18efe0f73f03d216a7f4e873907569922e800be`。
- 完整range保持：
  `origin/main...c18efe0f73f03d216a7f4e873907569922e800be`。
- 角色限制：本 agent 本轮是problem-discovery owner，后续不得担任该候选的
  closure reviewer或fresh final reviewer。

本轮没有修改代码、tests、planning、Phase 2、`review.md`、
`review-gate.json`、assignment或task commit plan；没有调用recorder，没有
commit、push、PR或其它发布副作用。

## 首次失败证据

主会话首次调用：

```text
.codex/skills/guru-review-branch/scripts/review-branch.sh ...
  --typed-exit passed
```

在 `cmd_review_branch` 的post-commit Phase 2 entry validation中失败，暴露错误：

```text
phase2_check_current_facts_invalid:
guru-check-task requires current approved guru-planning-approval-2.0 evidence.
```

同一时段，外层：

```text
check-planning-approval --require-exit approved --allow-committed-head
```

对同一 `planning-approval.json` 和 committed HEAD 返回 `status=ok`。该单次差异使
主会话最初提出假设：`validate_phase2_check(...allow_committed_head=True)` 内部的
`phase2_planning_projection` 没有向 `validate_planning_approval` 透传
`allow_committed_head`，从而形成post-commit nested mode不一致。

## 独立复现与代码路径

随后在同一worktree、task、HEAD和artifact bytes上直接执行：

| 调用 | 结果 |
| --- | --- |
| `validate_planning_approval(...allow_committed_head=False, required_exit="approved")` | `errors=[]` |
| `validate_planning_approval(...allow_committed_head=True, required_exit="approved")` | `errors=[]` |
| `phase2_planning_projection(root, task_dir)` | 成功 |
| `validate_phase2_check(...allow_committed_head=True)` | `errors=[]`、`typed_exit=passed` |

真实代码路径为：

1. `validate_phase2_check` 在current task分支调用
   `phase2_planning_projection(root, task_dir)`；
2. `phase2_planning_projection` 调用
   `validate_planning_approval(...required_exit="approved")`；
3. `validate_planning_approval` 虽声明 `allow_committed_head` 参数，但当前函数体
   没有基于该参数执行任何分支；
4. 因此当前实现中 `False`、`True` 与省略该参数在planning validation语义上等价。

这直接推翻了“nested mode未透传导致确定性post-commit失败”的初始根因假设。
同一candidate在随后直接validator/projection/Phase 2 retry中不能复现。

Planning validation会重新读取current authorities，其中包括live GitHub
authority；首次失败可能来自一次瞬时外部读取失败或其它未保留的临时条件，但现有
证据不能确定该根因。即使是瞬时外部依赖不可用，当前行为也是fail closed，不足以
证明runtime错误接受stale evidence、错误拒绝稳定有效evidence或违反Issue #131
normal-path contract。

## 候选资格化

### `C-131-R11-01`

- Affected behavior：正常Phase 2 -> commit -> Branch Review recorder链路中的
  planning/Phase 2 freshness validation。
- Requirement refs：
  - Issue #131 Entry Preconditions；
  - PRD R3 / R6 / AC3 / AC17；
  - `guru-review-branch` contract的planning approval、Phase 2 check与invocation
    freshness要求。
- Scenario class：`normal_required_behavior`。
- Normal-path reproducibility：
  - 有一次真实recorder失败；
  - 但随后同一HEAD、同一artifacts的两种planning validation、planning
    projection和allow-committed Phase 2 validation全部成功；
  - 初始代码根因假设被函数体真实行为否定；
  - 当前没有稳定命令、fixture或状态序列可以重现合同违反。
- Disposition：`rejected_candidate`。
- Qualification reason：candidate属于current scope，但现有证据没有证明当前实现
  在受支持normal path中存在可重复的correctness/compatibility violation。单次
  fail-closed结果和一个已被代码/重试证据推翻的根因假设，不能进入P0-P3 finding。
- Severity：无。
- Finding ref：无。

### 非阻塞观察

- 首次失败没有保留下层 `validate_planning_approval` 的完整 `error_codes`，因此无法
  事后确认是live authority瞬时失败还是其它临时条件。
- 该可观测性事实不构成Issue #131 current finding：当前没有需求要求把每次内部
  planning error展开为新的public DTO字段，也没有证据证明现有fail-closed route
  不正确。
- 如果未来在稳定外部状态下再次出现相同错误，应保留完整nested error codes、调用
  时间与authority读取结果，再按新的可重复证据重新资格化；本轮不创建required
  follow-up或scope proposal。

## Findings与route

- P0：0。
- P1：0。
- P2：0。
- P3：0。
- Scope proposals：0。
- 新qualified findings：0。
- Rejected candidates：1。

本轮不能作为最终 `guru-review-branch:passed` 证据：Round 11是问题发现角色，
使Round 10不再是assignment lifecycle中的最后一轮。本轮建议：

- internal disposition：`rejected_candidate`；
- next review intent：`fresh_final_review`；
- next reviewer：一个未参与Round 11 discovery、implementation、Phase 2或closure
  的全新technical agent；
- public typed exit：本轮不提前确定，必须由下一轮fresh final reviewer确认当前
  full range仍为零finding后再由owning Skill决定。

## 结论

首次recorder失败是真实观察，但当前无法稳定复现；随后所有direct validators、
planning projection和allow-committed Phase 2 validation均成功。由于
`allow_committed_head` 在当前planning validator函数体中没有形成模式分支，
“nested mode未透传”不是成立的根因。

按qualification-before-severity与honest-but-fallible normal-operation边界，
`C-131-R11-01`应记录为current-scope `rejected_candidate`，不得分配P0-P3，
不得路由implementation，也不需要scope confirmation。下一步仅需派发全新agent
执行fresh final review；本 agent不得继续担任closure或final reviewer。
