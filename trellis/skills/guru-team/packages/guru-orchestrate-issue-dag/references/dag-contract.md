# DAG Contract

## Graph And Live Dependency Authority

A node is the canonical pair `owner/repo + positive Issue number`. Use
`owner/repo#N` as its conversation identity. Different repositories’ #N are
different nodes; neither the coordinator directory nor Skill provider selects
a node’s repository. `depends_on: [A, B]` means that both A and B must satisfy
their complete completion contracts before this node can start. An edge is a
completion dependency, not permission to start from an unmerged branch.
Contract-only prerequisites use the separate readiness rule below; they do not
change the meaning of an existing `depends_on` edge.

Normalize graph input in the conversation. Require unique repository-qualified
node identities, included predecessor identities, no self-edge, and no directed cycle. Repeated edges
may be collapsed without changing meaning. Report a concrete cycle path when
one exists. Preserve node input order as the ready-set tie-breaker, never as an
implicit dependency. A serial list must explicitly become adjacent edges.

Read live Issue bodies, accepted maintainer comments, linked PRs, and repository
workflow. Classify referenced predecessors as hard, delivery-order preference,
informational, or superseded. Only accepted hard completion prerequisites
require full predecessor completion for eligibility. Required contract inputs
constrain only their consuming work under the readiness rule below. The user's
explicit graph may add an ordering preference; it may not remove a live hard
prerequisite. Do not revive superseded references.

If an included hard full-completion predecessor is missing an edge, show the
required edge and resolve the graph discrepancy before launch. If a hard
full-completion prerequisite is outside the selected nodes, verify its
completion directly and recheck it before the
dependent node starts. An incomplete external prerequisite blocks that node;
do not silently add another Issue, remove the prerequisite, or widen the run.
If it is already incomplete at initial preflight, return `dry_run_blocked`.
If it becomes unsatisfied after launch, apply the runtime failure policy.

Conflicting product or architecture authority needs a human decision. A stale
child summary is a discovery hint, not a change to accepted Issue scope.

## Contract Readiness And Mock Development

For Mobile/Web work that needs an API contract, distinguish a usable contract
from its provider Issue's complete implementation. When current authority
requires only the contract to start, normalize that prerequisite separately
from `depends_on`. Do not infer a full-completion edge from an API reference.
Do not silently reinterpret an explicit completion edge or a live requirement
to wait for backend completion; resolve that real discrepancy before affected
admission.

A node may declare `contract_dependencies`, a list of objects containing:

- `provider`: the repository-qualified Issue supplying the contract;
- `contract`: its live document/section locator, or the clearly identified
  expected contract location while its production is pending;
- `work`: the frontend work that consumes this contract.

Equivalent natural-language input or an unambiguous live contract-only
requirement may be normalized into that same form. Resolve the provider,
contract and consuming work before dispatch; a related link alone adds no gate.
The provider may be outside the selected nodes. Read its contract directly
without adding that Issue to the run or requiring its full completion. These
inputs identify ordinary prerequisites, not a readiness assertion or new state
artifact. Omitting the field preserves existing explicit completion edges.

At preflight and before first affected dispatch, use the applicable current
contract and accepted clarifications. Reuse a verified revision for both
consumers while it remains current. When a change or recovery calls its
applicability into question, refresh only the affected evidence. The coordinator
AI judges whether it describes the consuming work's request/response shape,
field meaning, errors, authentication and state behavior where applicable well
enough to implement against Mock data. A document's existence, a child saying
"contract ready", or the provider Issue's status alone is insufficient. Do not
require unrelated API details or deployment evidence for that judgment.

When the accepted contract is usable, promptly dispatch or continue each affected
App/Web owner, subject to slots, hard edges and actual exclusions. Give the owner
the exact contract revision or locator, supported work and any local hold.
Ask the owner to exercise the normal product entry through its actual client
wiring and replace only the relevant network responses with contract-based Mock
data. A standalone component, preview route or bypass of the real client does
not prove that path. Do not wait for the backend Issue to close, merge, deploy
or go live merely to begin this work. Reading an available provider-owned
contract does not authorize consuming its unmerged implementation or changing
the frontend's selected base.

A partial contract gap holds only the work that needs the missing detail.
Admit or continue the same frontend owner for independently supported work,
with a precise hold on the affected part. If no permitted work can proceed,
leave an unadmitted node waiting, or safely block an admitted owner under the
normal slot rules. Request the concrete missing contract detail from its
existing provider owner within current delegation; do not create another owner
or widen the run. Pending contract production by a selected eligible provider
is a schedulable wait, not by itself an invalid graph or a whole-run block.
Identify the producer's expected result and when to recheck it. Ask the original
owner to report the changed contract and its locator when it becomes available.
A dry-run states the first ready set, pending contract work and recheck
condition. If no supported producer or ready work can advance, use the existing
preflight or runtime blocked route with the exact missing condition.

If a contract changes or becomes unavailable, revalidate only the work that
uses the changed or missing part. Preserve completed work and keep unaffected
work moving under the failure policy. Provider implementation failure, reopening
or an incomplete deployment does not invalidate an independently usable
contract. Conversely, provider completion does not prove contract sufficiency.
Contract readiness and Mock progress never release a completion edge or prove
real integration, joint acceptance or Issue completion. Current accepted scope
still owns acceptance, integration-test and control-Issue responsibilities.

## Target Business Readiness And Acceptance Preparation

For a required real integration segment, use the accepted target environment
and the original owner's evidence that the relevant business operation works
there with the required identity, route, sample and business result. A merge,
deployment, health check, anonymous authentication response or technical smoke
does not establish this. Do not infer readiness for another operation from one
successful call. When the evidence is current and applicable, promptly dispatch
or continue the affected segment on its existing owner and within existing
slot and authority limits. Do not wait for provider Issue closure unless a
hard edge requires it. Readiness starts integration; only actual accepted
end-to-end evidence can establish joint acceptance.

If the target or tested operation materially changes, reassess only the
affected real integration. Keep unaffected results and Mock work. Have the
original owner report the next bounded recheck condition when readiness is missing.

At startup, identify from accepted scope the actual target environment and
access path, release owner, normal entry and build, and any required account,
sample or effective-time input. Give each unresolved item to its existing
responsible owner for preparation in parallel with independent work. Keep only
the affected work, missing condition, owner and next observable result in the
conversation. Do not copy credentials. This preparation is not a launch gate
or an extra acceptance obligation. Hold only the segment that needs a missing
input; a target business-path failure does not hold contract Mock or unrelated
work. Deployment, environment writes and other effects keep their existing
authorization. In a dry-run, report preparation needs without dispatching them.

## DAG Observation

Use the shared native observation bounds and timer migration. Use compact
native batches with each child's host and cursor. Make an immediate snapshot
for a new formal binding. Reuse the current batch's coverage before a disposition;
snapshot only uncovered targets needed to complete that coverage. Rotate batches
fairly when the platform limit is smaller than the active set.

Treat a timeout as no event, not as a changed child or a new dispatch condition.
On an unchanged batch, continue bounded observation without reopening chat
history, Issue bodies, contracts or resolved dispositions. Check an owned
external condition when its recheck is due or a relevant change is reported,
even if child text did not change. Respect the shared direct-confirmation
profile and its independent-operation readback. A fixed timer, serial short
polls and repeat snapshots do not supplement a covered native wait.

Ask each DAG child to report its changed result, evidence locator, affected
work and next condition with the shared minimal stop report. For a new fact
that affects a decision, consume that owner's decision-relevant delta. Use a
sufficient native result; otherwise read the smallest relevant turn or original
fact. Leave raw logs and full evidence at their owner. Read further only to
resolve a concrete gap, conflict, missed event, recovery or required gate.
Unchanged idle output does not justify sending the same instruction again.
Before a side effect or terminal result, preserve all shared fresh checks and
exact-operation recovery. A changed child result is a reason to verify a gate,
not a pass. Before instructing a merge, verify the required original-owner
results for the exact current candidate under the shared fresh merge gate.
After interruption, recover current binding and facts;
reuse complete current contracts, and reload missing or uncertain text.

## Membership And Repository Bindings

Accept an explicit selected node set or an explicit initiative authority locator.
For an initiative, read its current formal member table/bindings, each member’s
actual role, accepted requirements and completion gates. Follow necessary linked
authority, but do not promote every related link to membership or every reference
to a hard dependency. Preserve the selected set; explain a real membership or
scope conflict before the affected admission.

Distinguish product coordination from engineering delivery by actual duties,
not repository names. For example, product requirements already being ready is
an initial prerequisite fact; a product control Issue’s final acceptance may
wait for the engineering Issues. An engineering reference to those requirements
does not also require final product-Issue completion. Do not manufacture a cycle
by conflating those two obligations. A genuinely contradictory authority returns
to its original scope owner rather than being silently reordered.

Normalize every node, completion edge, contract prerequisite, exclusion and
completion override before graph validation. Canonical Issue URLs and equivalent graph notation may become
`owner/repo#N`. An unqualified integer is usable only with one unambiguous
repository context. Resolve conflicting repository/project/base choices before
affected admission; never guess from the current checkout or a same-number node.

Resolve each repository’s current saved local project, primary repository,
remote and selected base through the shared method. Reuse that binding for its
nodes. Retain per-node formal/pending child, host/cursor, Task/Delivery and PR
associations in this conversation. All observation, merge and completion proof
uses the node’s repository and selected base. There is one global execution slot pool. Each repository has one integration
owner for its selected base and original merge transaction. An unresolved
transaction holds another merge in that same repository; it does not serialize
an independent repository with passing gates and no dependency or actual shared
resource constraint.

## Preflight And Endpoint Compatibility

Apply the same-provider `issue-orchestration.md` shared preflight and AI Gate.
Additionally verify completion-graph membership/acyclicity, each contract's
provider, consuming work and current readiness, feasible positive-integer
concurrency, independent child branches/worktrees and Task/session evidence,
and explicit shared-resource exclusions where required. Apply shared environment
readiness per repository. An initial environment gap holds its nodes and
descendants; it does not make an otherwise valid graph invalid or suppress
independent work under `continue_independent`. Dry-run reports the gap without
provisioning. Global capability/authority gaps still hold all affected work. Exclusion groups
contain only included Issue identities and do not create dependency edges. File overlap alone does not prove
that independent worktrees cannot run in parallel.

Before a DAG dispatch that writes, verify the target's existing Issue/Task,
Delivery, branch and checkout boundary as applicable. Give the child only its
own authorized write scope, including any Task metadata or research it owns.
If another independent candidate owns changes in the registered checkout, use
the target workflow's existing checkout/owner route to isolate the writes or
hold the conflicting segment. Do not write either set into a shared candidate,
move another owner's changes, or create a second owner for the same Issue.
Continue independent work that has a suitable boundary. A separated checkout
does not waive formal Review or change the selected base.

Full Issue completion is the goal. If the human explicitly limits the current
segment to an earlier stage, test every edge against full predecessor completion.
If A must stop at PR publication while B needs A's completed result, report that
specific endpoint/dependency conflict before launch unless A already has fresh
full completion proof. A free slot does not resolve it. Never weaken an edge,
start from an unmerged predecessor branch, or silently drop selected nodes.

## Ready Set And Slots

Maintain these conceptual states in session context:

| State | Meaning |
| --- | --- |
| `waiting` | Not admitted; dependencies, slots, or declared resource exclusions prevent start. |
| `creating` | One creation was attempted; a formal child binding is not resolved yet. |
| `running` | Admitted child is working, awaiting a disposition, integrating, or finishing required closeout. Idle does not release its slot. |
| `blocked` | A concrete unresolved prerequisite or authority prevents bounded continuation; preserve its existing child and resources. |
| `stage_reached` | The explicitly requested earlier endpoint is verified, and the child is inactive at a safe boundary. This node is not `completed` and cannot release a dependency edge. |
| `completed` | All current completion gates pass. |

Calculate eligibility from live proof:

```text
eligible(v) = v has no existing admitted owner
              AND every depends_on predecessor is verified completed
              AND external prerequisites pass
              AND some permitted work has its applicable work-scoped inputs ready
              AND the node’s repository execution environment is verified ready
              AND v is not blocked or a completion descendant of a blocked node
              AND failure policy allows admission
              AND no occupied node shares an exclusive group with v

occupied = creating + running
free = max_parallel - count(occupied)
```

Work-scoped inputs are the applicable contract, target business readiness and
acceptance preparation inputs described above. Work without such a prerequisite
does not wait for it. A partial hold does not mark an otherwise actionable node
blocked. Contract providers do not count as completion predecessors unless
there is also a completion edge. Readiness does not reserve or free a slot:
with `max_parallel: 1`, a running backend still occupies the one slot. Do not
claim simultaneous execution, exceed the limit or manufacture backend completion
to admit the frontend; use the next normally available slot. An already admitted
frontend can resume its ready work within its existing occupied slot.

Admit the earliest eligible nodes until no slot or eligible node remains. Count
a creation attempt before making its tool call. If `free < 0` after recovery,
admit nothing new, observe the existing children, and resolve the mismatch.
Do not cancel work to repair accounting. A verified blocked node releases its
slot only after its child is inactive with a known safe disposition. Its shared
resource reservation remains if unresolved side effects still use that resource.

An earlier-stage node releases its execution slot when its stage proof and
inactive safe disposition are verified, with no unresolved operation. Keep its
existing child and resources. This permits the next independent node to run,
including PR-only runs with `max_parallel: 1`. Do not mark it `completed`,
resume it past the endpoint, or use it to satisfy a dependency. A resource still
in use retains its reservation. Whole-run stage completion follows Endpoint
Verification And Settlement below and the shared settlement method; reaching
the endpoint for one node does not end the run.

For a blocked admitted node to resume, first reacquire a slot and any retained
resource requirement; resume its same child before admitting new eligible nodes
in input order. Never create a second child to resume blocked work.

An exclusion group prevents simultaneous execution, not a fixed completion
order. Do not invent dependency edges to hide resource contention. File overlap
alone does not force whole-Issue serialization: independent worktrees plus
normal base reconciliation may suffice. A genuine acceptance dependency needs
an edge; a proven resource conflict needs an explicit scheduling constraint.

For a fork A -> {B, C}, admit B and C when A completes and slots permit. For
{B, C} -> D, admit D only after both complete. If B -> E and B completes first,
E may start while C is still running. There is no whole-wave barrier.

## Failure Propagation

Temporary model capacity, ordinary gate rework, and an owned bounded external
wait retain their existing owner; they are not permanent node failure.
Use the shared active-unblocking and wait-validity judgments before accepting
a node's block. A failed step or missing recommendation does not by itself
establish a node block or a terminal DAG result. For action authorization,
use `DAG Action Authorization And Handoff` in the same-provider shared method.

For a genuine block, identify the node, failed requirement, and transitive
completion descendants. Those descendants cannot start. Apply work-scoped
prerequisite gaps only to their consuming work. A blocked provider does not
invalidate a current usable contract or an unaffected target operation.
Already completed siblings stay complete
unless current evidence invalidates their own completion.

- `continue_independent`: continue admitted siblings and admit eligible nodes
  outside the blocked subgraph. Apply the shared Quiet Notifications conditions
  when reporting a block or a material change.
- `stop_dispatch`: stop all new admissions on the first genuine block. Let
  existing independent children reach a safe boundary under existing authority,
  then hold them; do not force-cancel or delete their work. Monitor until every
  child has a verified disposition.

A shared repository/tool/authority failure blocks every dependent node, not
just the first child that reports it. Re-evaluate the affected scope from facts.
Never mark a blocked node complete, skip it, or report the whole DAG completed.

If a previously completed predecessor is reopened, reverted, or fails a
required gate, stop new descendants. Give any admitted affected descendants a
scoped hold/revalidation instruction, preserving their work. The original
owners decide what needs rework. Do not auto-rollback unrelated results.

## Endpoint Verification And Settlement

Use the shared method's original-owner stage proof or full Issue completion
proof. Only full completion releases `depends_on` edges. Contract prerequisites
use their own readiness rule and do not establish a stage or completion result.
Use stage proof solely
for the safe slot release above and `dag_stage_completed` below when the human
explicitly limited execution. This existing exit retains its segment-only
meaning; no phase result or authority gap implicitly selects it. Resume the
same Issue owners for the remaining completion obligations when that limit ends.

- `progressing`: unfinished permitted work, a pending creation, an owned wait,
  observation recovery or incomplete safe settlement still requires supervision.
- `dag_stage_completed`: every selected node has reached the explicitly
  human-requested earlier stage; every child and operation is safely settled,
  and native child/operation settlement is verified. State actual remaining Issue/Task work.
- `dag_blocked`: the shared terminal-block test establishes that the requested
  endpoint remains unmet and no legal work can advance. Use its gap, checked
  directions, missing condition and resume explanation for affected nodes and
  descendants; preserve partial results, safely settle children and verify
  native child/operation settlement. Under
  `continue_independent`, first finish all remaining permitted independent work.
- `dag_completed`: every selected node passes fresh full completion proof,
  and all children and operations are safely settled.

For `stop_dispatch`, instruct existing children to hold at the next safe
workflow boundary, and observe them until that boundary is verified. Do not
interrupt a merge or claim a terminal outcome while a child remains active.
Shared settlement failure returns `progressing`, never a false terminal result.

## Public Conversation Contract

The conversation accepts an ordered nonempty `nodes` set, or an explicit
`initiative` authority locator whose formally bound members become that set.
For multi-repository selection, provide `repositories`, keyed by canonical
`owner/repo`; each value may provide `project_path` and `base_branch`. Resolve
omitted paths from actual saved projects and omitted bases from that repository’s
live default. Nodes contain `repository`, positive `issue`, and `depends_on`,
and may add the work-scoped `contract_dependencies` defined above.
Dependencies, `exclusive_groups` and per-node `completion_overrides` use
`owner/repo#N` (or equivalent canonical Issue URLs). All graph references must
resolve unambiguously. Included predecessors refer to selected identities;
external prerequisites use the existing live-proof rule, without expanding scope.

Existing single-repository input remains a shorthand: `repository`,
`project_path`, optional `base_branch`, and integer Issue nodes/edges/overrides
expand into the same repository-qualified graph. There is no second scheduler
or legacy execution path. Multi-repository configuration does not apply one
repository’s base or path to another. Keep this shorthand for existing callers;
removing it requires an explicit breaking change and caller migration.

Both forms accept optional positive-integer `max_parallel` (default 3), `mode`
(dry-run/auto/live; default auto), supported `child_model`/`child_thinking`,
`exclusive_groups`, `completion_overrides`, `failure_policy` (default
continue_independent), and explicit same-run resume selection. Equivalent graph
notation may be normalized in conversation. Carry each resolved repository/base
into child creation, PRs and completion proof under the shared method.
Full Issue completion is the goal. Resolve execution limits and authority only
from the human conversation under the shared method; they are not public data
fields or persistent state. A missing action permission does not select an
earlier-stage goal.

Return exactly one primary exit. Outputs stay in the current conversation;
they are concise action/results for their named consumer, not audit artifacts.
Apply the same-provider shared method's `Quiet Notifications` section to
delivery of these results. Keep routine `auto_started` and `progressing`
results within the active observation loop; a necessary handback preserves their
original next-observation consumer and remaining obligations. The shared timer
migration applies to existing old-run automations only.

| Exit | Minimal output and sole consumer |
| --- | --- |
| `dry_run_ready` | Normalized graph/settings, live identities, gate summary, first ready set, prospective effects and verification limits; dry-run response to the user. Auto/live consume ready preflight internally rather than emitting another final exit. |
| `dry_run_blocked` | Concrete failed preconditions or missing choice and useful available facts; user resolves them before re-entry. |
| `auto_started` | Admitted Issue/formal or pending chat bindings and its immediate native observation condition; next observation cycle in this coordinator. |
| `progressing` | Changed node results, concrete blockers or incomplete settlement, and next observation condition; next coordinator cycle. |
| `dag_blocked` | Incomplete nodes, concrete blockers and descendants, partial results and verified child/operation disposition. For each environment gap, include the exact repository and checkout path/remote, concrete supported user steps to establish the checkout/project/primary folder or complete the displayed trust review, and what will be reread before same-run resume; the user consumes those steps to resolve the block. |
| `dag_stage_completed` | Per-node original-owner stage evidence, unfinished Issue/Task work and safe child/operation settlement; user receives the requested stage result. |
| `dag_completed` | Per-Issue verified delivery, applicable release identity, validation limits and verified safe operation settlement; user receives final completion. |

Unknown, multiple or unmapped exits stop here. Do not import `chain_*` outcomes
or the sequence's one-child invariant.
