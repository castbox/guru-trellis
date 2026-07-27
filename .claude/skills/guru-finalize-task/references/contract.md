# Guru Finalize Task Contract

## Ownership

`guru-finalize-task` is the sole semantic owner of task finalization. It owns
closeout-plan review, side-effect confirmation, recovery routing, and the six
public exits. The existing #105 closeout engine remains the sole deterministic
implementation of plan construction, content push, verification boundary,
unique draft binding, final projection, archive transaction, three-way HEAD
validation, and draft-to-ready.

The package is active and directly discoverable. Its Interface keeps the
standard `workflow.routing=global_workflow` contract used by active Interface
1.3 packages. The registry independently declares
`workflow_integration_state=deferred`, so source and installed validation
require the complete package/distribution contract while rejecting any global
invoke or exit marker for this package. Issue #119 owns switching that registry
metadata to `integrated` and adding the global Finish invocation/order. This
package does not modify or overlay upstream `trellis-finish-work` entries.

## Preconditions

Workflow and standalone modes enforce the same objective preconditions:

- complete compatible Guru Team runtime and active package inventory;
- portable task/worktree or archived-task identity;
- current planning, Phase 2, scope ledger, Docs SSOT, Branch Review, publication
  review, body, and finish-summary-index evidence;
- credential-free repository/base/head/remote identity and GitHub access;
- official `task.py archive --no-commit` contract and empty `after_archive`
  hook;
- allowed metadata tail only.

Publication entry reruns the `guru-review-task-publication` owner checker.
Verification re-entry reruns the
`guru-verify-extension-installation` owner checker for the same task, plan, and
reviewed HEAD. Opaque references select owner-private checkpoints; callers do
not parse checkpoint bodies.

The generic verification checker remains strict. Only this finalizer may apply
the compatibility augmentation for a normal metadata tail created after #117:
the owner seed must match the immutable plan's active task locator, plan ref,
reviewed HEAD, and repository; the remote ref must still resolve to the recorded
HEAD; and the worktree may contain only the plan-declared evidence paths plus
declared uncommitted finalizer outputs. A later evidence HEAD must be the exact
validated evidence commit. Archived recovery reads the committed plan and #117
evidence blobs and accepts only the exact plan-bound archive transaction. Any
additional path, identity drift, or archive-commit drift remains blocked; this
does not relax `guru-verify-extension-installation` for other consumers.

## Semantic Profile

The exact stage order is:

1. Forward behavior: validate the input and run side-effect-free preview or
   current-state discovery.
2. AI Review Gate: judge plan sufficiency, scope, readiness, recovery route,
   findings, and revision action.
3. Conditional human confirmation: before the first side effect or a changed
   plan, confirm the exact `closeout_plan_digest`.
4. Recorder/validator: persist and check `task-finalization-gate.json` against
   current objective facts.
5. Typed exit: perform at most the deterministic transition authorized by the
   checked gate, then emit exactly one public DTO.

The recorder must run only after the AI Review Gate and any required human
confirmation. A script result is evidence for the AI loop, never the semantic
route decision.

## Immutable Preview And Transaction

Preview shows repository, base, branch, reviewed HEAD, task, archive locator,
upstream evidence references, verification requirement, metadata paths, PR
identity strategy, complete side effects, plan digest, and the exact canonical
plan bytes. Formal execution rebuilds the same bytes and digest before any side
effect. Drift blocks.

The deterministic order is fixed:

1. Build and prevalidate the immutable plan.
2. Push the exact reviewed content HEAD.
3. If required, stop before PR/archive and emit `verification_required`.
4. Consume same-plan verified or not-required evidence and push the exact
   pre-draft evidence allowlist.
5. Create or reuse the unique open draft for repo/head/base.
6. Build the final projection and final summary once using the real PR identity.
7. Invoke official `task.py archive --no-commit`, commit and push exactly one
   archive metadata transaction.
8. Require local HEAD, remote branch HEAD, and draft PR head SHA equality.
9. Mark the draft ready and perform no further repository write.

## Recovery

- Missing/stale publication evidence -> `publication_review_stale`.
- Content pushed with verification pending -> `verification_required`.
- Same-plan transient executor failure, draft-to-ready retry, interrupted
  active/archive move, or exact-commit continuation -> `resume_finalization`.
- Active task with a changed archive month -> `reprepare_required`; author a
  fresh intent/context, preview a new plan, and confirm its exact digest.
- Missing, closed, replaced, or ambiguous draft identity; unexpected path;
  invalid private state; or HEAD mismatch -> `blocked`.
- A completed ready recovery -> `published`.

`resume_finalization` is legal only from `content_pushed` with current verified
or not-required evidence, `evidence_ready`, `evidence_pushed`, `draft_bound`,
`projection_validated`, `archive_moved`, `archive_pushed`, or `archived`.
`prepared`, `reprepare_required`, stale state, and terminal `ready` never select
same-plan resume.

Recovery never exposes the private transition labels `prepared`,
`content_pushed`, `evidence_pushed`, `draft_bound`, `projection_validated`,
`archive_moved`, or `archive_pushed`. Users do not choose internal recovery
commands.

## Public Inputs

The seven closed profiles are:

- `publication_ready`: #116 seed plus fresh `finalization_intent`.
- `verification_verified`: #117 verified seed plus fresh `reentry_intent`.
- `verification_not_required`: #117 not-required seed plus fresh
  `reentry_intent`; this workflow-shaped compatibility profile remains stable.
- `standalone_verification_not_required`: the reachable task-bearing #117
  standalone seed `repo_ref/resolved_head/verification_ref` plus target-authored
  `profile/mode/task_ref`. The finalizer loads the private current plan and
  task-local owner evidence instead of publishing `plan_ref`.
- `same_plan_resume`: task/plan seed plus fresh recovery intent/context.
- `reprepare_preview`: task/reason seed plus fresh reprepare intent/context.
- `standalone_finalization`: caller-authored standalone task intent/context.

Producer seed fields and target authoring fields are disjoint. Their union
equals the target profile required set. Runtime performs a no-overwrite merge
and never invents AI intent, task identity, verification judgment, or owner
evidence. The standalone not-required binding requires the owner evidence,
repository, resolved HEAD, verification ref, task, and private plan to remain
current; same-plan recovery reuses that private binding.

## Public Exits

- `verification_required`: task, plan, repository, reviewed HEAD, verification
  target; `repo_ref` is exactly the immutable plan repository; consumed by
  `guru-verify-extension-installation`.
- `publication_review_stale`: task and stable stale reason; consumed by
  `guru-review-task-publication`.
- `resume_finalization`: task and same plan; consumed by this Skill.
- `reprepare_required`: task and `archive_month_changed`; consumed by this
  Skill's reprepare profile. The producer seed is exactly `task_ref` and
  `reason_code`.
- `published`: the exact plan archive locator and canonical PR number/URL;
  consumed by the Finish response.
- `blocked`: closed reason and remediation; consumed by the finalization stop.

Every DTO uses `exit_id`. Gate, plan, review, verification, PR, archive,
recovery, digest, path, blob, and full HEAD facts remain private.

The tracked gate never stores an early public `published` DTO. Before and
through archive it retains only the exact finalizer-private executor marker.
Recorder/checker and executor may validate that pending marker, while the public
wrapper reruns strict route validation and never executes the transition. Only
after the exact archive transaction and ready PR facts are proven may the
wrapper materialize the public DTO in memory, using the plan archive locator;
the materialized DTO is not written back to the gate.

## Script Boundary

Package scripts are dispatcher-only wrappers. Runtime commands may:

- preview through the existing closeout engine;
- record/check the private semantic gate;
- execute one checked deterministic transition through the same engine;
- select the schema for the actual exit and serialize the minimal DTO.

They may not decide close scope, plan sufficiency, publication readiness,
verification adequacy, Docs SSOT, safety/deployment conclusions, semantic pass,
or recovery intent.

## Evaluation And Distribution

Production eval invokes `scripts/invoke.sh` against a repo-local,
checker-passed private owner result. The adapter selects the schema using the
actual `exit_id`, validates it, then compares the expected exit. Expected exit
never enters the adapter/native request.

Shared, Codex, Claude, and Cursor consume byte-identical corpus files. Codex
also checks trusted Git root behavior, Claude checks its input protocol, Cursor
returns stable unsupported/unavailable outcomes, and shared checks request and
response parsing.

Canonical, installed shared, and selected platform package bytes must match.
Scripts remain executable. Preset initial install, reapply, update, managed
hash, `.new`/`.bak`, contract discovery, wrapper invocation, and clean
throwaway behavior are required release evidence.

## Scope Boundary

This contract does not change #105 transaction semantics, activate the global
Finish family, close #115, perform #119 combined acceptance, or remove
upstream overlays owned by #132. It does not add malicious-actor handling,
forgery defenses, concurrent finalizer locks, TOCTOU infrastructure, new fault
injection, incidental crash consistency, or cross-OS atomicity.
