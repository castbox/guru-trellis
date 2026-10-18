# #240 Architecture Contribution: Solution Mechanism Qualification

## Candidate Identity And Authority Boundary

- candidate identity: `architecture-contribution-240-solution-mechanism-v1`。
- requirement authority: live Issue #240 与 task `prd.md`。
- behavior authority: task `design.md`、`implement.md` 与 canonical `guru-qualify-solution-mechanism` package。
- source baseline: `docs/architecture/README.md` / `current-main-0.6.5-guru.43` / `superseded`。
- design constitution: `docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `current`。
- project change contract: `docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1` / `guru-trellis-architecture-change-concerns-v1`。
- change path: `target_native`。
- expected current identity: `current-main-0.6.5-guru.43`。
- review state: `passed`；PR #346 的完整 committed diff 独立 Branch Review 为 `passed`，P0-P3 open findings 为 0。
- promotion state: `reviewed_promoted`；successor `current-main-0.6.5-guru.44`。

This contribution remains the historical task-owned source. Its reviewed contract and
ADR-008 were serialized into current `current-main-0.6.5-guru.44`; PR #346 merged as
`2bafec114f2c6d499edf744b3ce3f5082a3212ef` and Issue #240 is closed. It does not claim
release proof or authorize any later mutation.

## Boundary And Decision

The current Guru Team graph has one public semantic owner for normal-scenario
qualification. Issue #240 adds a distinct public semantic owner for the
solution mechanism itself. The new owner reads the current requirement,
planning, Architecture/spec authority, dependency/caller graph, diff and
tests, then judges whether a proposed mechanism actually carries business
authority. It rejects OS lock/process/descriptor primitives when they carry
business correctness, identity, fencing, monitoring, cancellation, recovery,
publication, or evidence authority, while preserving ordinary file and
directory state/artifact operations.

The target boundary is one explicit `guru-qualify-solution-mechanism` owner,
with caller-local candidate construction and typed re-entry. The mechanism
owner does not absorb normal-scenario qualification, implementation severity,
publication readiness, or deterministic script judgment. No legacy authority,
dual-read, compatibility adapter, lock protocol, or business repository
migration is introduced.

## Required Concerns

| Concern | Applicability | #240 contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | Bind Guru Architecture 2.0, active `.43`, Issue/task authority and project contract v1. |
| `constitution-binding` | `applicable` | Apply concept completeness, cohesion/change isolation, minimum complexity and one-way convergence without copying principle prose into public Skill data. |
| `boundary-and-decision` | `applicable` | `target_native` adds a mechanism semantic owner and preserves the separate normal-scenario owner. |
| `owner-and-single-writer` | `applicable` | The new Skill owns mechanism qualification; callers own candidate sets; Architecture promotion remains the only shared-current writer. |
| `compatibility-and-exit` | `applicable` | No legacy adapter or dual-read; stable public ids and existing caller routes remain explicit and fail closed on unknown exits. |
| `gap-and-deviation` | `applicable` | Close the missing mechanism-qualification owner gap; do not alter existing Architecture GAP ownership. |
| `parallel-scope` | `applicable` | Allow this contribution, canonical package, projections, workflow and tests; forbid shared current, ADR index and unrelated Issues. |
| `evidence-and-freshness` | `applicable` | Phase 2 and Branch Review reread the live baseline and exact candidate; package, workflow, projection or test changes stale the corresponding result. |
| `review-and-promotion` | `applicable` | Keep the contribution task-owned until independent full-diff review; promotion is serialized and expected-current-bound. |

## Owners And Single Writer

- current scenario owner: `guru-qualify-normal-scenario`。
- target mechanism owner: `guru-qualify-solution-mechanism`。
- caller owners: planning, implementation discovery, Phase 2, Branch Review,
  Publication and task-free owners construct candidates and consume the typed
  mechanism result; they do not reproduce mechanism qualification.
- task writer: #240 task worktree and this contribution only。
- shared-current writer: the existing serialized Architecture promotion owner。
- compatibility owner: the mechanism Skill owner with the existing workflow
  router; no compatibility layer is retained。

## Before And After

- before: callers could qualify a problem scenario, but no independent public
  owner judged whether the proposed implementation mechanism was allowed to
  carry business authority。
- after: mechanism qualification is a separate semantic boundary。Candidate
  decisions use `qualified_current` as the wire name for
  `qualified_application_mechanism`; public typed exits are `classified`,
  `scope_confirmation_required`, `mechanism_revision_required`, and `blocked`。
  Ordinary files remain usable as state/artifacts but cannot become business
  authority through OS identity or process primitives。
- preserved: normal-scenario semantics, AI-first judgment, deterministic
  recorder/validator limits, one owner per typed exit, Architecture promotion
  lifecycle, public package distribution rules, and #260/#267 matrix ownership。

## Project Check And Evidence Boundary

Use `guru-trellis-architecture-convergence:repository:1` /
`guru-trellis-architecture-convergence@1`, with `ARCH-GOV-006..008`,
`ADR-005`, and `ARCH-GAP-006`. The project check must cover the new owner and
caller boundary, one-way target-native routing, required concerns, before/after
fitness, single-writer and parallel scope, public projection closure, and
freshness across the exact candidate.

The Phase 2 project-check contract for this candidate is descriptor-bound:

- descriptor identity: `guru-trellis-architecture-convergence:repository:1`;
- check identity/version: `guru-trellis-architecture-convergence` / `1`;
- entrypoint: `docs/architecture/06-governance/change-contract.md`;
- applicable scope: owner topology, target-native route, required concerns,
  before/after fitness, single-writer, parallel scope, projection closure and
  exact-candidate freshness;
- rule refs: `ARCH-GOV-006..008`; decision refs: `ADR-005`; gap refs:
  `ARCH-GAP-006`;
- result contract: `guru-project-architecture-check-result-2.0`;
- freshness source: current task candidate and the exact committed range used
  by the stage.

The semantic owner must record one result for this descriptor with explicit
`before`, `after`, `status`, `blocking`, evidence locator and freshness identity
at each stage. This contribution defines the required binding; it does not
freeze a stale result or replace the live stage gate.

Targeted package/runtime, canonical/installed, three-platform reapply, drift,
sidecar and projection evidence may support this task. Full clean throwaway,
upgrade/update, release and exact-candidate matrices remain owned by #260/#267
and are not claimed here. Dynamic Phase 2, committed Branch Review, promotion,
and post-promotion evidence must be recorded by their respective owners rather
than frozen into this contribution.

## ADR Candidate

- candidate: `ADR-008-CANDIDATE`。
- status: `accepted_as_ADR-008_in_current-main-0.6.5-guru.44`。
- reason: the task adds a public semantic owner and therefore changes the
  architecture owner topology and its boundary with the existing scenario
  owner; this is an architecture decision, not merely a schema addition。
- decision candidate: adopt separate scenario and mechanism qualification
  owners, with mechanism revision returning to the original caller and no OS
  primitive carrying business authority。
- rejected direction: merge both judgments into normal-scenario qualification,
  let scripts classify mechanism semantics, or let a lock/process primitive
  become a business authority through an adapter。
- acceptance evidence: PR #346 independent full-diff review passed; serialized Architecture
  promotion accepted ADR-008 into `.44`. The promotion-created #332 diff still requires fresh
  Phase 2/Commit/Branch Review before Publication。

## Explicit Boundaries

- this historical contribution authorizes no further shared-current write, release mutation,
  Issue closure, or worktree cleanup。
- no business repository migration and no production cancellation, recovery,
  deployment, or data operation。
- no complete multi-platform upgrade/release matrix claim。
