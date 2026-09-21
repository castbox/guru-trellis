# 11 Public Skill I/O 与迁移闭包

## 1. 要解决的问题

Owner名称清单不能证明production graph闭合。每个public Skill必须声明全部typed exits、每个exit的唯一consumer、
交给consumer的最小DTO，以及旧exit的确定处置。本文件独占该迁移合同；实现阶段不得再发明route、兼容alias、
nullable总DTO或未声明stop。

## 2. 公共DTO族

Public handoff只使用以下封闭DTO族。Repository context由调用图验证；跨repository mutation额外携带`repo_ref`。

| DTO | Exact fields | Direct consumer purpose |
| --- | --- | --- |
| `TaskIdentityDTO` | `task_id`、`task_ref` | 解析current tracked task artifact |
| `TaskLifecycleDTO` | `task_id`、`lifecycle_generation` | 区分Reactivate前后generation |
| `TaskArtifactDTO` | `task_id`、`task_ref`、`lifecycle_generation` | 同时读取artifact并验证generation |
| `ResultRefDTO` | `task_id`、`lifecycle_generation`、`result_id` | 消费一个named producer result |
| `IssueRefDTO` | `repo_ref`、`issue_number` | fresh读取exact Issue |
| `IssueIntakeRefDTO` | `repo_ref`、`issue_number`、`result_id` | fresh intake消费Issue创建或复用结果 |
| `SourceRelationRefDTO` | `task_id`、`lifecycle_generation`、`source_relation_id` | consumer fresh重读current source relation |
| `SourceCorrectionReadyDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`current_source`、`reviewed_source`、`accepted_scope_identity`、`target_relation_id`、`result_id` | Reactivate验证`current_source`并原子写入`reviewed_source` |
| `DeliveryTargetRefDTO` | `task_id`、`lifecycle_generation`、`target_relation_id` | consumer fresh重读current Delivery target |
| `BranchBindingRefDTO` | `task_id`、`lifecycle_generation`、`binding_epoch`、`binding_revision` | consumer fresh重读current branch association |
| `CheckpointRefDTO` | `task_id`、`lifecycle_generation`、`checkpoint_commit`、`checkpoint_ref`、`result_id` | 消费exact portable task-state checkpoint |
| `HandoffRefDTO` | `task_id`、`lifecycle_generation`、`handoff_id`、`receipt_ref`、`result_id` | 恢复同一machine-transfer transaction |
| `HandoffInventoryRefDTO` | `task_id`、`lifecycle_generation`、`handoff_id`、`inventory_id` | source-machine Cleanup重读exact local inventory |
| `ResourceSealRefDTO` | `task_id`、`lifecycle_generation`、`finish_result_id`、`inventory_id` | Cleanup重读sealed inventory |
| `TerminalFinishRefDTO` | `task_id`、`lifecycle_generation`、`finish_result_id`、`cleanup_state` | inventory缺失时证明Finish已terminal并进入manual Cleanup |
| `CleanupResultRefDTO` | `task_id`、`lifecycle_generation`、`cleanup_result_id` | 恢复同一Cleanup result |
| `PlanningApprovalRefDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`result_id` | Activation消费current Planning approval |
| `BaseReconcileResultDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`task_head`、`new_base_head`、`resume_target`、`result_id` | 恢复base reconcile后的exact stage |
| `BaseContinuitySeedDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`task_head`、`old_base_head`、`new_base_head`、`branch_review_commit`、`candidate_tree_sha256`、`relevant_paths`、`resume_target`、`result_id` | Branch Review执行bounded continuity |
| `BaseContinuityResultDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`branch_review_commit`、`resume_target`、`result_id` | base-continuity router恢复exact原stage |
| `Phase2ResultDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`phase2_commit_anchor`、`result_id` | Task Commit消费current Phase 2 pass |
| `TaskCommitResultDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`base_ref`、`branch_review_commit`、`result_id` | Branch Review消费exact committed candidate |
| `BranchReviewResultDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`branch_review_commit`、`result_id` | Publication消费current complete-range review |
| `PublicationReadyDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`branch_review_commit`、`pr_title`、`pr_body`、`result_id` | Finalizer消费reviewed closeout payload |
| `DeliveryReviewReadyDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`delivery_cycle_ref`、`reviewed_head`、`pr_title`、`pr_body`、`remaining_work_state`、`result_id` | Publish Delivery消费reviewed slice payload |
| `MergeReadyDTO` | `task_id`、`lifecycle_generation`、`repo_ref`、`pr_number`、`expected_head_sha`、`expected_base_branch`、`expected_head_branch`、`publication_body_sha256`、`result_id` | Merge PR fresh验证exact closeout PR |
| `DeliveryMergeReadyDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`delivery_cycle_ref`、`repo_ref`、`pr_number`、`expected_head_sha`、`publication_body_sha256`、`result_id` | Merge Delivery fresh验证exact slice PR |
| `TaskMergeResultDTO` | `task_id`、`lifecycle_generation`、`repo_ref`、`pr_number`、`merge_commit_sha`、`merge_lineage`、`result_id` | Completion消费exact closeout或pre-cutover recovered merge |
| `DeliveryMergeResultDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`delivery_cycle_ref`、`repo_ref`、`pr_number`、`reviewed_head`、`merge_commit_sha`、`result_id` | Completion消费exact Delivery merge |
| `FinalizerBaseReconcileSeedDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`task_head`、`publication_head`、`selected_base_ref`、`old_base_head`、`new_base_head`、`branch_review_commit`、`resume_target`、`result_id` | Base Reconcile消费Finalizer发现的exact evolved-base pair |
| `PublicationRefreshSeedDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`branch_review_commit`、`reason_code`、`result_id` | Publication重新审查exact reviewed content |
| `FinalizationReprepareRefDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`branch_review_commit`、`publication_head`、`reason_code`、`transaction_id`、`result_id` | Finalizer same-owner reprepare/recovery |
| `MergedPRRecoveryRefDTO` | `task_id`、`task_ref`、`lifecycle_generation`、`repo_ref`、`pr_number`、`expected_head_sha`、`result_id` | pre-cutover restore后由Merge owner恢复exact merged result |
| `TransactionRefDTO` | `task_id`、`lifecycle_generation`、`transaction_id`、`result_id` | same-owner transaction recovery |
| `ReasonDTO` | `reason_code`、`reason_refs` | named re-entry或stop定位缺失authority |

DTO不携带absolute path、checkout path、resource list、Issue snapshot、authorization、完整review evidence、private
checkpoint locator或generic digest bundle。只有上表operation-specific DTO中具有直接consumer的commit/head字段能
跨相邻Skill传递；它们只绑定该次handoff freshness，不进入tracked task metadata、session、association或通用
evidence authority。Consumer仍必须fresh重读live facts并验证这些identity。

DTO外独立public scalar enum只有以下三组：`session_outcome=session_bound|explicit_task_mode`；`resume_target`使用workflow已声明
的named target id；`merge_lineage=closeout|pre_cutover_recovered`。任何其它跨owner字段必须先进入上表中的named DTO；实现不得在schema中临时增加自由格式
`source_identity`、`target_ref`、`inventory_id`、`cleanup_state`或reviewed Issue payload。

## 3. 新增与替换owner的完整exit closure

表中列出的exit是对应Skill的全部external exits。同一invocation内的多轮选择、confirmation与即时retry不产生
额外public exit；需要跨invocation继续的未收敛transaction必须返回表中声明的same-owner resume exit。

| Producer | Exit | Minimal output | Unique consumer |
| --- | --- | --- | --- |
| `guru-create-issue` | `issue_created` | `IssueIntakeRefDTO` | `guru-sync-base` |
| `guru-create-issue` | `issue_reused` | `IssueIntakeRefDTO` | `guru-sync-base` |
| `guru-create-issue` | `blocked` | `ReasonDTO` | `issue-creation-blocked` stop |
| `guru-create-task` | `created` | `TaskArtifactDTO`、`BranchBindingRefDTO`、`session_outcome` | `guru-task-created` workflow target |
| `guru-create-task` | `session_binding_recovery_required` | `TaskArtifactDTO`、`ReasonDTO` | `guru-bind-task-session` |
| `guru-create-task` | `resume_creation` | `TransactionRefDTO`、`ReasonDTO` | `guru-create-task` same transaction profile |
| `guru-create-task` | `refresh_review` | `IssueRefDTO`、`ReasonDTO` | `guru-sync-base` |
| `guru-create-task` | `invalid_task_state` | `TaskIdentityDTO`、`ReasonDTO` | `invalid-task-state` stop |
| `guru-create-task` | `blocked` | `ReasonDTO` | `task-creation-blocked` stop |
| `guru-establish-task-identity` | `established` | `TaskArtifactDTO` | `guru-task-identity-established-router` |
| `guru-establish-task-identity` | `blocked` | `ReasonDTO` | `task-identity-establishment-blocked` stop |
| `guru-repair-task-lifecycle` | `repaired` | `TaskArtifactDTO` | `guru-task-lifecycle-repaired-router` |
| `guru-repair-task-lifecycle` | `blocked` | `ReasonDTO` | `task-lifecycle-repair-blocked` stop |
| `guru-rename-task` | `renamed` | new `TaskArtifactDTO`、`ResultRefDTO` | `guru-current-phase-router` |
| `guru-rename-task` | `blocked` | `ReasonDTO` | `task-rename-blocked` stop |
| `guru-reconcile-task-source` | `source_current` | `TaskArtifactDTO`、`SourceRelationRefDTO`、`ResultRefDTO` | `guru-task-source-current-router` |
| `guru-reconcile-task-source` | `source_correction_ready` | `SourceCorrectionReadyDTO` | `guru-reactivate-task` |
| `guru-reconcile-task-source` | `blocked` | `ReasonDTO` | `task-source-reconciliation-blocked` stop |
| `guru-retarget-task-delivery` | `target_current` | `TaskArtifactDTO`、`DeliveryTargetRefDTO`、`ResultRefDTO` | `guru-task-target-current-router` |
| `guru-retarget-task-delivery` | `planning_stale` | `TaskArtifactDTO`、`ReasonDTO` | `guru-approve-task-plan` |
| `guru-retarget-task-delivery` | `blocked` | `ReasonDTO` | `task-target-retarget-blocked` stop |
| `guru-activate-task` | `activated` | `TaskArtifactDTO`、`session_outcome` | `guru-resume-implementation` workflow target |
| `guru-activate-task` | `session_binding_recovery_required` | `TaskLifecycleDTO`、`ReasonDTO` | `guru-bind-task-session` |
| `guru-activate-task` | `blocked` | `ReasonDTO` | `task-activation-blocked` stop |
| `guru-establish-task-branch-binding` | `binding_established` | `TaskArtifactDTO`、`BranchBindingRefDTO` | `guru-task-binding-established-router` |
| `guru-establish-task-branch-binding` | `blocked` | `ReasonDTO` | `task-binding-establishment-blocked` stop |
| `guru-rebind-task-branch` | `rebound` | `TaskArtifactDTO`、new `BranchBindingRefDTO`、`ResultRefDTO` | `guru-task-rebound-router` |
| `guru-rebind-task-branch` | `already_bound` | `TaskArtifactDTO`、current `BranchBindingRefDTO`、`ResultRefDTO` | `guru-task-rebound-router` |
| `guru-rebind-task-branch` | `resume_rebind` | `TransactionRefDTO`、`ReasonDTO` | `guru-rebind-task-branch` same transaction profile |
| `guru-rebind-task-branch` | `reconcile_required` | `TaskArtifactDTO`、`ReasonDTO` | `task-branch-target-reconciliation-required` stop |
| `guru-rebind-task-branch` | `blocked` | `ReasonDTO` | `task-branch-rebind-blocked` stop |
| `guru-ensure-task-checkout` | `checkout_ready` | `TaskArtifactDTO`、`BranchBindingRefDTO`、`ResultRefDTO` | `guru-task-checkout-ready-router` |
| `guru-ensure-task-checkout` | `resume_checkout_acquisition` | `TransactionRefDTO`、`ReasonDTO` | `guru-ensure-task-checkout` same transaction profile |
| `guru-ensure-task-checkout` | `blocked` | `ReasonDTO` | `task-checkout-acquisition-blocked` stop |
| `guru-checkpoint-task-state` | `portable` | `TaskArtifactDTO`、`CheckpointRefDTO` | `guru-task-portable-router` |
| `guru-checkpoint-task-state` | `already_portable` | 与`portable`相同 | `guru-task-portable-router` |
| `guru-checkpoint-task-state` | `blocked` | `ReasonDTO` | `task-checkpoint-blocked` stop |
| `guru-transfer-task-machine` | `source_released` | `HandoffRefDTO`、`HandoffInventoryRefDTO` | `guru-cleanup-task-resources:machine_handoff_cleanup` |
| `guru-transfer-task-machine` | `destination_ready` | `TaskArtifactDTO`、new `BranchBindingRefDTO`、`HandoffRefDTO`、`session_outcome` | `guru-machine-transfer-ready-router` |
| `guru-transfer-task-machine` | `session_binding_recovery_required` | `TaskArtifactDTO`、`HandoffRefDTO`、`ReasonDTO` | `guru-bind-task-session` |
| `guru-transfer-task-machine` | `source_recovered` | `TaskArtifactDTO`、current `BranchBindingRefDTO`、`HandoffRefDTO` | `guru-machine-transfer-source-recovered-router` |
| `guru-transfer-task-machine` | `resume_transfer` | `HandoffRefDTO`、`ReasonDTO` | `guru-transfer-task-machine` same handoff profile |
| `guru-transfer-task-machine` | `blocked` | `ReasonDTO` | `machine-transfer-blocked` stop |
| `guru-bind-task-session` | `session_resumed` | `TaskArtifactDTO`、`resume_target` | `guru-bind-task-session-resume-router` |
| `guru-bind-task-session` | `session_rebound` | `TaskArtifactDTO`、`resume_target` | `guru-bind-task-session-rebind-router` |
| `guru-bind-task-session` | `task_switched` | `TaskArtifactDTO`、`resume_target` | `guru-bind-task-session-switch-router` |
| `guru-bind-task-session` | `reactivate_rebound` | `TaskArtifactDTO`、`resume_target` | `guru-bind-task-session-reactivate-router` |
| `guru-bind-task-session` | `session_manually_recovered` | `TaskArtifactDTO`、`resume_target` | `guru-bind-task-session-manual-recovery-router` |
| `guru-bind-task-session` | `explicit_task_mode` | `TaskArtifactDTO` | `guru-current-phase-router` |
| `guru-bind-task-session` | `binding_blocked` | `ReasonDTO` | `task-session-binding-blocked` stop |
| `guru-review-task-completion` | `remaining_work` | `TaskArtifactDTO`、`ReasonDTO` | `active-task-continuation` workflow target |
| `guru-review-task-completion` | `evidence_pending` | `TaskArtifactDTO`、`ReasonDTO` | `guru-review-task-completion` evidence-refresh profile |
| `guru-review-task-completion` | `additional_delivery_required` | `TaskArtifactDTO`、`ReasonDTO` | `task-delivery-planning-router` |
| `guru-review-task-completion` | `requirements_revision_required` | `TaskArtifactDTO`、`ReasonDTO` | `guru-clarify-requirements` active-task profile |
| `guru-review-task-completion` | `implementation_revision_required` | `TaskArtifactDTO`、`ReasonDTO` | `guru-resume-implementation` workflow target |
| `guru-review-task-completion` | `completed` | `ResultRefDTO` | `guru-complete-task-closure` |
| `guru-review-task-completion` | `blocked` | `ReasonDTO` | `task-completion-blocked` stop |
| `guru-complete-task-closure` | `closed` | Closure `ResultRefDTO` | `guru-finish-task` |
| `guru-complete-task-closure` | `no_mutation` | Closure `ResultRefDTO` | `guru-finish-task` |
| `guru-complete-task-closure` | `resume_closure` | `TransactionRefDTO` | `guru-complete-task-closure` |
| `guru-complete-task-closure` | `external_change_conflict` | `TransactionRefDTO`、`ReasonDTO` | `guru-complete-task-closure` semantic re-entry |
| `guru-complete-task-closure` | `blocked` | `ReasonDTO` | `task-closure-blocked` stop |
| `guru-finish-task` | `success` | `ResourceSealRefDTO` | `guru-cleanup-task-resources` normal profile |
| `guru-finish-task` | `closure_refresh_required` | Closure `ResultRefDTO`、`ReasonDTO` | `guru-complete-task-closure` |
| `guru-finish-task` | `resume_finish` | `TransactionRefDTO` | `guru-finish-task` |
| `guru-finish-task` | `manual_cleanup_required` | `TerminalFinishRefDTO`、`ReasonDTO` | `guru-cleanup-task-resources:manual_cleanup` |
| `guru-finish-task` | `blocked` | `ReasonDTO` | `task-finish-blocked` stop |
| `guru-cleanup-task-resources` | `cleaned` | `CleanupResultRefDTO` | `task-cleanup-complete` stop |
| `guru-cleanup-task-resources` | `remaining_resources` | `CleanupResultRefDTO`、`ReasonDTO` | `guru-cleanup-task-resources` same profile |
| `guru-cleanup-task-resources` | `manual_selection_required` | `TerminalFinishRefDTO`、`ReasonDTO` | `guru-cleanup-task-resources:manual_cleanup` |
| `guru-cleanup-task-resources` | `handoff_cleanup_complete` | `HandoffRefDTO`、`CleanupResultRefDTO` | `machine-transfer-await-destination` stop |
| `guru-cleanup-task-resources` | `handoff_cleanup_remaining` | `HandoffRefDTO`、`CleanupResultRefDTO`、`ReasonDTO` | `guru-cleanup-task-resources:machine_handoff_cleanup` |
| `guru-cleanup-task-resources` | `blocked` | `ReasonDTO` | `task-cleanup-blocked` stop |
| `guru-reactivate-task` | `reactivated_to_planning` | new `TaskArtifactDTO`、new `BranchBindingRefDTO`、`session_outcome` | `task-planning-router` |
| `guru-reactivate-task` | `session_binding_recovery_required` | new `TaskArtifactDTO`、`ReasonDTO` | `guru-bind-task-session` |
| `guru-reactivate-task` | `resume_reactivation` | `TransactionRefDTO`、`ReasonDTO` | `guru-reactivate-task` same transaction profile |
| `guru-reactivate-task` | `source_correction_required` | archived `TaskLifecycleDTO`、`ReasonDTO` | `guru-reconcile-task-source:prepare_reactivation_correction` |
| `guru-reactivate-task` | `reactivate_blocked` | `ReasonDTO` | `task-reactivate-blocked` stop |

`guru-task-identity-established-router`、`guru-task-lifecycle-repaired-router`、`guru-task-source-current-router`、
`guru-task-target-current-router`、`guru-task-binding-established-router`、`guru-task-rebound-router`、
`guru-task-checkout-ready-router`、`guru-task-portable-router`、`guru-machine-transfer-ready-router`、
`guru-machine-transfer-source-recovered-router`与`guru-current-phase-router`均是workflow target。它们只根据当前
declared intent和fresh lifecycle state选择本文件已列出的named Skill，不执行semantic判断，不产生新public DTO。

## 4. 现有stage owner的exit迁移

以下owner按表迁移exit与唯一consumer。其output中旧task path/workspace payload统一投影为`TaskArtifactDTO`；
现有内容identity、PR identity与result identity字段仅在原consumer直接需要时保留。

| Producer | Preserved exits and consumers |
| --- | --- |
| `guru-clarify-requirements` | `clear -> guru-requirements-clear-router`；`needs_context -> guru-discover-change-context`；`refresh_context -> guru-sync-base`；`retarget_context -> guru-sync-base`；`new_task -> guru-full-task-intake-chain`；`blocked -> stop`。active-task `clear`由router确定性投影到Planning或current phase，不执行scope判断 |
| `guru-approve-task-plan` | `approved -> phase-1-task-activation` workflow target；`revision_required -> self`；`clarify_scope -> guru-clarify-requirements`；`blocked -> stop`。workflow target完成dialogue-local planning pause后只调用`guru-activate-task` |
| `guru-reconcile-task-base` | `reconciled -> guru-base-reconciliation-router`；`review_continuity_required -> guru-review-branch`；`implementation_required -> guru-resume-implementation`；`planning_stale -> guru-approve-task-plan`；`scope_confirmation_required -> guru-clarify-requirements`；`blocked -> stop` |
| `guru-check-task` | `passed -> guru-create-task-commit`；`implementation_required -> guru-resume-implementation`；`planning_stale -> guru-approve-task-plan`；`blocked -> stop` |
| `guru-create-task-commit` | `committed -> guru-review-branch`；`revision-required -> self`；`blocked -> stop` |
| `guru-review-task-delivery` | `ready -> guru-publish-task-delivery`；`planning_revision_required -> task-delivery-planning-router`；`implementation_required -> guru-resume-implementation`；`scope_confirmation_required -> guru-clarify-requirements`；`blocked -> stop` |
| `guru-publish-task-delivery` | `ready_for_merge -> guru-merge-task-delivery`；`review_stale -> guru-review-task-delivery`；`resume_publication -> self`；`reprepare_required -> self`；`blocked -> stop` |
| `guru-review-branch` | `passed -> guru-review-task-publication`；`continuity_passed -> guru-base-continuity-passed-router`；`implementation_required -> guru-resume-implementation`；`scope_confirmation_required -> guru-clarify-requirements`；`blocked -> stop`；`archived_review_passed` retired |
| `guru-review-task-publication` | `ready -> guru-finalize-task`；`return_to_task_work -> guru-resume-implementation`；`blocked -> stop`；`archived_ready` retired。`ready`只证明publication payload与delivery readiness，不决定Closure disposition，不写closing keyword |
| `guru-finalize-task` | `base_reconciliation_required -> guru-reconcile-task-base`；`publication_review_stale -> guru-review-task-publication`；`resume_finalization -> self`；`reprepare_required -> self`；`ready_for_merge -> guru-merge-task-pr`；`blocked -> stop`；`archived_review_refresh` profile retired；新major contract不移动task到archive、不产生Issue closing effect |
| `guru-merge-task-delivery` | `delivered -> guru-review-task-completion`；`merge_blocked -> stop`；`implementation_required -> guru-resume-implementation`；`review_refresh_required -> guru-review-task-delivery` |
| `guru-merge-task-pr` | `merged -> guru-review-task-completion`；`review_refresh_required -> guru-review-branch`；`implementation_required -> guru-resume-implementation`；`merge_blocked -> stop`；`phase2_reentry_required`与`closure_mismatch` retired。Merge不读取closing keywords、不读取Issue、不验证Closure effect |
| `guru-restore-archived-task` | `restored_to_phase2 -> guru-resume-implementation`；`restored_for_merge_recovery -> guru-merge-task-pr` terminal-recovery profile；`restore_blocked -> stop` |

上述owner的output projection固定如下，不沿用旧path-only output：

| Producer exit | Minimal output |
| --- | --- |
| `guru-clarify-requirements:clear` active-task profile | `TaskArtifactDTO`、`ResultRefDTO` |
| `guru-approve-task-plan:approved` | `PlanningApprovalRefDTO` |
| `guru-reconcile-task-base:reconciled` | `BaseReconcileResultDTO` |
| `guru-reconcile-task-base:review_continuity_required` | `BaseContinuitySeedDTO` |
| `guru-check-task:passed` | `Phase2ResultDTO` |
| `guru-create-task-commit:committed` | `TaskCommitResultDTO` |
| `guru-review-branch:passed` | `BranchReviewResultDTO` |
| `guru-review-branch:continuity_passed` | `BaseContinuityResultDTO` |
| `guru-review-task-delivery:ready` | `DeliveryReviewReadyDTO` |
| `guru-publish-task-delivery:ready_for_merge` | `DeliveryMergeReadyDTO` |
| `guru-review-task-publication:ready` | `PublicationReadyDTO` |
| `guru-finalize-task:ready_for_merge` | `MergeReadyDTO` |
| `guru-finalize-task:base_reconciliation_required` | `FinalizerBaseReconcileSeedDTO` |
| `guru-finalize-task:publication_review_stale` | `PublicationRefreshSeedDTO` |
| `guru-finalize-task:resume_finalization|reprepare_required` | `FinalizationReprepareRefDTO` |
| `guru-merge-task-delivery:delivered` | `DeliveryMergeResultDTO` |
| `guru-merge-task-pr:merged` | `TaskMergeResultDTO`，normal profile固定`merge_lineage=closeout`，terminal-recovery profile固定`merge_lineage=pre_cutover_recovered` |
| `guru-restore-archived-task:restored_to_phase2` | `TaskArtifactDTO`、`ResultRefDTO` |
| `guru-restore-archived-task:restored_for_merge_recovery` | `TaskArtifactDTO`、`MergedPRRecoveryRefDTO` |

`guru-publish-task-delivery:resume_publication|reprepare_required`固定输出`TransactionRefDTO + ReasonDTO`；
`guru-finalize-task:resume_finalization|reprepare_required`继续输出`FinalizationReprepareRefDTO`。所有
`revision-required`、`revision_required`、`implementation_required`、`planning_stale|planning_revision_required`、
`scope_confirmation_required|clarify_scope`、`review_stale|review_refresh_required`与`return_to_task_work`输出固定为
`TaskArtifactDTO + ReasonDTO`。Same-owner transaction resume输出固定为对应named transaction DTO；普通blocked输出
固定为`ReasonDTO`。Pre-task Clarify profiles继续使用各自现有最小context DTO，但其中workspace/path字段数必须为0。

`SourceCorrectionReadyDTO.current_source`与`reviewed_source`严格使用问题02声明的`IssueSource|NoIssueSource`
封闭结构。`TransactionRefDTO.result_id`标识该transaction当前已持久化的恢复结果，不表示transaction已terminal；
consumer必须同时验证`transaction_id`并只恢复同一owner mutation。普通transaction的`lifecycle_generation`绑定
其current TaskLifecycleKey；Reactivate transaction固定绑定target generation `g+1`，private transaction另外保存并
验证source generation `g`，不得把两代authority合并。

`guru-create-task-workspace:created`迁移为`guru-create-task:created`；`refresh_review`与`invalid_task_state`保留exit id并
更换producer；旧`blocked` stop id改为`task-creation-blocked`。不存在同时发布old/new producer的兼容期。

新active graph对每个merge cycle恰好选择一条上游链：

- task closeout：Branch Review `passed` -> Publication Review `ready` -> Finalizer `ready_for_merge` ->
  Merge PR `merged`；
- active Delivery slice：Delivery Review `ready` -> Publish Delivery `ready_for_merge` -> Merge Delivery `delivered`。

同一cycle内两条链不互相调用，只在merge result之后进入Completion。Completion返回
`additional_delivery_required`时，同一TaskLifecycleKey的后续cycle进入active Delivery slice链；Completion
`completed`后固定进入Closure `closed|no_mutation` -> Finish `success|manual_cleanup_required` -> Cleanup。
Finalizer不得写archive locator、terminal status、Finish result或Cleanup inventory。Publication、Finalizer与
两个Merge owner均不得产生closing keyword、Issue mutation或Closure verification。

Pre-cutover premature archive固定分为两个互斥migration profile，不进入旧archived-review链：

1. PR尚未merged或不存在时，`guru-restore-archived-task:pre_merge_restore`把同一generation恢复为
   `active(in_progress)`；它采用仍匹配exact PR head的existing branch/checkout，或按共享acquisition合同从该head
   provision non-target branch，使旧Branch Review/Publication/Finalizer evidence stale，并只返回
   `restored_to_phase2`；
2. exact PR已经merged时，`guru-restore-archived-task:post_merge_restore`把同一generation恢复为
   `active(in_progress)`；它从live merge commit采用或provision一个不等于Delivery target的recovery branch，按
   create/reuse facts建立association与ownership，只返回`restored_for_merge_recovery`；`guru-merge-task-pr`从live
   merged PR恢复exact `merged` result，固定输出`merge_lineage=pre_cutover_recovered`后进入Completion，不重复merge
   或其它remote mutation。该lineage不伪造已退役的Branch Review/Publication pass；Completion固定读取restored
   `TaskArtifactDTO`、`MergedPRRecoveryRefDTO`、`TaskMergeResultDTO`、current accepted scope、live merged PR/merge
   commit/tree与current planning artifact，独立返回
   `completed|evidence_pending|remaining_work|requirements_revision_required|implementation_revision_required`。
   `evidence_pending`只表示上述固定输入暂时不可读或不完整，并重入同一migration Completion profile；它不得路由到
   旧Branch Review、closeout Publication、Delivery Review或Delivery Publication以补造历史pass。

Old Finalizer写入的archive presence不是Finish result。只有新`guru-finish-task` transaction产生的
`finish_in_progress|sealed`才能进入Finish recovery。上述migration完成前不得Reactivate、Cleanup或继续旧
`archived_review_passed -> archived_ready -> archived_review_refresh` route。

## 5. Consumer projection规则

1. Producer output到consumer input只执行字段select、rename与固定discriminator注入；不得读取producer private
   checkpoint、重新计算semantic conclusion或补造缺失字段。
2. Workflow target收到DTO后先验证schema、TaskLifecycleKey与current producer result identity，再调用唯一consumer。
3. Same-owner recovery只接受原transaction/result identity；结果丢失时rematerialize同一exit，不创建第二次mutation。
4. `blocked`永远进入named stop，不得由generic dispatcher猜测下一owner。
5. User selection发生在拥有该选择的semantic Skill内部。零候选与多候选保持Skill active，不通过`blocked`拒绝
   合法人工指定。
6. `reconcile_required`只说明当前指定target不满足rebind合同。它进入named non-terminal stop，保持原association
   与resource state不变；用户完成独立Git/history reconciliation或改选合法target后重新调用Rebind。Workflow
   router不得替用户决定reconcile机制。
7. `session_outcome`封闭为`session_bound`与`explicit_task_mode`。Session write/verify失败使用独立
   `session_binding_recovery_required` exit投影到`guru-bind-task-session`，不回滚已经提交的lifecycle mutation。
8. Exit或consumer未出现在本文件、interface package与workflow graph三方一致集合中时，activation gate失败。
9. Reserved receipt ref namespace不得出现在Create、Reactivate、Ensure Checkout、Rebind、Delivery target或
   missing-association candidate的validated target set中。

## 6. 旧public identity处置

| Old identity | Exact disposition |
| --- | --- |
| `guru-create-task-workspace` | retired；`guru-create-task`承担新contract |
| `guru-task-workspace-created` | retired；`guru-task-created`承担workflow target |
| `record-task-workspace-plan` | retired；`record-task-plan`承担deterministic recorder |
| `create-task-workspace` | retired；`create-task`承担executor |
| `check-task-workspace-result` | retired；`check-task-creation-result`承担validator |
| `recover-task-workspace-result` | retired；`recover-created-task-result`承担same-result recovery |
| `invoke-guru-create-task-workspace` | retired；`invoke-guru-create-task`承担launcher |
| `check-workspace-boundary` | retired；`check-task-checkout-boundary`承担validator |
| `guru-review-branch:archived_review_passed` | retired；pre-cutover premature archive先由Restore回到active graph |
| `guru-review-task-publication:archived_ready` | retired；pre-cutover premature archive先由Restore回到active graph |
| `guru-finalize-task:archived_review_refresh` | retired；不存在post-cutover archived Finalizer route |
| `guru-merge-task-pr:phase2_reentry_required` | retired；active task finding使用`implementation_required` |
| `guru-merge-task-pr:closure_mismatch` | retired；Merge不拥有Closure effect |
| Publication/Finalizer closing-keyword output | retired；PR body不得产生Issue closing effect |
| `guru-reactivate-task:reactivated_to_requirements` | retired；新generation固定先进入`reactivated_to_planning`，再由Planning route进入requirements |
| `guru-reactivate-task:reactivated_to_implementation` | retired；新generation必须先完成Planning approval与activation |
| `guru-reactivate-task:reactivated_to_evidence_refresh` | retired；新generation必须先完成Planning approval与activation，再由Completion owner判断evidence route |
| 其它workspace public ID | `retired_without_replacement`；production graph引用数必须为0 |

旧schema、example、consumer projection、workflow marker、stop id、command registry、manifest entry、continuation text与
platform overlay必须在同一activation candidate中完成上述处置。旧ID不得保留alias、deprecated reader或translation
shim。

## 7. Activation gate

Production activation前必须同时证明：

1. 每个public Skill的declared exits与本文件一致；
2. 每个exit恰好一个consumer；
3. 每个consumer input有确定性projection；
4. 每个workflow target与stop均存在且类型匹配；
5. old producer、old exit marker、old consumer、old schema与old command引用数均为0；
6. public output machine-local checkout/workspace path字段数为0；portable repository-relative `task_ref`不计入该项；
7. 所有recovery exit均绑定exact original transaction/result identity；
8. Publication、Finalizer与Merge的closing-keyword writer count和Issue closure-effect reader count均为0；
9. pre-cutover premature archive两条profile分别只能投影到`restored_to_phase2`与
   `restored_for_merge_recovery`；
10. unknown、multiple、unmapped exit固定fail closed。

## 8. 当前设计结论

1. Public API迁移以producer/exit/consumer/projection四元组为单位，不以owner名称清单替代；
2. 新增owner与受影响stage owner的全部exit均有唯一consumer；
3. `created`、`refresh_review`、`ready`、`blocked`、re-entry与recovery route均有明确处置；
4. 合法人工选择保留在semantic owner内部，不因自动推导失败而永久fail close；
5. Publication/Finalizer/Merge不再提前执行Closure，terminal graph只保留一个Issue disposition owner；
6. pre-cutover premature archive按merged state进入两条互斥Restore profile，不复用旧archived-review链；
7. old workspace public graph在one-step activation中彻底退出。

## 9. 跨任务 contract 承接

本文件的 public contract 是 #454 substrate 与上层 lifecycle graph 之间的迁移边界。#434、#443、#436 的新
consumer 必须在实现前完成 fresh contract reconcile，并逐项绑定到本文件声明的 DTO、exit、consumer 和 projection。
任何 package 不得通过保留旧 `workspace`、path-bearing session、旧 Reactivate exit 或自有 resource ledger 来绕过
该迁移。

`#454` 不接管 `#443`、`#436` 或 `#434` 的 semantic owner；它只提供共同 substrate 和 public I/O。`#434` 在
reconcile 后只编排并拥有 Delivery、Completion、Closure、Finish、Cleanup graph，不能重新实现 identity、session、
checkout、branch association、resource ledger 或 Reactivate。

历史 #443、#436 task 文档、旧 Issue evidence 与旧审查结论保持 immutable。contract reconcile 与 package migration
必须由当前 package 的迁移记录或新的 migration task 记录；不得回改历史 task 文档、不得新增旧 producer/new producer
双发布期、不得把旧 evidence 投影为新 contract 已通过。

实现顺序固定为：#454 contract 定稿 -> 受影响 package reconcile -> #454 substrate 实现 -> package/schema/
projection/route migration -> fresh reconcile #434 -> #434 production graph 实现与 activation。任一步骤缺少前置
contract 或 consumer projection 时，后续 activation 不可达。
