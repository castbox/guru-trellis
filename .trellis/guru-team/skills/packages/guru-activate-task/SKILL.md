---
name: guru-activate-task
description: Activate initial planning or resume approved active replanning, with same-operation read-only result recovery.
---

# Activate Task

`judgment_mode=semantic`. Workflow and standalone invocations use the same
entry checks and ordered profile: forward behavior -> AI Review Gate ->
conditional human confirmation -> recorder/validator -> one typed exit.

## Entry and forward behavior

For pending `activate` or `resume_execution`, consume the actual fresh
`guru-approve-task-plan:approved` DTO, current planning artifacts,
TaskId/generation/TaskRef, current C4 branch/resource ownership, selected-base
continuity from the `task_activation` pair guard, and current C5 session outcome.
For read-only result recovery, use the actual completed operation through this
owner and current lifecycle/session facts; the original DTO may have been lost.
A changed plan or base returns to its existing owner; a content token alone
never establishes a semantic pass.

Select the operation from the current lifecycle and the actual completed
operation. `activate` accepts only `planning` and changes only
`planning -> in_progress`; do not call the old `task.py start` writer.
`resume_execution` accepts only `in_progress` and consumes a newly reviewed
active plan without changing task metadata, TaskId, generation, branch,
checkout or resource ownership. It is neither a new task nor another first
activation. Do not use `recover_activation` to consume a new active plan.

Reread the official current session record through the binding owner's
current-branch checkout scope for every operation. A retained old checkout can
contain the same task artifact but is not a second current route. Declared
`session_bound` must resolve the exact TaskId, generation and TaskRef;
`explicit_task_mode` requires no available context key. Missing, stale or
switched session state returns to the session-binding owner.

## AI Review Gate and real acceptance boundary

Distinguish initial activation, new active replanning and same-operation
recovery. For pending activation/resume, review current requirement authority,
scope, the complete current plan and the actual Planning DTO. Present the current planning bundle and exact proposed
activation or execution-resume action, then wait for a clear affirmative reply
made after that presentation. Earlier task creation or execution acceptance
does not accept a new plan. Run the current `task_activation` pair guard after
that acceptance. These judgments and the reply stay in the dialogue; scripts
never receive or persist them. Lost or stale semantic DTOs return to Planning
for fresh review. If current-dialogue acceptance cannot be established before
a pending execution handoff, repeat the presentation and acceptance boundary.

For an already completed operation whose stdout was lost, review its current
identity and choose the corresponding read-only recovery. Recovery has no new
status/plan side effect and does not repeat a completed acceptance boundary.

## Recorder/validator and local result lifecycle

Use `scripts/invoke.sh --root <task-checkout> --input -`. Carry
`planning_result_id` verbatim from the actual approved DTO, never recompute it
while authoring `activate` or `resume_execution` input. The validator compares that content identity
with current `prd.md`, `design.md` and `implement.md`; it is not approval
or acceptance authority. Planning retires its own private checkpoint; this
owner never reads it.

After a completed `activate` or `resume_execution`, this owner records one
ignored, short-lived `execution-result.json` below its task owner-checkpoint
directory. It contains only operation, current planning identity, lifecycle
identity, branch-binding revision and execution continuity. It contains no
review conclusion, acceptance, process history or timestamps. A new completed
operation replaces the earlier result, without creating a result chain.

`recover_execution` has a distinct identity-only input: TaskId, TaskRef,
generation and current session mode. If both stdout and the original invocation
input or approved DTO were lost, the caller still supplies only those live
identities; it never rebuilds a Planning token. The original owner reads its
own completed `resume_execution` result to restore planning/continuity inputs,
then validates exact current planning, lifecycle, C4/C5 and continuity. It returns the same
`execution_resumed` output without rewriting task metadata or checkpoint bytes.
`recover_activation` keeps its published initial-transition recovery semantics
and pre-468 no-checkpoint compatibility; a retained resume result cannot be
relabeled as an initial activation. Missing completed resume evidence returns
to fresh Planning. Normal mismatches retain the result for its owner and
return the declared refresh or stop, never reconstruct semantic approval.

The direct consumers are same-owner output-loss recovery and the current
Phase 2 handoff/Check. After Check validates its own current producer checkpoint
and `passed` output, it calls the original owner port
`runtime/execution_result.py:retire_execution_result(root, task_ref=...)`.
The port rereads the authoritative task identity, planning, C4/resource pair,
unique current checkout and continuity itself; Check never reads this private
record. Absent pre-468 results and ordinary stale results return `False`
without blocking an otherwise current Check; stale bytes remain. A current
consumed result returns `True` and is deleted with its empty owner directory.
No permanent receipt, ledger or tracked gate artifact is created.

## Typed exits and controlled migration

Return exactly one declared exit: `activated` goes to
`guru-task-activated-router`; `execution_resumed` goes to
`guru-task-execution-resumed-router`; `refresh_review` goes to the existing
activation refresh router; `invalid_task_state` and `blocked` have their
existing fail-closed stops. Both successful routers hand the same minimal
TaskId/TaskRef/generation to Phase 2 execution.

Issue #468 migrates the single aggregate input/output schemas to 2.0 and
updates controlled workflow/interface consumers in place. Existing
`activate`/`recover_activation` payload shapes and `activated` 1.0 output
remain accepted with their original meanings; new actions are
`resume_execution`/`recover_execution`, with an independent
`execution_resumed` 1.0 output. There is one parser and no legacy fallback,
new Skill, lifecycle status or source authority.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
