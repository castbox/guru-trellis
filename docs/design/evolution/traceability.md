# Evolution Design Traceability

状态：`design_ready_for_delivery_planning` / `fresh_design_review_passed` /
`evolution_refactor_eligible`。Requirements authority is
[`requirement-main.md`](../../requirements/evolution/requirement-main.md) and
[`requirement-non-functional.md`](../../requirements/evolution/requirement-non-functional.md). This file owns
the current `REQ-REV-011..142` Requirements-to-Design planning allocation; Test execution ownership remains in
[`../../test/evolution/fixture-plan.md`](../../test/evolution/fixture-plan.md).

## 1. Functional Requirement Coverage

The expanded union below is exactly `EVO-REQ-001..084`.

| Requirement range | Design responsibilities / contract owner | Acceptance fixtures |
| --- | --- | --- |
| `EVO-REQ-001..009` | `EVO-DES-002,005,019..022,060`; Clarification/Sync/Discovery contracts | Intake, Detached Read, Base Refresh |
| `EVO-REQ-010..011` | `EVO-DES-006..018,022,038..042`; Admission/Router/Mode/Workspace/Disposition, including direct bound-event projection, 37 exact lifecycle owners, original-caller ownership for both specialist Skills and exact-current Workspace reuse with zero plan/confirmation/refusal/mutation | Entry Routing, Request Stop, Task Free, Semantic Confirmation, History Resume, Latest Intent, Active Disposition |
| `EVO-REQ-012` | `EVO-DES-023..027`; Plan author and approval with one displayed compound activation/approved-implementation-entry action and owner-local deterministic closure | Plan Normal, Semantic Confirmation |
| `EVO-REQ-013..020` | `EVO-DES-024,029,031,060..063`; Architecture owner and contribution | Architecture fixture family |
| `EVO-REQ-021..026` | `EVO-DES-009..011,023..027`; call/host-session-local envelope, zero pre-task repository-envelope write, stable authority-content prefix, Clarification/RDT/Architecture subprojection owners, Plan/Approval | Reviewed Design, Plan Normal, Freshness fixtures |
| `EVO-REQ-027..033` | `EVO-DES-028..032,064,071`; Implementation/Check/Commit/Reconcile/Review, #312 original-worktree/path-state classification and outstanding-only post-review promotion/spec-projection convergence | Full Normal, Branch Finding, Base Evolution, Parallel, promotion fixtures |
| `EVO-REQ-034` | `EVO-DES-013..018,033..042`; route/terminal/disposition owners | Entry Routing, None, History Resume, Active Disposition |
| `EVO-REQ-035..043` | `EVO-DES-033..042,066,072`; Delivery/Acceptance, separate provenance/push/Draft-PR actions, Finish/archive/Ready before archive-bound Merge, Closure/Cleanup and closed same-owner recovery inventory | Full Normal, None, Semantic Confirmation, Installed Provenance Publication, Provider/Finish Recovery, History Resume |
| `EVO-REQ-044..050` | `EVO-DES-009..011,065..067`; call/host-session-local private envelope, same-owner active-task checkpoint boundary, stable bound authority content and minimal evidence/DTOs | Plan Normal, Full Normal, Long Output, Latest Intent |
| `EVO-REQ-051` | `EVO-DES-003,053,065`; AI semantic owners and bounded workers | Full Normal, Stock Coexistence |
| `EVO-REQ-052..056` | `EVO-DES-043..048,056..059`; Distribution and activation owners, with Projection as the sole standalone Stock caller and Stock current returning to Projection revalidation | Projection, Stock Maintenance, Provider Recovery, Clean Install, Migration, Release |
| `EVO-REQ-057..058` | `EVO-DES-018`; nine closed wording caller profiles, profile-fixed qualification-scope Clarification and original-caller fresh re-entry | Wording Explicit, Qualify Explicit |
| `EVO-REQ-059..060` | `EVO-DES-019..022,038`; readiness/base/context recovery | Change Request, Base Refresh, Detached Read |
| `EVO-REQ-061` | `EVO-DES-023..024,031,060..064`; RDT/Architecture caller continuations, exact repository-bootstrap return router and Bootstrap-only already-current-aware spec projection refresh | SSOT Bootstrap, Architecture Promotion |
| `EVO-REQ-062..065` | `EVO-DES-023,029,031,060..064`; RDT contribution/promotion/freshness | RDT Lifecycle, RDT Downstream Freshness |
| `EVO-REQ-066` | `EVO-DES-020,068`; repository boundary | Submodule Boundary |
| `EVO-REQ-067` | `EVO-DES-016,038..042`; current-work/disposition/history owners | Active Disposition, History Resume |
| `EVO-REQ-068..080` | `EVO-DES-006,012,014,031,043,049..059,064,066`; stock policy, Projection-owned standalone maintenance/revalidation, manifest-bound Trellis reference, governed code-spec projection, caller-fixed adapters, R01..R09 retained profiles, host projection/distribution and exact recovery | Stock Coexistence, Stock Maintenance, Projection, SSOT Bootstrap, Clean Install, Migration |
| `EVO-REQ-081` | `EVO-DES-022,030,035..036,041,044..055,069,072`; side-effect-owning semantic Skills, including separate provenance-tail/branch-push/PR-create waits, the profile-fixed `stock-policy-action-confirmation-wait` and active disposition cleanup, apply one shared dialogue-local confirmation contract and owner-specific refusal outputs; Stock action-state continuation never directly authorizes mutation, while Publish refusal exits `publication_preparation_not_executed`, `branch_push_not_executed`, `pr_creation_not_executed` each carry action-local identity to one distinct named consumer, and exact-current Workspace reuse bypasses the boundary entirely | Semantic Confirmation, Stock Maintenance, Active Disposition, Full Normal, Provider Recovery, Finish Recovery, Release |
| `EVO-REQ-082` | `EVO-DES-034..036,060..063,070..072`; two-stage prerequisite/refactor eligibility, #312 original-worktree continuity and #311 installed source/target through Draft PR/archive/Ready/`ready_for_merge` | Evolution Prerequisite, Installed Provenance Publication, Base Evolution |
| `EVO-REQ-083` | `EVO-DES-043,048,065..068,070,073`; standalone Projection-owned non-null failure evidence before cleanup, exact blocked/re-entry and zero Finish/embedded ownership | Verifier Failure Evidence, Evolution Prerequisite, Projection |
| `EVO-REQ-084` | `EVO-DES-035,043,059,070,072`; existing installed publication/Projection responsibilities validate the three exact selected lists plus `all_platforms`, preserve subset/full-set argv semantics and fail before source checkout/apply/commit without adding a public profile or responsibility | Installed Provenance Publication, Evolution Prerequisite, Projection |

## 2. Nonfunctional Requirement Coverage

The expanded union below is exactly `EVO-NFR-001..034`.

| NFR range | Design mechanism | Measurement fixtures |
| --- | --- | --- |
| `EVO-NFR-001..008` | `EVO-DES-009..011,065..067`; one call/host-session-local envelope, consumer-minimal results, zero generic repository-envelope state and zero redundant work | Plan Normal, Full Normal, Long Output |
| `EVO-NFR-009..011` | `EVO-DES-006..008,033..042,048`; freshness, host-continuation isolation, same-owner task-checkpoint boundary and bounded provider recovery | Entry Routing, Latest Intent, Parallel, Provider Recovery |
| `EVO-NFR-012..013` | `EVO-DES-043..047,056..059`; live-derived projection and atomic install/migration | Projection, Clean Install, Migration, Release |
| `EVO-NFR-014..015` | `EVO-DES-002..005,025,028..031,060..067`; semantic owner/minimal data/SSOT trace | Full Normal, RDT/Architecture Downstream Freshness |
| `EVO-NFR-016` | `EVO-DES-048,066,068`; redaction and provider evidence boundary | Provider Recovery, Full Normal, Release |
| `EVO-NFR-017` | `EVO-DES-022,030,035..036,041,044..055,069,072`; exact-plan semantic affirmation, stale-plan rejection, named refusal route and zero authorization persistence across provenance-tail, push, PR creation, named Stock action confirmation and every later action owner | Semantic Confirmation, Stock Maintenance, Active Disposition, Full Normal, Provider Recovery, Finish Recovery, Release |
| `EVO-NFR-018` | `EVO-DES-020,068`; parent/nested repository isolation | Submodule Boundary |
| `EVO-NFR-019..021` | `EVO-DES-014,049,052..054,057..058`; exact role/caller/context closure, including reference caller profiles | Stock Coexistence |
| `EVO-NFR-022..027` | `EVO-DES-031,049..055,059,064,069`; selected action provenance, named confirmation wait, exact recovery and concrete successor reachability | Stock Maintenance, Semantic Confirmation, Projection, SSOT Bootstrap, Migration |
| `EVO-NFR-028..032` | `EVO-DES-006,009..012,054,057..059`; source stimulus, setup partition, lazy context | Entry Routing, Latest Intent, Stock Coexistence, Stock Maintenance |
| `EVO-NFR-033` | `EVO-DES-060..063,070..073`; exact two-stage freshness, merged-capability Design successor closure, installed publication continuity, base/worktree isolation and pre-cleanup verifier evidence | Evolution Prerequisite, Installed Provenance Publication, Verifier Failure Evidence, Base Evolution |
| `EVO-NFR-034` | `EVO-DES-035,043,059,070,072`; positive single/subset/all platform parity and invalid manifest identity zero-source-checkout/apply/commit/mutation coverage remain inside the existing installed publication fixture | Installed Provenance Publication, Evolution Prerequisite, Projection |

## 3. Capability And Goal Coverage

- `CUR-CAP-001..023` and `TARGET-DELTA-001..013` had one historical row each in
  [`capability-inventory.md`](./capability-inventory.md).
- `EVO-001..007` are allocated to `EVO-DES-001..073` through the functional groups above.
- `EVO-CAP-001` is primarily `EVO-DES-001,006..018,033..048,069`.
- `EVO-CAP-002` is primarily `EVO-DES-002,023,025,029,031,060..064`.
- `EVO-CAP-003` is primarily `EVO-DES-024,029,031,060..063`.
- `EVO-CAP-004` is primarily `EVO-DES-009..011,038..042,048,065..067,069`.
- All 50 `EVO-FIX-*` identities have a current planning mapping. The post-`REQ-REV-132` rows map to
  `EVO-DES-070..073`; #311 and PR #317 are carried by current capability successors rather than a new
  `TARGET-DELTA-014` or fixture.
- All 39 target public Skills are declared in [`contracts.md`](./contracts.md); the Trellis-reference and worker/
  provider adapters plus thin routers are not counted as public Skills. `guru-bootstrap-repository-ssot` owns the
  additional projection profile without adding a public identity. Every public external exit names one
  consumer/router/stop.

## 4. Closure Rules

Design trace is incomplete if any expanded ID is missing, duplicated across incompatible owners, points to an
unknown `EVO-DES-*`/fixture, or relies on a task planning document as repository authority. A range is only a
compact notation: deterministic closure expands it before comparing the expected sets.

Semantic review additionally checks that a listed successor preserves the actual behavior; textual presence alone
cannot pass. It also verifies that admission/pre-route/pre-task/task-free/standalone envelope persistence below
`.trellis/tasks/**`, `.trellis/workspace/**` or `.trellis/.runtime/**` is zero, and that any task-local checkpoint has
only the same Skill public-wrapper as consumer. This mapping is synchronized and has passed fresh Design review plus
deterministic closure for `REQ-REV-142`; Test status stays planned until the exact implementation candidate/range is
executed at its declared evidence layer.
