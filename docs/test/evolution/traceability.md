# Evolution Test Traceability

状态：`test_candidate_planned` / `design_ready_for_delivery_planning`. The execution-contract mapping is the 47-row table in
[`fixture-plan.md`](./fixture-plan.md); this file owns cross-authority set closure without duplicating fixture steps.

## 1. Requirements To Fixture Families

| Authority set | Fixture families |
| --- | --- |
| `EVO-REQ-001..009` | Intake Clear/Reviewed Design/Unclear, Detached Read, Base Refresh, Tech Revision |
| `EVO-REQ-010..011` | Entry Routing, Request Stop, Task Free, No Issue, Semantic Confirmation exact-current Workspace reuse, Active Disposition |
| `EVO-REQ-012..026` | Plan Normal, all Architecture planning/freshness fixtures, SSOT Bootstrap |
| `EVO-REQ-027..033` | Full Normal, Branch Finding, Base Evolution, Architecture Promotion with outstanding-only spec projection refresh and already-current double-none convergence, Parallel, RDT freshness |
| `EVO-REQ-034..043` | Entry Routing, None, Full Normal, Semantic Confirmation with separate push/PR-create actions and already-current no-mutation exits, Provider/Finish Recovery, History Resume, Active Disposition |
| `EVO-REQ-044..050` | Plan Normal, Full Normal, Latest Intent, Long Output |
| `EVO-REQ-051..056` | Full Normal, Projection, Provider Recovery, Clean Install, Migration, Release |
| `EVO-REQ-057..058` | Wording Explicit, Qualify Explicit with profile-fixed Clarification, original-caller candidate rebuild and fresh qualification |
| `EVO-REQ-059..067` | Change Request, Base Refresh, SSOT Bootstrap with exact RDT/Architecture caller return and projection-refresh return to Check, RDT Lifecycle/Freshness, Submodule Boundary, Active Disposition |
| `EVO-REQ-068..080` | Stock Coexistence with concrete meta/update-spec successors, Stock Maintenance, Entry Routing, SSOT Bootstrap, Clean Install, Migration, Projection |
| `EVO-REQ-081` | Semantic Confirmation, Active Disposition, Full Normal, Provider Recovery, Finish Recovery, Stock Maintenance, Clean Install, Migration, Release |

| Quality set | Fixture families |
| --- | --- |
| `EVO-NFR-001..008` | Plan Normal, Full Normal, Long Output |
| `EVO-NFR-009..011` | Entry Routing, Latest Intent, Parallel, Provider/Finish Recovery, History Resume |
| `EVO-NFR-012..013` | Projection, Clean Install, Migration, Release |
| `EVO-NFR-014..015` | Full Normal, Branch Finding, RDT/Architecture Downstream Freshness |
| `EVO-NFR-016` | Provider Recovery, Full Normal, Release |
| `EVO-NFR-017` | Semantic Confirmation, Active Disposition, Full Normal, Provider Recovery, Finish Recovery, Stock Maintenance, Clean Install, Migration, Release |
| `EVO-NFR-018` | Submodule Boundary |
| `EVO-NFR-019..032` | Stock Coexistence, Stock Maintenance, Entry Routing, Latest Intent, Projection, Migration |

## 2. Design Responsibility To Fixture Families

| Design set | Fixture families |
| --- | --- |
| `EVO-DES-001..005` | Full Normal, Projection, RDT/Architecture Lifecycle |
| `EVO-DES-006..018` | Entry Routing, Request Stop, Latest Intent, History Resume and specialist fixtures; lifecycle-bound acceptance requires direct `bound_event_ref,event_sequence` projection to one of exactly 37 owners, including Admission/Route Request/Answer/Current Work/History, rejects sequence-only/ambient lookup, and leaves Wording/Qualification ownership with their fixed original callers |
| `EVO-DES-019..022` | intake, task-free, change-request, base, detached-read and exact-current Workspace no-mutation fixtures |
| `EVO-DES-023..027` | Plan Normal, RDT Lifecycle and Architecture planning family; the one exact Approval plan must display activation plus immediate approved implementation entry/allowed writes, then its deterministic activation must close directly to `guru-implement-task:initial` or its own recovery block with zero implementation write |
| `EVO-DES-028..032` | Full Normal, Branch Finding, Base Evolution, promotion/projection/freshness fixtures |
| `EVO-DES-033..042` | Full Normal, Semantic Confirmation, None, Parallel, stage-specific Push/PR-create Provider Recovery, Finish Recovery, History/Disposition |
| `EVO-DES-043..048` | Projection, Clean Install, Migration, Release, Provider Recovery |
| `EVO-DES-049..059` | Stock Coexistence, Stock Maintenance, Projection, Clean Install, Migration |
| `EVO-DES-060..064` | RDT Lifecycle/Freshness, all Architecture contribution/promotion fixtures, Bootstrap-only spec projection refresh |
| `EVO-DES-065..068` | Plan Normal, Full Normal, Long Output, Provider Recovery, Submodule Boundary |
| `EVO-DES-069` | Semantic Confirmation, Active Disposition, Full Normal, Provider Recovery, Finish Recovery, Stock Maintenance, Clean Install, Migration, Release |

## 3. Inventory Closure

- Each `CUR-CAP-001..023` has a target owner and fixture in
  [`../../design/evolution/capability-inventory.md`](../../design/evolution/capability-inventory.md).
- Each `TARGET-DELTA-001..013` has a target allocation and acceptance family in the same file.
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
- Publication confirmation closure proves branch push and PR creation have distinct prepare/wait/confirmation-
  reentry/refusal/provider-recovery identities; neither stage accepts the other's continuation and push confirmation
  cannot authorize or construct PR creation. Exact already-current remote branch/READY PR paths return their current
  result without mutation or confirmation, including after confirmation/provider re-entry.
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
  `Projection -> Stock -> Projection stock_policy_reentry -> fresh complete validation`; Stock cannot complete the
  workflow or create a fifth distribution action.

## 4. Deterministic Planning Closure

The planning checker expands all `NNN..MMM` ranges and asserts exact equality for:

- `EVO-REQ-001..081`;
- `EVO-NFR-001..032`;
- `EVO-DES-001..069`;
- `CUR-CAP-001..023`;
- `TARGET-DELTA-001..013`;
- the frozen set of 47 `EVO-FIX-*` identities.

It also checks local Markdown links, manifest locators, fixture table column counts, 39 unique public Skill
identities / 43 profile rows, exactly 37 lifecycle owners and two specialist non-owners, every named refusal/blocked
consumer and recovery profile, nine wording and eleven
qualification caller profiles, 17 stock decision rows, nine profile-fixed retained rows, one Trellis-reference
  manifest writer/adapter family, one convergent `.trellis/spec` projection writer/return chain, one standalone
  Projection/Stock/Projection fresh-validation chain, one exact-current Workspace no-mutation convergence path, one
  compound activation/implementation-entry confirmation and two isolated push/PR-create confirmation subgraphs with
  no-mutation current exits.
These objective checks do not replace fresh semantic Design review.
