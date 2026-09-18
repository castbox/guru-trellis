# #435 技术设计：Active Task Delivery Loop

状态：Phase 1 candidate。Architecture contribution 与 proposed ADR 已建立；shared Architecture/RDT current 尚未 promotion，新 package 尚未接入 production workflow。

## 1. 设计结论

采用 `architecture_impact / target_native`。当前 Publication、Finalizer、Merge 把 Delivery、archive、Ready、Issue closure expectation 与 task terminal lifecycle 绑定在同一尾链。本任务直接建立三个职责内聚 owner，保留旧链运行直到 #434 原子切图，不增加 adapter 或双读。

命中的设计宪法原则：`concept-semantic-completeness`、`cohesion-change-isolation`、`minimum-necessary-complexity`、`debt-one-way-convergence`。

## 2. Owner topology

### D435-01 Review owner

`guru-review-task-delivery` 是 Delivery semantic readiness 的唯一 owner。闭合 exits 与 consumer 固定为：

| Exit | 最小 DTO | 唯一 consumer |
| --- | --- | --- |
| `ready` | `task_ref`, `delivery_cycle_ref`, `reviewed_head`, `pr_title`, `pr_body`, `remaining_work_state` | `guru-publish-task-delivery` |
| `planning_revision_required` | `task_ref`, `reason_refs` | Phase 1 Planning owner |
| `implementation_required` | `task_ref`, `finding_refs`, `resume_target=phase-2` | `guru-resume-implementation` |
| `scope_confirmation_required` | `task_ref`, `proposal_refs` | existing clarification route |
| `blocked` | `reason_code`, `remediation` | stop |

`delivery_cycle_ref` 是当前 cycle 的 call-local identity，不是历史 ledger。Review private gate在成功 projection 后退休；丢失 semantic output 时 fresh 重跑 Review。

### D435-02 Publish owner

`guru-publish-task-delivery` 独占 remote branch + current PR transaction。Exits 固定为：

| Exit | 最小 DTO | 唯一 consumer |
| --- | --- | --- |
| `ready_for_merge` | `task_ref`, `delivery_cycle_ref`, `repo_ref`, `pr_number`, `expected_head_sha`, `publication_body_sha256` | `guru-merge-task-delivery` |
| `review_stale` | `task_ref`, `stale_reason` | `guru-review-task-delivery` |
| `resume_publication` | `task_ref`, `transaction_ref` | same Publish owner |
| `reprepare_required` | `task_ref`, `reason_code` | same Publish owner |
| `blocked` | `reason_code`, `remediation` | stop |

Publish 复用现有 Finalizer 已验证的 push/PR/Draft/Ready deterministic primitives 与 #405 recovery semantics，但不复用 Finalizer 的 archive、finish-summary、task completion 或 terminal handoff authority。直接抽取 shared low-level utility 时，调用 owner必须仍为 Publish；禁止用 wrapper保留第二业务路径。

### D435-03 Merge owner

`guru-merge-task-delivery` 独占 remote merge gate、confirmation、mutation 与 terminal recovery。Exits 固定为：

| Exit | 最小 DTO | 唯一 consumer |
| --- | --- | --- |
| `delivered` | `task_ref`, `delivery_cycle_ref`, `repo_ref`, `pr_number`, `reviewed_head`, `merge_commit_sha` | #436 `guru-review-task-completion` |
| `merge_blocked` | `repo_ref`, `pr_number`, `reason_code`, `remediation` | stop |
| `implementation_required` | `task_ref`, `finding_refs`, `resume_target=phase-2` | `guru-resume-implementation` |
| `review_refresh_required` | `task_ref`, `reason_code` | `guru-review-task-delivery` |

不存在 closure-mismatch exit：Delivery PR没有 closing keyword，Merge post-check验证 Issue 仍 Open 或无 Issue mutation，而不是验证 closure。不存在 archive restore exit：task merge 前后均 active。

## 3. Delivery policy model

### D435-04 Planning shape

Planning artifacts必须表达以下四个不同集合：

1. `task_scope`：整个 accepted task scope；
2. `delivery_slice`：当前 cycle 承诺交付的 closed requirement/design/test refs；
3. `remaining_work`：task scope 减去已交付与当前 slice 后的明确 refs；
4. `independent_delivery_conditions`：当前 slice 在不依赖 remaining work 已完成时成立的可观察条件。

Check 与 Branch Review 对 current candidate 做完整影响检查，并对 `delivery_slice` 做满足性判断。它们不能把 `remaining_work` 误判成当前遗漏，也不能把 current-slice finding移到 remaining work。Task Commit只消费 fresh Check pass。

每个新 cycle 在已有 merged Delivery facts基础上重新形成 current `delivery_slice`；Planning owner只在 scope/policy 变化时重入。普通 remaining-work推进不创建替代 task。

## 4. Cross-branch Delivery identity

### D435-05 结构化 merge trailer

Merge owner已经控制 merge-commit `subject` 与 `body`，并使用 merge-commit method。将以下闭合 trailer附加到 fixed merge body：

```text
Guru-Task-Identity: <stable-task-id>
Guru-Delivery-Schema: 1
Guru-Delivery-Head: <40-hex-reviewed-head>
```

其中：

- `stable-task-id` 来源于原 task identity，Reactivate 不改变它；
- `Guru-Delivery-Head` 必须与 Publish/Review 绑定的 exact reviewed head 完全相同；
- PR number、merge commit SHA、parents、repository/base 与 merged time 从 GitHub/Git live facts取得；
- trailer只存在于业务 Delivery merge commit；Finish bookkeeping merge明确禁止这些 trailers。

Discovery 从 target base history筛选受控 merge commits，解析闭合 trailer，随后以 GitHub PR/merge facts交叉验证 repo、base、head、parents 与 merge result。Current branch、remote branch存活、PR body与 task creation branch/base 都不参与 identity authority。

该设计的直接 consumers为 #436 Completion 的历史 Delivery聚合和本任务的 terminal recovery/discovery tests。不存在其它持久化字段。仓库 merge policy若不支持 `--merge --subject --body-file`，Merge返回 `merge_blocked/unsupported_delivery_merge_policy`，不自动改用 squash/rebase。

## 5. Publish recovery

### D435-06 #405 迁移

Publish transaction使用单一 current schema，覆盖：

- initial no-PR push/create/bind/Ready；
- unique strict-ancestor PR adoption；
- current transaction 位于 bind 阶段且 remote/PR/Publication head equal、PR未绑定的恢复；
- metadata byte convergence；
- Draft-to-Ready 与 already-Ready；
- terminal output loss。

在任何剩余 mutation 前持久化精确 PR identity、head relation、原 Draft/Ready、metadata comparison 与 convergence decision。same-plan recovery只能继续原 transaction。旧 Finalizer transaction不被新 Publish双读或转换；#434 切图前由旧 owner完成或手工处置。

## 6. Merge recovery

### D435-07 Delivery terminal fact

Merge private gate绑定 first live PR snapshot、expected head、pre-merge base head、exact subject/body/trailer bytes与confirmation plan identity。Executor执行一次 expected-head merge，并验证：

- PR=`MERGED`；
- merge commit subject/body/trailer exact；
- parent 1为 pre-merge base head，parent 2承载 reviewed head；
- target base ref指向 merge commit；
- PR body无 closing keyword；
- no Issue close mutation由本 owner执行。

stdout loss通过同一 gate与live terminal facts重建同一 `delivered` DTO；不重复 merge。未知 commit shape、body/trailer drift、base/head drift或多个候选均 fail closed。

## 7. Base reconciliation

### D435-08 #407 resolved-tree route

直接演进 `guru-reconcile-task-base`：新增 owner-owned resolved-candidate profile；若现有 profile 可直接承载，则升级其 current-only shape。输入绑定 active MERGE_HEAD、prior task head、selected new base、stage-0 tree object、index-tree digest、parent order、clean staged state与 fresh Phase 2 identity。

确定性 executor在 mutation 前验证零 unresolved/unstaged/untracked、零其它 Git sequencer、exact branch/task/worktree与完整 tree identity；创建 parents `[prior_task_head, new_base_head]` 的唯一 local merge commit并验证结果。Executor result只服务 Reconcile recorder/checker与 stdout-loss recovery，不进入 Delivery public DTO。

该路径复用 existing `review_continuity_required` / full-review规则：真实 task content适配后必须 fresh Phase 2、Task Commit语义路径与完整 Branch Review；不得把 resolved tree降级为 base-only continuity。

## 8. Additive distribution 与 cutover boundary

### D435-09 实现位置

Canonical source：

- `trellis/skills/guru-team/packages/guru-review-task-delivery/`
- `trellis/skills/guru-team/packages/guru-publish-task-delivery/`
- `trellis/skills/guru-team/packages/guru-merge-task-delivery/`
- 现有 Planning/Approval、Check、Task Commit、Branch Review、Reconcile 的最小 current-only合同修改；
- workflow/spec/README、preset manifest/installer/validator、integration tests。

Installed 与 platform projections通过 preset apply生成。新 interfaces声明唯一 consumers，但 `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 不增加 mandatory invoke/active edge；#434 后续一次性完成 production graph activation。

旧 Publication/Finalizer/Merge/Restore package与测试在本任务中保持 current。任何 shared helper抽取必须证明旧链与新 package分别拥有清晰调用边界，不产生第二 semantic owner。

## 9. Docs SSOT Plan

策略：`delta_first`。

- Task authority：本 task 的 `prd.md`、`design.md`、`implement.md`。
- RDT contribution：实现阶段创建 `docs/requirements-design-test-contributions/435-active-task-delivery-loop/`，定义 R435/D435/T435 与 traceability；shared RDT current只在独立 committed review后 serialized promotion。
- Architecture：当前 task-owned contribution为 `docs/architecture/contributions/435-active-task-delivery-loop.md`，decision candidate为 `docs/architecture/adr/012-active-task-delivery-loop.md`。
- Durable workflow SSOT：canonical workflow/spec/README与 package contracts；task artifacts不成为公共 owner authority。
- Projection：canonical先改，preset apply同步 dogfood/installed/Shared/Codex/Claude/Cursor；逐项处理 `.new/.bak`。
- Promotion：Architecture/RDT contribution经 independent committed full-diff review后，以 expected `.54` serialized promotion；promotion-created diff fresh重跑 Phase 2、Task Commit与完整 Branch Review。
- Cutover：#434 独占生产图、旧 edge retirement与最终 graph count；本任务文档不得声称已激活。

## 10. Alternatives 与 rollback

- Delivery ledger：拒绝。新增长期 writer/state且Git/GitHub已有直接 consumer所需事实。
- PR body identity：拒绝。PR body是人类 publication payload，可编辑，且 `Refs` 文案不承担 lifecycle identity。
- current branch discovery：拒绝。Reactivate与branch cleanup会破坏历史发现。
- 覆盖 task creation fields：拒绝。混淆 immutable creation history与current workspace binding。
- old-output adapter或dual graph：拒绝。#434要求atomic cutover，adapter会形成第二 authority。
- squash/rebase fallback：拒绝。无法提供受控 merge-commit trailer与稳定 parents。

Rollback单位为三个 additive packages、前置 owner合同、Reconcile扩展、tests、docs/spec与managed projections。#434未切图，因此 rollback不迁移 production lifecycle state。
