# Guru Finalize Task Contract

## Ownership

`guru-finalize-task` is the sole semantic owner of task finalization. It owns
closeout-plan review, side-effect confirmation, recovery routing, and the six
public exits. The existing #105 closeout engine remains the sole deterministic
implementation of plan construction, content push, verification boundary,
unique draft binding, final projection, archive transaction, three-way HEAD
validation, and draft-to-ready.

The package is active, directly discoverable, and globally integrated. Its
Interface keeps the standard `workflow.routing=global_workflow` contract used
by active Interface 1.3 packages. The registry declares
`workflow_integration_state=integrated`; the global workflow mandatory invokes
the Skill after publication `ready` and uniquely consumes all six exits. Issue
#161 also turns the existing frozen `trellis-finish-work` platform entries into
thin global-workflow routers. Those entries invoke the semantic owners and do
not copy or directly execute this package's deterministic closeout internals.

## Preconditions

Workflow and standalone modes enforce the same objective preconditions:

- complete compatible Guru Team runtime and active package inventory;
- portable task/worktree or archived-task identity;
- current Publication `ready` DTO, scope ledger, durable task/content state,
  body, finish-summary-index, and live reviewed-content Git identity;
- credential-free repository/base/head/remote identity and GitHub access;
- official `task.py archive --no-commit` contract and empty `after_archive`
  hook;
- allowed metadata tail only.

Publication 2.0 entry consumes the minimal `ready` DTO directly, verifies live
content continuity, and runs the exact side-effect-free preview preflight. It
does not locate or rerun the Publication owner checkpoint. A complete legacy
1.x input may use its explicit one-time checker-backed projection.
Verification re-entry reruns the
`guru-verify-extension-installation` owner checker for the same task, plan, and
reviewed HEAD. Opaque verification and same-plan references select only the
owning Skill's private checkpoints; callers do not parse checkpoint bodies.

The generic verification checker remains strict. Only this finalizer may apply
the compatibility augmentation for a normal metadata tail created after #117:
the owner seed must match the immutable plan's active task locator, plan ref,
reviewed HEAD, and repository; the remote ref must still resolve to the recorded
HEAD; and the worktree may contain only the plan-declared transaction paths.
Schema 1.2 keeps `evidence_paths=[]` and current HEAD at the reviewed content
commit until archive. Persisted schema 1.1 compatibility alone may use a later
evidence HEAD, which must be the exact validated legacy evidence commit.
Archived recovery reads the committed plan and applicable #117 evidence blob
from the archive transaction. Any
additional path, identity drift, or archive-commit drift remains blocked; this
does not relax `guru-verify-extension-installation` for other consumers.

One active schema 1.2 pre-draft recovery is deterministic. When the checked
owner result is `publication_review_stale` solely because the reviewed content
HEAD is an ancestor of a newer real content HEAD, the public wrapper may retire
the exact old downstream projection before emitting the existing stale DTO.
The old canonical plan bytes must bind the task, branch, semantic Ledger,
PR body, finish-summary index and pending or passed marketplace projection.
The worktree must contain exactly those untracked outputs plus only the
plan-owned Ledger delta, with no staged path or later final summary. The wrapper
then restores the Ledger from the current-HEAD blob, removes the plan-owned
untracked projection and retires its private gate. Any mismatch is a zero-write
failure. This internal retirement does not decide whether the real content
change needs Phase 2, Task Commit or Branch Review; the workflow follows the
existing mapped stale route and current live task state.

## Semantic Profile

The exact stage order is:

1. Forward behavior: validate the input and run side-effect-free preview or
   current-state discovery.
2. AI Review Gate: judge plan sufficiency, scope, readiness, recovery route,
   findings, and revision action.
3. Conditional human confirmation: before the first side effect or a changed
   plan, present the one current action and ask `确认继续`; accept any clear
   affirmative reply in the current dialogue without recording it or requiring
   the user to repeat an internal digest.
4. Recorder/validator: persist and check the ignored owner-private
   `task-finalization-gate.json` checkpoint against current objective facts.
5. Typed exit: perform at most the deterministic transition authorized by the
   checked gate, then emit exactly one public DTO.

The recorder must run only after the AI Review Gate and any required human
confirmation. A script result is evidence for the AI loop, never the semantic
route decision.

One confirmed plan authorizes its complete declared push, required verification,
Draft PR, archive transaction and Ready transition. Verification, same-plan
resume and private checkpoints do not request generic continuation. A new
confirmation is required only when the side-effect set, target authority or
immutable plan changes; cross-month `reprepare_required` changes the plan and
therefore re-enters confirmation.

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
4. When the plan requires extension verification, consume same-plan verified
   evidence. A plan whose current reviewed paths require no extension
   verification continues without manufacturing a `not_required` handoff.
   Schema 1.2 does not create or push a separate evidence-metadata commit; its
   archive transaction remains a direct child of `reviewed_content_head`.
5. Create or reuse the unique open draft for repo/head/base. When that one
   candidate is an earlier confirmed-plan Draft, first prove its stable
   repo/head/base/current-HEAD/number/canonical-URL identity, then converge its
   title and exact body bytes to the current confirmed plan on the same PR,
   re-query it, and run the complete immutable metadata validation. A matching
   Draft causes no metadata mutation.
6. Build the final projection and final summary once using the real PR identity.
7. Invoke official `task.py archive --no-commit`, commit and push exactly one
   archive metadata transaction.
8. Require local HEAD, remote branch HEAD, and draft PR head SHA equality.
9. Mark the draft ready and perform no further repository write.

### Archive Artifact Lifecycle

Active-task artifacts may be necessary for current-step validation or crash
recovery without becoming permanent handoff documents. New closeout plans use
schema 1.2. `closeout-plan.json` and `finish-summary.json` are untracked active
transaction outputs that move with the task and become tracked only in the
single archive commit. `pr-readiness.json` and
`task-finalization-gate.json` never enter move paths, evidence paths, or the
archive. The Publication wrapper deletes `pr-readiness.json` after validating
its own typed output, before Finalizer entry. The Finalizer retains only its own
checkpoint across same-plan recovery and deletes it after the terminal public
`published` projection is validated.

Schema 1.2 has a 10-file compatibility allowlist: `task.json`, `prd.md`,
`design.md`, `implement.md`, `issue-scope-ledger.json`,
`planning-approval.json`, `phase2-check.json`, `review-gate.json`,
`closeout-plan.json`, and `finish-summary.json`. A newly produced AI-first task
normally has only the seven durable task/content/plan/summary files because the
three review checkpoints are ignored runtime state. Existing task-local review
artifacts may move once through this compatibility allowlist. When marketplace
verification applies, `marketplace-verification.json` is the only optional
schema 1.2 archive file, so the current archive contains at most 10 core files
or 11 files with marketplace evidence.

Intake/context snapshots, assignment or liveness state, commit plans, raw
review rounds, legacy `review.md`, `pr-body.md`, `pr-readiness.json`, and
`finish-summary-index.json` are current-step inputs or reconstructible facts and
are not copied into the long-term archive tree. A crash after move and before or
during pruning re-enters the same idempotent pruning step. Persisted schema 1.0
plans retain their original full-move transaction semantics, and schema 1.1
remains unchanged with its historical evidence commit and 11 core archive files
(plus optional marketplace evidence, for a maximum of 12). Neither legacy
schema is upgraded in place.

## Recovery

- Stale Publication DTO content identity, or missing/stale legacy 1.x
  publication evidence -> `publication_review_stale`. The exact active schema
  1.2 pre-draft head-mismatch projection described above is retired internally
  before this existing DTO is emitted.
- Content pushed with verification pending -> `verification_required`.
- Same-plan transient executor failure, draft-to-ready retry, interrupted
  active/archive move, or exact-commit continuation -> `resume_finalization`.
- Active task with a changed archive month -> `reprepare_required`; preview a
  new plan and obtain fresh current side-effect confirmation through the same generic
  prompt.
- Missing, closed, replaced, or ambiguous draft identity; unstable
  repo/head/base/HEAD/number/URL/Draft identity; unexpected path;
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

Workflow mode automatically consumes every non-terminal recovery exit.
`verification_required` is never rendered as a user-visible status or choice.

## Public Inputs

The seven closed profiles are:

- `publication_ready`: `profile`, `mode`, `task_ref`, and
  `reviewed_content_head` from the current Publication owner output.
- `verification_verified`: the minimal #117 verified seed; no routine re-entry
  intent is authored.
- `verification_not_required`: the minimal #117 not-required seed; this
  workflow-shaped compatibility profile remains stable.
- `standalone_verification_not_required`: the reachable task-bearing #117
  standalone seed `repo_ref/resolved_head/verification_ref` plus target-authored
  `profile/mode/task_ref`. The finalizer loads the private current plan and
  task-local owner evidence instead of publishing `plan_ref`.
- `same_plan_resume`: task/plan seed plus target-owned `profile` and `mode`.
- `reprepare_preview`: task/reason seed plus target-owned `profile` and `mode`.
- `standalone_finalization`: `profile`, `mode`, and `task_ref` only.

Producer seed fields and target authoring fields are disjoint. Their union
equals the target profile required set. Runtime performs a no-overwrite merge
and never invents task identity, verification judgment, or owner evidence. The
standalone not-required binding requires the owner evidence,
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

The ignored owner-private gate never stores an early public `published` DTO.
Before and through archive it retains only the exact finalizer-private executor
marker. Recorder/checker and executor may validate that pending marker, while
the public wrapper reruns strict route validation and never executes the
publish/archive transition; the bounded head-mismatch retirement above is the
only active pre-draft projection exception. Only after the exact archive
transaction and ready PR facts are
proven may the wrapper materialize the public DTO in memory, using the plan
archive locator; the materialized DTO is not written back to the gate. The
Finalizer then removes its checkpoint. The Publication checkpoint is neither
read nor consumed by this path; its minimal `ready` DTO was consumed at entry.

## Script Boundary

Package scripts are dispatcher-only wrappers. Runtime commands may:

- preview through the existing closeout engine;
- record/check the private semantic gate;
- execute one checked deterministic transition through the same engine;
- retire one exact plan-owned active schema 1.2 pre-draft projection after a
  checked publication HEAD mismatch;
- select the schema for the actual exit and serialize the minimal DTO.

They may not decide close scope, plan sufficiency, publication readiness,
verification adequacy, Docs SSOT, safety/deployment conclusions, semantic pass,
or user authorization.

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

This contract does not change #105 transaction semantics, close #115, claim
#119 combined acceptance, or remove upstream overlays owned by #132. Issue
#161 integrates the already active finalizer route without implicitly closing
or rewriting those related issues. It does not add malicious-actor handling,
forgery defenses, concurrent finalizer locks, TOCTOU infrastructure, new fault
injection, incidental crash consistency, or cross-OS atomicity.
