# #376 Base-continuity command Architecture contribution

## Identity And Authority Boundary

- candidate identity: `architecture-contribution-376-base-continuity-command-v1`.
- source authority: live Issue #376 and accepted scope expansion comment
  `issuecomment-5585538277`.
- requirement authority:
  `docs/requirements-design-test-contributions/376-base-continuity-command/requirements.md`.
- behavior authority:
  `docs/requirements-design-test-contributions/376-base-continuity-command/design.md`.
- task locator: `.trellis/tasks/09-07-376-reduce-base-interference`.
- current/expected baseline: `docs/architecture/README.md` /
  `current-main-0.6.5-guru.45` / `active`.
- candidate successor: `current-main-0.6.5-guru.46`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`.
- change path: `target_native`; ADR required: `false`.
- lifecycle state: `candidate`; shared current remains unchanged until an
  independent committed review and serialized promotion.

## Boundary And Decision

The `.45` before-state treats base reconciliation as a semantic owner and
validator-only step. After a completed full Branch Review, however, a compatible
base advance changes the current candidate tree and Publication identity. The
old route could either force a full implementation/review replay or accept a
caller-asserted current identity; neither preserves the existing ownership
contract.

The target keeps `guru-reconcile-task-base` as the sole semantic owner and adds
one package-private `execute-base-reconciliation` command. After the AI has
reviewed the exact old/new base pair and the user has confirmed that displayed
local Git action, the deterministic executor validates clean branch-bound state,
expected task/base heads, candidate tree and ancestry, then creates the unique
local reconciliation commit. It performs no push or provider mutation.

`guru-review-branch:base_continuity` then binds the prior full-review commit and
the current reconciled task HEAD separately, reviews only the exact base delta,
conflict resolution, candidate tree and affected validation, and projects the
current HEAD to Publication. This is bounded continuity evidence, not a second
full Branch Review. Any task-content, authority, scope or implementation change
continues to use Phase 2, Task Commit and full Branch Review.

## Required Concerns

| Concern | Applicability | Candidate contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | Bind Architecture 2.0, expected `.45`, live #376 scope and project change contract v1. |
| `constitution-binding` | `applicable` | Preserve semantic ownership, change isolation and minimum necessary complexity without copying principle prose. |
| `boundary-and-decision` | `applicable` | Use `target_native`: one package-private expected-head executor and one bounded continuity route, with no legacy dual-read. |
| `owner-and-single-writer` | `applicable` | Reconcile owns semantic classification and the local commit; Review Branch owns bounded review; Publication owns current reviewed-content identity; serialized owners alone write shared `.46`. |
| `compatibility-and-exit` | `applicable` | Existing public Skill and exit ids remain; current-only schema versions replace stale continuity meanings without a compatibility branch. |
| `gap-and-deviation` | `applicable` | Close the post-review base-continuity ownership gap without reopening a closed GAP or adding a second writer. |
| `parallel-scope` | `applicable` | Task writes only its package/spec/test/projection and isolated contributions before promotion; `.45`, other contributions and Issue #108 sidecars remain untouched. |
| `evidence-and-freshness` | `applicable` | Bind expected heads, ancestry, candidate tree, prior/current review identities and real cross-Skill Publication integration; stale or mismatched facts fail closed. |
| `review-and-promotion` | `applicable` | Contribution must receive independent committed review before expected-`.45` serialized promotion; the promotion diff then re-enters fresh Phase 2, commit and full Branch Review. |

## Before And After

- before: 23 active Skills / 97 exits / 77 commands; compatible post-review
  base evolution cannot create a current reviewed Publication identity without
  replaying the full task lifecycle.
- after candidate: 23 active Skills / 97 exits / 78 commands; one new command is
  package-private, local-only and expected-head bound; public Skill and exit ids
  are unchanged.
- preserved: semantic owner boundaries, action-local confirmation, strict
  Publication reviewed-content checking, no remote mutation, no authorization
  persistence, and the full-review route for real content or authority changes.

## Project Check And Promotion

- descriptor identity: `guru-trellis-architecture-convergence:repository:1`.
- check identity/version: `guru-trellis-architecture-convergence@1`.
- refs: `ARCH-GOV-006..008`, `ADR-005`, `ARCH-GAP-006`.
- current result: candidate implementation and targeted tests show no owner
  expansion, dual writer, compatibility branch or fitness regression; the
  shared `.45` command graph is nevertheless stale and must not be used as
  current proof.
- expected current identity: `current-main-0.6.5-guru.45`.
- promotion target: `current-main-0.6.5-guru.46` after independent committed
  review of this contribution.
- predecessor handling: preserve `.45` Requirements/Design/Test body and release
  facts, add only `superseded` / `successor=.46` lifecycle locators, and correct
  the `.45` Design manifest's inconsistent historical `command_count` from 81
  to the live `.45` value 77.
- ADR: not required because the implementation applies the existing semantic
  owner plus deterministic executor pattern and changes no long-term decision,
  principle exception, GAP lifecycle, owner or compatibility exit.
