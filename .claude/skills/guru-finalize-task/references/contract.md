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

- complete current Guru Team runtime and active package inventory;
- portable task/worktree or archived-task identity;
- current Publication `ready` DTO with exact title/body, scope ledger, durable
  task/content state, and live reviewed-content Git identity;
- credential-free repository/base/head/remote identity and GitHub access;
- official `task.py archive --no-commit` contract and empty `after_archive`
  hook;
- allowed metadata tail only.

The current Publication entry consumes the minimal `ready` DTO directly, verifies live
content continuity, and runs the exact side-effect-free preview preflight. It
does not locate or rerun the Publication owner checkpoint. Verification re-entry reruns the
`guru-verify-extension-installation` owner checker for the same task, plan, and
`branch_review_commit`. Opaque verification and same-plan references select only the
owning Skill's private checkpoints; callers do not parse checkpoint bodies.

The verification checker binds the current owner seed, immutable plan,
repository, remote ref, `branch_review_commit`, local and remote
reviewed-content identities, and the plan-declared transaction paths. Archived
recovery reads the committed plan and current verification evidence from the
archive transaction. Any additional path, content-identity drift, remote drift,
or archive-commit drift blocks without changing state.

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
immutable plan changes. Both cross-month and pre-PR provenance
`reprepare_required` replace the plan and therefore re-enter confirmation.

## Immutable Preview And Transaction

Preview shows repository, base, branch, `branch_review_commit`, separate
`reviewed_content_head` and `publication_head`, reviewed-content identity, task, archive locator,
upstream evidence references, verification requirement, metadata paths, PR
identity strategy, complete side effects, plan digest, and the exact canonical
plan bytes. Formal execution rebuilds the same bytes and digest before any side
effect. Drift blocks.

For every prepare and same-plan recovery, `tracked_move_paths` is rebuilt from
the live Git index and `untracked_archive_outputs` is its exact complement in
`move_paths`. The only legacy closeout-plan path accepts a complete schema 2.0
plan together with a current Publication 4.0 DTO whose task, commit, title, body
digest, and protected facts match. It rebuilds schema 3.0 from the DTO payload,
records the exact predecessor plan digest, and never reads the retired body or
summary-index files. Every other retired shape fails closed and requires
Publication re-entry. The immutable projection binds every tracked move
path whose current regular-file bytes or mode differ from its
`branch_review_commit` blob with one sorted task-relative `path`, Git `mode`,
and SHA-256 row. Duplicate, out-of-set, stale, missing, or unnecessary rows
fail closed. The plan file itself is the only self-referential exception: when
legacy Git already tracks `closeout-plan.json`, its current bytes are bound by
the plan's canonical schema and `plan_digest` rather than a recursive raw-file
SHA-256 row.

The immutable plan stores the exact reviewed `publish.title` and `publish.body`.
Same-plan recovery, Draft convergence, remote validation, and archive recovery
reuse those exact values and never read a Publication file or checkpoint.

Pre-move continuity, verification fallback, archive movement, and post-move
continuity consume that same projection. A tracked metadata tail is accepted
only while its mode and bytes exactly match its binding; an unbound difference
from the transaction parent remains blocked. Metadata intermediates selected
by the existing archive pruning contract are validated and moved first, then
explicitly pruned.
Archived recovery likewise accepts `closeout-plan.json` only when the same
projection classifies it exactly once, in either `tracked_move_paths` or
`untracked_archive_outputs`; it does not restore the new-task-only untracked
assumption after the archive commit.

The deterministic order is fixed:

1. Build and prevalidate the immutable plan.
2. Verify that current HEAD preserves the reviewed-content identity, then push that exact current HEAD.
3. If required, stop before PR/archive and emit `verification_required` carrying
   both reviewed and publication HEADs. The verifier targets publication HEAD
   while source provenance remains bound to reviewed content.
4. When the plan requires extension verification, consume same-plan verified
   evidence. A plan whose current reviewed paths require no extension
   verification continues without manufacturing a `not_required` handoff.
   The current plan does not create or push a separate evidence-metadata commit; its
   archive transaction remains a direct child of `publication_head`.
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
schema 3.0. In a new task, `closeout-plan.json` and `finish-summary.json` begin
as untracked active transaction outputs and become tracked in the single
archive commit. A migrated task may already track legacy `closeout-plan.json`;
the live Git index then classifies it as tracked throughout normalization,
continuity, movement, and archive commit, while `finish-summary.json` remains
the required untracked output. `pr-readiness.json` and
`task-finalization-gate.json` never enter move paths, evidence paths, or the
archive. The Publication wrapper deletes `pr-readiness.json` after validating
its own typed output, before Finalizer entry. The Finalizer retains only its own
checkpoint across same-plan recovery and deletes it after the terminal public
`published` projection is validated.

The archive contains exactly the durable files that exist from this seven-file
set: `task.json`, `prd.md`, `design.md`, `implement.md`,
`issue-scope-ledger.json`, `closeout-plan.json`, and `finish-summary.json`.
When marketplace verification applies, `marketplace-verification.json` is the
only optional archive file, so the archive contains at most eight files.

Intake/context snapshots, assignment or liveness state, commit plans, raw
review rounds, `review.md`, and `pr-readiness.json` are current-step inputs or
reconstructible facts and are not copied into the long-term archive tree. A
crash after move and before or during pruning re-enters the same idempotent
pruning step.

## Recovery

- Stale Publication DTO content identity, or missing/stale current Publication
  evidence -> `publication_review_stale`, carrying the exact stale
  `branch_review_commit` for Publication re-entry. If current Finalizer facts
  cannot supply that Git anchor, fail closed instead of inventing one.
- Content pushed with verification pending -> `verification_required`.
- Same-plan transient executor failure, draft-to-ready retry, interrupted
  active/archive move, or exact-commit continuation -> `resume_finalization`.
- Active task with a changed archive month -> `reprepare_required` with
  `archive_month_changed`; retire the old private plan/evidence, preview a new
  plan, and obtain fresh current side-effect confirmation. If either candidate
  is already tracked task content, fail closed before deletion.
- Pre-PR verification rejected only because the reviewed checkout provenance
  is stale -> `reprepare_required` with `provenance_tail_required`; generate or
  reuse the one allowlisted provenance tail, retire the old private
  plan/evidence, preview a new plan, and obtain fresh confirmation. A pre-#191
  schema 3.0 predecessor is accepted only when its exact legacy
  `verification_required` gate/request, task/repo/remote/base/head identity,
  active/no-PR/no-archive/single-consumer state, untracked artifacts,
  old-to-current reviewed ancestry, and fast-forwardable remote ancestor all
  remain current. Publication proves this without mutation; the checked
  Finalizer transition repeats the proof, retires the old state, creates or
  reuses the tail, and persists the fresh replacement plan. Other
  verification failures remain blocked. Tracked task artifacts are preserved
  and block this automatic cleanup path.
- Missing, closed, replaced, or ambiguous draft identity; unstable
  repo/head/base/HEAD/number/URL/Draft identity; unexpected path;
  invalid private state; or HEAD mismatch -> `blocked`.
- A completed ready recovery -> `published`.

`resume_finalization` is legal only from `content_pushed` with current verified
or not-required evidence, `evidence_ready`, `draft_bound`,
`projection_validated`, `archive_moved`, `archive_pushed`, or `archived`.
`prepared`, `reprepare_required`, stale state, and terminal `ready` never select
same-plan resume.

Recovery never exposes the private transition labels `prepared`,
`content_pushed`, `evidence_ready`, `draft_bound`, `projection_validated`,
`archive_moved`, or `archive_pushed`. Users do not choose internal recovery
commands.

Workflow mode automatically consumes every non-terminal recovery exit.
`verification_required` is never rendered as a user-visible status or choice.

## Public Inputs

The six closed profiles are:

- `publication_ready`: `profile`, `mode`, `task_ref`,
  `branch_review_commit`, `pr_title`, and exact UTF-8 `pr_body` from the current
  Publication owner output.
- `verification_verified`: the minimal #117 verified seed; no routine re-entry
  intent is authored.
- `standalone_verification_not_required`: the reachable task-bearing #117
  standalone seed `repo_ref/resolved_head/verification_ref` plus target-authored
  `profile/mode/task_ref`. The finalizer loads the private current plan and
  task-local owner evidence instead of publishing `plan_ref`.
- `same_plan_resume`: task/plan seed plus target-owned `profile` and `mode`.
- `reprepare_preview`: task/reason plus the producer-supplied
  `branch_review_commit` and `publication_head`, followed by target-owned
  `profile` and `mode`. This is the complete identity needed to rebuild a plan
  after the superseded plan and gate have been removed.
- `standalone_finalization`: `profile`, `mode`, and `task_ref` only.

Producer seed fields and target authoring fields are disjoint. Their union
equals the target profile required set. Runtime performs a no-overwrite merge
and never invents task identity, verification judgment, or owner evidence. The
standalone not-required binding requires the owner evidence,
repository, resolved HEAD, verification ref, task, and private plan to remain
current; same-plan recovery reuses that private binding.

## Public Exits

- `verification_required`: task, plan, repository, `branch_review_commit`,
  `publication_head`, and verification target; `repo_ref` is exactly the
  immutable plan repository; consumed by `guru-verify-extension-installation`.
- `publication_review_stale`: task, the exact stale `branch_review_commit`, and
  stable stale reason; consumed by `guru-review-task-publication`.
- `resume_finalization`: task and same plan; consumed by this Skill.
- `reprepare_required`: task plus `archive_month_changed` or
  `provenance_tail_required`, `branch_review_commit`, and `publication_head`;
  consumed by this Skill's reprepare profile. Archive-month recovery retains
  that already-current DTO in its gate because HEAD does not change. Provenance
  recovery retains a private marker until the deterministic executor has
  created or reused the tail, retired the old owner-private plan/gate/request,
  persisted the fresh replacement plan when base evolution superseded a
  pre-#191 predecessor, and can return both heads. Schema 2.0 output and schema 3.0 input add the
  provenance reason and direct-consumer identity while preserving the existing
  archive-month value.
- `published`: the exact plan archive locator and canonical PR number/URL;
  consumed by the Finish response.
- `blocked`: closed reason and remediation; consumed by the finalization stop.

Every DTO uses `exit_id`. Gate, plan, review, verification, PR, archive,
recovery, digest, path, blob, and unrelated Git HEAD facts remain private.

### Publication-head public I/O migration

The four pre-#191 public DTO schemas remain immutable compatibility assets:

- `guru-finalize-task-output-verification-required-2.0` at
  `schemas/public-verification-required-output.schema.json`;
- `guru-finalize-task-input-verification-verified-3.0` at
  `schemas/public-verification-verified-input.schema.json`;
- the corresponding Verifier input 2.0 and output 2.0 schemas in the consumer
  package.

Those legacy schemas keep their original bytes and do not contain
`publication_head`. The current Interface selects Finalizer output 3.0,
Verifier input 3.0, Verifier output 3.0, and Finalizer publication input 4.0.
Finalizer's current aggregate input is 5.0; aggregate 3.0 and the #191 aggregate
4.0 remain immutable compatibility assets. The executable current handoffs are the Interface
`project_verification_required` and Verifier `project_verified` projections:
each selects `publication_head` without renaming or defaulting it, merges only
the target-owned profile/mode authoring fields, and validates the result against
the current target schema.

A legacy DTO is validation-only compatibility evidence, not a current route.
Because its producer did not bind publication identity, the consumer must not
infer `publication_head` from `branch_review_commit`, live HEAD, or private
state. A current invocation receiving a payload that satisfies only a legacy
shape fails current-schema validation and re-enters the owning current producer:
Finalizer rebuilds the current plan/output before Verifier entry, and Verifier
reruns exact-ref verification before Finalizer re-entry. Package tests preserve the legacy byte
digests, validate legacy and current examples against their own schemas, reject
both cross-version substitutions, and execute both current projections against
their target schemas.

The ignored owner-private gate never stores an early public `published` DTO or
an early provenance-reprepare DTO. Those transitions retain the exact
finalizer-private executor marker while their output identity does not yet
exist. Archive-month reprepare changes no HEAD and retains its complete current
DTO. Recorder/checker and executor validate the corresponding form. The public
wrapper reruns strict route validation and never executes a publish/archive
transition; only after the exact archive transaction and ready PR facts are
proven may it materialize the `published` DTO in memory using the plan archive
locator. It never materializes reprepare after execution because that executor
retires the old gate and returns the DTO directly. The Publication checkpoint
is neither read nor consumed by this path; its minimal `ready` DTO was consumed
at entry. The next reprepare preview validates current HEAD and the optional
single-tail parent/allowlist contract without reading the retired plan.

## Script Boundary

Package scripts are dispatcher-only wrappers. Runtime commands may:

- preview through the existing closeout engine;
- record/check the private semantic gate;
- execute one checked deterministic transition through the same engine;
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
