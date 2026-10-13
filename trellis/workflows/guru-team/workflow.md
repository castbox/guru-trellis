# Guru Team Development Workflow
---

## Candidate migration boundary

This #531 source candidate is not the installed runtime of the development Task.
The installed legacy graph continues to own that Task until an explicit migration.
The source directly evolves #292's unique Author into scope-only writing and
eight Delivery profiles, preserving its purpose-bound Planning contracts.
Install only a complete reviewed upstream/Guru pair with matching Interfaces and
projections. Source edits and local tests do not migrate the development Task.
Missing projection or migration evidence fails closed before application.

## Global Workflow Contract

This marketplace workflow is the global Guru Team route. It owns only:

- tool-free initial request classification;
- global owner order and public Task/Delivery routing;
- one mandatory invocation marker for each active stable Guru Skill id;
- every external typed exit, its one declared consumer, and every workflow or
  stop target;
- workspace and task boundary selection, plus Delivery activation;
- Docs SSOT and post-Completion external-work-item Closure integration points;
- human-readable artifact presentation;
- user interaction, external side-effect boundaries, and the authenticated repo-bound `gh`-only GitHub I/O contract in `workflow-contract.md`.

The public graph authority is the active registry plus each package
interface.json. Producer outputs, consumer inputs, projections, and target-owned
authoring partitions come only from those interfaces. This workflow never
reconstructs a route from package implementation, runtime state, or package
artifacts.

The workflow marketplace installs only .trellis/workflow.md. The Guru Team
preset installs the compatible active packages and minimal shared kernel. Frontmatter
discovery is optional convenience; it never replaces a mandatory marker.

## Guru Team Gate

An explicit old-installation upgrade request enters standalone
`guru-upgrade-installation` from the reviewed target source package before
current installed-runtime preflight. It is outside business-task Intake.
Load that package's current contract and consume only its declared exits;
ordinary update, preset apply, and task readers remain current-only.

Explicit independent Git/GitHub requests use
[Manual Git/GitHub Operations](#manual-gitgithub-operations), not task-mode
selection or an inferred lifecycle continuation.

Classify the initial request before repository or network semantic reads:

- simple conversation or information-only requests about existing facts:
  answer directly without creating a GitHub Issue or Trellis task and without
  asking whether one should be created;
- requests to clarify requirements, design a proposed feature, or plan a change
  express change intent even when the user defers file writes or resource
  creation. “讨论需求”, “设计新功能”, and “先做规划” enter the current Guru owner
  route; deferring mutation does not turn them into information-only requests;
- change-intent requests that are not already inside an active-task route first
  invoke `guru-select-workflow-mode`, whether or not an Issue exists or the
  user mentioned task-free. The selector retains its standard/task-free choice;
  active-task change intent enters its existing phase/scope-change owner.
  Respect deferred side effects throughout the selected route;
- `standard_intake` enters guru-sync-base and the existing mapped graph, while
  `task_free` invokes `guru-execute-task-free-change`;
- only guru-create-task:created enters task planning; Issue creation returns to fresh Intake;
- `guru-select-workflow-mode` owns the semantic choice. The shortest explicit
  request is `这次走 task-free` and routes directly. Without explicit intent,
  high-confidence bounded, reversible, low-risk work routes automatically to
  task-free; evidence that is probably suitable but insufficient opens one
  concise mode question; clearly complex or high-risk work routes automatically
  to standard Intake. Issue presence, file count, path, or keywords never decide
  the mode by themselves. Needing isolated execution never alone selects
  standard Intake; the execution owner acquires a suitable linked non-base
  location before candidate writes under its own operation boundary.

Missing packages or markers, duplicate markers, unknown or multiple exits,
unmapped exits, consumer mismatch, target-kind mismatch, dangling targets, or
invalid interface projections stop fail closed.

## Integrated Public Graph

### Architecture Baseline owner
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
### Requirements Design Test SSOT owner
<!-- guru-skill-invoke: {"skill":"guru-maintain-requirements-design-test-ssot","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"ssot_current","consumer":{"kind":"workflow","id":"guru-requirements-design-test-ssot-current-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"sync_required","consumer":{"kind":"skill","id":"guru-maintain-requirements-design-test-ssot"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"revision_required","consumer":{"kind":"workflow","id":"guru-requirements-design-test-ssot-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"baseline_incomplete","consumer":{"kind":"workflow","id":"guru-requirements-design-test-ssot-bootstrap-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-requirements-design-test-ssot","exit":"blocked","consumer":{"kind":"stop","id":"requirements-design-test-ssot-blocked"}} -->
The active package and exit inventories come from the current registry and
Interfaces. Standalone installation upgrade and extension verification are
outside the business-task workflow's mandatory invokes.
### Cross-phase normal-scenario qualification owner
<!-- guru-skill-invoke: {"skill":"guru-qualify-normal-scenario","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"classified","consumer":{"kind":"workflow","id":"guru-normal-scenario-classified-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"scope_confirmation_required","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"mechanism_revision_required","consumer":{"kind":"workflow","id":"guru-normal-scenario-mechanism-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"blocked","consumer":{"kind":"stop","id":"normal-scenario-qualification-blocked"}} -->
### Cross-phase solution-mechanism qualification owner
<!-- guru-skill-invoke: {"skill":"guru-qualify-solution-mechanism","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-solution-mechanism","exit":"classified","consumer":{"kind":"workflow","id":"guru-solution-mechanism-classified-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-solution-mechanism","exit":"scope_confirmation_required","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-solution-mechanism","exit":"mechanism_revision_required","consumer":{"kind":"workflow","id":"guru-solution-mechanism-mechanism-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-solution-mechanism","exit":"blocked","consumer":{"kind":"stop","id":"solution-mechanism-qualification-blocked"}} -->
### Cross-phase root-cause qualification owner
<!-- guru-skill-invoke: {"skill":"guru-qualify-root-cause","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-root-cause","exit":"classified","consumer":{"kind":"workflow","id":"guru-root-cause-classified-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-root-cause","exit":"mechanism_revision_required","consumer":{"kind":"workflow","id":"guru-root-cause-mechanism-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-root-cause","exit":"diagnosis_required","consumer":{"kind":"workflow","id":"guru-root-cause-diagnosis-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-root-cause","exit":"blocked","consumer":{"kind":"stop","id":"root-cause-qualification-blocked"}} -->

### Phase 0 owners
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
### Delivery Planning owners
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
### Active-task base evolution owner
<!-- guru-skill-invoke: {"skill":"guru-reconcile-task-base","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"reconciled","consumer":{"kind":"workflow","id":"guru-base-reconciliation-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"review_continuity_required","consumer":{"kind":"skill","id":"guru-review-branch"}} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-resume-implementation"}} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"planning_stale","consumer":{"kind":"workflow","id":"guru-task-base-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"scope_confirmation_required","consumer":{"kind":"workflow","id":"guru-task-base-scope-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-reconcile-task-base","exit":"blocked","consumer":{"kind":"stop","id":"task-base-reconciliation-blocked"}} -->
### Phase 2 owner
<!-- guru-skill-invoke: {"skill":"guru-check-task","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"delivery_stopped","consumer":{"kind":"skill","id":"guru-review-task-completion"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"passed","consumer":{"kind":"skill","id":"guru-create-task-commit"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"resolved_reconciliation_passed","consumer":{"kind":"workflow","id":"guru-delivery-resolved-reconciliation-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-resume-implementation"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"planning_stale","consumer":{"kind":"workflow","id":"guru-task-check-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"blocked","consumer":{"kind":"stop","id":"task-check-blocked"}} -->
### Phase 3 owners
<!-- guru-skill-invoke: {"skill":"guru-create-task-commit","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"committed","consumer":{"kind":"skill","id":"guru-review-branch"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"revision-required","consumer":{"kind":"skill","id":"guru-create-task-commit"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"blocked","consumer":{"kind":"stop","id":"task-commit-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-review-branch","required":true} -->
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
<!-- guru-skill-exit: {"skill":"guru-reactivate-task","exit":"source_correction_required","consumer":{"kind":"workflow","id":"task-source-correction-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-reactivate-task","exit":"reactivate_blocked","consumer":{"kind":"stop","id":"task-reactivate-blocked"}} -->
## Workflow And Stop Targets
<!-- guru-workflow-target: {"id":"guru-bootstrap-repository-ssot-completed-router"} -->
<!-- guru-workflow-target: {"id":"guru-bootstrap-repository-ssot-baseline-incomplete-router"} -->
<!-- guru-stop-target: {"id":"guru-bootstrap-repository-ssot-blocked"} -->
<!-- guru-workflow-target: {"id":"guru-architecture-baseline-current-router"} -->
<!-- guru-workflow-target: {"id":"guru-architecture-baseline-sync-router"} -->
<!-- guru-workflow-target: {"id":"guru-architecture-baseline-bootstrap-router"} -->
<!-- guru-workflow-target: {"id":"guru-architecture-baseline-planning-router"} -->
<!-- guru-workflow-target: {"id":"guru-architecture-baseline-check-router"} -->
<!-- guru-stop-target: {"id":"architecture-baseline-blocked"} -->
<!-- guru-workflow-target: {"id":"guru-requirements-design-test-ssot-current-router"} -->
<!-- guru-workflow-target: {"id":"guru-requirements-design-test-ssot-planning-router"} -->
<!-- guru-workflow-target: {"id":"guru-requirements-design-test-ssot-bootstrap-router"} -->
<!-- guru-stop-target: {"id":"requirements-design-test-ssot-blocked"} -->
The graph declares every workflow and stop consumer from the active package interfaces.
<!-- guru-stop-target: {"id":"delivery-activation-blocked"} -->
<!-- guru-stop-target: {"id":"invalid-task-state"} -->
<!-- guru-stop-target: {"id":"invalid-delivery-state"} -->
<!-- guru-stop-target: {"id":"delivery-creation-blocked"} -->
<!-- guru-skill-exit: {"skill":"guru-activate-delivery","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-delivery","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-publish-task-delivery","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-delivery","exit":"delivery_scope_revised","consumer":{"kind":"workflow","id":"guru-delivery-scope-revised-router"}} -->
<!-- guru-workflow-target: {"id":"guru-delivery-started-router"} -->
<!-- guru-workflow-target: {"id":"guru-delivery-scope-revised-router"} -->
<!-- guru-workflow-target: {"id":"guru-delivery-planning-author-router"} -->
<!-- guru-workflow-target: {"id":"guru-delivery-selection-router"} -->
<!-- guru-workflow-target: {"id":"guru-delivery-activation-planning-router"} -->
<!-- guru-workflow-target: {"id":"original-request-route"} -->
<!-- guru-workflow-target: {"id":"guru-workflow-standard-intake-router"} -->
<!-- guru-workflow-target: {"id":"guru-normal-scenario-classified-router"} -->
<!-- guru-workflow-target: {"id":"guru-normal-scenario-mechanism-router"} -->
<!-- guru-workflow-target: {"id":"guru-solution-mechanism-classified-router"} -->
<!-- guru-workflow-target: {"id":"guru-solution-mechanism-mechanism-router"} -->
<!-- guru-workflow-target: {"id":"guru-root-cause-classified-router"} -->
<!-- guru-workflow-target: {"id":"guru-root-cause-mechanism-router"} -->
<!-- guru-workflow-target: {"id":"guru-root-cause-diagnosis-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-free-completed"} -->
<!-- guru-workflow-target: {"id":"guru-task-free-resume-active-task-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-free-scope-change-router"} -->
<!-- guru-workflow-target: {"id":"guru-requirements-clear-router"} -->
<!-- guru-workflow-target: {"id":"guru-full-task-intake-chain"} -->
<!-- guru-workflow-target: {"id":"guru-contract-wording-pass-router"} -->
<!-- guru-workflow-target: {"id":"guru-contract-wording-change-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-intake-router"} -->
<!-- guru-workflow-target: {"id":"guru-sync-base"} -->
<!-- guru-workflow-target: {"id":"guru-task-created"} -->
<!-- guru-workflow-target: {"id":"guru-current-task-identity-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-source-review-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-branch-established-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-branch-selection-router"} -->
<!-- guru-workflow-target: {"id":"guru-current-task-checkout-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-branch-binding-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-checkout-acquisition-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-branch-rebound-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-branch-rebind-refresh-router"} -->
<!-- guru-workflow-target: {"id":"guru-bind-task-session-resume-router"} -->
<!-- guru-workflow-target: {"id":"guru-bind-task-session-rebind-router"} -->
<!-- guru-workflow-target: {"id":"guru-bind-task-session-switch-router"} -->
<!-- guru-workflow-target: {"id":"guru-bind-task-session-reactivate-router"} -->
<!-- guru-workflow-target: {"id":"guru-bind-task-session-manual-recovery-router"} -->
<!-- guru-workflow-target: {"id":"guru-current-phase-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-plan-clarify-scope-router"} -->
<!-- guru-workflow-target: {"id":"phase-1-delivery-activation"} -->
<!-- guru-workflow-target: {"id":"guru-base-reconciliation-router"} -->
<!-- guru-workflow-target: {"id":"guru-base-continuity-passed-router"} -->
<!-- guru-workflow-target: {"id":"guru-resume-implementation"} -->
<!-- guru-workflow-target: {"id":"guru-task-base-planning-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-base-scope-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-check-planning-router"} -->
<!-- guru-workflow-target: {"id":"guru-delivery-resolved-reconciliation-router"} -->
<!-- guru-workflow-target: {"id":"guru-branch-review-implementation-router"} -->
<!-- guru-workflow-target: {"id":"guru-branch-review-scope-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-delivery-planning-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-delivery-scope-router"} -->
<!-- guru-workflow-target: {"id":"active-task-continuation"} -->
<!-- guru-workflow-target: {"id":"task-delivery-planning-router"} -->
<!-- guru-workflow-target: {"id":"task-requirements-revision-router"} -->
<!-- guru-workflow-target: {"id":"task-closure-refresh-router"} -->
<!-- guru-workflow-target: {"id":"task-planning-router"} -->
<!-- guru-workflow-target: {"id":"task-session-recovery-router"} -->
<!-- guru-workflow-target: {"id":"task-reactivation-resume-router"} -->
<!-- guru-workflow-target: {"id":"task-source-correction-router"} -->
<!-- guru-stop-target: {"id":"workflow-mode-selection-blocked"} -->
<!-- guru-stop-target: {"id":"normal-scenario-qualification-blocked"} -->
<!-- guru-stop-target: {"id":"solution-mechanism-qualification-blocked"} -->
<!-- guru-stop-target: {"id":"root-cause-qualification-blocked"} -->
<!-- guru-stop-target: {"id":"task-free-change-blocked"} -->
<!-- guru-stop-target: {"id":"base-sync-blocked"} -->
<!-- guru-stop-target: {"id":"change-context-blocked"} -->
<!-- guru-stop-target: {"id":"requirements-clarification-blocked"} -->
<!-- guru-stop-target: {"id":"contract-wording-blocked"} -->
<!-- guru-stop-target: {"id":"change-request-review-blocked"} -->
<!-- guru-stop-target: {"id":"issue-creation-blocked"} -->
<!-- guru-stop-target: {"id":"task-creation-blocked"} -->
<!-- guru-stop-target: {"id":"task-identity-blocked"} -->
<!-- guru-stop-target: {"id":"task-branch-binding-blocked"} -->
<!-- guru-stop-target: {"id":"task-branch-rebind-blocked"} -->
<!-- guru-stop-target: {"id":"task-session-binding-blocked"} -->
<!-- guru-stop-target: {"id":"task-plan-approval-blocked"} -->
<!-- guru-stop-target: {"id":"task-base-reconciliation-blocked"} -->
<!-- guru-stop-target: {"id":"task-check-blocked"} -->
<!-- guru-stop-target: {"id":"task-commit-blocked"} -->
<!-- guru-stop-target: {"id":"branch-review-blocked"} -->
<!-- guru-stop-target: {"id":"task-delivery-review-blocked"} -->
<!-- guru-stop-target: {"id":"task-delivery-publication-blocked"} -->
<!-- guru-stop-target: {"id":"task-delivery-merge-blocked"} -->
<!-- guru-stop-target: {"id":"task-completion-blocked"} -->
<!-- guru-stop-target: {"id":"task-closure-blocked"} -->
<!-- guru-stop-target: {"id":"task-finish-blocked"} -->
<!-- guru-stop-target: {"id":"task-cleanup-complete"} -->
<!-- guru-stop-target: {"id":"task-cleanup-blocked"} -->
<!-- guru-stop-target: {"id":"task-handoff-cleanup-await-destination"} -->
<!-- guru-stop-target: {"id":"task-reactivate-blocked"} -->
<!-- guru-stop-target: {"id":"legacy-archived-review-disposition-required"} -->
<!-- guru-workflow-target: {"id":"guru-task-plan-requirements-ready-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-scope-requirements-ready-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-plan-ready-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-plan-approval-revision-router"} -->
<!-- guru-stop-target: {"id":"task-plan-author-blocked"} -->
### Workflow target behavior
| Target | Global behavior |
| --- | --- |
| guru-task-scope-requirements-ready-router | Project actual Author task_ref/requirements_locator into original Clarify task_scope_requirements_acceptance; add current mode and the adjacent source_selection/revision_refs. Lost source selection re-enters original Clarify; neither metadata nor root PRD reconstructs it. |
| guru-task-plan-requirements-ready-router | Thin-project Author task_ref/delivery_key/candidate into original Architecture delivery_task_impact_sync candidate_assessment; obtain only its fresh authority/route fields from live facts. Never manufacture an impact conclusion or invent a DeliveryKey/planning_root. |
| guru-task-plan-ready-router | Project task_ref/delivery_key to Wording delivery_planning_artifacts and resolve its current three docs; invoke the original Wording owner. |
| guru-task-plan-approval-revision-router | Project task_ref/delivery_key and actual revision_actions to Author delivery_approval_revision, with current mode; no Approval self-writing edge remains. |
| guru-architecture-baseline-sync-router | Invoke original Architecture maintenance for the declared sync_kind/target. Preserve explicit DeliveryKey/planning_root where the selected Interface supports them. Retain planning purpose in this call-local route and rerun that purpose's task impact afterwards; no new assessment owner, checkpoint or lifecycle stage. |
| guru-architecture-baseline-current-router | Validate actual current authority and selected source_profile. Delivery planning dispatches solely by planning_purpose: candidate_assessment projects its actual assessment and key into Author delivery_solution_planning; final_plan projects the actual final assessment directly into adjacent Delivery Approval. Maintenance current reruns fresh impact for the original purpose/stage; promotion returns through fresh Phase 2/commit/review. Downstream Delivery/Completion still requires no_change or reviewed_promoted. |
| guru-architecture-baseline-bootstrap-router | Enter original foundation bootstrap or bounded repair for missing authority; retain the current planning_purpose in call-local route context, then rerun task impact for that purpose. Maintenance 2.0 current is not a planning 3.0 result. |
| guru-architecture-baseline-planning-router | For planning conflict/contract gap, project planning_purpose and concrete conflict/missing refs to Author architecture_conflict_resolution. Actual scope choice uses Clarify. Nonplanning repair keeps its original owner; never reinterpret these exits as current. |
| guru-architecture-baseline-check-router | Return `fitness_regression` to implementation/check and require the affected downstream stages again. |
| guru-requirements-design-test-ssot-current-router | Consume the reviewed authority locator, active version, scope, status, and freshness; the next owner rereads live Requirements, Design, and Test authority. |
| guru-requirements-design-test-ssot-planning-router | Return the exact affected scope and revision code to the current planning or implementation owner. |
| guru-requirements-design-test-ssot-bootstrap-router | Enter controlled foundation bootstrap or repair for the declared missing layer without expanding business scope. |
| original-request-route | Return to the original non-repository request. |
| guru-workflow-standard-intake-router | Enter the existing mandatory `guru-sync-base` route without requiring a pre-existing Issue. |
| guru-normal-scenario-classified-router | Validate the profile binding and return the current invocation-local classifications to the exact original owner. |
| guru-normal-scenario-mechanism-router | Validate the profile binding and return to the exact original owner for remove/replace, then require fresh qualification before further stage judgment. |
| guru-task-free-completed | Report the checked bounded-change edited paths, concise validation results, and explicit unverified boundaries without creating lifecycle or publication resources. |
| guru-task-free-resume-active-task-router | Resume the exact active task from its current status route. |
| guru-task-free-scope-change-router | Enter the existing Scope Change Gate through `guru-clarify-requirements`. |
| guru-requirements-clear-router | Validate the selected scope_ready 2.0 closed shape. Pre-publication scope_ready without task_key projects mode/task_ref/source_selection/revision_refs into Author task_scope_requirements. Post-publication scope_ready with task_key consumes actual accepted scope and routes by current obligations to explicit Creation, affected Delivery rework/withdrawal, or Completion; it never repeats scope writing or creates an empty Delivery. For clear, resume the declared initial Intake, non-current interrupted phase or standalone caller. |
| guru-full-task-intake-chain | Start a separately reviewed task intake from the returned draft. |
| guru-contract-wording-pass-router | change_request still enters original change-request review. delivery_planning_artifacts enters Architecture delivery_task_impact_sync final_plan on the actual current Delivery design, then adjacent Approval. Standalone follows its matching original caller. |
| guru-contract-wording-change-router | Delivery planning content_changed copies public task_ref/delivery_key/change_refs unchanged to Author input, adding only profile=delivery_wording_reentry and mode=workflow; never read private Wording revisions. Author re-enters the earliest affected dependency. Other profiles retain their original affected wording/upstream refresh. |
| guru-task-intake-router | Project `ready.transition.target.kind` exactly once: `proposed_draft` invokes `guru-create-issue`, while `existing_issue` and `standalone_request` invoke `guru-create-task`; never turn an Issue creation result into task creation without fresh Sync and Intake. |
| guru-sync-base | Re-enter `guru-sync-base` and then fresh Intake. `guru-create-issue:created` supplies the newly created exact source Issue and continues as a live Issue, never as a draft/Issue binding; `guru-create-issue:refresh_review` has no created Issue and retains the proposed draft for renewed review. `guru-create-task:refresh_review` retains its existing reviewed source route. No task creation is implied by this target. |
| guru-task-created | Resolve live TaskId/generation/session and checkout, retain adjacent source_selection/revision_refs, then invoke Author task_scope_requirements. Missing selection re-enters original Clarify/context; metadata/files do not reconstruct it. |
| guru-current-task-identity-router | Resume the current task owner only after exact TaskId, generation and source authority validation. |
| guru-task-source-review-router | Return ambiguous legacy source to fresh semantic review; do not guess Issue disposition from branch or PR text. |
| guru-task-branch-established-router | Re-resolve the active checkout with the established branch binding. |
| guru-task-branch-selection-router | Present current candidates for explicit choice, then revalidate through the binding owner. |
| guru-current-task-checkout-router | Resume the exact current lifecycle owner with the live resolved checkout. |
| guru-task-branch-binding-router | Invoke `guru-establish-task-branch-binding` for the exact active task. |
| guru-task-checkout-acquisition-router | Acquire the reviewed checkout through its task owner and re-resolve the same TaskId. |
| guru-task-branch-rebound-router | Re-resolve the task checkout at the new binding revision; do not carry an old session receipt. |
| guru-task-branch-rebind-refresh-router | Return to the rebind owner's fresh target review. |
| guru-bind-task-session-resume-router | Resume the exact TaskId/generation current phase after session validation. |
| guru-bind-task-session-rebind-router | Resume the exact task after current session binding recovery and phase revalidation. |
| guru-bind-task-session-switch-router | Switch only to the explicitly selected TaskId/generation and freshly resolve its phase. |
| guru-bind-task-session-reactivate-router | Resume the reactivated generation; old Finish/Cleanup receipts remain historical. |
| guru-bind-task-session-manual-recovery-router | Recheck the restored binding and current task boundary before phase routing. |
| guru-current-phase-router | Use current C3/C4/C5-resolved Task identity or explicit task mode, then the sole public Delivery continuation. Planning invokes Author delivery_initial_review for the exact selected key with fresh original source selection; no-current Delivery follows actual scope/Creation/Completion/closeout needs. Missing selection returns to its original producer. No Task status or recovered creation DTO supplies a phase. |
| guru-task-plan-clarify-scope-router | Enter the Scope Change Gate through guru-clarify-requirements. |
| phase-1-delivery-activation | Present the current Delivery approved plan, apply the current pair guard, then invoke `guru-activate-delivery`. |
| guru-delivery-planning-author-router | Consume Creation's actual task_ref/delivery_key/planning_root into Author delivery_initial_review with adjacent source_selection and mode. The Author resolves that public planning_root; lost source selection returns to original Clarify. |
| guru-delivery-selection-router | Read the exact TaskKey inventory for a real selection; obtain an explicit DeliveryKey before invoking Creation selection. Never infer identity from a sole inventory row. |
| guru-delivery-activation-planning-router | Return the selected Delivery to its current Planning owner, refresh affected evidence, then invoke Delivery Approval. |
| guru-delivery-scope-revised-router | Select mode/task_ref/delivery_key/source_selection/revision_refs unchanged from delivery_scope_revised; add fixed profile=delivery_active_task_scope_change; explicitly invoke guru-author-task-plan. This is same-slice rework, never a Planning approval. |
| guru-delivery-started-router | Consume the actual public Planning result for same-Delivery implementation. |
| guru-base-reconciliation-router | Consume the checked current pair and resume its closed `resume_target`. |
| guru-base-continuity-passed-router | Consume bounded continuity for the exact pair, reread actual public Check/full_review applicability, and resume the closed target only when both are current for the reconciled candidate. Missing/stale Check re-enters the existing legal rework/begin_check/Check/clean TaskCommit path; missing/stale full_review invokes independent complete Branch Review. Only the actual full Review result seeds Delivery Review. Bounded continuity never manufactures that result. |
| guru-resume-implementation | Resume Phase 2 implementation. |
| guru-task-base-planning-router | Return exact planning impact and DeliveryKey to Author delivery_active_task_scope_change after necessary original Clarify; preserve task/base identity and re-enter affected dependencies. |
| guru-task-base-scope-router | Enter the Scope Change Gate for the exact authority choice. |
| guru-task-check-planning-router | A planning gap invokes Author delivery_approval_revision with exact key and concrete current actions; actual requirement authority change first invokes original Clarify. Implementation-only repair retains Phase 2. |
| guru-delivery-resolved-reconciliation-router | Invoke Check owner’s explicit resolved projection with this TaskRef/DeliveryKey/phase2 commit anchor and fresh authoring of the actual Git integration facts. Feed its `delivery_resolved_candidate` input to Reconcile. The integration commit then returns through the reviewing owner’s rework, implementation begin_check and fresh applicable Check; only that Check may seed the first complete Branch Review. |
| guru-branch-review-implementation-router | Resume Phase 2, then repeat the downstream graph. |
| guru-branch-review-scope-router | Enter the Scope Change Gate, then repeat affected phases. |
| guru-task-delivery-planning-router | Copy Delivery Review planning_revision_required task_ref/delivery_key unchanged and rename reason_refs to revision_refs for `guru-author-task-plan:delivery_delivery_plan_revision`, adding current mode and revision_reason=delivery_policy_gap. Consume the Review owner's actual same-Delivery planning rework; preserve total accepted scope. |
| guru-task-delivery-scope-router | Enter fresh requirements clarification for the exact disputed slice. |
| active-task-continuation | Keep the task active and resume the earliest affected work owner for remaining work. |
| task-delivery-planning-router | Consume Completion additional_delivery_required's actual task_ref/task_key as the seed for `guru-create-delivery:delivery_creation`; reason stays call-local scope context, not an extra public input field. Creation owns the remaining declared scope_ref/delivery_profile/continuation_id/action inputs, slice judgment and necessary choice/side-effect handling. Only its actual created result enters guru-delivery-planning-author-router, then Author delivery_initial_review with original current source_selection; missing selection returns to original Clarify. Preserve the same TaskId/generation and total accepted scope; no old Delivery planning rewrite or Task-root creation inference. |
| task-requirements-revision-router | Consume Completion requirements_revision_required's actual task_ref/task_key/reason in original `guru-clarify-requirements:delivery_task_scope_revision`, with source_exit=requirements_revision_required and current mode/target_locator/resume_target/continuation_id; reason is call-local authority context. Follow actual scope_ready through guru-requirements-clear-router to Author task_scope_requirements, then scope_requirements_ready through guru-task-scope-requirements-ready-router to Clarify task_scope_requirements_acceptance. Only the published scope_ready returns to the clear-router for affected same-Delivery rework/withdrawal, explicit new Creation, or Completion without a Delivery, according to current obligations. Do not preselect old requirements_revision or create an empty slice. |
| task-closure-refresh-router | Refresh the exact source Issue closure fact before resuming Finish. |
| task-planning-router | Resolve the reactivated generation's current Task scope and fresh original source route. Required scope revision enters Author task_scope_requirements and original Clarify publication; unchanged scope routes to actual validation/Completion or explicit new Delivery Creation. Prior-generation approvals are not reused. |
| task-session-recovery-router | Enter `guru-bind-task-session` with current generation and checkout identity. |
| task-reactivation-resume-router | Re-enter the same Reactivate transaction's recovery path without duplicating mutation. |
| task-source-correction-router | Freshly review the legacy source identity before another Reactivate attempt. |

`guru-publish-task-delivery` owns the current PR and its output-loss recovery;
`guru-merge-task-delivery` owns one expected-head merge and emits only a Delivery
result. A stale review returns to Delivery Review, a base evolution returns
through Reconcile/continuity, and a task-content finding returns to Phase 2.
Neither PR state nor merge status is a Completion approval.

Every stop target returns the owning Skill result and safe remediation, then
waits for changed authority or external state. A stop never guesses another
route or exposes package-private state. This stops the automatic chain, not an
independently requested operation under
[Manual Git/GitHub Operations](#manual-gitgithub-operations).

### Mandatory Architecture stage routing

The old archived read-only Finalizer route has no new-graph consumer.
`archived_review_passed` stops at `legacy-archived-review-disposition-required`.
For an old in-flight task, read the exact task/PR/local/remote/base/Finalizer
facts and use a pinned compatible old version or per-case manual disposition;
never project old Finalizer or Merge DTOs into Delivery, Completion or Finish.
`castbox/ai-chat-roleplay-backend#154` / PR #156 is a terminal merged-PR example:
a prepared old preview is not permission to push or create another PR, and
the old execution preflight must reject the same terminal condition.

Every standard task invokes the one stable
`guru-maintain-architecture-baseline` owner through `task_impact_sync` at each
applicable stage. The single mandatory marker above identifies the Skill; these
stage calls are fresh invocations, not duplicated markers or reusable results.
Executor selection and assessment/eligibility behavior belong solely to that
Skill's contract. New assessment stages mandatory invoke it through its fresh
independent subagent entry; downstream stages invoke its current eligibility
entry and consume actual matching-stage output. The caller never substitutes
self-authoring, a prior-stage DTO or an overall gate for that invocation.

| Stage | Required Architecture call | Only current resume target |
| --- | --- | --- |
| Planning candidate | `delivery_task_impact_sync(stage=planning, planning_purpose=candidate_assessment)` | `guru-author-task-plan:delivery_solution_planning` |
| Planning final | `delivery_task_impact_sync(stage=planning, planning_purpose=final_plan)` | Adjacent Delivery `guru-approve-task-plan` |
| Qualified implementation expansion | `delivery_task_impact_sync(stage=implementation_discovery)` | `guru-phase2-implementation-coordinator` |
| Phase 2 | `delivery_task_impact_sync(stage=phase2)` | `guru-check-task` |
| Branch Review | `delivery_task_impact_sync(stage=branch_review)` over the committed full diff | `guru-review-branch` |
| Delivery Review | `delivery_task_impact_sync(stage=publication)` | `guru-review-task-delivery` |
| Completion/Finish | Actual Task `task_impact_sync(stage=acceptance_finish)` when no Delivery; selected Delivery uses `delivery_task_impact_sync` | `guru-review-task-completion` / `guru-finish-task` after Closure |

Every `baseline_current` carries `constitution_status=current` and its exact
source profile. Delivery rows resume only from
`source_profile=delivery_task_impact_sync` with the same DeliveryKey and planning
root; the Task-only acceptance/finish row uses `source_profile=task_impact_sync`.
`source_profile=delivery_bootstrap_foundation|delivery_repair` reruns
`delivery_task_impact_sync(stage=<affected-stage>)` with that same DeliveryKey and
planning root. Task-only `bootstrap_foundation|repair` reruns the matching
`task_impact_sync` call. `source_profile=delivery_promotion|promotion` always
re-enters fresh Phase 2, Task Commit, and
independent committed full-diff Branch Review before any downstream stage. A
missing result stops that stage. `baseline_incomplete` enters bootstrap/repair;
`architecture_conflict` or `contract_incomplete` returns to Planning/repair;
`fitness_regression` returns to implementation/check; and `blocked` stops.
Stale baseline, constitution, contribution, expected-current, or stage identity
always returns `sync_required` to the Architecture owner.
`sync_required(sync_kind=promotion_required)` enters that owner's declared
serialized promotion route; baseline/constitution advance or other stale
authority is repaired or resynchronized by that owner and the affected stage
is rerun.

Delivery Review rejects missing or stale Architecture evidence, every conflict,
incomplete contract, fitness regression, and `promotion_state=reviewed_candidate`.
Completion/Finish accepts a long-term Architecture change only as
`reviewed_promoted`, or accepts a current `no_change` proof when shared current
does not change. A promotion-created shared-current diff returns to fresh Phase
2, a new task commit, and independent committed full-diff Branch Review before
Delivery Review and Completion/Finish rerun. This router establishes Architecture
eligibility only; it does not absorb Delivery publication, whole-task Completion,
or post-Completion Closure/Finish judgments from their owning packages.

### Mandatory qualification profiles

The workflow invokes the normal and solution qualification owners at these exact candidate
boundaries. `guru-qualify-normal-scenario` qualifies the problem scenario and
`guru-qualify-solution-mechanism` qualifies the proposed mechanism; neither
owner replaces the other. Each caller supplies only its profile-specific
candidate set and live locators; the workflow consumes only the four declared
exits from each owner.

| Profile | Trigger before | Classified/mechanism return owner |
| --- | --- | --- |
| `task_free_pre_write` | task-free pre-write suitability or any target write | `guru-execute-task-free-change` |
| `task_free_evolution` | post-write scope/risk evolution judgment or further target write | `guru-execute-task-free-change` |
| `requirements_scope_set` | clarification scope proposal, scope question, or scope disposition | `guru-clarify-requirements` |
| `change_request_candidate_set` | change-request readiness finding, requested test, or blocker | `guru-review-change-request` |
| `planning_scenario_set` | planning acceptance, negative test, finding, or revision action | `guru-approve-task-plan` |
| `implementation_discovery` | Phase 2 edits or tests for a planning-external discovered candidate | `guru-phase2-implementation-coordinator` |
| `base_impact_candidate_set` | base-impact finding, validation obligation, or route | `guru-reconcile-task-base` |
| `phase2_candidate_set` | Phase 2 severity, finding, planning-stale, or implementation route | `guru-check-task` |
| `branch_review_candidate_set` | Branch Review severity, finding, scope route, or blocker | `guru-review-branch` |
| `publication_candidate_set` | Delivery Review finding, task-work return, or blocker | `guru-review-task-delivery` |

For every row above, the caller invokes `guru-qualify-solution-mechanism` with
the same profile before promoting a proposed mechanism into that stage's
acceptance, test, finding, implementation, or publication judgment. A forbidden
OS/kernel/process/descriptor mechanism returns `mechanism_revision_required`
and never enters scope confirmation.

`guru-qualify-normal-scenario:scope_confirmation_required` invokes
`guru-clarify-requirements:normal_scenario_scope_confirmation`, while
`guru-qualify-solution-mechanism:scope_confirmation_required` invokes
`guru-clarify-requirements:solution_mechanism_scope_confirmation`. Each
target-owned profile returns a real authority choice to the closed original
owner; a changed authority or candidate set starts fresh qualification. Already
rejected candidates never enter clarification. Unknown, empty, multiple,
mismatched, or unmapped normal-scenario results stop at
`normal-scenario-qualification-blocked`; the corresponding solution-mechanism
results stop at `solution-mechanism-qualification-blocked`.
For `implementation_discovery`, the semantic owner remains
`guru-phase2-implementation-coordinator`; its deterministic clarification resume
target is the existing `guru-resume-implementation` workflow API.


### Root-cause qualification routing

For each profile in the table, after the caller consumes actual normal and
solution qualification outcomes, explicitly load `guru-qualify-root-cause`
for new or materially changed eligible mechanisms. Consume still-applicable
same-mechanism conclusions at later stages; stage/caller change alone does not
repeat qualification. Step-local applicability and causal judgment belong to
the new package. Each stage still independently reviews current work/evidence.

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

Qualification is candidate admission only. #383 owns the common causal
completion SSOT and stage completion judgments; its absent file does not
block this candidate contract or cause a substitute completion owner.

## Phase Index

```text
Phase 0: Intake  -> base sync, context, clarification, review, Issue or task creation
Phase 1: Plan    -> Author requirements, candidate Architecture, Author solution, Wording, final Architecture, Approval, presentation, Delivery activation
Phase 2: Execute -> implementation discovery re-entry, Architecture candidate check, task check
Phase 3: Finish  -> docs reconciliation, commit, full-diff review, Delivery cycles, Completion, Closure, Finish, Cleanup
```

| State / availability | Route |
| --- | --- |
| no relevant Task or incomplete closeout | Invoke current mode selector; preserve task-free and manual requests. |
| current Delivery | Load the sole continuation, resolve public key/phase and applicable evidence. |
| Task without current Delivery | Scope/first-next slice/Completion/closeout by current authority; no automatic creation. |
| invalid identity/API/owner | Fail closed at the original owner. |

[trellis-runtime-contract]
{
  "delivery_api": "1.0",
  "task_schema": "2.0",
  "profiles": ["pull_request"],
  "owners": {
    "task_scope": "guru-clarify-requirements",
    "creation": "guru-create-delivery",
    "planning": "guru-activate-delivery",
    "implementation": "guru-delivery-implementation-projection",
    "check": "guru-check-task",
    "full_review": "guru-review-branch",
    "readiness": "guru-review-task-delivery",
    "publication": "guru-publish-task-delivery",
    "delivery": "guru-merge-task-delivery",
    "completion": "guru-review-task-completion",
    "closure": "guru-complete-task-closure"
  }
}
[/trellis-runtime-contract]

## Guru Continuation

[trellis-continuation]
### Guru caller continuation

For start, ordinary continuation, a resumed/new chat, and explicit
`trellis-continue`, first read the actual current-chat binding in this Git
common-dir and the current request. A valid formal Task uses the exact bound
Task route below. Stale, conflicting or unreadable binding stops at the original
identity owner; another chat's Task inventory does not establish this chat's
identity. A failed helper or missing injection is not `no_current_task`.

When upstream `trellis-continue` actually returns `no_current_task`, its stop
ends that upstream step only. This Guru workflow caller consumes the return by
freshly checking the absence of a relevant formal binding and reading current
request, live topology and complete candidate diff. Follow the existing
`[workflow-state:no_task]` route: a still-current same-scope task-free selection
re-enters `guru-execute-task-free-change`; a fresh bounded request invokes
`guru-select-workflow-mode` first. Preserve dialogue-local selection origin;
new-chat context must establish the scope and candidate from explicit request
and live facts, not a Task-free identity record. Missing location or scope
returns to its existing interaction/stop, not forced Task creation. Only an
exact relevant Task or archive enters its original lifecycle owner.

This caller does not create, activate or bind a Task to resume task-free work,
clear real bindings, or modify upstream start/continue/extractor/hooks. If a
native entry cannot deliver that upstream return to the Guru caller, stop that
dependent path and report the exact upstream entry/return and missing caller
consumption as unverified. Do not patch the upstream entry or claim a DTO/text
check proves native continuation.

### Bound formal Task / Delivery continuation

Resolve current TaskId/generation, C4 branch binding and unique checkout through
`guru-ensure-task-checkout`, then use the installed public Delivery current query.
Explicit-task mode requires a deliberately selected TaskId. Missing/stale/ambiguous
binding, unsupported schema/API or missing workflow declaration stops at its
original owner; inventory and directory names never select execution.

The sole continuation is used by SessionStart, UserPromptSubmit, start/continue,
natural-language and compressed/new-chat recovery. Execution mode changes the
carrier only. An adjacent checked DTO enters its declared consumer; absent/lost
output returns to its original producer. Public phase is an availability clue,
never a Planning, Check, full Review, readiness or Completion pass.

| Public current query / phase | Unique owner family |
| --- | --- |
| `no_current_task` | Use the Guru caller no-Task route above; preserve task-free and independent manual operations. |
| `no_current_delivery` | Current request/authority determines Task scope Clarify, explicitly selected first/next slice through `guru-create-delivery`, Completion evidence/validation or current Closure/Finish/Cleanup. No automatic empty Delivery. |
| `terminal_delivery` | Original terminal owner releases that exact selection; Task stays bound for Completion. Do not replace identity. |
| `current / planning` | Resume the same Delivery's unique Author, Wording, Architecture and Approval. Only its current `approved` enters `guru-activate-delivery`. |
| `current / implementing` | Resume current implementation; actual owner hands candidate through the public implementation projection to formal Check. |
| `current / checking` | Fresh Phase 2 Architecture then `guru-check-task`; ordinary quality methods do not write formal Check. |
| `current / reviewing` | Check/TaskCommit recovery and candidate binding precede first full independent Branch Review, then Delivery Review. Recover missing evidence through the original owner; phase does not substitute for the gate. |
| `current / publishing` | Current Delivery Review/Publish/Merge owner and original transaction; required gate refresh returns to its declared producer. |
| error / unknown | Fail closed with the exact identity/API/owner diagnostic. |

| Current output or change | Consumer / original producer |
| --- | --- |
| Task creation output lost | `guru-create-task` exact read-only recovery; no new Issue/Task/branch/worktree. |
| Delivery creation/select output lost | `guru-create-delivery` same-operation recovery with explicit public selection or its own retained create input, never sole inventory guessing. |
| Planning incomplete, approval missing/stale | Same Delivery Author/Wording/Architecture/Approval; D2 never overwrites D1's planning_root. |
| Current approval awaits acceptance | `phase-1-delivery-activation` presents current artifacts and invokes new Activation after its dialogue boundary and pair guard. |
| Activation result lost | Original `guru-activate-delivery` recovers the actual recorded result for the same key; no Task-status transition or new Delivery. |
| Check result lost | `guru-check-task` validates its own current evidence or performs fresh semantic Check; no pass from phase or files. |
| Check `passed` | Current pair guard, then `guru-create-task-commit` for necessary dirty content or clean committed candidate. |
| TaskCommit output lost | Same commit owner recovers exact candidate; no duplicate/empty/amended commit to restore stdout. |
| TaskCommit `committed` | Candidate continuity router: affected HEAD returns through Reviewing rework, implementation begin_check and applicable Check; unchanged clean candidate enters independent full Review directly. |
| Branch Review missing/stale | Fresh committed full-diff Architecture and `guru-review-branch`; Phase 2 or bounded continuity cannot replace first full Review. |
| Branch Review `passed` | Pair guard then `guru-review-task-delivery`; `ready` enters Publish, only `ready_for_merge` enters Merge. |
| Publish/Merge success output or public projection lost | Original transaction reads actual PR/HEAD/merge and retries the same public fact; no repeated remote side effect. |
| Same-Delivery findings/plan/base/readiness changes | Original affected owner judges dependency-scoped invalidation and invokes lawful earliest-owner rework. Commit and historical remote facts remain facts. |
| Whole accepted-scope change | `guru-clarify-requirements`, then affected Delivery owner; independent goals follow scope judgment rather than silently expanding this Task. |
| Whole withdrawal/supersession of undelivered slice | Scope decision then current phase owner public stop/release; no empty implementation or false delivery; PR/resources keep their own owner boundaries. |
| Verified `delivered` | `guru-review-task-completion` reviews whole current scope, unallocated work and applicable historical outcomes. |
| Evidence-only update / Reactivate-only validation | Completion's TaskKey entry; no new Delivery or old-generation pass. |
| Completion `completed` | Closure, acceptance-finish Architecture, Finish and Cleanup through their independent outputs. |
| Finished archive / unfinished closeout | Normal finished archive enters Reactivate with new generation; incomplete closeout returns to its original transaction, never new Task or Reactivate. |
| Planning wording is absent or stale | Freshly invoke `guru-review-contract-wording:delivery_planning_artifacts` for the selected public key. |
| Required prewrite Architecture output was lost or candidate facts changed | Re-enter the original Author candidate producer, then Architecture candidate_assessment 3.0 before solution writing. |
| Final Architecture is absent or stale after current Wording | Freshly invoke original Architecture final_plan 3.0 on the current design; its result goes directly to Approval. |

Local dependency gaps block only their true dependent work. The original scope
and stage owners continue independent necessary consumers and retain the exact
missing provider facts; no mock/empty result proves completion.

When a unique, complete, current side-effect plan is already displayed, `确认继续` authorizes only that exact plan. Run its original executor, verify live results, and emit the formal typed exit only on success. The workflow automatically consumes mapped transitions until a new independent side effect, material choice, or fail-closed stop appears. A changed target, payload, authority, or scope invalidates the old confirmation and requires a new display/confirmation. Authorization remains dialogue-local and never enters tracked files, ignored runtime, checkpoints, DTOs, schemas, or archives.
[/trellis-continuation]

[workflow-state:no_task]
For actual upstream `trellis-continue:no_current_task`, consume the Guru caller
continuation above before taking this route; it is not a Task-creation gate.
For an explicit independent Git/GitHub request, read Manual Git/GitHub Operations
in this workflow; missing context is not proof of no task.
Every change-intent request first resolves task identity for the current
workspace and requested Issue. Unrelated active tasks in the repository
inventory are not current-task conflicts, even for the same user; do not ask
the user to select one or switch to task-free because they exist. A checkout
path alone does not bind its task identity to that checkout.
A task bound to the current repository and TaskId must be validated; an incomplete or
conflicting identity stops at `invalid-task-state`. An unfinished task for the
same Issue must resolve to its existing identity rather than create a duplicate;
missing or conflicting bindings stop at `invalid-task-state`.
An archive projected by the current Finish but not yet verified on the target
base is an incomplete closeout, not a Reactivate candidate. Resolve its exact
TaskId/generation and original Closure/Finish transaction, then re-enter
`guru-finish-task:finish_reentry` when those inputs are current. If the
transaction cannot be recovered uniquely, stop for the documented per-case
manual disposition; never create a replacement task or treat the projection
as a normally finished archive.
For a request to continue the original accepted scope, discover relevant
normally finished archives by source Issue or explicit original TaskId before
mode selection. Prove one TaskId, source, accepted scope and terminal Git
identity, then invoke `guru-reactivate-task` for that archive; an ambiguous
or conflicting identity stops at `invalid-task-state`, not new task creation.
Legacy archives discovered by Issue are only candidates until this check.
An old Finalizer residue is not a normally completed archive: keep the task
and PR facts unchanged and route to pinned-old or per-case manual disposition.
Only when no relevant active task, archived incomplete-closeout identity, or
normally finished original-task Reactivate candidate exists does the request
invoke `guru-select-workflow-mode`, including requests without an Issue or
task-free wording.
`这次走 task-free` is direct.
Otherwise: high-confidence bounded low-risk -> `task_free`; insufficient
evidence -> one question; complex/high-risk -> `standard_intake`. Mapped exits
and same-scope retries do not ask again. A legitimate same-scope task-free
continuation re-enters its execution owner with current request and live facts.
Task-free requires suitable linked non-base execution before the first write;
its execution owner consumes location_required and the exact acquisition
action. No Task identity is introduced. Publication remains independent.
[/workflow-state:no_task]

[workflow-state:no_current_delivery]
Load the sole continuation; resolve the exact public Task/Delivery and original owner.
Phase or artifact presence is not a semantic pass.
[/workflow-state:no_current_delivery]

[workflow-state:task_error]
Load the sole continuation; resolve the exact public Task/Delivery and original owner.
Phase or artifact presence is not a semantic pass.
[/workflow-state:task_error]

[workflow-state:planning]
Load the sole continuation; resolve the exact public Task/Delivery and original owner.
Phase or artifact presence is not a semantic pass.
[/workflow-state:planning]

[workflow-state:implementing]
Load the sole continuation; resolve the exact public Task/Delivery and original owner.
Phase or artifact presence is not a semantic pass.
[/workflow-state:implementing]

[workflow-state:checking]
Load the sole continuation; resolve the exact public Task/Delivery and original owner.
Phase or artifact presence is not a semantic pass.
[/workflow-state:checking]

[workflow-state:reviewing]
Load the sole continuation; resolve the exact public Task/Delivery and original owner.
Phase or artifact presence is not a semantic pass.
[/workflow-state:reviewing]

[workflow-state:publishing]
Load the sole continuation; resolve the exact public Task/Delivery and original owner.
Phase or artifact presence is not a semantic pass.
[/workflow-state:publishing]

[workflow-state:delivered]
Load the sole continuation; resolve the exact public Task/Delivery and original owner.
Phase or artifact presence is not a semantic pass.
[/workflow-state:delivered]

[workflow-state:stopped]
Load the sole continuation; resolve the exact public Task/Delivery and original owner.
Phase or artifact presence is not a semantic pass.
[/workflow-state:stopped]

#### 0.0 Base synchronization

Invoke guru-sync-base and consume only its declared exit.

### Intake profile and method routing

For normal prompts, start/continue, resumed and compressed conversations,
load this current workflow and the exact current phase owner. Upstream
`trellis-brainstorm` is a discoverable method; if automatically selected or
reused, current pre-task intent belongs to Guru Clarify and bound Phase 1
writing belongs to Guru Author. Loading it during planning loads this workflow
and invokes Author; do not repeat completed Clarify interviews, ask routine
planning consent, reset task identity or let the method write business docs. Invoke
`guru-clarify-requirements` with `standard_intake` for ordinary initial Intake
or `reviewed_plan_intake` for explicitly selected existing requirements/design.
Initial requests first complete the mandatory selector → Sync → Discovery
graph and use actual `context_ready` as Clarify entry; loading a method alone
does not permit a product question before that entry. Deferred writes or
resource creation remain deferred throughout the graph.
Its six profiles and context loop are package-owned; method loading does not
create another Intake/Planning route. No-change active resume remains with its
current phase rather than restarting Intake.

Discovery `context_ready` dynamically projects `handoff_profile` into Clarify's
current profile input. Clarify `needs_context` enters Discovery `context_request`;
the actual return preserves the original profile/target/continuation and
required task or standalone identity. Every return freshly rebuilds input.
Unknown profiles or mismatched consumers fail closed.

The clear router hands source_selection to current Wording/readiness and task
intake. `guru-task-created` resolves live identity and then current Planning
consumes the adjacent selection, rereads Direct Source and introduced sections,
writes authority locators in prd.md, and records final design dispositions only
in design.md. Loss of selection re-enters original Clarify/context; the current unique Author is the mandatory consumer. Delivery-locator adaptation
remains subject to the candidate migration boundary above.

#### 0.1 Change-context discovery

Invoke guru-discover-change-context and consume only its declared exit.

#### 0.2 Requirements clarification

Invoke guru-clarify-requirements and consume only its declared exit.

#### 0.3 Contract wording review

Invoke guru-review-contract-wording and consume only its declared exit.

#### 0.4 Change-request review

Invoke guru-review-change-request and consume only its declared exit.

#### 0.5 Issue and task creation

The normal repo-changing route is:

guru-sync-base -> guru-discover-change-context ->
guru-clarify-requirements -> guru-review-contract-wording ->
guru-review-change-request -> `guru-task-intake-router` ->
`guru-create-issue` or `guru-create-task` by `ready.transition.target.kind`.

Only `guru-create-task:created` establishes the Task; current scope acceptance and
`guru-create-delivery:created` establish the first Delivery before its Planning. `guru-create-issue:created`
returns to Sync and fresh Intake with the live created Issue as `kind=issue`;
`guru-create-issue:refresh_review` returns with the proposed draft, without
inventing an Issue number. The workflow does not create the issue, branch,
worktree, or task directly. A Scope Change Gate during any active phase
uses guru-clarify-requirements and returns only through its mapped router.

## Phase 1: Plan

#### 1.1 Unique Author and global sequence

Mandatory invoke `guru-author-task-plan` for whole-scope writing and every
Delivery Planning entry, including prompt/start/continue/resume/compression and
mapped reentries. Load its closed profile from the actual original route.
The Author Skill owns source-design convergence, writing, policy/Docs plan,
qualification and dependency judgments; the workflow does not duplicate them.

Consume this one chain by stable owner and actual declared exits:
Author task_scope_requirements → scope_requirements_ready → original Clarify
task_scope_requirements_acceptance → public accepted scope → explicit Delivery
Creation → Author delivery_initial_review → requirements_ready → Architecture
delivery_task_impact_sync candidate_assessment → Author delivery_solution_planning
→ plan_ready → Wording delivery_planning_artifacts → Architecture
delivery_task_impact_sync final_plan → adjacent Delivery Approval → current
presentation/acceptance/pair guard → Delivery activation.

The current Architecture router dispatches by purpose, never by a guessed
stage or prior prose. Candidate current cannot reach Approval; final current
cannot return to Author. Sync/bootstrap/repair re-enters the original purpose.
Conflicts/gaps, regression and blocked retain their explicit consumers/stops.
Author and qualification packages own their step-local profile rules; Wording
owns rewrite and Approval owns its current independent review. Missing/stale
upstream output returns to its producer, and unknown/multiple/unmapped exits
stop. Old unnamed planning writers, direct planning Wording→Approval and
purpose-less task-impact planning 2.0 are retired by MIGRATION-292.

The Task root PRD retains the whole accepted scope. Initial public Task creation
has `accepted_scope=null`: the scope-only Author writes the root PRD and returns
scope_requirements_ready to original Clarify. Clarify rereads it and the actual
adjacent source selection before publishing the installed AuthorityRef through
accept_scope. Its checked post-publication scope_ready enters explicit Creation
or the affected current obligation route. This is Task scope acceptance, not
Delivery plan approval. A later slice rereads the accepted authority; a real
scope change repeats these two same-owner steps before affected rework or exit.
After this checked scope result, mandatory invoke `guru-create-delivery` for an
explicit first/next slice. Its `created` output enters the current unique Author
delivery_initial_review; #292 retains the sole writing responsibility.
The Author resolves public `planning_root`; no task-root development plan is reused.
Delivery Planning produces non-empty `prd.md`, `design.md`, and `implement.md`, plus
one explicit Docs SSOT Plan. Before presentation, invoke the planning profile
of guru-review-contract-wording.


#### 1.5 Delivery activation

Only approved is eligible for plan presentation. Carry its checked
`planning_result_id` unchanged into `guru-activate-delivery`; do not recompute the
identity from the current files when constructing Activation input. A changed
planning identity requires a fresh Planning Approval. Before the active-task pair
guard or any Delivery activation action, resolve the current human artifacts and
show clickable links to `prd.md`, `design.md`, and `implement.md`, together with
the AI semantic conclusion, key design choices, important alternatives and
trade-offs, and remaining unverified boundaries. State that the Delivery remains in
Phase 1 and implementation starts only after the current plan is accepted.

For normal `standard_intake`, stop at that presentation and wait for a clear
affirmative reply made after it. `确认继续`, `可以，继续实现`, `方案没问题，开始做`, and
semantic equivalents accept the complete displayed plan without requiring a
task id, path, branch, SHA, digest, summary repetition, or prescribed wording.
A question, challenge, revision request, partial choice, or ambiguous reply is
not acceptance. Answer a question and keep the same pause when the plan is
unchanged. If a planning artifact or the Docs SSOT Plan changes materially,
re-enter Author for the affected dependency, repeat Wording → final_plan
Architecture → Approval, then present the new
plan; no reply about an older presentation may be reused. Scope or requirement
authority change enters the existing clarification route and repeats the
affected Phase 1 chain. An open AI finding, unresolved scope, or material plan
gap never reaches a presentation that invites activation.

A Phase 0 confirmation never accepts a Phase 1 plan. A current request may
explicitly select autonomous execution and thereby omit only the ordinary plan
pause for an unchanged, fully approved plan. Do not infer that selection or
persist it. Scope, requirement authority, material design, or risk changes
still pause and use their existing route even during autonomous execution.
Neither ordinary nor autonomous Phase 1 progression authorizes task commit,
push, PR, merge, release, or cleanup.

The workflow judges the dialogue locally. It never records user confirmation,
wording, time, source, reference, digest, or approval state in tracked files,
ignored runtime, checkpoints, gates, handoffs, archives, schemas, or public
DTOs, and no recorder or validator parses the reply.

Only after the applicable dialogue boundary is satisfied does approved reach
the active-task pair guard with
`resume_target=delivery_activation`. An unchanged pair resumes activation; a
current pair consumes and routes its recorded exact typed output; a new pair
invokes guru-reconcile-task-base and follows only its declared exit.
After the checked pair route resolves, invoke `guru-activate-delivery` for the
same public DeliveryKey. D1, D2 and same-Delivery replanning use this same owner.
Consume only its declared output; original-owner recovery restores an actual
completed transition without another Task activation or new identity.
Revision and scope exits return only to their declared consumers.


For `guru-clarify-requirements:clear` in either Delivery scope profile, consume
`scope_action` explicitly. `no_change` resumes the original current owner;
`revised` re-enters the earliest affected owner after the Task scope projection.
`withdrawal_required` returns the selected Delivery to its actual current stage
owner, whose Skill performs the public stop and selection release. Clarify has
no stage-writer role. With no current Delivery, Task scope revision resumes
Completion or Creation as selected by the scope judgment and never fabricates
a Delivery solely to stop it. These are automatic mapped routes; PR closure
and resource deletion retain their separate exact side-effect boundaries.
For `planning`, invoke `guru-activate-delivery:delivery_scope_withdrawal`;
for checking/reviewing/publication stages, invoke the actual current stage
Skill's `delivery_scope_withdrawal` profile. In `implementing`, the current
implementation step reviews the scope decision, reason and evidence, then
calls `DeliveryProjection.stop_implementation(key, result)` with its explicit
result identity. This fixed-role projection records public stop/release and
recovers the same fact after output loss. Its returned TaskKey and existing
TaskRef seed `guru-review-task-completion:delivery_completion`; author only
mode/profile. Neither a stopped slice nor the projection decides Completion.


## Phase 2: Execute

#### 2.1 Implementation

Implementation callers inherit the subtraction-first contract from the approved
plan. Workers may execute approved-plan work only. If implementation discovers
an out-of-plan deprecated asset, compatibility need, or owner/authority change,
it stops before editing or adding tests and returns the existing invocation-local
candidate shape for qualification and owner routing.

Before the first edit, and again immediately before every subsequent source,
test, or task-artifact write, validate the live boundary:

    .trellis/guru-team/scripts/bash/check-task-checkout-boundary.sh --json --task <task-path>

The check is read-only at this boundary. Missing or stale task/runtime/worktree
identity is a fail-closed stop; do not rebuild mappings, switch directories,
stash, copy, migrate, clean, or continue writing. A `created` result from
`guru-create-task:created` is required before planning or implementation may
write anything.

Read the planning artifacts, curated specs, and live diff from that worktree.
Use the configured Trellis implement/check agents when available; their
terminal results are ephemeral evidence. Execute the approved Docs SSOT Plan
and implement the current scope.

Before selecting validation, read
`.trellis/spec/workflow/quality-guidelines.md` and apply its `Validation Scope
Ownership` contract. A generic extension change never authorizes the full
multi-platform Throwaway installer matrix.

Every dispatch prompt for an official Trellis implement, check, research,
channel-runtime, or independent-review worker authorizes approved-plan work
only. If that worker observes anything outside the approved planning, it must
stop before editing, adding a test, self-fixing, assigning severity,
classifying, or choosing a route, and return only one invocation-local
candidate shape: `candidate_ref`, `observed_behavior`, `locators`, and
`minimal_reproduction_hint`. The Guru owner rereads the live authority, caller,
diff, and tests and performs fresh qualification before it may continue that
work or dispatch a worker again for it. Official `trellis-*` agent files remain
unchanged upstream-owned inputs to this invocation contract.

If implementation discovery produces any candidate not already closed by the
approved planning, invoke
`guru-qualify-normal-scenario:implementation_discovery` before adding an edit,
test, finding, or route for that candidate. Rejected candidates are dropped;
then invoke `guru-qualify-solution-mechanism:implementation_discovery` and
`guru-qualify-root-cause:implementation_discovery` for new eligible mechanisms before
accepting a proposed implementation mechanism. Mechanism revision returns
here for remove/replace and a fresh invocation;
blocked stops. The coordinator consumes the result in-process and writes no
qualification artifact or checkpoint.

After qualification, an expansion of scope, risk, owner, state authority,
persistence, SDK lifecycle, external integration, or another architecture
boundary makes the Planning Architecture result stale. Stop before the expanded
edit or test and mandatory invoke
`guru-maintain-architecture-baseline:delivery_task_impact_sync(stage=implementation_discovery)`.
Only its fresh current route resumes this coordinator; stale authority returns
`sync_required` and every other non-current exit follows its unique router.
Dispatch the assessment through the Architecture Skill's independent entry,
not an implementation worker already exposed to task narratives. The two
qualification owners retain problem/task-necessity/mechanism judgments before
any planning-external edit or test; this coordinator consumes their routes.

#### 2.2 Task check

`guru-check-task` owns the complete semantic review for the current worktree,
including the subtraction-first policy and maintainability contract. The
workflow only supplies its mandatory Architecture result and consumes the
declared typed exit; it does not duplicate owner-level adequacy checks.

Mandatory invoke
`guru-maintain-architecture-baseline:delivery_task_impact_sync(stage=phase2)` over the
complete worktree candidate. Execute every applicable project Architecture
check and perform the first semantic before/after satisfaction judgment. Only
its fresh current route invokes guru-check-task; failed/unverified mandatory
checks, conflict, incompleteness, stale identity, or fitness regression follow
their Architecture routes and cannot become a Phase 2 pass.

Guru-check-task's passed exit first enters the active-task pair guard with
`resume_target=task_commit`. Only `unchanged` resumes directly to
guru-create-task-commit. A compatible `new_pair` must be integrated by the
confirmed expected-head Reconcile executor and its checked `reconciled` output
returns to fresh Phase 2; it cannot reuse the pre-integration check. Task or
planning findings return through their declared workflow targets.

## Phase 3: Finish

For a Guru task, `guru-finish-work` is the explicit finish launcher, not the
archive owner. Never invoke upstream-owned `trellis-finish-work`: it is not a
consumer in this graph. Only `guru-finish-task` may archive after Completion
and Closure; no caller invokes direct archival or retired session recording.

#### 3.3 Docs SSOT reconciliation

Reconcile durable specs and the approved Docs SSOT Plan.

#### 3.4 Task commit

Invoke `guru-create-task-commit` with the checked public DeliveryKey and
Check result. Its semantic owner selects the actual candidate path: necessary
dirty content uses the exact prepare/review/confirmation/executor transaction;
already committed content uses `delivery_committed_reentry` with a fresh Check
and returns the existing HEAD without stage or commit. Lifecycle metadata
written by the public API does not require a duplicate business commit. The
owner still proves committed stable Task identity and all current Delivery
planning files. Consume only its declared exit. Before consuming `committed`,
compare its HEAD with the actual public Check candidate. If the commit changed
HEAD, the current Reviewing owner performs its legal rework to implementing,
implementation performs `begin_check` for the exact committed candidate, and
`guru-check-task` freshly reviews that candidate. Valid tests may be reused after
applicability judgment. Its `passed` returns through the clean committed-reentry
TaskCommit path, with no second commit, before first complete Branch Review.
An unchanged clean candidate keeps its current Check and proceeds directly.
Only the resulting current committed DTO enters the active-task pair guard with `resume_target=branch_review` before Branch Review.
Only `unchanged` resumes directly to Branch Review. A compatible `new_pair` is
integrated as one confirmed expected-head local merge commit and returns to
fresh Phase 2; the pre-integration Task Commit result is not Branch Review
evidence.

#### 3.5 Branch review

`guru-review-branch` owns the independent complete-range semantic review for
delete, replace, merge, and compatibility-impacting ranges, including both
subtraction dimensions. It does not read Phase 2 evidence; the workflow only
routes its declared result.

After the task-commit pair guard resolves, mandatory invoke
`guru-maintain-architecture-baseline:delivery_task_impact_sync(stage=branch_review)`.
The Architecture owner independently recomputes applicable checks and
before/after satisfaction over the complete committed base-to-HEAD diff; it
cannot reuse Phase 2. Only its fresh current route invokes guru-review-branch,
which performs its own independent complete-range semantic review and likewise
cannot use Phase 2 as Branch Review proof.
Before dispatch, the current dialogue names the independent reviewer identity,
the exact committed `origin/<base>...HEAD` range, and the review target. On
return, it immediately reports the finding summary and semantic owner
conclusion. That conclusion remains provisional: only after the official
checker and the public wrapper both return `passed` for the same current
identity may the caller declare that Branch Review passed. Normal `passed` has
exactly one next consumer: it enters the pair guard with
`resume_target=publication_review`; the target resumes Delivery Review, and no
Finish, archive, or journal route may intervene.
The `base_continuity` profile binds the prior complete Branch Review commit
separately from the current committed reconciliation HEAD. It reviews only the
reconciliation-selected base delta, conflict resolution, resulting tree, and
affected validation; it never represents itself as a new complete Branch
Review. Its distinct `continuity_passed` exit projects the current
continuity-reviewed reconciliation commit as `branch_review_commit` to the
existing continuity router and preserves prior task-content review as private
evidence. The router rereads actual public Check and full_review applicability.
Reconciliation that changed the candidate requires the existing legal rework,
implementation begin_check, fresh Check and clean TaskCommit re-entry first.
If full_review is missing/stale, invoke the independent complete Branch Review;
its actual `passed` result, not bounded continuity, seeds Delivery Review.
Only a still-current actual full_review may resume the original closed target
without repeating that complete Review. This profile accepts
Reconcile outputs from `post_branch_review` and `post_publication` (the current
Delivery Review boundary retains that profile id). The legacy
`finalizer_base_mismatch` profile does not create a Finalizer production route.
`post_plan`, `post_check`, and `post_commit` must never enter bounded continuity
or use it as the first complete Branch Review.

#### 3.6 Delivery review and publication

After Branch Review and the pair guard, mandatory invoke
`guru-maintain-architecture-baseline:delivery_task_impact_sync(stage=publication)`.
Only fresh `baseline_current` with `promotion_state=no_change` or
`reviewed_promoted` enters `guru-review-task-delivery`. The semantic owner
checks the current independently deliverable slice, remaining task work,
validation and unverified boundaries, then authors the exact Chinese PR
title/body with `Refs` only. Missing or stale Architecture evidence returns
to its owner; task-content changes return to Phase 2 and full review.

The checked `ready` DTO enters `guru-publish-task-delivery`, whose own
preview/confirmation, exact HEAD, remote branch and PR transaction govern
push, Draft/Ready transition, and output-loss recovery. It never archives
the task or closes its source Issue. Only its current `ready_for_merge` enters
`guru-merge-task-delivery`; independent expected-head merge confirmation
remains mandatory. Merge output loss is recovered against the same PR and
merge identity. A task-work finding returns directly to the active
implementation owner; there is no archived-task restore step.
The Delivery Review pair guard retains profile `post_publication` but uses
`resume_target=delivery_publication`: unchanged and bounded-continuity routes
both resume the current `guru-publish-task-delivery` successor, never the
retired Finalizer.

#### 3.7 Completion, Closure and Finish

`guru-merge-task-delivery:delivered` feeds `guru-review-task-completion`.
Completion fresh reads the entire accepted scope, all business Delivery facts,
current evidence and requirements authority. A Reactivate generation with only
new validation uses its verified prior terminal archive and fresh current
evidence, not a same-generation merge or any historical Completion pass. Its incomplete exits keep the
same task active and route to the earliest affected owner; evidence-only
updates use its evidence-refresh entry without inventing a Delivery result.
Only `completed` feeds `guru-complete-task-closure`. Exact source Issue closure
requires its own review/confirmation; no-Issue, reference-only, follow-up and
parent dispositions produce `no_mutation` rather than a closing keyword.

After Closure, mandatory invoke
`guru-maintain-architecture-baseline:task_impact_sync(stage=acceptance_finish)`.
A shared-current change requires `reviewed_promoted`; no change requires
current `no_change`. Promotion diff re-enters fresh Phase 2, Task Commit and
independent Branch Review before this stage can pass again.
`guru-finish-task` alone archives the current lifecycle generation. Its
separately reviewed, expected-head-bound bookkeeping commit/PR contains only
the exact task archive and allowed terminal metadata, never business code;
it is not a Delivery cycle and never triggers Completion. The target base must
actually contain the unique terminal archive before `success` can feed
`guru-cleanup-task-resources`. Cleanup owns a separate exact resource review
and confirmation; failure does not undo Completion, Closure or Finish.
Before invoking Cleanup, resolve a retained checkout of the same Git common-dir
that is not among the sealed deletion targets, and invoke Cleanup with that
checkout as its repository root. In particular, after Finish in a Guru-owned
linked task worktree, move the invocation to the retained checkout before
reviewing or deleting the task worktree. If no suitable retained checkout is
available, stop and report the remaining resources for manual disposition;
do not run Cleanup from a worktree it must remove.

For a normally finished archived task, `guru-reactivate-task` first verifies
the original TaskId, source, archive Git identity, accepted scope and current
base. It increments the lifecycle generation and routes to Planning or its
declared session/source/recovery owner. Old Finish/Cleanup receipts cannot
operate on the new generation. Archives containing retired task personnel
fields are not lifecycle candidates. Their TaskIds remain reserved; exact
TaskId or strictly unique source Issue clues may locate one solely for a
read-only unsupported-format diagnostic. Only archives conforming to the
current upstream task schema can enter Reactivate. An old in-flight Finalizer
residue is not a Reactivate entry: use pinned-old or an explicit per-case
manual disposition without bridging old DTOs.

## Global Integration Boundaries

### Manual Git/GitHub Operations

This global boundary owns automatic-stop versus independent manual-operation
behavior. It applies when workflow-state injection, session/task routing, a
hook, checkpoint, or wrapper is missing, stale, or fails during normal use.
Stop that automatic invocation chain and report the failed step, original
error (with secrets redacted), known repo/task/worktree/branch/HEAD/Issue/PR,
and unfinished steps. Read available live facts directly; mark unreadable
facts `unknown`. Missing injection or a failed helper is not evidence of
`no_task`. This failure stop is distinct from the actual upstream
`trellis-continue:no_current_task` return consumed by the Guru caller above.
Do not enter new Intake, switch to task-free, rebuild mappings,
repair hooks/runtime, or manufacture checkpoints to continue.

An automatic stop does not prohibit a user's explicit independent manual
commit, push, PR creation/update, merge, Issue closure, tag/Release, or cleanup
request. The current-session AI handles that specific operation using `git`
and authenticated, explicitly repo-bound `gh`/`gh api`. This is not a new
workflow node, Skill, typed exit, executor, or recovery path, nor a successful
standalone Guru invocation. Phase 2, Task Commit, Branch Review, Delivery
Review/Publish/Merge, Completion, Closure, Finish and Cleanup keep their own
declared consumers; a separate manual operation cannot produce their results.

For each operation, reread its live facts and review its correctness. Display
the exact repository, worktree/path, branch/ref and HEAD (where applicable),
target resources, commands/payload, expected result, and side effects; obtain
confirmation for this operation in the current dialogue before executing it.
An earlier operation's confirmation does not authorize the next one. Before
execution, a changed target, HEAD, payload, or side-effect set requires a fresh
display and confirmation. A new commit SHA produced by the confirmed operation
is an expected result to verify, not a reason to reconfirm that same operation.
Never persist authorization or its process in files, schemas,
DTOs, checkpoints, or logs. If a fact required for this operation cannot be
read or an operation-specific check fails, stop this operation with its exact
reason; unrelated Guru residue alone does not block it.

| Operation | Fresh facts and exact display | Post-operation verification |
| --- | --- | --- |
| commit | Repo/worktree/branch/HEAD, complete staged and unstaged diff plus untracked contents, exact stage paths, Git transaction state, message, and hook effects. | Check new commit parents/tree/message and actual paths; preserve unrelated changes. Do not push. |
| push | Remote, refspec, local HEAD and remote HEAD, and branch update effects. | Read the specified remote branch HEAD; do not create a PR. |
| PR creation/update | Repo/PR/base/head/head SHA, exact Chinese title/body, Draft/Ready state, and closing-keyword effects. | Read actual PR identity, state and metadata; do not merge. |
| merge | PR, expected head, base, GitHub-returned merge eligibility/checks, merge method and exact payload, including automatic Issue-closing effects. Do not add Ruleset or branch-protection reads as prerequisites. | Read actual merge commit and PR state; verify the displayed automatic closing effects without calling Issue closure. |
| Issue closure | Exact Issue, current state, delivery evidence and reason for closure. | Read actual closed/open state; never infer closure from task residue. |
| tag/Release | Exact Guru candidate, existing release contract and its required evidence, tag target, notes, remote tags/Releases, and publishing effects. | Read actual tag/Release target and publication result; never publish upstream Trellis. |
| cleanup | Exact resource paths/refs, uncommitted contents, references/use state, and deletion impact. | Verify only listed resources were handled; do not expand deletion scope. |

Secret redaction, credentials/permissions, destructive-operation confirmation,
Git transaction correctness, and server-enforced remote rules still apply. A manual request
does not bypass the operation's own checks or the existing release contract.
Never chain later operations implicitly, including Ready changes, Issue
closure, release publication, or cleanup.

After success or failure, report two separate results: **Git/GitHub result**
(observed action and verification) and **Workflow residue** (remaining task,
runtime, Delivery, Completion, Closure, Finish and archive state, including
unknowns and unfinished steps). Do not write Phase 2, Branch Review, Delivery,
Completion, Closure, Finish or Cleanup results, forge gates, or clean runtime
residue to make a manual success look like Guru completion. An operation failure
is only that operation's
failure, not automatic Guru re-entry. Returning to Guru lifecycle still requires
its original current entry preconditions and declared routes.

### Workspace and task boundary

- In worktree mode, every source, test, and task-local write occurs only after
  a fresh read-only `check-task-checkout-boundary.sh` confirms that the expected
  TaskId/generation, current TaskBranchBinding, current repository root/cwd,
  branch and live Git worktree registration still match.
  The check must be repeated before each write, not only once when the phase
  starts. Missing `created` evidence or any identity/conflict drift blocks the
  write and routes to explicit recovery or re-selection.
- Editors without an explicit working-directory option use absolute paths under
  that confirmed task worktree.
- The task checkout is the live execution location, not task identity. It never means the
  retired `.trellis/workspace/<developer>/journal-*` namespace. Current task
  resolution uses task metadata, current checkout/branch, live Git worktree
  facts; it does not initialize or read retired workspace mappings, developer
  identity, workspace journal/index, session records, or legacy agent traces.
- Delivery activation consumes only the current Delivery Planning approved output.
- Downstream phases consume public DTOs and live facts, never an upstream
  package artifact.

### Active-task base evolution

At plan approval, Phase 2 pass, task commit, Branch Review pass, and Delivery
Review ready, invoke the package-local deterministic
pair guard before continuing. The guard observes the selected base ref once and
returns only objective unchanged/current/new/blocked pair state. Unchanged or
already-current pairs require no new semantic invocation, GitHub/Docs/history
reads, or interaction. `unchanged` resumes the closed `resume_target` directly;
`current_pair` consumes and routes the recorded exact typed output, then deletes
its one-use checkpoint. It must never resume from the guard's `resume_target`
alone because that would discard a previously recorded non-`reconciled` exit.
Only a new pair invokes guru-reconcile-task-base.

The semantic owner reads live authority and current task/base facts, follows
the installed semantic-retrieval SSOT, and returns exactly one declared exit.
The base pair is an integration clock independent from the live authority and
task-content clock. A base advance alone does not make planning or task content
stale. For `post_plan`, `post_check`, and `post_commit`, the guard derives the
operation pair from the unique live merge base and selected base HEAD; callers
do not provide old/new base SHAs. When the exact candidate is compatible, the
owner first displays and executes one confirmed expected-head local merge
commit. `post_plan` then resumes `delivery_activation`; `post_check` and
`post_commit` return to fresh Phase 2 so all downstream evidence is rebuilt
against the committed integration HEAD.
After complete Branch Review or Delivery Review, the
same compatible result may return `reconciled` only when the candidate preserves
the current reviewed-content identity. If task content remains unchanged but
the candidate needs a new reviewed-content identity, the owner returns
`review_continuity_required`; the current route uses the post-review profiles
and cannot replace the first complete Branch Review. The retained
`finalizer_base_mismatch` profile is not a current Finalizer entry. After the AI
judgment it displays the exact task branch, expected task/base HEADs, candidate
tree, commit scope, and zero remote
effects, obtains confirmation for that mutation, and invokes its deterministic
expected-head executor to create exactly one persistent local reconciliation
commit. The executor must prove clean branch-bound state, expected ancestry, and
candidate-tree equality before the result can enter `base_continuity`.
`planning_stale` requires an actual live authority or approved-planning-
assumption change with exact reason refs.
The workflow routers validate only the minimal pair/route DTO and never repeat
impact classification, candidate construction, validation selection, or review.
Mapped implementation, planning, scope, bounded-continuity, resume, and blocked
routes remain automatic and owner-specific.

### Architecture Baseline

The mandatory `guru-maintain-architecture-baseline` owner is the only semantic
owner of Architecture impact, project-check applicability, contribution/ADR,
promotion, and Architecture typed routes. Standard-task consumers reread live
project authority and use only one fresh stage result. They never copy design
constitution prose, project rules, or Architecture private state.

Planning assesses a real candidate before Author solution writing, then final
Wording-current facts immediately before Approval. Qualified implementation expansion
invalidates it. Phase 2 performs the first candidate before/after judgment, and
Branch Review independently recomputes over the committed full diff. Delivery
Review and Completion/Finish accept only current `no_change` or fully
`reviewed_promoted` state. Shared current changes only by serialized promotion
against expected current identity; a baseline advance returns `sync_required`,
and a promotion diff repeats Phase 2 and Branch Review before downstream reuse.

### Requirements, Design, and Test SSOT

The mandatory `guru-maintain-requirements-design-test-ssot` owner runs
`bootstrap_foundation` when the repository authority is absent or incompatible,
`task_impact_sync` for an approved task delta, `promotion` for a reviewed
isolated contribution, and `repair` for a bounded authority defect. Planning,
Phase 2 Check, Branch Review, Delivery Review, Completion, and Finish consume only
its public routes and reread the live Requirements, Design, and Test authority;
they never read package-private owner state. Architecture inheritance uses only
the public Architecture Baseline locator/version/status.

Each planning cycle chooses exactly one strategy:

- ssot_first;
- delta_first;
- bootstrap_or_repair_docs;
- no_docs_update_needed.

Phase 2 executes the chosen strategy. delta_first merges durable docs before
the final Phase 2 check. Branch Review verifies reconciliation but never
performs the first merge.

### External work item and closure

Delivery Review owns each slice's Refs-only PR payload, including an Issue-backed
Delivery targeting the default branch. Delivery Publish and Merge do not close
the source Issue, and Merge yields a Delivery result, not Task Completion.
`guru-review-task-completion` alone reviews the whole accepted scope and
current evidence; incomplete work keeps the same task active. Only its
`completed` exit enters `guru-complete-task-closure`, which owns the exact
source Issue disposition and any separate confirmed close mutation. No-Issue,
reference-only, follow-up and parent dispositions produce `no_mutation`.
`guru-finish-task` then persists the terminal archive; its bookkeeping PR also
has no Issue-closing keyword. Neither PR merge nor archive state substitutes
for Completion or Closure.

### Human artifacts

Before a planning, Phase 2, Branch Review, Delivery, Completion, Closure, or Finish stop, resolve human-authored artifacts:

    .trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task <task-path>

Show links only for existing `prd.md`, `design.md`, and `implement.md`. Resolve
from the active task through Delivery and Completion, and from the archive only
after Finish. Do not require a fixed table, and do not expose JSON gates, checkpoints, raw agent
reports, payloads, or digests as standard handoff artifacts.

### Interaction and side effects

- Ask only for missing intent, a material scope or plan choice, new external authority, or one fully displayed side-effect set.
- For one current, unique, unambiguous side-effect plan, prompt only 确认继续 and accept any clear affirmative reply.
- Automatically consume mapped exits and mapped re-entry routes.
- Authorization exists only in the current dialogue and is never persisted.
- Issue/task creation, task commit, Delivery push/PR, Delivery merge, post-Completion Issue Closure, Finish archive/bookkeeping, cleanup, and any new external mutation keep their own bounded authority.
- No Skill pass creates permission for a later unrelated side effect.
The confirmation boundary marker IDs below remain static compatibility identifiers;
they do not route to a Finalizer. Current side-effect plans and consumers are
owned by the active Delivery, Closure, Finish and Cleanup Skills above.
<!-- guru-confirmation-boundary: {"id":"issue_creation","profiles":["new_issue"]} -->
<!-- guru-confirmation-boundary: {"id":"workspace_and_task","profiles":["open_issue","new_issue"]} -->
<!-- guru-confirmation-boundary: {"id":"phase_1_plan_review","profiles":["open_issue","new_issue"]} -->
<!-- guru-confirmation-boundary: {"id":"finalizer_side_effect_set","profiles":["open_issue","new_issue"]} -->
<!-- guru-confirmation-boundary: {"id":"expected_head_merge","profiles":["open_issue","new_issue"]} -->

### Platform entry and ownership

Official Trellis owns trellis-start, trellis-continue, trellis-finish-work,
official hooks, agents, runtime agents, bundled skills, and meta references.
The Guru preset does not install or managed-upgrade those paths.

Guru routing is guaranteed by this workflow graph and the installed active
guru-* packages. The only explicit Guru platform entries are the Codex, Claude,
and Cursor guru-finish-work launchers. They read live context and
.trellis/workflow.md, invoke the public graph, and do not depend on package
runtime implementation or package-private artifacts.

## Final Fail-Closed Rule

At every hop, select exactly one Interface-declared exit and exactly one
Interface-declared consumer. If the package, marker, exit, target, projection,
or required live boundary is missing, stale, ambiguous, mismatched, duplicated,
or unknown, stop. Never infer an alternate route from prose, examples, old
artifacts, runtime source, or platform-specific behavior.
This automatic-chain rule preserves the separately requested operation boundary
in [Manual Git/GitHub Operations](#manual-gitgithub-operations).

### Accepted whole-scope change: original stage-owner re-entry

After original Clarify task_scope_requirements_acceptance emits scope_ready2.0,
read current obligations and the exact affected Delivery. The clear-router
retains original source_selection/revision_refs and author-refined scope_action.
For an undelivered retained slice, review actual slice anchors against accepted
scope and invoke original current owner with delivery_scope_revision: planning
→ guru-activate-delivery; checking → guru-check-task; reviewing → the interrupted
guru-review-branch or guru-review-task-delivery; publishing → the interrupted
guru-publish-task-delivery or guru-merge-task-delivery. Do not select a reviewing
or publishing owner merely by phase; retain the actual interrupted semantic step.
Each profile takes mode/task_ref/key/scope_ref/source_selection/revision_refs and
its exact completed semantic gate. No stale downstream gate is an entry proof.
For implementing, the existing guru-phase2-implementation-coordinator reviews
the same scope disposition and calls DeliveryProjection.revise_implementation_scope
with the explicit key and actual reviewed scope_ref, then projects the same
five handoff fields to Author delivery_active_task_scope_change. This remains
within the original implementation step, without another Skill or stage owner.
Output loss re-enters the same owner and recovers public planning scope plus
cleared gate results; it does not manufacture approval or repeat first Activation.
Withdrawal keeps original stop/release entries. Delivered/history-only slices
keep historical facts and are not silently reworked; unmet current obligations
use explicit Creation or whole Completion according to the original judgment.
