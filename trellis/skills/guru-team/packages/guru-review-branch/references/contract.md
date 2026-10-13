## Public Delivery integration 1.0

This current Skill consumes the target installation's reviewed Delivery API
1.0 and Task schema 2.0 through a thin projection. `task_ref` is a locator;
`delivery_key` is the opaque public identity. Read the current `interface.json`
profile schema and its exact exit consumer before invoking. Do not derive an
identity from branch, worktree, legacy cycle, PR, or Task status. D1 and later
Deliveries use the same entry and lifecycle. The public phase never proves a
semantic pass. Historical facts never prove a currently applicable gate.

Read the Delivery's public `planning_root` for its three planning documents and
context JSONL; Task-root PRD remains overall scope. Rework keeps the Delivery
identity and returns through the real current stage owner's public operation to
the earliest affected role. Invalidate only the affected results. Unchanged,
still-applicable execution facts need not be rerun. A successful recorder is
objective evidence only; the AI must actually perform this Skill's full review.
Missing public API or an unmigrated old record stops with precise migration
remediation. Do not install a private alternative, select a source fallback,
convert a legacy checkpoint into pass, or switch an old installation before
upstream migration/default-cutover qualification.

### Independent Review and continuity

Use `delivery_branch_review` with current Check result, committed candidate and
complete base-to-HEAD range. Retain independent findings, scope proposals,
Architecture promotion/fresh final review, and qualification duties. Passed
Review records public `full_review`, handing its exact result ID to Readiness.
After local checkpoint consumption, lost stdout recovers only the actually
recorded applicable public result with matching predecessor/candidate/producer.

`delivery_base_continuity` keeps the exact prior full Review, integration pair,
current reconciled HEAD/tree, relevant paths and declared resume target. A
continuity conclusion is not a new full Review pass. `delivery_archived_review`
reviews actual archived content and payload separately; it does not write a
current Delivery gate or reset historical phase. Legacy archives remain history
until their original migration owner resolves a public identity.

### Scope withdrawal in the current stage

`delivery_scope_withdrawal` is an independent semantic entry with mode,
`task_ref` and `delivery_key`. Before authoring its separate review input,
read the current whole-scope decision and selected undelivered slice; judge
that its full scope was withdrawn/replaced, with no remaining obligations in
that slice. Partial changes use ordinary same-Delivery rework. This package
uses only its fixed public role and expected phase; it never accepts a role
parameter or selects an owner from phase. Record the actual reason,
`scope_decision` and minimum evidence through public `stop`, then release the
selection. `delivery_stopped` hands Task identity to whole-task Completion.
Stop preserves commits/PR/resources; PR close and cleanup require their actual
owners and any necessary current side-effect confirmation. Lost output retries
the identical stored stop result and releases selection without another stop.

## Preserved semantic and transaction duties

The duties below apply to the current Delivery input and output contracts.
Historical data is read only by its named history or migration owner.

# `guru-review-branch` Contract

GitHub review/check/mergeability facts use the shared authenticated,
repo-bound `gh` adapter in `.trellis/spec/workflow/workflow-contract.md`; they
remain evidence for, not substitutes for, this Skill's semantic judgment.

## Actual Candidate Set

Complete the selected profile's semantic review before forming the actual
candidate set. When that complete review finds no real candidate, record
`candidate_classifications=[]` and invoke none of the three nonempty-only
qualification owners. Do not invent a no-defect candidate from a reviewed file,
feature, or a passing check. An empty set does not establish `passed`,
`continuity_passed`, or `archived_review_passed`: every applicable entry,
Architecture, Docs, range, dimension, evidence, freshness and route condition
still applies. Bounded continuity remains bounded and archived review read-only.

When real candidates exist, invoke the existing normal-scenario and
solution-mechanism owners, then root-cause qualification for eligible refs,
using `branch_review_candidate_set`. Keep every actual terminal classification,
witness and semantic disposition. Nonempty all-rejected candidates are distinct
from no candidates. Every finding, proposal, observation, follow-up and rejected
candidate still binds a classified ref; an empty set cannot carry such a row.

## Entry

### Archived Review

The independent `delivery_archived_review` reads the exact archive, actual
current-generation Completion/Closure and selected Delivery planning_root.
It requires committed plans/summary, completely clean checkout, exact registered
branch, selected local/live base, one current Open Ready PR and current payload
snapshot. It does not consume current Check or write active Delivery gates.
Independently review full archived range, requirements, Architecture and tests;
findings or insufficient authority return blocked without repair or mutation.

The independent private schema `guru-review-branch-private-delivery-archived-gate-1.0` (version
`archived-1.0`) binds the current B, A, PR identity and snapshot to the freshly
authored semantic result. Its only outcomes are `archived_review_passed` and
`blocked`. A pass forbids open findings and scope proposals. A blocked result
preserves actual open findings or proposals instead of relabeling them as
external failures, and never routes to restoration or implementation.
Existing recorder/check/invoke commands validate this new variant and retire
it on either successfully projected exit. Ordinary schema 7.0 remains exact
and does not accept this new variant or change its blocked semantics.

The `archived_review_passed` DTO contains task_ref, branch_review_commit A,
pr_payload_snapshot_sha256 and reviewed_base_head B, plus exit_id. Its sole
current consumer is the `legacy-archived-review-disposition-required` stop.
It is read-only historical evidence, not a seed for Delivery, Completion or
Reactivate. The old Publication consumer is available only in a pinned old
graph; it is not invoked from the current graph. Full review bodies, findings,
private checkpoint and the PR number remain private.

### Ordinary Entry

Use `delivery_branch_review` with current Check, exact committed candidate,
base and initial/fresh-final intent. The current TaskCommit consumer supplies
identity only; live Git and public Check establish actual content applicability.

Workflow and standalone mode use the same eight preconditions: runtime,
workspace, task identity, the committed DTO plus live Git, the current Issue
source Issue identity, complete review range, working tree, and invocation freshness.
The Skill reads the Delivery plans and actual public Check predecessor,
not Phase 2 private evidence or a Task Commit candidate.
Input that does not satisfy the current public schema fails closed.

Before the full-range review, the global workflow mandatory invokes
`guru-maintain-architecture-baseline:delivery_task_impact_sync(stage=branch_review)`.
That semantic owner independently reruns applicable project Architecture checks
and recomputes before/after satisfaction from the complete committed
base-to-HEAD diff. Branch Review consumes only its fresh checked current route,
then rereads the live Architecture Baseline, design-constitution authority, and
task-local Architecture change contract. It never opens Architecture private
state; this consumer does not read Architecture private state and never treats
the Phase 2 Architecture result as current Branch Review evidence.

Apply the Architecture contract's Independent assessment entry to a new fresh
reviewer for this committed candidate. A compliant worker may perform
Architecture first and this complete review afterwards; do not dispatch a
narrative-preloaded overall worker and ask it to retroactively author the
Architecture pass. Actual results and exact committed identities stay separate.

### Whitespace Candidate Hygiene

An extra blank line at end of file, including multiple blank lines after the
last meaningful line, is formatting noise rather than a Branch Review finding
when it is the only observed issue and the file's meaningful bytes are
unchanged. Keep it as a non-blocking observation and do not assign severity or
route it to implementation. This exception is deliberately narrow: trailing
spaces on non-blank lines, indentation changes, whitespace inside strings or
configuration values, invalid encoding, and whitespace that changes a
parser/linter/formatter contract remain reviewable candidates.

Every official independent-review worker is invoked with a prompt that
authorizes approved-plan work only. If it observes a planning-external
candidate, it stops before any edit, added test, self-fix, severity,
classification, or route and returns only the invocation-local
`candidate_ref`, `observed_behavior`, `locators`, and
`minimal_reproduction_hint`. The Guru owner rereads the live range and
authority and completes fresh `branch_review_candidate_set` qualification
before continuing or redispatching work for that candidate. Official
`trellis-*` agent files remain unchanged and upstream-owned.

The independent current-only `delivery_base_continuity` profile is entered
only from `guru-reconcile-task-base:review_continuity_required`. Its
`branch_review_commit` is the prior full Branch Review commit and its
`task_head` is the current committed reconciled HEAD. The recorder requires
`task_head == HEAD`, requires the prior review commit and `new_base_head` to be
ancestors of that HEAD, and recomputes the committed tree identity to match the
exact `candidate_tree_sha256`. The profile also binds one exact
`old_base_head...new_base_head` pair, relevant paths, and original resume target.
It reviews only that bounded integration surface; it does not rewrite or replay
the task-content review and its success is not a full Branch Review.

The committed-tree reader consumes the candidate row representation defined by
[`guru-reconcile-task-base`](../../guru-reconcile-task-base/references/contract.md#candidate-and-script-boundary).
It includes `160000`/`commit` gitlinks using their recorded path and OID without
reading child objects or initializing submodules. Blob-backed rows and existing
recorder/checker identity comparisons remain unchanged; this consumer does not
define a separate algorithm or rewrite the producer's candidate token.

## Semantic Review

Before full-range Docs, code, test, fixture, consumer, or history retrieval,
read `.trellis/spec/workflow/semantic-retrieval.md`. Use its minimal concept
family and evidence-coverage bar during candidate qualification, including
before any negative existence or impact conclusion. Search transcripts and
query metadata remain transient and never enter the gate or public handoff.

Independently apply
`.trellis/spec/workflow/quality-guidelines.md#test-and-validation-value` to the
tests, validation gates and proof claims in the complete committed review
range. Check the actual entry, observed behavior and defect detection against
live requirements; neither Phase 2 approval nor passing commands settle test
value. Keep bounded continuity review within its integration surface and
archived review read-only. Qualified current-scope defects and evidence gaps
use the profile's existing finding or blocked routes and existing gate fields.

Perform one independent semantic review of the complete current
`origin/<base>...HEAD` range. For a nonempty actual candidate set, invoke
`guru-qualify-normal-scenario:branch_review_candidate_set` before assigning
severity. Candidate input carries no decision, scenario class, severity,
expected route, or caller assertion of a normal path. Only candidates returned
eligible through `classified` may become a P0-P3 finding.

Before a revision, test, severity or route, independently establish the problem,
the current goal/affected contract that requires fixing it, and mechanism
suitability through both existing qualification owners. Necessary local
refactoring, consumer adaptation and old-path exit remain required; unrelated
historical debt is not automatically a current finding, gate or follow-up.
Task scope does not negate an evidenced Architecture violation, and finding
one does not authorize changing goals or authority. Green tests, prior approval
and reviewer advice are not necessity evidence.

Attribute red tests with bounded evidence to regression, inseparable current
prerequisite, unrelated history, environment or unresolved cause. Stop repair
and investigation when unrelatedness is established; do not claim unresolved
failures are historical or widen scope to achieve full green. A required
release gate may block publication without authorizing unrelated repair. Bind
legal non-default configuration and protection invariants to their authority;
defaults/recommendations and missing diagnostic labels do not become business
rejection conditions.

For a full `branch_review`, independently bind the approved Delivery slice,
explicit remaining work, observable independent-delivery conditions, and
validation boundary to the complete committed range. Remaining work outside
the current slice is not a current omission, but hidden remaining work, a
current-slice defect, or a slice that depends on the remaining work already
being complete prevents `passed`. This compact semantic evidence remains in
the private gate and does not expand the existing `passed` DTO.

A resolved-tree reconciliation that returned through fresh Phase 2 requires
this complete full-range review after Reconcile creates or recovers the exact
merge commit. The `base_continuity` profile cannot replace that review: bounded
base continuity is not used for a conflict-resolved tree containing task
adaptations.

For delete, replace, merge, or compatibility-impacting ranges, independently
recompute `code_subtraction` and `docs_ssot_subtraction` using the durable
subtraction-first policy. Check direct evolution, affected deprecated-asset
exit, real supported consumers, current compatibility contracts, and
category-specific reasons for growth. A non-server compatibility mechanism not
specifically approved in the current conversation before coding, compatibility
tests, or self-fixing remains unsupported; it cannot be justified by a generic
safety or compatibility statement.

The review lifecycle is visible in the current dialogue. Immediately before
dispatch, the caller presents the independent reviewer identity, exact
committed `origin/<base>...HEAD` range, and review target. Immediately after
return, it presents the final finding summary and the semantic owner's
conclusion. These notices and the reviewer transcript are transient dialogue
context only; they do not enter the gate, public DTO, private checkpoint, or a
tracked review report.
`scope_confirmation_required` enters requirements clarification;
`mechanism_revision_required` returns to task work for remove/replace and a
fresh complete review; `blocked` stops. Rejected or disproved candidates remain
non-blocking observations and cannot become scope confirmation, negative tests,
implementation, follow-up, or publication blockers,
follow-ups or rejections.

The complete-range review independently checks that the committed diff and any
task-owned contribution agree with the current constitution, change path,
required project checks, before/after state, GAP and owner transitions, and ADR
trigger decision. Missing or stale Architecture identity routes
`sync_required`; missing applicable contract/check facts route
`contract_incomplete`; `architecture_conflict` returns to Planning; and a new or
worsened deviation routes `fitness_regression` to implementation/check. These
routes remain owned by `guru-maintain-architecture-baseline` and the global
router, not by this package's five Branch Review exits.

Return `implementation_required` for an open current-scope finding. After its
fix passes Phase 2 and a fresh commit, run one internal closure judgment by the
finding owner or, only after a real unfinished event, a replacement. Retain the
original `introduced_head`, bind the fixing `fix_head`, bind a later
`closure_head`, and carry only concrete closure evidence into the next
judgment. The distinct fresh-final result records `review_commit`. These commit
anchors intentionally differ across a normal fix and closure sequence;
ancestry, not equality, proves finding continuity.

Closure has no public exit, recorder call, or artifact. The AI workflow
immediately dispatches a distinct fresh reviewer over the complete current
range. That reviewer consumes the transient closure result, authors one
`fresh_final_review`, and is the only reviewer whose compact passing gate is
persisted. A closure reviewer never also performs the fresh final review.

An Architecture promotion diff follows the same rule: it returns through fresh
Phase 2 Architecture/check, a new task commit, and an independent complete-range
Branch Review. Only that post-promotion review can support the later Delivery Review
Architecture stage; no pre-promotion Branch Review or Phase 2 conclusion is
reused.

Mapped finding-fix, stale, re-entry and final-review routes continue within the
AI workflow. They are not user choices. A user prompt remains only for real
scope/authority decisions or a separately displayed Git/GitHub side effect.

## Current constitution consumption

Independently apply `minimum-necessary-complexity` from the unique current
project authority to all added capabilities in the complete committed range,
including public contracts and abstractions. Consume task-applicable
conclusions and current evidence; do not copy principle prose or reuse Phase 2
approval. Current responsibilities and all applicable contracts govern the
necessity judgment, including when functional tests pass.

Qualify concrete observations through existing Branch Review profiles before
severity or findings. `mechanism_revision_required` returns through the
existing mechanism router for remove/replace, preserving accepted scope and
requiring a fresh complete review. A requirement-authority conflict re-enters
the Architecture owner and its `architecture_conflict` Planning consumer,
then existing clarification when source scope changes; review again against
the revised current authority. Missing applicable evidence uses
`contract_incomplete` or existing blocked handling. A real scope choice uses
`scope_confirmation_required`; an open qualified current-scope finding uses
`implementation_required`. These are existing distinct owners and routes.

Neither an approved requirement, future-related word, nor functional-test pass
alone settles the observation. Never silently delete accepted scope. Keep
applicable evidence in existing finding/gate fields without per-capability
records, scores, keyword classifiers, public DTO growth or new exits.

## Causal committed review

Read `.trellis/spec/workflow/causal-completion-semantics.md` and independently
apply it to the exact full committed range and real consumers. Inspect
implementation-time additions, fixture/filter/default/error assertions, known
first failure, sample completeness and failure redistribution. Current
qualification applicability informs the review; Phase 2 pass does not replace
it. Unknown cause alone creates no diagnosis/mitigation finding. Preserve
protection supported by current authority and actual ownership.

Committed mechanism deviations use `implementation_required`; a genuine change
to accepted product scope uses `scope_confirmation_required`. Evidence gaps
are stated at their actual layer and handled under the existing profile's
contracts, without turning mitigation or a test pass into a repair claim.
Bounded continuity remains bounded; archived review remains read-only.

## Gate And Exits

After the AI gate exists, `review-branch` writes one compact owner-private
`review-gate.json` at
`.trellis/.runtime/guru-team/owner-checkpoints/<task-key>/<delivery-uuid>/review-gate.json` and
returns only a minimal task/exit/checkpoint receipt. The task owner and package
resolver determine the path; callers cannot choose a gate locator.
`check-review-gate` resolves that exact checkpoint and validates
objective structure, task/base/reviewed-content identity, complete range, finding
lifecycle, fresh-final intent, facts digest and exact consumer. It never
decides review sufficiency, severity or route. The checker recalculates
`guru-reviewed-content-1.0`: excluded task/runtime metadata may change without
staling the gate, while any reviewed-content change makes it stale. Git commit
anchors remain responsible only for review range and finding ancestry.

The current gate schema directly records this Branch Review owner's final
candidate classifications and, for every candidate, the direct-consumer witness
`requirement_refs`, `supported_entry_refs`, `existing_caller_refs`,
`honest_action_sequence`, `defect_observation`, and `excluded_assumptions`.
It never stores or points to qualification stdout, a result/report, a temporary
locator, or a qualification checkpoint. Legacy gates are stale and require a
fresh complete Branch Review.

The Branch Review public wrapper accepts current public input only, internally
reruns `check-review-gate`, validates the selected output schema and never
accepts caller-authored gate or checker output. The semantic owner's passing
conclusion is provisional. The caller may use the formal wording "Branch
Review passed" only after both the official checker and the public wrapper
return `passed` for the same current task, committed range, review commit, and
reviewed-content identity. A recorder receipt, provisional owner conclusion,
or checker result without the wrapper result cannot support that announcement.
The checker returns `status=owner_checkpoint_validated` and
`formal_exit=false`; it is objective checkpoint evidence only, never a Branch
Review result.
Successful `passed`,
`continuity_passed`, and zero-payload stop `blocked` projection deletes the
checkpoint and empty owner directory. `implementation_required` and
`scope_confirmation_required` retain the same checkpoint for their mapped
same-owner re-entry; a
duplicate invocation deterministically returns the same DTO and creates no
second state. Delivery Review receives only the minimal typed DTO and live Git
facts; it never reads or deletes Branch Review private state. A failed checker
or invalid projection retains the checkpoint for same-owner repair. Missing
after retirement, wrong-task/base/HEAD/content, unsafe components, and symlink
ancestors or gate files fail closed.

The current Delivery private gate uses `guru-review-branch-private-delivery-gate-1.0`
with schema_version 7.0, public key and Check predecessor plus profile-specific identity,
`review_commit`, `reviewed_content_algorithm`, `reviewed_content_sha256`, and
the final terminal candidate-classification witness required by its direct
consumer. For `base_continuity`, `review_commit` equals the current committed
`task_head`; the integration pair separately retains
`prior_branch_review_commit`, current task HEAD, exact old/new base pair,
candidate tree, relevant paths, and resume target. Aggregate input schema 3.0,
base-continuity input/output schema 1.0, and gate schema 6.0 or older remain
legacy stale inventory, not current runtime authority. Runtime never dual-reads,
rewrites, or migrates them.

Return exactly one of:

- `passed`: minimal `task_ref`, `delivery_key`, `full_review_result_id`,
  and `branch_review_commit` seed for
  `guru-review-task-delivery`, only after the current Branch Review-stage
  Architecture result passes independently;
- `continuity_passed`: current Delivery output projects the public key, exact pair and
  candidate identity to the workflow-owned `guru-base-continuity-passed-router`,
  sets `branch_review_commit` to the current continuity-reviewed `task_head`,
  and resumes the original target without claiming a full Branch Review;
- `implementation_required`: public key, `branch_review_commit` and current finding refs;
- `scope_confirmation_required`: public key and exact proposal refs;
- `blocked`: stable reason/remediation only;
- `delivery_stopped`: Task locator and TaskKey for whole-task Completion.

Unknown, multiple, stale, unmapped or consumer-mismatched results fail closed.

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
