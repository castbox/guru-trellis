# #434 Public API Cutover

This is the closed disposition of the pre-#434 public IDs affected by the
task-workspace split and terminal-graph retirement. `replaced(new_id)` means
call the new owner with its current contract after fresh review; it never means
that an old DTO or checkpoint can be passed through. IDs not listed below are
not implicitly mapped by prefix. The old graph is available only from a pinned
compatible pre-cutover version.

| Old ID | Disposition |
| --- | --- |
| `guru-create-task-workspace` | `retired_without_replacement` (split into checkout acquisition, Issue creation, task creation, identity and binding) |
| `record-task-workspace-plan` | `replaced(record-task-plan)` |
| `create-task-workspace` | `replaced(create-task)` |
| `check-task-workspace-result` | `replaced(check-task-creation-result)` |
| `recover-task-workspace-result` | `replaced(recover-created-task-result)` |
| `invoke-guru-create-task-workspace` | `replaced(invoke-guru-create-task)` |
| `guru-task-workspace-created` | `replaced(guru-task-created)` |
| `task-workspace-blocked` | `retired_without_replacement` |
| `check-workspace-boundary` | `replaced(check-task-checkout-boundary)` |
| `guru-stage0-create-task-workspace-input-aggregate-2.0` | `retired_without_replacement` |
| `guru-stage0-create-task-workspace-input-execute-reviewed-plan-2.0` | `retired_without_replacement` |
| `guru-stage0-create-task-workspace-input-recover-created-result-1.0` | `retired_without_replacement` |
| `guru-stage0-create-task-workspace-invalid-task-state-stop-2.0` | `retired_without_replacement` |
| `guru-stage0-create-task-workspace-invocation-error-1.0` | `retired_without_replacement` |
| `guru-stage0-create-task-workspace-output-blocked-2.0` | `retired_without_replacement` |
| `guru-stage0-create-task-workspace-output-created-2.0` | `retired_without_replacement` |
| `guru-stage0-create-task-workspace-output-invalid-task-state-2.0` | `retired_without_replacement` |
| `guru-stage0-create-task-workspace-output-refresh-review-2.0` | `retired_without_replacement` |
| `guru-stage0-create-task-workspace-workflow-created-input-2.0` | `retired_without_replacement` |
| `guru-stage0-invocation-workspace-mutation-1.0` | `retired_without_replacement` |
| `https://github.com/castbox/guru-trellis/schemas/guru-task-workspace-plan-2.0.json` | `retired_without_replacement` |
| `https://github.com/castbox/guru-trellis/schemas/guru-task-workspace-result-3.0.json` | `retired_without_replacement` |
| `guru-review-task-publication` | `retired_without_replacement` (new Delivery Review has different authority) |
| `record-task-publication-review` | `retired_without_replacement` |
| `check-task-publication-review` | `retired_without_replacement` |
| `invoke-guru-review-task-publication` | `retired_without_replacement` |
| `review-task-publication-content-identity` | `retired_without_replacement` |
| `guru-production-review-task-publication-workflow-return-to-task-work-input-1.0` | `retired_without_replacement` |
| `guru-production-review-task-publication-stop-blocked-input-1.0` | `retired_without_replacement` |
| `guru-finalize-task` | `retired_without_replacement` (Finish does not publish Delivery) |
| `preview-finalization` | `retired_without_replacement` |
| `record-finalization-gate` | `retired_without_replacement` |
| `check-finalization-gate` | `retired_without_replacement` |
| `execute-finalization-transition` | `retired_without_replacement` |
| `invoke-guru-finalize-task` | `retired_without_replacement` |
| `finalize-task-content-identity` | `retired_without_replacement` |
| `guru-finalize-task-workflow-published-input-1.0` | `retired_without_replacement` |
| `guru-finalize-task-stop-blocked-input-1.0` | `retired_without_replacement` |
| `guru-merge-task-pr` | `retired_without_replacement` (Delivery Merge has a new result) |
| `preview-task-pr-merge` | `retired_without_replacement` |
| `record-task-pr-merge` | `retired_without_replacement` |
| `check-task-pr-merge` | `retired_without_replacement` |
| `execute-task-pr-merge` | `retired_without_replacement` |
| `watch-task-pr-checks` | `retired_without_replacement` |
| `invoke-task-pr-merge` | `retired_without_replacement` |
| `guru-merge-task-pr-workflow-merged-input-1.0` | `retired_without_replacement` |
| `guru-merge-task-pr-stop-merge-blocked-input-1.0` | `retired_without_replacement` |
| `guru-merge-task-pr-stop-closure-mismatch-input-1.0` | `retired_without_replacement` |
| `guru-restore-archived-task` | `retired_without_replacement` (Reactivate requires a normally finished archive) |
| `restore-archived-task` | `retired_without_replacement` |
| `prepare-task.sh` | `retired_without_replacement` |
| `start-task.sh` | `retired_without_replacement` (`guru-activate-task` is a new status-only owner) |
| `finish-work.sh` | `retired_without_replacement` (the platform finish entry routes current owners) |

Legacy tracked task fields remain readable only at their declared normalization
boundary. The current runtime does not consume `task.json.branch`, persisted
checkout paths, task/workspace mappings, or old terminal DTOs as authority.
Old work in progress stays on a pinned compatible version or gets a separate
manual disposition after exact task, PR, remote/local HEAD, base, archive and
Issue checks. A merged old PR with a divergent remote head, such as
`castbox/ai-chat-roleplay-backend#154` / PR #156, is not a reusable Delivery
result; a prepared old Finalizer preview is not executable proof. Do not edit
that business repository, reuse its merged PR, or silently bypass Finalizer.
Normally finished old archives can enter current Reactivate only after unique
source Issue, TaskId, finish-summary/index and archived Git identity checks.
