# Guru Team Development Workflow
---

## Global Workflow Contract

This marketplace workflow is the global Guru Team route. It owns only:

- tool-free initial request classification;
- phase order and current-task status routing;
- one mandatory invocation marker for each active stable Guru Skill id;
- every external typed exit, its one declared consumer, and every workflow or
  stop target;
- workspace and task boundary selection, plus task activation;
- Docs SSOT and Issue Scope Ledger integration points;
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

Classify the initial request before repository or network semantic reads:

- simple conversation or a non-file-changing request: answer directly without
  creating a GitHub Issue or Trellis task and without asking whether one should
  be created;
- a file-changing request that is not already inside an active-task route first
  invokes `guru-select-workflow-mode`, whether or not an Issue exists or the
  user mentioned task-free. Issue-backed or task-like requests that only ask
  for information remain non-file-changing and are answered directly;
- `standard_intake` enters guru-sync-base and the existing mapped graph, while
  `task_free` invokes `guru-execute-task-free-change`;
- only guru-create-task-workspace:created enters task planning;
- `guru-select-workflow-mode` owns the semantic choice. The shortest explicit
  request is `这次走 task-free` and routes directly. Without explicit intent,
  high-confidence bounded, reversible, low-risk work routes automatically to
  task-free; evidence that is probably suitable but insufficient opens one
  concise mode question; clearly complex or high-risk work routes automatically
  to standard Intake. Issue presence, file count, path, or keywords never decide
  the mode by themselves.

Missing packages or markers, duplicate markers, unknown or multiple exits,
unmapped exits, consumer mismatch, target-kind mismatch, dangling targets, or
invalid interface projections stop fail closed.

## Integrated Public Graph

### Architecture Baseline owner
<!-- guru-skill-invoke: {"skill":"guru-maintain-architecture-baseline","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-architecture-baseline","exit":"baseline_current","consumer":{"kind":"workflow","id":"guru-architecture-baseline-current-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-maintain-architecture-baseline","exit":"sync_required","consumer":{"kind":"skill","id":"guru-maintain-architecture-baseline"}} -->
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
The installed graph is exactly 20 active Skills and 85 package exits. The
business-task workflow is exactly 19 mandatory invokes and 83 external exits.
### Cross-phase normal-scenario qualification owner
<!-- guru-skill-invoke: {"skill":"guru-qualify-normal-scenario","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"classified","consumer":{"kind":"workflow","id":"guru-normal-scenario-classified-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"scope_confirmation_required","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"mechanism_revision_required","consumer":{"kind":"workflow","id":"guru-normal-scenario-mechanism-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-qualify-normal-scenario","exit":"blocked","consumer":{"kind":"stop","id":"normal-scenario-qualification-blocked"}} -->
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
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"ready","consumer":{"kind":"skill","id":"guru-create-task-workspace"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"clarify_requirements","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"review_wording","consumer":{"kind":"skill","id":"guru-review-contract-wording"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"refresh_context","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-change-request","exit":"blocked","consumer":{"kind":"stop","id":"change-request-review-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-create-task-workspace","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"created","consumer":{"kind":"workflow","id":"guru-task-workspace-created"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"refresh_review","consumer":{"kind":"skill","id":"guru-sync-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-workspace","exit":"blocked","consumer":{"kind":"stop","id":"task-workspace-blocked"}} -->
### Phase 1 owner
<!-- guru-skill-invoke: {"skill":"guru-approve-task-plan","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"approved","consumer":{"kind":"workflow","id":"phase-1-task-activation"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"revision_required","consumer":{"kind":"skill","id":"guru-approve-task-plan"}} -->
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
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"passed","consumer":{"kind":"skill","id":"guru-create-task-commit"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-resume-implementation"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"planning_stale","consumer":{"kind":"workflow","id":"guru-task-check-planning-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-check-task","exit":"blocked","consumer":{"kind":"stop","id":"task-check-blocked"}} -->
### Phase 3 owners
<!-- guru-skill-invoke: {"skill":"guru-create-task-commit","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"committed","consumer":{"kind":"skill","id":"guru-review-branch"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"revision-required","consumer":{"kind":"skill","id":"guru-create-task-commit"}} -->
<!-- guru-skill-exit: {"skill":"guru-create-task-commit","exit":"blocked","consumer":{"kind":"stop","id":"task-commit-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-review-branch","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"passed","consumer":{"kind":"skill","id":"guru-review-task-publication"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"continuity_passed","consumer":{"kind":"workflow","id":"guru-base-continuity-passed-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-branch-review-implementation-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"scope_confirmation_required","consumer":{"kind":"workflow","id":"guru-branch-review-scope-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"blocked","consumer":{"kind":"stop","id":"branch-review-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-review-task-publication","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-publication","exit":"ready","consumer":{"kind":"skill","id":"guru-finalize-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-publication","exit":"return_to_task_work","consumer":{"kind":"workflow","id":"guru-task-publication-work-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-task-publication","exit":"blocked","consumer":{"kind":"stop","id":"task-publication-review-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-finalize-task","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"base_reconciliation_required","consumer":{"kind":"skill","id":"guru-reconcile-task-base"}} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"publication_review_stale","consumer":{"kind":"skill","id":"guru-review-task-publication"}} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"resume_finalization","consumer":{"kind":"skill","id":"guru-finalize-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"reprepare_required","consumer":{"kind":"skill","id":"guru-finalize-task"}} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"ready_for_merge","consumer":{"kind":"skill","id":"guru-merge-task-pr"}} -->
<!-- guru-skill-exit: {"skill":"guru-finalize-task","exit":"blocked","consumer":{"kind":"stop","id":"task-finalization-blocked"}} -->
<!-- guru-skill-invoke: {"skill":"guru-merge-task-pr","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-pr","exit":"merged","consumer":{"kind":"workflow","id":"guru-finalization-finish-response"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-pr","exit":"merge_blocked","consumer":{"kind":"stop","id":"task-pr-merge-blocked"}} -->
<!-- guru-skill-exit: {"skill":"guru-merge-task-pr","exit":"closure_mismatch","consumer":{"kind":"stop","id":"task-pr-closure-mismatch"}} -->
## Workflow And Stop Targets
<!-- guru-workflow-target: {"id":"guru-architecture-baseline-current-router"} -->
<!-- guru-workflow-target: {"id":"guru-architecture-baseline-bootstrap-router"} -->
<!-- guru-workflow-target: {"id":"guru-architecture-baseline-planning-router"} -->
<!-- guru-workflow-target: {"id":"guru-architecture-baseline-check-router"} -->
<!-- guru-stop-target: {"id":"architecture-baseline-blocked"} -->
<!-- guru-workflow-target: {"id":"guru-requirements-design-test-ssot-current-router"} -->
<!-- guru-workflow-target: {"id":"guru-requirements-design-test-ssot-planning-router"} -->
<!-- guru-workflow-target: {"id":"guru-requirements-design-test-ssot-bootstrap-router"} -->
<!-- guru-stop-target: {"id":"requirements-design-test-ssot-blocked"} -->
The graph contains exactly 31 workflow targets and 20 stop targets.
<!-- guru-workflow-target: {"id":"original-request-route"} -->
<!-- guru-workflow-target: {"id":"guru-workflow-standard-intake-router"} -->
<!-- guru-workflow-target: {"id":"guru-normal-scenario-classified-router"} -->
<!-- guru-workflow-target: {"id":"guru-normal-scenario-mechanism-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-free-completed"} -->
<!-- guru-workflow-target: {"id":"guru-task-free-resume-active-task-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-free-scope-change-router"} -->
<!-- guru-workflow-target: {"id":"guru-requirements-clear-router"} -->
<!-- guru-workflow-target: {"id":"guru-full-task-intake-chain"} -->
<!-- guru-workflow-target: {"id":"guru-contract-wording-pass-router"} -->
<!-- guru-workflow-target: {"id":"guru-contract-wording-change-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-workspace-created"} -->
<!-- guru-workflow-target: {"id":"guru-task-plan-clarify-scope-router"} -->
<!-- guru-workflow-target: {"id":"phase-1-task-activation"} -->
<!-- guru-workflow-target: {"id":"guru-base-reconciliation-router"} -->
<!-- guru-workflow-target: {"id":"guru-base-continuity-passed-router"} -->
<!-- guru-workflow-target: {"id":"guru-resume-implementation"} -->
<!-- guru-workflow-target: {"id":"guru-task-base-planning-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-base-scope-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-check-planning-router"} -->
<!-- guru-workflow-target: {"id":"guru-branch-review-implementation-router"} -->
<!-- guru-workflow-target: {"id":"guru-branch-review-scope-router"} -->
<!-- guru-workflow-target: {"id":"guru-task-publication-work-router"} -->
<!-- guru-workflow-target: {"id":"guru-finalization-finish-response"} -->
<!-- guru-stop-target: {"id":"workflow-mode-selection-blocked"} -->
<!-- guru-stop-target: {"id":"normal-scenario-qualification-blocked"} -->
<!-- guru-stop-target: {"id":"task-free-change-blocked"} -->
<!-- guru-stop-target: {"id":"base-sync-blocked"} -->
<!-- guru-stop-target: {"id":"change-context-blocked"} -->
<!-- guru-stop-target: {"id":"requirements-clarification-blocked"} -->
<!-- guru-stop-target: {"id":"contract-wording-blocked"} -->
<!-- guru-stop-target: {"id":"change-request-review-blocked"} -->
<!-- guru-stop-target: {"id":"task-workspace-blocked"} -->
<!-- guru-stop-target: {"id":"task-plan-approval-blocked"} -->
<!-- guru-stop-target: {"id":"task-base-reconciliation-blocked"} -->
<!-- guru-stop-target: {"id":"task-check-blocked"} -->
<!-- guru-stop-target: {"id":"task-commit-blocked"} -->
<!-- guru-stop-target: {"id":"branch-review-blocked"} -->
<!-- guru-stop-target: {"id":"task-publication-review-blocked"} -->
<!-- guru-stop-target: {"id":"task-finalization-blocked"} -->
<!-- guru-stop-target: {"id":"task-pr-merge-blocked"} -->
<!-- guru-stop-target: {"id":"task-pr-closure-mismatch"} -->
### Workflow target behavior
| Target | Global behavior |
| --- | --- |
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
| guru-requirements-clear-router | Resume the caller declared by the clarification contract: initial Intake, active-task planning, an interrupted phase, or standalone caller. |
| guru-full-task-intake-chain | Start a separately reviewed task intake from the returned draft. |
| guru-contract-wording-pass-router | Route the checked profile to change-request review, planning approval, or the standalone caller. |
| guru-contract-wording-change-router | Re-enter the affected wording route and any required upstream refresh. |
| guru-task-workspace-created | Resolve the created task worktree and enter Phase 1. |
| guru-task-plan-clarify-scope-router | Enter the Scope Change Gate through guru-clarify-requirements. |
| phase-1-task-activation | Present the current approved plan, wait at the dialogue-local review boundary when required, then validate the approved DTO and run the official task start transition. |
| guru-base-reconciliation-router | Consume the checked current pair and resume its closed `resume_target`. |
| guru-base-continuity-passed-router | Consume bounded continuity for the exact pair and resume its closed `resume_target`. |
| guru-resume-implementation | Resume Phase 2 implementation. |
| guru-task-base-planning-router | Return the exact planning impact to the Planning owner. |
| guru-task-base-scope-router | Enter the Scope Change Gate for the exact authority choice. |
| guru-task-check-planning-router | Route the declared planning action to plan approval or requirements clarification. |
| guru-branch-review-implementation-router | Resume Phase 2, then repeat the downstream graph. |
| guru-branch-review-scope-router | Enter the Scope Change Gate, then repeat affected phases. |
| guru-task-publication-work-router | Resume Phase 2 for task-content findings. |
| guru-finalization-finish-response | Return the canonical merged PR URL and merge commit identity. |
| task-pr-merge-blocked | Stop before merge and report the exact live readiness remediation. |
| task-pr-closure-mismatch | Stop after merge and report the exact GitHub Issue closure mismatch without hand-closing it. |
The Finalizer stale projection supplies exactly `task_ref`,
`branch_review_commit`, and `stale_reason`; the Publication caller authors only
its declared profile, mode, and review intent. Inputs outside the current stale
profile stop fail closed. When live reviewed content advances beyond that
commit, Publication may return a checked task-work finding to the existing Phase
2 router, while `ready` remains continuity-strict.

Every stop target returns the owning Skill result and safe remediation, then
waits for changed authority or external state. A stop never guesses another
route or exposes package-private state.

### Mandatory qualification profiles

The workflow invokes the stable `guru-qualify-normal-scenario` id at these exact
candidate boundaries. Each caller supplies only its profile-specific candidate
set and live locators; the workflow consumes only the four declared exits.

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
| `publication_candidate_set` | Publication finding, task-work return, or blocker | `guru-review-task-publication` |

`scope_confirmation_required` always invokes
`guru-clarify-requirements:normal_scenario_scope_confirmation`. That target-owned
profile returns a real authority choice to the closed original owner; a changed
authority or candidate set starts fresh qualification. Already rejected
candidates never enter clarification. Unknown, empty, multiple, mismatched, or
unmapped results stop at `normal-scenario-qualification-blocked`.
For `implementation_discovery`, the semantic owner remains
`guru-phase2-implementation-coordinator`; its deterministic clarification resume
target is the existing `guru-resume-implementation` workflow API.

## Phase Index

```text
Phase 0: Intake  -> issue-backed base sync, context, clarification, review, workspace
Phase 1: Plan    -> planning artifacts, plan approval, plan review pause, task activation
Phase 2: Execute -> implementation, task check
Phase 3: Finish  -> docs reconciliation, commit, branch review, publication, finalization
```

| State | Route |
| --- | --- |
| no active task | Tool-free classification, then Phase 0 for repo-changing work. |
| planning | Produce the three planning documents and Docs SSOT Plan, run wording review, then invoke guru-approve-task-plan. |
| in_progress | Validate the task worktree, implement the approved scope, then invoke guru-check-task. |
| completed | Enter Phase 3 through the canonical guru-finish-work route. |

[workflow-state:no_task]
Every file-changing request first invokes `guru-select-workflow-mode`, including
requests without an Issue or task-free wording. `这次走 task-free` is direct.
Otherwise: high-confidence bounded low-risk -> `task_free`; insufficient
evidence -> one question; complex/high-risk -> `standard_intake`. Mapped exits
and same-scope retries do not ask again. Task-free still requires checkout
suitability before bounded writes and never authorizes Git/GitHub publication.
[/workflow-state:no_task]

[workflow-state:planning]
Complete prd.md, design.md, implement.md, and the Docs SSOT Plan. Run the
planning wording route and guru-approve-task-plan. Automatically consume mapped
non-approved exits. A checked approved exit enters the workflow-owned plan
presentation and dialogue-local review pause before task activation.
[/workflow-state:planning]

[workflow-state:planning-inline]
Use the same planning route. Inline execution does not weaken mandatory Skill
invocation or task activation.
[/workflow-state:planning-inline]

[workflow-state:in_progress]
Validate the task worktree, implement the approved scope, collect configured
Trellis implementation/check evidence, and invoke guru-check-task. Do not create
implementation-handoff.md.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Use the same approved plans, specs, implementation boundary, and mandatory
guru-check-task route.
[/workflow-state:in_progress-inline]

[workflow-state:completed]
Use canonical guru-finish-work and automatically consume the declared
publication, verification, resume, and reprepare exits.
[/workflow-state:completed]

#### 0.0 Base synchronization

Invoke guru-sync-base and consume only its declared exit.

#### 0.1 Change-context discovery

Invoke guru-discover-change-context and consume only its declared exit.

#### 0.2 Requirements clarification

Invoke guru-clarify-requirements and consume only its declared exit.

#### 0.3 Contract wording review

Invoke guru-review-contract-wording and consume only its declared exit.

#### 0.4 Change-request review

Invoke guru-review-change-request and consume only its declared exit.

#### 0.5 Task workspace creation

The normal repo-changing route is:

guru-sync-base -> guru-discover-change-context ->
guru-clarify-requirements -> guru-review-contract-wording ->
guru-review-change-request -> guru-create-task-workspace.

Only the created exit enters planning. The workflow does not create the issue,
branch, worktree, or task directly. A Scope Change Gate during any active phase
uses guru-clarify-requirements and returns only through its mapped router.

## Phase 1: Plan

#### 1.1 Planning artifacts

Planning produces non-empty `prd.md`, `design.md`, and `implement.md`, plus
one explicit Docs SSOT Plan. Before presentation, invoke the planning profile
of guru-review-contract-wording.

#### 1.4 Task plan approval

Invoke guru-approve-task-plan and consume only its declared exit.

#### 1.5 Task activation

Only approved is eligible for plan presentation. Before the active-task pair
guard or any task activation action, resolve the current human artifacts and
show clickable links to `prd.md`, `design.md`, and `implement.md`, together with
the AI semantic conclusion, key design choices, important alternatives and
trade-offs, and remaining unverified boundaries. State that the task remains in
Phase 1 and implementation starts only after the current plan is accepted.

For normal `standard_intake`, stop at that presentation and wait for a clear
affirmative reply made after it. `确认继续`, `可以，继续实现`, `方案没问题，开始做`, and
semantic equivalents accept the complete displayed plan without requiring a
task id, path, branch, SHA, digest, summary repetition, or prescribed wording.
A question, challenge, revision request, partial choice, or ambiguous reply is
not acceptance. Answer a question and keep the same pause when the plan is
unchanged. If a planning artifact or the Docs SSOT Plan changes materially,
repeat planning wording review and guru-approve-task-plan, then present the new
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
`resume_target=task_activation`. An unchanged pair resumes activation; a
current pair consumes and routes its recorded exact typed output; a new pair
invokes guru-reconcile-task-base and follows only its declared exit.
After the checked pair route resolves, require workspace-boundary success,
validate the approved DTO, and run:

    python3 ./.trellis/scripts/task.py start <task-path>

The status write is not a second planning judgment. Revision and scope exits
return only to their declared consumers.

## Phase 2: Execute

#### 2.1 Implementation

Before edits, validate:

    .trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>

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
mechanism revision returns here for remove/replace and a fresh invocation;
blocked stops. The coordinator consumes the result in-process and writes no
qualification artifact or checkpoint.

#### 2.2 Task check

Invoke guru-check-task. Its passed exit first enters the active-task pair guard
with `resume_target=task_commit`; only the checked resumed route continues to
guru-create-task-commit. Task or planning findings return through their
declared workflow targets.

## Phase 3: Finish

#### 3.3 Docs SSOT reconciliation

Reconcile durable specs and the approved Docs SSOT Plan.

#### 3.4 Task commit

Invoke guru-create-task-commit and consume only its declared exit. Committed
enters the active-task pair guard with `resume_target=branch_review` before
Branch Review.

#### 3.5 Branch review

Invoke guru-review-branch over the complete committed base-to-HEAD range.
Normal passed enters the pair guard with `resume_target=publication_review`.
The `base_continuity` profile reviews only the reconciliation-selected delta,
candidate, and affected validation; its distinct continuity_passed exit resumes
the original closed target without replacing the task-content review.

#### 3.6 Publication review

After branch review passes, invoke guru-review-task-publication. Its semantic owner authors and reviews the exact Chinese PR title/body from live authority.
The checked ready DTO carries that payload directly to Finalizer without a task-local publication handoff file.
`ready` enters the pair guard with `resume_target=task_finalization`; the caller
must not push the reviewed/publication HEAD or create a PR first. Only the
checked resumed route enters Finalizer.

#### 3.7 Finalization

Invoke guru-finalize-task and consume its declared exit; `ready_for_merge` immediately invokes `guru-merge-task-pr`, and only `merged` reaches the finish response after a separate expected-head confirmation, without base sync or direct Issue closure.

Only publication ready enters finalization. Finalizer alone may display and execute the bounded push, PR, archive, and Ready side-effect set.
Verification, stale publication, base reconciliation, resume, and reprepare
exits are automatically consumed by their declared Skills; the workflow never
calls closeout executors directly. A Finalizer base-only mismatch returns
`base_reconciliation_required` with `resume_target=finalization_resume`;
publication_review_stale remains limited to Publication content or metadata.

Before its first remote mutation, Finalizer requires no Open PR and only an absent remote branch or strict historical ancestor of the reviewed commit; recovery accepts only transaction-bound remote/PR identity.
Reprepare keeps title/body in Finalizer owner-private state while its public DTO remains minimal. `close_issues=[]` is refs-only: close keywords stay empty and merge closure is vacuously complete without Issue effects.

## Global Integration Boundaries

### Workspace and task boundary

- In worktree mode, every task-local write occurs only after
  check-workspace-boundary.sh confirms that expected workspace equals the
  current repository root.
- Editors without an explicit working-directory option use absolute paths under
  that confirmed task worktree.
- Task activation consumes only guru-approve-task-plan:approved.
- Downstream phases consume public DTOs and live facts, never an upstream
  package artifact.

### Active-task base evolution

At plan approval, Phase 2 pass, task commit, Branch Review pass, Publication
ready, and Finalizer base-only mismatch, invoke the package-local deterministic
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
The workflow routers validate only the minimal pair/route DTO and never repeat
impact classification, candidate construction, validation selection, or review.
Mapped implementation, planning, scope, bounded-continuity, resume, and blocked
routes remain automatic and owner-specific.

### Docs SSOT

The mandatory `guru-maintain-requirements-design-test-ssot` owner runs
`bootstrap_foundation` when the repository authority is absent or incompatible,
`task_impact_sync` for an approved task delta, `promotion` for a reviewed
isolated contribution, and `repair` for a bounded authority defect. Planning,
Phase 2 Check, Branch Review, Publication, acceptance, and Finish consume only
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

### Issue Scope Ledger

issue-scope-ledger.json is the task-local close/reference authority.
close_issues alone may use PR close keywords. related_issues and followup_issues
remain open. A new or changed scope decision enters the Scope Change Gate
before implementation resumes.

### Human artifacts

Before a planning, Phase 2, Branch Review, publication, or finalization stop, resolve human-authored artifacts:

    .trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task <task-path>

Show links only for existing `prd.md`, `design.md`, and `implement.md`. Resolve from the active task first and from the archive after publication. Do not
require a fixed table, and do not expose JSON gates, checkpoints, raw agent
reports, payloads, or digests as standard handoff artifacts.

### Interaction and side effects

- Ask only for missing intent, a material scope or plan choice, new external authority, or one fully displayed side-effect set.
- For one current, unique, unambiguous side-effect plan, prompt only 确认继续 and accept any clear affirmative reply.
- Automatically consume mapped exits and mapped re-entry routes.
- Authorization exists only in the current dialogue and is never persisted.
- Issue/workspace/task creation, task commit, push/PR/archive, merge, cleanup, and any new external mutation keep their own bounded authority.
- No Skill pass creates permission for a later unrelated side effect.
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
