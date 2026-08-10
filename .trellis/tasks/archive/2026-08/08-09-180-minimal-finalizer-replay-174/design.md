# Technical Design

## 1. Design Principles

1. AI owns intent, scope, adequacy, readiness, findings and route; scripts own only repo-bound facts, schema validation, deterministic mutations and minimal recording.
2. Public DTOs are minimal direct-consumer handoffs. Owner-private state is ignored, short-lived and deleted after its consumer completes. Durable archive data exists only for a named historical consumer.
3. Git/GitHub/Trellis live facts are reread at each boundary. A digest can bind one local consumer but is never workflow authority or user authorization.
4. Current contracts use new versioned IDs. Retired `published`/closeout schemas remain byte-stable fixtures and never enter current routing.

## 2. Target Workflow Graph

```text
guru-create-task-commit:committed
  -> guru-review-branch:passed
  -> guru-review-task-publication:ready
  -> guru-finalize-task:ready_for_merge
  -> guru-merge-task-pr
       merged           -> guru-finalization-finish-response
       merge_blocked    -> task-pr-merge-blocked
       closure_mismatch -> task-pr-closure-mismatch
```

- Finalizer retains its existing recovery owners (`verification_required`, `publication_review_stale`, `resume_finalization`, `reprepare_required`, `blocked`) and replaces only current terminal `published` with `ready_for_merge`.
- Adding `guru-merge-task-pr` changes the current graph to 15 mandatory Skills and 57 external exits. The two new stop consumers make the workflow/stop target closure 33; validators and durable docs must derive/assert the same values from the graph rather than leave stale 14/54/31 literals.
- The finish response moves after `guru-merge-task-pr:merged`. `ready_for_merge` is not completion and does not close the Issue.

## 3. Finalizer Transaction Redesign

### 3.1 State Separation

| State | Location | Lifetime | Content |
| --- | --- | --- | --- |
| Publication DTO | public in-memory projection | Finalizer entry only | task ref, reviewed commit, exact PR title/body |
| Finalizer transaction | `.trellis/.runtime/guru-team/<task>/finalization-transaction.json` | first external side effect through `ready_for_merge`/blocked cleanup | current schema/version, task/repo/base/branch identity, reviewed/publication head, exact publication input needed for resume, next transition, optional bound PR identity |
| Finalizer semantic gate | existing owner-private runtime | one checked transition | AI route and minimal executor marker only |
| Finish summary | archived task | durable | minimal change-context index/summary and PR identity |
| Verification result | archived task only when applicable | durable direct consumer | minimal immutable verification identity/profile/result/boundaries |

The transaction schema must not copy live remote facts, reviewed paths, archive projection, full finish-summary template, command transcripts, authorization or complete verification evidence. Preview/execute rebuild those facts from Git/GitHub/task files and compare them with the small immutable identity before mutation.

### 3.2 Transition Model

1. `publication_ready`: build side-effect-free live preview in memory.
2. After one Finalizer confirmation, recorder writes only the checked semantic gate.
3. Immediately before the first external mutation, executor writes minimal recoverable transaction input when the current execution will return a mapped re-entry before `ready_for_merge`; a no-re-entry execution keeps that input in memory.
4. Push exact `publication_head` with Git transport.
5. When verification applies, emit the mapped verifier route. The transaction points to the immutable target identity, not to a copied verifier report.
6. Create/reuse exact Draft, archive via official `task.py archive --no-commit`, commit/push archive metadata, enforce local/remote/PR expected-head equality, mark Ready.
7. Project `ready_for_merge`, validate it, then delete Finalizer transaction/gates/requests and any superseded owner-private state.

Archive recovery must be based on live Git commit/tree/PR facts plus minimal `finish-summary.json`/verification result, not a committed transaction plan. Pre-current archived `closeout-plan.json` remains readable only in explicit legacy recovery tests; current tasks never create or retain it.

## 4. Verification Reuse

### 4.1 Identity Key

The verifier reuse key is the closed tuple:

```text
target repo + remote/ref + branch_review_commit + publication_head
+ extension source commit + capability profile
```

The private execution checkpoint records command completion and sanitized result references incrementally. If wrapper/stdout serialization fails after command success, re-entry checks the exact tuple and reconstructs the owner result from those completed facts. It reruns only missing capabilities; a complete tuple result is recorded once and directly checked by Finalizer.

### 4.2 Durable Result

Replace the current large task artifact with a versioned minimal result containing only:

- schema/skill identity and stable `verification_ref`;
- target repo/ref, reviewed/publication head and source commit;
- selected capability profile;
- semantic result and explicit unverified boundaries;
- final consumer/result identity needed by Finalizer and archived history.

Full command argv/output digest inventory, asset catalog, ownership scan, findings history and retry metadata remain owner-private and are deleted after successful Finalizer consumption. Current and legacy schemas are selected explicitly by Interface versions.

## 5. `guru-merge-task-pr` Package

### 5.1 Public I/O

- Workflow input profile: Finalizer seed containing canonical repo/PR identity, `expected_head_sha`, reviewed base/head branches and the reviewed close-Issue set, plus target-authored `profile=ready_for_merge`, `mode=workflow`.
- Standalone profile: repo-bound PR URL/number plus caller-authored expected SHA, base/head branches and close-Issue set; the Skill rereads the same live facts and does not require an active task.
- Outputs:
  - `merged`: minimal PR URL/number and merged commit identity for finish response.
  - `merge_blocked`: closed reason/remediation for pre-merge live gate failure.
  - `closure_mismatch`: merged PR identity plus exact close-issue mismatch needed by the recovery stop.

No input/output carries authorization, Finalizer transaction, full PR review payload, local main identity or cleanup instructions.

### 5.2 Semantic And Deterministic Boundary

The AI gate owns:

- repository/base/head correctness and expected-head continuity;
- PR Open/Ready state, required checks/reviews and mergeability sufficiency;
- merge policy/method selection when uniquely determined;
- close keyword scope and all close issues being Open before merge;
- whether the exact plan is ready for one current-dialogue confirmation.

Deterministic runtime commands own:

- repo-bound `gh pr view`/`gh api` fact capture with required fields;
- gate schema/freshness/consumer validation;
- `gh pr merge --match-head-commit <sha>` (or equivalent expected-head precondition) using the reviewed method;
- post-merge repo-bound reread of PR and Issues and timestamp ordering;
- deletion of the owner-private merge gate after a terminal projection.

The package has a thin dispatcher-only wrapper, package-local schemas/examples/evals/tests, registry row, current production manifest coverage and installed discovery copies. It never calls `guru-sync-base` or local Git synchronization commands.

## 6. Task Commit Eligibility Matrix

`guru-create-task-commit` keeps `judgment_mode=semantic` and existing commit execution ownership. The AI-authored candidate gains an objective `routine_auto_commit_eligible` conclusion with evidence references for:

- dedicated task/worktree/branch identity;
- default/protected/shared/other-task exclusion;
- no remote branch or PR consumer;
- current Phase 2/finding closure and fixed scope/purpose;
- exact owned staging set and clean unrelated-path classification;
- ordinary new commit operation and canonical message.

The checker recomputes objective Git/GitHub facts but does not decide eligibility. A checked eligible candidate executes immediately. Same-scope corrections use the current `revision-required` loop; unsafe or authority-changing cases remain `blocked` or conditional human choice. No confirmation field is added to the candidate schema or public DTO.

## 7. Migration And Compatibility

- Preserve old `published` output schema/example and old closeout/verification schemas as immutable legacy assets with explicit `legacy_*` IDs.
- Add new current versions for `ready_for_merge`, minimal transaction/verification state and merge package; current Interface aggregates select only these versions.
- Update `guru-team-extension.json`, preset managed asset inventory and installed manifest validation to remove current closeout-plan claims and add merge assets.
- Update all graph-count assertions, production contract manifests, eval route groups and finish-family integration tests in one activation transaction.
- Dogfood copies are produced by preset apply; no manual divergence is accepted.

## 8. Failure And Recovery Matrix

| Condition | Route | Mutation rule |
| --- | --- | --- |
| Publication/content identity stale | `publication_review_stale` | no publish/merge mutation |
| Verification evidence missing for current immutable tuple | `verification_required` | run only missing verification work |
| Same transaction interrupted | `resume_finalization` | reuse current transaction and current confirmation only while exact plan unchanged |
| Archive month/provenance identity changes | `reprepare_required` | rebuild and reconfirm changed Finalizer plan |
| Finalizer reaches Ready PR | `ready_for_merge` | clean Finalizer private state; Issue remains Open |
| PR gate/check/review/mergeability/head fails | `merge_blocked` | no merge mutation |
| Expected-head merge succeeds and issues auto-close | `merged` | no local main sync or cleanup |
| PR merged but close issue state/timestamp mismatches | `closure_mismatch` | read-only report; never hand-close |

## 9. Validation Architecture

- Package contract/schema/eval tests for Finalizer, Verifier, Commit and new Merge Skill.
- Runtime unit tests for transaction recovery, verification exactly-once, expected-head merge and closure timestamp ordering.
- Merge authority regressions for post-Finalizer PR-body close-keyword additions/removals and base/head branch drift while the head SHA remains unchanged.
- Finish-family integration from Publication DTO through Finalizer `ready_for_merge`, Merge `merged`, and finish response.
- Negative tests for Draft/stale head/missing checks/reviews/non-mergeable PR, close-keyword mismatch, manual early closure, no GitHub auto-close and forbidden Issue close calls.
- One controlled #174 replay session with chained public projections, wrapper execution receipts, dialogue-boundary event receipts, call counters and terminal artifact scan; isolated canned eval totals are not replay evidence.
- Source/installed package validation, production manifest activation, canonical/dogfood byte equality, preset initial/reapply, marketplace init/preview/switch, official update/reapply, all-platform discovery, executable bits and zero `.new`/`.bak`.

## 10. Rollback

- Before publication, revert the single task commit range; legacy schemas remain available and no user repository migration is required.
- Activation is fail closed: registry/current manifest/workflow/package bytes switch together or preset validation preserves the previous known-good graph.
- No database, deployment, secret, container or infrastructure migration is involved.
