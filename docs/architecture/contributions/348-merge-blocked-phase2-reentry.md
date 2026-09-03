# #348 Architecture Contribution: Archived Task Phase 2 Re-entry

## Candidate Identity And Authority Boundary

- candidate identity: `architecture-contribution-348-merge-blocked-phase2-reentry-v1`.
- requirement authority: live Issue #348 and task `prd.md`.
- behavior authority: task `design.md`, `implement.md`, and the canonical Merge/recovery packages.
- current baseline: `docs/architecture/README.md` / `current-main-0.6.5-guru.43` / `active`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1` / `guru-trellis-architecture-change-concerns-v1`.
- change path: `target_native`.
- expected current identity: `current-main-0.6.5-guru.43`.
- review state: `pending independent committed full-diff review`.
- promotion state: `required_not_started`.
- ADR required: `false`.

This is a task-owned candidate. It does not claim CURRENT, promotion, release,
merge, Issue closure, or permission to write the shared Architecture Baseline.

## Boundary And Decision

The current graph correctly blocks Merge but has no legal recovery edge when an
open PR needs an in-scope task-content fix after its task was archived. The
target boundary adds one Merge exit, `phase2_reentry_required`, and one recovery
owner, `guru-restore-archived-task`. Merge retains semantic ownership of the
task-work versus external-blocker decision. The recovery owner rereads live
identity and performs only deterministic local reuse of the original task,
branch, worktree, remote branch, and PR.

The public handoff contains only repository, PR/head/branch, Issue, task/archive,
finding, and Phase 2 identity. Owner-private runtime mapping remains ordinary
application state. No lock, PID, process tree, signal, file descriptor, inode,
or file-open state carries business authority. No legacy fallback, dual-read,
replacement object, or second merge owner is introduced.

## Required Concerns

| Concern | Applicability | #348 contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | Bind Architecture 2.0, active `.43`, Issue/task authority, and project change contract v1. |
| `constitution-binding` | `applicable` | Apply concept completeness, cohesion/change isolation, minimum complexity, and one-way convergence without copying principle prose into public data. |
| `boundary-and-decision` | `applicable` | `target_native` adds one recovery owner after Merge while preserving Merge scope judgment and Phase 2 ownership. |
| `owner-and-single-writer` | `applicable` | Merge owns finding classification; recovery owns local restoration; existing downstream Skills retain their results; Architecture promotion remains the sole shared-current writer. |
| `compatibility-and-exit` | `applicable` | External blockers keep `merge_blocked`; successful restoration has one Phase 2 consumer; unknown, stale, or conflicting identity fails closed. |
| `gap-and-deviation` | `applicable` | Close only the missing post-archive task-work recovery edge; do not change #223, #248, #261, or existing Architecture GAP lifecycle. |
| `parallel-scope` | `applicable` | Allow this contribution, RDT contribution, canonical packages, projections, workflow, docs, and tests; forbid shared current and unrelated task resources. |
| `evidence-and-freshness` | `applicable` | Bind live Issue/task scope, complete worktree candidate, package/runtime tests, workflow closure, reapply/drift, and stage-local identity. |
| `review-and-promotion` | `applicable` | Keep this contribution task-owned until independent full-diff review; any shared-current promotion is serialized and expected-current-bound. |

## Owners And Single Writers

- task-work classification owner: `guru-merge-task-pr` semantic gate.
- archived-task recovery owner: `guru-restore-archived-task`.
- deterministic local writer: the recovery package command, after current live
  facts and semantic result have been validated together.
- downstream owners: Phase 2, Task Commit, Branch Review, Publication,
  Finalizer, Delivery, and Merge rerun independently with fresh evidence.
- task writer: the #348 worktree and its task-owned contributions.
- shared-current writer: the existing serialized Architecture/RDT promotion
  owners only.

## Before And After

- before: `merge_blocked` has only a stop consumer; an archived task with an
  open same-head PR cannot return to Phase 2 without manual archive movement or
  duplicate task resources.
- after: an AI-reviewed in-scope content finding emits a minimal recovery DTO;
  the recovery owner validates PR/Issue/branch/task/archive/worktree identity,
  restores the same task idempotently, retires stale downstream authority, and
  returns to Phase 2.
- preserved: external blocker termination, expected-head Merge semantics,
  existing Issue/branch/worktree/PR identity, AI-first judgment, deterministic
  script limits, and all downstream independent gates.

## Project Check Contract

Use `guru-trellis-architecture-convergence:repository:1` /
`guru-trellis-architecture-convergence@1`, binding `ARCH-GOV-006..008`,
`ADR-005`, and `ARCH-GAP-006`.

- applicable scope: stage invocation, current authority binding, target-native
  owner topology, required concern completeness, before/after regression,
  single-writer and parallel isolation, projection closure, and freshness.
- before: Merge blocks safely but has no contract-owned same-task remediation
  route after archive.
- after: one semantic route and one deterministic recovery owner restore the
  original task identity and force all downstream evidence to rerun.
- expected result: `pass / blocking=true` only when the complete current
  candidate keeps external blockers terminal, has no dual writer or stale
  authority reuse, and all required projections and focused tests pass.
- evidence locator: this contribution, the RDT contribution, current diff, and
  the focused validation summaries produced by the stage owner.
- freshness source: the complete current worktree candidate or exact committed
  range for the invoking stage.

## ADR And Promotion Boundary

No ADR candidate is required. The change adds a missing route within the
accepted lifecycle recovery model (`DES-011`, `BEH-006`) and does not replace an
architecture decision, principle exception, shared owner, GAP lifecycle, or
compatibility exit. Architecture/RDT promotion remains a later serialized step
after independent committed full-diff review.

## Explicit Boundaries

- no shared current edit, commit, push, PR, merge, release, Issue closure, or
  worktree cleanup.
- no automatic check override or external-provider remediation.
- no complete multi-platform throwaway, upgrade/update, or Release Gate matrix
  claim.
