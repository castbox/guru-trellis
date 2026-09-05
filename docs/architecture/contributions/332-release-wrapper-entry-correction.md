# #332 Original public-entry convergence Architecture contribution

## Identity And Authority Boundary

- candidate identity: `architecture-contribution-332-release-wrapper-entry-correction-v1`.
- source authority: live Issue #332, live #330, PR #341, and the user's current clarification.
- requirement authority: `docs/requirements-design-test-contributions/332-release-wrapper-entry-correction/requirements.md`.
- behavior authority: `docs/requirements-design-test-contributions/332-release-wrapper-entry-correction/design.md`.
- task locator: `.trellis/tasks/09-05-332-release-matrix-public-wrapper-contract`.
- current/expected baseline: `docs/architecture/README.md` / `current-main-0.6.5-guru.44` / `active`.
- candidate successor: `current-main-0.6.5-guru.45`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` / `guru-trellis-architecture-change-concerns-v1`.
- change path: `dedicated_refactor_slice`; ADR required: `false`.
- planning state: `reviewed_candidate`; independent committed review and promotion remain pending.

This contribution records the architecture correction needed before #332 can resume release preparation. It does not
rewrite `.44`, execute implementation, claim Phase 2 or Branch Review success, or record dynamic release state.

## Boundary And Decision

The `.44` before-state contains PR #341's four-stage transaction capabilities, but exposes them through four newly
named facade wrappers/commands and in three stages marks the former `invoke.sh` entry as compatible or legacy. At the
same time, generic projection verifiers hard-code `scripts/invoke.sh`, which creates a second and contradictory source
of wrapper authority and rejects the valid `guru-restore-archived-task/scripts/restore-archived-task.sh` contract.

The target keeps the four pre-existing `scripts/invoke.sh` wrappers and stable command ids as the only public entry
identities. PR #341's low-call transaction and recovery capabilities move behind those entries. Runtime selects the
compatibility branch only when old argument forms are present. The four facade entries are deleted rather than
installed into a shared directory, and every generic distributor/verifier selects the exact wrapper declared by the
package Interface. This preserves behavior while removing dual entry authority and normal-path duplicate work.

## Required Concerns

| Concern | Applicability | Candidate contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | Bind Architecture 2.0, active/expected `.44`, live #332/#330 clarification, and project change contract v1. |
| `constitution-binding` | `applicable` | Hit `concept-semantic-completeness`, `cohesion-change-isolation`, `minimum-necessary-complexity`, and `debt-one-way-convergence`; create no duplicate principle prose. |
| `boundary-and-decision` | `applicable` | Use `dedicated_refactor_slice`: preserve public behavior/identity and converge the erroneous facade layer into original entries. |
| `owner-and-single-writer` | `applicable` | Each Skill's original command owns invocation mode; Interface owns public wrapper identity; task writes contributions; serialized owners alone write shared `.45`. |
| `compatibility-and-exit` | `applicable` | Old argument shapes remain package-local compatibility branches. Exit when declared old callers are migrated; no second public wrapper exists during migration. |
| `gap-and-deviation` | `applicable` | Close dual-entry, hard-coded-wrapper, and nonexistent-shared-asset deviations; retain no new deviation and do not reopen closed `ARCH-GAP-006`. |
| `parallel-scope` | `applicable` | Task may write its branch packages/specs/tests/contributions; it may not modify `.44`, other task contributions, old candidate worktrees, tags, Releases, or unrelated worktrees. |
| `evidence-and-freshness` | `applicable` | Planning evidence binds live #330/#332/PR #341, `.44`, Interface/package graph, task docs, and this contribution; implementation and release evidence must be regenerated at their owning stages. |
| `review-and-promotion` | `applicable` | Planning review may establish `reviewed_candidate`; independent committed full-diff review precedes expected-`.44` serialized `.45` promotion, whose diff re-enters Phase 2/commit/Branch Review. |

## Owners, Compatibility, And Deletion

- current entry/runtime owner: each of the four existing Skill packages and its stable original command.
- target entry/runtime owner: unchanged; only the internal Happy/compatibility dispatch is consolidated.
- public wrapper authority: each package's `interface.json.public_contracts.invocation.wrapper`.
- task writer: `332-release-matrix-public-wrapper-contract` worktree.
- shared-current writer: serialized Architecture and RDT promotion owners only.
- compatibility owner: the original command's package-local runtime.
- compatibility exit: remove the old-argument branch only after live callers and fixtures prove it has no remaining
  consumer under a separately reviewed migration; this task does not pre-empt that later decision.
- facade deletion conditions: original wrapper directly reaches transaction behavior; old argument fixtures pass;
  canonical/installed/platform inventories select one Interface wrapper; managed removals and sidecar checks pass.

Allowed parallel scope is task-isolated package/runtime/test/spec/contribution work. Forbidden scope is shared `.44`
mutation before promotion, a new shared companion facade, a second public command, changes to #348 identity, and any
write to the old detached candidate checkout.

## Before And After

- before: 23 active Skills / 97 exits / 81 commands; four closeout stages expose a second facade command/wrapper;
  generic consumers also guess `scripts/invoke.sh`; preset README names nonexistent shared facade assets.
- after candidate: 23 active Skills / 97 exits / 77 commands; each closeout stage has one original public wrapper and
  command; compatibility is an argument branch; generic consumers follow Interface; shared assets match disk.
- preserved: semantic owners, public Skill ids, typed exits, public DTO meanings, confirmation boundaries, mutation
  ordering, expected-head/freshness, mapped recovery, watcher, stdout-loss recovery, terminal stop, historical `.44`,
  historical PR #341, tags, Releases, and Issue closure ownership.

## Project Check Contract And Planning Result

- descriptor identity: `guru-trellis-architecture-convergence:repository:1`.
- check identity/version: `guru-trellis-architecture-convergence@1`.
- entrypoint: `docs/architecture/06-governance/change-contract.md`.
- applicable scope: authority/path uniqueness, required concerns, owner/single-writer, compatibility exit, before/after
  regression, contribution review, expected-current promotion, and release freshness.
- refs: `ARCH-GOV-006..008`, `ADR-005`, `ARCH-GAP-006`.
- result contract: `guru-project-architecture-check-result-2.0`.
- planning before: public-entry ownership and generic wrapper authority are contradictory.
- planning after: one original entry per closeout Skill, Interface-driven consumers, bounded compatibility branch, and
  expected-`.44` successor plan are complete and mutually consistent.
- planning status: `pass`, `blocking=true`; evidence is this contribution plus the task planning docs and live
  #330/#332/PR #341 reads. This pass covers planning adequacy only. Implementation, Phase 2, committed review,
  promotion, and exact-candidate Release Gate remain unverified and must be rerun from their own fresh identities.

## Evidence, Review, Promotion, And ADR

- planning test refs: task `implement.md` validation strategy and RDT `test.md`.
- planning runtime refs: current Interface/command/package/projection inventories at base `593872c4...`.
- external refs: live #330, live #332, merged PR #341, and remote `main@593872c4...`.
- external status: verified for planning authority only.
- review: Planning semantic review complete; independent committed full-diff review pending.
- expected current identity: `current-main-0.6.5-guru.44`.
- promotion: required; promoted identity empty until serialized owner creates `.45`.
- ADR: not required because this contribution restores conformance to existing constitution and `ADR-005`; it adds no
  new architecture decision, owner, exception, or compatibility authority.

## Explicit Boundaries

- Do not create a new task, branch, worktree, public Skill, public wrapper, shared facade, tag, or GitHub Release.
- Do not modify the existing `.44` authority or `docs/architecture/contributions/332-release-v0615-guru5.md`.
- Do not modify the old detached candidate checkout or reuse its Release Gate evidence.
- Do not execute Phase 2, task activation, commit, push, PR, merge, Release Gate, Issue closure, or cleanup during this
  Planning contribution step.
