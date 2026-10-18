# #292 Planning Author migration

Apply the complete matching preset and marketplace workflow together. The
canonical Author package must be source-valid before the workflow switch;
preset installation alone does not change `.trellis/workflow.md`.
Preview with the source-locked Trellis CLI `workflow --marketplace <provider>
--template guru-team --create-new`, compare the preview with canonical bytes,
existing workflow and template hash/sidecars, then apply using the same provider
and `--force`. Preserve actual target edits and inspect each sidecar.

## Current public boundary

- `guru-author-task-plan` is the sole business writer for task PRD, design,
  implement and official planning JSONL. Its eight independent inputs and four
  exits are selected by Interface 1.6; read its package contract for behavior.
- Original qualifiers add `author_candidate_set`, fixed caller Author, bound
  to existing author_paths/author_identity. Approval's planning_scenario_set
  retains its three-file input and caller. Selected aggregate/output and router
  contracts are 2.0; historical schemas remain pinned.
- Architecture keeps its original owner and four profiles. Task-impact planning
  selects independent purpose-specific 3.0 inputs and semantic result;
  candidate_assessment returns to Author and final_plan to adjacent Approval.
  Purpose-less task-impact planning 2.0 is retired. Nonplanning task impact,
  bootstrap, repair and promotion retain legal 2.0 inputs. Seven selected 3.0
  output unions carry both branches. The sync workflow target is a thin return
  to the same Architecture owner, retaining the call's purpose through repair;
  all current callers use that Interface consumer, including nonplanning.
- Approval selects private planning-approval 4.0. Approved/Activation identity
  keeps its meaning. Revision output/consumer 2.0 carries concrete actions to
  Author through the approval revision router. Approval no longer writes plans.
- `production-current-v5` is the current four-package submanifest; the
  unversioned production-current.json aliases it. Versioned v4 remains history.
  Its original 160-case qualification control is unchanged. Author's added
  profile has zero cases in that historical corpus, which proves no new native
  behavior. The old Approval self-authoring seed edge is retired.

## In-flight and owner returns

Interrupted old planning reruns the earliest affected current owner with the
same TaskId/generation and current source/checkout resolution. Never guess a
purpose, transform an old private result into approval, infer approval from
three files, or create a replacement task. Missing current ephemeral producer
results return to their producer. Existing activation/resume_execution dialogue
and pair guard remain unchanged; installation grants no execution permission.

Discovery's existing task-bound entry now accepts both current `planning` and
`in_progress` lifecycles. This enables lost source-selection recovery before
activation while preserving TaskId/generation/branch/checkout validation and
terminal-state rejection. No new Discovery profile, source model or checkpoint
is introduced; normal review remains stdout-only.

Wording planning pass reaches final Architecture. Its selected content-changed
output and workflow consumer 2.0 use a closed planning branch with
`task_ref/change_refs`; the Wording owner projects checked scope identity and
completed revision locators. The original router adds fixed
`profile=wording_reentry` and `mode=workflow` and passes those two fields to the
existing Author input without private-result reads. Nonplanning change-request
and explicit-path branches retain `exit_id/profile/continuation_id` and their
original routes. Historical 1.0 remains pinned, not a current planning input.
Reapply the matching package and workflow together; an old held planning DTO
returns to Wording. Only the original owner may reserialize a still-current
unchanged result with its actual checker receipt; stale or missing evidence
requires fresh complete review. Never invent changed refs, add a revision to
obtain an exit, or relabel an existing pass/blocked result.

Delivery Review policy revision and Completion next independent
Delivery retain their two original routers and distinct reasons. Other
Completion/Phase 2, authority promotion and terminal owners retain their edges.
Start/continue/native brainstorm remain upstream-owned; Guru workflow dispatch
and the installed Author own planning. Do not patch/delete upstream skills,
hooks, CLI source or global packages to enforce this migration.

## Verification boundary

Check source, installed and declared platform projections, overlay drift and
reapply. Separate wrapper/schema proof from real planning/native evidence;
normal prompts, docs states, source design A-D, revision and recovery must be
actually exercised. A missing native/compression observation stays unverified.
One representative clean throwaway and existing update/reapply are sufficient
for this Issue; full multi-platform Upgrade/Release matrices remain with their
original owners. This migration does not publish a software version.

## #292 active-scope boundary

Clarify owns accepted scope before the original Author writes planning.
Current active private result is 4.0; scope_ready public output and the original
clear-router's independent consumer input are 1.0. The output is exactly
exit_id/mode/task_ref/source_selection/revision_refs. The thin router drops
exit_id, adds fixed profile=active_task_scope_change and passes the remaining
fields unchanged to Author's existing input 1.0. AI chooses revision_refs from
actual revisions; scripts do not infer them. Updated planning, planning hashes,
reentry owners and active_task_scope_update are not Clarify prerequisites.
Original Sync/Discovery still handles source mutation or missing context.
Original activation/resume_execution retains TaskId/generation and in_progress.
Historical private3.0/public-clear3.0/clear-consumer2.0 bytes remain unchanged;
old successful active results require fresh original Clarify, while other
profiles keep their contracts. This migration does not imply native semantic,
fixture resume, full installer-matrix or release qualification.
