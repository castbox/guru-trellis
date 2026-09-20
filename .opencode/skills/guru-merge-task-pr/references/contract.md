# Contract

## Closeout Identity And Review Re-entry

Preview has an input/diagnostic contract, not a semantic-pass contract. Known
package failures preserve an explicit `code`, `field_path`, and bounded
`remediation` through the dispatcher. The package classifies these errors at
their source; it does not match natural-language exception text or expose raw
stderr, credentials, local paths, or PR payloads. Unexpected implementation
exceptions still use the generic `internal_error` fallback.

A current, complete Merge input and a real failed semantic dimension may
produce `merge_blocked` with a specific `reason_code` and remediation. This
remains the same fail-closed stop, not an automatic recovery edge. Invalid or
missing input returns its diagnostic before a gate is recorded. The four
existing public exits and their consumers are unchanged.

Normal Finalizer `ready_for_merge` consumption uses the actual public handoff
and current PR facts. Merge does not read Branch Review private files. Its
successful producer retires that checkpoint, so absence alone does not
invalidate a previously consumed review or create an additional gate.
The Branch Review diagnostic `stale_identity` can also describe a missing
checkpoint; it is not proof of an old-schema file or of the Merge failure's
cause.

An interrupted caller must first resolve the same archived task from task,
worktree and committed/live Finalizer facts. Only Finalizer's exact transaction
recovery may converge an old active locator; Merge never edits mappings or
invents a task. Current terminal recovery reprojects the original reviewed
closeout authority, not a new review of archive HEAD.

An unchanged-profile archived Branch Review -> Publication -> Finalizer replay
is not supported. The dedicated chain is archived_review_request ->
review_refresh_required -> Branch Review archived_review ->
archived_review_passed -> Publication archived_publication_review ->
archived_ready -> Finalizer archived_review_refresh -> original ready_for_merge.
The three intermediate edges each require their own workflow-owned Architecture
stage: branch_review, publication, acceptance_finish. Do not rewrite task
status, summary, private evidence, or create an empty commit. New archive HEAD A
is not the original closeout review tip H; Finalizer owns that distinction.

## Archived Review Request

This independent profile has a closed schema, schema_version 2.0 and mode
workflow or standalone. Its payload is exactly task_ref (archived locator),
repo_ref, pr_number, expected_head_sha. No old Publication digest, reviewed merge
message or prior semantic result is accepted. The AI determines whether current
review is necessary before invocation; ordinary Ready handoffs remain on their
original path and require no additional checkpoint.

Preview and each recorder/checker/invoke reread the completed task and current
committed five-file archive, summary PR/branch/base identity, exact current
checkout/worktree, both task/workspace mapping projections, the configured
publish remote's canonical repository identity (empty remote uses `origin`),
remote branch HEAD, selected local origin/base ref and live GitHub facts.
expected_head_sha must equal local HEAD, remote branch HEAD and live PR HEAD.
The PR must still be Ready/Open with the exact branch/base; the local selected
base object must equal the live base ref and be an ancestor of A. Missing or
stale mappings are diagnostics, never repaired here. No other owner's private
checkpoint is read, and no fetch, ref update, task write, archive, push, PR edit,
Ready transition or Issue mutation is performed.

The existing six dimensions have profile-specific scope: pr_ready checks the
existing Ready/Open object; repository_and_head binds archive/publish-remote/mappings
and HEAD; checks_and_reviews checks current required CI and review evidence;
mergeability and repository_policy check current entry blockers;
publication_effect assesses whether this request may enter a new Publication
review without treating the snapshot as old approval. Content/authority gaps
and external blockers remain truthful merge_blocked results or diagnostics,
not successful refreshes. A pending/failed required check cannot produce a
successful refresh. The recorder only validates an AI-authored route and six
dimension results: all passed plus no objective blocker permits the requested
review_refresh_required; a real failed dimension or blocker permits
merge_blocked. merged, closure_mismatch and phase2_reentry_required are not
valid routes for this profile.

review_refresh_required emits exactly exit_id, task_ref, branch_review_commit
(A), pr_payload_snapshot_sha256. The snapshot is SHA-256 of UTF-8 JSON
`{"title":title,"body":body}`, sorted keys, compact separators and no trailing
newline; neither string is trimmed or newline-normalized. It is a fresh
snapshot, not approval or authorization. Its sole consumer is Branch Review's
archived_review profile through a select projection and target-owned authoring
seed (only profile/mode are authored).

The package-private archived-review-gate.json is separate from the original
merge gate. It contains only the exact input, current facts binding, six
semantic results and chosen route. Check/execute revalidate it; invoke records
or consumes only this profile's gate and retires it before returning. The
execute wrapper for this profile only projects the checked result and retires
that gate. It cannot call the merge executor or materialize a merge body.
Public input aggregate 3.0 adds this independent schema; original input/gate
2.0 schemas and the four existing output contracts remain unchanged.

## Semantic And Mutation Boundary

`judgment_mode=semantic`. The AI reads the repo-bound live PR and compares its
base/head branches, expected SHA, and PR-body close keywords with the minimal
reviewed authority supplied by Finalizer or the standalone caller. It also reads
checks, reviews, mergeability and repository merge policy. The Finalizer edge
remains a seed: the Merge AI authors one concrete Chinese `summary` and the
exact PR-native Chinese `subject/body` before the semantic gate. Active input
and gate schemas are 2.0; no legacy adapter is supported.
It selects one method only when policy and
reviewed intent determine it, displays the exact action, and accepts
`确认继续` without asking the user to repeat identities.

Workflow-mode `ready_for_merge` additionally requires
`publication_body_sha256`, the exact Finalizer handoff for the
Publication-reviewed PR body UTF-8 bytes. Merge validates that digest against
the first live PR read before repository-policy or base-ref reads, closing-keyword
derivation, Issue reads, gate recording, or merge mutation. Body-only drift
fails closed under the existing error contract; the caller must obtain a fresh
Publication decision and Finalizer handoff. Merge does not own a typed
reprepare exit. `standalone_merge` rejects the field and does not claim
Publication authority.

The recorder/checker preserve only the current semantic gate, including the
reviewed-message identity and pre-merge base head. The executor materializes the
reviewed body in its ignored owner directory and runs authenticated repo-bound
`gh pr merge --match-head-commit --merge --subject --body-file`; every success,
failure and terminal recovery removes that file. It then rereads the PR, merge
commit, remote base ref and Issues. `merged` requires PR `MERGED`, a complete
merge commit SHA, parents exactly `[pre-merge base head, expected head]`, exact
reviewed subject/body, remote base at the merge SHA, and every
close Issue `CLOSED`/`COMPLETED`, and `closed_at >= merged_at`.
`closure_mismatch` reports exact mismatches without closing anything.
`phase2_reentry_required` represents one AI-reviewed current-scope task-work
finding that requires changing the archived task content. It carries only the
exact PR/task/archive/finding identity required by
`guru-restore-archived-task`, performs no remote mutation, and does not require
merge confirmation. Provider, permission, ruleset, required-check,
mergeability, and other external blockers remain `merge_blocked`, which also
performs no mutation.

## Original Public Invoke Contract

`invoke-task-pr-merge` through `scripts/invoke.sh` is the sole public
post-confirmation Happy Path. A new transaction requires the current public
input and AI-authored semantic review;
it performs exactly one complete pre-merge snapshot, records the gate from that
same checked object, runs the unique expected-head mutation, performs exactly
one complete post-merge snapshot, persists the terminal result, projects the
existing public DTO, and removes the gate/body state. It does not call the
package-private recorder/checker/executor commands and therefore does not
repeat their full reads.

If the mutation completed but stdout, the post-read, or terminal persistence
was lost, the next invocation with the same `--review-input` performs one
read-only snapshot. A
retained non-terminal gate remains the primary recovery receipt. If successful
terminal cleanup already removed that gate, the caller must resupply the same
AI-authored semantic review; an exact already-merged PR reconstructs an
in-memory gate from the live merge commit's two parents, validates the reviewed
message and terminal facts, and returns without writing private state or
repeating the mutation. An unmerged state continues only when the same retained
gate/input/base/head facts remain current. A persisted terminal output is
similarly revalidated once, projected, and cleaned. After any terminal or
re-entry DTO is selected, the public invocation performs only local gate/body
cleanup and returns; it does
not start CI polling or any other Git, GitHub, Trellis, workflow, Issue,
base-sync, or cleanup operation.

The `record`, `check`, and `execute` commands remain package-private diagnostics
and bounded recovery surfaces.
## Required Check Watcher

`watch-task-pr-checks` is one deterministic external-CI watcher bound to exact
`repo`, PR number, and expected head SHA. Each poll first verifies the same PR
head and then reads only GitHub's required checks. It returns one stable fact
status: `checks_succeeded`, `checks_failed`, `checks_pending_timeout`, or
`head_changed`, plus the observed checks, poll count, and
`external_ci_wait_ms`. It performs no merge mutation, semantic readiness
decision, route selection, Issue mutation, or terminal follow-up, and it must
not be combined with another watcher or Agent while-loop.

The reviewed body canonical form ends at the final `PR: #<pull_request>`
line without a trailing newline. This is the exact body returned by GitHub's
commit API after `--body-file` persistence, so the post-merge comparison does
not weaken or normalize either side.

After post-merge verification, the executor persists the minimal terminal
output before returning it to the dispatcher. If stdout is lost, the same gate
must reread the exact PR, expected head and branches, merge commit message and
parents, remote base ref, close keywords, and Issue closure facts. Only an exact terminal match is returned;
the executor performs zero repeated GitHub mutation, and a persisted
`closure_mismatch` remains that exit until consumed.

The closure verification set is parsed from the live PR body. Before merge this
set is observed but does not trigger Issue reads or a new closure decision. After
merge, every named Issue must be `CLOSED`/`COMPLETED` with `closed_at >= merged_at`;
an empty set is vacuously complete and triggers no Issue reads.

The gate is ignored owner-private runtime and is deleted after its typed output
is consumed. It never stores authorization, Finalizer transaction, local base
state, task cleanup instructions, or full GitHub payloads.
