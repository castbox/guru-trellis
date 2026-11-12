# Guru Team routing reference

This managed Markdown reference is part of the global workflow, not a second
workflow or a runtime route table. The registry and each package Interface own
public Skill contracts. The markers below declare their mandatory invocation,
exit and unique consumer integration. The runtime checks that agreement; AI
executes the original target conditions and original Skill contracts.

After an original Skill returns one typed exit, query the existing
`discover-skill-contract` command with `--skill <producer> --exit <exit>`.
Use only that consumer and entry. Unknown, multiple, unmapped, mismatched or
missing graph facts stop; a query result never establishes semantic pass.
Do not load this complete reference on the normal current-step path.

## Mandatory Skills and exits

The active inventory comes from the current registry and Interfaces.
Standalone-only installation upgrade and extension verification remain outside
the business-task mandatory invokes. Qualification invocation is conditional
on each original owner's applicability contract, as defined below.

<!-- guru-skill-invoke: {"skill":"guru-bootstrap-repository-ssot","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-bootstrap-repository-ssot","exit":"completed","consumer":{"kind":"workflow","id":"guru-bootstrap-repository-ssot-completed-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-bootstrap-repository-ssot","exit":"baseline_incomplete","consumer":{"kind":"workflow","id":"guru-bootstrap-repository-ssot-baseline-incomplete-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-bootstrap-repository-ssot","exit":"repair_required","consumer":{"kind":"skill","id":"guru-bootstrap-repository-ssot"}} -->
<!-- guru-skill-exit: {"skill":"guru-bootstrap-repository-ssot","exit":"blocked","consumer":{"kind":"stop","id":"guru-bootstrap-repository-ssot-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-maintain-architecture-baseline","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-architecture-baseline","exit":"baseline_current","consumer":{"kind":"workflow","id":"guru-architecture-baseline-current-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-architecture-baseline","exit":"sync_required","consumer":{"kind":"workflow","id":"guru-architecture-baseline-sync-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-architecture-baseline","exit":"baseline_incomplete","consumer":{"kind":"workflow","id":"guru-architecture-baseline-bootstrap-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-architecture-baseline","exit":"architecture_conflict","consumer":{"kind":"workflow","id":"guru-architecture-baseline-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-architecture-baseline","exit":"contract_incomplete","consumer":{"kind":"workflow","id":"guru-architecture-baseline-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-architecture-baseline","exit":"fitness_regression","consumer":{"kind":"workflow","id":"guru-architecture-baseline-check-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-architecture-baseline","exit":"blocked","consumer":{"kind":"stop","id":"architecture-baseline-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-maintain-requirements-design-test-ssot","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"candidate_ready","consumer":{"kind":"workflow","id":"guru-requirements-design-test-ssot-current-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"ssot_current","consumer":{"kind":"workflow","id":"guru-requirements-design-test-ssot-current-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"sync_required","consumer":{"kind":"skill","id":"guru-maintain-requirements-design-test-ssot"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"revision_required","consumer":{"kind":"workflow","id":"guru-requirements-design-test-ssot-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"baseline_incomplete","consumer":{"kind":"workflow","id":"guru-requirements-design-test-ssot-bootstrap-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"blocked","consumer":{"kind":"stop","id":"requirements-design-test-ssot-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-qualify-normal-scenario","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"classified","consumer":{"kind":"workflow","id":"guru-normal-scenario-classified-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"scope_confirmation_required","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"mechanism_revision_required","consumer":{"kind":"workflow","id":"guru-normal-scenario-mechanism-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"blocked","consumer":{"kind":"stop","id":"normal-scenario-qualification-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-qualify-solution-mechanism","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-solution-mechanism","exit":"classified","consumer":{"kind":"workflow","id":"guru-solution-mechanism-classified-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-solution-mechanism","exit":"scope_confirmation_required","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-solution-mechanism","exit":"mechanism_revision_required","consumer":{"kind":"workflow","id":"guru-solution-mechanism-mechanism-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-solution-mechanism","exit":"blocked","consumer":{"kind":"stop","id":"solution-mechanism-qualification-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-qualify-root-cause","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-root-cause","exit":"classified","consumer":{"kind":"workflow","id":"guru-root-cause-classified-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-root-cause","exit":"mechanism_revision_required","consumer":{"kind":"workflow","id":"guru-root-cause-mechanism-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-root-cause","exit":"diagnosis_required","consumer":{"kind":"workflow","id":"guru-root-cause-diagnosis-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-root-cause","exit":"blocked","consumer":{"kind":"stop","id":"root-cause-qualification-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-select-workflow-mode","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-select-workflow-mode","exit":"standard_intake","consumer":{"kind":"workflow","id":"guru-workflow-standard-intake-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-select-workflow-mode","exit":"task_free","consumer":{"kind":"skill","id":"guru-execute-task-free-change"}} -->
<!-- guru-skill-exit: {"skill":"guru-select-workflow-mode","exit":"blocked","consumer":{"kind":"stop","id":"workflow-mode-selection-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-execute-task-free-change","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-execute-task-free-change","exit":"completed","consumer":{"kind":"workflow","id":"guru-task-free-completed"}} -->
<!-- guru-skill-exit: {"skill":"guru-execute-task-free-change","exit":"resume_active_task","consumer":{"kind":"workflow","id":"guru-task-free-resume-active-task-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-execute-task-free-change","exit":"scope_change","consumer":{"kind":"workflow","id":"guru-task-free-scope-change-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-execute-task-free-change","exit":"location_required","consumer":{"kind":"skill","id":"guru-execute-task-free-change"}} -->
<!-- guru-skill-exit: {"skill":"guru-execute-task-free-change","exit":"reselect_mode","consumer":{"kind":"skill","id":"guru-select-workflow-mode"}} -->
<!-- guru-skill-exit: {"skill":"guru-execute-task-free-change","exit":"explicit_choice_required","consumer":{"kind":"skill","id":"guru-execute-task-free-change"}} -->
<!-- guru-skill-exit: {"skill":"guru-execute-task-free-change","exit":"blocked","consumer":{"kind":"stop","id":"task-free-change-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-sync-base","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-sync-base","exit":"synced","consumer":{"kind":"skill","id":"guru-discover-change-context"}} -->
<!-- guru-skill-exit: {"skill":"guru-sync-base","exit":"baseline_ready","consumer":{"kind":"skill","id":"guru-discover-change-context"}} -->
<!-- guru-skill-exit: {"skill":"guru-sync-base","exit":"skipped","consumer":{"kind":"workflow","id":"original-request-route"}} -->
<!-- guru-skill-exit: {"skill":"guru-sync-base","exit":"blocked","consumer":{"kind":"stop","id":"base-sync-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-discover-change-context","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-discover-change-context","exit":"context_ready","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-discover-change-context","exit":"refresh_base","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-discover-change-context","exit":"blocked","consumer":{"kind":"stop","id":"change-context-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-clarify-requirements","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"clear","consumer":{"kind":"workflow","id":"guru-requirements-clear-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"scope_ready","consumer":{"kind":"workflow","id":"guru-requirements-clear-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"needs_context","consumer":{"kind":"skill","id":"guru-discover-change-context"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"refresh_context","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"retarget_context","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"new_task","consumer":{"kind":"workflow","id":"guru-full-task-intake-chain"}} -->
<!-- guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"blocked","consumer":{"kind":"stop","id":"requirements-clarification-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-review-contract-wording","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-contract-wording","exit":"pass","consumer":{"kind":"workflow","id":"guru-contract-wording-pass-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-contract-wording","exit":"content_changed","consumer":{"kind":"workflow","id":"guru-contract-wording-change-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-contract-wording","exit":"blocked","consumer":{"kind":"stop","id":"contract-wording-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-review-change-request","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"ready","consumer":{"kind":"workflow","id":"guru-task-intake-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"clarify_requirements","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"review_wording","consumer":{"kind":"skill","id":"guru-review-contract-wording"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"refresh_context","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"blocked","consumer":{"kind":"stop","id":"change-request-review-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-create-issue","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-issue","exit":"created","consumer":{"kind":"workflow","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-issue","exit":"refresh_review","consumer":{"kind":"workflow","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-issue","exit":"blocked","consumer":{"kind":"stop","id":"issue-creation-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-create-task","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-task","exit":"created","consumer":{"kind":"workflow","id":"guru-task-created"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task","exit":"refresh_review","consumer":{"kind":"workflow","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task","exit":"blocked","consumer":{"kind":"stop","id":"task-creation-blocked"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task","exit":"invalid_task_state","consumer":{"kind":"stop","id":"invalid-task-state"}} -->
<!-- guru-skill-invoke: {"skill":"guru-establish-task-identity","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-establish-task-identity","exit":"identity_established","consumer":{"kind":"workflow","id":"guru-current-task-identity-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-establish-task-identity","exit":"source_review_required","consumer":{"kind":"workflow","id":"guru-task-source-review-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-establish-task-identity","exit":"invalid_task_state","consumer":{"kind":"stop","id":"invalid-task-state"}} -->
<!-- guru-skill-exit: {"skill":"guru-establish-task-identity","exit":"blocked","consumer":{"kind":"stop","id":"task-identity-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-establish-task-branch-binding","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-establish-task-branch-binding","exit":"binding_established","consumer":{"kind":"workflow","id":"guru-task-branch-established-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-establish-task-branch-binding","exit":"selection_required","consumer":{"kind":"workflow","id":"guru-task-branch-selection-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-establish-task-branch-binding","exit":"invalid_task_state","consumer":{"kind":"stop","id":"invalid-task-state"}} -->
<!-- guru-skill-exit: {"skill":"guru-establish-task-branch-binding","exit":"blocked","consumer":{"kind":"stop","id":"task-branch-binding-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-ensure-task-checkout","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-ensure-task-checkout","exit":"checkout_resolved","consumer":{"kind":"workflow","id":"guru-current-task-checkout-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-ensure-task-checkout","exit":"binding_required","consumer":{"kind":"workflow","id":"guru-task-branch-binding-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-ensure-task-checkout","exit":"checkout_required","consumer":{"kind":"workflow","id":"guru-task-checkout-acquisition-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-ensure-task-checkout","exit":"invalid_task_state","consumer":{"kind":"stop","id":"invalid-task-state"}} -->
<!-- guru-skill-invoke: {"skill":"guru-rebind-task-branch","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-rebind-task-branch","exit":"rebound","consumer":{"kind":"workflow","id":"guru-task-branch-rebound-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-rebind-task-branch","exit":"refresh_review","consumer":{"kind":"workflow","id":"guru-task-branch-rebind-refresh-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-rebind-task-branch","exit":"invalid_task_state","consumer":{"kind":"stop","id":"invalid-task-state"}} -->
<!-- guru-skill-exit: {"skill":"guru-rebind-task-branch","exit":"blocked","consumer":{"kind":"stop","id":"task-branch-rebind-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-bind-task-session","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-bind-task-session","exit":"session_resumed","consumer":{"kind":"workflow","id":"guru-bind-task-session-resume-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-bind-task-session","exit":"session_rebound","consumer":{"kind":"workflow","id":"guru-bind-task-session-rebind-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-bind-task-session","exit":"task_switched","consumer":{"kind":"workflow","id":"guru-bind-task-session-switch-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-bind-task-session","exit":"reactivate_rebound","consumer":{"kind":"workflow","id":"guru-bind-task-session-reactivate-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-bind-task-session","exit":"session_manually_recovered","consumer":{"kind":"workflow","id":"guru-bind-task-session-manual-recovery-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-bind-task-session","exit":"explicit_task_mode","consumer":{"kind":"workflow","id":"guru-current-phase-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-bind-task-session","exit":"binding_blocked","consumer":{"kind":"stop","id":"task-session-binding-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-create-delivery","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-delivery","exit":"created","consumer":{"kind":"workflow","id":"guru-delivery-planning-author-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-delivery","exit":"scope_revision_required","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-delivery","exit":"selection_required","consumer":{"kind":"workflow","id":"guru-delivery-selection-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-delivery","exit":"blocked","consumer":{"kind":"stop","id":"delivery-creation-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-activate-delivery","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-activate-delivery","exit":"delivery_started","consumer":{"kind":"workflow","id":"guru-delivery-started-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-activate-delivery","exit":"delivery_stopped","consumer":{"kind":"skill","id":"guru-review-task-completion"}} -->
<!-- guru-skill-exit: {"skill":"guru-activate-delivery","exit":"planning_refresh_required","consumer":{"kind":"workflow","id":"guru-delivery-activation-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-activate-delivery","exit":"invalid_delivery_state","consumer":{"kind":"stop","id":"invalid-delivery-state"}} -->
<!-- guru-skill-exit: {"skill":"guru-activate-delivery","exit":"blocked","consumer":{"kind":"stop","id":"delivery-activation-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-author-task-plan","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-author-task-plan","exit":"requirements_ready","consumer":{"kind":"workflow","id":"guru-task-plan-requirements-ready-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-author-task-plan","exit":"plan_ready","consumer":{"kind":"workflow","id":"guru-task-plan-ready-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-author-task-plan","exit":"clarify_scope","consumer":{"kind":"workflow","id":"guru-task-plan-clarify-scope-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-author-task-plan","exit":"blocked","consumer":{"kind":"stop","id":"task-plan-author-blocked"}} -->
<!-- guru-skill-exit: {"skill":"guru-author-task-plan","exit":"scope_requirements_ready","consumer":{"kind":"workflow","id":"guru-task-scope-requirements-ready-router"}} -->
<!-- guru-skill-invoke: {"skill":"guru-approve-task-plan","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"approved","consumer":{"kind":"workflow","id":"phase-1-delivery-activation"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"revision_required","consumer":{"kind":"workflow","id":"guru-task-plan-approval-revision-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"clarify_scope","consumer":{"kind":"workflow","id":"guru-task-plan-clarify-scope-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"blocked","consumer":{"kind":"stop","id":"task-plan-approval-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-reconcile-task-base","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"reconciled","consumer":{"kind":"workflow","id":"guru-base-reconciliation-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"review_continuity_required","consumer":{"kind":"skill","id":"guru-review-branch"}} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-resume-implementation"}} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"planning_stale","consumer":{"kind":"workflow","id":"guru-task-base-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"scope_confirmation_required","consumer":{"kind":"workflow","id":"guru-task-base-scope-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"blocked","consumer":{"kind":"stop","id":"task-base-reconciliation-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-create-task-commit","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"pre_review_committed","consumer":{"kind":"workflow","id":"guru-pre-review-commit-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"revision-required","consumer":{"kind":"skill","id":"guru-create-task-commit"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"blocked","consumer":{"kind":"stop","id":"task-commit-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-review-branch","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"planning_stale","consumer":{"kind":"workflow","id":"guru-task-check-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"delivery_stopped","consumer":{"kind":"skill","id":"guru-review-task-completion"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"passed","consumer":{"kind":"skill","id":"guru-review-task-delivery"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"archived_review_passed","consumer":{"kind":"stop","id":"legacy-archived-review-disposition-required"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"continuity_passed","consumer":{"kind":"workflow","id":"guru-base-continuity-passed-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-branch-review-implementation-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"scope_confirmation_required","consumer":{"kind":"workflow","id":"guru-branch-review-scope-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"blocked","consumer":{"kind":"stop","id":"branch-review-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-review-task-delivery","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-delivery","exit":"delivery_stopped","consumer":{"kind":"skill","id":"guru-review-task-completion"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-delivery","exit":"ready","consumer":{"kind":"skill","id":"guru-publish-task-delivery"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-delivery","exit":"planning_revision_required","consumer":{"kind":"workflow","id":"guru-task-delivery-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-delivery","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-resume-implementation"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-delivery","exit":"scope_confirmation_required","consumer":{"kind":"workflow","id":"guru-task-delivery-scope-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-delivery","exit":"blocked","consumer":{"kind":"stop","id":"task-delivery-review-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-publish-task-delivery","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"draft_revision_ready","consumer":{"kind":"workflow","id":"guru-draft-revision-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"draft_published","consumer":{"kind":"workflow","id":"guru-draft-feedback-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"delivery_stopped","consumer":{"kind":"skill","id":"guru-review-task-completion"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"ready_for_merge","consumer":{"kind":"skill","id":"guru-merge-task-delivery"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"review_stale","consumer":{"kind":"skill","id":"guru-review-task-delivery"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"resume_publication","consumer":{"kind":"skill","id":"guru-publish-task-delivery"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"reprepare_required","consumer":{"kind":"skill","id":"guru-publish-task-delivery"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"blocked","consumer":{"kind":"stop","id":"task-delivery-publication-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-merge-task-delivery","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-delivery","exit":"delivery_stopped","consumer":{"kind":"skill","id":"guru-review-task-completion"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-delivery","exit":"delivered","consumer":{"kind":"skill","id":"guru-review-task-completion"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-delivery","exit":"merge_blocked","consumer":{"kind":"stop","id":"task-delivery-merge-blocked"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-delivery","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-resume-implementation"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-delivery","exit":"review_refresh_required","consumer":{"kind":"skill","id":"guru-review-task-delivery"}} -->
<!-- guru-skill-invoke: {"skill":"guru-review-task-completion","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-completion","exit":"remaining_work","consumer":{"kind":"workflow","id":"active-task-continuation"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-completion","exit":"evidence_pending","consumer":{"kind":"skill","id":"guru-review-task-completion"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-completion","exit":"additional_delivery_required","consumer":{"kind":"workflow","id":"task-delivery-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-completion","exit":"requirements_revision_required","consumer":{"kind":"workflow","id":"task-requirements-revision-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-completion","exit":"implementation_revision_required","consumer":{"kind":"workflow","id":"guru-resume-implementation"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-completion","exit":"completed","consumer":{"kind":"skill","id":"guru-complete-task-closure"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-completion","exit":"blocked","consumer":{"kind":"stop","id":"task-completion-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-complete-task-closure","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-complete-task-closure","exit":"no_mutation","consumer":{"kind":"skill","id":"guru-finish-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-complete-task-closure","exit":"closed","consumer":{"kind":"skill","id":"guru-finish-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-complete-task-closure","exit":"resume_closure","consumer":{"kind":"skill","id":"guru-complete-task-closure"}} -->
<!-- guru-skill-exit: {"skill":"guru-complete-task-closure","exit":"external_change_conflict","consumer":{"kind":"skill","id":"guru-complete-task-closure"}} -->
<!-- guru-skill-exit: {"skill":"guru-complete-task-closure","exit":"blocked","consumer":{"kind":"stop","id":"task-closure-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-finish-task","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-finish-task","exit":"success","consumer":{"kind":"skill","id":"guru-cleanup-task-resources"}} -->
<!-- guru-skill-exit: {"skill":"guru-finish-task","exit":"resume_finish","consumer":{"kind":"skill","id":"guru-finish-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-finish-task","exit":"blocked","consumer":{"kind":"stop","id":"task-finish-blocked"}} -->
<!-- guru-skill-exit: {"skill":"guru-finish-task","exit":"closure_refresh_required","consumer":{"kind":"workflow","id":"task-closure-refresh-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-finish-task","exit":"manual_cleanup_required","consumer":{"kind":"skill","id":"guru-cleanup-task-resources"}} -->
<!-- guru-skill-invoke: {"skill":"guru-cleanup-task-resources","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-cleanup-task-resources","exit":"cleaned","consumer":{"kind":"stop","id":"task-cleanup-complete"}} -->
<!-- guru-skill-exit: {"skill":"guru-cleanup-task-resources","exit":"remaining_resources","consumer":{"kind":"skill","id":"guru-cleanup-task-resources"}} -->
<!-- guru-skill-exit: {"skill":"guru-cleanup-task-resources","exit":"blocked","consumer":{"kind":"stop","id":"task-cleanup-blocked"}} -->
<!-- guru-skill-exit: {"skill":"guru-cleanup-task-resources","exit":"manual_cleanup_required","consumer":{"kind":"skill","id":"guru-cleanup-task-resources"}} -->
<!-- guru-skill-exit: {"skill":"guru-cleanup-task-resources","exit":"handoff_cleanup_complete","consumer":{"kind":"stop","id":"task-handoff-cleanup-await-destination"}} -->
<!-- guru-skill-exit: {"skill":"guru-cleanup-task-resources","exit":"handoff_cleanup_remaining","consumer":{"kind":"skill","id":"guru-cleanup-task-resources"}} -->
<!-- guru-skill-invoke: {"skill":"guru-reactivate-task","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-reactivate-task","exit":"reactivated_to_planning","consumer":{"kind":"workflow","id":"task-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-reactivate-task","exit":"session_binding_recovery_required","consumer":{"kind":"workflow","id":"task-session-recovery-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-reactivate-task","exit":"resume_reactivation","consumer":{"kind":"workflow","id":"task-reactivation-resume-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-reactivate-task","exit":"reactivate_blocked","consumer":{"kind":"stop","id":"task-reactivate-blocked"}} -->
<!-- guru-skill-exit: {"skill":"guru-activate-delivery","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-delivery","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-delivery","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"legacy_controls_retired","consumer":{"kind":"workflow","id":"legacy-maintenance-publish-task-delivery-legacy-controls-retired"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"verified_legacy_history","consumer":{"kind":"workflow","id":"legacy-maintenance-publish-task-delivery-verified-legacy-history"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"unverified_legacy_history","consumer":{"kind":"workflow","id":"legacy-maintenance-publish-task-delivery-unverified-legacy-history"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-delivery","exit":"legacy_controls_retired","consumer":{"kind":"workflow","id":"legacy-maintenance-merge-task-delivery-legacy-controls-retired"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-delivery","exit":"verified_legacy_history","consumer":{"kind":"workflow","id":"legacy-maintenance-merge-task-delivery-verified-legacy-history"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-delivery","exit":"unverified_legacy_history","consumer":{"kind":"workflow","id":"legacy-maintenance-merge-task-delivery-unverified-legacy-history"}} -->
<!-- guru-skill-exit: {"skill":"guru-finish-task","exit":"legacy_controls_retired","consumer":{"kind":"workflow","id":"legacy-maintenance-finish-task-legacy-controls-retired"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"legacy_controls_retired","consumer":{"kind":"workflow","id":"legacy-maintenance-approve-task-plan-legacy-controls-retired"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"legacy_controls_retired","consumer":{"kind":"workflow","id":"legacy-maintenance-review-branch-legacy-controls-retired"}} -->

## Workflow and stop consumers

### guru-bootstrap-repository-ssot-completed-router

<!-- guru-workflow-target: {"id":"guru-bootstrap-repository-ssot-completed-router"} -->

Consume the original Bootstrap result through the [mandatory Architecture stage routing](#mandatory-architecture-stage-routing), retaining the original caller and stage. The original Bootstrap/Architecture contracts own the matching input and next invocation; a Bootstrap result is not a later-stage impact pass.

### guru-bootstrap-repository-ssot-baseline-incomplete-router

<!-- guru-workflow-target: {"id":"guru-bootstrap-repository-ssot-baseline-incomplete-router"} -->

Return the declared missing authority to original Bootstrap/bounded repair under [mandatory Architecture stage routing](#mandatory-architecture-stage-routing). Resume only the original purpose and stage after fresh impact; incomplete authority cannot continue as current.

### guru-bootstrap-repository-ssot-blocked

<!-- guru-stop-target: {"id":"guru-bootstrap-repository-ssot-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### guru-architecture-baseline-current-router

<!-- guru-workflow-target: {"id":"guru-architecture-baseline-current-router"} -->

Validate actual authority and source_profile. Planning candidate_assessment projects only the actual assessment/key to Author delivery_solution_planning; final_plan projects the actual final assessment directly to adjacent Approval. Precommit promotion returns through the original Architecture owner for actual-write/readback applicability, then original TaskCommit preparation. integrated_pending_review never enters readiness. The same new independent committed reviewer consumes matching branch_review assessment and completes original Review. Publication/Completion eligibility still requires no_change or reviewed_promoted. Bootstrap/repair retains original purpose/stage and exact recovery owner.

### guru-architecture-baseline-sync-router

<!-- guru-workflow-target: {"id":"guru-architecture-baseline-sync-router"} -->

Invoke original Architecture maintenance for the declared sync_kind/target. Preserve explicit DeliveryKey/planning_root where the selected Interface supports them. Retain planning purpose in this call-local route and rerun that purpose's task impact afterwards. For final_integration promotion-origin bootstrap/repair, retain the original promotion profile/key/root/stage call-locally and project maintenance to its existing phase2 stage; maintenance current returns only to that original promotion for reread and candidate rebinding, never as promoted success. No new assessment owner, checkpoint or lifecycle stage.

### guru-architecture-baseline-bootstrap-router

<!-- guru-workflow-target: {"id":"guru-architecture-baseline-bootstrap-router"} -->

Enter original foundation bootstrap or bounded repair for missing authority. Final-integration promotion origins use the same call-local maintenance phase2 projection and return to the original promotion as the sync-router; other origins retain planning_purpose and rerun the original task impact. Maintenance current is neither a planning 3.0 result nor promoted success.

### guru-architecture-baseline-planning-router

<!-- guru-workflow-target: {"id":"guru-architecture-baseline-planning-router"} -->

For planning conflict/contract gap, project planning_purpose and concrete conflict/missing refs to Author architecture_conflict_resolution. Actual scope choice uses Clarify. Nonplanning repair keeps its original owner; never reinterpret these exits as current.

### guru-architecture-baseline-check-router

<!-- guru-workflow-target: {"id":"guru-architecture-baseline-check-router"} -->

Return `fitness_regression` to implementation/check and require the affected downstream stages again.

### architecture-baseline-blocked

<!-- guru-stop-target: {"id":"architecture-baseline-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### guru-requirements-design-test-ssot-current-router

<!-- guru-workflow-target: {"id":"guru-requirements-design-test-ssot-current-router"} -->

candidate_ready retains complete isolated contribution and actual authority for original promotion after engineering preparation; it is not independent success. Invoke original RDT promotion at final_integration for actual changes. ssot_current resumes its caller with real integration/readback facts; complete necessary Architecture integration, then original TaskCommit. This route creates no candidate Check or public pass. The next original owner rereads applicable complete bodies.

### guru-requirements-design-test-ssot-planning-router

<!-- guru-workflow-target: {"id":"guru-requirements-design-test-ssot-planning-router"} -->

Return the exact affected scope and revision code to the current planning or implementation owner.

### guru-requirements-design-test-ssot-bootstrap-router

<!-- guru-workflow-target: {"id":"guru-requirements-design-test-ssot-bootstrap-router"} -->

Enter controlled foundation bootstrap or repair for the declared missing layer without expanding business scope.

### requirements-design-test-ssot-blocked

<!-- guru-stop-target: {"id":"requirements-design-test-ssot-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### delivery-activation-blocked

<!-- guru-stop-target: {"id":"delivery-activation-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### invalid-task-state

<!-- guru-stop-target: {"id":"invalid-task-state"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### invalid-delivery-state

<!-- guru-stop-target: {"id":"invalid-delivery-state"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### delivery-creation-blocked

<!-- guru-stop-target: {"id":"delivery-creation-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### guru-delivery-started-router

<!-- guru-workflow-target: {"id":"guru-delivery-started-router"} -->

Consume the actual public Planning result for same-Delivery implementation.

### guru-delivery-scope-revised-router

<!-- guru-workflow-target: {"id":"guru-delivery-scope-revised-router"} -->

Select mode/task_ref/delivery_key/source_selection/revision_refs unchanged from delivery_scope_revised; add fixed profile=delivery_active_task_scope_change; explicitly invoke guru-author-task-plan. This is same-slice rework, never a Planning approval.

### guru-delivery-planning-author-router

<!-- guru-workflow-target: {"id":"guru-delivery-planning-author-router"} -->

Consume Creation/Selection's unchanged created DTO through the explicit receiving-session continuation before entering Author or another stage owner. That continuation checks the receiving caller's own Task/Delivery facts and rereads this exact public key, phase, scope and planning_root. Only a current planning Delivery with an actual initial-requirements obligation and matching Author entry projects task_ref/delivery_key plus adjacent source_selection and mode to delivery_initial_review; lost source selection returns to original Clarify. All other objects, including planning with existing work/gates, enter the sole Bound formal Task / Delivery continuation at their actual outstanding obligation and original owner. Existing planning resumes applicable Author/Wording/Architecture/Approval or current approved to Activation, preserving identity, plans and applicable results; missing/stale outputs return to their producer. created does not imply a new object, planning phase or gate pass; this consumer writes no phase/cache and never resets it.

### guru-delivery-selection-router

<!-- guru-workflow-target: {"id":"guru-delivery-selection-router"} -->

Read the exact TaskKey inventory for a real selection; obtain an explicit DeliveryKey before invoking Creation selection. Never infer identity from a sole inventory row.

### guru-delivery-activation-planning-router

<!-- guru-workflow-target: {"id":"guru-delivery-activation-planning-router"} -->

Return the selected Delivery to its current Planning owner, refresh affected evidence, then invoke Delivery Approval.

### original-request-route

<!-- guru-workflow-target: {"id":"original-request-route"} -->

Return to the original non-repository request.

### guru-workflow-standard-intake-router

<!-- guru-workflow-target: {"id":"guru-workflow-standard-intake-router"} -->

Enter the existing mandatory `guru-sync-base` route without requiring a pre-existing Issue.

### guru-normal-scenario-classified-router

<!-- guru-workflow-target: {"id":"guru-normal-scenario-classified-router"} -->

Validate the profile binding and return the current invocation-local classifications to the exact original owner.

### guru-normal-scenario-mechanism-router

<!-- guru-workflow-target: {"id":"guru-normal-scenario-mechanism-router"} -->

Validate the profile binding and return to the exact original owner for remove/replace, then refresh affected original-owner judgments before further stage judgment.

### guru-solution-mechanism-classified-router

<!-- guru-workflow-target: {"id":"guru-solution-mechanism-classified-router"} -->

Validate the profile binding and return the actual invocation-local classifications to the exact original owner in [Mandatory qualification profiles](#mandatory-qualification-profiles). Each stage still performs its own complete current judgment.

### guru-solution-mechanism-mechanism-router

<!-- guru-workflow-target: {"id":"guru-solution-mechanism-mechanism-router"} -->

Validate the profile binding and return to the exact original owner for remove/replace under [Mandatory qualification profiles](#mandatory-qualification-profiles). Refresh affected original-owner judgments before continuing. This result never becomes scope confirmation.

### guru-root-cause-classified-router

<!-- guru-workflow-target: {"id":"guru-root-cause-classified-router"} -->

Consume the original closed result and select the existing owner by profile under [Root-cause qualification routing](#root-cause-qualification-routing). Candidate dispositions return to that owner; they do not establish repair or completion.

### guru-root-cause-mechanism-router

<!-- guru-workflow-target: {"id":"guru-root-cause-mechanism-router"} -->

Consume the original closed result under [Root-cause qualification routing](#root-cause-qualification-routing). Return candidate refs/reasons to the existing profile owner for remove/replace and complete-set re-entry.

### guru-root-cause-diagnosis-router

<!-- guru-workflow-target: {"id":"guru-root-cause-diagnosis-router"} -->

Consume the original closed result under [Root-cause qualification routing](#root-cause-qualification-routing). Return paused repair refs/gaps to the existing profile owner for bounded investigation and resubmission.

### guru-task-free-completed

<!-- guru-workflow-target: {"id":"guru-task-free-completed"} -->

Report the checked bounded-change edited paths, concise validation results, and explicit unverified boundaries without creating lifecycle or publication resources.

### guru-task-free-resume-active-task-router

<!-- guru-workflow-target: {"id":"guru-task-free-resume-active-task-router"} -->

Resume the exact active task from its current status route.

### guru-task-free-scope-change-router

<!-- guru-workflow-target: {"id":"guru-task-free-scope-change-router"} -->

Enter the existing Scope Change Gate through `guru-clarify-requirements`.

### guru-requirements-clear-router

<!-- guru-workflow-target: {"id":"guru-requirements-clear-router"} -->

Validate the selected scope_ready 2.0 closed shape. Pre-publication scope_ready without task_key projects mode/task_ref/source_selection/revision_refs into Author task_scope_requirements. Post-publication scope_ready with task_key consumes actual accepted scope and routes by current obligations to explicit Creation, affected Delivery rework/withdrawal, or Completion; it never repeats scope writing or creates an empty Delivery. For clear, resume the declared initial Intake, non-current interrupted phase or standalone caller.

### guru-full-task-intake-chain

<!-- guru-workflow-target: {"id":"guru-full-task-intake-chain"} -->

Start a separately reviewed task intake from the returned draft.

### guru-contract-wording-pass-router

<!-- guru-workflow-target: {"id":"guru-contract-wording-pass-router"} -->

change_request still enters original change-request review. delivery_planning_artifacts enters Architecture delivery_task_impact_sync final_plan on the actual current Delivery design, then adjacent Approval. Standalone follows its matching original caller.

### guru-contract-wording-change-router

<!-- guru-workflow-target: {"id":"guru-contract-wording-change-router"} -->

Delivery planning content_changed copies public task_ref/delivery_key/change_refs unchanged to Author input, adding only profile=delivery_wording_reentry and mode=workflow; never read private Wording revisions. Author re-enters the earliest affected dependency. Other profiles retain their original affected wording/upstream refresh.

### guru-task-intake-router

<!-- guru-workflow-target: {"id":"guru-task-intake-router"} -->

Project `ready.transition.target.kind` exactly once: `proposed_draft` invokes `guru-create-issue`, while `existing_issue` and `standalone_request` invoke `guru-create-task`; never turn an Issue creation result into task creation without fresh Sync and Intake.

### guru-sync-base

<!-- guru-workflow-target: {"id":"guru-sync-base"} -->

Re-enter `guru-sync-base` and then fresh Intake. `guru-create-issue:created` supplies the newly created exact source Issue and continues as a live Issue, never as a draft/Issue binding; `guru-create-issue:refresh_review` has no created Issue and retains the proposed draft for renewed review. `guru-create-task:refresh_review` retains its existing reviewed source route. No task creation is implied by this target.

### guru-task-created

<!-- guru-workflow-target: {"id":"guru-task-created"} -->

Resolve live TaskId/generation and checkout, then check the receiving session's own binding through the explicit receiving-session continuation. Retain adjacent source_selection/revision_refs and invoke Author task_scope_requirements only after that Task entry is satisfied; no Delivery is needed for root requirements. Missing source selection re-enters original Clarify/context; metadata/files do not reconstruct it.

### guru-current-task-identity-router

<!-- guru-workflow-target: {"id":"guru-current-task-identity-router"} -->

Resume the current task owner only after exact TaskId, generation and source authority validation.

### guru-task-source-review-router

<!-- guru-workflow-target: {"id":"guru-task-source-review-router"} -->

Return ambiguous legacy source to fresh semantic review; do not guess Issue disposition from branch or PR text.

### guru-task-branch-established-router

<!-- guru-workflow-target: {"id":"guru-task-branch-established-router"} -->

Re-resolve the active checkout with the established branch binding.

### guru-task-branch-selection-router

<!-- guru-workflow-target: {"id":"guru-task-branch-selection-router"} -->

Present current candidates for explicit choice, then revalidate through the binding owner.

### guru-current-task-checkout-router

<!-- guru-workflow-target: {"id":"guru-current-task-checkout-router"} -->

Resume the exact current lifecycle owner with the live resolved checkout.

### guru-task-branch-binding-router

<!-- guru-workflow-target: {"id":"guru-task-branch-binding-router"} -->

Invoke `guru-establish-task-branch-binding` for the exact active task.

### guru-task-checkout-acquisition-router

<!-- guru-workflow-target: {"id":"guru-task-checkout-acquisition-router"} -->

Acquire the reviewed checkout through its task owner and re-resolve the same TaskId.

### guru-task-branch-rebound-router

<!-- guru-workflow-target: {"id":"guru-task-branch-rebound-router"} -->

Re-resolve the task checkout at the new binding revision; do not carry an old session receipt.

### guru-task-branch-rebind-refresh-router

<!-- guru-workflow-target: {"id":"guru-task-branch-rebind-refresh-router"} -->

Return to the rebind owner's fresh target review.

### guru-bind-task-session-resume-router

<!-- guru-workflow-target: {"id":"guru-bind-task-session-resume-router"} -->

Resume the exact TaskId/generation current phase after session validation.

### guru-bind-task-session-rebind-router

<!-- guru-workflow-target: {"id":"guru-bind-task-session-rebind-router"} -->

Resume the exact task after current session binding recovery and phase revalidation.

### guru-bind-task-session-switch-router

<!-- guru-workflow-target: {"id":"guru-bind-task-session-switch-router"} -->

Switch only to the explicitly selected TaskId/generation and freshly resolve its phase.

### guru-bind-task-session-reactivate-router

<!-- guru-workflow-target: {"id":"guru-bind-task-session-reactivate-router"} -->

Resume the reactivated generation; old Finish/Cleanup receipts remain historical.

### guru-bind-task-session-manual-recovery-router

<!-- guru-workflow-target: {"id":"guru-bind-task-session-manual-recovery-router"} -->

Recheck the restored binding and current task boundary before phase routing.

### guru-current-phase-router

<!-- guru-workflow-target: {"id":"guru-current-phase-router"} -->

Use current C3/C4/C5-resolved Task identity or explicit task mode, then the sole public Delivery continuation. Planning resumes the actual outstanding obligation in the sole continuation: only initial slice requirements enter Author delivery_initial_review with fresh original source selection. Existing planning resumes its applicable Author/Wording/Architecture/Approval owner, or current approved goes to Activation; missing/stale outputs re-enter their original producer, never reset planning from phase alone. No-current Delivery follows actual scope/Creation/Completion/closeout needs. Missing selection returns to its original producer. No Task status or recovered creation DTO supplies a phase.

### guru-task-plan-clarify-scope-router

<!-- guru-workflow-target: {"id":"guru-task-plan-clarify-scope-router"} -->

Enter the Scope Change Gate through guru-clarify-requirements.

### phase-1-delivery-activation

<!-- guru-workflow-target: {"id":"phase-1-delivery-activation"} -->

Present the current Delivery approved plan, then invoke `guru-activate-delivery` after its dialogue boundary.

### guru-base-reconciliation-router

<!-- guru-workflow-target: {"id":"guru-base-reconciliation-router"} -->

Consume the fixed integration result and resume its closed target through the original candidate/Check/Review applicability owners.

### guru-base-continuity-passed-router

<!-- guru-workflow-target: {"id":"guru-base-continuity-passed-router"} -->

Return the bounded result to the original Check/Branch Review applicability owners; only their real current candidate-bound results resume the closed target. Continuity is not a full Review gate.

### guru-pre-review-commit-router

<!-- guru-workflow-target: {"id":"guru-pre-review-commit-router"} -->

Consume original TaskCommit pre_review_committed task_ref/key/branch_review_commit. Original implementation constructor reads the same Delivery fixed B and complete actual committed H, then invokes public begin_check. Project unchanged Candidate base/head and exact TaskRef/key into original Review delivery_branch_review current input; author only mode and actual review_intent. Do not hand-fill content_ref, add a commit, push or synthesize Check. Missing/changed facts return to original implementation/commit owner.

### guru-draft-feedback-router

<!-- guru-workflow-target: {"id":"guru-draft-feedback-router"} -->

This is an original existing Draft recovery fact under MIGRATION-794. Preserve exact PR/HEAD and report recovered already-executed effects. Resume current implementation or committed review obligations from actual public state. No early content-review or new push/PR is triggered; Draft supplies no pass.

### guru-draft-revision-router

<!-- guru-workflow-target: {"id":"guru-draft-revision-router"} -->

Consume original return-to-Draft result and resume the same Delivery through lawful implementation rework. Preserve real PR and completed effects. Engineering work, necessary integration and a successor local commit precede current independent review and Delivery Review readiness before any new push.

### guru-resume-implementation

<!-- guru-workflow-target: {"id":"guru-resume-implementation"} -->

Resume Phase 2 through the original owner's lawful nonterminal Delivery continuation. For a Completion TaskRef/TaskKey return, read that Task's public current continuation and project its actual selected DeliveryKey and planning_root before dispatch. Missing, terminal or mismatched selection returns to Completion for a fresh route; this router neither creates nor reopens a Delivery.

### guru-task-base-planning-router

<!-- guru-workflow-target: {"id":"guru-task-base-planning-router"} -->

Return exact planning impact and DeliveryKey to Author delivery_active_task_scope_change after necessary original Clarify; preserve task/base identity and re-enter affected dependencies.

### guru-task-base-scope-router

<!-- guru-workflow-target: {"id":"guru-task-base-scope-router"} -->

Enter the Scope Change Gate for the exact authority choice.

### guru-task-check-planning-router

<!-- guru-workflow-target: {"id":"guru-task-check-planning-router"} -->

For current Review planning_stale/reapprove_plan, project only task_ref/delivery_key/revision_actions to original Author delivery_approval_revision with current mode. clarify_requirements passes actual proposal_refs to original Clarify. An already executed rollback is recovered by its same original Review owner before this handoff; never repeat rework or restore cleared Planning. Explicit old Check rollback recovery retains its original result and supported 1.0 projection under MIGRATION-794; this router consumes that actual completed handoff without invoking development Check.

### guru-delivery-resolved-reconciliation-router

This is an explicit standalone/recovery reference, outside the active marker graph.

Resolved Git integration belongs to original Reconcile and exact local commit owners. Retain actual committed_candidate_anchor, fixed B and complete integration facts. After legal rework, original implementation binds actual committed H through constructor/begin_check; current Review covers Task/base attribution, conflict resolution and affected consumers. No resolved Check producer or precommit pass is created.

### guru-branch-review-implementation-router

<!-- guru-workflow-target: {"id":"guru-branch-review-implementation-router"} -->

Resume Phase 2, then repeat the downstream graph.

### guru-branch-review-scope-router

<!-- guru-workflow-target: {"id":"guru-branch-review-scope-router"} -->

Enter the Scope Change Gate, then repeat affected phases.

### guru-task-delivery-planning-router

<!-- guru-workflow-target: {"id":"guru-task-delivery-planning-router"} -->

Copy Delivery Review planning_revision_required task_ref/delivery_key unchanged and rename reason_refs to revision_refs for `guru-author-task-plan:delivery_delivery_plan_revision`, adding current mode and revision_reason=delivery_policy_gap. Consume the Review owner's actual same-Delivery planning rework; preserve total accepted scope.

### guru-task-delivery-scope-router

<!-- guru-workflow-target: {"id":"guru-task-delivery-scope-router"} -->

Enter fresh requirements clarification for the exact disputed slice.

### active-task-continuation

<!-- guru-workflow-target: {"id":"active-task-continuation"} -->

Keep the task active and resume the earliest affected work owner for remaining work.

### task-delivery-planning-router

<!-- guru-workflow-target: {"id":"task-delivery-planning-router"} -->

Consume Completion additional_delivery_required's actual task_ref/task_key as the seed for `guru-create-delivery:delivery_creation`; reason stays call-local scope context, not an extra public input field. Creation owns the remaining declared scope_ref/delivery_profile/continuation_id/action inputs, slice judgment and necessary choice/side-effect handling. Only its actual created result enters guru-delivery-planning-author-router for a fresh public phase read; a new planning slice proceeds to Author delivery_initial_review with original current source_selection, while a recovered progressed slice returns to its actual continuation owner. Missing source selection returns to original Clarify. Preserve the same TaskId/generation and total accepted scope; no old Delivery planning rewrite or Task-root creation inference.

### task-requirements-revision-router

<!-- guru-workflow-target: {"id":"task-requirements-revision-router"} -->

Consume Completion requirements_revision_required's actual task_ref/task_key/reason in original `guru-clarify-requirements:delivery_task_scope_revision`, with source_exit=requirements_revision_required and current mode/target_locator/resume_target/continuation_id; reason is call-local authority context. Follow actual scope_ready through guru-requirements-clear-router to Author task_scope_requirements, then scope_requirements_ready through guru-task-scope-requirements-ready-router to Clarify task_scope_requirements_acceptance. Only the published scope_ready returns to the clear-router for affected same-Delivery rework/withdrawal, explicit new Creation, or Completion without a Delivery, according to current obligations. Do not preselect old requirements_revision or create an empty slice.

### task-closure-refresh-router

<!-- guru-workflow-target: {"id":"task-closure-refresh-router"} -->

Refresh the exact source Issue closure fact before resuming Finish.

### task-planning-router

<!-- guru-workflow-target: {"id":"task-planning-router"} -->

Resolve the reactivated generation's current Task scope and fresh original source route. Required scope revision enters Author task_scope_requirements and original Clarify publication; unchanged scope routes to actual validation/Completion or explicit new Delivery Creation. Prior-generation approvals are not reused.

### task-session-recovery-router

<!-- guru-workflow-target: {"id":"task-session-recovery-router"} -->

Resolve the actual current key/ref; invoke original `guru-establish-task-branch-binding`, then `guru-ensure-task-checkout`, then `guru-bind-task-session`. Preserve already valid controls and establish only missing current-environment facts.

### task-reactivation-resume-router

<!-- guru-workflow-target: {"id":"task-reactivation-resume-router"} -->

Re-enter the same Reactivate owner with transaction_id/result_id. For shared-archive pending output, generation identifies the frozen plan's target only; it proves no active Task and must not enter Planning/Bind. Recover the same public operation and route its actual applied key/ref.

### workflow-mode-selection-blocked

<!-- guru-stop-target: {"id":"workflow-mode-selection-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### normal-scenario-qualification-blocked

<!-- guru-stop-target: {"id":"normal-scenario-qualification-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### solution-mechanism-qualification-blocked

<!-- guru-stop-target: {"id":"solution-mechanism-qualification-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### root-cause-qualification-blocked

<!-- guru-stop-target: {"id":"root-cause-qualification-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-free-change-blocked

<!-- guru-stop-target: {"id":"task-free-change-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### base-sync-blocked

<!-- guru-stop-target: {"id":"base-sync-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### change-context-blocked

<!-- guru-stop-target: {"id":"change-context-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### requirements-clarification-blocked

<!-- guru-stop-target: {"id":"requirements-clarification-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### contract-wording-blocked

<!-- guru-stop-target: {"id":"contract-wording-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### change-request-review-blocked

<!-- guru-stop-target: {"id":"change-request-review-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### issue-creation-blocked

<!-- guru-stop-target: {"id":"issue-creation-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-creation-blocked

<!-- guru-stop-target: {"id":"task-creation-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-identity-blocked

<!-- guru-stop-target: {"id":"task-identity-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-branch-binding-blocked

<!-- guru-stop-target: {"id":"task-branch-binding-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-branch-rebind-blocked

<!-- guru-stop-target: {"id":"task-branch-rebind-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-session-binding-blocked

<!-- guru-stop-target: {"id":"task-session-binding-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-plan-approval-blocked

<!-- guru-stop-target: {"id":"task-plan-approval-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-base-reconciliation-blocked

<!-- guru-stop-target: {"id":"task-base-reconciliation-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-check-blocked

This is an explicit standalone/recovery reference, outside the active marker graph.

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-commit-blocked

<!-- guru-stop-target: {"id":"task-commit-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### branch-review-blocked

<!-- guru-stop-target: {"id":"branch-review-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-delivery-review-blocked

<!-- guru-stop-target: {"id":"task-delivery-review-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-delivery-publication-blocked

<!-- guru-stop-target: {"id":"task-delivery-publication-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-delivery-merge-blocked

<!-- guru-stop-target: {"id":"task-delivery-merge-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-completion-blocked

<!-- guru-stop-target: {"id":"task-completion-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-closure-blocked

<!-- guru-stop-target: {"id":"task-closure-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-finish-blocked

<!-- guru-stop-target: {"id":"task-finish-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-cleanup-complete

<!-- guru-stop-target: {"id":"task-cleanup-complete"} -->

Report the original Cleanup result and its verified resource outcome. This is a terminal response, not another automatic lifecycle route.

### task-cleanup-blocked

<!-- guru-stop-target: {"id":"task-cleanup-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### task-handoff-cleanup-await-destination

<!-- guru-stop-target: {"id":"task-handoff-cleanup-await-destination"} -->

Report the original machine-handoff cleanup result and wait for the declared destination completion. Do not infer cleanup or execute another resource mutation.

### task-reactivate-blocked

<!-- guru-stop-target: {"id":"task-reactivate-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### legacy-archived-review-disposition-required

<!-- guru-stop-target: {"id":"legacy-archived-review-disposition-required"} -->

Stop at the selected old archive/Finalizer disposition. Load [archived review and Finalizer](legacy.md#archived-review-and-finalizer); preserve exact task/PR facts and the pinned-old or per-case manual route. No current lifecycle pass is inferred.

### guru-task-plan-requirements-ready-router

<!-- guru-workflow-target: {"id":"guru-task-plan-requirements-ready-router"} -->

Thin-project Author task_ref/delivery_key/candidate into original Architecture delivery_task_impact_sync candidate_assessment; obtain only its fresh authority/route fields from live facts. Never manufacture an impact conclusion or invent a DeliveryKey/planning_root.

### guru-task-scope-requirements-ready-router

<!-- guru-workflow-target: {"id":"guru-task-scope-requirements-ready-router"} -->

Project actual Author task_ref/requirements_locator into original Clarify task_scope_requirements_acceptance; add current mode and the adjacent source_selection/revision_refs. Lost source selection re-enters original Clarify; neither metadata nor root PRD reconstructs it.

### guru-task-plan-ready-router

<!-- guru-workflow-target: {"id":"guru-task-plan-ready-router"} -->

Project task_ref/delivery_key to Wording delivery_planning_artifacts and resolve its current three docs; invoke the original Wording owner.

### guru-task-plan-approval-revision-router

<!-- guru-workflow-target: {"id":"guru-task-plan-approval-revision-router"} -->

Project task_ref/delivery_key and actual revision_actions to Author delivery_approval_revision, with current mode; no Approval self-writing edge remains.

### task-plan-author-blocked

<!-- guru-stop-target: {"id":"task-plan-author-blocked"} -->

Return the owning Skill result and safe remediation, then stop this automatic chain until authority or external state changes. Do not guess another route or expose package-private state. An independently requested operation retains the Manual Git/GitHub Operations entry in the workflow.

### legacy-maintenance-publish-task-delivery-legacy-controls-retired

<!-- guru-workflow-target: {"id":"legacy-maintenance-publish-task-delivery-legacy-controls-retired"} -->

Return only to the explicitly selected original legacy maintenance call. Load [selected maintenance owner exits](legacy.md#selected-maintenance-owner-exits); preserve its exact controls-retired/history disposition. Never enter ordinary publication, merge, Completion or Finish from this result.

### legacy-maintenance-publish-task-delivery-verified-legacy-history

<!-- guru-workflow-target: {"id":"legacy-maintenance-publish-task-delivery-verified-legacy-history"} -->

Return only to the explicitly selected original legacy maintenance call. Load [selected maintenance owner exits](legacy.md#selected-maintenance-owner-exits); preserve its exact controls-retired/history disposition. Never enter ordinary publication, merge, Completion or Finish from this result.

### legacy-maintenance-publish-task-delivery-unverified-legacy-history

<!-- guru-workflow-target: {"id":"legacy-maintenance-publish-task-delivery-unverified-legacy-history"} -->

Return only to the explicitly selected original legacy maintenance call. Load [selected maintenance owner exits](legacy.md#selected-maintenance-owner-exits); preserve its exact controls-retired/history disposition. Never enter ordinary publication, merge, Completion or Finish from this result.

### legacy-maintenance-merge-task-delivery-legacy-controls-retired

<!-- guru-workflow-target: {"id":"legacy-maintenance-merge-task-delivery-legacy-controls-retired"} -->

Return only to the explicitly selected original legacy maintenance call. Load [selected maintenance owner exits](legacy.md#selected-maintenance-owner-exits); preserve its exact controls-retired/history disposition. Never enter ordinary publication, merge, Completion or Finish from this result.

### legacy-maintenance-merge-task-delivery-verified-legacy-history

<!-- guru-workflow-target: {"id":"legacy-maintenance-merge-task-delivery-verified-legacy-history"} -->

Return only to the explicitly selected original legacy maintenance call. Load [selected maintenance owner exits](legacy.md#selected-maintenance-owner-exits); preserve its exact controls-retired/history disposition. Never enter ordinary publication, merge, Completion or Finish from this result.

### legacy-maintenance-merge-task-delivery-unverified-legacy-history

<!-- guru-workflow-target: {"id":"legacy-maintenance-merge-task-delivery-unverified-legacy-history"} -->

Return only to the explicitly selected original legacy maintenance call. Load [selected maintenance owner exits](legacy.md#selected-maintenance-owner-exits); preserve its exact controls-retired/history disposition. Never enter ordinary publication, merge, Completion or Finish from this result.

### legacy-maintenance-finish-task-legacy-controls-retired

<!-- guru-workflow-target: {"id":"legacy-maintenance-finish-task-legacy-controls-retired"} -->

Return only to the explicitly selected original legacy maintenance call. Load [selected maintenance owner exits](legacy.md#selected-maintenance-owner-exits); preserve its exact controls-retired/history disposition. Never enter ordinary publication, merge, Completion or Finish from this result.

### legacy-maintenance-approve-task-plan-legacy-controls-retired

<!-- guru-workflow-target: {"id":"legacy-maintenance-approve-task-plan-legacy-controls-retired"} -->

Return only to the explicitly selected original legacy maintenance call. Load [selected maintenance owner exits](legacy.md#selected-maintenance-owner-exits); preserve its exact controls-retired/history disposition. Never enter ordinary publication, merge, Completion or Finish from this result.

### legacy-maintenance-check-task-legacy-controls-retired

This is an explicit standalone/recovery reference, outside the active marker graph.

Return only to the explicitly selected original legacy maintenance call. Load [selected maintenance owner exits](legacy.md#selected-maintenance-owner-exits); preserve its exact controls-retired/history disposition. Never enter ordinary publication, merge, Completion or Finish from this result.

### legacy-maintenance-review-branch-legacy-controls-retired

<!-- guru-workflow-target: {"id":"legacy-maintenance-review-branch-legacy-controls-retired"} -->

Return only to the explicitly selected original legacy maintenance call. Load [selected maintenance owner exits](legacy.md#selected-maintenance-owner-exits); preserve its exact controls-retired/history disposition. Never enter ordinary publication, merge, Completion or Finish from this result.

## Shared publication and stop boundaries

`guru-publish-task-delivery` owns the current PR and its output-loss recovery;
`guru-merge-task-delivery` owns one expected-head merge and emits only a Delivery
result. A materially stale review returns to its original owner; actual integration blockers enter
Reconcile/continuity, and task-content findings return to their affected owner.
Neither PR state nor merge status is a Completion approval.

Every stop target returns the owning Skill result and safe remediation, then
waits for changed authority or external state. A stop never guesses another
route or exposes package-private state. This stops the automatic chain, not an
independently requested operation under Manual Git/GitHub Operations. Use the
repository-relative locator for the selected layout:
`trellis/workflows/guru-team/workflow.md#manual-gitgithub-operations` for source,
or `.trellis/workflow.md#manual-gitgithub-operations` for installed.


## Mandatory Architecture stage routing

For a selected old Finalizer/archive disposition, load [legacy maintenance boundaries](legacy.md#archived-review-and-finalizer).

Every standard task invokes the one stable
`guru-maintain-architecture-baseline` owner through `task_impact_sync` at each
applicable stage. The single mandatory invocation marker in this reference identifies the Skill; these
stage calls are fresh invocations, not duplicated markers or reusable results.
Executor selection and assessment/eligibility behavior belong solely to that
Skill's contract. Each assessment stage invokes its first independent or
independent-continuation entry as applicable; downstream stages invoke its
current eligibility entry and consume actual matching-stage output.
The caller never substitutes
self-authoring, a prior-stage DTO or an overall gate for that invocation.

| Stage | Required Architecture call | Only current resume target |
| --- | --- | --- |
| Planning candidate | `delivery_task_impact_sync(stage=planning, planning_purpose=candidate_assessment)` | `guru-author-task-plan:delivery_solution_planning` |
| Planning final | `delivery_task_impact_sync(stage=planning, planning_purpose=final_plan)` | Adjacent Delivery `guru-approve-task-plan` |
| Qualified implementation expansion | `delivery_task_impact_sync(stage=implementation_discovery)` | `guru-phase2-implementation-coordinator` |
| Precommit integration | Original `delivery_promotion(stage=final_integration)` for necessary complete changes after engineering preparation | Original TaskCommit; integrated_pending_review is not a pass |
| Committed Review | `delivery_task_impact_sync(stage=branch_review)` over fixed complete B..H under the same new independent reviewer | Original Review completes all Check/full_review duties once |
| Delivery Review | `delivery_task_impact_sync(stage=publication)` | `guru-review-task-delivery` |
| Completion/Finish | Actual Task `task_impact_sync(stage=acceptance_finish)` when no Delivery; selected Delivery uses `delivery_task_impact_sync` | `guru-review-task-completion` / `guru-finish-task` after Closure |

Every `baseline_current` carries `constitution_status=current` and its exact
source profile. Delivery rows resume only from
`source_profile=delivery_task_impact_sync` with the same DeliveryKey and planning
root; the Task-only acceptance/finish row uses `source_profile=task_impact_sync`.
`source_profile=delivery_bootstrap_foundation|delivery_repair` reruns
`delivery_task_impact_sync(stage=<affected-stage>)` with that same DeliveryKey and
planning root. Task-only `bootstrap_foundation|repair` reruns the matching
`task_impact_sync` call. For a final-integration promotion origin, both maintenance
profiles instead use the sync-router phase2 projection and return only to the
original promotion; `baseline_incomplete` uses that same bootstrap-router return. `source_profile=delivery_promotion|promotion` returns to
the original Architecture owner for actual-write applicability, then original
implementation prepares the exact local commit before committed review. The Architecture package owns when
changed facts require another assessment. A promotion alone does not replay
an earlier independent assessment or a completed full Review. A
missing result stops that stage. `baseline_incomplete` enters bootstrap/repair;
`architecture_conflict` or `contract_incomplete` returns to Planning/repair;
`fitness_regression` returns to implementation/check; and `blocked` stops.
A stale identity for the explicitly stage-applicable baseline, constitution,
contribution or candidate returns `sync_required` to the Architecture owner.
Unrelated overall CURRENT/version/ref advancement does not change that
applicability. `sync_required(sync_kind=promotion_required)` enters the original
promotion route at the precommit integration boundary. Its actual integrated
content enters TaskCommit and the committed Review. Only a real affected
dependency is reconsidered.
Promotion's own expected-current write mismatch remains local to promotion.

Delivery Review rejects missing or stale Architecture evidence, every conflict,
incomplete contract, fitness regression, and `promotion_state=reviewed_candidate`.
Completion/Finish accepts a long-term Architecture change only as
`reviewed_promoted`, or accepts a current `no_change` proof when shared current
does not change. Engineering preparation, TaskCommit and the single independent
committed full-diff Review include the promoted files. Completion/Finish does not promote
an already accepted contribution again. This router establishes Architecture
eligibility only; it does not absorb Delivery publication, whole-task Completion,
or post-Completion Closure/Finish judgments from their owning packages.

## Mandatory qualification profiles

At the candidate boundaries below, the original caller first reads each
qualifier's own short `references/applicability.md` from the complete matching
provider's `guru-qualify-normal-scenario`, `guru-qualify-solution-mechanism`, and
`guru-qualify-root-cause` packages. Installed paths are under
`.trellis/guru-team/skills/packages/`; canonical source paths are under
`trellis/skills/guru-team/packages/`. The caller judges those conditions
independently before loading any qualifier's full Skill or contract. Conditions
and complete qualification behavior remain step-local to those original owners.

When an owner's conditions require a current invocation, the workflow must
explicitly load that stable Skill and invoke its original semantic loop with the actual
applicable nonempty profile-specific candidate set and live locators. Adopt a
still-applicable conclusion when its owner conditions permit. If an owner does
not trigger, load no full body, assemble no input and emit no classified,
empty or skipped result for it. The original stage still performs its complete
current judgment. The workflow consumes the original declared exits only.

| Profile | Boundary for the caller's applicability judgment | Classified/mechanism return owner |
| --- | --- | --- |
| `task_free_pre_write` | task-free pre-write suitability or any target write | `guru-execute-task-free-change` |
| `task_free_evolution` | post-write scope/risk evolution judgment or further target write | `guru-execute-task-free-change` |
| `requirements_scope_set` | clarification scope proposal, scope question, or scope disposition | `guru-clarify-requirements` |
| `change_request_candidate_set` | change-request readiness finding, requested test, or blocker | `guru-review-change-request` |
| `author_candidate_set` | Author candidate before independent Architecture assessment | `guru-author-task-plan` |
| `planning_scenario_set` | planning acceptance, negative test, finding, or revision action | `guru-approve-task-plan` |
| `implementation_discovery` | Phase 2 edits or tests for a planning-external discovered candidate | `guru-phase2-implementation-coordinator` |
| `base_impact_candidate_set` | base-impact finding, validation obligation, or route | `guru-reconcile-task-base` |
| `phase2_candidate_set` | Explicit pinned-old Check recovery only; not the active development graph | Original supported Check provider |
| `branch_review_candidate_set` | Branch Review severity, finding, scope route, or blocker | `guru-review-branch` |
| `publication_candidate_set` | Delivery Review finding, task-work return, or blocker | `guru-review-task-delivery` |

For the seven Task/Delivery rows, each current invocation supplies the original
caller's complete `target.delivery_key` under input 2.0 / aggregate 3.0.
Explicit identity, Planning paths and caller-held continuation follow the
original normal qualifier's `references/contract.md#explicit-taskdelivery-target`.
The implementation coordinator reads that same contract before assembling
`implementation_discovery`; all callers keep their own current Task/key/profile
and purpose while consuming the unchanged output. This does not add a
qualification store or alter the pinned-old Check boundary.

For every row, the caller separately applies normal, solution and root
conditions. Normal's scenario admission does not replace solution's authority
placement or root's causal admission, and none replaces the stage judgment.
A triggered solution qualification that finds a forbidden mechanism returns
`mechanism_revision_required` and never enters scope confirmation. The
applicability judgment is not an OS/kernel/process/descriptor keyword filter.

`guru-qualify-normal-scenario:scope_confirmation_required` invokes
`guru-clarify-requirements:normal_scenario_scope_confirmation`, while
`guru-qualify-solution-mechanism:scope_confirmation_required` invokes
`guru-clarify-requirements:solution_mechanism_scope_confirmation`. Each
target-owned profile returns a real authority choice to the closed original
owner; material changes refresh affected judgments under the original owner's
conditions. Lost necessary conclusions return to their original owner for
recovery or fresh judgment. Stage/caller change alone does not repeat the same
qualification. Already rejected candidates never enter clarification. Unknown, empty, multiple,
mismatched, or unmapped normal-scenario results stop at
`normal-scenario-qualification-blocked`; the corresponding solution-mechanism
results stop at `solution-mechanism-qualification-blocked`.
For `implementation_discovery`, the semantic owner remains
`guru-phase2-implementation-coordinator`; its deterministic clarification resume
target is the existing `guru-resume-implementation` workflow API.


## Root-cause qualification routing

For each profile in the table, apply root's own short conditions independently.
When they require a current invocation, the caller must explicitly load
`guru-qualify-root-cause` for its actual eligible nonempty set. The caller first
completes current scenario and authority-placement judgments, consuming actual
normal/solution outcomes when those owners triggered and resolving their
non-passing routes. It does not require or invent an outcome from an owner that
correctly did not trigger. Consume still-applicable conclusions under root's
conditions; each stage still independently reviews current work/evidence.

The three root-cause workflow routers consume their own closed schemas with
direct projections. All select the existing owner in the table by `profile`;
`implementation_discovery` resumes through `guru-resume-implementation` with
`guru-phase2-implementation-coordinator` retaining semantic ownership.
`classified` hands candidate dispositions to the stage; `mechanism_revision_required`
returns candidate refs/reasons for remove/replace and complete-set reentry;
`diagnosis_required` returns paused repair refs/gaps for bounded investigation
and resubmission through that owner. Delivery uses its current
`planning_revision_required|implementation_required|scope_confirmation_required|blocked`
according to its own review. These routers do not decide completion, production
permission, scope expansion or publication. Unknown/multiple/unmapped results
stop at `root-cause-qualification-blocked`, which consumes the concrete reason.

Qualification remains candidate admission only. Existing stage owners read
`.trellis/spec/workflow/causal-completion-semantics.md` for the common causal
evidence and completion semantics, retaining their own current judgments.


## Bootstrap repair re-entry

Re-enter that same owner using its declared Interface rename and caller authoring. Preserve the original invocation context; consume the actual repair result through its declared exit.
