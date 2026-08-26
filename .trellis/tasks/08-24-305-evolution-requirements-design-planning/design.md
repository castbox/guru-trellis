# #305 Evolution Design Planning Projection

## Authority

- Change authority: GitHub Issue #305.
- Requirements: `docs/requirements/evolution/` with current `requirements_ready_for_design` /
  `requirements_trace_ready_for_design`, bound to `evolution-requirements-revision-2026-08-27` and
  `REQ-REV-011..132`; this Design projection is `requirements_input_current` / `design_ready_for_delivery_planning`.
- Target Design: `docs/design/evolution/` / `guru-trellis-evolution-design-2026-08-26` /
  `design_ready_for_delivery_planning`.
- Target Test: `docs/test/evolution/` / `guru-trellis-evolution-test-2026-08-26` /
  `test_candidate_planned` / `design_ready_for_delivery_planning`.
- Current as-built authority: `.40` RDT/Architecture at
  `d907fcc5e17f23b6499648e5e9a208457f2d6f8b`; target docs do not replace current before reviewed
  implementation/promotion.

This file is a task projection. Design behavior and public contracts are owned only by repository Design.

## Current-To-Target Reconciliation

Current capability is preserved by `docs/design/evolution/capability-inventory.md`: all
`CUR-CAP-001..023` have target owners/fixtures, and all `TARGET-DELTA-001..013` have Design allocation.
Private current schemas, wrapper routes, aggregate gate artifacts and 21/89 magic counts are not preserved as
target API.

Target decisions:

- retain marketplace workflow id `guru-team` but introduce `guru-team-evolution-contract-1.0` and mandatory
  atomic existing-repository migration;
- use one private invocation `context_envelope`, lazy authority/provider projections and consumer-minimal public
  results; section owners perform initial/targeted live reads, consumers do not repeat unchanged full reads, and
  every public input is constructible without a generic frame/private/ambient lookup;
- use one plan author/one approval and one standard implementation owner;
- split Delivery, Acceptance, Publish, Merge, Closure, Finish, Cleanup and history by exact ownership/re-entry;
- split Publish further into independent branch-push and PR-create prepare/wait/confirmation/refusal/recovery stages,
  with live already-current remote branch/READY PR paths advancing without mutation or confirmation;
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
| Requirements change | `EVO-REQ-081`, `TARGET-DELTA-013`, `EVO-DES-069` and the 47th semantic-confirmation fixture are bound to the current passed Requirements gate; the revised projection then passed the fresh Design gate | closed in reviewed candidate |
| Requirements status projection | `EVO-EVD-043` made the prior ready binding stale; `REQ-REV-129..132` have now passed the fresh gate, and Design/Test/Architecture/task projections bind the same `evolution-requirements-revision-2026-08-27` ready identity | requirements input current; fresh Design review passed |
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
| `DES-REV-001` / blocking P2 | `guru-publish-task-pr` previously combined branch push and PR creation behind one confirmation boundary. It now has disjoint `push_prepare/push_confirmation_reentry/push_provider_reentry` and `pr_create_prepare/pr_creation_confirmation_reentry/pr_provider_reentry` graphs, two named waits, two refusal targets and two recovery routes; push confirmation cannot authorize PR creation | closed in revised candidate; fresh review passed |
| `DES-REV-002` / blocking P2 | raw `trellis-meta` managed absence previously pointed only to descriptive “lazy reference” prose. The candidate now defines preset-single-written `guru-trellis-reference-manifest-1.0`, fixed source precedence, caller-bound `guru-trellis-reference-read-adapter-1.0` standalone/embedded profiles, synchronous return and active/new-change write routing | closed in revised candidate; fresh review passed |
| `DES-REV-003` / blocking P2 | raw `trellis-update-spec` managed absence previously lacked one projection owner, review trigger and downstream recheck. Branch Review now selects independent promotion/projection discriminators: only exact double-none enters delivery, while Bootstrap `projection_refresh` is the sole `.trellis/spec` writer for `authority_only|with_code_spec` after any selected promotion is current. The latter requires a same-range contribution ref even when no authority promotion is selected; both emit `guru-code-spec-projection-1.0` and return only through fresh Check/Commit/Branch Review | closed in revised candidate; fresh review passed |
| `DES-REV-004` / blocking P2 | promotion/projection previously selected from contribution presence in the complete diff without distinguishing outstanding work from target identities already made current, so the mandatory fresh Check/Commit/full-diff review could select the same work forever. Branch Review now live-compares authority/contribution/projection targets, emits refs only for not-yet-current work, permits exact `promotion_kind=none,projection_kind=none` when the complete diff still contains already-current changes, and reopens only material drift; Bootstrap returns an already-current projection without rewriting it | closed in revised candidate; fresh review passed |
| `DES-REV-005` / blocking P2 | the accepted-route router invoked undeclared `guru-publish-task-pr:push`, publication wording called recoverable `push_blocked/pr_blocked` terminal, and no explicit already-current branch/PR convergence path prevented repeated confirmation or mutation. The router now invokes `push_prepare`; every publication entry live-rereads state, exact remote HEAD and exact READY PR return no-mutation `branch_published/ready_pr_current`, divergent state uses stage-specific recoverable re-entry, and push/PR-create continuations remain disjoint | closed in revised candidate; fresh review passed |
| `DES-REV-006` / blocking P2 | `lifecycle_bound` previously projected only sequence/order to the selected owner, so the owner could not consume the causally bound host event without an ambient history lookup. Admission and the closed router now carry `bound_event_ref,event_sequence` directly; the ref binds host event identity/session/current content and no new envelope/receipt is created | closed in revised candidate; fresh review passed |
| `DES-REV-007` / blocking P2 | stable authority content had no complete subprojection ownership contract, and `provider_context` named only a delivery-oriented consumer subset. Clarification, RDT and Architecture now exclusively own their applicable authority subprojections while downstream semantic owners use the same bound content; the provider inventory now covers every declared Git/GitHub/Trellis-upstream/Guru-preset/Release action and controlled adapter with an exact owner | closed in revised candidate; fresh review passed |
| `DES-REV-008` / blocking P2 | approved Planning previously entered `phase-1-task-activation` without a declared successor or failure contract. Activation is now an Approval-internal deterministic substep: only a current transition emits `approved -> task_ref` and immediately invokes `guru-implement-task:initial`; objective failure remains in Approval recovery | closed in revised candidate; fresh review passed |
| `DES-REV-009` / blocking P2 | task `implement.md` previously made the current Design-review continuation proceed into wording, RDT/Architecture impact and task-plan approval before binding Design readiness. The current sequence now binds `design_ready_for_delivery_planning` immediately after a clean fresh Design gate and stops; all later Planning gates require a separate continuation and cannot be inferred from this review confirmation | closed in revised candidate; fresh review passed |
| `DES-REV-010` / blocking P2 | the lifecycle registry previously omitted five legal owners: Admission, Route Request, Answer, Current Work and History. Section 3.1 now defines exactly 37 lifecycle owners including those five; Wording and Qualification are the only two public specialist non-owners and their fixed original caller retains lifecycle ownership | closed in revised candidate; fresh review passed |
| `DES-REV-011` / blocking P2 | standalone Stock had a `standalone` profile but no exact producer. Projection is now its sole caller; Stock current returns only to Projection `stock_policy_reentry`, which freshly validates the complete surface before completion. Stock does not terminate the workflow or create a fifth distribution route | closed in revised candidate; fresh review passed |
| `DES-REV-012` / blocking P2 | Planning previously displayed only task activation before directly entering Implementation, so the confirmation did not cover the full next action. Approval now displays one compound plan with activation plus immediate approved implementation scope/allowed writes, excludes Commit and later delivery, and permits Implementation only after a current transition; transition failure writes nothing | closed in revised candidate; fresh review passed |
| `DES-REV-013` / blocking P2 | Workspace `create_or_reuse` previously required a displayed plan and confirmation even when the exact resource set was already current. Workspace now live-resolves resource plus ownership/isolation state first, returns `workspace_current -> task_impact_sync` with zero plan/confirmation/refusal/mutation for exact-current reuse, and enters the confirmation boundary only for pending creation/transfer/isolation | closed in revised candidate; fresh review passed |
| `DES-REV-014` / blocking P2 | after `DES-REV-013`, generic decision/delivery/capability/gate wording still required every potential side-effect owner to display a plan and own a refusal, so exact-current Workspace could be routed back into a confirmation loop. The shared rule now first resolves whether an action remains: every no-mutation current exit bypasses plan/confirmation/refusal, exact-current Workspace is explicitly closed in contracts/gates/slices, and only a pending action enters its owner-local confirmation graph | closed in revised candidate; fresh review passed |

## Architecture Alignment

- profile: `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`.
- impact/path: `architecture_impact` / `target_native`.
- current: `current-main-0.6.5-guru.40`, constitution
  `guru-trellis-design-constitution-v1`, change contract
  `guru-trellis-architecture-change-contract-v1`.
- task contribution:
  `docs/architecture/contributions/305-evolution-workflow-convergence.md`.
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
| `docs/test/evolution/` | evidence strategy and 47 planned fixture contracts |
| Architecture contribution | target-native decision, GAP/owner/compatibility/ADR candidate |

## Design Gate

The target is ready for delivery planning only after the current Requirements candidate first reaches its ready
gate, deterministic set/link/table closure passes, and a fresh
independent semantic review of the complete Design/Test/Architecture/task-planning candidate reports open
`P1=0`, blocking `P2=0`, `P3=0`, high-risk question `=0`.

The fresh review must explicitly close `DES-REV-001..014`; lexical presence without the two publication subgraphs,
their already-current no-mutation exits, the reference caller/return contract, a projection trigger/return chain that
converges from the complete diff to outstanding-work double-none, direct bound-event delivery, complete authority/
provider ownership, the exact 37-owner/two-specialist lifecycle partition, the standalone
Projection/Stock/Projection fresh-validation chain, the compound activation/implementation-entry confirmation and
the exact-current Workspace no-mutation path and current Phase 1 stop boundary is not sufficient.

Current result: the revised exact candidate closed `DES-REV-001..014`, passed the fresh independent full Design
review and deterministic planning closure on `2026-08-27`, and has open `P1=0`, blocking `P2=0`, `P3=0`, high-risk
question `=0`. Design/Test/Architecture/task projections are bound to
`design_ready_for_delivery_planning`, and this continuation stops in Phase 1.

The gate does not activate the task or authorize code, stock mutation, install/migration execution, commit, remote
delivery or Release.
