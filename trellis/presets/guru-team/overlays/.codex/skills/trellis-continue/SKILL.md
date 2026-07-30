---
name: trellis-continue
description: "Advance the current Guru Team task through planning, implementation, review, and publication readiness using the canonical workflow."
---

<!-- guru-team-overlay: v1 -->

# Guru Team Trellis Continue

Read current state instead of replaying remembered steps:

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

Use `.trellis/workflow.md` as the global route and load each mandatory owner by
stable Skill id. This entry never copies a package schema, evidence recipe,
review loop, confirmation algorithm, or typed-exit payload.

## Route

- `planning`: complete the task's proportionate planning documents and Docs
  SSOT decision, then invoke `guru-approve-task-plan`. The owner decides whether
  revision, clarification, or user approval is required. Only `approved` may
  transition the task to `in_progress`.
- `in_progress`: validate the workspace and current planning approval, then
  implement and run `guru-check-task`. Agent terminal output is ephemeral input
  to the final Phase 2 judgment; do not create a separate
  `implementation-handoff.md`. Persist only the final checker-passed Phase 2
  result. Batch qualified findings before another check and commit cycle.
- after Phase 2: invoke `guru-create-task-commit`, then
  `guru-review-branch`. Automatically consume declared revision and finding
  routes; stop only for missing authority, unresolved scope, or a real blocker.
- after Branch Review `passed`: author the current `pr-body.md` and
  `finish-summary-index.json`, invoke `guru-review-task-publication`, and
  automatically consume its internal metadata-revision route. `ready` means the
  task may enter the explicit finalization entry.

## Interaction Budget

Do not expose internal digests, recorder steps, `verification_required`,
`resume_finalization`, or other machine routes as user decisions. Ask the user
only for missing intent, a material scope/plan choice, new external authority,
or the bounded publication/finalization side effects. A generic
`确认继续` must never be required between automatically mapped Skill exits.
When one current, unique side effect has been fully displayed, use `确认继续` as
the prompt and accept any clear affirmative reply; never require the user to
repeat a SHA, digest, or prescribed sentence. Reconfirm only after plan, HEAD,
target, scope, or authority changes.

## Evidence And Recovery

Use live source, planning, diff, tests, terminal results, and current owner gates
directly. Do not transcribe the same facts into handoff or liveness prose.
Platform wait timeouts are observations, not failures. Persist recovery evidence
only when an unfinished agent is actually replaced, using the private
`record-agent-recovery.sh` / `check-agent-recovery.sh` checkpoint; otherwise
the completed terminal result is sufficient input to the semantic owner.

Before a planning, review, or publication stop, run:

```bash
.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task <task-path>
```

Show only the human-authored artifacts that exist. JSON gates remain internal.
All task paths must resolve inside the task worktree. This entry never stages,
commits, pushes, creates a PR, archives a task, or invokes finalization itself.
