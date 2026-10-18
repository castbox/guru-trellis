# #419 Active-task continuation Architecture contribution

## Identity And Authority Boundary

- candidate identity: `architecture-contribution-419-active-task-continuation-v1`.
- lifecycle state: `reviewed_promoted`; absorbed by `current-main-0.6.17-guru.54`.
- source authority: [Issue #419](https://github.com/castbox/guru-trellis/issues/419)
  contract `2026-09-17-r7`.
- task locator: `.trellis/tasks/09-17-419-active-task-continuation`.
- RDT contribution:
  `docs/requirements-design-test-contributions/419-active-task-continuation/`.
- source/expected baseline: `docs/architecture/README.md` /
  predecessor `current-main-0.6.17-guru.53`; current successor
  `current-main-0.6.17-guru.54` / `active`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`; accepted ADR:
  [ADR-011](../adr/011-active-task-continuation-authority.md).

This contribution records the stable target boundary and promotion provenance
only. It does not record task progress, Gate results, user authorization, or
release readiness. Independent Architecture and RDT owners serialized the
reviewed `.53 -> .54` promotion; `.53` remains immutable history.

## Before And Target

Before: active-task continuation is inferred from coarse task status and broad
workflow breadcrumbs. That cannot distinguish unfinished Phase 2 from a
completed Task Commit, Branch Review, or Publication boundary after public
output is lost. Re-entering from a new session can therefore repeat the wrong
owner or stop on a clean committed worktree.

Target: the current workflow contains one non-empty `[trellis-continuation]`
block as the sole detailed resume authority. It interprets exact current-task
facts, consumes current adjacent public DTOs directly, returns deterministic
output loss to the original producer, and reruns semantic owners fresh when
their call-local output is gone. Phase Index, task status, hooks, platform
entries, and old conversation text never become a second route authority.

Phase 1 preserves the existing owners for task-created attachment, planning
authoring, wording, Planning Architecture, approval, plan presentation, and
activation. Lost task/workspace `created` output uses the original
`guru-create-task-workspace:recover_created_result` read-only checker and cannot
create or repair another workspace/task. Activation uses a workflow-owned
`initial|recovery` contract. Both modes bind the exact current task, worktree,
branch, mapping, and expected status before any mutation; `initial` then runs
the official transition once and verifies `in_progress`, while an already
successful transition uses `recovery` to rematerialize its result without
running twice. Confirmation remains dialogue-local.

Phase 2 uses the existing checker-to-public-invoker path to rematerialize a
current retained `passed` result; it does not add a public recovery profile.
Task Commit retains its existing same-candidate `recovery_resume`. Lost Branch
Review and Publication results require fresh semantic review because successful
checkpoints retire. The target stops at the existing Finalizer entry and does
not enter archived, Merge, or transaction recovery owned by #418 and the
current closeout packages.

## Ownership And Single Writers

- upstream Trellis owns continuation extraction/loading, official
  `trellis-start` / `trellis-continue`, hooks, generated platform entries, and
  `trellis-meta`.
- the Guru marketplace workflow owns the Guru continuation body and its global
  mapped routes.
- each semantic Skill remains the single writer of its judgment and public
  output; deterministic recovery remains inside the mutation/result producer.
- the Guru preset owns only Guru packages, runtimes, schemas, discovery copies,
  and additive `guru-finish-work` entries. Reapply does not own or modify the
  active workflow or upstream entries.
- Architecture and RDT shared current remain owned by their existing
  expected-current-bound promotion profiles. The promoted contribution and
  accepted ADR record provenance without becoming another current authority.

## Required Concerns

| Concern | Applicability | Candidate contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | Bind live #419 r7, current `.53`, the exact task, current workflow, and producer Interfaces; drift returns to the earliest affected owner. |
| `constitution-binding` | `applicable` | Preserve semantic completeness, cohesion/change isolation, minimum necessary complexity, and one-way debt convergence without copying constitution prose. |
| `boundary-and-decision` | `applicable` | One workflow continuation block owns detailed routes; breadcrumbs and entries remain fact/loading layers. |
| `owner-and-single-writer` | `applicable` | Adjacent DTOs go to unique consumers; output-loss recovery and semantic reruns stay with original producers/owners. |
| `compatibility-and-exit` | `applicable` | Existing Phase 2 and Task Commit public contracts are reused; no global persistent stage state, semantic resolver, or dual route table is added. |
| `gap-and-deviation` | `applicable` | Close the active pre-Finalizer cross-session gap without expanding #398 or #418 archived/merge ownership. |
| `parallel-scope` | `applicable` | This task writes isolated code/docs/spec/tests only; shared current and unrelated worktrees remain untouched. |
| `evidence-and-freshness` | `applicable` | Bind real workflow/package wrappers and exact upstream candidate evidence; old candidate, old gate, or old confirmation is stale. |
| `review-and-promotion` | `applicable` | Independent full-diff review must precede any serialized Architecture/RDT promotion; promotion-created diff re-enters fresh Phase 2, commit, and review. |

## Exact-upstream Validation Contract

The only accepted upstream integration candidate is
`43fffc170927c85d9f7fc106cc5a059e80d4530b`. Its ordered parents are
`db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0` and
`df12903220ce22b2c84782968ed5c93406b5738b`; its tree is
`02fc0922f535200f67de7f6ba7920e3c763d7e95`. Evidence using a branch, PR head,
short SHA, different parent order, or later upstream revision is not evidence
for this contribution.

The acceptance proof is limited to the continuation defect: verify the upstream
extractor, `get_context.py --mode continuation`, workflow-neutral
`trellis-start` / `trellis-continue`, Guru continuation and producer-owned
recovery through source/installed package runtime, evals, and real Git/task
fixtures. Canonical, installed, dogfood, and declared-platform Guru projections
must agree. Upstream ownership, dogfood drift, current-worktree sidecar/residue
hygiene, and `git diff --check` must pass, and the task diff must not modify
upstream-owned start/continue/hooks/platform/`trellis-meta` paths.

#419 does not own disposable installation, update, workflow-switch, or release
compatibility evidence. Live #410 owns those Release Gate checks and must create
them independently from a fresh Guru release candidate after #419 merges. Any
partial or interrupted #419 release-validation output is outside this
contribution and cannot be reused.

## Review, ADR, And Promotion

[ADR-011](../adr/011-active-task-continuation-authority.md) is accepted by the
expected-`.53` serialized promotion to `.54`. The RDT owner promoted the matching
R419/D419/T419 contribution into the same current identity.

Any promotion-created combined diff must then repeat fresh Phase 2, Task Commit,
and complete Branch Review before Publication. #410 must freeze a new release
candidate from post-merge live authority; this contribution is not cross-SHA
release evidence.
