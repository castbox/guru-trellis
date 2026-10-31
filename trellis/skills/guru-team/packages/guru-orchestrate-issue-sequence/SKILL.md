---
name: guru-orchestrate-issue-sequence
description: Explicitly coordinate an ordered GitHub Issue chain across separate Codex chats and worktrees. Invoke by name when each Issue must fully finish before the next begins, with heartbeat supervision and live completion proof. Do not use implicitly or for unordered parallel work. Discussing the Skill or requesting a dry-run does not launch execution.
---

# Guru Issue Sequence Orchestrator

`judgment_mode=semantic`. This standalone Codex Skill owns one repository's
strictly ordered Issue chain. Keep at most one current Issue child, including
pending creation. Complete and verify that Issue before creating or adopting
the next. The coordinator judges progress and endpoint proof; it does not
implement Issues or replace their repository workflow.

## Load The Same-Provider Contracts

Resolve the complete Guru source or installation providing this Skill. Before
substantive output, fully read its `clear-technical-writing.md`. The source spec
root is `trellis/presets/guru-team/spec/workflow`; the installed root is
`.trellis/spec/workflow`. Until loading succeeds, give only a short progress or
missing-file diagnostic. After recovery, load it and continue without new approval.

Before preflight, live execution, every heartbeat or recovery, read that same
provider's `issue-orchestration.md` in full and this package's
[complete chain contract](references/chain-contract.md). Package-local references
come from `trellis/skills/guru-team/packages/guru-orchestrate-issue-sequence` in
source or `.trellis/guru-team/skills/packages/guru-orchestrate-issue-sequence`
after installation. A discovery projection is only an entry locator. Do not
mix providers or use a historical personal copy. The target repository may be
elsewhere and need not install these orchestration Skills.

The shared method exclusively defines endpoint interpretation, current-dialogue
authority, child operation, heartbeat, continuation, merge/completion proof and
supported recovery. Apply it at startup, resume and child continuation alike.
The local contract owns exact order, dependency compatibility, serial
advancement, earlier-stage disposition and this Skill's public I/O.

## Execute The Sequence

1. Resolve the conversation inputs from the local contract. Preserve the exact
   nonempty Issue order; identify current hard dependencies from live sources.
2. Perform the shared read-only preflight and AI Gate for the whole chain.
   Resolve the actual human endpoint before launch. Check that it fits strict
   complete-before-next advancement. A dry-run returns its one ready/blocked
   result and stops; auto/live consume ready preflight internally.
3. Start or recover the one native current-chat heartbeat, default every two
   minutes. Create only the current Issue child, or recover its exact existing
   owner. Preserve pending creation; immediately observe each newly formal child.
4. Apply the shared observation and progress method to that same child on every
   cycle. A phase transition, supported recovery, merge or temporary capacity
   error does not permit creating a later Issue. Give an actionable idle child
   one useful disposition instead of waiting for fixed wording.
5. Prove the current Issue fully complete through the shared method, including
   required closeout and accepted overrides. Only then advance to the next
   Issue. An earlier-stage result never satisfies this advancement gate.
6. Recheck semantic sufficiency and current live facts. Settle using the local
   contract and native child/operation/heartbeat validation, then return exactly
   one declared exit. Tool status never substitutes for AI judgment.

## Exits

The [public conversation contract](references/chain-contract.md#public-conversation-contract)
owns the minimal output and sole consumer for `dry_run_ready`,
`dry_run_blocked`, `auto_started`, `progressing`, `chain_blocked`,
`chain_stage_completed`, and `chain_completed`. Unknown or multiple exits stop.

Instruction-only execution creates no coordinator Task, script, status artifact,
schema, authorization record or persistent checkpoint. Shared recovery requires
an original-owner supported route; this Skill grants no general permission to
bypass defective workflow machinery. Child evidence and semantic gates remain
with the target repository's original owners.
