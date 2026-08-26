# #305 Evolution Workflow Convergence Architecture Contribution And ADR Candidate

## Candidate Identity And Authority Boundary

- candidate identity: `architecture-contribution-305-evolution-workflow-convergence-v1`.
- requirement authority: `docs/requirements/evolution/` with current gate `requirements_ready_for_design` /
  `requirements_trace_ready_for_design`, bound to `evolution-requirements-revision-2026-08-27` and
  `REQ-REV-011..132`; this contribution is `requirements_input_current` / `design_ready_for_delivery_planning`.
- behavior authority: `docs/design/evolution/` and planned `docs/test/evolution/`.
- task: `08-24-305-evolution-requirements-design-planning`.
- current Architecture: `docs/architecture/README.md` / `current-main-0.6.5-guru.40` / `active`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`.
- impact/path: `architecture_impact` / `target_native`.
- contribution state: `design_ready_for_delivery_planning`.
- promotion state: `not_authorized_not_started`; expected current at any future promotion is freshly reread live
  current, not a value reserved by this planning document.

This contribution describes a target decision. It does not make the target graph, stock policy, contract identity
or Release current, and it does not modify shared Architecture or the ADR index.

## Boundary And Decision

Current `.40` implements a four-Phase Guru workflow with 21 active public Skill packages and 89 exits. It already
owns strong RDT/Architecture, review, provider and finalization capabilities, but the top-level flow still assumes
file-changing task work as the dominant entry, task planning carries too much coordination context, standard
implementation lacks one explicit owner, and official Trellis stock Skills/workers can remain discoverable beside
Guru owners after projection. Current verifier/finalizer boundaries also aggregate responsibilities that the
Evolution lifecycle needs to route and recover independently.

The target boundary is one user invocation from admission to exactly one terminal. It introduces:

1. `guru-team-evolution-contract-1.0` with 39 public closed-loop Skills and uniquely consumed external exits;
2. one private invocation-scoped `guru-context-envelope-1.0` whose stable primary prefix is applicable repository
   RDT -> Architecture Baseline/constitution/change contract -> task `prd.md`/`design.md`/`implement.md`, with lazy
   stock/provider/implementation projections and a minimal decision-relevant live tail; cache is optional and never
   authority, while each AI owner judges the same applicable bound content directly without assignment/signoff/
   transaction handoff or fact restatement. Clarification, RDT and Architecture own disjoint requirement-delta/
   reviewed-design, repository-RDT and baseline/constitution/change-contract subprojections respectively;
3. one standard plan author and one approval, plus one standard implementation owner. Approval displays one compound
   exact next-action plan covering both task activation and immediate entry into the approved implementation
   scope/allowed writes while excluding Commit and later delivery actions; it owns the post-confirmation deterministic
   activation substep and, only after its transition is current, closes directly as
   `approved -> guru-implement-task:initial`; activation is not an extra router or terminal;
4. target-native delivery, history, Finish and Cleanup owners with exact failure re-entry;
5. a Guru preset-owned post-projection stock policy for the frozen 17 assets and nine retained host rows;
6. one activation manifest and mandatory existing-repository migration that cut over atomically with zero legacy
   consumer after activation;
7. one dialogue-local semantic confirmation invariant used only when a real choice or side effect remains pending:
   no-mutation current exits bypass plan display/confirmation/refusal, while pending actions accept clear affirmation
   after an unchanged exact plan, preserve exact-action scope only, and require zero fixed prompt/password/hash/digest/task/path/branch/
   SHA/identity/summary/prescribed-wording challenge, `确认执行 <hash>`, scripted reply parsing or authorization
   state; every refusal has one owner-specific zero-side-effect output, and merge/closure/Finish/Cleanup confirmations
   never inherit from one another, including active-lifecycle disposition cleanup.
8. one closed edge-construction rule: every consumer input is satisfied by the selected public exit projection or
   resolved by that consumer's exact live-fact owner; generic frames, implicit pass-through and private/ambient
   lookup cannot fabricate missing fields. Release pending/unknown progress and true partial publication use
   disjoint recovery identities.
9. profile-fixed opaque caller continuations for cross-owner clarification and Bootstrap: qualification scope goes
   through the unique Clarification owner and back to the original caller for fresh candidate reconstruction and
   qualification; RDT/Architecture incomplete requests return only to their exact authority owner's
   `bootstrap_reentry`, with no origin inference from task, checkpoint, envelope file or ambient state.
10. one complete recovery topology: exactly 37 of the 39 public Skills are registered lifecycle owners, including
    Admission, Route Request, Answer, Current Work and History; Wording and Qualification are specialist non-owners
    whose fixed original caller retains ownership. Every ordinary recoverable block has one producer-owned continuation and one
    same-owner profile; nine wording profiles and ten active four-result qualification profiles return only the
    original caller's opaque continuation, while standalone qualification has only its three applicable results;
    terminal/new-invocation results have no fake continuation. Clean, Migration and standalone Stock transaction
    refusals retain only their exact action continuation, and controlled adapter outputs carry no generic caller ref.
11. one closed lifecycle and retained-context topology: `lifecycle_bound` sends
    `lifecycle_ref,bound_event_ref,event_sequence` through the closed router to the registered exact owner, where the
    ref binds host event identity/session/current content and forbids sequence-only or ambient-history recovery;
    four irreversible remote owners converge through one named wait before Disposition re-entry;
    post-owner and post-remote pending intent use distinct fresh Admission profiles. Admission binding/isolation and
    Answer provider recovery stay distinct, cleanup refusal with a current choice bypasses the later-choice wait,
    R01..R09 bind nine exact host context owners, and all suppressed rows share only the Route Request success edge.
12. one Guru-owned Trellis reference boundary replacing raw `trellis-meta`: the preset transaction single-writes
    `guru-trellis-reference-manifest-1.0`, caller-fixed `guru-trellis-reference-read-adapter-1.0` profiles read it
    lazily, and all writes enter active/new-change governance before adapter invocation.
13. one `.trellis/spec` projection single writer replacing raw `trellis-update-spec`:
    Branch Review independently selects only authority promotion and `none|authority_only|with_code_spec` projection
    work not already current at live target identities; `guru-bootstrap-repository-ssot:projection_refresh` runs for
    the latter two only after all selected RDT/Architecture promotion is current, requires a same-range contribution
    ref that is still missing from current projection for `with_code_spec`, writes only a missing
    `guru-code-spec-projection-1.0`, and returns through fresh Check/Commit/Branch Review. That complete-diff review
    recognizes already-current targets and converges to exact `promotion_kind=none,projection_kind=none`; material
    drift reopens the affected owner instead of replaying current work.
14. two independent PR-publication side effects inside the Publish owner: branch push and PR creation have separate
    prepare/wait/confirmation-reentry/refusal/provider-recovery identities, so push confirmation cannot authorize PR
    creation. Every entry first rereads live state: an exact remote branch already at the bound HEAD or exact
    base/head PR already live READY advances without mutation or confirmation, while divergent state stays in the
    corresponding recoverable stage. Merge remains a third independent owner/action.
15. one standalone stock-maintenance subgraph: Projection alone may call Stock, Stock current returns only to
    Projection `stock_policy_reentry`, and Projection freshly validates the complete surface before the workflow can
    complete. Stock never creates a fifth distribution route or owns the top-level terminal.

Marketplace workflow id `guru-team` remains stable as the distribution entry. The runtime contract behind it is a
new breaking identity. Stable id retention is therefore paired with an explicit migration contract, not a claim
of old/new API compatibility.

## Required Concern Review

| Concern | Applicability | #305 candidate contract |
| --- | --- | --- |
| `authority-binding` | applicable | bind Guru Architecture 2.0, active `.40`, current RDT, constitution and change contract; target docs never claim current runtime |
| `constitution-binding` | applicable | hit `concept-semantic-completeness`, `cohesion-change-isolation`, `minimum-necessary-complexity`, `debt-one-way-convergence`; no principle prose copied into public DTOs |
| `boundary-and-decision` | applicable | one invocation boundary, 39-Skill owner graph, private envelope, stock control plane and atomic activation are the selected target |
| `owner-and-single-writer` | applicable | every semantic step has one Skill owner; stock policy has one preset transaction owner; reapply is fixed to Existing Migrator; shared RDT/Architecture promotion remains serialized |
| `compatibility-and-exit` | applicable | `target_native`; no legacy adapter/selector/dual-read; migration final validation proves zero legacy consumer before activation |
| `gap-and-deviation` | applicable | plan closes current entry/implementation/stock/distribution ownership gaps; no release GAP or unrelated current debt is absorbed |
| `parallel-scope` | applicable | future slices may build dormant target packages in isolated tasks; activation and shared-current promotion each remain single-writer |
| `evidence-and-freshness` | applicable | Planning is bound to the current `requirements_ready_for_design` / `requirements_trace_ready_for_design` identity for `REQ-REV-011..132`; the stable RDT/Architecture/task-doc prefix, minimal live tail, cache-non-authority and AI-owned judgment constraints are explicit, and the revised exact candidate passed fresh Design review. Each public edge proves consumer-input construction without hidden state, and later stages bind their exact implementation or committed range and rerun affected gates |
| `review-and-promotion` | applicable | fresh independent Design review precedes delivery planning; implementation contribution/ADR promotion requires later committed full-diff review and expected-current reread |

## Owner And Single-Writer Model

| Boundary | Current/target owner rule |
| --- | --- |
| top-level admission and lifecycle binding | target `guru-admit-invocation`; `lifecycle_bound` carries a host identity/session/current-content `bound_event_ref` plus monotonic `event_sequence` directly to one of exactly 37 registered owners, including Admission/Route Request/Answer/Current Work/History; Wording/Qualification remain specialist non-owners under their fixed original callers; lifecycle-binding and post-receipt isolation blocks have different owner re-entry, post-owner/post-remote pending intent uses two fresh-entry profiles, and hooks/stock surfaces cannot create a second entry or ambient event lookup |
| route selection | `guru-route-request`; secondary mode/distribution classification remains with its exact route owner |
| task planning | `guru-plan-task`, then one `guru-approve-task-plan` review; one displayed compound plan covers activation plus immediate approved implementation entry/allowed writes and excludes Commit/later delivery; its confirmed deterministic activation is an internal substep whose current transition alone emits `approved -> guru-implement-task:initial`, while objective failure remains in Approval recovery with zero implementation write |
| standard implementation | `guru-implement-task`; worker is caller-bound evidence/execution only |
| RDT / Architecture | Clarification owns current requirement-delta/reviewed-design binding, RDT owns repository RDT, and Architecture owns baseline/constitution/change-contract; applicable downstream owners use the same stable bound content, task contributions are isolated and shared current is serialized |
| `.trellis/spec` projection | `guru-bootstrap-repository-ssot:projection_refresh` after outstanding reviewed promotion/code-spec work; already-current target returns without write, fresh committed review converges to double-none, and no raw Skill/preset/worker writer exists |
| Trellis reference | preset transaction writes the manifest; profile-fixed adapter reads for Answer/exact embedded caller; writes use active/new-change owner |
| stock source | official Trellis package remains source owner |
| stock action/provenance | current ownership 3.0 forbids upstream-path mutation; one preset transaction first validates ownership 4.0 exact post-projection claims, then `guru-maintain-stock-projection` may act without acquiring source ownership. Standalone action is produced only by Projection and returns current only to its `stock_policy_reentry` for fresh full validation; Stock never completes the route |
| provider result | closed Git actions cover Sync, task-free/standard local write, Commit and branch Publish; GitHub covers PR Publish, Merge and Closure; Trellis upstream covers clean Install/existing Migration; Guru preset covers Install, Stock/Reapply and activation validation; Release owns its exact immutable-candidate stages and every controlled adapter is caller-fixed. Push/PR-create continuations and recoveries are disjoint, already-current remote branch/READY PR uses their no-mutation current exits, direct Answer promotes controlled-adapter block into its own recovery, Release zero-completed/unknown progress and true partial state are disjoint, and Merge/Closure recovery carries exact continuation |
| side-effect confirmation | each exact semantic action owner first resolves whether an action remains. No-mutation current exits bypass plan/confirmation/refusal; otherwise the owner authors/displays its private plan, judges dialogue-local affirmation under the full item-7 prohibition set and owns one named zero-side-effect refusal output, including disposition cleanup. Exact-current Workspace reuse returns `workspace_current` with zero plan display, confirmation wait and mutation; scripts/schemas/DTOs never parse, match, validate or persist the reply/authorization |
| public input construction | selected exit projection or exact consumer-owned live-fact projection only; no generic frame, implicit relay, producer checkpoint, envelope-file or ambient runtime lookup |
| clarification/bootstrap return | exact producer profile plus unchanged caller-owned continuation; Clarification returns scope choice to the original qualification caller, while Bootstrap returns authority identities only to the originating RDT/Architecture owner |
| blocked/recovery return | ordinary blocks use the complete same-owner inventory in `contracts.md`; lifecycle owners come only from the closed registry, irreversible remote disposition uses the four-owner named convergence wait, wording/qualification use closed original-caller returns, and terminal blocks start a new invocation and cannot enter a repair profile |
| retained/adapter caller | retained R01..R09 profiles fix nine exact hook-policy/session/workflow-breadcrumb context owners and each controlled-adapter profile fixes its direct caller; no public caller id/ref is accepted or returned |
| activation | clean-install or migration transaction validates one activation manifest; no other writer |
| post-review authority promotion | Branch Review supplies a closed outstanding none/RDT/Architecture/both plan; deterministic router invokes only not-yet-current authority promotion owners serially, invokes Bootstrap-only missing spec projection refresh, then forces fresh Check/Commit/Review whose already-current result is exact double-none |
| this planning task | only Evolution Requirements/Design/Test, task planning projection and this contribution |

Platform commands, prompts, hooks and workers may load/route but cannot duplicate step-local semantics. Thin routers
only validate an already selected profile/exit and project to the declared consumer.

## Compatibility And Exit

- path: `target_native`. Dormant target packages may coexist in source before activation, but no runtime caller
  dual-reads old and target contracts.
- retained public entry: marketplace workflow id `guru-team` with new contract identity and mandatory migration.
- pre-cutover current: old workflow and recoverable lifecycle/history/ref state remain authoritative.
- cutover: explicit workflow force write or ordered byte-equal observation at the workflow-switch boundary,
  followed by preset reapply and one final validation.
- activation condition: workflow, registry/interfaces, runtime, stock policy, adapters/workers and selected host
  projections all bind the same candidate, including ownership contract 4.0/schema/validator, Trellis reference
  manifest/adapter and code-spec projection contract; target consumer count
  before activation is zero. Current ownership 3.0 never authorizes stock mutation.
- exit condition: after activation, old registry/schema/route/private artifact consumer and raw discoverable stock
  semantic/worker counts are zero; retained historical data remains reachable through the new history owner.
- failure: pre-cutover returns preserved old current; post-cutover only forward-recovers to new current or remains
  migration-blocked. No fallback changes the selected contract.

## GAP And Deviation Ledger

| Candidate ref | Before | Target closure | Owner / proof |
| --- | --- | --- | --- |
| `ARCH-305-GAP-001` | no single admission owner covers every request family/latest-intent boundary | one admission/envelope/receipt/isolation contract and six routes; lifecycle-bound events carry identity/session/current content directly to the exact owner | admission/entry fixtures |
| `ARCH-305-GAP-002` | planning/context rereads and spec update owners overlap | stable RDT -> Architecture -> task-doc prefix plus minimal live tail, cache-non-authority, AI-owned direct judgment, three disjoint authority subprojection owners, exact Bootstrap caller return, complete provider action-owner inventory, Bootstrap-only convergent post-review `.trellis/spec` projection with already-current double-none exit, one author and one approval | Plan/RDT/Architecture/Provider/SSOT Bootstrap fixtures |
| `ARCH-305-GAP-003` | standard Phase 2 implementation caller is not a complete public owner and planning activation has no closed successor or complete authorization scope | one compound exact plan displays activation plus immediate approved implementation entry/allowed writes; Approval-internal deterministic activation closes directly to `guru-implement-task:initial`, and `guru-implement-task` plus bounded workers owns Phase 2 | Plan Normal/Full Normal/Branch Finding fixtures |
| `ARCH-305-GAP-004` | projected stock semantic/worker surfaces may compete with Guru owners and standalone stock action lacks a closed producer/return | exact 9/1/2/5 policy plus nine retained nonsemantic rows, manifest-bound meta successor, review-trigger-bound update-spec successor and sole `Projection -> Stock -> Projection fresh validation` standalone chain | Stock Coexistence/Maintenance/Projection fixtures |
| `ARCH-305-GAP-005` | distribution/finalizer responsibilities and recovery are aggregated | route-specific projection/install/migration/Release, separate push/PR-create/merge actions and delivery/Finish/Cleanup owners | distribution/recovery fixtures |
| `ARCH-305-GAP-006` | Workspace create-or-reuse conflates exact-current reuse with a pending resource mutation confirmation | live-resolve resource and ownership/isolation state first; exact-current reuse emits `workspace_current` with zero plan/confirmation/refusal/mutation, while only creation/transfer/isolation enters the confirmation boundary | Semantic Confirmation/Task Free/Full Normal fixtures |

These are task candidate refs, not active shared `ARCH-GAP-*` identities. Future promotion decides the successor
baseline identities after implementation evidence. Existing `.40` GAP/release ownership, including #267/#304
boundaries, is retained and not closed here. No new legacy deviation is planned.

## Parallel Scope

- allowed: separately reviewed delivery slices listed in `docs/design/evolution/delivery-plan.md`, each with an
  isolated task/worktree/branch/contribution and dormant target namespace until activation.
- allowed: read-only sharing of the same exact Requirements/Design/Test candidate and live current Architecture
  identity; downstream implementation slices start only after the planning gates freeze that candidate.
- forbidden: two activation writers, two shared-current promotion writers, partial host activation, direct edit of
  shared current before review, competing closure of the same GAP, or one slice consuming another's private state.
- stale rule: Requirements/Design/Architecture or predecessor public contract material change returns the slice to
  its earliest affected owner. A shared current advance requires fresh impact reconciliation before promotion.

## Before, After, Checks And Evidence

- before evidence: current `.40` Architecture/RDT plus current 21-Skill/89-exit inventory; frozen official Trellis
  `0.6.15` stock snapshot; current Evolution Requirements candidate with 51 UC, 81 REQ, 32 NFR, 23 current
  capabilities, 13 target deltas and 47 fixtures. Its live gate is currently `requirements_ready_for_design` /
  `requirements_trace_ready_for_design`; the `REQ-REV-011..132` projection remained current through the passed fresh
  Design review.
- after Design candidate: `EVO-DES-001..069`, 39 public Skill contracts with exactly 37 lifecycle owners/two
  specialist non-owners and a closed recovery inventory, exact
  17-asset/9-profile-fixed-retained-row decisions, independent Trellis-reference/code-spec-projection identities,
  one standalone Projection/Stock/Projection fresh-validation chain, one exact-current Workspace no-mutation path,
  one compound activation/implementation-entry confirmation, convergent already-current promotion/projection handling, isolated push/PR-create confirmation
  subgraphs with no-mutation current exits, a 47-fixture Test plan and ten serial delivery suggestions.
- Planning project check: fresh Design review and static set/link/table closure passed with `DES-REV-001..014`
  closed and open `P1=0`, blocking `P2=0`, `P3=0`, high-risk question `=0`. Planning wording, Architecture impact
  and task-plan approval are separately owned Phase 1 workflow evidence; they are not established or persisted by
  this Design-review result. No package/runtime/installed/provider/Release evidence exists in this planning task.
- later evidence: each implementation slice must bind exact candidate/range, execute only its owned fixtures and
  record unverified matrix boundaries. Atomic migration and full matrix/Release cannot be inferred from ordinary
  slice tests.
- freshness: current planning authority ref is `d907fcc5e17f23b6499648e5e9a208457f2d6f8b`; any live authority advance
  is reread and semantically reconciled before a later stage uses this result.

## ADR-305-CANDIDATE

- status: `candidate_design_reviewed_not_promoted`; not an accepted ADR.
- trigger: #305 changes long-term system boundary, public owner topology, compatibility strategy, stock
  projection ownership and activation semantics.
- decision: adopt the target-native Evolution contract with one invocation envelope, one semantic owner per
  closed step, preset-owned exact stock projection policy, manifest-bound Trellis reference, Bootstrap-only minimal
  code-spec projection, separate push/PR-create actions and atomic existing-repository migration under the retained
  `guru-team` marketplace id.
- rejected: patching stock prompts while keeping their matchers; modifying upstream/global package state; keeping
  raw stock providers/workers discoverable; task artifacts as repository RDT; old/new dual-read or fallback;
  partial platform activation; one finalizer/verifier aggregate owning unrelated semantic terminals.
- consequence: implementation is split into dormant serial slices and activates only when the full graph is
  current. Existing repositories require an explicit migration; unknown/user-modified/sidecar state blocks rather
  than being overwritten. Runtime context and handoffs shrink, while semantic reviews and capability evidence
  remain mandatory at their unique owners.
- acceptance condition: reviewed implementation of every selected owner/action, all 47 applicable fixture families,
  full committed-diff review, reviewed task contribution/ADR, expected-current serialized promotion, atomic
  migration proof, full declared matrix and exact-candidate Release at their dedicated owners.

## Explicit Boundaries

- #305 ends at reviewed Requirements/Design/Test/planning and delivery suggestions. It does not implement or
  activate any target contract.
- This contribution does not create delivery Issues, change #267/#304, initialize submodules, modify current
  Architecture/RDT, publish a tag/Release or claim any fixture executed.
- Official Trellis documentation and supported extension surfaces remain authoritative for implementation;
  package internals are evidence, not a Guru public API.
