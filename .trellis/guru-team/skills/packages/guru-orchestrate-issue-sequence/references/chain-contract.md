# Strict Serial Chain Contract

## Input And Order

Normalize in the current conversation:

| Input | Contract |
| --- | --- |
| `repository` | Exact GitHub `owner/repo`; one repository per run. |
| `project_path` | Absolute path to its current saved local Codex project. |
| `issues` | Ordered nonempty list of unique positive Issue numbers; arbitrary length 1..N. |
| `mode` | `dry-run`, `auto` or `live`; omitted means `auto`. |
| `child_model`, `child_thinking` | Exact current supported settings, resolved before live effects under the shared method. |
| `completion_overrides` | Optional per-Issue accepted extra gates, such as exact published tag, Release, package or smoke. |
| `coordinator_role` | `coordinator` in this chat; no extra coordinator chat is created. |
| `resume` | Optional explicit recovery/adoption selection; fresh ownership and completion proof are required. |

Preserve supplied order exactly. Numeric order and example length add no
requirements. Endpoint and authority are read only from actual human messages
under the shared `issue-orchestration.md`; they are not normalized data fields.

The current Issue is the earliest selected Issue without fresh full completion
proof. Keep one child or pending creation for it. A current child waiting on a
phase, merge, repair, release, closeout or external operation still owns that
position. Do not pre-create, bind or begin a later Issue as a convenience.

## Dependencies And Preflight

Apply the shared whole-run read-only preflight and AI Gate. For each referenced
predecessor classify current accepted meaning: hard completion prerequisite,
preferred order, informational context or superseded. Only accepted hard
prerequisites constrain readiness; preserve the user's explicit strict order.
Do not revive superseded references as gates.

An included hard predecessor must occur earlier in the chain or already have
fresh full completion proof. An external hard predecessor must independently
pass the same current proof before launch and be rechecked before admission.
If the supplied order contradicts a live prerequisite, report the exact conflict
before creating a child or heartbeat. Do not reorder, add or skip Issues silently.

Detect overlap by selected `repository + Issue`, including coordinators with
different lists or ordering. Current context must prove ownership; a similar
title alone is insufficient. An unrelated active Task is not a current conflict.
On resume, recover the original child/Task/Delivery instead of creating a duplicate.

## Earlier Endpoint Compatibility

Resolve the actual human endpoint before launch using the shared method.
This Skill's strict complete-before-next rule remains in force for every step.
An earlier-stage result, including a reviewed ready PR, does not release the
next sequence position even when the Issues have no technical dependency.

A requested earlier endpoint is compatible when every selected Issue before
the last has already passed fresh full completion proof and the last selected
Issue is the only remaining work item. A single-Issue chain is the simplest
case. Verify the remaining Issue's requested stage and safe inactive disposition,
then use `chain_stage_completed`; do not claim full Issue completion.

If the human asks for an earlier endpoint for multiple still-incomplete Issues,
show the concrete conflict during preflight. For example, “publish PRs for A
then B without merging A” cannot satisfy this strict serial contract. Ask only
whether to change the endpoint/selection or explicitly choose an appropriate
DAG run; do not silently switch Skills, weaken advancement or start A first
while postponing the decision. Return `dry_run_blocked` while unresolved.

If the human changes the endpoint during a live run, assess the remaining
selection through the same rule. Hold affected mutations and report a genuine
choice. Keep already admitted work safe and retain its owner; do not present
completion of only a prefix as stage completion for the whole selected chain.

## Serial Advancement And Failure

Use the shared method for child creation, async result recovery and progress
dispositions. Creation occupies the current position before its tool call. An
unresolved result never permits another creation. Bind the formal child and
immediately snapshot it; later waits retain its own cursor.

Fresh full Issue completion proof is the sole advancement gate. Check its
required Task closeout and every accepted override, including published-version
proof for a release Issue. Verify the platform's actual resulting commits for
squash/rebase, rather than requiring the old feature HEAD to be an ancestor.
Only after that proof may the coordinator create or adopt the next Issue child.

When the remote base evolves, use the current child's original reconciliation
owner and refresh affected gates. A reported complete/completed status, a merge
alone or a closed Issue without correct delivery does not release the position.

Ordinary rework, supported recovery, pending creation and bounded waits retain
the current owner. Temporary model capacity retries preserve the same child
and settings under the shared rule. A genuine block stops serial advancement;
never skip to a later Issue. There is no `continue_independent` policy here.

## Settlement

Apply the shared safe settlement and heartbeat-stop proof. A terminal result
requires inactive safely disposed children, no unresolved creation or operation,
and verified stopped heartbeat. Until those facts pass, return `progressing`
with the exact unfinished settlement rather than claiming a terminal outcome.

- `chain_completed`: all selected Issues freshly satisfy full completion proof.
- `chain_stage_completed`: the earlier-endpoint compatibility rule holds; all
  prior selected Issues are fully complete and the last selected Issue reaches
  the explicitly requested earlier stage. State its remaining Issue/Task work.
- `chain_blocked`: the requested endpoint remains unmet, a concrete prerequisite
  or missing choice has no supported current continuation, and the current
  child has a verified safe disposition. Report the exact block and partial
  completed results. A child's “waiting for confirmation” text alone is no block.

Resume the same chain after the concrete blocker is resolved. Recover the
current position, exact child and current proofs. Do not ask again for existing
recoverable delegation or broaden it from an assistant statement. No later Issue
starts merely because the heartbeat was restarted.

## Public Conversation Contract

Return exactly one primary exit, directly in the current conversation. These
outputs are action/results for their sole consumer, not persistent artifacts.
The stage exit is additive; `chain_completed` retains full-completion meaning.

| Exit | Minimal output and sole consumer |
| --- | --- |
| `dry_run_ready` | Normalized chain/settings, live identities, per-Issue gate/dependency summary, first current Issue, prospective effects and limits; dry-run response to the user. Auto/live consume ready preflight internally rather than emitting another final exit. |
| `dry_run_blocked` | Actual failed preconditions or missing choice with useful available facts; user resolves them before same-chain preflight re-entry. |
| `auto_started` | Current Issue/formal or pending child binding and heartbeat identity; next observation cycle in this coordinator. |
| `progressing` | Changed current-Issue result, exact remaining prerequisite/settlement and next observation condition; next coordinator cycle. |
| `chain_blocked` | Current Issue, genuine blocker, completed prefix, remaining Issues and verified child/heartbeat disposition; user resolves it before same-chain resume. |
| `chain_stage_completed` | Fully completed prefix, last Issue's stage proof, its remaining Issue/Task work and safe child/heartbeat settlement; user receives the requested stage result. |
| `chain_completed` | Per-Issue verified delivery, applicable release identity, validation limits and heartbeat stop; user receives full completion. |

Unknown, multiple or unmapped exits stop here. Do not import `dag_*` outcomes
or allow DAG slot rules to weaken strict serial advancement.
