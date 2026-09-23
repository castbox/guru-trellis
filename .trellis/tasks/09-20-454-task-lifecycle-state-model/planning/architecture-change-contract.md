# Phase C3 Architecture Change Contract

## 1. Identity

- Task: `.trellis/tasks/09-20-454-task-lifecycle-state-model`
- Lifecycle generation: `1`
- Requirement authority: live `castbox/guru-trellis#454`
- Guru Architecture public contract: `guru-maintain-architecture-baseline:2.0`
- Current baseline: `current-main-0.6.17-guru.61`
- Constitution: `docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`
- Project change contract: `docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1`
- Change path: `target_native`
- Current candidate contribution id:
  `architecture-contribution-454-task-lifecycle-state-model-c3-provenance-v1`
- Contribution locator:
  `docs/architecture/contributions/454-task-lifecycle-state-model-c3-provenance.md`
- Expected current identity: `current-main-0.6.17-guru.60`
- Promoted successor identity: `current-main-0.6.17-guru.61`
- Promotion state: `reviewed_promoted`
- C3 RDT candidate:
  `docs/requirements-design-test-contributions/454-task-lifecycle-state-model-c3-provenance/`

The promoted `architecture-contribution-454-task-lifecycle-state-model-v1`
remains immutable evidence for C2 and D0. The promoted
`architecture-contribution-454-task-lifecycle-state-model-c3-v1` remains
immutable evidence for the original C3 slice in `current-main-0.6.17-guru.60`.
Implementation discovery finding `BR454-C3-P2-011` requires this distinct
task-owned candidate before source or test edits because live path, branch and
HEAD facts cannot prove transaction origin after same-path replacement.

## 2. Boundary And Decision

Current `.61` authority contains the shared lifecycle kernel, D0 stage-evidence
correction, the promoted C3 checkout substrate and the reviewed provenance
continuity delta. The remaining current production graph still uses
the predecessor task/workspace model.

The promoted C3 provenance delta adds only the next target-native substrate
slice:

1. call-local checkout acquisition, candidate, resolution and selection DTOs;
2. common-dir based live Git/worktree fact inspection;
3. checkout discovery, validation, classification and explicit selection;
4. adopt/provision transactions with bounded rollback and read-only recovery;
5. one closed ordinary JSON provenance marker in the created linked worktree's
   Git administrative directory, owned by the acquisition transaction and read
   only by the same owner's output-loss recovery; the direct handoff retires it
   immediately before invoking its consumer, while worktree removal removes it
   with the original resource;
6. one stable `guru-ensure-task-checkout` id reserved only as `state=planned`
   registry metadata and canonical `planned_skill_ids`; no canonical package
   directory exists until E434 delivers package, selector, workflow and
   installed/platform projections in one activation boundary.

C3 does not create branch association, session or resource-ledger stores. The
transaction marker is not task, session, branch, workspace or resource-ledger
authority and is never projected through a public DTO. It does not activate a
production owner and does not read or write legacy task or workspace mappings.
C4-C7, D443, D436 and E434 remain owned by their existing later slices.

Decision refs: `ARCH-FND-001..006`, `ARCH-GOV-006..009`, `ARCH-GAP-009`,
`ARCH-GAP-011`, `ADR-015`, and all five Design Constitution principles.

## 3. Required Concerns

| Concern | Applicability | C3 candidate contract |
| --- | --- | --- |
| authority-binding | applicable | Bind Architecture 2.0, promotion expected current `.60`, promoted current `.61`, Issue #454 and generation 1. |
| constitution-binding | applicable | Use official Git extension surfaces, unique owners, minimum state and one-way convergence. |
| boundary-and-decision | applicable | C3 is `target_native`; checkout facts remain call-local, while one owner-private transaction marker supplies only non-reconstructible creation provenance to output-loss recovery. The planned Skill id has no package tree. |
| owner-and-single-writer | applicable | The checkout acquisition transaction is the sole marker writer and recovery is its sole reader; C3 otherwise writes shared checkout DTO/runtime and non-active planned metadata. E434 exclusively owns complete package composition and activation. |
| compatibility-and-exit | applicable | No alias, adapter, dual-read or dual-write; predecessor remains active only until E434 atomic cutover. |
| gap-and-deviation | applicable | Narrow `ARCH-GAP-011` by adding checkout substrate without claiming branch/session/resource or production completion. |
| parallel-scope | applicable | Before promotion, only the task-local contract and C3 canonical files are allowed. The reviewed promotion additionally owns the exact `.61` Architecture/RDT authority and navigation declared by the promotion contribution; all other shared current files and active selectors remain forbidden. |
| evidence-and-freshness | applicable | Bind the complete dirty/untracked C3 worktree, same-path replacement and marker lifecycle tests, schema validation, line limits and zero legacy-reader/forbidden-mechanism checks. |
| review-and-promotion | applicable | The provenance delta was independently reviewed against expected current `.60` and serialized into `.61` as `reviewed_promoted`; the promotion-created diff requires fresh Phase 2, Task Commit and independent full-diff Branch Review before Publication. |

## 4. Owner And Single Writer

- Framework TaskId/session primitive writer: fixed `castbox/Trellis` source.
- C2 shared lifecycle kernel owner: promoted #454 `.59` contribution.
- C3 checkout substrate writer: this task and candidate.
- C3 acquisition marker writer/reader: `provision_linked_worktree` writes the
  marker only for transaction-created worktrees; the same acquisition owner's
  output-loss recovery validates it; successful `post_acquire` consumption
  removes it.
- C4 branch association/rebind writer: later #454 slice, not started here.
- C5 session/resource writer: later #454 slice, not started here.
- C6/C7 package composition and validation writers: later #454 slices.
- D443 and D436 package migration writers: their dedicated later slices.
- Planned registry metadata and canonical `planned_skill_ids` writer: this C3
  candidate.
- Complete `guru-ensure-task-checkout` package, workflow, active registry
  selector, active graph manifest and installed/platform activation writer:
  E434.
- Shared Architecture/RDT promotion writer: serialized Architecture/RDT owner.

Discovery of a need to write another owner's surface invalidates this result
and returns to Architecture `implementation_discovery` before editing.

## 5. Compatibility And Deletion

Compatibility layer: none.

The predecessor production assets remain unchanged because C3 is deliberately
inactive. That coexistence is not a compatibility promise. E434 may remove the
old path only after C4-C7 and D443/D436 are complete, active reader/writer and
public-ID consumers are zero, and the replacement graph is complete in one
activation candidate.

## 6. Parallel Scope

Allowed before promotion: the C3 runtime, shared DTO additions, focused tests,
`guru-ensure-task-checkout` `state=planned` registry row, canonical
`planned_skill_ids`, active-package ownership validation updates, and this
task-local planning authority. The reviewed promotion additionally owns only
the exact `.61` Architecture/RDT authority files and navigation declared by the
promotion contribution.

Forbidden: `.trellis/scripts/**`, shared current Architecture/RDT, source lock,
active/integrated registry selector, `active_skill_ids`, active graph manifest,
production workflow edges, installed/platform projections, C4-C7 runtime or
D/E package migration.

## 7. Before And After

Before the reviewed provenance delta: `.60` contains the promoted C3 checkout substrate, but output-loss
recovery proves only path, branch and HEAD. After the original Guru-created
worktree is removed, an honest caller can recreate the same branch/HEAD at the
same path and the current recovery incorrectly restores Guru ownership.

After promoted successor `.61`:

- DTO count changes from 35 to 39 with four call-local checkout DTOs;
- live resolution derives candidates from `git worktree list --porcelain -z`
  and current repository facts instead of persisted paths;
- zero, one and multiple validated candidates have closed classification;
- authority conflicts cannot be downgraded by selection;
- adopt and provision routes validate fresh HEAD/repository/branch/task facts;
- rollback removes only transaction-created resources whose identities still
  match;
- transaction-created linked worktrees carry one closed owner-private marker
  under their Git administrative directory; recovery requires the exact marker
  plus fresh live facts, so same-path replacement fails closed;
- direct `post_acquire` handoff removes the marker before invoking the consumer;
  marker-retirement or callback failure rolls back the transaction-created
  resource, and recovery itself performs no Git mutation;
- `guru-ensure-task-checkout` is reserved by a `state=planned` registry row and
  canonical `planned_skill_ids` membership, with no canonical package directory;
- active registry selector, `active_skill_ids`, workflow, active graph and
  installed/platform bytes are unchanged.

## 8. Evidence And Review

Current candidate surfaces:

- `trellis/skills/guru-team/contracts/task-lifecycle/**`
- `trellis/skills/guru-team/runtime/task_lifecycle/git_facts.py`
- `trellis/skills/guru-team/runtime/task_lifecycle/checkout_resolution.py`
- `trellis/skills/guru-team/runtime/task_lifecycle/checkout_acquisition.py`
- `trellis/skills/guru-team/runtime/task_lifecycle/tests/test_checkout_substrate.py`
- `trellis/skills/guru-team/registry.json`
- `trellis/guru-team-extension.json`
- `trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py`

Required Phase 2 evidence includes the complete lifecycle/runtime suite,
Draft 2020-12 schemas, active package source validation, planned/active
ownership validation including planned-directory absence, Python compilation,
`git diff --check`, touched source line limits, workspace boundary, protected
active-surface identity, and static proof that new C3 runtime has zero
mapping/path-authority access.

The complete preset suite is also executed but is not silently folded into the
focused pass set. The raw-apply fixture currently requires canonical/installed
byte parity and can report conflict because C3 is forbidden to synchronize the
installed DTO and registry copies. That case and the suite
must be reported as unpassed; changing installed/platform projections to make
it pass belongs to E434 and is forbidden in this candidate.

ADR: no new ADR. `ADR-015` already owns lifecycle identity and the
framework/extension boundary. The marker is a bounded transaction-recovery
implementation of the existing conservative ownership rule; it adds no owner,
compatibility exit or durable lifecycle authority.

Promotion state: `reviewed_promoted`. The independent reviewed committed range
is `origin/main@9c2238bad7e73ea4a1f23dddcb7e8e9204c244da...b816aca8d6520bf90c52c6210ff3155174da86f3`.
It closed `BR454-C3-P2-010` and `BR454-C3-P2-011` without a new P0-P3 finding
and serialized expected current `.60` into successor `.61`. This promotion does
not prove the promotion-created worktree diff's downstream gates.

## 9. Resume Boundary

The active task remains `in_progress`. The serialized `.60 -> .61` promotion
does not reactivate, commit, publish or authorize any Git/GitHub mutation. Its
promotion-created dirty diff must re-enter fresh
`task_impact_sync(stage=phase2)` and `guru-check-task`, then Task Commit and an
independent complete committed-range Branch Review before Publication.
