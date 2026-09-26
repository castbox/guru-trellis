---
name: guru-activate-task
description: Activate an approved planning task through current lifecycle and base facts, with read-only output-loss recovery.
---

# Activate Task

This semantic owner consumes a fresh `guru-approve-task-plan:approved` result,
the current task lifecycle, selected base continuity, and the current session
outcome. Review the exact planning artifacts and acceptance before invocation;
the recorder cannot approve a plan. A changed plan or base returns to its
owner. The only task mutation is `planning -> in_progress`, with no legacy
branch/path field written. Do not call the old `task.py start` status writer.

Use `scripts/invoke.sh --root <task-checkout> --input -` with the reviewed
structured input. If output is lost after the transition, invoke the
`recover_activation` profile: it rereads the same lifecycle and continuity
without writing the task again. Carry `planning_result_id` verbatim from the
checked `guru-approve-task-plan:approved` DTO; never recompute it while building
Activation input. It is a content identity, not approval authority: it must
equal the digest of the current `prd.md`, `design.md`, and `implement.md`. The approved
typed exit is the semantic prerequisite; its private checkpoint is retired by
that producer and is never read by Activation. Return exactly one declared
typed exit.
