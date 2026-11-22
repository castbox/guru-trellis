---
name: guru-publish-task-delivery
description: Assess Delivery readiness, present the exact PR preview, and execute or recover Publication.
---

# Guru Publish Task Delivery

Read the complete provider's `review-sufficiency.md` and
`.trellis/spec/workflow/causal-completion-semantics.md` before judging readiness.

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

Read and apply `.trellis/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage`
for shared candidate coverage, engineering facts and recovery. This package
retains its own current judgment, formal result and action boundary.

Read the current Delivery integration contract in [references/contract.md](references/contract.md) first.

## Current preparation and execution

1. Resolve the exact Delivery and candidate. On continuation, first read its
   public Publication, existing PR and original transaction status through
   this owner. If the attributable PR is already MERGED, enter the applicable
   original Merge recovery. A pending action uses the current preparation path.
2. Read the actual passed full Review and Publication-stage Architecture
   qualification for this candidate. Read the accepted task scope, current
   Delivery plan and all three planning bodies. Load the installed shared
   planning body and its Delivery templates. Review the available evidence,
   the fixed candidate, remaining Task responsibility, source and live GitHub
   facts. Adopt any still-applicable independent evidence. Return to the
   original owner for any missing or stale prerequisite.
3. Judge readiness in all ten original dimensions. Author the result using
   `schemas/semantic-publication-readiness-1.0.schema.json`. Use actual Chinese
   PR title/body, Refs for the exact source Issue, current slice summary,
   remaining responsibility and unverified boundaries. Apply the three
   original qualifier applicability conditions to any real candidates. Use
   `publication_candidate_set` only for an applicable nonempty set. Scope,
   planning, implementation and evidence gaps retain their original routes.
4. Invoke `delivery_prepare_publication` through `scripts/invoke.sh --input ...
   --review-input ...`. The runtime checks the supplied judgment and current
   facts, records readiness and returns `publication_prepared` with the exact
   actions. Preparation performs no push or PR mutation.
5. Present the actual repo, base/head, reviewed commit, existing PR or its
   planned creation, remote head, concrete pending actions and the exact
   displayed PR text and disclosures. Obtain dialogue-local confirmation if
   any pending action writes to the remote. Submit the exact prepared object
   to `delivery_execute_publication` with the passed publication action
   review. Pass its objective `preview_identity` as
   `--confirmed-preview-sha256` only after confirmation when actions remain.
   The executor rereads the current facts. When the preview or pending action
   set has materially changed, prepare and present it again before execution.
   Never put confirmation wording or authorization into any carrier.
6. Consume `ready_for_merge` only when the current Publication matches its
   prescribed Merge input. Merge confirms its own action. Use the original
   Closure for the source Issue after Task Completion.

If readiness advanced the phase but the preview was lost before the original
transaction existed, verify current full Review and re-enter
`delivery_prepare_publication` on the same key. Publication resets the
readiness role through its existing legal rework and records one fresh result.
If an original transaction exists, first recover its completed facts. Refresh
the preview for remaining actions using the exact same transaction and PR.
Use `delivery_same_plan_resume` with the original reference when available.
Use `delivery_reprepare_publication` for the same Delivery when a refreshed
entry is required. Recovering a terminal fact requires only readback.

Historical normal `delivery_review_ready` uses the prior complete provider.
See MIGRATION-900 for the active cutover and MIGRATION-794 for retired early
Draft actions. See [the contract](references/contract.md) for the exact current
inputs, exits and recovery cases.

## Current-stage scope revision

`delivery_scope_revision` is this existing owner's semantic re-entry after original
Clarify has published the changed whole-Task scope. Read actual accepted scope,
selected Delivery and obligations; review the retained slice anchors and original
source_selection/revision_refs. Complete the AI gate before invoking this profile.
Do not require stale Planning/Check/Review/Readiness evidence to revise scope.
Project only the reviewed current scope_ref through upstream rework to planning;
invalidate planning/check/full_review/readiness and retain identity, candidate and
historical publication/delivery facts. No new acceptance or approval is inferred.
`delivery_scope_revised` goes only to guru-delivery-scope-revised-router and the
same Delivery Author active_task_scope_change. A retry after lost output reads
matching public scope, planning phase and cleared results; it returns the same
minimal handoff, without replaying rework or installing an approval token.
A new change receives fresh original Clarify and this owner judgment.

For explicit selected legacy maintenance, load the legacy section in `references/legacy-maintenance.md` and use `scripts/legacy-maintenance.sh`; ordinary current invocation remains unchanged.

## Shared Open PR recovery

When the original private transaction is unavailable, read
[Shared Open PR recovery](references/contract.md#shared-open-pr-recovery-635).
Use its independent `delivery_remote_draft_recovery` or
`delivery_remote_ready_recovery` input with exact PR and available source commit.
Review the complete B..H/source/local deltas and public identity/Planning before
invocation. Remote PR head and local binding are separate facts. Retain the
same PR and original executor. Ready may complete remaining actions after
a current applicable readiness result. Draft recovery2.0 only reports already completed exact
PR/HEAD/payload facts and performs no remote action. Pending Draft work returns
to current committed Review/readiness. No remaining remote mutation means no
new confirmation. Missing applicability returns to its original owner;
MERGED recovery stays with Merge.
