---
name: guru-orchestrate-issue-dag
description: Explicitly coordinate a GitHub Issue dependency graph across Codex chats and worktrees, with bounded parallel execution, heartbeat supervision and live endpoint proof. Invoke by name for DAG, fan-out or fan-in orchestration. Discussing this Skill, drawing a graph or requesting a dry-run does not start execution. Single-Issue workflow stages retain their original owners.
---

# Guru Issue DAG Orchestrator

`judgment_mode=semantic`. This standalone Codex Skill owns one repository's
cross-Issue DAG. The coordinator reads live evidence, schedules eligible nodes,
judges progress and proves the requested endpoint. Each Issue has its own child
chat/worktree and executes the target repository's complete current workflow.
The coordinator does not implement Issues or enter a single-Issue workflow phase.

## Load The Same-Provider Contracts

Resolve the complete Guru source or installation providing this Skill. Before
substantive output, fully read its `clear-technical-writing.md`. The source spec
root is `trellis/presets/guru-team/spec/workflow`; the installed root is
`.trellis/spec/workflow`. Until loading succeeds, give only a short progress or
missing-file diagnostic. After recovery, load it and continue without new approval.

Before preflight, live execution, every heartbeat or recovery, read that same
provider's `issue-orchestration.md` in full and this package's
[complete DAG contract](references/dag-contract.md). Package-local references
come from `trellis/skills/guru-team/packages/guru-orchestrate-issue-dag` in source
or `.trellis/guru-team/skills/packages/guru-orchestrate-issue-dag` after installation.
A discovery projection is only an entry locator. Do not mix providers or use a
historical personal copy. The target repository may be elsewhere and need not
install these orchestration Skills.

The shared method exclusively defines endpoint interpretation, current-dialogue
authority, child operation, heartbeat, continuation, merge/completion proof and
supported recovery. Apply it at startup, resume and child continuation alike.
The local contract owns graph normalization, eligibility, slots, exclusion,
failure propagation, stage settlement and this Skill's public I/O.

## Execute The DAG

1. Resolve the conversation inputs from the local contract. Normalize equivalent
   edge notation; `A -> B` means B waits for A's full completion. Input order
   breaks ties among eligible nodes, never creates implicit edges. Clarify only
   actual ambiguous dependencies or choices before affected admission.
2. Perform the shared read-only preflight and AI Gate for the entire graph.
   Verify acyclicity, hard prerequisites, exclusions and endpoint compatibility.
   A dry-run returns `dry_run_ready|dry_run_blocked` and stops. Auto/live consume
   ready preflight internally and launch only within current human instructions.
3. Start or recover the one native current-chat heartbeat, default every two
   minutes. Recompute eligibility; reserve each slot before creating its child.
   Preserve pending bindings and immediately observe each newly formal child.
   Fill available slots without creating blocked descendants or duplicate owners.
4. Observe every admitted unfinished node each cycle under the shared method.
   Give each actionable idle node one current disposition. Keep sibling work
   moving; one busy child, merge or repair cannot starve other observations.
5. Verify full completion before releasing any dependency. A join waits for all
   predecessors. Refill a free slot immediately when an eligible node exists;
   do not impose a wave barrier. An earlier requested stage frees only the
   execution slot under local rules, never a hard dependency edge.
6. Recheck current live facts and semantic sufficiency, settle under the local
   contract, validate child/operation/heartbeat facts with native tools, and
   return exactly one declared exit. Tool status never substitutes for AI judgment.

## Exits

The [public conversation contract](references/dag-contract.md#public-conversation-contract)
owns the minimal output and sole consumer for `dry_run_ready`,
`dry_run_blocked`, `auto_started`, `progressing`, `dag_blocked`,
`dag_stage_completed`, and `dag_completed`. Unknown or multiple exits stop.

Use [graph examples](references/examples.md) only as illustrative inputs.
Instruction-only execution creates no coordinator Task, script, status artifact,
schema, authorization record or persistent checkpoint. Child evidence and
semantic gates stay with the target repository's original owners.
