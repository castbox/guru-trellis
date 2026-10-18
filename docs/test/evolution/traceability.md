# Evolution Test Traceability

状态：`test_candidate_planned` / `fresh_design_review_passed` / `evolution_refactor_eligible`. The execution-contract mapping is the 50-row table in
[`fixture-plan.md`](./fixture-plan.md); this file owns cross-authority set closure without duplicating fixture steps.

## 1. Requirements To Fixture Families

| Authority set | Fixture families |
| --- | --- |
| `EVO-REQ-001..009` | Intake Clear/Reviewed Design/Unclear, Detached Read, Base Refresh, Tech Revision |
| `EVO-REQ-010..011` | Entry Routing, Request Stop, Task Free, No Issue, Semantic Confirmation exact-current Workspace reuse, Active Disposition |
| `EVO-REQ-012..026` | Plan Normal, all Architecture planning/freshness fixtures, SSOT Bootstrap |
| `EVO-REQ-027..033` | Full Normal, Branch Finding, Base Evolution, Architecture Promotion with outstanding-only spec projection refresh and already-current double-none convergence, Parallel, RDT freshness |
| `EVO-REQ-034..043` | Entry Routing, None, Full Normal, Semantic Confirmation with separate provenance-tail/push/PR-create actions and already-current no-mutation exits, Provider/Finish Recovery, History Resume, Active Disposition |
| `EVO-REQ-044..050` | Plan Normal, Full Normal, Latest Intent, Long Output, including host-continuation-only pre-task/standalone recovery and same-owner task checkpoint ownership |
| `EVO-REQ-051..056` | Full Normal, Projection, Provider Recovery, Clean Install, Migration, Release |
| `EVO-REQ-057..058` | Wording Explicit, Qualify Explicit with profile-fixed Clarification, original-caller candidate rebuild and fresh qualification |
| `EVO-REQ-059..067` | Change Request, Base Refresh, SSOT Bootstrap with exact RDT/Architecture caller return and projection-refresh return to Check, RDT Lifecycle/Freshness, Submodule Boundary, Active Disposition |
| `EVO-REQ-068..080` | Stock Coexistence with concrete meta/update-spec successors, Stock Maintenance, Entry Routing, SSOT Bootstrap, Clean Install, Migration, Projection |
| `EVO-REQ-081` | Semantic Confirmation, including the three distinct Publish refusal exits/outputs/consumers; Active Disposition, Full Normal, Provider Recovery, Finish Recovery, Stock Maintenance, Clean Install, Migration, Release |
| `EVO-REQ-082` | Evolution Prerequisite, Installed Provenance Publication, Base Evolution |
| `EVO-REQ-083` | Verifier Failure Evidence, Evolution Prerequisite, Projection |
| `EVO-REQ-084` | Installed Provenance Publication, Evolution Prerequisite, Projection |

| Quality set | Fixture families |
| --- | --- |
| `EVO-NFR-001..008` | Plan Normal, Full Normal, Long Output, with zero generic repository-envelope state |
| `EVO-NFR-009..011` | Entry Routing, Latest Intent, Parallel, Provider/Finish Recovery, History Resume, Verifier Failure Evidence, with host-continuation isolation and same-owner task checkpoint boundaries |
| `EVO-NFR-012..013` | Projection, Clean Install, Migration, Release |
| `EVO-NFR-014..015` | Full Normal, Branch Finding, RDT/Architecture Downstream Freshness |
| `EVO-NFR-016` | Provider Recovery, Full Normal, Release, Verifier Failure Evidence |
| `EVO-NFR-017` | Semantic Confirmation, Active Disposition, Full Normal, Provider Recovery, Finish Recovery, Stock Maintenance, Clean Install, Migration, Release |
| `EVO-NFR-018` | Submodule Boundary |
| `EVO-NFR-019..032` | Stock Coexistence, Stock Maintenance, Entry Routing, Latest Intent, Projection, Migration |
| `EVO-NFR-033` | Evolution Prerequisite, Installed Provenance Publication, Verifier Failure Evidence, Base Evolution |
| `EVO-NFR-034` | Installed Provenance Publication, Evolution Prerequisite, Projection |

## 2. Design Responsibility To Fixture Families

The table below is the revised candidate projection over `REQ-REV-133..142`. The selected-base six-dimension
classification, authority rebind, merged-behavior reconciliation and Requirements-stage successor zero-loss are
current. `EVO-DES-070..073` allocate the two-stage eligibility gate, #312 original-worktree continuity, #311 installed
publication terminal and standalone verifier failure lifecycle; existing `EVO-DES-035/072` also carry PR #317 exact
platform-set preservation. The mapping is complete and current as a reviewed planning projection;
`evolution_refactor_eligible` is current while fixture execution remains pending.

| Design set | Fixture families |
| --- | --- |
| `EVO-DES-001..005` | Full Normal, Projection, RDT/Architecture Lifecycle |
| `EVO-DES-006..018` | Entry Routing, Request Stop, Latest Intent, History Resume and specialist fixtures; lifecycle-bound acceptance requires direct `bound_event_ref,event_sequence` projection to one of exactly 37 owners, including Admission/Route Request/Answer/Current Work/History, rejects sequence-only/ambient lookup, leaves Wording/Qualification ownership with their fixed original callers, and keeps admission/isolation cross-turn state in host continuation with zero repository-envelope write |
| `EVO-DES-019..022` | intake, task-free, change-request, base, detached-read and exact-current Workspace no-mutation fixtures |
| `EVO-DES-023..027` | Plan Normal, RDT Lifecycle and Architecture planning family; the one exact Approval plan must display activation plus immediate approved implementation entry/allowed writes, then its deterministic activation must close directly to `guru-implement-task:initial` or its own recovery block with zero implementation write |
| `EVO-DES-028..032` | Full Normal, Branch Finding, Base Evolution, promotion/projection/freshness fixtures |
| `EVO-DES-033..042` | Full Normal, Semantic Confirmation, None, Parallel, stage-specific provenance-tail/Push/PR-create Provider Recovery, Finish Recovery, History/Disposition |
| `EVO-DES-043..048` | Projection, Clean Install, Migration, Release, Provider Recovery |
| `EVO-DES-049..059` | Stock Coexistence, Stock Maintenance, Projection, Clean Install, Migration |
| `EVO-DES-060..064` | RDT Lifecycle/Freshness, all Architecture contribution/promotion fixtures, Bootstrap-only spec projection refresh |
| `EVO-DES-065..068` | Plan Normal, Full Normal, Long Output, Provider Recovery, Submodule Boundary; pre-task/standalone context is call/host-session-local and any task checkpoint has only its same Skill wrapper as consumer |
| `EVO-DES-069` | Semantic Confirmation, Active Disposition, Full Normal, Provider Recovery, Finish Recovery, Stock Maintenance, Clean Install, Migration, Release |
| `EVO-DES-070` | Evolution Prerequisite, Installed Provenance Publication, Verifier Failure Evidence |
| `EVO-DES-071` | Base Evolution, Evolution Prerequisite |
| `EVO-DES-072` | Installed Provenance Publication, Full Normal, Provider Recovery, Finish Recovery, Evolution Prerequisite |
| `EVO-DES-073` | Verifier Failure Evidence, Projection, Provider Recovery, Evolution Prerequisite |

## 3. Inventory Closure

- Each `CUR-CAP-001..023` has a target owner and fixture in
  [`../../design/evolution/capability-inventory.md`](../../design/evolution/capability-inventory.md).
- Each `TARGET-DELTA-001..013` has a Requirements allocation and acceptance family. #311 is no longer duplicated as
  a new target delta: its installed publication and verifier failure behaviors are current capabilities carried by
  `CUR-CAP-013/014/017/018/019` and target `EVO-REQ-037,053,082..084`; PR #317 exact platform-set preservation is
  folded into `CUR-CAP-013/014/017` and the same installed fixture.
- All 50 `EVO-FIX-*` identities have one Requirements execution-contract row and one Design planning mapping; the
  mappings are synchronized but not reused as pre-`REQ-REV-142` review proof.
- `EVO-FIX-EVOLUTION-PREREQUISITE` records six independent dimensions for each prerequisite. Its current positive
  sample is #311 PR #313/merge `21c7da1…` reachable with `OPEN + follow-up-only`, and #312 PR #314/merge
  `3efcce7…` reachable with `CLOSED`; neither lifecycle label substitutes for accepted scope, exact identity,
  reachability or accepted-scope finding verification. Inventory rebind, merged-behavior reconciliation and
  requirement/normal-path zero-loss is current for `origin/main@5650df47…`; fresh Requirements semantic, Strict
  technical and deterministic closure gates have passed, and the later fresh Design review/deterministic closure has
  made the Design successor allocation current.
- Stock acceptance expands to exactly 17 role rows, nine retained host rows, one shared layer, three supported
  hosts and the per-host setup partition defined by Design.
- Public contract acceptance derives the target Skill set live from `contracts.md`; the Design candidate contains
  39 unique public Skill identities across 43 profile rows. Routers/adapters are checked separately and do not
  inflate either public count.
- Lifecycle acceptance derives the closed Section 3.1 registry live: exactly 37 of those 39 public Skills own
  `lifecycle_intent_reentry|current_work_resume`; the five admission/answer/resolution owners are present, while
  Wording and Qualification are the two specialist non-owners whose fixed original callers retain ownership.
- Specialist closure expands the nine wording profiles and eleven qualification caller profiles, verifies all four
  results for the ten active qualification callers, verifies only classified/scope-confirmation/blocked for
  standalone, and returns each selected exit's unchanged caller continuation to exactly one original-caller re-entry.
- Recovery closure expands every `contracts.md` Section 7.1 row and verifies that ordinary recoverable blocks have
  exactly one constructible same-owner input, declared terminal blocks have no continuation, and Clean/Migration/
  standalone Stock refusal re-entry remains distinct from defect recovery. It separately closes Admission binding
  and isolation repair, Answer-owned provider recovery, the Section 3.1 lifecycle registry, named remote convergence,
  post-owner/post-remote fresh Admission and direct cleanup-refusal choice re-entry.
- Context closure proves Clarification, RDT and Architecture each own one disjoint `authority_context` subprojection,
  downstream semantic owners use the same applicable stable bound content rather than summary handoffs, and the
  complete Git/GitHub/Trellis-upstream/Guru-preset/Release plus controlled-adapter provider action inventory gives
  every declared action one exact owner/profile/direct consumer.
- Invocation-state closure proves admission/pre-route/pre-task/task-free/standalone cross-turn recovery uses only the
  current host continuation, generic files below `.trellis/tasks/**`, `.trellis/workspace/**` and
  `.trellis/.runtime/**` are zero, and any post-task private checkpoint is consumed and retired only by the same
  Skill public-wrapper rather than by another Skill.
- Publication confirmation closure proves provenance-tail preparation, branch push and Draft PR creation have
  distinct prepare/wait/confirmation-reentry/refusal/provider-recovery identities; no stage accepts another stage's
  continuation. Exact already-current tail, remote branch and Draft/READY PR return current results without mutation
  or confirmation. Draft PR enters Finish; Finish alone archives, pushes the archive head, marks Ready and emits the
  archive-bound `ready_for_merge_ref`; Merge cannot run before that result. On `none`, Acceptance emits only
  `acceptance_ref`, Finish accepts no delivery fact, and successful Finish is the sole `delivery_fact_ref` producer.
- Workspace confirmation closure proves exact matching resources and ownership/isolation return `workspace_current`
  without action-plan display, confirmation wait, refusal branch or mutation; only pending creation, transfer or
  isolation enters the confirmation graph.
- Stock closure binds R01..R09 to nine exact host context owners, keeps authorized downstream context projections
  consumer-minimal, gives all nine suppressed rows the single Route Request admission-success edge, and rejects
  caller-authored standalone identity or aggregate embedded-result shapes. It separately requires the
  preset-written Trellis-reference manifest/caller-fixed adapter family and the Bootstrap-owned
  code-spec-review-trigger-to-projection/fresh-review chain before raw meta/update-spec absence may pass; the chain
  selects only outstanding work and its fresh complete-diff review must converge already-current targets to exact
  double-none. Standalone stock action has exactly one producer and return path,
  `Projection -> Stock -> stock-policy-action-confirmation-wait -> Stock standalone_action_reentry -> Projection
  stock_policy_reentry -> fresh complete validation` when a mutation remains; no-confirm deterministic action may
  bypass only the wait, and no-mutation current bypasses the action subgraph. Embedded/reapply action-state variants
  use the same named wait before their profile-fixed re-entry. Missing confirmation, refusal and material drift remain
  zero-side-effect owner-local branches; Stock cannot complete the workflow or create a fifth distribution action.

## 4. Deterministic Planning Closure

The planning checker expands all `NNN..MMM` ranges and asserts exact equality for:

- `EVO-REQ-001..084`;
- `EVO-NFR-001..034`;
- `EVO-DES-001..073`;
- `CUR-CAP-001..023`;
- `TARGET-DELTA-001..013`;
- the frozen Requirements-stage set of 50 `EVO-FIX-*` identities.

It also checks local Markdown links, manifest locators, fixture table column counts, 39 unique public Skill
identities / 43 profile rows, exactly 37 lifecycle owners and two specialist non-owners, every named refusal/blocked
consumer and recovery profile, nine wording and eleven
qualification caller profiles, 17 stock decision rows, nine profile-fixed retained rows, one Trellis-reference
  manifest writer/adapter family, one convergent `.trellis/spec` projection writer/return chain covering
  zero-promotion `authority_only` repair and same-range `with_code_spec`, one standalone
  Projection/Stock/Projection fresh-validation chain, one exact-current Workspace no-mutation convergence path, one
  compound activation/implementation-entry confirmation, three isolated provenance-tail/push/Draft-PR confirmation
  subgraphs, one installed platform-preservation matrix with invalid identity blocked before extension source
  checkout/apply/commit, one Finish-before-Merge chain with no-mutation current exits and one Projection-owned standalone verifier
  evidence-before-cleanup lifecycle, zero generic invocation-envelope repository state and one same-owner consumer
  for every allowed task-local checkpoint.
These objective checks do not replace either semantic review. The fresh Requirements semantic, Strict technical and
fresh Design reviews are current. The checks verify deterministic closure for the same current candidate.

Prerequisite closure is deliberately two-stage: exact-base rebind plus requirement/normal-path fixture zero gap and
fresh Requirements review established `requirements_ready_for_design`; the subsequent Design successor/
fixture-mapping zero gap, fresh Design review and deterministic closure established `evolution_refactor_eligible`.
Both results are current, and the second remains not a precondition of the first. The Requirements fixture set includes #311's complete installed publication terminal
through Draft PR/archive/Ready/`ready_for_merge` with zero completed-mutation replay, evidence-before-cleanup
standalone verifier failure preservation, PR #317 exact installed platform-set preservation, and #312's unrelated-dirty
isolation alongside clean-tracked continuation and real blocker preservation.
