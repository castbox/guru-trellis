# #452 All-Platform Projection And Exact Selection Contribution

## Identity And Authority Boundary

- candidate identity: `architecture-contribution-452-all-platform-projection-v1`.
- lifecycle state: `reviewed_promoted`; shared current is `current-main-0.6.17-guru.58` after expected-current-bound serialized Architecture promotion.
- source authority: live Issue #452 plus superseding platform-contract comment `issuecomment-5748684130`; `issuecomment-5747785875` is superseded for `--all-platforms` semantics.
- task locator: `.trellis/tasks/09-20-452-all-platform-support`.
- related RDT contribution: `docs/requirements-design-test-contributions/452-all-platform-support/`.
- source/expected baseline: `docs/architecture/README.md` / predecessor `current-main-0.6.17-guru.57` / `active`; promoted successor `current-main-0.6.17-guru.58` / `active`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` / content identity `9f6100720327ad1f9a7f438bc829d568dfe71b368ae1c3fc184e2d26f8ac470b` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1` / concern set `guru-trellis-architecture-change-concerns-v1`.
- Guru contract: `guru-maintain-architecture-baseline:2.0`.
- change path: `target_native`.

This contribution owns only the #452 platform-distribution and installed-selection
delta. It does not rewrite the already promoted #443 session-binding history,
activate the #434 production graph, or authorize a release, tag, GitHub Release,
business-repository production upgrade, push, PR, merge, Issue closure, or cleanup.

## Architecture Decision

The supported platform model has exactly two authority layers:

1. `upstream_platforms`: the complete platform inventory from the pinned upstream
   Trellis `AI_TOOLS` registry. The current pinned inventory contains 22 platform
   identities. Each descriptor retains the canonical `AITool` id and its unique
   public `cliFlag`, plus registry identity, source commit, native template/root
   and entry form.
2. `selected_platforms`: the exact non-empty set of registry `cliFlag` values
   recorded by the target repository installed manifest/provenance. Each value
   maps uniquely to one canonical `AITool` id. Install, reapply, update, drift
   and upgrade consumers use this target-local selection unchanged.

`default_platforms = [claude, codex, cursor]` is an installer entry policy used
only when no `--platform` value is supplied. It is not a third capability
inventory. The guru-trellis repository is one business-repository instance whose
explicit dogfood selection is the same three platforms.

Repeated `--platform <cli-flag>` selects an exact subset. When none are supplied,
the installer selects the default three. The public `--all-platforms` option,
its manifest state and every upgrade/throwaway branch are removed; callers that
need a larger set repeat `--platform`. Upgrade owners do not use the default:
they reread the target manifest and reapply its exact selection through repeated
`--platform` arguments.

OpenCode is one ordinary upstream platform. Its explicit projection and native
load path must work, but canonical support does not install it into guru-trellis
dogfood. No `guru_supported_platforms`, four-platform tier, or deferred 18-platform
inventory remains in the target architecture.

## Authority And Ownership

- pinned upstream `AI_TOOLS` owns the complete set of platform identities and
  upstream-native template/root metadata;
- the Guru preset owns explicit projection descriptors, public package material,
  managed paths, executable modes and deterministic validation for every pinned
  upstream identity;
- the target repository installed manifest/provenance owns `selected_platforms`;
- the installer owns flag parsing and selection expansion, but does not invent or
  widen an upgrade selection;
- the upgrade/reprepare caller owns reading and validating the target manifest,
  then passing repeated `--platform` arguments;
- guru-trellis dogfood manifest and drift validation own only the explicit
  Claude/Codex/Cursor installed selection;
- public Skill/package contracts remain platform-neutral and package-private
  `tests/` remain source-only.

The current installer, compatibility matrix and installer test source files are
all near the repository's 3000-line threshold. Before adding platform behavior,
the implementation mechanically splits inventory/selection logic,
compatibility descriptor helpers and new platform-selection tests into focused
modules while preserving behavior and keeping every touched non-generated file
within the limit.

The single writer for canonical platform descriptors and installation projection
is the Guru preset. The single writer for one target repository's installed
selection is that target's preset application transaction.

## Required Concerns

| Concern | Applicability | #452 binding |
| --- | --- | --- |
| `authority-binding` | `applicable` | Bind Architecture `.57`, constitution content identity, change-contract identities, live Issue #452 and the pinned upstream registry source. |
| `constitution-binding` | `applicable` | `concept-semantic-completeness`, `cohesion-change-isolation`, `minimum-necessary-complexity` and `debt-one-way-convergence` require two named authorities, one selection writer and deletion of the unsupported middle tier. |
| `boundary-and-decision` | `applicable` | `target_native`; upstream inventory, default entry policy and target installed selection have distinct owners and consumers. |
| `owner-and-single-writer` | `applicable` | Upstream owns platform identities; Guru owns projection descriptors; each target manifest owns its exact installed selection. |
| `compatibility-and-exit` | `applicable` | Existing valid selections remain valid; upgrade preserves them exactly. The old Guru-supported/deferred tier and source-dogfood inference are deleted once all consumers use the two-layer model. |
| `gap-and-deviation` | `applicable` | Close the four-platform/deferred-model deviation and stale current platform projection without changing #434 or release ownership. |
| `parallel-scope` | `applicable` | Task-local Architecture/RDT contributions and preset implementation may proceed; shared current authority, #434 routes and release transactions remain serialized or forbidden. |
| `evidence-and-freshness` | `applicable` | Bind current task planning, pinned upstream inventory, manifest selection fixtures, source/installed/platform parity, dogfood drift and exact candidate validation. |
| `review-and-promotion` | `applicable` | Planning candidate -> fresh Phase 2 -> Task Commit -> independent committed full-diff Branch Review -> expected-current-bound Architecture/RDT promotion -> fresh downstream gates. |

## Current And Target Boundaries

Before this task, current `.57` and the existing #452 candidate mix historical
three-platform evidence with a candidate Shared/Codex/Claude/Cursor/OpenCode
projection. Installer naming and ownership assertions can retain an unnecessary
all-platform selection mode or infer a target selection from source dogfood. That
state cannot represent the accepted inventory and exact-selection contract.

After the candidate:

- one pinned inventory describes every upstream platform that may be selected
  explicitly;
- each upstream platform has an explicit native projection descriptor and
  fail-closed parity validation;
- repeated `--platform` expresses every explicit subset; no full-inventory
  convenience option exists;
- no flags select Claude/Codex/Cursor for a new installation;
- upgrades preserve the exact target-manifest selection through repeated
  `--platform`, including one platform, arbitrary subsets, the three-platform
  dogfood set and all 22 platforms;
- guru-trellis drift compares shared assets plus its selected three platform
  projections while canonical ownership still validates the complete inventory;
- OpenCode explicit install and actual-load are validated without making OpenCode
  a dogfood default;
- the old four-platform/deferred middle layer and fixed overlay-count inference
  have no consumer and are removed.

## Compatibility, Gaps And Deletion

Compatibility is required for existing valid installed selections, not for the
incorrect intermediate capability taxonomy. The preset and upgrade owner must
continue to honor `.new`/`.bak`, previous-managed hashes, sidecar/removal
provenance and unknown-local-edit preservation.

- closed by this candidate: the current candidate's four-platform supported tier,
  the 18-platform deferred set, the public `--all-platforms` option and related
  state, default Codex/Cursor-only behavior, and source-dogfood inference during
  upgrade;
- retained: #434 production graph activation, external CLI availability evidence,
  exact-candidate Release Gate, tag, GitHub Release and business production proof;
- new deviations: none accepted. A missing upstream projection is a blocking
  implementation defect, not a deferred-success state.

Deletion conditions are complete when no canonical/installed/spec/test consumer
reads `guru_supported_platforms` or `deferred_platforms`, every upgrade path uses
manifest-derived repeated `--platform`, and source/installed/platform/dogfood
validators agree on their separate inventory and selection responsibilities.

## Parallel Scope

Allowed task-isolated work:

- this Architecture contribution and the matching RDT contribution;
- preset inventory/descriptors, installer, manifest/provenance, ownership,
  compatibility/throwaway helpers, tests and documentation required by #452;
- generated dogfood synchronization after canonical implementation is reviewed.

Forbidden parallel mutation:

- direct shared-current Architecture/RDT edits outside serialized promotion;
- #434 Delivery/Completion/Closure/Finish graph activation;
- upstream Trellis source, global npm or `node_modules` modification;
- release/tag/GitHub Release, business-repository mutation, or reuse of stale
  Phase 2 and Branch Review evidence.

## Project Check And Evidence Plan

- check descriptor: `guru-trellis-architecture-convergence:repository:1`;
- check id/version: `guru-trellis-architecture-convergence` / `1`;
- entrypoint: `docs/architecture/06-governance/change-contract.md`;
- refs: `ARCH-GOV-006..009`, `ARCH-INT-001`, `ARCH-INT-006`, `ARCH-INT-012`,
  `ARCH-GAP-006`, `ARCH-GAP-008`, `ADR-005`, `ADR-009`;
- before: mixed three/four-platform candidate wording, obsolete all-platform
  semantics and no #452 task-owned authority;
- after candidate: two-layer authority, complete pinned inventory projection,
  exact target selection preservation and explicit three-platform dogfood;
- planning check status: reviewed against current Issue/task/Architecture/RDT
  authority; implementation/runtime evidence remains `unverified` until Phase 2;
- required test refs: `T452-01..12` in the matching RDT contribution;
- required runtime refs: installer selection, manifest/provenance resolver,
  ownership validator, dogfood drift checker, compatibility matrix and throwaway
  actual-load evidence;
- external refs: pinned upstream Trellis `AI_TOOLS` source identity and Issue #452;
- external status: `unverified` for platform CLIs unavailable in the current
  environment; absence of a CLI does not defer its projection implementation.

No new ADR is required. This contribution applies existing decisions that
registry/interface authority drives projection, installed manifest authority
drives target selection, one writer owns each boundary, and unsupported
intermediate inventories must converge away. It does not introduce a new
long-lived tradeoff, exception, dual writer or compatibility layer.

## Review And Promotion

- review: `reviewed`; independent committed range is
  `origin/main@361da96327824503ffb4fb4189291b3b9b4e23ae...HEAD@b4b4ebfdd29188a36866fd832b65cc6438420acf`;
- promotion: `reviewed_promoted`; expected current identity was
  `current-main-0.6.17-guru.57` and promoted current identity is
  `current-main-0.6.17-guru.58`;
- any promotion-created diff must re-enter fresh Phase 2, Task Commit and
  independent complete-range Branch Review before Publication.
