# #305 Evolution Design Planning Projection

## Authority

- Change authority: GitHub Issue #305.
- Requirements: `docs/requirements/evolution/` with current
  `requirements_ready_for_design` / `requirements_trace_ready_for_design`, bound to `REQ-REV-011..138`; selected base
  `3efcce72a0d47e38ec725aa8c0f8498992f3416f` contains PR #313/#314 merges, with #311 `OPEN` only for
  `follow-up-only` work and #312 `CLOSED`. Merge/lifecycle, #305 authority rebind, merged-behavior reconciliation and
  the 83/13/50 Requirements-stage zero-loss comparison and fresh Requirements dual review are current.
- Target Design: `docs/design/evolution/` / `guru-trellis-evolution-design-2026-08-29` /
  `design_ready_for_delivery_planning` / `fresh_design_review_passed` / `evolution_refactor_eligible`.
- Target Test: `docs/test/evolution/` / `guru-trellis-evolution-test-2026-08-29` /
  `test_candidate_planned` / `design_ready_for_delivery_planning` / `fresh_design_review_passed`; all 50 Requirements
  fixtures have reviewed Design allocation, `evolution_refactor_eligible` is current, and all fixtures remain
  `planned_not_executed`.
- Current as-built authority: `.41` RDT/Architecture at selected-base
  `3efcce72a0d47e38ec725aa8c0f8498992f3416f`, source baseline
  `651defee871d4bb07683547df09d1e0ac62b4a49` + #311 serialized promotion delta. The `.40` / `d907fcc5...`
  snapshot is historical comparison evidence; target docs do not replace current before reviewed
  implementation/promotion.

This file is a task projection, not parallel Design authority. Repository Design alone owns behavior/public contracts;
this continuation projects its revised `EVO-DES-001..073` candidate and the current fresh Design gate result.

## Current-To-Target Reconciliation

The historical pre-`REQ-REV-133` projection in `docs/design/evolution/capability-inventory.md` allocated
`CUR-CAP-001..023` and `TARGET-DELTA-001..013`. Current Requirements fold #311 into
`CUR-CAP-013/014/017/018/019` and #312 into `CUR-CAP-012`; selected-base current-to-target comparison therefore keeps
13 target deltas and removes the duplicate historical `TARGET-DELTA-014`. `EVO-REQ-082..083`, `EVO-NFR-033` and the
three post-`REQ-REV-132` fixtures are allocated by `EVO-DES-070..073` with zero candidate successor gap.
Private current schemas, wrapper routes, aggregate gate artifacts and 21/89 magic counts are not preserved as
target API.

Target decisions:

- retain marketplace workflow id `guru-team` but introduce `guru-team-evolution-contract-1.0` and mandatory
  atomic existing-repository migration;
- use one private invocation `context_envelope`, lazy authority/provider projections and consumer-minimal public
  results; section owners perform initial/targeted live reads, consumers do not repeat unchanged full reads, and
  every public input is constructible without a generic frame/private/ambient lookup;
- use one plan author/one approval and one standard implementation owner;
- split Delivery, Acceptance, Publish, Finish, Merge, Closure, Cleanup and history by exact ownership/re-entry;
- split Publish into independent immutable-source provenance/metadata-tail, branch-push and Draft-PR prepare/wait/
  confirmation/refusal/recovery stages; Draft PR always enters Finish, Finish alone archives/pushes/marks Ready and
  emits archive-bound `ready_for_merge_ref`, then Merge/Closure/terminal/Cleanup follow in order;
- preserve #312 original-active-worktree clean-tracked continuation in Reconcile while unrelated dirty state stays
  untouched and real same-task/runtime/worktree/branch blockers remain blocked;
- keep standalone verifier failure evidence and evidence-before-cleanup lifecycle inside Projection; embedded findings
  remain caller-owned and Finish consumes no verifier state;
- close every ordinary recoverable block through one producer-owned continuation/same-owner profile, while wording
  and qualification return only the original caller's opaque continuation;
- register exactly 37 lifecycle owners across the 39 public Skills, including Admission, Route Request, Answer,
  Current Work and History; Wording and Qualification remain specialist non-owners whose fixed original caller keeps
  lifecycle ownership;
- manage frozen official stock as `9 suppressed / 1 provider / 2 explicit / 5 workers`, plus nine retained
  nonsemantic host rows;
- replace raw `trellis-meta` with preset-written `guru-trellis-reference-manifest-1.0` plus caller-fixed read adapter,
  while all writes use active/new-change governance;
- replace raw `trellis-update-spec` with Bootstrap-only post-review `guru-code-spec-projection-1.0` and fresh
  Check/Commit/Branch Review; promotion/projection selection includes only work not already current and that fresh
  complete-diff review converges to exact double-none after current targets are observed;
- allow standalone stock maintenance only through
  `Projection -> Stock -> Projection stock_policy_reentry -> fresh complete validation`; Stock does not complete the
  workflow or create a fifth distribution action;
- make the single Planning confirmation plan display both task activation and immediate entry into the approved
  implementation scope/allowed writes, while excluding Commit and all later delivery actions; activation failure
  produces zero implementation write;
- accept clear dialogue-local confirmation only after an unchanged exact side-effect plan, with zero fixed
  prompt/password/hash/digest/task/path/branch/SHA/identity/summary/prescribed-wording challenge,
  `确认执行 <hash>`, script parsing or authorization persistence; exact-current Workspace reuse bypasses plan display,
  confirmation wait, refusal handling and mutation;
- require ownership 4.0 validation before any future upstream-path stock mutation, and freeze the delivery candidate
  only after all 39 public Skills are implemented/reviewed before the immutable matrix;
- do not modify official Trellis source/global installation and do not retain legacy route/adapter/fallback.

## Review And Revision Delta

The status phrase `closed in revised candidate; fresh review passed` (and equivalent `closed in candidate` wording)
in the historical table below refers only to the pre-`REQ-REV-133` Design candidate. It is not a current Design gate
result; the current prerequisite row and the Design Gate section below are authoritative for this continuation.

| Finding group | Design closure | Status |
| --- | --- | --- |
| Admission/answer | `request_ref` now closes Admission -> Request Router; direct-answer profile is explicit; provider unavailable/access/incomplete remains `answered` with unverified facts, while only stale/mismatched answer scope/profile/consumer binding may block; suppression/provider/retained collisions have three role-local blocked exits | closed in candidate |
| Specialist | wording review-only/change-scoped exit sets are disjoint; ten active qualification profiles expose four results while standalone exposes only classified/scope-confirmation/blocked; scope confirmation goes through one profile-fixed Clarification route and returns to the original caller for fresh candidate reconstruction and qualification | closed in revised candidate; fresh review passed |
| Return graph | `guru-requirements-current-router` owns eight ordinary caller returns; eleven qualification-scope returns use caller-owned opaque continuations, and RDT/Architecture Bootstrap returns only to the exact originating authority owner | closed in revised candidate; fresh review passed |
| Public I/O | Architecture target input is self-contained; retained-host has an explicit public contract; standalone and embedded projection/stock exits are mutually exclusive | closed in candidate |
| Provider/recovery | Git/GitHub/Trellis/preset/Release action profiles are closed; atomic state is `completed|pending|unknown`, with partial only as aggregate | closed in candidate |
| Worker/setup | platform/channel implementation adapters each own task-free/standard profiles; host setup uses the seven Requirements cells | closed in candidate |
| Distribution | UPDATE dry-run selects exactly one `--migrate --skip-all|--skip-all` branch; ownership 3.0 forbids mutation until ownership 4.0 validation | closed in candidate |
| Delivery slicing | Slice 02 defers stock-guard closure to Slice 06; candidate freezes after all 39 Skills at Slice 08; Slice 09 is immutable matrix only and Slice 10 Release-only | closed in candidate |
| Historical Requirements change | `EVO-REQ-081`, `TARGET-DELTA-013`, `EVO-DES-069` and the 47th semantic-confirmation fixture were bound to the pre-`REQ-REV-133` reviewed candidate | historical closure only; stale |
| Current prerequisite/rebind change | `REQ-REV-133..138` adds `EVO-REQ-082..083`, `EVO-NFR-033`, two-stage eligibility, full installed publication terminal continuity, unrelated-dirty isolation, evidence-before-cleanup verifier failure preservation and three fixtures; selected-base comparison folds #311/#312 into existing current capabilities and removes duplicate `TARGET-DELTA-014` | Requirements ready; Design allocation, fresh review and deterministic closure passed |
| Confirmation contract projection | Design summaries, Release wait transitions, Architecture contribution, fixture and task projection carry the complete prohibited-challenge set and AI-only reply judgment | closed in candidate |
| Planning/Architecture projection | task PRD records only the objective Phase 1 route, not a prior user confirmation; Architecture contribution scope includes Evolution Requirements/Design/Test | closed in candidate |
| Planning gate order | fresh full Design review precedes wording/RDT/Architecture/task-plan approval; any later content revision returns to deterministic closure and fresh exact-candidate Design review | closed in candidate |
| Stable context and AI ownership | applicable repository RDT -> Architecture -> task `prd.md`/`design.md`/`implement.md` is the stable locator/identity/order prefix; live facts/delta/unresolved items form the minimal tail; cache is optional and non-authoritative; every AI owner judges directly, while human-style assignment/signoff/transaction handoff, current-fact restatement and same-source unchanged full reread counts are zero | closed in candidate; fresh review passed |
| Side-effect refusal graph | Sync, pending-action Workspace, Commit, PR publication, READY merge, manual Issue closure, Finish/archive, Cleanup, clean install, migration, stock maintenance, plan activation and Release now have explicit owner-local zero-side-effect refusal outputs; no-mutation current exits bypass plan/confirmation/refusal, including exact-current Workspace reuse; Finish is semantic because confirmation is inside its boundary while transitions remain deterministic | closed in candidate; fresh review passed |
| Stock/adapter blocked consumers | standalone suppression/provider failures have two named maintenance stops; embedded stock and every controlled-adapter blocked result return only to the exact profile-fixed caller | closed in candidate; fresh review passed |
| Public edge construction | removed caller-authored runtime facts and generic frames, made profile-specific caller continuations explicit, added missing range/continuation identities, and required each consumer input to be satisfied only by the selected exit projection or its exact live-fact owner | closed in revised candidate; fresh review passed |
| Provider progress DTO | Release zero-completed/unknown publication now uses `publication_progress_ref`, true partial alone uses `published_partial_ref`; Merge and Closure recovery require exact continuation | closed in revised candidate; fresh review passed |
| Disposition/reapply ownership | active-lifecycle cleanup refusal without one retain/suspend choice now has only `active_lifecycle_disposition_choice_required`; stock reapply is fixed to Existing Migrator's ordered UPDATE/PRESET-REAPPLY cell | closed in revised candidate; fresh review passed |
| Admission/lifecycle recovery closure | separated lifecycle binding, independent isolation and Answer-owned provider repair; added the closed Section 3.1 lifecycle owner registry, exact post-owner/post-remote fresh Admission profiles, named four-owner remote convergence and direct-versus-later disposition choice re-entry | closed in revised candidate; fresh review passed |
| Specialist/stock closure | added the complete Section 7.1 same-owner inventory; nine wording profiles; ten active four-result qualification profiles plus standalone three-result qualification; exact Clean/Migration/standalone-Stock refusal re-entry; R01..R09 exact host context owners; one shared suppression-success edge; disjoint embedded Stock variants; and zero generic adapter/standalone caller refs | closed in revised candidate; fresh review passed |
| `DES-REV-001` / blocking P2 | `guru-publish-task-pr` previously combined branch push and PR creation behind one confirmation boundary. It now has disjoint `push_prepare/push_confirmation_reentry/push_provider_reentry` and `pr_create_prepare/pr_creation_confirmation_reentry/pr_provider_reentry` graphs, two named waits, exact `branch_push_not_executed -> task-branch-push-not-executed` and `pr_creation_not_executed -> task-pr-creation-not-executed` refusal routes, and two recovery routes; push confirmation cannot authorize PR creation | closed in revised candidate; fresh review passed |
| `DES-REV-002` / blocking P2 | raw `trellis-meta` managed absence previously pointed only to descriptive “lazy reference” prose. The candidate now defines preset-single-written `guru-trellis-reference-manifest-1.0`, fixed source precedence, caller-bound `guru-trellis-reference-read-adapter-1.0` standalone/embedded profiles, synchronous return and active/new-change write routing | closed in revised candidate; fresh review passed |
| `DES-REV-003` / blocking P2 | raw `trellis-update-spec` managed absence previously lacked one projection owner, review trigger and downstream recheck. Branch Review now selects independent promotion/projection discriminators: only exact double-none enters delivery, while Bootstrap `projection_refresh` is the sole `.trellis/spec` writer for `authority_only|with_code_spec` after any selected promotion is current. The latter requires a same-range contribution ref even when no authority promotion is selected; both emit `guru-code-spec-projection-1.0` and return only through fresh Check/Commit/Branch Review | closed in revised candidate; fresh review passed |
| `DES-REV-004` / blocking P2 | promotion/projection previously selected from contribution presence in the complete diff without distinguishing outstanding work from target identities already made current, so the mandatory fresh Check/Commit/full-diff review could select the same work forever. Branch Review now live-compares authority/contribution/projection targets, emits refs only for not-yet-current work, permits exact `promotion_kind=none,projection_kind=none` when the complete diff still contains already-current changes, and reopens only material drift; Bootstrap returns an already-current projection without rewriting it | closed in revised candidate; fresh review passed |
| `DES-REV-005` / blocking P2 | the accepted-route router invoked undeclared `guru-publish-task-pr:push`, publication wording called recoverable `push_blocked/pr_blocked` terminal, and no explicit already-current branch/PR convergence path prevented repeated confirmation or mutation. The router now enters provenance preparation; exact current tail/remote HEAD/Draft-or-READY PR return no-mutation `publication_head_current/branch_published/draft_pr_current`, divergent state uses stage-specific re-entry, and Draft PR enters Finish rather than Merge | closed in revised candidate; current fresh review passed |
| `DES-REV-006` / blocking P2 | `lifecycle_bound` previously projected only sequence/order to the selected owner, so the owner could not consume the causally bound host event without an ambient history lookup. Admission and the closed router now carry `bound_event_ref,event_sequence` directly; the ref binds host event identity/session/current content and no new envelope/receipt is created | closed in revised candidate; fresh review passed |
| `DES-REV-007` / blocking P2 | stable authority content had no complete subprojection ownership contract, and `provider_context` named only a delivery-oriented consumer subset. Clarification, RDT and Architecture now exclusively own their applicable authority subprojections while downstream semantic owners use the same bound content; the provider inventory now covers every declared Git/GitHub/Trellis-upstream/Guru-preset/Release action and controlled adapter with an exact owner | closed in revised candidate; fresh review passed |
| `DES-REV-008` / blocking P2 | approved Planning previously entered `phase-1-task-activation` without a declared successor or failure contract. Activation is now an Approval-internal deterministic substep: only a current transition emits `approved -> task_ref` and immediately invokes `guru-implement-task:initial`; objective failure remains in Approval recovery | closed in revised candidate; fresh review passed |
| `DES-REV-009` / blocking P2 | task `implement.md` previously made the Design-review continuation proceed into wording, RDT/Architecture impact and task-plan approval before binding Design readiness. The pre-`REQ-REV-133` sequence bound readiness immediately after its clean fresh Design gate and stopped; all later Planning gates required a separate continuation | historical closure only; stale under `REQ-REV-133` |
| `DES-REV-010` / blocking P2 | the lifecycle registry previously omitted five legal owners: Admission, Route Request, Answer, Current Work and History. Section 3.1 now defines exactly 37 lifecycle owners including those five; Wording and Qualification are the only two public specialist non-owners and their fixed original caller retains lifecycle ownership | closed in revised candidate; fresh review passed |
| `DES-REV-011` / blocking P2 | standalone Stock had a `standalone` profile but no exact producer. Projection is now its sole caller; Stock current returns only to Projection `stock_policy_reentry`, which freshly validates the complete surface before completion. Stock does not terminate the workflow or create a fifth distribution route | closed in revised candidate; fresh review passed |
| `DES-REV-012` / blocking P2 | Planning previously displayed only task activation before directly entering Implementation, so the confirmation did not cover the full next action. Approval now displays one compound plan with activation plus immediate approved implementation scope/allowed writes, excludes Commit and later delivery, and permits Implementation only after a current transition; transition failure writes nothing | closed in revised candidate; fresh review passed |
| `DES-REV-013` / blocking P2 | Workspace `create_or_reuse` previously required a displayed plan and confirmation even when the exact resource set was already current. Workspace now live-resolves resource plus ownership/isolation state first, returns `workspace_current -> task_impact_sync` with zero plan/confirmation/refusal/mutation for exact-current reuse, and enters the confirmation boundary only for pending creation/transfer/isolation | closed in revised candidate; fresh review passed |
| `DES-REV-014` / blocking P2 | after `DES-REV-013`, generic decision/delivery/capability/gate wording still required every potential side-effect owner to display a plan and own a refusal, so exact-current Workspace could be routed back into a confirmation loop. The shared rule now first resolves whether an action remains: every no-mutation current exit bypasses plan/confirmation/refusal, exact-current Workspace is explicitly closed in contracts/gates/slices, and only a pending action enters its owner-local confirmation graph | closed in revised candidate; fresh review passed |

| Finding | Current defect | Revision action | Status |
| --- | --- | --- | --- |
| `DES-REV-015` / blocking P2 | merged prerequisite readiness and runtime refactor eligibility previously shared one gate, allowing Design or runtime to consume incomplete successor evidence | `EVO-DES-070` separates `requirements_ready_for_design` from Design mapping/review and `evolution_refactor_eligible` | closed in candidate; current fresh review passed |
| `DES-REV-016` / blocking P2 | #312 original-worktree/path-state continuity had Requirements acceptance but no current Design owner | `EVO-DES-071` assigns exact clean-tracked continuation and blocker preservation to `guru-reconcile-task-base` including `repair_reentry` | closed in candidate; current fresh review passed |
| `DES-REV-017` / P1 | #311 installed publication could lose immutable-source provenance or bypass Finish by routing Draft PR directly to Merge | `EVO-DES-072` assigns provenance/push/Draft PR to Publish, summary/archive/archive-push/Ready to Finish, and only archive-bound merge to Merge | closed in candidate; current fresh review passed |
| `DES-REV-018` / blocking P2 | standalone verifier cleanup could erase the only failure evidence or leak ownership into Finalizer | `EVO-DES-073` keeps non-null safe failure binding and exact re-entry in Projection before cleanup; embedded findings remain caller-owned and Finish never consumes verifier state | closed in candidate; current fresh review passed |
| `DES-REV-019` / P1 | the router summary still sent accepted GitHub work directly to `push_prepare`, sent none to an undefined closure target and sent the delivery terminal back to Finish, contradicting the complete delivery graph | `guru-accepted-route-router` now enters `provenance_prepare` or `guru-finalize-task:none`; `guru-delivery-terminal-router` enters Cleanup only | closed in revised candidate; current fresh review passed |
| `DES-REV-020` / blocking P2 | Branch Review returned base evolution through undeclared `guru-reconcile-task-base:reentry` | the return now uses the declared `guru-reconcile-task-base:base_reentry` profile | closed in revised candidate; current fresh review passed |
| `DES-REV-021` / blocking P2 | the stock `trellis-finish-work` successor still modeled Finish after the delivery terminal | its successor now enters `guru-finalize-task:github_pr` from an exact Draft/READY PR or `guru-finalize-task:none` from accepted none work | closed in revised candidate; current fresh review passed |
| `DES-REV-022` / P3 | confirmation, capability and Test projections omitted the provenance action or `EVO-DES-072`, Provider Recovery omitted `EVO-DES-073`, and some wording retained the obsolete post-Finish Cleanup name | all projections now carry provenance-tail/push/PR-create as three actions, delivery-terminal Cleanup and the complete `EVO-DES-072..073` mappings | closed in revised candidate; current fresh review passed |
| `DES-REV-023` / blocking P2 | the current Design Gate required explicit closure only through `DES-REV-018`, so it could pass without closing already-current `DES-REV-019..022` | the gate now binds the complete current `DES-REV-001..043` set, including findings introduced by this revision round | closed in revised candidate; current fresh review passed |
| `DES-REV-024` / blocking P2 | seven Design/Test/task projections reversed the required #311 standalone verifier evidence/cleanup order | every affected projection now consistently requires non-null structured evidence before cleanup | closed in revised candidate; current fresh review passed |
| `DES-REV-025` / blocking P2 | `CUR-CAP-006`, `EVO-DES-069` and task implementation projection omitted installed publication provenance-tail preparation from the exact action chain | all three now preserve provenance-tail preparation as an independent action before branch push and Draft PR creation and bind it to `EVO-DES-072` | closed in revised candidate; current fresh review passed |
| `DES-REV-026` / blocking P2 | the terminal gate's ordered “respectively” wording mapped installed publication, verifier failure, base evolution and Evolution prerequisite to the wrong `EVO-DES-070..073` owners | the gate now names each exact mapping explicitly: prerequisite `070`, base evolution `071`, installed publication `072`, verifier failure `073` | closed in revised candidate; current fresh review passed |
| `DES-REV-027` / blocking P2 | the `EVO-NFR-033` Test trace omitted the Verifier Failure Evidence fixture even though that NFR owns both installed publication and verifier-failure preservation | the row now includes the independent Verifier Failure Evidence fixture | closed in revised candidate; current fresh review passed |
| `DES-REV-028` / blocking P2 | unquoted manifest provenance was truncated at `#311` by normal YAML parsing, hiding the selected-base and review-state tail | both manifests now use folded block scalars whose parsed value retains the complete provenance | closed in revised candidate; current fresh review passed |
| `DES-REV-029` / P3 | the scope ledger still called #311/#312 pending capability-preservation inputs after their accepted implementations became selected-base current | the related entries now distinguish merged/current-capability preservation from #311 follow-up-only work and #312 closed state | closed in revised candidate; current fresh review passed |
| `DES-REV-030` / P3 | the three-column finding ledger header was followed by four-column `DES-REV-015..029` rows, so normal Markdown rendering misprojected revision actions and statuses | the historical three-column rows and current four-column revision rows now use separate explicit table headers | closed in revised candidate; current fresh review passed |
| `DES-REV-031` / blocking P2 | the Architecture contribution declared `fresh_design_review_passed` while its Planning project check still said no fresh Design finding count existed, making the current Design gate self-contradictory | the stale paragraph now binds the closed `DES-REV-001..031` range and exact zero open-finding counts while preserving the no-runtime-evidence and no-promotion boundaries | closed in revised candidate; current fresh review passed |
| `DES-REV-032` / blocking P2 | the root Requirements navigation still projected `docs/design/evolution/` as `design_review_stale` after the current Design gate passed, so a supported authority entry could route a later owner back to completed review work | the navigation now preserves the historical stale boundary while projecting the current `design_ready_for_delivery_planning` / `fresh_design_review_passed` / `evolution_refactor_eligible` state | closed in revised candidate; current fresh review passed |
| `DES-REV-033` / blocking P2 | Test traceability's deterministic-closure paragraph still declared fresh Design review pending and denied current Design closure after the same file and all current authority projections declared that gate passed | the paragraph now distinguishes deterministic closure from the now-current semantic Requirements and Design gates without claiming fixture execution | closed in revised candidate; current fresh review passed |
| `DES-REV-034` / blocking P2 | the task Design Authority section projected `fresh_design_review_passed` and `evolution_refactor_eligible` but still described the same current projection as having a pending fresh Design gate | the task projection now names the current fresh Design gate result while preserving the historical pre-`REQ-REV-133` stale boundary | closed in revised candidate; current fresh review passed |
| `DES-REV-035` / blocking P2 | the supported Requirements README and current-capability inventory still labeled the current target Design mapping stale after all 50 fixtures received reviewed Design allocation and the refactor eligibility gate became current | both projections now preserve only the historical pre-`REQ-REV-133` stale binding, distinguish Requirements-only coverage from later Design proof, and project the current 50/50 mapping/fresh review without claiming fixture execution | closed in revised candidate; current fresh review passed |
| `DES-REV-036` / blocking P2 | the Requirements main definition still used present-tense Requirements-only continuation wording that said Design projection revision and fresh review remained for the next stage, contradicting the current 50/50 mapping, fresh Design review, deterministic closure and refactor eligibility | the historical Requirements-only stop is now explicit, while the current continuation projects the completed Design gate, Phase 1 stop and no-runtime/no-resource-creation boundaries | closed in revised candidate; current fresh review passed |
| `DES-REV-037` / blocking P2 | Requirements required closure and delivery terminal before Finish, while the same current contract required Finish to create archive/Ready/`ready_for_merge` before Merge and Closure, deadlocking both supported delivery routes | Requirements scenarios, functional order, state graph, fixtures and capability projection now match the current Design order: GitHub Publication/Draft PR -> Finish -> Merge -> Closure -> terminal -> Cleanup, and none Acceptance -> Finish -> Closure-N/A -> terminal -> Cleanup | closed in revised candidate; current fresh review passed |
| `DES-REV-038` / blocking P2 | the none-route public contract emitted `delivery_fact_ref` from Acceptance, consumed it as a Finish input and emitted the same-named ref again after Finish, contradicting the required Acceptance -> Finish -> delivery-fact order and leaving no unique stage identity | none Acceptance now emits only `acceptance_ref`; `guru-finalize-task:none` consumes only task/acceptance identity and is the sole none-route `delivery_fact_ref` producer after its durable result is current; Requirements semantics, fixtures, traceability, capability and Architecture projections assert zero pre-Finish delivery fact | closed in revised candidate; current fresh review passed |
| `DES-REV-039` / blocking P2 | Requirements Section 0, task PRD and Architecture contribution still described fresh Design as pending/stale after the same current candidate declared its fresh Design review, deterministic closure and refactor eligibility current, so supported authority readers could repeat or reject the completed gate | all current-stage projections now distinguish the historical pre-`REQ-REV-133` stale binding from the reviewed current target planning, bind the completed Phase 1 Design gate and preserve zero runtime/delivery/shared-current action | closed in revised candidate; current fresh review passed |
| `DES-REV-040` / blocking P2 | the Requirements current-capability inventory completion contract still said the current result only allowed a later fresh Design and that Design still had to complete successor mapping/review, after the same exact candidate already declared those steps and `evolution_refactor_eligible` current | inventory item 13 now distinguishes the Requirements-stage result's own proof boundary from the later current Design-stage result and explicitly forbids repeating the completed Design gate | closed in revised candidate; current fresh review passed |
| `DES-REV-041` / blocking P2 | the supposedly independent Branch Review discriminators prohibited `promotion_kind=none,projection_kind=authority_only`, leaving the normal state “shared RDT/Architecture current, authority locator/usage/freshness projection missing or stale, no same-range code-spec contribution” without a constructible repair route | the closed matrix now permits `authority_only` with any promotion kind including `none`, keeps double-none only for a fully current authority/projection target, reserves `with_code_spec` for a same-range code-spec ref, and synchronizes the router, fixture, Test, Architecture and task projections | closed in revised candidate; current fresh review passed |
| `DES-REV-042` / blocking P2 | `guru-publish-task-pr` declared complete separate refusals for provenance preparation, branch push and Draft-PR creation, but the branch-push refusal had no output/consumer and the Draft-PR path had no refusal exit/output/consumer, so two supported normal refusal paths were not constructible | the public contract now closes `branch_push_not_executed -> task_ref,acceptance_ref,publication_head_ref -> task-branch-push-not-executed` and `pr_creation_not_executed -> task_ref,acceptance_ref,published_head_ref -> task-pr-creation-not-executed`; Design, Test, Architecture and task projections require three distinct action-local zero-side-effect consumers | closed in revised candidate; current fresh review passed |
| `DES-REV-043` / blocking P2 | the task finding ledger marked `DES-REV-042` as fresh-review pending while supported Design/Test/Architecture/task projections still bound the current pass to `DES-REV-001..041` and exposed `fresh_design_review_passed` / `evolution_refactor_eligible`, so a normal downstream reader could consume stale pre-042 gate evidence | every current gate projection now binds the complete `DES-REV-001..043` set, includes the three publication-refusal subgraphs and this stale-projection correction, reports zero open findings only for that exact candidate, and preserves the Phase 1/no-runtime boundary | closed in revised candidate; current fresh review passed |

## Architecture Alignment

- profile: `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`.
- impact/path: `architecture_impact` / `target_native`.
- current at selected base: `current-main-0.6.5-guru.41`, source baseline
  `651defee871d4bb07683547df09d1e0ac62b4a49` + #311 serialized promotion delta, constitution
  `guru-trellis-design-constitution-v1`, change contract
  `guru-trellis-architecture-change-contract-v1`.
- task contribution:
  `docs/architecture/contributions/305-evolution-workflow-convergence.md`.
- contribution state: `design_ready_for_delivery_planning` / `fresh_design_review_passed` / `not_promoted`.
- hit principles: `concept-semantic-completeness`, `cohesion-change-isolation`,
  `minimum-necessary-complexity`, `debt-one-way-convergence`.
- ADR: `ADR-305-CANDIDATE` is required because owner topology, compatibility exit, stock ownership and
  activation semantics change; it remains candidate and is not added to the shared ADR index here.
- shared-current writer: none in this task. Future reviewed promotion remains expected-current serialized.

All required Architecture concerns are applicable and explicitly filled in the contribution. There is no
compatibility layer; dormant target source may be built serially, but runtime cutover is atomic.

## Design Deliverables

| Repository authority | Task-specific purpose |
| --- | --- |
| `docs/design/evolution/design-main.md` | complete invocation/workflow, recovery, distribution, stock and RDT/Architecture behavior |
| `docs/design/evolution/contracts.md` | 39 public Skill contracts, profiles, constructible input/output projections and consumers; private envelope/reference/worker/provider adapters |
| `docs/design/evolution/stock-and-distribution.md` | exact 17-asset/9-retained-row action, concrete raw-meta/update-spec successor proof and install/migration/activation design |
| `docs/design/evolution/capability-inventory.md` | current capability and target delta successor closure |
| `docs/design/evolution/traceability.md` | Requirements/NFR/Design/Test set allocation |
| `docs/design/evolution/decisions.md` | accepted/rejected design directions |
| `docs/design/evolution/delivery-plan.md` | ten serial future implementation/matrix/Release suggestions |
| `docs/test/evolution/` | 50 fixture contracts with candidate `EVO-DES-001..073` mapping; all remain `planned_not_executed` |
| Architecture contribution | target-native decision, GAP/owner/compatibility/ADR candidate |

## Design Gate

The selected base already contains accepted #311/#312 merges, exact `.41` RDT/Architecture/capability identities are
rebound, and the complete 83-requirement / 13-target-delta / 50-fixture Requirements-stage successor set has zero gap.
The merge-bound Requirements candidate has passed both fresh full-document reviews. This continuation has allocated
successors/mappings for all current Requirements and fixtures and has now completed a fresh independent semantic
review of the complete Design/Test/Architecture/task-planning candidate. That review reported open `P1=0`, blocking
`P2=0`, `P3=0`, high-risk question `=0`.

The fresh review explicitly closed `DES-REV-001..043`; lexical presence without the three publication subgraphs,
their already-current no-mutation exits, the reference caller/return contract, a projection trigger/return chain that
includes zero-promotion authority-only repair and converges from the complete diff to outstanding-work double-none,
direct bound-event delivery, complete authority/
provider ownership, the exact 37-owner/two-specialist lifecycle partition, the standalone
Projection/Stock/Projection fresh-validation chain, the compound activation/implementation-entry confirmation and
the exact-current Workspace no-mutation path and current Phase 1 stop boundary is not sufficient.

Current result: `REQ-REV-133..138` invalidated the pre-`REQ-REV-133` review result and split Requirements readiness
from refactor eligibility. Selected-base authority rebind and Requirements-stage zero-loss are current; Design/Test/
Architecture/task projections now carry `design_ready_for_delivery_planning` / `fresh_design_review_passed` /
`evolution_refactor_eligible`, with 73 Design responsibilities and all 50 fixture mappings allocated. This
continuation remains in Phase 1 and stops at the completed Design review and deterministic closure.

The gate does not activate the task or authorize code, stock mutation, install/migration execution, commit, remote
delivery or Release.
