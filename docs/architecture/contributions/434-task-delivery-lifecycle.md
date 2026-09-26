# #434 Task Delivery Lifecycle Architecture contribution

## Identity And Authority Boundary

- candidate identity: `architecture-contribution-434-task-delivery-lifecycle-v1`.
- lifecycle state: `reviewed_candidate`; not promoted.
- source authority: `castbox/guru-trellis#434`, contract `2026-09-18-r4`.
- task locator: `.trellis/tasks/09-18-434-task-delivery-lifecycle`.
- behavior authority: task `prd.md` and `design.md`.
- source/expected baseline: `docs/architecture/README.md` / `current-main-0.6.17-guru.66` / `active` at `origin/main@bab8cfcd534692735b9240b25dd8bc63e40a5cb4`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`.
- proposed decision: [ADR-012](../adr/012-task-delivery-lifecycle.md).

This candidate now records the uncommitted #434 activation change set on the
selected base. #435/#436/#443 historical capabilities and #454 C2-C7/D443/D436
source changes are merged. The former 32 active / six planned selector and
22/98 graph have been replaced in this worktree by 34 active packages / 155
package exits / 104 commands and 33 mandatory invokes / 153 production exits.
Installed source/Shared/Codex/Claude/Cursor projections validate with zero
conflicts and sidecars after the managed-backup recovery. Current integration,
fixed complete-old/new graphs and mixed-graph rejection pass. The representative
Codex clean/focused local workflow sample and two preset reapplications pass;
remote marketplace installation is outside #434 acceptance. `.66`
remains shared current authority. After the 1.7 installed-distribution fix,
two fresh independent read-only subagent reviews of the uncommitted candidate
found no P0-P3 findings. Formal Phase 2, committed Branch Review, serialized promotion and
the dedicated multi-platform Release matrix remain open.

## Before And Target

Before: `guru-review-task-publication -> guru-finalize-task ->
guru-merge-task-pr` binds business Delivery to pre-merge task archive and uses
`guru-restore-archived-task` when merge-time task work is discovered. Issue
closure intent is encoded before whole-task completion, and one merge is
treated as the terminal closeout candidate.

Target: one active task can produce ordered business Delivery cycles. A
Delivery merge produces only a Delivery result. Fresh Task Completion decides
remaining work or completion; only completion reaches explicit Issue Closure,
Official Finish persistence, and Resource Cleanup. A normally finished task
can later Reactivate under the same task identity and route to the actual
requirements, Planning, implementation, validation, or evidence-refresh owner.
If its next generation only needs validation, Completion uses the verified
preceding terminal archive and current-generation reactivation/validation
evidence without a new business Delivery. Delivery-backed Completion still
requires its own generation's merge. Old-generation closeout, merge and Finish
receipts cannot be projected into either current completion path.

## Ownership And Single Writers

- #435 packages own Delivery Review, Publish, Merge and required current-slice
  adaptations; they do not own whole-task completion or archive.
- #436 packages own Completion, Closure, Finish, Cleanup and Reactivate; #443 owns Session Binding, Rebind, Switch and Resume; they do
  not own Delivery payload or merge readiness.
- #434 owns the #454 Phase E434 canonical package implementation (six planned
  IDs and independent Issue creation owner), global workflow graph, exact
  interface/version binding, atomic activation, migration statement, and
  old-edge retirement. #454 Phase C/D substrate and #435/#436/#443 step-local
  semantics remain with their respective owners.
- the global workflow owns ordering and unique typed consumers, not step-local
  semantic results.
- The task-creation owner binds the reviewed TaskRef to the current Shanghai
  business date at mutation time; official task creation refuses a changed
  date before writing the task, while read-only recovery keeps its prior ref.
- Approval's checked `approved` DTO carries the reviewed planning identity.
  Activation consumes it unchanged and compares it with the current three
  planning documents after the private checkpoint is retired. A changed plan
  returns to Approval without treating the digest as approval authority.
- Completion's single evidence-pending exit has two declared authoring variants
  against one consumer input: same-generation Delivery merge or verified prior
  Reactivate archive. Both project to the same current profile and validate
  independently; neither adds a second global edge.
- Finish's administrative bookkeeping rejects legacy and current Delivery
  trailers as well as Issue-closing keywords, including on an open-PR re-entry
  before merge. Validation precedes the initial local archive mutation.
- Installed graph validation rejects parsed invoke/exit markers outside the
  currently declared package graph, not just missing required markers.
- RDT and Architecture serialized owners remain the only writers of shared
  current authority.

## Required Concerns

| Concern | Applicability | Candidate contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | Bind #434 r4 and #454 current contract, merged #435/#436/#443 plus D443/D436 exact interfaces, current `.66`, derived candidate 34/155/104 and 33/153, and current installed graph; old 32/39 inventories are historical. |
| `constitution-binding` | `applicable` | Use official Trellis extension surfaces; preserve semantic completeness, owner isolation, minimum complexity and one-way convergence. |
| `boundary-and-decision` | `applicable` | Delivery, Completion, Closure, Finish, Cleanup and Reactivate are distinct lifecycle concepts with closed owners and unique edges. |
| `owner-and-single-writer` | `applicable` | Child packages own step semantics; #434 owns only the global graph; deterministic scripts do not decide routes or completion. |
| `compatibility-and-exit` | `applicable` | Directly replace the old active closeout graph. No dual graph, old-output adapter or schema dual-read remains on current main. |
| `gap-and-deviation` | `applicable` | Close the pre-merge archive/Restore coupling and early closure-intent gap without adding an Acceptance phase or generic archive recovery. |
| `parallel-scope` | `applicable` |  #435/#436/#443 may build isolated additive packages; none may switch production workflow before #434 activation. Shared current promotion remains serialized. |
| `evidence-and-freshness` | `applicable` | Current source/installed closure reports 34 active/104 commands and 33 mandatory invokes/153 production exits, with zero sidecars and dogfood drift. Activation 4/4 and projected Completion authoring variants 47/47 pass. Installer/upgrade/native-load 181/181, focused gate 62/62, lifecycle/Completion/Finish 217/217, current graph/qualification 95 passed/1 source-environment skip, and a local Codex clean/focused sample passed. Two fresh independent read-only reviews found no P0-P3 on the uncommitted candidate; formal Phase 2 and committed full Branch Review remain pending. Pinned-old eval is historical only; remote marketplace is unused and the dedicated full Release matrix is outside #434 acceptance. |
| `review-and-promotion` | `applicable` | Independent full-diff review precedes expected-current promotion; promotion-created diff repeats Phase 2, commit and full Branch Review. |

## Compatibility And Deletion

Long-term runtime compatibility is not required. The transition boundary is a
version boundary:

- before activation, the complete old graph remains current;
- after activation, the complete new graph is current;
- in-flight old tasks finish on a pinned old version or use explicit manual
  disposition;
- normally completed legacy archives may enter fresh Reactivate;
- incomplete old archive residue is not a valid Reactivate input.
- a schema-1 or legacy schema-2 archive without generation, or old schema-2 with explicit generation zero and its matching retired `task.json.archive_dir`, is accepted only when its terminal TaskId, generation and summary are present in the selected Git base and match the unique archive addition, with no C5 ledger; reviewed source correction can derive the legacy Issue from an exact URL or `GitHub Issue #N` scope with explicit repository context. Local-number Issue discovery also checks the selected repository's GitHub origin. Matching in-flight old Finalizer state blocks Reactivate. Other explicit-generation schema-2 archives require a C5 Finish seal or manual receipt.
- old archive discovery by source Issue reads the committed task source and archive Git identity; empty finish-summary indexes cannot exclude a valid source. It proves a unique TaskId/source before Reactivate; directory naming and old PR state are not completion authority.
- `castbox/ai-chat-roleplay-backend#154` demonstrates an in-flight old chain whose merged PR #156, older remote head and newer reviewed local head disagree with Finalizer preview/execution. Pin a compatible old version or review each manual disposition; do not rewrite business mappings, reuse the merged PR or synthesize new Delivery results.

The old Publication, Finalizer, Merge and Restore packages lose active runtime
authority only when every new package/interface/consumer/projection is present
and new-graph integration passes. Their current selectors, markers, consumer
schemas, platform projections and current-only tests then exit together.
Historical Issues, ADRs, version docs and Git history remain historical records.
Post-publication base continuity now targets `delivery_publication` consistently
through Reconcile and Branch Review; qualification publication consumers project
the current Delivery Review owner. The retired Finalizer/Publication identifiers
remain historical-only and cannot become current workflow authority by re-entry.
Completion's two current evidence authoring variants are declared by the new
`skill-interface-1.7` contract. The previously published 1.4 schema keeps its
byte identity; this migration changes only Completion's interface and its
current registry/manifest/discovery/eval consumers, not historical schema IDs.
The preset's shared schema inventory and installed provenance must include
1.7 as well; source-only schema validation cannot establish installed closure.

## Project Check

Descriptor: `guru-trellis-architecture-convergence:repository:1` /
`guru-trellis-architecture-convergence@1`.

Earlier planning result was bound to `.56` and is stale after base reconciliation. A fresh Planning architecture review must bind `.66`, constitution,
change contract, exact owner split, target-native path, old asset exit,
parallel package boundary, contribution/ADR requirement and promotion re-entry.
The implementation before/after state and exact child interfaces are now in
the candidate; its current test evidence is recorded above. Independent Phase 2
and complete Branch Review remain required before promotion.

## Review, ADR, And Promotion

The candidate requires ADR-012 because it changes lifecycle concepts, closure
ownership, archive timing, recovery semantics and the active owner graph.
Independent committed Branch Review is pending; two earlier read-only reviews
do not establish the revised candidate. Expected current identity is
`current-main-0.6.17-guru.66`; any current advance requires fresh synchronization.
Promotion is required only after implementation, project checks and independent
full-diff Architecture review. Promotion-created bytes must re-enter Phase 2,
Task Commit and independent Branch Review before Delivery publication.
