# Evolution Test Strategy

状态：`test_candidate_planned` / `fresh_design_review_passed` / `evolution_refactor_eligible`。This strategy verifies the target contract without confusing docs, static
closure, runtime behavior, installed behavior, external facts or Release proof.

## 1. Evidence Layers

| Layer | Proves | Does not prove |
| --- | --- | --- |
| `static_contract` | ids, schemas, tables, links, graph closure, exact owner/consumer and projection inventory | AI semantic sufficiency or runtime behavior |
| `semantic_eval` | representative honest inputs produce the right scope/finding/route/revision decision | side-effect execution or installed parity |
| `package_runtime` | validators/executors, call/host-session-local envelope, task-local same-owner checkpoint boundary and producer-consumer transitions behave for the exact source candidate | host projection or external provider |
| `workflow_integration` | one invocation follows the declared owner graph, freshness and re-entry without duplicate work | clean/existing installation across hosts |
| `projection_installed` | canonical/dogfood/installed/shared/host bytes, modes, graph, stock action and sidecar behavior | an unexecuted matrix cell or remote outcome |
| `controlled_provider` | Git/GitHub/Trellis provider inputs, receipts, partial/unknown outcome and forward recovery under a controlled target | production or immutable Release facts |
| `live_external` | exact remote PR/Issue/tag/Release state after authorized action | any other candidate or environment |
| `release_exact` | immutable exact-candidate pre-publish, publication and tag-pinned post-publish proof | future-version compatibility |

An upper layer does not replace a lower semantic contract, and a lower layer never claims an upper-layer result.
Missing credentials, unsupported host/provider or unavailable external state is `skip_unverified`/`blocked`, not
pass.

## 2. Candidate Binding

Every executed fixture binds:

- `fixture_id`, candidate kind and exact source/commit/tree or installed/release identity;
- applicable Requirements, Design and public contract identities;
- owner/profile, direct consumer and expected typed terminal;
- dependency identities used by the call/host-session-local envelope or an allowed task-local same-owner checkpoint,
  plus their current/stale classification and direct consumer;
- evidence layer actually executed, observed actions and explicit unverified boundaries.
- for standalone verifier failure only, the pre-cleanup stage/cell/command/exit/safe-tail/hash-size evidence identity
  and the subsequent cleanup/blocked/re-entry observation; embedded callers do not inherit that verifier lifecycle.
- for installed provenance preparation, the parent manifest's three exact selected lists plus `all_platforms`, the
  projected provider argv, parent/post-reprepare set equality and the pre-extension-source-checkout/apply/commit
  failure observation; this remains part of the existing installed-publication fixture identity.

Equivalent identity refresh may reuse unchanged semantic work only after live comparison. Material scope,
authority, package, projection, provider or candidate change invalidates the earliest affected result and all
downstream evidence. Results from a different candidate are never promoted by relabeling.

## 3. Fixture Execution Contract

Each row in `fixture-plan.md` is one fixture family, not one assertion. A future implementation Issue expands only
the profiles/cells required by its accepted slice. Every applicable family must include:

1. one supported normal success path;
2. ordinary honest-but-fallible stale/missing/mismatch or provider failure relevant to the contract;
3. the declared typed blocked/re-entry result and exact repair/resume input: every ordinary recoverable block must
   match exactly one `contracts.md` Section 7.1 producer/profile row, while declared specialist/terminal exceptions
   must match their separate closed contract;
4. proof that completed actions are not repeated and unaffected work is not rerun;
5. zero forbidden owner, route, artifact, read or side effect where the Requirements define a zero count.

No adversarial artifact forgery, malicious bypass, lock/TOCTOU stress, crash-consistency injection or arbitrary
cross-OS hardening is added unless a future accepted requirement explicitly adds it.

## 4. Semantic And Deterministic Responsibilities

- Semantic fixtures provide evidence to the AI owner; a script exit code cannot decide intent, scope, sufficiency,
  finding severity, revision action, route, approval or Architecture/RDT meaning.
- Deterministic checks may validate closed ID sets, JSON/schema, exact path/mode/HEAD, typed exit mapping,
  activation identity and objective action state.
- Every public Skill edge validates its selected output against the consumer-owned input using only
  `direct|select|rename|normalize`. A consumer-owned live fact must be absent from caller-authored input and resolved
  through its exact envelope section owner; generic frames, implicit pass-through, private checkpoint/envelope-file
  reads, ambient Git lookup and runtime-source interpretation all fail the contract fixture.
- Admission/pre-route/pre-task/task-free/standalone fixtures require call/host-session-local continuation and zero
  generic repository envelope/checkpoint path or write. Missing/stale continuation must reach the exact owner's
  existing block/re-entry and live reconstruction. Once a task is current, any allowed ignored checkpoint has one
  exact same-Skill public-wrapper consumer and is never readable by a downstream Skill.
- Admission fixtures keep lifecycle causality/identity failure (`binding_blocked -> binding_reentry`) separate from
  post-receipt isolation failure (`independent_request_isolation_blocked -> isolation_repair_reentry`). Post-owner and
  post-remote pending intents enter only their two fresh Admission profiles; isolation recovery reuses the existing
  envelope and receipt. `lifecycle_bound` must carry `bound_event_ref,event_sequence`; the ref binds the host event
  identity/session and current content, and the router projects both fields directly to the registered owner's exact
  `lifecycle_intent_reentry`. Bound-intent/current-work routing accepts only the closed Section 3.1 owner registry and
  its exact `lifecycle_intent_reentry|current_work_resume` profile, never a generic matching owner/profile or an
  ambient host-history lookup. That registry contains exactly 37 lifecycle owners, including Admission, Route Request,
  Answer, Current Work and History; Wording and Qualification are the only two public specialist non-owners, and their
  fixed original caller retains lifecycle ownership.
- Authority fixtures prove three distinct `authority_context` subprojection owners: Clarification owns current
  requirement-delta/reviewed-design binding, RDT owns repository RDT, and Architecture owns baseline/constitution/
  change contract. Applicable Plan/Approval/Implementation/Check/Review/Readiness/Acceptance owners judge the same
  stable bound authority content directly; a minimal public projection or producer summary cannot replace that
  content or create a second source-reading chain.
- Direct-answer fixtures distinguish terminal answer-scope/profile/consumer binding failure from a controlled
  adapter's recoverable provider boundary. The latter is promoted to Answer-owned `answer_provider_blocked` and may
  re-enter only Answer `provider_reentry`; provider unavailability/access denial/incomplete facts remain truthful
  `answered` results with an unverified boundary. `trellis_reference` must select
  `guru-trellis-reference-manifest-1.0` by its official-doc/local-runtime/package-snapshot precedence and call only
  the standalone Answer profile of `guru-trellis-reference-read-adapter-1.0`; a write intent must enter active/
  new-change routing before adapter invocation, with raw `trellis-meta` calls at zero.
- Qualification scope fixtures must pass an opaque caller continuation through the profile-fixed Clarification
  owner, obtain a real scope choice, return to the original caller, rebuild the complete candidate set and freshly
  qualify. Ten active qualification profiles cover all four results; standalone covers only
  `classified|scope_confirmation_required|blocked`, and its mechanism-revision result/profile is invalid. Bootstrap
  fixtures independently bind RDT and Architecture caller continuations and return only to that authority owner's
  `bootstrap_reentry`; router origin inference and direct Clarification-to-Qualification shortcuts are invalid.
- Wording fixtures must cover the one standalone and four active content callers through all nine closed producer
  profiles. Pass, revision, content-changed and blocked outputs must return the unchanged caller continuation to the
  exact `wording_*_reentry`; arbitrary active callers, generic caller ids and direct router completion are invalid.
- `guru-finalize-task` is semantic because it consumes the exact Draft/READY PR and publication head, owns the
  summary/official-archive/archive-commit-and-push/Ready plan and confirmation boundary, and alone emits the
  archive-bound `ready_for_merge_ref`. Its transition executor records `completed|pending|unknown` deterministically;
  Merge, Closure and Cleanup remain later semantic owners and cannot consume the Finish confirmation.
- Plan fixtures treat `phase-1-task-activation` only as the deterministic substep inside
  `guru-approve-task-plan` after current semantic approval and confirmation. The one displayed exact next-action plan
  includes both task activation and immediate entry into the approved implementation scope/allowed writes, while
  excluding Commit and every later delivery action. A current transition alone emits `approved -> task_ref` and
  immediately invokes `guru-implement-task:initial`; transition failure uses the Approval owner's declared recoverable
  block with zero implementation write. The substep is never a router, public terminal or orphan result.
- Disposition fixtures route an irreversible remote candidate only through
  `active-lifecycle-remote-convergence-wait` to one of the four registered remote owners, then join that owner's
  `remote_outcome_ref` with the Disposition-owned continuation for `remote_reentry`. A cleanup refusal carrying one
  retain/suspend choice enters `cleanup_refusal_choice_reentry` directly; only a later choice produced by the named
  wait enters `choice_reentry`.
- Worker/provider fixtures assert that results return to the exact caller and cannot progress phase, approve, assign
  finding severity, mutate shared authority or create a second top-level route.
- Provider fixtures derive the closed action inventory from `provider_context`: Git covers Sync, task-free/standard
  local write, Commit, publication-tail commit, branch Publish and Finish archive commit/push; GitHub covers Draft PR
  Publish, Ready, Merge and Closure; Trellis upstream covers clean Install and existing Migration; standalone verifier,
  Guru preset Install/Stock/Reapply/activation validation, Release's immutable-candidate stages and controlled adapters
  retain their exact owners. Every declared action has exactly one owner/profile/direct consumer, and no delivery-only
  subset may stand in for the complete inventory.
- Authority/code-spec convergence fixtures compute promotion/projection inputs only from work outstanding against live
  target identities. They bind each not-yet-current authority contribution, missing/stale authority
  locator/usage/freshness projection and each same-range code-spec contribution missing from the current projection.
  The normal no-promotion authority-repair cell requires
  `promotion_kind=none,projection_kind=authority_only` with no promotion/code-spec ref; other cells bind only their
  selected authority owner plus
  `guru-bootstrap-repository-ssot:projection_refresh`, and require
  `spec_projection_ref -> guru-check-task:authority_reentry -> fresh Commit -> fresh Branch Review`. The fresh complete
  diff still contains the original changes, but exact already-current authority/projection identities must yield
  `promotion_kind=none,projection_kind=none`; material drift reopens only the affected work. Raw `trellis-update-spec`,
  preset/reapply, hooks and workers have zero `.trellis/spec` writes.
- Publication fixtures first resolve immutable extension source and target reviewed checkout, validate lineage and
  normalized reviewed-content equality, and isolate metadata-tail preparation from branch push and Draft PR creation.
  Each action has its own prepare/wait/refusal/provider re-entry. Refusal coverage requires
  `publication_preparation_not_executed -> task-publication-preparation-not-executed`,
  `branch_push_not_executed -> task-branch-push-not-executed` and
  `pr_creation_not_executed -> task-pr-creation-not-executed`, with exactly the action-local minimal identity and no
  shared/default consumer. Exact current metadata tail returns
  `publication_head_current`, an exact remote branch at that head returns `branch_published`, and an exact base/head
  Draft or READY PR returns `draft_pr_current`, all with zero mutation/confirmation. That result enters Finish, never
  Merge. Finish alone produces summary/archive/archive-push/Ready and archive-bound `ready_for_merge_ref`; only then
  may Merge run. Divergence re-enters only the owning stage and never repeats a completed mutation or crosses a
  continuation.
- Workspace fixtures live-resolve the exact repo/Issue/base/branch/worktree/task/path plus ownership/isolation state
  before constructing an action plan. An exact-current reuse emits `workspace_current` with zero plan display,
  confirmation wait, refusal branch and mutation; pending creation, transfer or isolation alone enters the
  `EVO-REQ-081` confirmation boundary, whose unconfirmed plan remains only in the current call/host session and creates
  no generic repository plan/envelope/checkpoint state.
- Standalone verifier failure fixtures capture a schema-valid non-null failure before temporary workspace cleanup.
  Matrix commands retain their applicable cell; matrix-external command/asset/ownership/sidecar/capability failures
  are `postcheck_failure`. The verifier/projection owner alone returns the blocked result and exact re-entry;
  Finalizer consumption and embedded-caller ownership takeover are invalid.

## 5. Context And Continuity Measurements

For each applicable normal run, measure exact counts rather than relative speed claims:

- independent call/host-session-local invocation envelope construction and admission receipt: exactly one;
- generic repository-envelope path creation/write during admission, pre-route, pre-task, task-free or standalone:
  zero; every allowed post-task checkpoint has exactly one same-Skill public-wrapper consumer;
- lifecycle-bound event new envelope/receipt/top-level reroute: zero;
- lifecycle-bound event missing `bound_event_ref`, losing host identity/session/current content, or requiring ambient
  host-history lookup: zero;
- initial authority/provider full read by its owning envelope section: at most one per applicable dependency;
- applicable repository RDT, Architecture Baseline and task `prd.md`/`design.md`/`implement.md` appear in stable
  locator/identity/order, while decision-relevant live facts/current delta/unresolved items form the minimal changing
  tail; task documents never replace repository authority;
- cache hit, cache miss and cache unavailable runs resolve the same current authority/freshness and semantic result;
- unchanged same-source full reread by a downstream consumer, duplicated semantic gate, unconsumed artifact/script
  result, repeated question or repeated side effect: zero;
- human-style assignment/signoff/transaction handoff and already-current fact restatement: zero; each AI owner
  decides directly from the current stable authority prefix and minimal tail;
- public output field without a direct consumer: zero;
- duplicated/missing Clarification/RDT/Architecture `authority_context` subprojection owner, semantic consumer using a
  producer summary instead of the same bound authority content, or declared provider action without one exact owner:
  zero;
- recoverable block without exactly one constructible owner re-entry, or a terminal/new-invocation result carrying
  a fake continuation: zero;
- generic matching Skill/profile, generic current/remote owner, task/private/ambient owner inference, or standalone
  `caller_id=standalone`: zero;
- cumulative stdout reinjection, invalid wait handle reuse and unbounded no-progress pending: zero;
- raw `trellis-before-dev` call and second spec full-read chain: zero;
- raw `trellis-meta`/`trellis-update-spec` call, generic Trellis-reference caller, second `.trellis/spec` writer, or
  authority-promotion/code-spec-contribution path that skips projection refresh/fresh Check/Commit/Review: zero;
- already-current authority promotion/projection selected again, current metadata tail recommitted, already-current
  remote branch pushed again, exact Draft/READY PR created again, current archive/archive push/Ready repeated, or a
  no-mutation current path requesting confirmation: zero;
- current plan activation that terminates before `guru-implement-task:initial`, exposes an activation router/public
  result, or routes transition failure outside the Approval owner: zero;
- fixed confirmation prompt/password/hash/digest/task-id/path/branch/SHA/identity/summary/prescribed-wording
  challenge, `确认执行 <hash>`, lexical `合并PR` gate, script/validator/recorder confirmation parsing and
  persisted authorization: zero;
- explicit-refusal output without one named owner/re-entry, refusal mislabeled as blocked/provider defect, or one
  confirmation consumed by a later Commit/provenance-tail/branch-push/PR-create/Finish/Merge/Closure/Cleanup/disposition-cleanup/
  Release action: zero;
- secret/credential/raw sensitive record in output or artifact: zero.
- verifier `failed + null failure`, cleanup before failure evidence, wrong stage/cell, unbounded or credential-bearing
  error tail, full stdout/stderr persistence beyond hash/size, or Finalizer consumption of verifier evidence: zero.

Elapsed time, rounds, token/byte compression and worker count are diagnostics only. They cannot independently pass
or fail the product contract.

## 6. Stock And Distribution Selection

- `EVO-FIX-STOCK-COEXISTENCE` is admission-only: it proves collision classification/redirect/block and passive
  context isolation, with stock mutation count zero.
- `EVO-FIX-STOCK-MAINTENANCE` owns selected absence/quarantine/replacement/context actions, user modification,
  sidecar, per-action `completed|pending|unknown`, aggregate partial/unknown/action-required priority and exact
  re-entry. Every pending mutation must first pass the single profile-fixed
  `stock-policy-action-confirmation-wait`: clear affirmative reaches only the matching standalone/embedded/reapply
  action re-entry, missing confirmation remains waiting, refusal returns the exact action-not-executed shape, material
  drift performs zero mutation and rebuilds the plan, and an action-state continuation can never directly authorize
  mutation. It also proves standalone suppression/provider blocked targets are distinct, every adapter block returns
  synchronously to its profile-fixed caller without a public caller ref, refusal has an action-not-executed result
  that can re-enter only the same stock owner, every R01..R09 retained profile fixes one exact hook-policy/session/
  workflow-breadcrumb context owner, and standalone, retained-host and embedded/reapply exit sets are disjoint.
  Embedded/reapply `returned_to_caller` uses six disjoint `policy_result` variants; fields from another variant and
  aggregate optional result fields are rejected, and only action-state variants carry an action continuation.
- Standalone stock maintenance has one producer and one return chain only:
  `guru-validate-extension-projection:standalone -> guru-maintain-stock-projection:standalone ->
  guru-validate-extension-projection:stock_policy_reentry -> fresh complete projection validation`. Stock never
  completes the workflow directly and this chain does not create a fifth distribution route.
- All nine suppressed rows share exactly one admission-success edge,
  `guru-admit-invocation:request_admitted -> guru-route-request:top_level`. Their Guru capability successors remain
  downstream route owners and are never substituted for that guard-success consumer.
- `trellis-meta` suppression passes only when the preset-written reference manifest, its source precedence, all
  caller-fixed adapter profiles and the active/new-change write route are reachable. `trellis-update-spec`
  suppression passes only when the Bootstrap-owned review-trigger-to-projection/fresh-review chain is reachable. Raw
  absence alone is not success for either asset.
- A normal implementation slice tests only affected shared/host cells. `EVO-DEL-09` owns the full declared
  Codex/Claude/Cursor clean/existing/update/reapply matrix.
- Clean install and existing migration are disjoint preclassified routes. Existing migration always evaluates the
  five ordered cells and one final validation, including an all-N/A composite. UPDATE dry-run selects exactly
  `--migrate --skip-all` when migration is required or `--skip-all` otherwise; ownership 4.0 must be current before
  any selected stock mutation.
- Capability loss compares only `workflow/task_data/docs_authority`; public Skill/API/distribution/installed/host
  mismatch is a separate consistency finding. Both block, but results are not mislabeled.
- Release proof is valid only for the immutable candidate that passed the full predecessor matrix and received
  dialogue-local semantic publication confirmation under `EVO-DES-069`; a clear affirmative after the unchanged
  exact plan is sufficient and authorizes only publication. A zero-completed/unknown first publication action uses
  only `publication_progress_ref`; `published_partial_ref` is accepted only after at least one action is confirmed
  completed and another remains pending.

## 7. Planning-Stage Gate

At this planning stage, allowed checks are static: file/link/manifest/table structure, ID set closure, 39 unique
public Skill identities / 43 profile rows, exactly 37 lifecycle owners plus two specialist non-owners, every
output-to-consumer-input projection, external-exit consumer closure,
  the complete Section 7.1 recovery inventory, nine wording profiles, ten active four-result qualification profiles
  plus one standalone three-result profile, 50 fixture rows,
17 stock rows,
9 retained rows, one reference-manifest writer/caller-bound adapter family, one convergent authority/code-spec
projection writer/return chain covering zero-promotion `authority_only`, same-range `with_code_spec` and an
already-current double-none exit, one standalone
`Projection -> Stock -> named action confirmation wait when mutation remains -> Stock action re-entry -> Projection
fresh validation` chain, one exact-current Workspace no-mutation convergence path,
one compound activation/implementation-entry confirmation, three independent provenance-tail/branch-push/Draft-PR
  confirmation subgraphs, one platform-preserving installed reprepare matrix with invalid-identity zero extension
  source checkout/apply/commit/managed mutation, one Finish-before-Merge chain with no-mutation current exits, standalone verifier
evidence-before-cleanup, zero admission/pre-route/pre-task/task-free/standalone generic repository-envelope paths,
same-Skill/same-wrapper ownership for any task-local checkpoint and trace range coverage. Runtime, installed, provider and Release rows remain
`planned_not_executed`.

The current selected-base rebind and Requirements-stage successor zero-loss projection bind
`origin/main@5650df47…`, 84 Requirements, 34 NFR and the existing 50 fixture families. Fresh Requirements semantic,
Strict technical and deterministic closure gates have passed, so `requirements_ready_for_design` is current. All 50 fixture successors retain Design planning
allocation. The pre-`REQ-REV-142` fresh Design review and deterministic closure remain stale historical evidence;
current fresh Design review and deterministic closure have passed, so `fresh_design_review_passed` /
`evolution_refactor_eligible` are current. The prerequisite fixtures specifically preserve #311 through Draft
PR/archive/Ready/`ready_for_merge` without
completed-mutation replay and through evidence-before-cleanup standalone verifier failure handling, plus #312 through
clean-tracked continuation, unrelated-dirty isolation and real blockers, and PR #317 through exact installed
platform-set preservation with invalid identity blocked before extension source checkout/apply/commit.
The current Test projection is a Design-review candidate and does not require or imply implementation tests.
