# #305 Evolution Planning Execution And Validation Plan

## Boundary

This is the execution and validation plan for the current #305 Phase 1 Design continuation. It is not an
implementation plan for changing the Guru runtime. The live task status remains `in_progress` from a historical
activation, but `REQ-REV-133..138` and the latest user decision keep the current continuation in Phase 1. #311/#312
are merged into the selected base, their capabilities are rebound, Requirements is current, and reviewed Design/Test/
Architecture/task projections now cover the complete 83/33/23/13/50/73 set. The fresh Design gate passed and this
continuation stops in Phase 1. Runtime/workflow/Skill/schema/script/preset/overlay changes, stock mutation, installation,
migration, provider action and Release remain outside this continuation.

## Test Authority

- target strategy: `docs/test/evolution/test-strategy.md`.
- fixture plan: `docs/test/evolution/fixture-plan.md` with 50 rows, all `planned_not_executed`; every row has candidate
  Design ownership and `EVO-DES-001..073` mapping.
- trace: `docs/test/evolution/traceability.md`.
- current as-built Test remains `docs/test/versions/current-main-0.6.5-guru.41/` at selected-base
  `3efcce72…` and supplies only current capability context, not target execution PASS; `.40`/`d907fcc5…` is
  historical comparison evidence.

## Candidate Execution Sequence

1. Bind the selected-base #311/#312 Issue/PR/merge identities as related prerequisite inputs only; do not close,
   implement, merge or otherwise mutate either Issue in #305.
2. Freshly read selected-base `.41` RDT/Architecture/inventory, reclassify both merged results as current-base
   capabilities, and compare all current capabilities against target requirements and normal-path fixtures.
3. Complete `REQ-REV-133..138` across Requirements main/NFR/inventory and the 52 UC / 83 REQ / 33 NFR / 23 current
   capability / 13 target delta / 50 fixture closure. #311 is folded into `CUR-CAP-013/014/017/018/019`, #312 into
   `CUR-CAP-012`; no fifth core capability or duplicate `TARGET-DELTA-014` remains.
4. Run deterministic structure/count/link/table/YAML/JSON checks against the exact current candidate.
5. Run fresh full-document Requirements semantic and Strict technical reviews. Fix every P1/P2/P3 finding and rerun
   both reviews against each changed candidate until both are clean.
6. Only after steps 4-5 are current may the Requirements/trace statuses become
   `requirements_ready_for_design` / `requirements_trace_ready_for_design`; rerun deterministic checks and both fresh
   reviews against that final identity.
7. Revise Design/Test/Architecture/task projections for the full current capability set. Allocate `EVO-DES-070..073`
   to the two-stage gate, #312 Reconcile continuity, #311 Publish/Finish/Merge terminal and Projection-owned verifier
   failure lifecycle; map all 50 fixtures without changing Requirements semantics.
8. Run fresh full-document Design review across repository Design, Test projection, Architecture contribution and task
   projections. Fix every P1/P2/P3/high-risk finding and rerun against the changed candidate until clean.
9. Run deterministic set/link/table/YAML/JSON/consumer/recovery closure for 83/33/23/13/50/73, 39 public Skills,
   43 profile rows, 37 lifecycle owners and two specialist non-owners.
10. Only after steps 8-9 are current may Design become `design_ready_for_delivery_planning`, review become
    `fresh_design_review_passed` and refactor become `evolution_refactor_eligible`; then stop in Phase 1.

Current sequence result: steps 1-10 are complete. The final fresh Design review closed `DES-REV-001..048` with open
P1=0, blocking P2=0, P3=0 and high-risk question=0; deterministic closure passed. The historical
`DES-REV-001..014` result and task activation are not current evidence and authorize no Phase 2/runtime action.

## Planning Validation

| Check | Expected planning result | Evidence boundary |
| --- | --- | --- |
| whitespace/diff | `git diff --check` passes | no semantic or runtime claim |
| navigation/links/manifests/GFM tables | all local locators resolve and candidate statuses agree | no installed projection claim |
| closed ID sets | Requirements 83, NFR 33, candidate Design 73, current capabilities 23, target deltas 13, fixtures 50 | presence alone does not prove semantic adequacy or current Design review |
| public graph | 39 unique public Skill identities / 43 profile rows; exactly 37 lifecycle owners include Admission/Route Request/Answer/Current Work/History while Wording/Qualification are the two specialist non-owners under their fixed callers; every consumer input is constructible without generic frame/private lookup; admission/pre-route/pre-task/task-free/standalone envelope state stays in the call stack or host current-session continuation with zero generic repository-envelope write, missing/stale continuation uses exact-owner block/re-entry plus live reconstruction, and any post-task checkpoint remains one exact Skill's existing task-local ignored state for its same-owner public wrapper only; `bound_event_ref,event_sequence` reaches the registered lifecycle owner directly; Clarification/RDT/Architecture subprojection ownership and the full provider action-owner inventory are closed; every ordinary recoverable block maps to one Section 7.1 same-owner profile; lifecycle binding, independent isolation and Answer provider recovery are distinct; the Section 3.1 registry, four-owner remote convergence and post-owner/post-remote fresh Admission edges are closed; exact-current Workspace reuse returns `workspace_current -> task_impact_sync` with zero plan/confirmation/refusal/mutation, while creation/transfer/isolation alone enters confirmation; the single Approval plan displays activation plus immediate approved implementation entry/allowed writes, and its internal activation closes only as `approved -> guru-implement-task:initial` or its own block with zero implementation write; nine wording profiles and ten active four-result plus one standalone three-result qualification profile return only through original-caller continuations; Bootstrap returns authority bootstrap through an opaque continuation to the exact RDT/Architecture owner and returns outstanding authority/code-spec projection work to fresh Check, including `promotion_kind=none,projection_kind=authority_only` when shared authority is current but its locator/usage/freshness projection needs repair; the subsequent full-diff review emits exact double-none only for already-current targets; provenance-tail preparation, push and PR create have separate waits/continuations/refusals/recoveries plus no-mutation current exits; recoverable blocks are not mislabeled terminal, true terminal blocks have no fake continuation, and every external exit, explicit refusal and adapter blocked result has one named profile-fixed consumer/router/stop | adapters/routers counted separately; no runtime claim |
| delivery/recovery graph | accepted GitHub work enters provenance preparation before push and Draft PR; accepted none work carries only acceptance identity into Finish, has zero pre-Finish delivery fact and receives its sole `delivery_fact_ref` from successful Finish; Draft/READY PR enters Finish, archive-bound Ready enters Merge, Closure creates the delivery terminal and that terminal enters Cleanup only; Branch Review base evolution uses declared `base_reentry`; semantic confirmation traces include all three Publish actions and `EVO-DES-072`; Provider Recovery includes Projection-owned verifier evidence/re-entry through `EVO-DES-073` | planning projection only; no provider action or runtime claim |
| stock closure | 17 exact rows with `9/1/2/5`; nine retained profiles bind nine exact host context owners; all suppressed rows have the one Route Request admission-success edge; selected action/owner/consumer/block present; raw meta successor binds the preset reference manifest/caller-fixed adapter/write route, raw update-spec successor binds promotion/Bootstrap projection/fresh review; embedded `policy_result` variants are disjoint; no generic adapter caller ref or standalone caller id; standalone refusal re-entry is exact. When a mutation remains, the sole standalone path is `Projection -> Stock -> stock-policy-action-confirmation-wait -> Stock standalone_action_reentry -> Projection stock_policy_reentry -> fresh complete validation`; embedded/reapply use the same named wait before their profile-fixed action re-entry, missing/refusal/drift remain owner-local and an action-state continuation never directly authorizes mutation. Stock cannot complete the workflow or create a fifth distribution route | no file mutation or host matrix execution |
| RDT impact | Requirements and selected-base capability rebind are current; Test has complete candidate Design mapping and stays `planned_not_executed` | no runtime/Test execution or current promotion claim |
| Architecture impact | task contribution is `design_ready_for_delivery_planning` / `fresh_design_review_passed` / `not_promoted`; selected-base current Architecture is input, while shared current and ADR index remain unchanged | no accepted ADR/shared-current promotion |
| semantic Requirements review | fresh full-document semantic and Strict technical review passed for the final 83/13/50 candidate | Design eligibility only; no Design execution in this continuation |
| semantic Design review | fresh full-document review passed for the complete 73-responsibility/50-fixture candidate with P1/P2/P3/high-risk counts all zero | establishes planning readiness only; no runtime/Test execution claim |

Publish refusal closure is projected explicitly: provenance, branch-push and Draft-PR creation refusals emit
`publication_preparation_not_executed`, `branch_push_not_executed` and `pr_creation_not_executed`; their outputs
carry only the corresponding task/acceptance/head identity and terminate at the distinct
`task-publication-preparation-not-executed`, `task-branch-push-not-executed` and
`task-pr-creation-not-executed` consumers. No default refusal consumer or provider-block fallback is permitted.

Historical package/runtime/installed/live/Release results are not rerun or relabeled. Any unavailable external fact
is an explicit unverified boundary.

## Docs SSOT Plan

- Repository Requirements remains the only upstream authority in `docs/requirements/evolution/`; its current
  `requirements_ready_for_design` / `requirements_trace_ready_for_design` identity is bound to `REQ-REV-011..138`.
  The selected
  post-#311/#312 base is bound to `3efcce72…` / `.41`; merge/lifecycle facts are current, while the #305 authority
  rebind, merged-behavior reconciliation, Requirements-stage zero-loss comparison and fresh Requirements dual review
  are current; every prior Design review binding remains stale, while the revised Design candidate has passed the
  current fresh review and deterministic closure.
- Normal execution orders applicable repository RDT, Architecture Baseline and task `prd.md`/`design.md`/
  `implement.md` as the stable primary context; decision-relevant live facts, current delta and unresolved items are
  the minimal changing tail. Cache is optional and never authority. Each AI owner judges directly from this context;
  human-style assignment/signoff/transaction handoff and already-current fact restatement are forbidden projections.
- Admission/pre-route/pre-task/task-free/standalone continuation lives only in the call stack or host current session
  and writes no generic repository envelope. Missing/stale continuation re-enters the exact owner and reconstructs
  from live authority. After task creation, an exact Skill may use only its existing task-local ignored owner-private
  checkpoint for non-reconstructible state consumed by that same Skill's public wrapper; downstream Skills never read it.
- Repository target Design and Test live only under `docs/design/evolution/` and `docs/test/evolution/`.
- Architecture impact lives only in the #305 task contribution; shared current and ADR index remain unchanged.
- Task `prd.md` owns requirement locator/delta/acceptance; `design.md` owns Design/Architecture reconciliation;
  this file owns execution/validation/delivery mapping.
- `.trellis/spec` receives no target projection during #305. A future reviewed implementation range may project
  only when Branch Review finds outstanding `authority_only|with_code_spec` work, every selected RDT/Architecture
  promotion, if any, is current; `authority_only` may pair with `promotion_kind=none` for missing/stale authority
  locator/usage/freshness and carries no code-spec ref, while the latter variant carries its same-range contribution ref that is still missing from
  current projection, through `guru-bootstrap-repository-ssot:projection_refresh`, then must repeat
  Check/Commit/Branch Review. That fresh complete-diff review emits exact double-none when target authority/projection
  identities are already current and reopens material drift only. This branch does include planning-authority
  consistency edits to the root, workflow/preset and platform-facing README/instruction text. It does not change
  runtime Skill/schema/script/installer/preset-overlay/workflow executable projections in this planning phase.

## Delivery Mapping

The revised Design candidate decomposes possible future implementation in
`docs/design/evolution/delivery-plan.md` into dormant contract,
admission/reference, planning, implementation/projection-refresh, delivery with separate provenance/push/Draft-PR/
Finish/Merge/Closure/Cleanup, Projection-owned verifier failure recovery,
stock, clean-install, migration, full-matrix and exact-Release
slices. Requirements convergence, Design review and deterministic closure are current, but those suggestions remain
non-actionable until a future independently authorized delivery intake. Each later
slice requires fresh intake and its own RDT/Architecture
contribution/review; exact resource-plan confirmation is required only when creation, transfer or isolation remains
pending, while exact-current reuse bypasses plan/confirmation/refusal. None is implicitly authorized by approving
this task plan.

The eventual #305 planning delivery route, commit scope and PR action are selected only after this fresh Design gate
and a later separately authorized workflow entry; the merge-bound fresh Requirements gate is current. Each external side effect still requires
its own current exact-action plan. No commit/push/PR is part of the current continuation.
