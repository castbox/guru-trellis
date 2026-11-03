# DAG Contract

## Graph And Live Dependency Authority

An Issue is a node. `depends_on: [A, B]` means that both A and B must satisfy
their complete completion contracts before this node can start. An edge is a
completion dependency, not permission to start from an unmerged branch.

Normalize graph input in the conversation. Require unique positive Issue
numbers, included predecessor identities, no self-edge, and no directed cycle. Repeated edges
may be collapsed without changing meaning. Report a concrete cycle path when
one exists. Preserve node input order as the ready-set tie-breaker, never as an
implicit dependency. A serial list must explicitly become adjacent edges.

Read live Issue bodies, accepted maintainer comments, linked PRs, and repository
workflow. Classify referenced predecessors as hard, delivery-order preference,
informational, or superseded. Only accepted hard dependencies constrain
eligibility. The user's explicit graph may add an ordering preference; it may
not remove a live hard prerequisite. Do not revive superseded references.

If an included hard predecessor is missing an edge, show the required edge and
resolve the graph discrepancy before launch. If a hard prerequisite is outside
the selected nodes, verify its completion directly and recheck it before the
dependent node starts. An incomplete external prerequisite blocks that node;
do not silently add another Issue, remove the prerequisite, or widen the run.
If it is already incomplete at initial preflight, return `dry_run_blocked`.
If it becomes unsatisfied after launch, apply the runtime failure policy.

Conflicting product or architecture authority needs a human decision. A stale
child summary is a discovery hint, not a change to accepted Issue scope.

## Preflight And Endpoint Compatibility

Apply the same-provider `issue-orchestration.md` shared preflight and AI Gate.
Additionally verify graph membership/acyclicity, feasible positive-integer
concurrency, independent child branches/worktrees and Task/session evidence,
and explicit shared-resource exclusions where required. Exclusion groups
contain only included Issue identities and do not create dependency edges. File overlap alone does not prove
that independent worktrees cannot run in parallel.

For an earlier endpoint, test every edge against full predecessor completion.
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
              AND every predecessor is verified completed
              AND external prerequisites pass
              AND v is not blocked or descended from a blocked node
              AND failure policy allows admission
              AND no occupied node shares an exclusive group with v

occupied = creating + running
free = max_parallel - count(occupied)
```

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

For a genuine block, identify the node, failed requirement, and transitive
descendants. Descendants cannot start. Already completed siblings stay complete
unless current evidence invalidates their own completion.

- `continue_independent`: continue admitted siblings and admit eligible nodes
  outside the blocked subgraph. Report the block once, then meaningful changes.
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
proof. Only full completion releases dependency edges. Use stage proof solely
for the safe slot release above and `dag_stage_completed` below.

- `progressing`: unfinished permitted work, a pending creation, an owned wait,
  observation recovery or incomplete safe settlement still requires supervision.
- `dag_stage_completed`: every selected node has reached the explicitly
  human-requested earlier stage; every child and operation is safely settled,
  and heartbeat stop is verified. State actual remaining Issue/Task work.
- `dag_blocked`: the requested endpoint remains unmet and no legal work can
  advance. Identify concrete blocks and affected descendants, preserve partial
  results, safely settle children and verify heartbeat stop. Under
  `continue_independent`, first finish all remaining permitted independent work.
- `dag_completed`: every selected node passes fresh full completion proof,
  and all children, operations and heartbeat are safely settled.

For `stop_dispatch`, instruct existing children to hold at the next safe
workflow boundary, and observe them until that boundary is verified. Do not
interrupt a merge or claim a terminal outcome while a child remains active.
Shared settlement failure returns `progressing`, never a false terminal result.

## Public Conversation Contract

The input is one repository and saved project path, ordered nonempty `nodes`
with unique positive `issue` and included `depends_on` predecessors, optional
positive-integer `max_parallel` (default 3), `mode` (dry-run/auto/live; default auto),
optional native `child_model`/`child_thinking`, per-Issue `completion_overrides`,
`exclusive_groups`, `failure_policy` (default continue_independent), and explicit
resume selection. Equivalent graph notation may be normalized in conversation.
Resolve endpoint and authority only from the human conversation under the shared
method; they are not public data fields or persistent state.

Return exactly one primary exit. Outputs stay in the current conversation;
they are concise action/results for their named consumer, not audit artifacts.

| Exit | Minimal output and sole consumer |
| --- | --- |
| `dry_run_ready` | Normalized graph/settings, live identities, gate summary, first ready set, prospective effects and verification limits; dry-run response to the user. Auto/live consume ready preflight internally rather than emitting another final exit. |
| `dry_run_blocked` | Concrete failed preconditions or missing choice and useful available facts; user resolves them before re-entry. |
| `auto_started` | Admitted Issue/formal or pending chat bindings and heartbeat identity; next observation cycle in this coordinator. |
| `progressing` | Changed node results, concrete blockers or incomplete settlement, and next observation condition; next coordinator cycle. |
| `dag_blocked` | Incomplete nodes, concrete blockers and descendants, partial results and verified child/heartbeat disposition; user resolves the block before same-run resume. |
| `dag_stage_completed` | Per-node original-owner stage evidence, unfinished Issue/Task work and safe child/heartbeat settlement; user receives the requested stage result. |
| `dag_completed` | Per-Issue verified delivery, applicable release identity, validation limits and verified heartbeat stop; user receives final completion. |

Unknown, multiple or unmapped exits stop here. Do not import `chain_*` outcomes
or the sequence's one-child invariant.
