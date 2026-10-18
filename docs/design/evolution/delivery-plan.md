# Evolution Delivery Plan

状态：`fresh_design_review_passed` / `evolution_refactor_eligible` / `issue_suggestions_only`。This revised slice
projection incorporates #311/#312 merged capabilities and carries PR #317 exact installed platform-set preservation
through the existing `EVO-DES-035,043,059,070,072` responsibilities and
`EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION`; it adds no delivery slice. This is a reviewed planning suggestion set,
but remains non-actionable until a future delivery intake is independently authorized against the current
`evolution_refactor_eligible` identity. It does not
create Issues, activate this task, implement, commit, publish or Release.

## 1. Sequencing Contract

- Every slice starts from fresh current RDT/Architecture, creates its own task-local contributions, runs targeted
  tests, passes committed full-diff review, and uses serialized promotion only when shared current changes.
- `EVO-DEL-01` may start only from the exact `evolution_refactor_eligible` identity produced by
  `EVO-DES-070`; material selected-base/RDT/Architecture/Requirements/Design/fixture drift returns to that earliest
  owner rather than being patched in a delivery slice.
- Target packages may be merged dormant under the new contract identity. Until `EVO-DEL-08` atomic activation,
  the current runtime continues to use the current contract; no target consumer reads legacy output and no current
  consumer reads target output.
- A slice may not add a temporary legacy adapter, workflow selector, dual registry, fallback, or public optional
  aggregate merely to allow partial activation.
- Each slice consumes only predecessor reviewed public contracts, not predecessor private checkpoints or long
  handoff artifacts.
- Every slice that may own a side effect first live-resolves whether an action remains. A no-mutation current exit
  bypasses plan display, confirmation wait and refusal handling. Only a pending action applies `EVO-DES-069` locally:
  after displaying the unchanged current exact action plan, any clear semantic affirmative is sufficient and
  authorizes only that action. No slice adds a fixed
  prompt/password/hash/digest/task/path/branch/SHA/identity/summary/prescribed-wording challenge, confirmation
  parser or persisted authorization field.
- Ordinary slices run scope-targeted validation. The complete host/install/update/migration matrix and immutable
  exact-candidate proof belong only to `EVO-DEL-09` and `EVO-DEL-10`.
- Candidate freeze occurs only after `EVO-DEL-01..08` have delivered and independently reviewed all 39 public
  Skills, private adapters/routers, ownership 4.0 handoff, stock policy, projection/install/migration path and one
  activation candidate. `EVO-DEL-09` consumes that immutable identity; any implementation or contract change makes
  its evidence stale and returns to the owning earlier slice before a new full matrix run.

## 2. Serial Slices

| Slice | Independently deliverable scope | Depends on | Required acceptance / exit |
| --- | --- | --- | --- |
| `EVO-DEL-01` contract foundation | new contract/registry/interface identities, public I/O validators, thin router validation, call/host-session-local envelope contract plus task-local same-Skill checkpoint boundary, `guru-trellis-reference-manifest-1.0`, `guru-code-spec-projection-1.0`, closed recoverable-block/re-entry inventory, semantic-confirmation/refusal invariant and dormant activation-manifest shape | exact #305 `evolution_refactor_eligible` identity | 39 Skill inventory, `EVO-DES-001..073` and every output-to-consumer-input projection close without generic frame/private lookup; exactly 37 Skills are lifecycle owners and the two specialists retain original-caller ownership; admission/pre-route/pre-task/task-free/standalone generic repository-envelope paths and writes are zero; any task checkpoint has the same Skill public-wrapper as its only consumer; every ordinary recoverable block maps to one same-owner profile, terminal blocks have no fake continuation, and every refusal has one zero-side-effect target; reference/projection identities have one writer each; authorization fields/parsers are absent; no current route changes |
| `EVO-DEL-02` admission and request families | Admission, isolation, six top-level routes, direct answer including `trellis_reference`, current-work/history/disposition, explicit specialist adapters and the caller-fixed reference adapter; stock guard call boundary is wired but remains dormant/fail-closed until Slice 06 supplies the policy plane | 01 | non-stock Entry Routing, Request Stop, Active Disposition, History Resume, Wording/Qualification and Latest Intent targeted cells pass; cross-turn isolation and standalone Answer/provider repair use host continuation with zero repository-envelope state, and missing/stale continuation reaches the exact owner block/re-entry; reference lookup follows manifest precedence and returns only to Answer/exact embedded caller while all writes re-enter active/new-change; lifecycle binding/isolation and Answer provider recovery remain distinct, lifecycle resume uses the closed registry and remote convergence uses the named four-owner wait; nine wording profiles and ten active four-result qualification profiles return only to their original callers, while standalone qualification exposes only its three applicable results; stock collision/retained/provider branches remain explicitly unverified and cannot be claimed current before 06 |
| `EVO-DEL-03` intake and planning | mode/task-free, Sync/Discovery/Clarification/Readiness/Workspace, RDT then Architecture impact, `guru-plan-task`, one approval | 01-02 | Intake, Task Free, Base, Change Request, Plan, RDT/Architecture planning fixtures pass; exact-current Workspace reuse returns `workspace_current -> task_impact_sync` with zero plan display/confirmation/refusal/mutation, while only pending creation/transfer/isolation enters its confirmation graph; the one exact Planning confirmation plan includes task activation plus immediate approved implementation entry and excludes later delivery actions; normal wrapper/repeated-read and second routine confirmation counts are zero |
| `EVO-DEL-04` implementation and review | `guru-implement-task`, separate platform/channel caller-bound implementation adapters, check workers, Check/Commit/Reconcile/Branch Review, #312 original-worktree continuity, contribution freshness and Bootstrap `projection_refresh` return to fresh Check/Commit/Review | 01,03 | Full Normal through candidate review, Branch Finding, Base Evolution, Gitlink/submodule and downstream freshness targeted fixtures pass; path-clean tracked same-task state continues in the original active worktree, unrelated dirty remains untouched, and every true artifact/identity blocker remains closed; a reviewed code-spec contribution has exactly one `.trellis/spec` writer, only outstanding work is selected, and the fresh complete-diff review converges already-current authority/projection targets to exact double-none before delivery |
| `EVO-DEL-05` delivery, Finish and cleanup | delivery route/readiness/acceptance; separate installed/self-hosted provenance-tail, branch-push and Draft-PR subgraphs; summary/archive/archive-push/Ready Finish; archive-bound Merge, closure, Cleanup and durable history | 01,04 | GitHub controlled integration and `none` route, Installed Provenance Publication, Semantic Confirmation, Provider Recovery and Finish Recovery pass; three Publish actions have separate prepare/wait/re-entry/refusal/recovery and completed-state no-mutation exits, with `publication_preparation_not_executed`, `branch_push_not_executed` and `pr_creation_not_executed` projecting action-local identity to three distinct named zero-side-effect consumers; source/target lineage and normalized reviewed content remain exact; Finish alone produces official archive/Ready/`ready_for_merge`, terminal reinvoke replays no Git/GitHub/archive mutation, READY merge has no lexical gate, and Finish/Merge/Closure/Cleanup refusals/recoveries remain disjoint; no remote live claim required |
| `EVO-DEL-06` stock control plane | ownership 4.0 handoff, canonical stock policy, exact provenance/file-context-sidecar state, 9 absence actions, 3 quarantine adapters, 5 worker replacements, 9 profile-fixed retained rows, and the Slice-02 admission guard policy implementation | 01-05 | Stock Coexistence and Maintenance pass on representative shared/host cells; Slice-02 deferred stock guard branches close through the one Route Request success edge; meta/reference and update-spec/projection successor proofs are current before their raw surfaces become absent; every retained profile binds its exact host context owner, embedded result variants are disjoint, Projection is the fixed standalone Stock caller and Stock current returns only to Projection revalidation, standalone refusal re-entry is exact, user edits/sidecars are preserved, and raw dispatch count is zero in selected cells |
| `EVO-DEL-07` projection and clean install | canonical/dogfood/installed generator, preset transaction, reference manifest projection, code-spec projection-contract projection, host setup partition, Projection-owned standalone verifier failure lifecycle and clean installer | 01-06 | Projection, Verifier Failure Evidence and one representative clean throwaway pass; matrix and postcheck failures bind non-null bounded credential-safe evidence before cleanup and re-enter Projection only; embedded callers and Finish consume none of that lifecycle; standalone policy maintenance follows only `Projection -> Stock -> named action confirmation wait when mutation remains -> Stock action re-entry -> Projection fresh validation`, with missing/refusal/drift owner-local and no fifth distribution action; manifest source precedence, one-writer ownership, reapply/drift and executable/mode checks pass; preset reapply does not perform code-spec promotion/write; full matrix explicitly unverified |
| `EVO-DEL-08` existing migration and atomic cutover | five-cell migration, lifecycle/history/ref preservation, unique cutover, preset reapply, final validation and activation | 01-07 | representative existing migration including pre/post-cutover recovery passes; all 39 public Skills and selected adapters are current in one activation candidate; target-before-activation and legacy-after-activation consumer counts zero; candidate is then frozen for 09 |
| `EVO-DEL-09` cumulative compatibility matrix | execute all declared Codex/Claude/Cursor clean/existing/update/reapply/workflow-switch cells, setup partition, standalone verifier failure cells and normal A/B lifecycle against the frozen Slice-08 candidate; implementation/contract writes are forbidden | immutable candidate from 01-08 | complete exact matrix plus matrix-external `postcheck_failure` evidence pass from that identity; any finding returns to an owning earlier slice and invalidates the matrix rather than being patched or deferred into Release |
| `EVO-DEL-10` exact Release | invoke the already implemented/reviewed `guru-release-candidate` pre-publish/semantic-confirmation/publication/tag-pinned post-publish and published-unverified recovery boundary; candidate writes are forbidden | exact immutable candidate that passed 09 plus independent release authority | same-identity Release evidence passes; zero-completed/unknown progress and true partial publication use disjoint DTOs; clear affirmation is dialogue-local and exact-action-scoped; the full `EVO-DES-069` challenge/parser/persistence zero-count set holds; no candidate modification, fallback or republish of the same identity |

Slices are suggestions for future Issue creation. Exact Issue identities, branch/worktree plans and remote side
effects require a new live intake and confirmation; this document does not reserve numbers or mutate #267/#304.

## 3. Slice Ownership Boundaries

| Concern | Single owner across slices | Forbidden expansion |
| --- | --- | --- |
| public graph | contract registry/workflow owner | step-local behavior copied into workflow/platform entry |
| invocation state | Admission/envelope owner | task journal or public DTO as a second invocation state |
| standard plan | `guru-plan-task` | wording/qualification/upstream brainstorm as mandatory author |
| implementation | task-free owner or `guru-implement-task`, exactly one | autonomous worker phase progression |
| shared RDT/Architecture | respective semantic owner/promotion single writer | slice directly editing current without promotion gate |
| `.trellis/spec` projection | `guru-bootstrap-repository-ssot:projection_refresh` | raw update-spec, preset/reapply or worker acting as a second writer |
| Trellis reference | preset-written manifest + caller-fixed read adapter | raw meta matcher/write route or generic reference caller |
| stock projection | stock policy/preset transaction owner | hook/Skill deleting upstream output independently |
| provider outcome | exact action owner; provenance tail, branch push, Draft PR, Finish/archive-push/Ready and Merge remain separate stages and already-current live state advances without mutation | retry/fallback route chosen by child provider, current action repeated, confirmation reused by a later action, or Merge before archive-bound `ready_for_merge` |
| activation | migration/clean transaction and activation validator | partial host activation or mixed graph |
| Release | `guru-release-candidate` | ordinary slice claiming full compatibility or publication proof |

## 4. Acceptance At Every Slice

Each implementation Issue must record:

1. exact accepted scope and predecessor public identity;
2. RDT/Architecture impact and task-owned contribution;
3. target Design responsibilities and fixture rows owned by the slice;
4. targeted static/semantic/runtime/projection/installed/provider evidence and honest unverified boundaries;
5. independent committed full-diff review and any required serialized promotion;
6. proof that current/target state labels remain truthful, the semantic-confirmation zero-count invariants hold for
   any owned side effect, and no protected later slice was silently absorbed.

Failure to meet a predecessor contract returns to that predecessor Issue/owner; it does not create a compatibility
wrapper in the current slice.
